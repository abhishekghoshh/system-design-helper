# Environment Configuration and Secrets

## Theory

### What is Environment Configuration?

Environment configuration is the practice of managing settings that change between environments (development, staging, production) **outside** of your application code. Secrets are a subset — sensitive values like API keys, database passwords, and encryption keys that must never be exposed.

**The Core Principle:** Configuration and secrets should **never** be hardcoded in source code or committed to version control.

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

### Configuration Hierarchy

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

### Environment Variables

The most common way to pass configuration:
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
- Use libraries to load: `dotenv` (Node.js), `python-dotenv` (Python)

### Secrets Management (Production)

For production systems, environment variables alone aren't enough. Use dedicated secret managers:

**AWS Secrets Manager:**
```python
import boto3
client = boto3.client('secretsmanager')
secret = client.get_secret_value(SecretId='prod/db/password')
```

**HashiCorp Vault:**
```bash
vault kv get secret/prod/database
# Returns: { "password": "encrypted-value" }
```

**Key Features of Secret Managers:**
- **Encryption at rest**: Secrets stored encrypted (AES-256)
- **Access control**: IAM policies determine who can read which secrets
- **Audit logging**: Every access is logged
- **Automatic rotation**: Change passwords/keys on a schedule without downtime
- **Versioning**: Roll back to previous secret values

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

### Configuration per Environment

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

**12-Factor App Principle (Factor III — Config):**
Store config in the environment. If you can open-source your codebase without exposing secrets, you're doing it right.
