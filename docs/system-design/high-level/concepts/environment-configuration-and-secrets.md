# Environment Configuration and Secrets

## Blogs and websites


## Medium


## Youtube


## Theory

### Introduction

- Environment configuration is the practice of managing settings that change between environments (development, staging, production) **outside** of your application code, so the exact same build artifact can run unmodified in every environment.
- **Secrets** are a special, more sensitive subset of configuration — values like database passwords, API keys, TLS private keys, and encryption keys — that must additionally be **encrypted, access-controlled, and audited**, not just externalized.
- Broadly this page is organized into:
    - The core principle and why hardcoding config/secrets is dangerous
    - The configuration hierarchy (env vars → `.env` files → config files → secret managers → feature flags)
    - Environment variables and `.env` files for local development, with Java code
    - Per-environment configuration using Spring profiles
    - Production secrets management (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault) with Java code
    - Secret rotation, Kubernetes/Docker secrets, and security tooling
    - Real-life incidents caused by leaked secrets, and how to prevent them
- This is a high-yield topic in system design and backend interviews — expect questions on **why not to hardcode secrets**, **how a secret manager works end-to-end**, **how rotation works without downtime**, and **what you'd do if a secret leaked into Git history**.

**The Core Principle:** Configuration and secrets should **never** be hardcoded in source code or committed to version control. The same compiled binary/container image should be deployable to dev, staging, and production — only the *externally supplied* configuration changes.

```mermaid
flowchart LR
    Build["Single Build Artifact\n(container image / jar)"]
    Build --> Dev[Dev Environment]
    Build --> Stage[Staging Environment]
    Build --> Prod[Production Environment]

    CfgDev[("Dev Config\n+ Dev Secrets")] --> Dev
    CfgStage[("Staging Config\n+ Staging Secrets")] --> Stage
    CfgProd[("Prod Config\n+ Prod Secrets")] --> Prod
```

> **Real-life use case:** A payments company builds one Docker image per Git commit (`payments-api:sha-abc123`) in CI. That *exact same image* is deployed to dev, staging, and production — the only thing that differs is the environment variables and secrets injected at deploy time (sandbox Stripe key in dev/staging, live Stripe key in production). This guarantees "what you tested is what you ship" — there's no separate "prod build" that could behave differently.

**Interview Q&A**

- **Q: Why is externalizing configuration considered a best practice rather than just a convenience?**
    A: It lets you build a single artifact once and promote that exact artifact through every environment, eliminating "it worked in staging but not prod" bugs caused by environment-specific code paths or rebuilds. It also means secrets never need to be baked into an image (which would be visible to anyone who can pull it) and lets you change configuration (timeouts, feature flags, credentials) without a code change or redeploy.
- **Q: What's the difference between "configuration" and "secrets" in this context?**
    A: Configuration is any environment-varying setting (port numbers, log levels, feature flags, hostnames) — not sensitive, safe to commit non-secret defaults. Secrets are a subset of configuration that's additionally *sensitive*: if leaked, they grant access to something (a database, an API, an encryption key), so they need encryption at rest, access control, and audit logging on top of just being "externalized."

### Why It Matters

```
❌ Hardcoded (NEVER do this):
  db_password = "super_secret_123"
  api_key = "sk-live-abc123xyz"
  → Committed to Git → Visible to everyone with repo access
  → Same value in dev and production → Dangerous
  → Rotating a key requires code change + deploy

✓ Environment-based:
  db_password = os.environ["DB_PASSWORD"]
  api_key = os.environ["API_KEY"]
  → Different values per environment
  → Secrets not in code
  → Can rotate without code changes
```

- **Blast radius of a hardcoded secret:** once a secret is committed, it lives forever in Git history — even if you delete it in a later commit, `git log -p` (or a leaked backup/fork) still exposes it. Rotating it means changing the value **everywhere it was hardcoded**, then rebuilding and redeploying every service that used the old build.
- **Blast radius of an externalized secret:** rotation is just "update the value in the secret store" — no code change, no rebuild, and typically no redeploy (the app re-reads the secret at next startup or on a refresh interval).

> **Real-life incident:** In 2016, Uber engineers accidentally published AWS credentials in a public GitHub repository. Attackers scraped the credentials within hours and used them to access an S3 bucket containing rider/driver data for **57 million users**. The root cause was a hardcoded secret in source code rather than a secret manager — this is one of the most cited case studies for *why* secrets management is a hard requirement, not a nice-to-have.

**Interview Q&A**

- **Q: A teammate says "we'll just delete the secret from the file in the next commit, it's fine." Why is that wrong?**
    A: Git preserves full history — the old commit (and the secret in it) is still retrievable via `git log`, `git show <old-sha>`, or by anyone who already cloned/forked the repo before the deletion. The only safe remediation once a secret is committed is to treat it as **compromised and rotate it immediately** at the source (database, cloud provider, third-party API) — deleting it from the file does not undo the exposure, though `git filter-repo`/BFG can be used afterward to scrub history as defense-in-depth.

### Configuration Hierarchy

Configuration sources form a layered hierarchy — from simplest/least-secure (hardcoding, which you should never use) to most robust/secure (dedicated secret managers with encryption, access control, and rotation).

```mermaid
flowchart TB
    L1["1. Environment Variables\n(host/container-level, most common)"]
    L2["2. .env Files\n(local development only, gitignored)"]
    L3["3. Config Files\n(non-secret settings, safe to commit)"]
    L4["4. Secret Managers\n(AWS Secrets Manager, Vault, Azure Key Vault)"]
    L5["5. Feature Flags / Remote Config\n(LaunchDarkly, Firebase Remote Config)"]

    L1 --> App[Application]
    L2 --> App
    L3 --> App
    L4 -->|"encrypted, audited, rotatable"| App
    L5 -->|"toggle behavior without a deploy"| App
```

