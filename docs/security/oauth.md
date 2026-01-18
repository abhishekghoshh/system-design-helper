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

### Client Registration Process

Before a client application can use OAuth 2.0, it must be registered with the **Authorization Server**. This registration process establishes trust and provides the client with credentials needed for authentication.

#### Why Client Registration is Required

- **Identify the Application**: Each client gets a unique identifier (`client_id`)
- **Security**: Confidential clients receive a `client_secret` for authentication
- **Validate Redirects**: Authorization server maintains allowed redirect URIs to prevent attacks
- **Configure Permissions**: Define what scopes/permissions the client can request
- **Track Usage**: Monitor and audit client application activity

#### Client Types

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Types                             │
└─────────────────────────────────────────────────────────────┘

1. CONFIDENTIAL CLIENTS
   ├─ Can securely store credentials
   ├─ Have both client_id AND client_secret
   ├─ Run on secure servers
   └─ Examples:
      ├─ Server-side web applications (Node.js, Django, Spring)
      ├─ Backend services
      └─ Microservices

2. PUBLIC CLIENTS
   ├─ Cannot securely store secrets
   ├─ Have only client_id (NO client_secret)
   ├─ Code is accessible to users
   └─ Examples:
      ├─ Single Page Applications (React, Vue, Angular)
      ├─ Mobile apps (iOS, Android)
      ├─ Desktop applications
      └─ Browser-based apps
```

#### Registration Process

**Manual Registration (Most Common)**:

```
┌──────────────────┐                                  ┌──────────────────┐
│   Developer      │                                  │  Authorization   │
│                  │                                  │     Server       │
│                  │                                  │  (e.g., Google,  │
│                  │                                  │   Auth0, Okta)   │
└────┬─────────────┘                                  └────────┬─────────┘
     │                                                         │
     │ (1) Navigate to Developer Console/Portal               │
     │     (e.g., console.cloud.google.com)                   │
     │                                                         │
     │ (2) Fill Registration Form:                            │
     │     - Application Name                                 │
     │     - Application Type (Web, SPA, Mobile, etc.)        │
     │     - Redirect URIs                                    │
     │     - Allowed Scopes                                   │
     │     - Application Logo & Description                   │
     │─────────────────────────────────────────────────────▶  │
     │                                                         │
     │                                                         │ (3) Validate Input
     │                                                         │     - Check redirect URIs
     │                                                         │     - Verify application details
     │                                                         │
     │ (4) Return Client Credentials:                         │
     │     ┌────────────────────────────────────────┐         │
     │     │ client_id: abc123xyz456                │         │
     │     │ client_secret: secret_abc123 (if conf.)|         │
     │     │ redirect_uris: [...]                   │         │
     │     │ allowed_scopes: [...]                  │         │
     │     └────────────────────────────────────────┘         │
     │◀────────────────────────────────────────────────────── │
     │                                                         │
     │ (5) Store credentials securely                         │
     │                                                         │
     ▼                                                         ▼
```

**Dynamic Client Registration (RFC 7591)**:

For automated registration via API:

```
┌──────────────────┐                                  ┌──────────────────┐
│   Client App     │                                  │  Authorization   │
│                  │                                  │     Server       │
└────┬─────────────┘                                  └────────┬─────────┘
     │                                                         │
     │ POST /register                                         │
     │ Content-Type: application/json                         │
     │                                                         │
     │ {                                                       │
     │   "redirect_uris": [                                   │
     │     "https://client.example.com/callback"              │
     │   ],                                                    │
     │   "client_name": "My Application",                     │
     │   "token_endpoint_auth_method": "client_secret_basic", │
     │   "grant_types": ["authorization_code", "refresh"],    │
     │   "response_types": ["code"],                          │
     │   "scope": "read write"                                │
     │ }                                                       │
     │─────────────────────────────────────────────────────▶  │
     │                                                         │
     │                                                         │ Validate & Create
     │                                                         │
     │ Response:                                              │
     │ {                                                       │
     │   "client_id": "s6BhdRkqt3",                           │
     │   "client_secret": "ZJYCqe3GGRvdrudKyZS0XhGv...",      │
     │   "client_id_issued_at": 1234567890,                   │
     │   "client_secret_expires_at": 1234657890,              │
     │   "redirect_uris": [...],                              │
     │   "grant_types": [...],                                │
     │   "response_types": [...]                              │
     │ }                                                       │
     │◀────────────────────────────────────────────────────── │
     │                                                         │
     ▼                                                         ▼
