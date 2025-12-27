# Design Rate Limiter

## Youtube

- [Rate Limiter System Design: Token Bucket, Leaky Bucket, Scaling](https://www.youtube.com/watch?v=YXkOdWBwqaA)

- [7: Design a Rate Limiter | Systems Design Interview Questions With Ex-Google SWE](https://www.youtube.com/watch?v=VzW41m4USGs)

- [How to Implement Rate Limiting | Rate Limiting Strategies - System Design](https://www.youtube.com/watch?v=eR66m7TaV5A)
- [Master Rate Limiting - System Design](https://www.youtube.com/watch?v=CVItTb_jdkE)

- [Five Rate Limiting Algorithms ~ Key Concepts in System Design](https://www.youtube.com/watch?v=mQCJJqUfn9Y)

- [What is Rate Limiting / API Throttling? | System Design Concepts](https://www.youtube.com/watch?v=9CIjoWPwAhU)

- [System Design Interview: Design a Distributed Rate Limiter w/ a Ex-Meta Staff Engineer](https://www.youtube.com/watch?v=MIJFyUPG4Z4)
  - [Design a Rate Limiter](https://www.hellointerview.com/learn/system-design/problem-breakdowns/distributed-rate-limiter)

- [Rate Limiting system design | TOKEN BUCKET, Leaky Bucket, Sliding Logs](https://www.youtube.com/watch?v=mhUQe4BKZXs)

- [12. Design Rate Limiter | API Rate Limiter System Design | Rate Limiting Algorithms | Rate Limiter](https://www.youtube.com/watch?v=X5daFTDfy2g)


## Website

- [Rate Limiter](https://www.techprep.app/system-design/high-level-design/rate-limiter/solution)
- [Design A Rate Limiter](https://bytebytego.com/courses/system-design-interview/design-a-rate-limiter)


## Blogs

- [Rate Limiting Fundamentals](https://blog.bytebytego.com/p/rate-limiting-fundamentals)
- [Rate Limiter For The Real World](https://blog.bytebytego.com/p/rate-limiter-for-the-real-world)




## Designing

### Overview

Rate limiting is a critical technique to control the rate of requests sent or received by a service. It protects against DDoS attacks, reduces costs, and prevents server overload. When a client exceeds the rate limit, the server returns **HTTP Status Code 429 (Too Many Requests)**.

Common use cases:
- API throttling (e.g., Twitter API: 300 requests/15 minutes)
- DDoS attack prevention
- Cost control for third-party APIs
- Resource management

---

### 1. Token Bucket Algorithm

#### Description
The Token Bucket algorithm is one of the most popular rate limiting algorithms. Imagine a bucket that holds tokens. Each request consumes one token. Tokens are added to the bucket at a fixed rate. If the bucket is full, new tokens are discarded. When a request arrives, it checks if there's a token available. If yes, the request is processed and a token is removed. If no, the request is rejected.

#### Diagram
```
Time: 0s      1s      2s      3s      4s
      ┌─┐     ┌─┐     ┌─┐     ┌─┐     ┌─┐
      │5│ →   │5│ →   │5│ →   │4│ →   │5│
      └─┘     └─┘     └─┘     └─┘     └─┘
Bucket (capacity=5, refill=1 token/sec)

Request at 3s → Token available → Accept (tokens: 5→4)
Request at 3.5s → Token available → Accept (tokens: 4→3)
```

#### Advantages
- Memory efficient - only needs to track token count and timestamp
- Allows burst traffic - clients can save up tokens for sudden spikes
- Easy to implement and understand
- Smooth traffic flow over time

#### Disadvantages
- Two parameters to tune (bucket size and refill rate)
- Difficult to tune parameters optimally for all scenarios
- May allow bursts that could overwhelm downstream services

#### Implementation

**Storage:** Typically uses **Redis** for distributed systems (stores token count and last refill time)

**Configuration Parameters:**
- `bucket_capacity`: Maximum number of tokens (e.g., 10)
- `refill_rate`: Tokens added per second (e.g., 1 token/sec)

**Ease of Implementation:** ⭐⭐⭐⭐ (4/5) - Easy to implement

#### Code Example

```python
import time
import redis

class TokenBucket:
    def __init__(self, capacity, refill_rate, redis_client, key):
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.redis = redis_client
        self.key = key
        
    def allow_request(self, tokens=1):
        """Check if request is allowed"""
        now = time.time()
        
        # Get current state from Redis
        pipe = self.redis.pipeline()
        pipe.get(f"{self.key}:tokens")
        pipe.get(f"{self.key}:last_refill")
        current_tokens, last_refill = pipe.execute()
        
        # Initialize if first time
        if current_tokens is None:
            current_tokens = self.capacity
            last_refill = now
        else:
            current_tokens = float(current_tokens)
            last_refill = float(last_refill)
        
        # Calculate tokens to add based on time elapsed
        elapsed = now - last_refill
        tokens_to_add = elapsed * self.refill_rate
        current_tokens = min(self.capacity, current_tokens + tokens_to_add)
        
        # Check if enough tokens
        if current_tokens >= tokens:
            current_tokens -= tokens
            # Update Redis
            pipe = self.redis.pipeline()
            pipe.set(f"{self.key}:tokens", current_tokens)
            pipe.set(f"{self.key}:last_refill", now)
            pipe.execute()
            return True
        
        return False

# Usage
redis_client = redis.Redis(host='localhost', port=6379)
limiter = TokenBucket(capacity=10, refill_rate=1, redis_client=redis_client, key="user:123")

if limiter.allow_request():
    print("Request allowed")
else:
    print("Rate limit exceeded - 429")
```

---

### 2. Leaky Bucket Algorithm

#### Description
The Leaky Bucket algorithm is similar to a bucket with a hole at the bottom. Requests enter the bucket as water. The bucket has a fixed capacity. Water leaks out of the bucket at a constant rate (processes requests). If the bucket is full when a request arrives, the request is rejected. This algorithm smooths out bursts and processes requests at a constant rate.

#### Diagram
```
Incoming Requests (variable rate)
         ↓↓↓
      ┌─────┐
      │ ░░░ │  ← Bucket (Queue)
      │ ░░░ │     Capacity: 5
      │ ░░░ │
      └──┬──┘
         ↓ (constant outflow rate)
    Processed Requests
```

#### Advantages
- Smooth and consistent output rate
- Memory efficient with fixed queue size
- Good for scenarios requiring stable outbound rate
- Simple to implement with a queue

#### Disadvantages
- A burst of traffic fills up the queue, and recent requests are rate limited
- Not suitable if requests need immediate processing
- Older requests in queue may become stale
- Difficult to tune bucket size appropriately

#### Implementation

**Storage:** Uses **Redis** (stores queue of requests with timestamps)

**Configuration Parameters:**
- `bucket_capacity`: Maximum queue size (e.g., 100)
- `outflow_rate`: Requests processed per second (e.g., 10/sec)

**Ease of Implementation:** ⭐⭐⭐ (3/5) - Moderate complexity

#### Code Example

```python
import time
import redis
from collections import deque

class LeakyBucket:
    def __init__(self, capacity, outflow_rate, redis_client, key):
        self.capacity = capacity
        self.outflow_rate = outflow_rate  # requests per second
        self.redis = redis_client
        self.key = key
        
    def allow_request(self):
        """Check if request can be added to bucket"""
        now = time.time()
        
        # Get queue from Redis (stored as list)
        queue = self.redis.lrange(f"{self.key}:queue", 0, -1)
        queue = [float(ts) for ts in queue]
        
        # Remove leaked (processed) requests
        leaked_time = now - (len(queue) / self.outflow_rate)
        queue = [ts for ts in queue if ts > leaked_time]
        
        # Check capacity
        if len(queue) < self.capacity:
            # Add request to queue
            self.redis.rpush(f"{self.key}:queue", now)
            self.redis.ltrim(f"{self.key}:queue", -self.capacity, -1)
            self.redis.expire(f"{self.key}:queue", 3600)  # 1 hour TTL
            return True
        
        return False

# Usage
redis_client = redis.Redis(host='localhost', port=6379)
limiter = LeakyBucket(capacity=100, outflow_rate=10, redis_client=redis_client, key="user:123")

if limiter.allow_request():
    print("Request queued")
else:
    print("Bucket full - 429")
```

---

### 3. Fixed Window Counter Algorithm

#### Description
The Fixed Window Counter algorithm divides time into fixed-size windows (e.g., 1 minute) and maintains a counter for each window. When a request arrives, the algorithm increments the counter for the current window. If the counter exceeds the threshold, the request is rejected. At the start of a new window, the counter resets to zero.

#### Diagram
```
Window 1       Window 2       Window 3
(0-60s)        (60-120s)      (120-180s)
┌────────┐    ┌────────┐    ┌────────┐
│Count: 8│    │Count: 5│    │Count: 3│
│Limit:10│    │Limit:10│    │Limit:10│
└────────┘    └────────┘    └────────┘
0s    60s    120s   180s

Issue: Spike at window boundary
    Window 1          Window 2
      ↓                 ↓
  ────┼─────────────────┼────
  50s-60s: 10 req  |  60s-70s: 10 req
        = 20 requests in 20s! (2x limit)
```

#### Advantages
- Very simple to implement
- Memory efficient - stores only one counter per window
- Fast lookup and update
- Works well with Redis TTL

#### Disadvantages
- **Boundary issue**: Spike at window edges can exceed rate limit (2x the limit)
- Not smooth - resets abruptly at window boundaries
- Doesn't account for distribution within window

#### Implementation

**Storage:** **Redis** with key expiration

**Configuration Parameters:**
- `window_size`: Duration in seconds (e.g., 60)
- `max_requests`: Maximum requests per window (e.g., 100)

**Ease of Implementation:** ⭐⭐⭐⭐⭐ (5/5) - Very easy to implement

#### Code Example

```python
import time
import redis
import math

class FixedWindowCounter:
    def __init__(self, window_size, max_requests, redis_client, key):
        self.window_size = window_size  # in seconds
        self.max_requests = max_requests
        self.redis = redis_client
        self.key = key
        
    def allow_request(self):
        """Check if request is allowed in current window"""
        now = time.time()
        window_key = f"{self.key}:{math.floor(now / self.window_size)}"
        
        # Increment counter
        current_count = self.redis.incr(window_key)
        
        # Set expiration on first request in window
        if current_count == 1:
            self.redis.expire(window_key, self.window_size * 2)
        
        # Check limit
        if current_count <= self.max_requests:
            return True
        
        return False

# Usage
redis_client = redis.Redis(host='localhost', port=6379)
limiter = FixedWindowCounter(window_size=60, max_requests=100, 
                             redis_client=redis_client, key="user:123")

if limiter.allow_request():
    print("Request allowed")
else:
    print("Window limit exceeded - 429")
```

---

### 4. Sliding Window Log Algorithm

#### Description
The Sliding Window Log algorithm keeps a log (sorted set) of timestamps for all requests. When a new request arrives, it removes all timestamps older than the current time minus the window size, then counts the remaining timestamps. If the count is below the limit, the request is allowed and its timestamp is added to the log.

#### Diagram
```
Window Size: 60s
Current Time: 100s
Look back to: 40s

Timeline:
35s  42s  55s  58s  70s  85s  95s  [100s - NEW REQUEST]
 X    ✓    ✓    ✓    ✓    ✓    ✓
(old) ← Sliding Window (60s) →

Count in window: 6
If limit = 10: Allow request
```

#### Advantages
- Very accurate - no boundary issues
- True sliding window (not fixed intervals)
- Precise rate limiting
- Fair distribution of requests

#### Disadvantages
- Memory intensive - stores timestamp for every request
- Expensive for high traffic (needs to scan and clean logs)
- Requires more storage (grows with traffic)
- Slower than counter-based approaches

#### Implementation

**Storage:** **Redis Sorted Set** (ZSET) with timestamps as scores

**Configuration Parameters:**
- `window_size`: Duration in seconds (e.g., 60)
- `max_requests`: Maximum requests per window (e.g., 100)

**Ease of Implementation:** ⭐⭐⭐ (3/5) - Moderate complexity

#### Code Example

```python
import time
import redis

class SlidingWindowLog:
    def __init__(self, window_size, max_requests, redis_client, key):
        self.window_size = window_size  # in seconds
        self.max_requests = max_requests
        self.redis = redis_client
        self.key = f"{key}:log"
        
    def allow_request(self):
        """Check if request is allowed using sliding window"""
        now = time.time()
        window_start = now - self.window_size
        
        # Use pipeline for atomic operations
        pipe = self.redis.pipeline()
        
        # Remove old entries outside the window
        pipe.zremrangebyscore(self.key, 0, window_start)
        
        # Count requests in current window
        pipe.zcard(self.key)
        
        # Execute pipeline
        _, current_count = pipe.execute()
        
        # Check limit
        if current_count < self.max_requests:
            # Add current request timestamp
            self.redis.zadd(self.key, {now: now})
            self.redis.expire(self.key, self.window_size * 2)
            return True
        
        return False

# Usage
redis_client = redis.Redis(host='localhost', port=6379)
limiter = SlidingWindowLog(window_size=60, max_requests=100, 
                          redis_client=redis_client, key="user:123")

if limiter.allow_request():
    print("Request allowed")
else:
    print("Rate limit exceeded - 429")
```

---

### 5. Sliding Window Counter Algorithm

#### Description
The Sliding Window Counter is a hybrid approach that combines Fixed Window Counter and Sliding Window Log. It uses two fixed windows (current and previous) and calculates an approximate count based on the overlap. This provides better accuracy than Fixed Window Counter with lower memory usage than Sliding Window Log.

#### Diagram
```
Previous Window    Current Window
    (0-60s)           (60-120s)
   ┌──────┐          ┌──────┐
   │ 80   │          │ 40   │
   └──────┘          └──────┘
        
Current Time: 90s (30s into current window)

Formula:
Estimated Count = (Previous × Overlap%) + Current
                = (80 × 50%) + 40
                = 40 + 40 = 80

If limit = 100: Allow request
```

#### Advantages
- Good balance between accuracy and memory
- Better than Fixed Window (smoother)
- More memory efficient than Sliding Window Log
- Handles boundary issues well

#### Disadvantages
- Only an approximation (not 100% accurate)
- Slightly more complex than Fixed Window
- Assumes uniform distribution in previous window
- Still has minor edge cases

#### Implementation

**Storage:** **Redis** with two counters

**Configuration Parameters:**
- `window_size`: Duration in seconds (e.g., 60)
- `max_requests`: Maximum requests per window (e.g., 100)

**Ease of Implementation:** ⭐⭐⭐⭐ (4/5) - Moderately easy

#### Code Example

```python
import time
import redis
import math

class SlidingWindowCounter:
    def __init__(self, window_size, max_requests, redis_client, key):
        self.window_size = window_size  # in seconds
        self.max_requests = max_requests
        self.redis = redis_client
        self.key = key
        
    def allow_request(self):
        """Check if request is allowed using sliding window counter"""
        now = time.time()
        current_window = math.floor(now / self.window_size)
        previous_window = current_window - 1
        
        # Calculate time elapsed in current window
        elapsed_time_in_current = now - (current_window * self.window_size)
        overlap_percentage = 1 - (elapsed_time_in_current / self.window_size)
        
        # Get counters
        prev_key = f"{self.key}:{previous_window}"
        curr_key = f"{self.key}:{current_window}"
        
        prev_count = int(self.redis.get(prev_key) or 0)
        curr_count = int(self.redis.get(curr_key) or 0)
        
        # Calculate estimated count
        estimated_count = (prev_count * overlap_percentage) + curr_count
        
        # Check limit
        if estimated_count < self.max_requests:
            # Increment current window counter
            pipe = self.redis.pipeline()
            pipe.incr(curr_key)
            pipe.expire(curr_key, self.window_size * 2)
            pipe.execute()
            return True
        
        return False

# Usage
redis_client = redis.Redis(host='localhost', port=6379)
limiter = SlidingWindowCounter(window_size=60, max_requests=100, 
                               redis_client=redis_client, key="user:123")

if limiter.allow_request():
    print("Request allowed")
else:
    print("Rate limit exceeded - 429")
```

---

## Comparison Table

| Algorithm | Accuracy | Memory | Performance | Allows Bursts | Complexity |
|-----------|----------|--------|-------------|---------------|------------|
| Token Bucket | Good | Low | High | Yes | Easy |
| Leaky Bucket | Excellent | Medium | Medium | No | Moderate |
| Fixed Window | Poor | Very Low | Very High | Yes | Very Easy |
| Sliding Window Log | Excellent | High | Low | No | Moderate |
| Sliding Window Counter | Good | Low | High | Partial | Easy |

---

## Redis vs Configuration

### When to use Redis:
- **Distributed systems** (multiple servers need shared state)
- **High traffic** scenarios
- **Dynamic rate limits** that change frequently
- **Per-user/per-IP** rate limiting

### When to use In-Memory/Config:
- **Single server** applications
- **Low traffic** scenarios
- **Static rate limits** that rarely change
- **Global rate limiting** (same for all users)

### Hybrid Approach:
```python
# Config file (config.yaml)
rate_limits:
  api_v1: 100 requests per minute
  api_v2: 1000 requests per minute
  
# Redis stores the actual counters/state
# Config stores the limits/rules
```

---

## Which Algorithm to Choose?

- **Token Bucket**: Best for most use cases, especially APIs (used by Amazon, Stripe)
- **Leaky Bucket**: When you need smooth, consistent output rate
- **Fixed Window**: Simple caching, non-critical rate limiting
- **Sliding Window Log**: When accuracy is critical and memory is not a concern
- **Sliding Window Counter**: Good balance for high-traffic systems (used by Cloudflare)

---

## Return HTTP Status Code

When rate limit is exceeded, return:
```
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1640000000
Retry-After: 60

{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Please try again later."
}
```