```
1. Environment Variables (most common)
   └─ Set on the host/container: export DB_HOST=localhost

2. .env Files (local development)
   └─ .env file loaded by app: DB_HOST=localhost
   └─ NEVER committed to Git (.gitignore)

3. Config Files (non-secret settings)
   └─ config/production.yaml, config/development.yaml
   └─ Can be committed (no secrets)

4. Secret Managers (production secrets)
   └─ AWS Secrets Manager, HashiCorp Vault, Azure Key Vault
   └─ Encrypted, access-controlled, audit-logged

5. Feature Flags / Remote Config
   └─ LaunchDarkly, Firebase Remote Config
   └─ Toggle features without deploys
```

**Interview Q&A**

- **Q: If environment variables already solve "don't hardcode secrets," why do production systems still need a dedicated secret manager?**
    A: Plain environment variables are externalized but not *protected* — they're often visible in process listings (`/proc/<pid>/environ`), container inspect output, CI logs, or crash dumps, and rotating one means restarting every process that reads it. Secret managers add encryption at rest, fine-grained IAM-based access control, audit logging of every read, automatic rotation on a schedule, and versioning — capabilities plain env vars don't provide on their own. In practice, secret managers are often used to *populate* environment variables or in-memory config at startup, combining both layers.

### Environment Variables

The most common way to pass configuration — set on the host, in a container's runtime, or in an orchestrator's manifest, and read by the application without ever appearing in source code.

```mermaid
flowchart LR
    subgraph Host["Host / Container Runtime"]
        EnvBlock["DATABASE_URL=...\nAPI_KEY=...\nNODE_ENV=production"]
    end
    EnvBlock -->|injected at process start| Proc[Application Process]
    Proc -->|reads once at startup| Config[In-memory Config Object]
```

```bash
# Setting environment variables
export DATABASE_URL="postgresql://user:pass@host:5432/mydb"
export REDIS_URL="redis://localhost:6379"
export API_KEY="sk-live-abc123"
export NODE_ENV="production"
export LOG_LEVEL="info"

# Accessing in code
# Python
import os
db_url = os.environ["DATABASE_URL"]

# Node.js
const dbUrl = process.env.DATABASE_URL;

# Go
dbUrl := os.Getenv("DATABASE_URL")
```

**Java: reading environment variables directly**

```java
public class DatabaseConfig {
    private final String databaseUrl;
    private final String apiKey;

    public DatabaseConfig() {
        // System.getenv throws nothing — returns null if unset, so fail fast on missing required config.
        this.databaseUrl = requireEnv("DATABASE_URL");
        this.apiKey = requireEnv("API_KEY");
    }

    private static String requireEnv(String name) {
        String value = System.getenv(name);
        if (value == null || value.isBlank()) {
            throw new IllegalStateException("Missing required environment variable: " + name);
        }
        return value;
    }
}
```

**Java: Spring Boot `@Value` and `@ConfigurationProperties`**

```java
// Simple injection of a single environment-backed property.
@Component
public class PaymentGatewayClient {

    @Value("${STRIPE_API_KEY}")
    private String stripeApiKey;
}

// Preferred for grouped settings — type-safe, validated, and testable.
@ConfigurationProperties(prefix = "database")
@Validated
public class DatabaseProperties {

    @NotBlank
    private String url;      // bound from DATABASE_URL via relaxed binding

    @NotBlank
    private String username; // bound from DATABASE_USERNAME

    @NotBlank
    private String password; // bound from DATABASE_PASSWORD — sourced from a secret manager, never logged

    // getters/setters omitted
}
```

- Spring Boot's "relaxed binding" automatically maps `DATABASE_URL` (env var) to `database.url` (property), so the same `DatabaseProperties` class works whether the value came from an OS environment variable, a `.env`-derived property, or `application.yaml`.
- **Never** log a `@ConfigurationProperties` object's `toString()` if it contains a password field — override `toString()` to mask secrets, or exclude sensitive fields from logging frameworks (e.g. Logback's `%mask` or a custom `PasswordMaskingConverter`).

**Interview Q&A**

- **Q: What's a downside of environment variables even though they're "externalized"?**
    A: They're visible to anything with access to the process — `docker inspect`, `/proc/<pid>/environ` on Linux, container orchestrator dashboards, or accidentally logged crash reports/stack traces can all leak them. They also aren't encrypted at rest in most orchestrators' default configuration (a plain Kubernetes ConfigMap/Secret is only base64-encoded, not encrypted, unless encryption-at-rest is explicitly enabled on the cluster). This is why sensitive values are usually sourced from a secret manager and only briefly materialized as an env var/in-memory value at runtime.
- **Q: Why prefer `@ConfigurationProperties` over many individual `@Value` fields in a Spring Boot app?**
    A: `@ConfigurationProperties` groups related settings into one validated, type-safe object (supporting `@NotBlank`/`@Min`/nested objects via `@Validated`), fails fast at startup if required properties are missing, and is easier to unit test (just construct the POJO) — whereas dozens of scattered `@Value("${...}")` fields are harder to validate collectively and to mock in tests.

### .env Files (Local Development)

```bash
# .env (in project root, NOT committed to Git)
DATABASE_URL=postgresql://localhost:5432/mydb_dev
REDIS_URL=redis://localhost:6379
API_KEY=sk-test-dev-key
NODE_ENV=development
LOG_LEVEL=debug
```

