# HTTP / HTTPS (HyperText Transfer Protocol)

## Theory

### HTTP and REST Fundamentals

**HTTP (HyperText Transfer Protocol)** is the foundation of data communication on the web. It's a **request-response**, **stateless**, **application-layer** protocol that defines how clients (browsers, apps) and servers exchange information.

**How HTTP Works:**
```
1. Client opens a TCP connection to the server
2. Client sends an HTTP request (method, URL, headers, body)
3. Server processes the request
4. Server sends an HTTP response (status code, headers, body)
5. Connection may be reused (keep-alive) or closed
```

**Key Characteristics:**
- **Stateless**: Each request is independent. The server doesn't remember previous requests. State is managed via cookies, tokens, or sessions.
- **Text-based** (HTTP/1.1): Human-readable headers and messages. HTTP/2+ uses binary framing.
- **Extensible**: Custom headers and content types allow flexible communication.

**REST (Representational State Transfer)** is an architectural style built on top of HTTP. It treats everything as a **resource** identified by a URL, manipulated through standard HTTP methods.

**REST Principles:**
- **Resources**: Everything is a resource (`/users`, `/products/123`)
- **HTTP Methods as Verbs**: GET (read), POST (create), PUT (update), DELETE (remove)
- **Stateless**: Server holds no client context between requests
- **Uniform Interface**: Consistent URL patterns and response formats
- **Cacheable**: Responses declare cacheability via headers

**HTTP Request Anatomy:**
```http
GET /api/users/123 HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbG...
Accept: application/json
```

**HTTP Response Anatomy:**
```http
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: max-age=3600

{"id": 123, "name": "John", "email": "john@example.com"}
```

**HTTPS** is HTTP over TLS/SSL. It encrypts all communication between client and server, preventing eavesdropping, tampering, and impersonation. HTTPS is mandatory for any production system.

---

Application layer protocol for web communication.

**HTTP Methods:**
- **GET**: Retrieve data
- **POST**: Submit data
- **PUT**: Update/replace resource
- **PATCH**: Partial update
- **DELETE**: Remove resource
- **HEAD**: Get headers only
- **OPTIONS**: Get supported methods

**HTTP Status Codes:**

**1xx - Informational** (Request received, processing)
```
100 Continue          → "Keep sending request body"
101 Switching Protocols → "Upgrading to WebSocket"
```

**2xx - Success** (Request succeeded)
```
200 OK                → "Success, here's your data"
201 Created           → "Resource created successfully"
202 Accepted          → "Request accepted, processing async"
204 No Content        → "Success, but no data to return"
206 Partial Content   → "Here's part of the file (resume download)"
```

**3xx - Redirection** (Further action needed)
```
301 Moved Permanently → "Resource moved, update bookmarks"
302 Found            → "Temporary redirect, try this URL"
304 Not Modified     → "Use your cached version"
307 Temporary Redirect → "Temporary, keep using original URL"
308 Permanent Redirect → "Permanent, change all references"
```

**4xx - Client Errors** (Client messed up)
```
400 Bad Request      → "Your request is malformed"
401 Unauthorized     → "You need to authenticate"
403 Forbidden        → "Authenticated but not allowed"
404 Not Found        → "Resource doesn't exist"
405 Method Not Allowed → "Can't POST to this endpoint"
409 Conflict         → "Resource state conflict"
429 Too Many Requests → "Rate limit exceeded"
```

**5xx - Server Errors** (Server messed up)
```
500 Internal Server Error → "Something broke on our end"
502 Bad Gateway          → "Upstream server error"
503 Service Unavailable  → "Temporarily down/overloaded"
504 Gateway Timeout      → "Upstream server didn't respond"
```

**Real API Example:**
```http
# Success flow
POST /api/users HTTP/1.1
Host: api.example.com
Content-Type: application/json

{"name": "John", "email": "john@example.com"}

↓ Response:
HTTP/1.1 201 Created
Location: /api/users/123
Content-Type: application/json

{"id": 123, "name": "John", "email": "john@example.com"}

# Error flow
POST /api/users HTTP/1.1
{"name": "John"}  ← Missing email

↓ Response:
HTTP/1.1 400 Bad Request

{"error": "email is required"}
```

## HTTPS: Security Through Encryption