```

#### Registration Information

**Required Information**:

| Field | Description | Example |
|-------|-------------|---------|
| **client_id** | Unique identifier for the client | `abc123xyz456` |
| **client_secret** | Secret key (confidential clients only) | `secret_abc123...` |
| **redirect_uris** | Allowed callback URLs after authorization | `["https://app.com/callback"]` |
| **application_name** | Human-readable name | "My Photo App" |
| **application_type** | Type of client | `web`, `native`, `spa` |
| **grant_types** | Allowed OAuth flows | `["authorization_code", "refresh_token"]` |
| **response_types** | Allowed response types | `["code"]` |
| **scopes** | Permissions the client can request | `["read:user", "write:user"]` |

**Optional Information**:
- **logo_uri**: URL to application logo
- **tos_uri**: Terms of service URL
- **policy_uri**: Privacy policy URL
- **contacts**: Developer contact emails
- **jwks_uri**: JSON Web Key Set URL for token validation

#### Redirect URI Security

**Critical Security Requirement**: Redirect URIs must be explicitly registered to prevent authorization code interception.

```
Valid Redirect URIs:
───────────────────
✅ https://app.example.com/callback
✅ https://app.example.com/oauth/callback
✅ myapp://callback (mobile app custom scheme)
✅ http://localhost:3000/callback (development only)

Invalid/Risky Patterns:
──────────────────────
❌ https://app.example.com/* (wildcard not allowed)
❌ http://app.example.com/callback (HTTP in production)
❌ https://evil.com/callback (not registered)
❌ https://app.example.com/callback?param=value (query params)

Attack Prevention:
─────────────────
If attacker tries: https://evil.com/steal
→ Authorization server checks registered URIs
→ Redirect URI doesn't match
→ Request REJECTED
→ Attack prevented!
```

#### Post-Registration Steps

1. **Secure Storage**:
   ```
   Confidential Clients (Server-side):
   - Store client_secret in environment variables
   - Use secret management services (AWS Secrets Manager, HashiCorp Vault)
   - Never commit to version control
   
   Public Clients:
   - Only client_id needed
   - Can be in client-side code
   - Use PKCE for additional security
   ```

2. **Configure Application**:
   ```javascript
   // Server-side (Confidential)
   const oauth2Config = {
     client_id: process.env.OAUTH_CLIENT_ID,
     client_secret: process.env.OAUTH_CLIENT_SECRET,
     redirect_uri: 'https://yourapp.com/callback',
     authorization_endpoint: 'https://auth-server.com/oauth/authorize',
     token_endpoint: 'https://auth-server.com/oauth/token'
   };
   
   // Client-side (Public)
   const oauth2Config = {
     client_id: 'abc123xyz456', // Public, can be in code
     redirect_uri: 'https://yourapp.com/callback',
     authorization_endpoint: 'https://auth-server.com/oauth/authorize',
     token_endpoint: 'https://auth-server.com/oauth/token',
     usePKCE: true // Always use PKCE for public clients
   };
   ```

3. **Test the Integration**:
   - Use development/sandbox environment first
   - Verify redirect URIs work correctly
   - Test token exchange process
   - Validate scope permissions

#### Client Management

**Update Client Configuration**:
- Modify redirect URIs
- Update scopes
- Rotate client secrets (confidential clients)
- Change application metadata

**Revoke/Delete Client**:
- Immediately invalidates all tokens
- Remove client from authorization server
- Users must re-authorize if client is re-registered

**Monitor Client Activity**:
- Track token issuance rates
- Monitor failed authentication attempts
- Audit scope usage
- Detect suspicious patterns

#### Real-World Examples

**Google OAuth Registration**:
1. Go to Google Cloud Console
2. Create a new project
3. Enable OAuth 2.0 APIs
4. Configure OAuth consent screen
5. Create credentials (OAuth 2.0 Client ID)
6. Specify application type and redirect URIs
7. Receive `client_id` and `client_secret`

**GitHub OAuth Registration**:
1. Go to Settings → Developer settings → OAuth Apps
2. Click "New OAuth App"
3. Fill in application details and callback URL
4. Receive `client_id` and `client_secret`

**Auth0 Registration**:
1. Create an Auth0 account
2. Create a new application
3. Choose application type (SPA, Web, Native)
4. Configure allowed callback URLs
5. Receive `client_id` and `client_secret`

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

**Python Implementation Example:**

```python
import requests
import secrets
from urllib.parse import urlencode, urlparse, parse_qs
from flask import Flask, request, redirect, session

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# OAuth 2.0 Configuration
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
AUTHORIZATION_URL = 'https://auth-server.com/oauth/authorize'
TOKEN_URL = 'https://auth-server.com/oauth/token'
REDIRECT_URI = 'http://localhost:5000/callback'
SCOPE = 'read:user write:user'

