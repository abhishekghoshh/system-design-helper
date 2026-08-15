# Performance & Resilience Patterns

## Blogs and websites


## Medium

- [Introduction to API Rate Limiting: Understanding the Basics and Its Importance](https://medium.com/the-developers-diary/introduction-to-api-rate-limiting-understanding-the-basics-and-its-importance-fde0b5af995b)

## Youtube


## Theory

### What is Rate Limiting?

Rate limiting is a technique used to control the number of requests a client can make to a server within a given time window. It acts as a gatekeeper that prevents any single user or service from overwhelming your system.

**Why Rate Limiting Matters:**
- **Prevents abuse**: Stops malicious actors from DDoS attacks or brute-force attempts
- **Ensures fairness**: No single user can monopolize resources
- **Protects infrastructure**: Prevents cascading failures under load spikes
- **Controls cost**: Limits compute/bandwidth usage on pay-per-use infrastructure

**How It Works (Conceptually):**
```
Client sends request
  → Rate limiter checks: "Has this client exceeded N requests in T seconds?"
    → NO  → Forward request to server → Return response
    → YES → Return 429 Too Many Requests
```

**Common Algorithms Explained:**

1. **Fixed Window**: Divide time into fixed intervals (e.g., 1-minute windows). Count requests per window. Simple but has burst issues at window boundaries.

2. **Sliding Window Log**: Track timestamps of each request. Count requests within a rolling window. Precise but memory-intensive.

3. **Sliding Window Counter**: Hybrid of fixed window and sliding log. Weights the previous window count by overlap percentage. Good balance of accuracy and efficiency.

4. **Token Bucket**: A bucket holds tokens (max capacity = burst size). Tokens are added at a fixed rate. Each request consumes one token. If empty, request is rejected. Allows controlled bursts.

5. **Leaky Bucket**: Requests enter a queue (bucket). Processed at a constant rate. If bucket is full, excess requests are dropped. Smooths out traffic.

**Where to Implement:**
- **API Gateway**: Most common — centralized, handles rate limiting before requests reach services
- **Load Balancer**: Can do basic IP-based limiting
- **Application Layer**: Fine-grained per-user or per-endpoint limits
- **Redis/Memcached**: Distributed counters for rate limiting across multiple servers

**Rate Limiting vs Throttling:**
- Rate limiting: Hard cutoff — reject excess requests (429 response)
- Throttling: Soft control — slow down or queue excess requests

---

### Rate Limiting

Control number of requests in time window.

**Algorithms:**
- **Fixed Window**: Count requests per fixed time window
- **Sliding Window**: Rolling time window
- **Token Bucket**: Tokens added at fixed rate
- **Leaky Bucket**: Requests processed at fixed rate

**Benefits:**
- Prevent abuse
- Ensure fair usage
- Protect backend
- Cost control

**Implementation:**
- API Gateway
- Redis
- Nginx
- Application code

### Throttling

Deliberately slow down processing to protect system.

**Types:**
- **Request throttling**: Limit incoming requests
- **Resource throttling**: Limit resource consumption
- **User throttling**: Limit per user

**Difference from Rate Limiting:**
- Rate limiting: Hard limits, reject excess
- Throttling: Slow down, queue excess

### Backpressure

Downstream component signals upstream to slow down.

**Mechanisms:**
- Bounded queues
- Reactive Streams
- TCP flow control
- HTTP/2 flow control

**Benefits:**
- Prevent system overload
- Graceful degradation
- Resource protection

### Idempotency

Multiple identical requests have same effect as single request.

**HTTP Idempotent Methods:**
- GET, PUT, DELETE, HEAD, OPTIONS
- NOT POST (creates new resource each time)

**Implementation:**
- Idempotency keys
- Database constraints
- Check before insert
- State machines

**Use Cases:**
- Payment processing
- Order submission
- Retry logic

### Circuit Breaker

Prevent cascading failures by failing fast.

**States:**
- **Closed**: Normal operation
- **Open**: Requests fail immediately
- **Half-Open**: Test if service recovered

**Benefits:**
- Fail fast
- Prevent resource exhaustion
- Allow service recovery
- Graceful degradation

**Tools:**
- Hystrix (Netflix, deprecated)
- Resilience4j
- Polly (.NET)

### Retry Mechanisms

Automatically retry failed operations.

**Strategies:**
- **Fixed delay**: Wait same time between retries
- **Exponential backoff**: Increase delay exponentially
- **Jitter**: Add randomness to avoid thundering herd

**Best Practices:**
- Set max retries
- Only retry transient failures
- Use exponential backoff
- Implement idempotency

### Bulkhead Pattern

Isolate resources to prevent cascading failures.

**Example:**
- Separate connection pools per service
- Separate thread pools
- Resource quotas

**Benefits:**
- Fault isolation
- Resource protection
- Prevent total system failure

### Health Checks

Monitor service health and availability.

**Types:**
- **Liveness**: Is service running?
- **Readiness**: Can service handle requests?
- **Startup**: Has service finished initialization?

**Implementation:**
- HTTP endpoints (`/health`, `/ready`)
- Periodic polling
- Metrics collection

**Use Cases:**
- Load balancer routing
- Auto-scaling decisions
- Container orchestration
- Service discovery