**HTTP vs HTTPS:**
```
HTTP (Insecure):
Client ←─────plaintext─────→ Server
       "password123"  ← Anyone can read!
       
HTTPS (Secure):
Client ←───encrypted───→ Server
       "8x$mK9#..."  ← Gibberish to eavesdroppers
```

**TLS Handshake (How HTTPS Works):**
```
1. Client Hello
   ┌────────┐                    ┌────────┐
   │ Client │ ──────────────────→ │ Server │
   └────────┘  "Let's use TLS 1.3"└────────┘
                "Supported ciphers: ..."

2. Server Hello + Certificate
   ┌────────┐                    ┌────────┐
   │ Client │ ←────────────────── │ Server │
   └────────┘  "Use TLS 1.3"      └────────┘
                "Here's my certificate"
                "Signed by: Let's Encrypt"

3. Client Verifies Certificate
   ┌────────┐
   │ Client │ Checks:
   └────────┘   ✓ Certificate signed by trusted CA?
                ✓ Domain matches?
                ✓ Not expired?
                ✓ Not revoked?

4. Key Exchange
   ┌────────┐                    ┌────────┐
   │ Client │ ←───────────────→  │ Server │
   └────────┘  Generate shared    └────────┘
                encryption key
                (using asymmetric crypto)

5. Encrypted Communication
   ┌────────┐                    ┌────────┐
   │ Client │ ←═════════════════→ │ Server │
   └────────┘  All data encrypted └────────┘
                with shared key
```

**What HTTPS Protects Against:**

```
✓ Eavesdropping
  Attacker: Can't read passwords, credit cards, messages

✓ Tampering
  Attacker: Can't modify requests/responses

✓ Impersonation
  Attacker: Can't pretend to be your bank

✗ Doesn't protect against
  - Server being hacked
  - Client having malware
  - DNS hijacking (before connection)
  - Trust in CA system being broken
```

**SSL Certificate Example:**
```
Certificate:
  Subject: CN=example.com
  Issuer: CN=Let's Encrypt
  Valid: 2026-01-01 to 2026-04-01 (90 days)
  Public Key: RSA 2048 bits
  Signature Algorithm: SHA256-RSA
  Subject Alternative Names:
    - example.com
    - www.example.com
    - *.example.com (wildcard)
```

**Check Certificate:**
```bash
# Using OpenSSL
openssl s_client -connect example.com:443 -servername example.com

# Using curl
curl -vI https://example.com

# Browser: Click padlock icon in address bar
```

## HTTP/1.1 vs HTTP/2 vs HTTP/3

**HTTP/1.1 (1997-2015):**
```
Limitations:
┌──────────────────────────────────────┐
│ Request 1 → Response 1               │
│ Request 2 → Response 2 (waits!)      │
│ Request 3 → Response 3 (waits!)      │
└──────────────────────────────────────┘

Problems:
- Head-of-line blocking
- 1 request at a time per connection
- Workaround: Multiple connections (6-8)
- Large headers (repeated cookies, etc.)
```

**HTTP/2 (2015):**
```
Improvements:
┌──────────────────────────────────────┐
│      Single TCP Connection           │
├─────────┬─────────┬─────────┬────────┤
│Stream 1 │Stream 2 │Stream 3 │Stream 4│
│ Request │ Request │ Request │ Request│
│Response │Response │Response │Response│
└─────────┴─────────┴─────────┴────────┘

Features:
✓ Multiplexing: Multiple requests in parallel
✓ Header Compression: HPACK algorithm
✓ Server Push: Send resources before requested
✓ Binary Protocol: More efficient parsing

Example:
Browser requests index.html
  ↓
Server pushes:
  - style.css
  - script.js
  - logo.png
Before browser even asks!
```

**HTTP/3 (2020+):**
```
Built on QUIC (over UDP, not TCP):

HTTP/2 Problem:
┌──────────────────┐
│  TCP Layer       │ ← One packet lost = all streams blocked
└──────────────────┘

HTTP/3 Solution:
┌──────────────────┐
│  QUIC (UDP)      │ ← Each stream independent
└──────────────────┘

Benefits:
✓ Faster connection setup (0-RTT)
✓ Better loss recovery (no head-of-line blocking)
✓ Connection migration (survive IP changes)
✓ Built-in encryption (TLS 1.3 mandatory)

Mobile Example:
Phone switches from WiFi to 4G
  ↓
HTTP/2: Connection drops, restart handshake (slow)
HTTP/3: Connection continues seamlessly (fast)
```