@app.route('/login')
def login():
    """Step 1: Redirect user to authorization server"""
    # Generate state for CSRF protection
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    
    # Build authorization URL
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE,
        'state': state
    }
    
    authorization_url = f"{AUTHORIZATION_URL}?{urlencode(params)}"
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    """Step 2: Handle callback and exchange code for token"""
    # Verify state to prevent CSRF
    state = request.args.get('state')
    if state != session.get('oauth_state'):
        return 'Invalid state parameter', 400
    
    # Get authorization code
    code = request.args.get('code')
    if not code:
        error = request.args.get('error', 'Unknown error')
        return f'Authorization failed: {error}', 400
    
    # Exchange code for access token
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    
    response = requests.post(TOKEN_URL, data=token_data)
    
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access_token']
        refresh_token = tokens.get('refresh_token')
        
        # Store tokens securely (use encrypted session/database in production)
        session['access_token'] = access_token
        session['refresh_token'] = refresh_token
        
        return 'Login successful! Access token obtained.'
    else:
        return f'Token exchange failed: {response.text}', 400

@app.route('/api/user')
def get_user():
    """Step 3: Use access token to call protected API"""
    access_token = session.get('access_token')
    if not access_token:
        return 'Not authenticated', 401
    
    # Call protected API with access token
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api-server.com/user', headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        # Token expired, need to refresh
        return 'Token expired', 401
    else:
        return f'API call failed: {response.text}', response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

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

**Python Implementation Example:**

```python
import requests
from typing import Dict, Optional

class PasswordGrantClient:
    def __init__(self, client_id: str, client_secret: str, token_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.access_token = None
        self.refresh_token = None
    
    def authenticate(self, username: str, password: str, scope: str = '') -> Dict:
        """Authenticate using username and password"""
        token_data = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': scope
        }
        
        response = requests.post(self.token_url, data=token_data)
        
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens['access_token']
            self.refresh_token = tokens.get('refresh_token')
            return tokens
        else:
            raise Exception(f'Authentication failed: {response.text}')
    
    def call_api(self, api_url: str, method: str = 'GET', data: Optional[Dict] = None) -> Dict:
        """Make authenticated API request"""
        if not self.access_token:
            raise Exception('Not authenticated')
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        
        if method == 'GET':
            response = requests.get(api_url, headers=headers)
        elif method == 'POST':
            response = requests.post(api_url, headers=headers, json=data)
        else:
            raise ValueError(f'Unsupported method: {method}')
        
        response.raise_for_status()
        return response.json()

# Usage Example
if __name__ == '__main__':
    client = PasswordGrantClient(
        client_id='your_client_id',
        client_secret='your_client_secret',
        token_url='https://auth-server.com/oauth/token'
    )
    
    try:
        # Authenticate
        tokens = client.authenticate(
            username='user@example.com',
            password='user_password',
            scope='read write'
        )
        print(f"Access Token: {tokens['access_token']}")
        
        # Call protected API
        user_data = client.call_api('https://api-server.com/user')
        print(f"User Data: {user_data}")
        
    except Exception as e:
        print(f"Error: {e}")
```

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

**Python Implementation Example:**