```bash
# .env.example (committed to Git — template without real values)
DATABASE_URL=postgresql://user:password@host:5432/dbname
REDIS_URL=redis://localhost:6379
API_KEY=your-api-key-here
NODE_ENV=development
LOG_LEVEL=debug
```

**Rules:**
- `.env` → in `.gitignore` (never committed)
- `.env.example` → committed (shows required variables without real values)
- Use libraries to load: `dotenv` (Node.js), `python-dotenv` (Python), `dotenv-java` / `spring-dotenv` (Java)

**Java: loading a `.env` file with the `dotenv-java` library**

```java
import io.github.cdimascio.dotenv.Dotenv;

public class AppConfig {
    public static void main(String[] args) {
        // Looks for a .env file in the working directory; ignored if missing (e.g. in prod where real env vars are set).
        Dotenv dotenv = Dotenv.configure()
                .ignoreIfMissing()
                .load();

        String databaseUrl = dotenv.get("DATABASE_URL");
        String apiKey = dotenv.get("API_KEY");
        // Values are now available exactly as if they came from a real OS environment variable.
    }
}
```

> **Real-life use case:** A new engineer joins the team and runs `cp .env.example .env`, fills in their own local Postgres/Redis URLs, and runs the app with zero code changes and zero risk of accidentally using (or leaking) a production credential — the `.env.example` file doubles as living documentation of every configuration variable the service needs.

**Interview Q&A**

- **Q: Why have both a `.env` file and a `.env.example` file?**
    A: `.env` holds real (even if only local/dev-tier) values and must never be committed — it's personal to each developer's machine. `.env.example` is committed and acts as a template/checklist showing every variable the app requires (with placeholder values), so new team members and CI know exactly what to configure without ever seeing a real secret.
- **Q: Should `.env` files ever be used in production?**
    A: Generally no — in production, config/secrets should come from the orchestrator's injected environment variables (populated from a secret manager) rather than a flat file sitting on disk, which is harder to rotate, audit, and encrypt at rest compared to a dedicated secret store. `.env` files are best scoped to local development and sometimes CI.

### Secrets Management (Production)

For production systems, environment variables alone aren't enough — they aren't encrypted at rest by default, rotating them means restarting processes, and there's no audit trail of who read what. Dedicated **secret managers** solve all three problems.

```mermaid
sequenceDiagram
    participant App as Application (IAM Role / Service Identity)
    participant SM as Secret Manager (AWS Secrets Manager / Vault)
    participant KMS as Encryption Key (KMS/HSM)
    participant DB as Database

    App->>SM: GetSecretValue("prod/db/password")\n(authenticated via IAM role, no long-lived credential)
    SM->>SM: Check IAM policy: is App allowed to read this secret?
    SM->>KMS: Decrypt secret ciphertext
    KMS-->>SM: Plaintext secret
    SM-->>App: Plaintext secret (over TLS)
    SM->>SM: Write audit log entry (who, what, when)
    App->>DB: Connect using retrieved password
```

**AWS Secrets Manager (Python quick reference):**
```python
import boto3
client = boto3.client('secretsmanager')
secret = client.get_secret_value(SecretId='prod/db/password')
```

**Java: AWS Secrets Manager (AWS SDK v2) with in-memory caching**

```java
@Component
public class SecretsManagerConfigSource {

    private final SecretsManagerClient client = SecretsManagerClient.create(); // credentials via IAM role, not hardcoded
    private final Map<String, CachedSecret> cache = new ConcurrentHashMap<>();
    private static final Duration TTL = Duration.ofMinutes(5);

    public String getSecret(String secretId) {
        CachedSecret cached = cache.get(secretId);
        if (cached != null && !cached.isExpired()) {
            return cached.value(); // avoid hitting Secrets Manager on every request
        }

        GetSecretValueRequest request = GetSecretValueRequest.builder()
                .secretId(secretId)
                .build();
        String value = client.getSecretValue(request).secretString();
        cache.put(secretId, new CachedSecret(value, Instant.now().plus(TTL)));
        return value;
    }

    private record CachedSecret(String value, Instant expiresAt) {
        boolean isExpired() {
            return Instant.now().isAfter(expiresAt);
        }
    }
}
```

**HashiCorp Vault (CLI quick reference):**
```bash
vault kv get secret/prod/database
# Returns: { "password": "encrypted-value" }
```

**Java: HashiCorp Vault via Spring Cloud Vault**

```yaml
# bootstrap.yaml — Spring Cloud Vault fetches secrets before the app context even starts,
# and injects them as regular Spring properties.
spring:
  cloud:
    vault:
      uri: https://vault.internal:8200
      authentication: KUBERNETES          # short-lived token via the pod's K8s service account
      kv:
        enabled: true
        backend: secret
        default-context: payments-service # reads secret/payments-service/*
```

```java
@ConfigurationProperties(prefix = "database")
public class DatabaseProperties {
    private String password; // bound transparently from Vault — code never calls Vault's API directly
}
```

**Azure Key Vault** works the same way conceptually: an app authenticates via a **Managed Identity** (no credential to manage at all), calls `SecretClient.getSecret("db-password")`, and Azure AD verifies the identity's RBAC role before decrypting and returning the value.

**Key Features of Secret Managers:**
- **Encryption at rest**: Secrets stored encrypted (AES-256, via a KMS/HSM-backed key)
- **Access control**: IAM policies/RBAC determine which identity can read which secret
- **Audit logging**: Every read is logged (who, what secret, when, from where)
- **Automatic rotation**: Change passwords/keys on a schedule without downtime (see below)
- **Versioning**: Roll back to a previous secret value if a rotation breaks something