**Performance Comparison:**
```
Loading website with 100 resources:

HTTP/1.1:
├─ Connection setup: 100ms
├─ Request 1-6: parallel (200ms)
├─ Request 7-12: wait... (200ms)
├─ Request 13-18: wait... (200ms)
└─ Total: ~1.5 seconds

HTTP/2:
├─ Connection setup: 100ms
├─ All 100 requests: parallel (200ms)
└─ Total: ~300ms (5x faster!)

HTTP/3:
├─ Connection setup: 0ms (0-RTT)
├─ All 100 requests: parallel (200ms)
└─ Total: ~200ms (7.5x faster!)
```

**Adoption Status:**
```
HTTP/1.1: 100% support (fallback)
HTTP/2:   ~95% support (widely deployed)
HTTP/3:   ~70% support (growing rapidly)

Major sites using HTTP/3:
- Google
- Facebook
- Cloudflare
- Netflix
```

## HTTP: Advantages & Disadvantages

**Advantages:**
```
✓ Universal Support
  - Works on every platform
  - Every language has HTTP libraries
  - Browser native support

✓ Simple & Human-Readable
  - Text-based protocol
  - Easy to debug (curl, browser DevTools)
  - Self-documenting (headers explain themselves)

✓ Stateless
  - Each request independent
  - Easy to scale horizontally
  - Simple load balancing

✓ Firewall-Friendly
  - Ports 80/443 usually open
  - Works through corporate proxies
  - NAT traversal easier

✓ Rich Ecosystem
  - Countless tools and libraries
  - Well-understood debugging
  - Mature best practices

✓ Flexible
  - Works with any content type
  - Extensible via headers
  - Supports various auth methods
```

**Disadvantages:**
```
✗ Overhead
  - Text format larger than binary
  - Headers repeated on every request
  - Verbose for simple operations

✗ Stateless Complexity
  - Session management needed
  - Cookies/tokens for state
  - Authentication on every request

✗ Latency
  - HTTP/1.1: Head-of-line blocking
  - Multiple round trips for handshake
  - Not ideal for real-time

✗ Security Requires HTTPS
  - Plain HTTP is insecure
  - Certificate management overhead
  - TLS adds latency

✗ Not Bidirectional (HTTP/1.1)
  - Client must initiate
  - Server can't push (until HTTP/2)
  - Polling needed for updates

✗ Resource Intensive
  - Connection overhead
  - Keep-alive helps but not perfect
  - Server resources per connection
```

## Alternatives to HTTP

**1. WebSockets**
```
Use When:
  ✓ Bidirectional communication needed
  ✓ Real-time updates (chat, gaming)
  ✓ Continuous data stream
  ✓ Low latency critical

Advantages over HTTP:
  + Full-duplex (both directions)
  + Single persistent connection
  + Lower overhead (no headers per message)
  + Server can push anytime

Disadvantages:
  - More complex to implement
  - Harder to load balance
  - Firewall issues possible
  - Connection state management

Example:
  Chat application: HTTP → WebSocket
  Before: Poll every 1s for new messages
  After: Server pushes messages instantly
```

**2. gRPC**
```
Use When:
  ✓ Microservices communication
  ✓ Performance critical
  ✓ Strongly typed contracts needed
  ✓ Streaming required

Advantages over HTTP/REST:
  + Binary protocol (smaller, faster)
  + HTTP/2 multiplexing built-in
  + Code generation (type safety)
  + Bidirectional streaming
  + Better performance (10x faster)

Disadvantages:
  - Not browser-native
  - Less human-readable
  - Steeper learning curve
  - Limited tooling vs REST
  - Requires HTTP/2

Comparison:
  REST API: 1000 requests/sec
  gRPC: 10,000+ requests/sec (same hardware)
```

**3. GraphQL**
```
Use When:
  ✓ Complex data requirements
  ✓ Multiple client types (web, mobile)
  ✓ Avoid over-fetching
  ✓ Flexible queries needed

Advantages over REST:
  + Single endpoint
  + Request exactly what you need
  + No over-fetching or under-fetching
  + Strong typing
  + Real-time via subscriptions

Disadvantages:
  - Caching harder
  - Complexity for simple cases
  - Can expose too much
  - Query cost unpredictable
  - Learning curve

Example:
  REST: 3 endpoints, 2 KB response (over-fetch)
  GraphQL: 1 endpoint, 0.5 KB (exact data)
```