```python
import requests
import time
from typing import Dict, Optional
from threading import Lock

class ClientCredentialsClient:
    def __init__(self, client_id: str, client_secret: str, token_url: str, scope: str = ''):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.scope = scope
        self.access_token = None
        self.token_expiry = 0
        self._lock = Lock()
    
    def get_access_token(self) -> str:
        """Get valid access token, refreshing if necessary"""
        with self._lock:
            # Check if token is still valid (with 60s buffer)
            if self.access_token and time.time() < (self.token_expiry - 60):
                return self.access_token
            
            # Request new token
            return self._request_token()
    
    def _request_token(self) -> str:
        """Request new access token using client credentials"""
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.scope
        }
        
        response = requests.post(self.token_url, data=token_data)
        
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens['access_token']
            expires_in = tokens.get('expires_in', 3600)
            self.token_expiry = time.time() + expires_in
            return self.access_token
        else:
            raise Exception(f'Token request failed: {response.text}')
    
    def call_api(self, api_url: str, method: str = 'GET', data: Optional[Dict] = None) -> Dict:
        """Make authenticated API request"""
        access_token = self.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}
        
        if method == 'GET':
            response = requests.get(api_url, headers=headers)
        elif method == 'POST':
            response = requests.post(api_url, headers=headers, json=data)
        elif method == 'PUT':
            response = requests.put(api_url, headers=headers, json=data)
        elif method == 'DELETE':
            response = requests.delete(api_url, headers=headers)
        else:
            raise ValueError(f'Unsupported method: {method}')
        
        response.raise_for_status()
        return response.json() if response.content else {}

# Usage Example - Microservice to Microservice Communication
if __name__ == '__main__':
    # Initialize client
    client = ClientCredentialsClient(
        client_id='service-a-client-id',
        client_secret='service-a-secret',
        token_url='https://auth-server.com/oauth/token',
        scope='api:read api:write'
    )
    
    try:
        # Call another service's API
        data = client.call_api('https://service-b.com/api/data')
        print(f"Data from Service B: {data}")
        
        # Create resource on another service
        new_resource = client.call_api(
            'https://service-b.com/api/resource',
            method='POST',
            data={'name': 'New Resource', 'value': 123}
        )
        print(f"Created: {new_resource}")
        
    except Exception as e:
        print(f"Error: {e}")
```

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

**Python Implementation Example:**

```python
import requests
import time
from typing import Dict

class DeviceFlowClient:
    def __init__(self, client_id: str, device_code_url: str, token_url: str):
        self.client_id = client_id
        self.device_code_url = device_code_url
        self.token_url = token_url
    
    def start_device_flow(self, scope: str = '') -> Dict:
        """Step 1: Request device and user codes"""
        data = {
            'client_id': self.client_id,
            'scope': scope
        }
        
        response = requests.post(self.device_code_url, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Device code request failed: {response.text}')
    
    def poll_for_token(self, device_code: str, interval: int = 5, timeout: int = 300) -> Dict:
        """Step 2: Poll for access token"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            token_data = {
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
                'device_code': device_code,
                'client_id': self.client_id
            }
            
            response = requests.post(self.token_url, data=token_data)
            
            if response.status_code == 200:
                # Success! User has authorized
                return response.json()
            
            error_data = response.json()
            error = error_data.get('error')
            
            if error == 'authorization_pending':
                # User hasn't completed authorization yet, wait and retry
                print('Waiting for user authorization...')
                time.sleep(interval)
            elif error == 'slow_down':
                # Increase polling interval
                interval += 5
                time.sleep(interval)
            elif error == 'expired_token':
                raise Exception('Device code expired. Please start over.')
            elif error == 'access_denied':
                raise Exception('User denied authorization')
            else:
                raise Exception(f'Token request failed: {response.text}')
        
        raise Exception('Timeout waiting for user authorization')
    
    def authenticate(self, scope: str = '') -> Dict:
        """Complete device flow authentication"""
        # Step 1: Get device code
        device_info = self.start_device_flow(scope)
        
        # Display instructions to user
        print(f"\n{'='*60}")
        print(f"Please visit: {device_info['verification_uri']}")
        print(f"And enter code: {device_info['user_code']}")
        print(f"{'='*60}\n")
        
        # Alternative: verification_uri_complete for QR codes
        if 'verification_uri_complete' in device_info:
            print(f"Or scan this URL: {device_info['verification_uri_complete']}\n")
        
        # Step 2: Poll for token
        interval = device_info.get('interval', 5)
        tokens = self.poll_for_token(device_info['device_code'], interval)
        
        return tokens

# Usage Example - Smart TV or IoT Device
if __name__ == '__main__':
    client = DeviceFlowClient(
        client_id='smart-tv-client-id',
        device_code_url='https://auth-server.com/oauth/device/code',
        token_url='https://auth-server.com/oauth/token'
    )
    
    try:
        # Start authentication flow
        tokens = client.authenticate(scope='tv:control media:play')
        
        print(f"\n✅ Authentication successful!")
        print(f"Access Token: {tokens['access_token'][:20]}...")
        
        # Now use the access token to call APIs
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        response = requests.get('https://api-server.com/user/profile', headers=headers)
        print(f"User Profile: {response.json()}")
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
```

#### 6. Refresh Token Grant

**Best for**: Obtaining new access tokens without user re-authentication

**Description**: Allows clients to obtain a new access token using a refresh token when the current access token expires, without requiring user interaction.

