# Manage your environment variables

## Theory

Environment variables are a standard way to inject configuration and secrets (API keys, DB credentials) without hardcoding them.
They matter because leaked `.env` files are a top cause of credential exposure — so handling, rotation, and scoping need care.
Key subtopics: `.env` files vs secret managers, never committing secrets, per-environment overrides, and validating required vars at startup.

> Scope note: this page is the interview-ready guide to environment variables and secret injection —
> `.env` files vs secret managers, 12-factor config, Spring externalized configuration, rotation,
> startup validation, and leak prevention. Deep identity, transport, and pipeline mechanics live in
> linked pages (authentication, encryption, certificates, DevSecOps). It assumes basic deploys and
> focuses on decisions interviewers probe: where secrets live, how they rotate, and how they never leak.

### Topics Covered

1. [.env Files vs Secret Managers](#1-env-files-vs-secret-managers)
2. [Twelve-Factor Config and Spring Externalized Configuration](#2-twelve-factor-config-and-spring-externalized-configuration)
3. [Rotation and Startup Validation](#3-rotation-and-startup-validation)
4. [Leak Prevention Git History CI Masking and Pre-commit](#4-leak-prevention-git-history-ci-masking-and-pre-commit)
5. [Threats and Mitigations](#5-threats-and-mitigations)
6. [Per-Environment Scoping and Overrides](#6-per-environment-scoping-and-overrides)
7. [Best Practices](#7-best-practices)
8. [Interview Questions and Answers](#8-interview-questions-and-answers)

### 1. .env Files vs Secret Managers

A `.env` file is a local key-value file loaded into process environment at boot, convenient for
development but a plain file on disk with no encryption, audit, or rotation. A secret manager
(AWS Secrets Manager, HashiCorp Vault, GCP Secret Manager, Azure Key Vault, Doppler, Infisical)
is a service that stores encrypted secrets, injects them at runtime, versions every read and
write, and rotates values without redeploying code. Interviews expect you to place each on the
correct side of the dev-versus-prod line and defend the boundary.

Use `.env` for local development defaults that are non-sensitive or dummy values: ports, feature
flags, local database URLs with throwaway passwords. Use a manager for anything real: production
database passwords, API keys, signing keys, TLS private keys, OAuth client secrets, and any
credential whose leak pages someone at 3 AM. The rule interviewers want to hear is simple: if
revoking it would hurt, it does not belong in a file that can be copied, screenshotted, or
committed by accident.

The failure mode of `.env` is that it looks like configuration but behaves like a secret dump.
Developers share it over Slack, copy it into Docker images, mount it into containers with broad
permissions, and commit `.env.example` that slowly drifts into `.env` with real values. There is
no who-read-what trail, no per-service scoping, and rotation means editing files on every host
and restarting everything by hand. Managers invert each property: encrypted at rest, TLS in
transit, IAM-scoped reads, full audit logs, versioned values, and rotation via API.

| Dimension | `.env` files | Secret managers |
|---|---|---|
| Storage | Plaintext file on disk, readable by any process or user with file access | Encrypted at rest with KMS-backed keys, decrypted only at read time |
| Access control | OS file permissions only, usually `644` and shared | IAM roles per service and environment, least-privilege read policies |
| Audit trail | None, no record of who read or changed a value | Every read, write, and rotation logged with actor and timestamp |
| Rotation | Manual edit plus restart on every host, easy to miss one | API or scheduled rotation, versioned values, dual-password support |
| Scoping | Single flat file, all vars visible to the whole process | Per-service, per-environment, per-version scoping with references |
| Cost and complexity | Zero setup, works offline, ideal for laptops | Network dependency, client setup, caching and fallback design needed |
| Interview verdict | Local dev and tests only, never committed with real values | Production and staging default for every real secret |

A typical hybrid setup shows the intended split. Local boot loads `.env` for convenience while
production injects from the manager and refuses to start without it:

```bash
# Local development: dotenv loads throwaway values, real secrets never live here.
# .env (committed as .env.example only, values are dummies)
DATABASE_URL=postgres://dev:dev@localhost:5432/app
LOG_LEVEL=debug
STRIPE_KEY=dummy_test_key_replace_in_manager
```

```bash
# Production: secrets come from the manager, never from a file in the image.
# ECS / Kubernetes / systemd injects these at boot; the app just reads environ.
export DATABASE_URL="$(aws secretsmanager get-secret-value --secret-id prod/db-url --query SecretString --output text)"
export STRIPE_KEY="$(vault kv get -field=key secret/prod/stripe)"
node server.js
```

The snippets above are explained as the boundary to defend. The local file uses obvious dummy
values so a leak proves nothing and linters can assert no `sk-live` pattern appears. The
production boot reads from the manager over authenticated TLS, so the value never touches git,
chat, or image layers, and rotation is a manager-side version bump plus a restart or reload.
If the manager is unreachable, the process fails closed at startup rather than running with
stale or empty secrets.

### 2. Twelve-Factor Config and Spring Externalized Configuration

Twelve-factor config (factor III) says configuration that varies between deploys must live in
the environment, not in code or checked-in property files. Code plus config equals a release:
the same immutable artifact runs in dev, staging, and prod, and only injected variables change
its behavior. That separation is what lets you promote one Docker image through every stage,
roll back without rebuilding, and scale horizontally without editing files on hosts.

The rule distinguishes config from code cleanly. Anything that changes per environment — database
URLs, API endpoints, credentials, feature flags, ports, log levels — is config and must be
injectable without a rebuild. Anything stable across environments — algorithms, timeouts baked
into SLAs, retry policies reviewed in code — stays in code or versioned defaults. Secrets are a
subset of config with extra handling: encrypted, scoped, audited, and rotated. Interviewers check
that you never justify rebuilding an image just to change a URL or a key.

Spring Boot implements the same idea as externalized configuration with a strict precedence
chain: command-line arguments beat `SPRING_APPLICATION_JSON`, which beats OS environment
variables, which beat `.env`-style `application-{profile}.properties` files. The app reads a
relaxed-binding key like `db.url` from `DB_URL`, `db-url`, or `db.url` interchangeably, so
platform env stores work without Spring-specific syntax. Profiles (`dev`, `staging`, `prod`)
select defaults while the environment always wins for real secrets.

The code below shows the interview-safe Spring pattern: constructor-bound `@ConfigurationProperties`
with validation, never field-injected `@Value` for secrets without defaults:

```java
// Good: type-safe, validated, constructor-bound config. Fails fast on missing secrets.
import jakarta.validation.constraints.NotBlank;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

@Validated
@ConfigurationProperties(prefix = "app.db")
public record DbConfig(
    @NotBlank String url,
    @NotBlank String username,
    @NotBlank String password
) {}
```

The snippet above is explained field by field. The `record` with `final` fields makes config
immutable after binding, so no post-startup mutation can swap a URL under a running pool. The
`@NotBlank` constraints trigger startup failure with a clear message when a variable is missing
instead of a `NullPointerException` at first query time. The `app.db` prefix maps to `APP_DB_URL`,
`APP_DB_USERNAME`, and `APP_DB_PASSWORD` via relaxed binding, which is exactly how container
platforms inject without touching property files.

```java
// Wiring: enable binding and inject the whole config object, not individual strings.
// Application.java
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@EnableConfigurationProperties(DbConfig.class)
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

// Usage: a service depends on DbConfig, making required secrets explicit in the signature.
import javax.sql.DataSource;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DataSourceConfig {
    @Bean
    public DataSource dataSource(DbConfig cfg) {
        // cfg.url(), cfg.username(), cfg.password() already validated as non-blank.
        return buildPooledDataSource(cfg.url(), cfg.username(), cfg.password());
    }

    private DataSource buildPooledDataSource(String url, String user, String pass) {
        // HikariCP or similar: pool sizing itself comes from separate APP_POOL_* vars.
        return null; // replaced with real builder in production code
    }
}
```

The snippet above is explained as the composition to narrate. The `@EnableConfigurationProperties`
registration keeps binding in one place instead of scattered `@Value("${...}")` strings that fail
silently to `null`. Injecting `DbConfig` as a bean makes every secret dependency visible in
constructors, so tests can pass fakes and reviewers can see the full secret surface. The legacy
`@Value("${APP_DB_PASSWORD}")` alternative is discouraged for secrets because it spreads key names
through code, needs repetitive defaults, and skips bean-validation guarantees.

### 3. Rotation and Startup Validation

Rotation replaces a secret with a new value on a schedule or on suspicion of leak, and every
consumer picks it up without downtime or manual file edits. Startup validation refuses to boot
when a required variable is missing or malformed, so misconfiguration fails in deploy logs
instead of as a midnight `NullPointerException`. Interviews pair them deliberately: rotation
tests whether you design for change, validation tests whether you fail fast and loud.

Rotation strategies form a ladder of maturity. Manual rotation means generating a new password,
updating the manager, and restarting services — fine for side projects, unacceptable at scale
because someone always forgets a host. Scheduled rotation runs every 30 to 90 days via the
manager's lambda or Vault dynamic secrets, with versioned values so rollback is one pointer
move. Dynamic or short-lived secrets go further: Vault or RDS IAM auth mints a credential valid
for minutes, so there is nothing long-lived to leak at all. Dual-password support (old plus new
accepted during a window) lets database passwords flip with zero dropped connections.

The Node pattern below shows startup validation every backend should copy: a schema declares
required vars, parses `process.env` once, and exits non-zero with a readable error before any
port opens:

```javascript
// Good: validate once at boot, fail closed with a clear message.
const { z } = require("zod");

const EnvSchema = z.object({
  NODE_ENV: z.enum(["development", "test", "staging", "production"]),
  DATABASE_URL: z.string().url(),          // malformed URL caught here, not at first query
  JWT_SECRET: z.string().min(32),          // short secrets rejected before signing anything
  STRIPE_KEY: z.string().startsWith("sk-"), // wrong-environment key caught immediately
  LOG_LEVEL: z.enum(["debug", "info", "warn", "error"]).default("info"),
});

function loadEnv() {
  const parsed = EnvSchema.safeParse(process.env);
  if (!parsed.success) {
    console.error("Invalid environment:", parsed.error.flatten().fieldErrors);
    process.exit(1); // fail fast: orchestrator retries, alerting fires, no half-boot service
  }
  return parsed.data;
}

const env = loadEnv();
module.exports = { env };
```

The snippet above is explained line by line. The `zod` schema is the single source of truth for
which vars exist and what shape they take, replacing scattered `process.env.X || "default"`
checks that hide missing secrets. URL, length, and prefix constraints catch the classic deploy
bugs: a pasted username instead of a URL, a truncated secret, a test key in production. Exiting
with code 1 before listening lets Kubernetes or ECS mark the deploy failed and keep the old
healthy revision serving, which is exactly the behavior to name in interviews.

The Java equivalent leans on bean validation plus a startup runner that pings dependencies:

```java
// Good: validated properties plus a smoke check before accepting traffic.
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;

@Component
public class StartupValidator implements ApplicationRunner {
    private final DbConfig dbConfig;

    public StartupValidator(DbConfig dbConfig) {
        this.dbConfig = dbConfig;
    }

    @Override
    public void run(ApplicationArguments args) {
        // @NotBlank on DbConfig already rejected blanks; here we check reachability.
        if (!pingDatabase(dbConfig.url())) {
            throw new IllegalStateException(
                "DATABASE unreachable at boot: " + masked(dbConfig.url()));
        }
        // Rotation hook: log the secret version (never the value) so audits trace rollouts.
        System.out.println("Config loaded and validated for url=" + masked(dbConfig.url()));
    }

    private boolean pingDatabase(String url) {
        // Real code: open a connection with a 5s timeout, run SELECT 1, close it.
        return url != null && url.startsWith("jdbc:");
    }

    private String masked(String url) {
        // Never log credentials: strip userinfo before any log line.
        return url.replaceAll("://.*@", "://***@");
    }
}
```

The snippet above is explained as the defense-in-depth pairing. Constructor injection guarantees
the config bean exists and passed validation before this runner executes, so ordering is safe by
framework contract. The ping converts a typo'd host into a crash-loop with a clear log instead
of a service that accepts traffic and fails every request. Masking before logging is the habit
interviewers listen for: even error paths must not echo secrets into log retention.

Rotation without reload design still causes outages, so name the reload mechanism. Poll the
manager every few minutes for version changes, subscribe to rotation events (Secrets Manager
rotation lambda plus SNS, Vault lease expiry), or accept `SIGHUP` to re-read secrets without
dropping connections. Kubernetes users mount secrets as volumes that update atomically and watch
the file timestamp. Whatever the trigger, keep two passwords valid during the window and drain
old connections before revoking — the zero-downtime sentence that closes this answer.

### 4. Leak Prevention Git History CI Masking and Pre-commit

Leaked secrets are forever: git history replicates them to every clone, Docker layers preserve
them even after deletion, and log aggregators retain them for months. Prevention therefore has
three gates — never commit, never print, never bake — each with its own tooling. Interviewers
grade this section by whether you can narrate a leak response, not just prevention.

Gate one is never commit. A root `.gitignore` lists `.env`, `.env.*` (except `.env.example`),
`*.pem`, `*.key`, and `secrets/` directories, and `.env.example` ships only dummy values as the
template new hires copy. A pre-commit hook runs gitleaks or TruffleHog on staged diffs and
rejects pushes matching entropy or pattern rules (AWS keys, `sk-live`, private key headers).
Server-side scanning (GitHub secret scanning plus push protection) blocks even bypassed hooks,
and dependency-era tools like `git-secrets` add provider-specific patterns for AWS and Stripe.

```bash
# .gitignore: block the files that cause 90 percent of secret leaks.
.env
.env.* 
!.env.example
*.pem
*.key
secrets/
```

```yaml
# .pre-commit-config.yaml: scan every commit locally before it reaches the remote.
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.24.0
    hooks:
      - id: gitleaks
        args: ["protect", "--staged", "--verbose"]
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: detect-private-key
```

The snippets above are explained as the two-layer commit gate. The ignore file is the coarse
filter that stops whole files, while the hook is the fine filter that catches a pasted key
inside an otherwise innocent file. Pinning hook revisions keeps scans reproducible across
machines, and `protect --staged` scans exactly what is about to commit rather than the whole
tree. The key interview line: client hooks are conveniences, server push-protection is the
enforcement, and both must exist because `--no-verify` bypasses the first.

Gate two is never print: CI masking and log redaction. CI systems (GitHub Actions, GitLab CI,
Jenkins) mark secret variables as masked so their values render as `***` in job logs, and
workflows must pass them as environment references rather than echoing them into commands.
Application logging adopts the same discipline: structured loggers carry a redaction list for
`password`, `secret`, `token`, `authorization`, and error serializers strip them before emit.

```yaml
# GitHub Actions: secrets referenced, never echoed; masking is automatic.
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy with masked secrets
        env:
          DATABASE_URL: ${{ secrets.PROD_DATABASE_URL }}
          STRIPE_KEY: ${{ secrets.PROD_STRIPE_KEY }}
        run: |
          ./deploy.sh  # scripts must not `echo $STRIPE_KEY` or `env | sort` in CI
```

The snippet above is explained as the print discipline. Referencing `${{ secrets.* }}` keeps
values out of workflow files and lets the platform mask them in output, while passing them as
`env:` avoids shell interpolation into `ps` listings or debug traces. A common follow-up to
volunteer: disable command echo (`set +x`) around secret use and audit `deploy.sh` for stray
`printenv` or verbose curl flags that would undo masking.

Gate three is never bake: secrets stay out of images and bundles. Dockerfiles copy code but
never `.env`, using BuildKit `--mount=type=secret` for build-time keys that vanish from layers,
and multi-stage builds keep deploy images minimal. Frontend bundles get special warning: any
`REACT_APP_*` or `VITE_*` variable ships to browsers, so public keys only, never private ones.

When prevention fails, the response is revoke first, clean second. Revoke and rotate the exposed
credential immediately, check manager audit logs and provider dashboards for anomalous use, then
purge history with `git filter-repo` or BFG plus force-push and expire every clone — deleting
the file in a new commit is not enough because the old blob remains fetchable. File this runbook
beside the rotation one; interviewers award full marks for "revoke, assess, purge, rotate" in
that order.

### 5. Threats and Mitigations

Every environment-variable decision is a threat-model row: an asset the attacker wants, a path
to reach it, and a control that kills the class rather than one instance. The table below is the
whiteboard version to reproduce under pressure, ordered from most to least commonly probed.

| Threat | How it happens | Mitigation (control that kills the class) |
|---|---|---|
| Committed `.env` in git history | `.env` added before `.gitignore`, cloned and scraped forever | `.gitignore` plus pre-commit gitleaks plus push protection; revoke on leak |
| Secret in Docker image layer | `COPY . .` bakes `.env`, history keeps it after delete | `.dockerignore`, BuildKit secret mounts, runtime injection only |
| Secret in logs or error pages | `console.log(process.env)`, stack traces echo config | Startup masking, redaction lists, uniform errors, secret-scan on logs |
| Secret in CI output | `echo $KEY` or verbose flags print masked values into job logs | Masked vars, `set +x`, audit scripts, short-lived OIDC tokens over static keys |
| Over-broad access | One shared prod key readable by every service and intern laptop | Per-service IAM roles, per-environment scopes, least-privilege read policies |
| Stale secret after employee exit | Ex-devices and CI caches retain keys with no expiry | Rotation on departure, short TTLs, dynamic secrets, revocation runbook |
| Wrong-environment injection | Prod key pasted into staging or test key shipped to prod | Prefix validation at startup, distinct key prefixes, separate manager paths |
| No rotation after suspected leak | Team deletes the commit but keeps using the exposed key | Mandatory revoke-and-rotate policy, versioned secrets, anomaly alerts |
| Frontend bundle leak | `VITE_STRIPE_SECRET` ships to browsers, scraped in minutes | Public-only prefixes, backend proxy for private calls, bundle scan in CI |
| Downgrade to plaintext fallback | App runs with empty secret when manager is down, signing disabled | Fail closed at boot, no insecure defaults, cached encrypted fallback only |

Two scenarios show how to narrate the table. First, the classic `.env` commit: the candidate
states revoke-rotated keys, `filter-repo` purge, push-protection enablement, and a gitleaks gate
in CI — prevention, detection, and response in one breath. Second, the CI echo: the candidate
points to masked vars, OIDC federation instead of stored cloud keys, and a script audit that
removes `env` dumps — proving they think about transitive exposure, not just files.

### 6. Per-Environment Scoping and Overrides

Separate manager paths per environment (`dev/`, `staging/`, `prod/`) with distinct IAM roles so
a staging deploy can never read prod secrets even with a copy-pasted config. Non-secret defaults
live in versioned `application-{profile}.properties` while every secret is overridden by the
environment, preserving twelve-factor precedence. Naming conventions (`PROD_DB_URL` vs
`STAGING_DB_URL` or path-scoped identical names) plus startup prefix checks catch cross-env
paste errors before traffic flows.

### 7. Best Practices

1. Inject secrets at runtime from a manager; `.env` holds local dummies only, never real values.
2. Validate all required vars at startup with schemas and fail closed on missing or malformed input.
3. Scope per service and environment with least-privilege reads; one shared prod key is a finding.
4. Rotate on schedule and on departure, leak suspicion, or incident — revoke first, purge second.
5. Never commit, print, or bake secrets: ignore files, pre-commit scans, CI masking, secret mounts.
6. Mask and redact in logs and errors; audit secret versions used, never their values.
7. Keep frontend bundles public-only; private calls go through a backend proxy.
8. Rehearse rotation and revocation runbooks; measure time-to-rotate, not intentions.

### 8. Interview Questions and Answers

**Q1 (Beginner): Where should secrets live, and why not in `.env` in git?**
In a secret manager injected at runtime, scoped per service and environment with audit and
rotation. Git is replicated forever, images layer files into history, and logs retain echoes —
so a committed secret must be revoked, not just deleted, with scanning to prevent return.

**Q2 (Beginner): `.env` versus secret manager — when is each right?**
`.env` for local non-sensitive defaults and dummy keys; managers for every real credential.
The test is revocation pain: if leaking it hurts, it needs encryption, IAM scoping, audit, and
rotation that only a manager provides.

**Q3 (Intermediate): What is twelve-factor config, and how does Spring implement it?**
Config varying by deploy lives in the environment, so one immutable artifact promotes through
all stages. Spring uses externalized precedence (flags beat JSON beat env beat profile files)
with relaxed binding plus validated `@ConfigurationProperties` that fail fast on missing secrets.

**Q4 (Intermediate): `@Value` versus `@ConfigurationProperties` for secrets?**
Prefer constructor-bound `@ConfigurationProperties` with bean validation: immutable, centralized,
and startup-checked. Scattered `@Value` strings duplicate key names, skip validation, and fail
silently to null — harder to review and test.

**Q5 (Intermediate): How do you validate environment variables at startup?**
Parse once against a schema (zod in Node, bean validation in Spring), enforce shapes like URLs
and key prefixes, and exit non-zero before listening. Orchestrators keep the old revision alive
while alerts fire on the failed deploy.

**Q6 (Intermediate): How do you rotate a database password with zero downtime?**
Dual-password window: add the new credential in the manager, roll services to accept both, flip
the database, drain old connections, then revoke. Versioned secrets plus event-driven reload
(SNS, Vault lease expiry, volume-watch) avoid manual host edits.

**Q7 (Intermediate): A `.env` was pushed to GitHub — what do you do?**
Revoke and rotate immediately, check audit logs for misuse, purge with `git filter-repo` plus
force-push and expire clones, then enable push protection and pre-commit gitleaks. Deleting in a
new commit alone leaves the blob fetchable.

**Q8 (Senior): How do you stop secrets leaking through CI and Docker?**
Masked CI vars referenced never echoed, `set +x` around secret use, OIDC federation over stored
cloud keys, `.dockerignore` plus BuildKit secret mounts, runtime-only injection, and bundle scans
blocking private keys from frontend prefixes.

**Q9 (Senior): Design secret injection for ten microservices across three environments.**
Per-service IAM roles reading per-environment manager paths, short-lived dynamic credentials
where possible, startup schema validation with prefix checks, version-logged loads with masked
values, scheduled plus event-driven rotation, and centralized audit with revocation runbooks.

## Youtube

- [Your .env File Is Lying to You](https://www.youtube.com/watch?v=Hn5sgLafAMQ)