**4. Server-Sent Events (SSE)**
```
Use When:
  ✓ One-way updates (server → client)
  ✓ Simpler than WebSocket
  ✓ Auto-reconnect needed
  ✓ Text-based updates

Advantages over HTTP polling:
  + Real-time push
  + Automatic reconnection
  + Built-in event IDs
  + Simpler than WebSocket

Advantages over WebSocket:
  + Simpler (just HTTP)
  + Better browser support
  + HTTP/2 compatible

Disadvantages vs WebSocket:
  - One-way only (server → client)
  - Text only (no binary)
  - Less efficient than WebSocket

Example:
  Stock ticker: SSE perfect (server pushes prices)
  Chat: WebSocket better (bidirectional)
```

**5. Message Queues (Kafka, RabbitMQ)**
```
Use When:
  ✓ Asynchronous processing
  ✓ Decoupling services
  ✓ High throughput needed
  ✓ Reliability critical

Advantages over HTTP:
  + Guaranteed delivery
  + Buffering (handle spikes)
  + Replay capability
  + Decoupling
  + Higher throughput

Disadvantages:
  - More complex infrastructure
  - Not for synchronous requests
  - Eventual consistency
  - Additional latency

Example:
  Order processing:
  HTTP: Synchronous, fails if service down
  Kafka: Async, queued until service recovers
```

**6. UDP-based Protocols (QUIC, WebRTC)**
```
Use When:
  ✓ Real-time media (video, voice)
  ✓ Gaming
  ✓ IoT with packet loss tolerance
  ✓ Ultra-low latency needed

Advantages over HTTP/TCP:
  + Lower latency (no retransmission delays)
  + Better for real-time
  + Connection migration (HTTP/3)
  + No head-of-line blocking

Disadvantages:
  - Less reliable (no guaranteed delivery)
  - Firewall issues
  - More complex implementation
  - Not suitable for most APIs

Example:
  Video call: UDP (some frame loss acceptable)
  File download: TCP (every byte matters)
```

## Decision Matrix: Which Protocol?

| Need | Best Choice | Why |
|------|-------------|-----|
| **REST API** | HTTP/2 | Standard, widely supported |
| **Real-time chat** | WebSocket | Bidirectional, low latency |
| **Live notifications** | SSE | Simple, auto-reconnect |
| **Microservices** | gRPC | Performance, type safety |
| **Complex queries** | GraphQL | Flexible, avoid over-fetch |
| **Async processing** | Message Queue | Reliable, decoupled |
| **Video streaming** | WebRTC/QUIC | Low latency, packet loss OK |
| **File upload** | HTTP multipart | Simple, standard |
| **Bulk data transfer** | HTTP/2 or gRPC | Streaming, efficient |

## When NOT to Use HTTP

```
✗ Real-time gaming
  → Use UDP/WebSocket (latency critical)

✗ Video/voice calls
  → Use WebRTC (packet loss tolerable)

✗ High-frequency trading
  → Use custom binary protocol (microseconds matter)

✗ IoT sensors (millions)
  → Use MQTT (lightweight, pub/sub)

✗ Inter-service calls (microservices)
  → Consider gRPC (faster, type-safe)

✗ Large file transfers (GB+)
  → Consider BitTorrent/custom (P2P, resumable)
```

## HTTP Best Practices

**Do's:**
```
✓ Use HTTPS everywhere (even dev)
✓ Implement proper HTTP status codes
✓ Use HTTP/2 minimum (HTTP/3 when possible)
✓ Implement caching headers
✓ Compress responses (gzip, brotli)
✓ Use connection pooling
✓ Implement rate limiting
✓ Version your APIs (/v1/, /v2/)
✓ Use idempotent methods correctly
✓ Return proper error messages
```

**Don'ts:**
```
✗ Don't use GET for state changes
✗ Don't send sensitive data in URLs
✗ Don't ignore status codes (don't return 200 for errors)
✗ Don't create new connections per request
✗ Don't send uncompressed large payloads
✗ Don't use HTTP for real-time gaming
✗ Don't expose internal error details
✗ Don't use custom headers when standard ones exist
```