```
┌──────────────────┐                                  ┌──────────────────┐
│     Client       │                                  │  Authorization   │
│  (Application)   │                                  │     Server       │
└────┬─────────────┘                                  └────────┬─────────┘
     │                                                         │
     │ Initial authorization flow completed                   │
     │ Client has: access_token + refresh_token               │
     │                                                         │
     │ ═══════════════════════════════════════════════════════│
     │           Time passes... access_token expires          │
     │ ═══════════════════════════════════════════════════════│
     │                                                         │
     │ (1) Access token expired (401 Unauthorized)            │
     │                                                         │
     │ (2) POST /token with:                                  │
     │     - grant_type=refresh_token                         │
     │     - refresh_token=<refresh_token>                    │
     │     - client_id                                        │
     │     - client_secret (for confidential clients)         │
     │     - scope (optional, to request reduced scope)       │
     │─────────────────────────────────────────────────────▶  │
     │                                                         │
     │ (3) Validate refresh token:                            │
     │     - Check if not expired                             │
     │     - Check if not revoked                             │
     │     - Verify client credentials                        │
     │     - Validate requested scope                         │
     │                                                         │
     │ (4) Return new tokens:                                 │
     │     {                                                  │
     │       "access_token": "new_access_token",              │
     │       "token_type": "Bearer",                          │
     │       "expires_in": 3600,                              │
     │       "refresh_token": "new_refresh_token",            │
     │       "scope": "read write"                            │
     │     }                                                  │
     │◀────────────────────────────────────────────────────── │
     │                                                         │
     │ (5) Use new access_token                               │
     │                                                         │
     ▼                                                         ▼
┌──────────────────┐
│   Resource       │
│    Server        │
└──────────────────┘
```

**Key Characteristics**:

1. **No User Interaction**: Tokens renewed silently in background
2. **Refresh Token Rotation**: Best practice is to issue new refresh token with each use
3. **Reduced Scope**: Can request narrower permissions than original grant
4. **Long-Lived**: Refresh tokens typically valid for days/weeks/months
5. **Revocable**: Can be revoked by authorization server or user

**Security Considerations**:

```
Refresh Token Rotation (Recommended):
─────────────────────────────────────

Request 1:  refresh_token_1 → new access_token + refresh_token_2
Request 2:  refresh_token_2 → new access_token + refresh_token_3
Request 3:  refresh_token_3 → new access_token + refresh_token_4

Old refresh tokens are invalidated after use.

If refresh_token_1 is used again after refresh_token_2 was issued:
→ Token theft detected!
→ Revoke entire token family
→ User must re-authenticate
```

**Best Practices**:

- ✅ Implement refresh token rotation
- ✅ Store refresh tokens securely (encrypted, server-side)
- ✅ Set appropriate expiration times
- ✅ Implement token revocation endpoint
- ✅ Monitor for suspicious refresh patterns
- ✅ Limit refresh token lifetime
- ✅ Bind refresh tokens to specific clients

**Token Response Example**:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "tGzv3JOkF0XG5Qx2TlKWIA",
  "scope": "read write"
}
```

**Error Responses**:
```http
// Invalid or expired refresh token
{
  "error": "invalid_grant",
  "error_description": "The refresh token is invalid or expired"
}

// Refresh token has been revoked
{
  "error": "invalid_grant", 
  "error_description": "Token has been revoked"
}

// Invalid scope request
{
  "error": "invalid_scope",
  "error_description": "Requested scope exceeds original grant"
}
```

**Use Cases**:
- Mobile applications maintaining long-term access
- Background services that need continuous API access
- Web applications providing seamless user experience
- Reducing authentication friction for users

**Refresh Token vs Access Token**:

| Feature | Access Token | Refresh Token |
|---------|-------------|---------------|
| **Purpose** | Access protected resources | Obtain new access tokens |
| **Lifetime** | Short (minutes to hours) | Long (days to months) |
| **Sent to Resource Server** | Yes | No (only to auth server) |
| **Exposure Risk** | Higher (frequent use) | Lower (infrequent use) |
| **Can be Revoked** | Usually not individually | Yes |
| **Storage** | Memory/session storage | Secure persistent storage |

**Python Implementation Example:**

```python
import requests
import time
from typing import Dict, Optional
import json