**Interview Q&A**

- **Q: Walk through what happens when a service starts up and needs its database password from AWS Secrets Manager.**
    A: The service's compute (EC2 instance/ECS task/Lambda) has an **IAM role** attached — no static AWS credentials are hardcoded anywhere. At startup, the app's SDK calls `GetSecretValue` for a secret ID like `prod/db/password`; AWS verifies the calling role's IAM policy permits reading that specific secret, then uses KMS to decrypt the stored ciphertext and returns the plaintext over TLS. AWS logs the access (via CloudTrail) for audit. The app typically caches the value in memory for a short TTL rather than calling Secrets Manager on every request, to reduce latency and API cost.
- **Q: What's the advantage of a secret manager over just storing secrets as encrypted environment variables?**
    A: An environment variable, once set, is static for the life of the process — rotating it requires restarting every instance. A secret manager decouples the *storage/rotation* of the secret from the *running process*: you can rotate the underlying secret centrally, and well-designed clients either re-fetch on a TTL or receive a push notification, without a full redeploy. You also get centralized, fine-grained access policies and a full audit trail, which plain env vars (even if individually encrypted) don't provide out of the box.
- **Q: Why does Vault authentication via Kubernetes use short-lived tokens instead of a static Vault token?**
    A: A pod's Kubernetes service account token is automatically rotated and scoped to that pod's identity; Vault verifies it against the Kubernetes API on each login and issues a short-lived Vault token in exchange. If that token leaks, it expires quickly and is scoped only to what that specific service account/policy allows — far smaller blast radius than a long-lived, broadly-scoped static Vault token embedded in config.

### Secret Rotation

Rotation means periodically replacing a secret's value (a DB password, an API key, a TLS cert) **without causing an outage**, so a leaked-but-undetected secret has a limited window of usefulness even if it's never explicitly reported as compromised.

```mermaid
sequenceDiagram
    participant Sched as Rotation Scheduler
    participant SM as Secret Manager
    participant DB as Database
    participant App as Running App Instances

    Sched->>SM: Trigger rotation for prod/db/password
    SM->>DB: Create NEW password (old password still valid)
    SM->>SM: Store new version as "AWSPENDING" / v2
    Note over App: Old instances keep using cached v1 — still valid, no downtime
    SM->>App: App refreshes cache (TTL expiry or push notification) → fetches v2
    App->>DB: Connect using v2 — succeeds because both v1 and v2 are valid during overlap window
    Sched->>DB: After overlap window, invalidate v1 (old password)
    SM->>SM: Mark v2 as "AWSCURRENT"
```

- **Dual-validity window:** the critical trick that avoids downtime — the *old* and *new* secret values are both valid simultaneously for a grace period, so in-flight requests using cached old credentials don't fail while other instances pick up the new value.
- **Java: handling rotation gracefully with a retry-on-auth-failure pattern** (in case an instance's cache is stale past the overlap window):

```java
public Connection getDbConnection() throws SQLException {
    try {
        return dataSource.getConnection(); // uses cached password
    } catch (SQLException authFailure) {
        // Password may have rotated and our cache expired — force a refresh and retry once.
        secretsManagerConfigSource.evictCache("prod/db/password");
        dataSource.setPassword(secretsManagerConfigSource.getSecret("prod/db/password"));
        return dataSource.getConnection();
    }
}
```

**Interview Q&A**

- **Q: How do you rotate a database password with zero downtime across 50 running service instances?**
    A: The secret manager rotates the password *at the database* by creating a new credential while the old one is still valid (a dual-validity/overlap window), rather than immediately invalidating the old one. Running instances continue using their cached old password successfully until their cache TTL expires or they receive a rotation notification, at which point they fetch the new value. Only after all instances have had time to pick up the new credential does the rotation process invalidate the old one. Without this overlap window, any instance still using a cached old password would start failing to connect the instant rotation completes.
- **Q: What should an application do if a database connection suddenly fails with an authentication error in production?**
    A: Before assuming an outage, check whether a secret rotation just occurred — if the app's secret cache is stale (past the provider's dual-validity window), it will be presenting an invalidated password. A resilient client should catch auth-specific failures, force-refresh the cached secret, and retry the connection once before treating it as a hard failure/alerting on-call.

### Best Practices

```
✓ Never hardcode secrets in source code
✓ Use .env for local dev, secret managers for production
✓ Add .env to .gitignore
✓ Provide .env.example as a template
✓ Use different secrets per environment (dev ≠ staging ≠ prod)
✓ Rotate secrets regularly (90 days for passwords)
✓ Use least privilege (services only access secrets they need)
✓ Encrypt secrets at rest and in transit
✓ Audit secret access (who accessed what, when)
✓ Use short-lived tokens where possible (temporary credentials)

✗ Never log secrets (mask in logs)
✗ Never pass secrets in URLs or query parameters
✗ Never share secrets via Slack/email (use a vault)
✗ Never use the same secret across environments
✗ Never commit .env files to Git
```

#### OWASP Mapping and Tooling

Hardcoded/leaked secrets map directly to **OWASP Top 10 A05:2021 – Security Misconfiguration** and contribute to **A02:2021 – Cryptographic Failures** when the exposed secret is a cryptographic key. Practical defenses:

