# Application security

## Youtube

- [OAuth 2.0: Explained with API Request and Response Sample | High Level System Design](https://www.youtube.com/watch?v=3Gx3e3eLKrg)

- [Token vs Session Authentication | Authentication Explained!!!](https://www.youtube.com/watch?v=QzntvHz23tw)
- [OAuth2 Can Be Hacked Without PKCE | PKCE Explained](https://www.youtube.com/watch?v=hpryVn8LT4E)

- [99% of Developers Don't Get OAuth](https://www.youtube.com/watch?v=-VwWitk4_s4)


## Udemy

- [The Nuts and Bolts of OAuth 2.0](https://www.udemy.com/course/oauth-2-simplified/)
- [Advanced OAuth Security](https://www.udemy.com/course/advanced-oauth-security/)
- [Enterprise OAuth 2.0 and OpenID Connect](https://www.udemy.com/course/enterprise-oauth-for-developers/)


## Theory

### What is OAuth 2.0?

OAuth 2.0 is an **authorization framework** that enables third-party applications to obtain limited access to a user's resources on another service without exposing the user's credentials. It's the industry-standard protocol for authorization.

**Key Characteristics:**
- **Authorization, not Authentication**: OAuth 2.0 is designed for authorization (granting access to resources), not authentication (verifying identity)
- **Delegated Access**: Allows users to grant applications access to their data on other services
- **Token-based**: Uses access tokens instead of sharing passwords
- **Scopes**: Defines granular permissions for what the application can access

### OAuth 2.0 Components

```
┌─────────────────────────────────────────────────────────────┐
│                     OAuth 2.0 Architecture                   │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  Resource Owner  │  (End User)
│   (User)         │  - Owns the protected resources
└────────┬─────────┘  - Grants access to client application
         │
         │ (1) Authorization Request
         │
         ▼
┌──────────────────┐         (2) Authorization Grant         ┌──────────────────┐
│     Client       │─────────────────────────────────────────▶│ Authorization    │
│  (Application)   │                                          │     Server       │
│                  │◀─────────────────────────────────────────│                  │
└────────┬─────────┘         (3) Access Token                └──────────────────┘
         │                                                     - Authenticates user
         │                                                     - Issues tokens
         │                                                     - Validates scopes
         │
         │ (4) Access Token
         │
         ▼
┌──────────────────┐
│   Resource       │
│    Server        │
│   (API Server)   │
└──────────────────┘
- Hosts protected resources
- Validates access tokens
- Serves protected data
```

**Components Explained:**

1. **Resource Owner (User)**
   - The entity that owns the protected resources
   - Typically an end-user who can grant access to their data
   - Example: A user with photos on Google Photos

2. **Client (Application)**
   - The application requesting access to protected resources
   - Must be registered with the authorization server
   - Has a client ID and optionally a client secret
   - Types: Public clients (mobile/SPA) and Confidential clients (server-side)
   - Example: A photo printing service requesting access to Google Photos

3. **Authorization Server**
   - Issues access tokens after authenticating the resource owner
   - Validates client credentials
   - Manages consent and scopes
   - Example: Google's OAuth 2.0 server, Auth0, Okta

4. **Resource Server (API Server)**
   - Hosts the protected resources
   - Validates access tokens before serving requests
   - Often the same as the authorization server in simple setups
   - Example: Google Photos API

### OAuth 2.0 Grant Types (Flows)

#### 1. Authorization Code Flow

**Best for**: Server-side web applications (confidential clients)

**Description**: The most secure and commonly used flow. The client receives an authorization code which is then exchanged for an access token.

```
┌──────────┐                                          ┌──────────────────┐
│  User    │                                          │  Authorization   │
│ (Browser)│                                          │     Server       │
└────┬─────┘                                          └────────┬─────────┘
     │                                                         │
     │ (1) User clicks "Login with Google"                    │
     │─────────────────────────────────────────────────────▶  │
     │                                                         │
     │ (2) Redirect to Authorization Server                   │
     │    with client_id, redirect_uri, scope, state          │
     │                                                         │
     │ (3) User authenticates & grants permission             │
     │◀────────────────────────────────────────────────────── │
     │                                                         │
     │ (4) Redirect to Client with authorization code         │
     │                                                         │
     ▼                                                         │
┌──────────────────┐                                          │
│   Client         │                                          │
│  (Backend)       │                                          │
└────┬─────────────┘                                          │
     │                                                         │
     │ (5) Exchange code for access token                     │
     │    POST with code, client_id, client_secret            │
     │─────────────────────────────────────────────────────▶  │
     │                                                         │
     │ (6) Return access_token & refresh_token                │
     │◀────────────────────────────────────────────────────── │
     │                                                         │
     │ (7) Use access token to call API                       │
     │                                                         │
     ▼                                                         ▼
┌──────────────────┐
│   Resource       │
│    Server        │
└──────────────────┘
```

**Flow Steps:**
1. User initiates login
2. Client redirects to authorization server with parameters
3. User authenticates and grants permission
4. Authorization server redirects back with authorization code
5. Client exchanges code for access token (server-to-server)
6. Authorization server returns access token and refresh token
7. Client uses access token to access protected resources

**Parameters:**
- `response_type=code`
- `client_id`: Your application's identifier
- `redirect_uri`: Where to redirect after authorization
- `scope`: Requested permissions
- `state`: CSRF protection token

#### 2. Implicit Flow (Deprecated)

**Best for**: Previously used for SPAs (now deprecated in favor of Authorization Code + PKCE)

**Description**: Access token is returned directly in the URL fragment without an intermediate authorization code.

```
┌──────────┐                                          ┌──────────────────┐
│  User    │                                          │  Authorization   │
│ (Browser)│                                          │     Server       │
└────┬─────┘                                          └────────┬─────────┘
     │                                                         │
     │ (1) Redirect to Authorization Server                   │
     │    with response_type=token                            │
     │─────────────────────────────────────────────────────▶  │
     │                                                         │
     │ (2) User authenticates & grants permission             │
     │                                                         │
     │ (3) Redirect with access token in URL fragment         │
     │    http://client.com/callback#access_token=xyz         │
     │◀────────────────────────────────────────────────────── │
     │                                                         │
     ▼                                                         ▼

⚠️  DEPRECATED: Not recommended due to security concerns
    - Tokens exposed in browser history
    - No refresh tokens
    - Use Authorization Code + PKCE instead
```

#### 3. Resource Owner Password Credentials Flow

**Best for**: Trusted first-party applications only (not recommended for third-party apps)

**Description**: User provides credentials directly to the client application, which exchanges them for an access token.

```
┌──────────┐
│  User    │
└────┬─────┘
     │
     │ (1) User enters username & password directly in app
     │
     ▼
┌──────────────────┐                                  ┌──────────────────┐
│     Client       │                                  │  Authorization   │
│  (Application)   │                                  │     Server       │
└────┬─────────────┘                                  └────────┬─────────┘
     │                                                         │
     │ (2) POST request with:                                 │
     │     - grant_type=password                              │
     │     - username                                         │
     │     - password                                         │
     │     - client_id & client_secret                        │
     │─────────────────────────────────────────────────────▶  │
     │                                                         │
     │ (3) Validate credentials                               │
     │                                                         │
     │ (4) Return access_token & refresh_token                │
     │◀────────────────────────────────────────────────────── │
     │                                                         │
     ▼                                                         ▼

⚠️  USE WITH CAUTION:
    - Only for highly trusted applications (own company apps)
    - User credentials exposed to client
    - No OAuth benefits for third-party apps
```

**When to use:**
- Mobile apps for your own service
- Migration from legacy authentication systems
- Testing and development

#### 4. Client Credentials Flow

**Best for**: Server-to-server (machine-to-machine) authentication

**Description**: Client authenticates using its own credentials, no user involvement.

```
┌──────────────────┐                                  ┌──────────────────┐
│     Client       │                                  │  Authorization   │
│  (Application/   │                                  │     Server       │
│   Service)       │                                  │                  │
└────┬─────────────┘                                  └────────┬─────────┘
     │                                                         │
     │ (1) POST request with:                                 │
     │     - grant_type=client_credentials                    │
     │     - client_id                                        │
     │     - client_secret                                    │
     │     - scope (optional)                                 │
     │─────────────────────────────────────────────────────▶  │
     │                                                         │
     │ (2) Validate client credentials                        │
     │                                                         │
     │ (3) Return access_token                                │
     │◀────────────────────────────────────────────────────── │
     │                                                         │
     │ (4) Use access token to call API                       │
     │                                                         │
     ▼                                                         ▼
┌──────────────────┐
│   Resource       │
│    Server        │
│   (API)          │
└──────────────────┘
```

**Use Cases:**
- Microservices authentication
- Batch jobs accessing APIs
- Background services
- Server-to-server API calls

**Characteristics:**
- No user context or refresh tokens
- Client acts on its own behalf
- Tokens typically short-lived

#### 5. Device Authorization Grant (Device Code Flow)

**Best for**: Devices with limited input capabilities (Smart TVs, IoT devices)

```
┌──────────────────┐                                  ┌──────────────────┐
│     Device       │                                  │  Authorization   │
│  (Smart TV)      │                                  │     Server       │
└────┬─────────────┘                                  └────────┬─────────┘
     │                                                         │
     │ (1) POST to /device/code endpoint                      │
     │─────────────────────────────────────────────────────▶  │
     │                                                         │
     │ (2) Return device_code, user_code,                     │
     │     verification_uri                                   │
     │◀────────────────────────────────────────────────────── │
     │                                                         │
     │ (3) Display: "Go to google.com/device                  │
     │              and enter code: ABCD-1234"                │
     │                                                         │
     │                           ┌──────────┐                 │
     │                           │  User    │                 │
     │                           │ (Phone)  │                 │
     │                           └────┬─────┘                 │
     │                                │                       │
     │                                │ (4) Visit URL         │
     │                                │     Enter code        │
     │                                │─────────────────────▶ │
     │                                │                       │
     │                                │ (5) Authenticate      │
     │                                │     & authorize       │
     │                                │                       │
     │ (6) Poll for token                                     │
     │    (every few seconds)                                 │
     │─────────────────────────────────────────────────────▶  │
     │                                                         │
     │ (7) Return access_token when user completes            │
     │◀────────────────────────────────────────────────────── │
     │                                                         │
     ▼                                                         ▼
```

### OAuth 2.0 Concepts

#### JWT (JSON Web Token)

**Description**: A compact, URL-safe token format for representing claims between two parties.

**Structure**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

┌─────────────── Header ──────────────┐   ┌────────────── Payload ─────────────┐   ┌──── Signature ────┐
│                                      │   │                                     │   │                   │
│ {                                    │ . │ {                                   │ . │ HMACSHA256(       │
│   "alg": "HS256",                    │   │   "sub": "1234567890",              │   │   base64(header)  │
│   "typ": "JWT"                       │   │   "name": "John Doe",               │   │   + "." +         │
│ }                                    │   │   "iat": 1516239022,                │   │   base64(payload),│
│                                      │   │   "exp": 1516242622,                │   │   secret          │
└──────────────────────────────────────┘   │   "scope": "read:user"              │   │ )                 │
                                            │ }                                   │   │                   │
                                            └─────────────────────────────────────┘   └───────────────────┘
```

**Parts**:
1. **Header**: Algorithm and token type
2. **Payload**: Claims (user data, permissions, expiration)
3. **Signature**: Ensures token integrity

**Benefits**:
- Self-contained: Contains all necessary information
- Stateless: No server-side session storage needed
- Verifiable: Signature prevents tampering

**Common Claims**:
- `iss` (issuer): Who created the token
- `sub` (subject): Who the token is about
- `aud` (audience): Who the token is intended for
- `exp` (expiration): When the token expires
- `iat` (issued at): When the token was created
- `scope`: Permissions granted

#### Token Exchange

**Description**: Process of exchanging one type of token for another, or refreshing an expired access token.

**Access Token vs Refresh Token**:

```
┌─────────────────────────────────────────────────────────────┐
│                    Token Lifecycle                          │
└─────────────────────────────────────────────────────────────┘

Initial Authorization:
─────────────────────
Authorization Server returns both tokens:
  ├─ Access Token  (short-lived: 1 hour)
  └─ Refresh Token (long-lived: 30 days)

Using Access Token:
──────────────────
Client → Resource Server
  Header: Authorization: Bearer <access_token>
  
Access Token Expires:
────────────────────
┌──────────────────┐                              ┌──────────────────┐
│     Client       │                              │  Authorization   │
└────┬─────────────┘                              │     Server       │
     │                                            └────────┬─────────┘
     │ POST /token                                         │
     │  grant_type=refresh_token                          │
     │  refresh_token=<refresh_token>                     │
     │  client_id & client_secret                         │
     │─────────────────────────────────────────────────▶  │
     │                                                     │
     │ New access_token & refresh_token                   │
     │◀─────────────────────────────────────────────────  │
     │                                                     │
     ▼                                                     ▼
```

**Token Refresh Flow**:
1. Access token expires
2. Client sends refresh token to authorization server
3. Server validates refresh token
4. Server issues new access token (and optionally new refresh token)
5. Client uses new access token

#### JWKS (JSON Web Key Set)

**Description**: A set of public keys used to verify JWT signatures.

**Purpose**:
- Allows resource servers to verify tokens without sharing secrets
- Enables key rotation without service interruption
- Supports multiple keys simultaneously

**Structure**:
```json
{
  "keys": [
    {
      "kty": "RSA",
      "use": "sig",
      "kid": "key-id-1",
      "n": "0vx7agoebGcQSuuPiLJXZptN9nndrQmbXEps2aiAFbWhM78LhWx...",
      "e": "AQAB"
    },
    {
      "kty": "RSA",
      "use": "sig", 
      "kid": "key-id-2",
      "n": "xjlCRBqkQxrXLhAz4rCuYn8FaEH3xPFgPAp1cYcPwzPnHdkN...",
      "e": "AQAB"
    }
  ]
}
```

**How It Works**:
```
┌──────────────────┐                              ┌──────────────────┐
│  Authorization   │                              │   Resource       │
│     Server       │                              │    Server        │
└────┬─────────────┘                              └────────┬─────────┘
     │                                                     │
     │ (1) Publishes JWKS at                              │
     │     /.well-known/jwks.json                         │
     │◀────────────────────────────────────────────────── │
     │                                                     │
     │ (2) Resource server fetches                        │
     │     public keys & caches them                      │
     │                                                     │
     ▼                                                     │
                                                           │
┌──────────────────┐                                      │
│     Client       │                                      │
└────┬─────────────┘                                      │
     │                                                     │
     │ (3) Request with JWT                               │
     │    Authorization: Bearer <jwt>                     │
     │─────────────────────────────────────────────────▶  │
     │                                                     │
     │ (4) Resource server:                               │
     │     - Extracts 'kid' from JWT header               │
     │     - Finds matching key in JWKS                   │
     │     - Verifies signature                           │
     │     - Validates claims (exp, aud, etc.)            │
     │                                                     │
     │ (5) Returns protected resource                     │
     │◀─────────────────────────────────────────────────  │
     │                                                     │
     ▼                                                     ▼
```

**Benefits**:
- No shared secrets between services
- Supports asymmetric encryption (public/private keys)
- Enables distributed token verification
- Allows key rotation

### PKCE (Proof Key for Code Exchange)

#### What is PKCE?

**PKCE** (pronounced "pixy") is an extension to OAuth 2.0 Authorization Code Flow that provides additional security, especially for public clients (mobile apps, SPAs) that cannot securely store client secrets.

**Pronunciation**: "pixy"  
**RFC**: RFC 7636

#### Why is PKCE Needed?

**Security Vulnerabilities in Standard OAuth 2.0**:

1. **Authorization Code Interception**: 
   - Mobile apps use custom URL schemes (e.g., `myapp://callback`)
   - Malicious apps can register the same URL scheme
   - Attacker can intercept the authorization code

2. **No Client Secret Protection**:
   - Public clients (SPAs, mobile apps) cannot securely store secrets
   - Client secrets embedded in apps can be extracted
   - Compromised secrets affect all users

**Attack Scenario Without PKCE**:
```
┌──────────┐                                          ┌──────────────────┐
│  User    │                                          │  Authorization   │
│ (Mobile) │                                          │     Server       │
└────┬─────┘                                          └────────┬─────────┘
     │                                                         │
     │ (1) Login request                                      │
     │─────────────────────────────────────────────────────▶  │
     │                                                         │
     │ (2) Redirect: myapp://callback?code=AUTH_CODE          │
     │◀────────────────────────────────────────────────────── │
     │                                                         │
     X  INTERCEPTED BY MALICIOUS APP!                         │
     │                                                         │
┌────▼─────────────┐                                          │
│  Malicious App   │                                          │
│  (registered     │                                          │
│   myapp://)      │                                          │
└────┬─────────────┘                                          │
     │                                                         │
     │ (3) Exchange code for token                            │
     │    (no secret needed for public clients)               │
     │─────────────────────────────────────────────────────▶  │
     │                                                         │
     │ (4) Access token (COMPROMISED!)                        │
     │◀────────────────────────────────────────────────────── │
     │                                                         │
     ▼                                                         ▼
```

#### How PKCE Works

PKCE adds a cryptographic challenge to the authorization flow:

```
┌─────────────────────────────────────────────────────────────┐
│                     PKCE Flow                                │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐
│     Client       │
│  (Mobile App)    │
└────┬─────────────┘
     │
     │ (1) Generate code_verifier (random string)
     │     code_verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
     │
     │ (2) Generate code_challenge
     │     code_challenge = BASE64URL(SHA256(code_verifier))
     │     code_challenge = "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"
     │
     │ (3) Authorization request with code_challenge
     │     /authorize?
     │       response_type=code
     │       &client_id=CLIENT_ID
     │       &redirect_uri=myapp://callback
     │       &code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM
     │       &code_challenge_method=S256
     │
     ▼
┌──────────────────┐                              ┌──────────────────┐
│  User (Browser)  │                              │  Authorization   │
└────┬─────────────┘                              │     Server       │
     │                                            └────────┬─────────┘
     │                                                     │
     │ ───────────────────────────────────────────────▶   │
     │                                                     │
     │                                                     │ (4) Store code_challenge
     │                                                     │     with authorization code
     │                                                     │
     │ (5) Redirect: myapp://callback?code=AUTH_CODE      │
     │◀─────────────────────────────────────────────────  │
     │                                                     │
     ▼                                                     │
┌──────────────────┐                                      │
│     Client       │                                      │
│  (Mobile App)    │                                      │
└────┬─────────────┘                                      │
     │                                                     │
     │ (6) Token request with original code_verifier      │
     │     POST /token                                    │
     │       grant_type=authorization_code                │
     │       &code=AUTH_CODE                              │
     │       &redirect_uri=myapp://callback               │
     │       &client_id=CLIENT_ID                         │
     │       &code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU... │
     │─────────────────────────────────────────────────▶  │
     │                                                     │
     │                                                     │ (7) Verify:
     │                                                     │     SHA256(code_verifier)
     │                                                     │     == code_challenge
     │                                                     │
     │ (8) Return access_token (only if verified!)        │
     │◀─────────────────────────────────────────────────  │
     │                                                     │
     ▼                                                     ▼
```

**PKCE Parameters**:

1. **code_verifier**: 
   - Random cryptographic string (43-128 characters)
   - Created by client, kept secret
   - Example: `dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk`

2. **code_challenge**:
   - Derived from code_verifier
   - Sent in authorization request
   - Method: `plain` or `S256` (SHA-256 hash)
   - Example: `BASE64URL(SHA256(code_verifier))`

3. **code_challenge_method**:
   - `S256`: SHA-256 hash (recommended)
   - `plain`: Use verifier as-is (not recommended)

#### PKCE Security Benefits

**Protection Against Interception**:
```
Even if authorization code is intercepted:

┌────────────────────┐
│  Malicious App     │
│  (has auth code)   │
└────┬───────────────┘
     │
     │ (1) Tries to exchange code for token
     │     POST /token
     │       code=INTERCEPTED_CODE
     │       client_id=CLIENT_ID
     │       (no code_verifier!)
     │
     ▼
┌──────────────────┐
│  Authorization   │
│     Server       │
└────┬─────────────┘
     │
     │ (2) REJECTED!
     │     - Missing code_verifier
     │     - OR wrong code_verifier
     │     - Cannot generate valid code_challenge
     │
     ▼
     X  Attack prevented!
```

**Key Security Properties**:

1. **Dynamic Secret**: 
   - New code_verifier for each authorization flow
   - Cannot be pre-computed or reused

2. **One-way Function**:
   - code_challenge derived from code_verifier (SHA-256)
   - Cannot reverse-engineer verifier from challenge

3. **Client Binding**:
   - Only the client that started the flow can complete it
   - Intercepted code is useless without verifier

4. **No Shared Secrets**:
   - No client_secret needed
   - Perfect for public clients

#### PKCE vs Standard OAuth 2.0

| Aspect | Standard OAuth 2.0 | OAuth 2.0 + PKCE |
|--------|-------------------|------------------|
| **Client Secret** | Required for confidential clients | Not required |
| **Code Interception** | Vulnerable | Protected |
| **Public Clients** | Less secure | Highly secure |
| **Mobile Apps** | Risky | Recommended |
| **SPAs** | Implicit flow (deprecated) | Authorization Code + PKCE |
| **Complexity** | Simpler | Slightly more complex |
| **Security** | Good for confidential clients | Excellent for all clients |

#### When to Use PKCE

✅ **Always Use PKCE For**:
- Mobile applications (iOS, Android)
- Single Page Applications (SPAs)
- Desktop applications
- Any public client that cannot securely store secrets

✅ **Recommended Even For**:
- Server-side web applications (defense in depth)
- All new OAuth 2.0 implementations

❌ **Not Applicable For**:
- Client Credentials flow (no user interaction)
- Resource Owner Password flow (deprecated)

#### Implementation Example

**Step 1: Generate Code Verifier and Challenge**
```javascript
// Generate code_verifier (random string)
function generateCodeVerifier() {
  const array = new Uint8Array(32);
  crypto.getRandomValues(array);
  return base64URLEncode(array);
}

// Generate code_challenge from verifier
async function generateCodeChallenge(verifier) {
  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const hash = await crypto.subtle.digest('SHA-256', data);
  return base64URLEncode(new Uint8Array(hash));
}
```

**Step 2: Authorization Request**
```http
GET /authorize?
  response_type=code&
  client_id=YOUR_CLIENT_ID&
  redirect_uri=https://yourapp.com/callback&
  scope=read:user&
  state=random_state&
  code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM&
  code_challenge_method=S256
```

**Step 3: Token Request**
```http
POST /token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&
code=AUTHORIZATION_CODE&
redirect_uri=https://yourapp.com/callback&
client_id=YOUR_CLIENT_ID&
code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
```

#### Summary

PKCE is a critical security enhancement for OAuth 2.0 that:
- ✅ Prevents authorization code interception attacks
- ✅ Eliminates need for client secrets in public clients
- ✅ Provides cryptographic binding between authorization and token requests
- ✅ Is now recommended for ALL OAuth 2.0 clients
- ✅ Is mandatory for SPAs and mobile apps

**Best Practice**: Always use PKCE with Authorization Code flow for modern applications.