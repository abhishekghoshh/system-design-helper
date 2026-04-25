# Security

## Theory

### Authentication vs Authorization Explained

Authentication and authorization are two distinct but related security concepts that are often confused.

**Authentication (AuthN)** answers: *"Who are you?"*
It is the process of verifying a user's identity. When you log in with a username and password, the system authenticates you. Think of it as showing your ID card at the entrance of a building — the guard checks that you are who you claim to be.

**Authorization (AuthZ)** answers: *"What are you allowed to do?"*
It determines what resources or actions an authenticated user can access. After showing your ID, the building lets you into floor 3 but not the server room — that's authorization.

**Key Differences:**

| Aspect | Authentication | Authorization |
|--------|---------------|---------------|
| **Question** | Who are you? | What can you access? |
| **Happens** | First (before authorization) | After authentication |
| **Mechanism** | Passwords, tokens, biometrics, MFA | Roles, policies, ACLs, scopes |
| **Fails with** | 401 Unauthorized | 403 Forbidden |
| **Visible to user** | Yes (login screen) | Often invisible |
| **Example** | Logging into Gmail | Accessing a shared doc vs owner settings |

**How They Work Together:**
```
User enters credentials
  → Authentication: "Is this user real?" (validates identity)
    → YES → Authorization: "What can this user do?" (checks permissions)
      → Grant/deny access to specific resources
    → NO → 401 Unauthorized
```

**Common Authentication Methods:**
- **Password-based**: Traditional username + password
- **Token-based**: JWT, session tokens
- **OAuth/OIDC**: Delegated auth via third-party (Google, GitHub)
- **SAML**: Enterprise SSO (XML-based federation)
- **Biometrics**: Fingerprint, face recognition
- **MFA**: Combines two or more factors (something you know + have + are)

**Common Authorization Models:**
- **RBAC (Role-Based)**: Permissions assigned to roles, users assigned to roles
- **ABAC (Attribute-Based)**: Policies based on user/resource/environment attributes
- **ACL (Access Control Lists)**: Explicit list of who can access what
- **ReBAC (Relationship-Based)**: Permissions based on relationships (Google Zanzibar)

**Real-World Example — E-commerce App:**
```
Customer logs in (Authentication)
  → Can view products, place orders (Authorization: customer role)
  → Cannot access admin dashboard (Authorization: denied)

Admin logs in (Authentication)
  → Can manage products, view analytics (Authorization: admin role)
  → Cannot delete other admins (Authorization: super-admin only)
```

---

## Authentication vs Authorization

**Authentication**: Verify identity (Who are you?)
- Username/password
- OAuth
- SAML
- Biometrics
- Multi-factor authentication (MFA)

**Authorization**: Verify permissions (What can you do?)
- Role-based (RBAC)
- Attribute-based (ABAC)
- Access control lists (ACL)

## OAuth
Open standard for delegated authorization.

**Flow (Authorization Code):**
1. User clicks "Login with Google"
2. Redirect to OAuth provider
3. User approves
4. Redirect back with code
5. Exchange code for access token
6. Use token to access resources

**OAuth 2.0 Grant Types:**
- Authorization Code (server-side apps)
- Implicit (deprecated)
- Client Credentials (service-to-service)
- Resource Owner Password (legacy)
- PKCE (mobile/SPA apps)

## JWT (JSON Web Token)
Compact, self-contained token for secure information transfer.

**Structure:**
```
Header.Payload.Signature
```

**Parts:**
- **Header**: Algorithm and type
- **Payload**: Claims (user data)
- **Signature**: Verify authenticity

**Pros:**
- Stateless
- Cross-domain
- Self-contained
- Scalable

**Cons:**
- Cannot revoke (until expiry)
- Size (larger than session ID)
- Vulnerable if stolen

**Best Practices:**
- Short expiration
- HTTPS only
- Secure storage
- Refresh tokens for long sessions