- **Pre-commit secret scanning:** tools like `git-secrets`, `gitleaks`, or `truffleHog` run in a pre-commit hook or CI pipeline and block a commit/PR if it matches known secret patterns (AWS access key format, private key headers, high-entropy strings).
- **Platform-native scanning:** GitHub's **secret scanning + push protection** rejects a `git push` outright if it detects a recognizable secret pattern, and partner providers (AWS, Stripe, etc.) are automatically notified to revoke leaked keys.
- **Least privilege IAM:** scope each service's secret-read permission to only the specific secret(s) it needs (`prod/payments-service/db-password`), not a wildcard `secret:*` — this limits blast radius if one service's credentials are compromised.
- **Short-lived credentials over static ones:** prefer IAM roles / Workload Identity / Managed Identity (which issue temporary, auto-rotated credentials) over long-lived access keys wherever the platform supports it.

**Interview Q&A**

- **Q: A secret scanning tool flags a hardcoded API key in a PR — what's the correct remediation sequence?**
    A: (1) Immediately **rotate/revoke** the exposed key at its source (the third-party provider or internal secret manager) — treat it as compromised regardless of whether the PR was merged, since anyone who fetched the branch already has it. (2) Remove the hardcoded value from the code and replace it with a reference to the secret manager/environment variable. (3) Optionally scrub the value from Git history (`git filter-repo`/BFG) as defense-in-depth, understanding this doesn't undo any exposure that already happened. (4) Only after rotation is confirmed should the PR be merged.
- **Q: Why is "least privilege" specifically important for secret access, beyond general security hygiene?**
    A: If every service can read every secret (a common shortcut in early-stage systems), compromising *any single service* gives an attacker access to *all* secrets — turning one vulnerability into a full-system breach. Scoping each service's IAM policy to only the secrets it actually needs means a compromised service only leaks the blast radius of its own credentials.

### Configuration per Environment

Non-secret settings that differ by environment (port, log level, feature toggles, timeouts) are usually kept in **config files per environment**, loaded based on an `ENV`/`profile` variable — while secrets referenced *inside* those files still come from a secret manager, not from the file itself.

```mermaid
flowchart LR
    EnvVar["SPRING_PROFILES_ACTIVE=production"] --> App[Application Startup]
    App --> Load{Load config file\nfor active profile}
    Load --> Dev["application-development.yaml\n(debug=true, port=3000)"]
    Load --> Stage["application-staging.yaml\n(debug=false, port=8080)"]
    Load --> Prod["application-production.yaml\n(debug=false, port=8080)"]
```

```yaml
# config/development.yaml
server:
  port: 3000
  debug: true
logging:
  level: debug

# config/production.yaml
server:
  port: 8080
  debug: false
logging:
  level: warn
```

**Java: Spring Boot profile-specific configuration**

```yaml
# application-development.yaml
server:
  port: 3000
logging:
  level:
    root: DEBUG
feature-flags:
  new-checkout-flow: true

# application-production.yaml
server:
  port: 8080
logging:
  level:
    root: WARN
feature-flags:
  new-checkout-flow: false
```

```java
@Configuration
public class FeatureFlagConfig {

    // Only registered when the "development" profile is active — e.g. a verbose debug endpoint.
    @Bean
    @Profile("development")
    public DebugController debugController() {
        return new DebugController();
    }

    @Bean
    @Profile("!development") // active in staging/production, never in dev
    public RateLimiter productionRateLimiter() {
        return new RateLimiter(1000); // strict prod limit, relaxed/absent in dev
    }
}
```

The active profile is selected purely via an environment variable at deploy time — `SPRING_PROFILES_ACTIVE=production` — so the *same* build artifact picks up different, environment-appropriate configuration without any code change, directly reinforcing the core principle from the introduction.

**Interview Q&A**