class TokenManager:
    def __init__(self, client_id: str, client_secret: str, token_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = 0
    
    def set_tokens(self, access_token: str, refresh_token: str, expires_in: int = 3600):
        """Set initial tokens (from authorization code flow)"""
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expiry = time.time() + expires_in
    
    def refresh_access_token(self) -> Dict:
        """Refresh the access token using refresh token"""
        if not self.refresh_token:
            raise Exception('No refresh token available')
        
        token_data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        response = requests.post(self.token_url, data=token_data)
        
        if response.status_code == 200:
            tokens = response.json()
            
            # Update tokens
            self.access_token = tokens['access_token']
            # Server may issue new refresh token (rotation)
            if 'refresh_token' in tokens:
                self.refresh_token = tokens['refresh_token']
            
            expires_in = tokens.get('expires_in', 3600)
            self.token_expiry = time.time() + expires_in
            
            return tokens
        else:
            error = response.json()
            if error.get('error') == 'invalid_grant':
                # Refresh token expired or revoked
                raise Exception('Refresh token invalid. Please re-authenticate.')
            raise Exception(f'Token refresh failed: {response.text}')
    
    def get_valid_access_token(self) -> str:
        """Get valid access token, automatically refreshing if needed"""
        # Check if token is expired or about to expire (60s buffer)
        if not self.access_token or time.time() >= (self.token_expiry - 60):
            if self.refresh_token:
                print('Access token expired, refreshing...')
                self.refresh_access_token()
            else:
                raise Exception('No valid access token and no refresh token')
        
        return self.access_token
    
    def call_api_with_retry(self, api_url: str, method: str = 'GET', 
                           data: Optional[Dict] = None, max_retries: int = 1) -> Dict:
        """Call API with automatic token refresh on 401 errors"""
        for attempt in range(max_retries + 1):
            try:
                access_token = self.get_valid_access_token()
                headers = {'Authorization': f'Bearer {access_token}'}
                
                if method == 'GET':
                    response = requests.get(api_url, headers=headers)
                elif method == 'POST':
                    response = requests.post(api_url, headers=headers, json=data)
                else:
                    raise ValueError(f'Unsupported method: {method}')
                
                if response.status_code == 401 and attempt < max_retries:
                    # Token might be invalid, try refreshing
                    print('Received 401, attempting to refresh token...')
                    self.refresh_access_token()
                    continue
                
                response.raise_for_status()
                return response.json() if response.content else {}
                
            except requests.exceptions.HTTPError as e:
                if attempt >= max_retries:
                    raise
        
        raise Exception('Max retries exceeded')
    
    def save_tokens(self, filepath: str):
        """Save tokens to file (encrypt in production!)"""
        tokens = {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'token_expiry': self.token_expiry
        }
        with open(filepath, 'w') as f:
            json.dump(tokens, f)
    
    def load_tokens(self, filepath: str):
        """Load tokens from file"""
        try:
            with open(filepath, 'r') as f:
                tokens = json.load(f)
                self.access_token = tokens['access_token']
                self.refresh_token = tokens['refresh_token']
                self.token_expiry = tokens['token_expiry']
        except FileNotFoundError:
            pass

# Usage Example
if __name__ == '__main__':
    token_manager = TokenManager(
        client_id='your_client_id',
        client_secret='your_client_secret',
        token_url='https://auth-server.com/oauth/token'
    )
    
    # Set initial tokens (from authorization code flow)
    token_manager.set_tokens(
        access_token='initial_access_token',
        refresh_token='initial_refresh_token',
        expires_in=3600
    )
    
    try:
        # Make API calls - tokens will be automatically refreshed
        user_data = token_manager.call_api_with_retry(
            'https://api-server.com/user/profile'
        )
        print(f"User Profile: {user_data}")
        
        # Save tokens for later use
        token_manager.save_tokens('tokens.json')
        
        # Simulate token expiration
        time.sleep(2)
        token_manager.token_expiry = time.time() - 100  # Force expiry
        
        # This will automatically refresh the token
        posts = token_manager.call_api_with_retry(
            'https://api-server.com/user/posts'
        )
        print(f"User Posts: {posts}")
        
    except Exception as e:
        print(f"Error: {e}")
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

#### Complete Python Implementation

```python
import secrets
import hashlib
import base64
import requests
from urllib.parse import urlencode, urlparse, parse_qs
from flask import Flask, request, redirect, session, jsonify

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# OAuth 2.0 Configuration
CLIENT_ID = 'your_client_id'
AUTHORIZATION_URL = 'https://auth-server.com/oauth/authorize'
TOKEN_URL = 'https://auth-server.com/oauth/token'
REDIRECT_URI = 'http://localhost:5000/callback'
SCOPE = 'read:user write:user'

class PKCEHelper:
    """Helper class for PKCE implementation"""
    
    @staticmethod
    def generate_code_verifier(length: int = 128) -> str:
        """Generate a cryptographically random code verifier.
        
        Args:
            length: Length of verifier (43-128 characters)
        
        Returns:
            URL-safe base64 encoded string
        """
        if length < 43 or length > 128:
            raise ValueError('Code verifier length must be between 43 and 128')
        
        # Generate random bytes
        random_bytes = secrets.token_bytes(length)
        
        # Base64 URL encode (without padding)
        code_verifier = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
        code_verifier = code_verifier.rstrip('=')
        
        # Ensure length is within bounds
        return code_verifier[:length]
    
    @staticmethod
    def generate_code_challenge(code_verifier: str, method: str = 'S256') -> str:
        """Generate code challenge from verifier.
        
        Args:
            code_verifier: The code verifier string
            method: 'S256' (SHA-256) or 'plain'
        
        Returns:
            Code challenge string
        """
        if method == 'S256':
            # SHA-256 hash
            digest = hashlib.sha256(code_verifier.encode('utf-8')).digest()
            # Base64 URL encode (without padding)
            code_challenge = base64.urlsafe_b64encode(digest).decode('utf-8')
            return code_challenge.rstrip('=')
        elif method == 'plain':
            # Use verifier as-is (not recommended)
            return code_verifier
        else:
            raise ValueError(f'Unsupported method: {method}')

@app.route('/login')
def login():
    """Initiate OAuth 2.0 with PKCE flow"""
    # Generate PKCE parameters
    code_verifier = PKCEHelper.generate_code_verifier()
    code_challenge = PKCEHelper.generate_code_challenge(code_verifier, 'S256')
    
    # Store code_verifier in session (needed for token exchange)
    session['code_verifier'] = code_verifier
    
    # Generate state for CSRF protection
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    
    # Build authorization URL with PKCE parameters
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE,
        'state': state,
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }
    
    authorization_url = f"{AUTHORIZATION_URL}?{urlencode(params)}"
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    """Handle OAuth callback and exchange code for token with PKCE"""
    # Verify state parameter
    state = request.args.get('state')
    if state != session.get('oauth_state'):
        return jsonify({'error': 'Invalid state parameter'}), 400
    
    # Get authorization code
    code = request.args.get('code')
    if not code:
        error = request.args.get('error', 'Unknown error')
        error_description = request.args.get('error_description', '')
        return jsonify({
            'error': error,
            'error_description': error_description
        }), 400
    
    # Retrieve code_verifier from session
    code_verifier = session.get('code_verifier')
    if not code_verifier:
        return jsonify({'error': 'Missing code verifier'}), 400
    
    # Exchange authorization code for access token with code_verifier
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'code_verifier': code_verifier  # PKCE parameter
    }
    
    # Note: No client_secret needed for public clients with PKCE!
    
    response = requests.post(TOKEN_URL, data=token_data)
    
    if response.status_code == 200:
        tokens = response.json()
        
        # Clear PKCE parameters from session
        session.pop('code_verifier', None)
        session.pop('oauth_state', None)
        
        # Store tokens securely
        session['access_token'] = tokens['access_token']
        session['refresh_token'] = tokens.get('refresh_token')
        
        return jsonify({
            'message': 'Authentication successful',
            'access_token': tokens['access_token'][:20] + '...',  # Truncated for display
            'token_type': tokens.get('token_type', 'Bearer'),
            'expires_in': tokens.get('expires_in')
        })
    else:
        error_data = response.json()
        return jsonify({
            'error': 'Token exchange failed',
            'details': error_data
        }), 400

@app.route('/api/protected')
def protected_resource():
    """Access protected resource using access token"""
    access_token = session.get('access_token')
    if not access_token:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Call protected API
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api-server.com/user', headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        return jsonify({'error': 'Token expired or invalid'}), 401
    else:
        return jsonify({'error': 'API call failed'}), response.status_code

# Standalone PKCE Client for Mobile/Desktop Apps
class PKCEOAuthClient:
    """Complete PKCE OAuth 2.0 client for public applications"""
    
    def __init__(self, client_id: str, authorization_url: str, 
                 token_url: str, redirect_uri: str):
        self.client_id = client_id
        self.authorization_url = authorization_url
        self.token_url = token_url
        self.redirect_uri = redirect_uri
        self.code_verifier = None
        self.access_token = None
        self.refresh_token = None
    
    def get_authorization_url(self, scope: str = '', state: str = None) -> str:
        """Generate authorization URL with PKCE parameters"""
        # Generate PKCE parameters
        self.code_verifier = PKCEHelper.generate_code_verifier()
        code_challenge = PKCEHelper.generate_code_challenge(self.code_verifier)
        
        if not state:
            state = secrets.token_urlsafe(32)
        
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': scope,
            'state': state,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256'
        }
        
        return f"{self.authorization_url}?{urlencode(params)}", state
    
    def exchange_code_for_token(self, authorization_code: str) -> dict:
        """Exchange authorization code for access token using PKCE"""
        if not self.code_verifier:
            raise Exception('No code verifier available. Call get_authorization_url first.')
        
        token_data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'code_verifier': self.code_verifier
        }
        
        response = requests.post(self.token_url, data=token_data)
        
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens['access_token']
            self.refresh_token = tokens.get('refresh_token')
            return tokens
        else:
            raise Exception(f'Token exchange failed: {response.text}')
    
    def call_api(self, api_url: str, method: str = 'GET', data: dict = None) -> dict:
        """Make authenticated API request"""
        if not self.access_token:
            raise Exception('Not authenticated')
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        
        if method == 'GET':
            response = requests.get(api_url, headers=headers)
        elif method == 'POST':
            response = requests.post(api_url, headers=headers, json=data)
        else:
            raise ValueError(f'Unsupported method: {method}')
        
        response.raise_for_status()
        return response.json()

# Usage Example for Mobile/Desktop App
if __name__ == '__main__':
    # Example 1: Flask Web App
    print("Starting Flask app with PKCE support...")
    print("Visit http://localhost:5000/login to test")
    # app.run(debug=True, port=5000)
    
    # Example 2: Standalone Client (Mobile/Desktop)
    print("\n" + "="*60)
    print("Standalone PKCE Client Example")
    print("="*60)
    
    client = PKCEOAuthClient(
        client_id='mobile-app-client-id',
        authorization_url='https://auth-server.com/oauth/authorize',
        token_url='https://auth-server.com/oauth/token',
        redirect_uri='myapp://callback'
    )
    
    # Step 1: Generate authorization URL
    auth_url, state = client.get_authorization_url(scope='read:user write:user')
    print(f"\n1. Open this URL in browser:\n{auth_url}\n")
    print(f"State (store this): {state}\n")
    
    # Step 2: After user authorizes, get the code from redirect
    # In a real app, this would come from the redirect handler
    authorization_code = input("2. Enter the authorization code from redirect: ")
    
    try:
        # Step 3: Exchange code for token
        tokens = client.exchange_code_for_token(authorization_code)
        print(f"\n✅ Authentication successful!")
        print(f"Access Token: {tokens['access_token'][:20]}...")
        print(f"Token Type: {tokens.get('token_type')}")
        print(f"Expires In: {tokens.get('expires_in')} seconds")
        
        # Step 4: Call protected API
        user_data = client.call_api('https://api-server.com/user')
        print(f"\nUser Data: {user_data}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
```

**Key Security Features in Implementation:**

1. **Cryptographically Random Verifier**: Uses `secrets` module for secure random generation
2. **SHA-256 Challenge**: One-way hash prevents reverse engineering
3. **No Client Secret**: Safe for public clients (mobile/SPA)
4. **State Parameter**: CSRF protection
5. **Session Security**: Secure storage of code_verifier during flow
6. **URL-Safe Encoding**: Proper base64 URL encoding without padding

**Testing the Implementation:**

```python
# Unit tests for PKCE functions
import unittest

class TestPKCE(unittest.TestCase):
    def test_code_verifier_length(self):
        verifier = PKCEHelper.generate_code_verifier()
        self.assertTrue(43 <= len(verifier) <= 128)
    
    def test_code_challenge_s256(self):
        verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
        challenge = PKCEHelper.generate_code_challenge(verifier, 'S256')
        expected = "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"
        self.assertEqual(challenge, expected)
    
    def test_code_challenge_plain(self):
        verifier = "test_verifier"
        challenge = PKCEHelper.generate_code_challenge(verifier, 'plain')
        self.assertEqual(challenge, verifier)
    
    def test_url_safe_encoding(self):
        verifier = PKCEHelper.generate_code_verifier()
        # Should not contain +, /, or =
        self.assertNotIn('+', verifier)
        self.assertNotIn('/', verifier)
        self.assertNotIn('=', verifier)

if __name__ == '__main__':
    unittest.main()
```