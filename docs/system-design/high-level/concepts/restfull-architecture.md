# REST API (Representational State Transfer)

## Blogs and websites

- [REST Architectural Constraints](https://restfulapi.net/rest-architectural-constraints/)
- [REST API Architectural Constraints](https://www.geeksforgeeks.org/javascript/rest-api-architectural-constraints/)

## Medium


## Youtube


## Theory

Architectural style using HTTP for web services.

**Principles:**
- **Stateless**: Each request contains all needed information
- **Client-Server**: Separation of concerns
- **Cacheable**: Responses can be cached
- **Uniform Interface**: Consistent resource manipulation
- **Layered System**: Hierarchical architecture

**Best Practices:**
- Use nouns for resources (`/users`, `/products`)
- Use HTTP methods correctly
- Version your API (`/v1/users`)
- Return appropriate status codes
- Use pagination for large datasets
- Implement HATEOAS (links to related resources)

**Example:**
```
GET    /api/v1/users          # List users
GET    /api/v1/users/{id}     # Get user
POST   /api/v1/users          # Create user
PUT    /api/v1/users/{id}     # Update user
DELETE /api/v1/users/{id}     # Delete user
```

### REST API: Advantages

```
✓ Simple & Intuitive
  - Easy to understand (resources + HTTP methods)
  - Self-documenting (URLs describe resources)
  - Low learning curve
  - Standard conventions

✓ Stateless
  - Each request independent
  - Easy to scale horizontally
  - Simple load balancing
  - No server-side session management

✓ Cacheable
  - HTTP caching built-in
  - CDN support
  - Browser caching
  - Reduces server load

✓ Wide Adoption
  - Every language has HTTP libraries
  - Countless tools (Postman, curl, Swagger)
  - Large developer community
  - Abundant documentation

✓ Flexible
  - Works with any data format (JSON, XML, etc.)
  - Platform agnostic
  - Can evolve independently
  - Versioning strategies available

✓ Separation of Concerns
  - Client and server independent
  - Multiple clients (web, mobile, IoT)
  - Backend changes don't break clients
```

**Performance:**
```
Typical REST API:
  Request: 500-2000 bytes (headers + JSON)
  Response: 1000-5000 bytes
  Latency: 50-200ms
  Throughput: 1000-5000 req/sec (single server)
```

### REST API: Disadvantages

```
✗ Over-fetching
  - Get entire user object when you only need name
  - Wastes bandwidth
  - Slower for clients
  
  Example:
  GET /users/123 returns:
  {
    "id": 123,
    "name": "John",      ← Need this
    "email": "...",      ← Don't need
    "address": {...},    ← Don't need
    "preferences": {...} ← Don't need
  }

✗ Under-fetching (N+1 Problem)
  - Need multiple requests for related data
  - More round trips = higher latency
  
  Example:
  GET /posts/1         (get post)
  GET /users/123       (get author)
  GET /posts/1/comments (get comments)
  GET /users/456       (get commenter)
  Total: 4 requests = 4 × 50ms = 200ms

✗ Multiple Endpoints
  - Need to know many URLs
  - Documentation required
  - Version management complex
  
  GET /users
  GET /posts
  GET /comments
  GET /likes
  ... (100+ endpoints for large apps)

✗ Rigid Structure
  - Fixed responses per endpoint
  - Can't customize per client
  - Mobile needs less data than web
  - One size fits all

✗ Versioning Challenges
  - Breaking changes require new version
  - /v1/ vs /v2/ endpoint proliferation
  - Deprecation management
  - Multiple versions to maintain

✗ No Built-in Real-time
  - Need polling or webhooks
  - WebSockets separate concern
  - Not event-driven
```

### Alternatives to REST

**1. GraphQL**
```
What it solves:
  ✓ Over-fetching → Request exact fields needed
  ✓ Under-fetching → Get related data in one request
  ✓ Multiple endpoints → Single endpoint
  ✓ Versioning → No versions, evolve schema

Example:
  query {
    user(id: 123) {
      name          ← Only these fields
      posts {
        title       ← Nested in one request
      }
    }
  }

Advantages over REST:
  + Single endpoint (/graphql)
  + Request exactly what you need
  + Strongly typed schema
  + No over/under-fetching
  + Self-documenting (introspection)
  + Real-time via subscriptions

Disadvantages:
  - More complex to implement
  - Caching harder (not URL-based)
  - Learning curve
  - Query complexity management needed
  - Can expose too much data
  - Performance unpredictable (query depth)

When to use:
  → Complex data requirements
  → Multiple client types (web, mobile, IoT)
  → Rapid frontend development
  → Need flexibility

When REST is better:
  → Simple CRUD
  → Need HTTP caching
  → Team unfamiliar with GraphQL
  → Simpler is better
```

**2. gRPC**
```
What it solves:
  ✓ Performance → Binary protocol (10x faster)
  ✓ Type safety → Protobuf contracts
  ✓ Streaming → Built-in bidirectional streaming
  ✓ Code generation → Auto-generate clients

Example Protobuf:
  service UserService {
    rpc GetUser(UserRequest) returns (User);
    rpc StreamUsers(Empty) returns (stream User);
  }
  
  message User {
    int32 id = 1;
    string name = 2;
  }

Advantages over REST:
  + Much faster (binary vs JSON)
  + Smaller payloads (protobuf)
  + Type safety (compile-time checks)
  + Streaming built-in
  + HTTP/2 multiplexing
  + Code generation

Disadvantages:
  - Not browser-native (needs gRPC-web)
  - Less human-readable
  - Steeper learning curve
  - Less tooling than REST
  - Binary debugging harder

Performance:
  REST: 1,000 req/sec
  gRPC: 10,000+ req/sec

When to use:
  → Microservices communication
  → Performance critical
  → Internal APIs
  → Streaming needed

When REST is better:
  → Public APIs
  → Need browser support
  → Team unfamiliar with protobuf
  → Human-readable debugging important
```

**3. SOAP**
```
Legacy protocol (don't use for new projects)

Advantages:
  + Strict standards (WS-* specs)
  + Built-in security (WS-Security)
  + ACID transactions
  + Formal contracts (WSDL)

Disadvantages:
  - Extremely verbose (XML)
  - Complex
  - Slower than REST
  - Dated

When you see it:
  → Enterprise legacy systems
  → Banking/financial systems
  → SOAP is being phased out

Migration path: SOAP → REST or GraphQL
```

**4. tRPC (TypeScript RPC)**
```
For TypeScript full-stack:

Advantages over REST:
  + End-to-end type safety
  + No code generation
  + Autocomplete in IDE
  + Automatic API client

Example:
  // Server
  const userRouter = router({
    getById: procedure
      .input(z.number())
      .query(({ input }) => db.user.find(input))
  });
  
  // Client (fully typed!)
  const user = await trpc.user.getById.query(123);

When to use:
  → TypeScript project (frontend + backend)
  → Want type safety without GraphQL complexity
  
Limitation:
  - TypeScript only
  - Not for public APIs
```

### REST API Best Practices

**URL Design:**
```
Good:
  GET  /users              (list)
  GET  /users/123          (get one)
  POST /users              (create)
  PUT  /users/123          (update all)
  PATCH /users/123         (update partial)
  DELETE /users/123        (delete)
  
  GET  /users/123/posts    (nested resource)
  GET  /posts?userId=123   (filter via query param)

Bad:
  GET  /getUsers           ← Don't use verbs
  POST /users/delete/123   ← Use DELETE method
  GET  /user-list          ← Use plural nouns
  GET  /USERS              ← Use lowercase
```

**Status Codes:**
```
Use correctly:
  200 OK                   ← Success with body
  201 Created              ← Resource created
  204 No Content           ← Success, no body
  
  400 Bad Request          ← Client error (validation)
  401 Unauthorized         ← Not authenticated
  403 Forbidden            ← Authenticated but not allowed
  404 Not Found            ← Resource doesn't exist
  409 Conflict             ← Duplicate, constraint violation
  422 Unprocessable        ← Semantic errors
  429 Too Many Requests    ← Rate limited
  
  500 Internal Error       ← Server error
  502 Bad Gateway          ← Upstream error
  503 Service Unavailable  ← Temporarily down
```

**Response Format:**
```
Consistent structure:
  {
    "data": {...},
    "meta": {
      "timestamp": "2026-01-25T10:30:00Z",
      "requestId": "abc123"
    }
  }

Error response:
  {
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "Invalid email format",
      "field": "email",
      "details": [...]
    }
  }

Pagination:
  {
    "data": [...],
    "pagination": {
      "page": 1,
      "pageSize": 20,
      "total": 100,
      "totalPages": 5
    },
    "links": {
      "next": "/users?page=2",
      "prev": null
    }
  }
```

**Versioning:**
```
Option 1: URL versioning (most common)
  /api/v1/users
  /api/v2/users
  
  Pros: Clear, easy to route
  Cons: URL proliferation

Option 2: Header versioning
  GET /api/users
  Accept: application/vnd.api.v1+json
  
  Pros: Clean URLs
  Cons: Less visible

Option 3: Query parameter
  /api/users?version=1
  
  Pros: Flexible
  Cons: Pollutes query params

Recommendation: URL versioning (/v1/, /v2/)
```

**Security:**
```
✓ Use HTTPS always
✓ Authenticate with JWT/OAuth
✓ Validate all input
✓ Rate limit requests
✓ Use API keys for clients
✓ Implement CORS properly
✓ Don't expose stack traces
✓ Log security events
✓ Use OWASP guidelines
```

**Performance:**
```
✓ Implement caching headers
✓ Use gzip/brotli compression
✓ Paginate large collections
✓ Use field filtering (?fields=name,email)
✓ Implement ETags for conditional requests
✓ Use connection pooling
✓ Monitor slow endpoints
✓ Implement request timeout
```

### When to Use REST vs Alternatives

| Scenario | Use This | Why |
|----------|----------|-----|
| **Public API** | REST | Standard, widely understood |
| **Internal microservices** | gRPC | Performance, type safety |
| **Mobile app with complex UI** | GraphQL | Avoid over/under-fetching |
| **Simple CRUD** | REST | Simplest, good enough |
| **Real-time updates** | GraphQL Subscriptions or WebSocket | Event-driven |
| **TypeScript full-stack** | tRPC | Type safety |
| **Legacy enterprise** | SOAP | Required by old systems |
| **High performance** | gRPC | 10x faster than REST |
| **Multiple client types** | GraphQL | Flexible queries |
| **File uploads** | REST (multipart) | Standard, simple |

---

### REST Architectural Constraints

### Introduction

- [REST API Best Practices](https://www.youtube.com/watch?v=8XK2o5MfxkE)
- [The Right Way To Build REST APIs](https://www.youtube.com/watch?v=CVBpYfPKGlE)
- [Everything You NEED to Know About WEB APP Architecture](https://www.youtube.com/watch?v=sDlCSIDwpDs)


#### Comparisions

- [HTTP vs WebSockets: Performance (Latency - CPU - Memory - Network)](https://www.youtube.com/watch?v=UtyxjO8LJQs)


#### Idempotent API design

- [14. Design Idempotent POST API | System Design to Handle Duplicate Request by Idempotency Handler](https://www.youtube.com/watch?v=mI73eTlSqeU)