- **Q: If `application-production.yaml` contains a `database.password: ${DB_PASSWORD}` placeholder, where does the actual value come from?**
    A: The `${DB_PASSWORD}` placeholder is resolved from an environment variable (or a property source registered earlier in Spring's `PropertySource` chain) at startup — that environment variable is itself populated by the orchestrator (Kubernetes/ECS) from a secret manager. The YAML file itself never contains the real secret value, only a reference to where it should be sourced from — so the file is safe to commit to Git.
- **Q: What's the risk of putting `debug: true` or verbose logging as the default in a shared config file instead of profile-specific files?**
    A: If a shared/base config accidentally leaks into production (e.g. a missing `SPRING_PROFILES_ACTIVE` env var causes it to fall back to defaults), verbose debug logging can leak sensitive request/response payloads (including secrets/PII) into logs, and disabling security features meant only for local convenience (e.g. relaxed CORS, disabled auth) can become a real vulnerability. Always make production the explicit, intentional profile rather than relying on a default that happens to be safe.

### Kubernetes and Docker Secrets

Container orchestrators have their own primitives for injecting configuration and secrets, which are commonly used as the final delivery mechanism *in front of* (or instead of) a full external secret manager.

```mermaid
flowchart TB
    subgraph K8s["Kubernetes Cluster"]
        CM["ConfigMap\n(non-secret config)"]
        Sec["Secret\n(base64-encoded, not encrypted by default)"]
        Pod["Pod: app container"]
        CM -->|"envFrom / volumeMount"| Pod
        Sec -->|"envFrom / volumeMount"| Pod
    end
    ExtVault["External Secret Manager\n(Vault / AWS Secrets Manager)"] -->|"External Secrets Operator\nsyncs into"| Sec
```

```yaml
# Kubernetes Secret (base64-encoded — NOT encryption; enable etcd encryption-at-rest for real protection)
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
data:
  password: c3VwZXJzZWNyZXQxMjM=   # base64 of "supersecret123"
---
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: app
          envFrom:
            - configMapRef:
                name: app-config      # non-secret settings
            - secretRef:
                name: db-credentials  # secret settings
```

```yaml
# docker-compose.yaml — using Docker secrets (mounted as files, not env vars, reducing accidental leakage via `docker inspect`)
services:
  app:
    image: myapp:latest
    secrets:
      - db_password
secrets:
  db_password:
    file: ./secrets/db_password.txt   # gitignored; in real deployments sourced from a vault/CI secret store
```

- A plain Kubernetes `Secret` is only **base64-encoded**, not encrypted — anyone with `get secrets` RBAC permission (or etcd access) can trivially decode it. Real protection requires enabling **encryption at rest** for the cluster's etcd store and tightly scoping RBAC.
- The **External Secrets Operator** (or cloud-native equivalents like AWS Secrets Manager's CSI driver) bridges the gap: it syncs values from a real secret manager into native Kubernetes `Secret` objects on a schedule, so pods still consume the familiar Kubernetes API while the actual source of truth (and rotation) lives in Vault/AWS/Azure.
- Docker secrets (used with Swarm or Compose) are mounted as files under `/run/secrets/<name>` rather than environment variables — this avoids the secret showing up in `docker inspect` or child-process environment dumps.

**Interview Q&A**

- **Q: Is a Kubernetes `Secret` actually secure by default?**
    A: No — by default it's only base64-encoded (trivially reversible), not encrypted, and stored in etcd in plaintext unless the cluster operator has explicitly enabled **encryption at rest**. Access is controlled purely by Kubernetes RBAC (`get`/`list` on `secrets`), so a misconfigured RBAC role or a compromised pod with a broad service account can read every secret in its namespace. Production clusters should enable etcd encryption at rest, restrict RBAC tightly, and often layer an external secret manager (via the External Secrets Operator) on top rather than relying on native `Secret` objects alone.
- **Q: Why mount a secret as a file instead of an environment variable in a container?**
    A: File-based secrets aren't captured by `docker inspect`/`kubectl describe pod` (which do show env vars in plaintext), aren't inherited by child processes the way environment variables are, and are easier to rotate in place (overwrite the file; the app watches for changes) without restarting the container — whereas environment variables are fixed for the life of the process.

### Real-Life Case Studies

- **Uber (2016):** Engineers committed AWS credentials to a private GitHub repository that was nonetheless accessible; attackers extracted the keys and accessed an S3 bucket with 57 million riders'/drivers' records. Lesson: even "private" repos are not a substitute for secret management — a leaked credential in Git history is a leaked credential, period.
- **Capital One (2019):** A misconfigured **AWS WAF (web application firewall) IAM role** with overly broad permissions was exploited via SSRF to retrieve temporary security credentials from the EC2 instance metadata service, which were then used to access and exfiltrate over 100 million customers' data from S3. Lesson: least-privilege IAM policies and metadata service hardening (IMDSv2) are essential even when using "proper" credential mechanisms — over-permissioned roles are almost as dangerous as hardcoded secrets.
- **Travis CI (2021):** A bug allowed environment variables (including secrets) from a public repository's build to be exposed to forks/PRs from external contributors via `.travis.yml` history. Lesson: CI/CD pipelines are a secret-handling surface too — treat CI environment variables with the same rigor as application secrets, and be wary of secrets being echoed into build logs.
- **Codecov (2021 supply-chain attack):** Attackers modified Codecov's Bash Uploader script to exfiltrate CI environment variables (many containing cloud credentials and signing keys) from thousands of customer pipelines. Lesson: any third-party script/dependency that runs inside your CI pipeline has access to your secrets — vet and pin dependencies, and prefer short-lived, narrowly-scoped CI credentials (OIDC federation to cloud providers instead of long-lived static keys) so a compromised build step has limited value to steal.

**Interview Q&A**

- **Q: What's a common thread across most real-world secret-leak incidents?**
    A: The secret was either hardcoded/committed somewhere it shouldn't have been (source code, CI config, a script), or the credential that *was* properly issued (an IAM role, a metadata-service token) was **over-permissioned** relative to what the compromised component actually needed. Both point to the same two mitigations: never hardcode secrets, and enforce least privilege so that even a legitimately-issued credential can't be leveraged into a full-system breach.
- **Q: How does using OIDC-based CI/CD authentication (e.g. GitHub Actions → AWS via OIDC) reduce risk compared to storing long-lived cloud credentials as CI secrets?**
    A: OIDC federation lets the CI job **request a short-lived, narrowly-scoped credential just-in-time** from the cloud provider, authenticated by a signed token asserting the specific repo/workflow's identity — there's no long-lived access key sitting in CI secret storage at all that could be exfiltrated by a compromised build step or a malicious third-party action. Even if a token is captured mid-build, it expires quickly and is scoped to only the permissions that specific workflow was granted.

### The 12-Factor App Principle (Factor III — Config)

> Store config in the environment. If you can open-source your codebase without exposing secrets, you're doing it right.

This single sentence from the [12-factor app methodology](https://12factor.net/config) is the underlying justification for everything above: config (including secrets) must be strictly separated from code, varies per deploy (dev/staging/prod), and is never grouped into named, hardcoded "environments" in the code itself — it's supplied purely through the environment at runtime.

---

## Summary: Cheat Sheet

| Layer | Used For | Committed to Git? | Encrypted? | Rotatable Without Redeploy? |
|---|---|---|---|---|
| Hardcoded values | Never — anti-pattern | N/A | N/A | N/A |
| Environment variables | Simple config, all envs | N/A (set outside code) | No (plaintext in process) | No (requires restart) |
| `.env` files | Local development only | ❌ No (`.env.example` only) | No | N/A (local only) |
| Config files (YAML/JSON per profile) | Non-secret, per-environment settings | ✅ Yes | No | Requires redeploy for the file itself |
| Secret Managers (AWS/Vault/Azure) | Production secrets | N/A (not files) | ✅ Yes (KMS/HSM) | ✅ Yes (dual-validity rotation) |
| Kubernetes `Secret` (native) | Cluster-native secret delivery | ❌ No | ⚠️ Base64 only by default | Partial — needs a controller/operator to auto-refresh |
| Feature flags / remote config | Toggling behavior | N/A | N/A | ✅ Yes (instant) |

## Interview Questions Recap

**1. Why should configuration and secrets never be hardcoded in source code?**

Hardcoding ties a value to a specific build, so the same binary/image can't be safely promoted across dev/staging/prod without either containing every environment's secrets simultaneously or requiring separate builds per environment (defeating "build once, deploy everywhere"). Once committed, a secret lives in Git history permanently — even deleting it in a later commit doesn't remove it from `git log`, prior clones, or forks. Hardcoded secrets also can't be rotated without a code change and a redeploy, meaning a compromised value stays exploitable for as long as it takes to notice, fix, review, build, and ship — versus seconds in a secret manager. Real incidents (Uber 2016, countless GitHub secret-scanning alerts) trace directly back to this anti-pattern.

**2. Walk through the configuration hierarchy from least to most robust, and when you'd use each layer.**

(1) **Environment variables** — the baseline mechanism for any non-hardcoded config, set by the host/container/orchestrator; used everywhere but not encrypted or access-controlled on their own. (2) **`.env` files** — a local-development convenience that loads a set of environment variables from a gitignored file, paired with a committed `.env.example` template; not meant for production. (3) **Config files per environment** (`application-production.yaml`) — non-secret, structured settings (ports, log levels, feature toggles) safe to commit, loaded based on an active profile/environment variable. (4) **Secret managers** (AWS Secrets Manager, Vault, Azure Key Vault) — the production-grade layer for actual secrets, adding encryption at rest, IAM-based access control, audit logging, and rotation. (5) **Feature flags / remote config** (LaunchDarkly) — for toggling application *behavior* (not credentials) instantly without any deploy at all. In practice, production systems use multiple layers together: a config file selects environment-specific non-secret settings, while placeholders inside it are resolved from a secret manager via environment variables injected by the orchestrator.

**3. What's the difference between a `.env` file and a secret manager, and why isn't a `.env` file sufficient for production?**

A `.env` file is a flat, unencrypted text file read at process startup — convenient for local development because any teammate can `cp .env.example .env` and fill in local values with zero infrastructure. It has no access control (anyone who can read the filesystem can read every secret in it), no audit trail, no automatic rotation, and if accidentally committed, is a direct secret leak. A secret manager stores each secret encrypted at rest (via a KMS/HSM-backed key), enforces per-secret IAM/RBAC policies (so a service can only read the secrets it's explicitly authorized for), logs every access, supports scheduled rotation with a dual-validity window to avoid downtime, and versions values so a bad rotation can be rolled back. Production systems use a secret manager as the source of truth and typically only materialize values as environment variables briefly at runtime, injected by the orchestrator.

**4. Explain how a service authenticates to AWS Secrets Manager or HashiCorp Vault without hardcoding its own credentials.**

The service runs with an **identity** attached by the platform rather than a static credential embedded in config: on AWS, an **IAM role** attached to the EC2 instance/ECS task/Lambda; in Kubernetes with Vault, the pod's **Kubernetes service account token**, which Vault verifies against the Kubernetes API before issuing a short-lived Vault token; on Azure, a **Managed Identity**. The SDK/client library automatically discovers and uses this ambient identity to call `GetSecretValue`/Vault's API — no access key, password, or token is ever written into source code or a config file. The secret manager checks that identity's policy permits reading the requested secret, decrypts it via KMS/HSM, and returns the plaintext over TLS, logging the access. This "credential to fetch other credentials" is itself short-lived and automatically rotated by the platform, closing the loop on hardcoded secrets entirely.

**5. How does secret rotation work without causing a production outage?**

The key mechanism is a **dual-validity (overlap) window**: when rotation is triggered, the secret manager creates a *new* credential at the source (e.g. a new DB password) while the *old* one remains valid for a grace period, rather than invalidating the old value immediately. Running application instances continue operating successfully on their cached old value during this window. As instances' caches expire (TTL) or they receive a push notification, they fetch the new value and start using it — all without a coordinated restart. Only after the overlap window has elapsed (giving every instance a chance to pick up the new value) does the rotation process invalidate the old credential. A well-designed client also catches authentication failures as a signal to force-refresh its cached secret and retry once, providing a safety net if an instance's cache outlives the overlap window.

**6. What's actually wrong with Kubernetes' native `Secret` object from a security standpoint, and how do teams address it?**

A native Kubernetes `Secret` is only **base64-encoded**, not encrypted — trivially reversible by anyone who can `kubectl get secret -o yaml` or read the underlying etcd data directly. By default, etcd itself stores this data unencrypted on disk unless the cluster operator explicitly enables **encryption at rest**, and access is gated purely by Kubernetes RBAC, so an overly broad service account or RBAC misconfiguration can expose every secret in a namespace. Teams address this by enabling etcd encryption at rest, tightly scoping RBAC (`get`/`list` on `secrets` limited to only the pods/service accounts that need it), and often layering an external secret manager on top via the **External Secrets Operator** (or a cloud-native CSI driver), so the actual source of truth, encryption, and rotation live in Vault/AWS Secrets Manager/Azure Key Vault, while pods still consume the familiar Kubernetes `Secret`/env var interface.

**7. Give a concrete example of how you'd structure configuration for a Spring Boot service across dev, staging, and production, including where secrets fit in.**

Use Spring profiles: `application-development.yaml`, `application-staging.yaml`, and `application-production.yaml` each hold non-secret, environment-appropriate settings (server port, log level, feature flags) and are all safely committed to Git. Any secret referenced inside these files (e.g. `database.password: ${DB_PASSWORD}`) is a placeholder resolved from an environment variable at startup, never a literal value. The orchestrator (Kubernetes/ECS) sets `SPRING_PROFILES_ACTIVE=production` (selecting which YAML loads) and separately injects `DB_PASSWORD` as an environment variable sourced from a secret manager (directly, or via Spring Cloud Vault which fetches and binds it as a regular Spring property before the app context even starts). The result: the exact same compiled JAR/container image, differing only in which profile is activated and which secrets are injected by the platform at deploy time — no rebuild required to move between environments.

**8. What OWASP category do leaked/hardcoded secrets fall under, and what tooling helps prevent them?**

Hardcoded and leaked secrets map to **OWASP Top 10 A05:2021 – Security Misconfiguration**, and when the leaked value is itself a cryptographic key, it also implicates **A02:2021 – Cryptographic Failures**. Prevention tooling operates at multiple points: **pre-commit hooks** (`git-secrets`, `gitleaks`) scan a diff locally before it's even committed; **CI pipeline scanning** (`truffleHog`, `gitleaks` in CI) catches anything that slips past local hooks; and **platform-native scanning** (GitHub secret scanning + push protection) can outright reject a `git push` containing a recognizable secret pattern, and automatically notifies the relevant provider (AWS, Stripe, etc.) to revoke a leaked key. None of these are a substitute for the underlying practice (secret managers, least privilege, no hardcoding) — they're a safety net to catch mistakes before or shortly after they happen.

**9. If a secret scanning tool flags a real API key committed in a pull request, what's the correct incident response — in order?**

(1) **Rotate/revoke the key immediately at its source** (the third-party provider or the internal secret manager) — treat it as compromised the moment it's known to have been committed, regardless of whether the branch was merged or public, since anyone who already cloned/fetched has it. (2) **Fix the code** to reference the secret manager/environment variable instead of the literal value. (3) **Scrub Git history** (`git filter-repo` or BFG Repo-Cleaner) as defense-in-depth — understanding this does not retroactively undo any exposure that already occurred. (4) Only merge the fix once rotation is confirmed complete, and consider auditing logs for any suspicious use of the old key during the exposure window.

**10. Compare how AWS Secrets Manager, HashiCorp Vault, and Azure Key Vault authenticate an application, and what they have in common.**

**AWS Secrets Manager** relies on an **IAM role** attached to the compute resource (EC2/ECS/Lambda) — the SDK auto-discovers temporary credentials from the instance/task metadata and calls `GetSecretValue`, gated by an IAM policy. **HashiCorp Vault** supports multiple auth backends, but in Kubernetes the common pattern is the pod's **service account token**, which Vault validates against the Kubernetes API and exchanges for a short-lived Vault token scoped by a Vault policy. **Azure Key Vault** uses a **Managed Identity** assigned to the compute resource, authenticated via Azure AD, with access gated by Azure RBAC roles. All three share the same underlying design: the application never holds a static, long-lived credential to authenticate to the secret store — it holds (or is granted) a short-lived, platform-issued identity, and the actual secret is fetched just-in-time, decrypted server-side (via KMS/Vault's barrier/Azure's HSM), and returned over TLS with every access logged for audit.

**11. Why should CI/CD pipelines be treated as a secret-handling surface with the same rigor as application code, and what's an example of what can go wrong?**

CI/CD pipelines routinely need real credentials (cloud deploy keys, package registry tokens, signing keys) to do their job, making them an attractive target — a compromised or malicious build step (a modified third-party GitHub Action, a tampered dependency's install script) runs with the same access as the pipeline's configured secrets. The **Codecov 2021 supply-chain attack** is the canonical example: attackers modified Codecov's own Bash Uploader script (widely used inside customer CI pipelines) to silently exfiltrate every environment variable in the build environment — capturing cloud credentials and signing keys across thousands of unrelated companies' pipelines, none of whom had a code-level vulnerability themselves. Mitigations include: minimizing which secrets are exposed to which pipeline stages (least privilege within CI itself), pinning third-party actions/scripts to a specific commit SHA (not a mutable tag), and preferring short-lived, OIDC-federated cloud credentials over long-lived static keys stored as CI secrets, so a compromised build step captures a token that expires quickly and is narrowly scoped.

**12. What's the practical difference between a Kubernetes `ConfigMap` and a Kubernetes `Secret`, and is that difference meaningful for security?**

Structurally, `ConfigMap` and `Secret` are nearly identical Kubernetes objects — both store key-value data and can be mounted into pods as environment variables or files. The only built-in differences are that `Secret` data is base64-encoded (vs. plaintext in a `ConfigMap`) and Kubernetes applies slightly different handling in some contexts (e.g. `kubectl describe pod` doesn't print `Secret` values by default, though it does for `ConfigMap`s). Crucially, **base64 is encoding, not encryption** — it provides no real confidentiality, so from a pure security standpoint a `Secret` is not meaningfully more protected than a `ConfigMap` unless the cluster additionally has etcd encryption at rest enabled and tight RBAC scoping. This is precisely why production-grade systems don't rely on native `Secret` objects alone and instead layer a real secret manager (via an operator/CSI driver) on top for actual encryption, rotation, and audit logging.



