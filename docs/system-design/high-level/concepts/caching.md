# Caching

## Blogs and websites


## Medium

- [6 Cache Strategies to Save Your Database's Performance](https://levelup.gitconnected.com/6-cache-strategies-to-save-your-databases-performance-762ed2cccfa8)

## Youtube


## Theory

### What is Caching?

#### The Art of Remembering: The Most Powerful Optimization

Caching is arguably the **single most impactful** optimization in system design. It's based on a profound observation about data access patterns: **locality of reference**—the same data is accessed repeatedly, and recently accessed data is likely to be accessed again soon.

#### The Deep Theory: Why Caching Works

**The Fundamental Principle:**
Accessing data has a cost—in time, money, and resources. That cost varies wildly:
```
CPU L1 Cache:      0.5 nanoseconds   (baseline)
CPU L2 Cache:      7 nanoseconds     (14x slower)
RAM:               100 nanoseconds   (200x slower)
SSD:               150,000 nanoseconds (300,000x slower)
HDD:               10,000,000 nanoseconds (20 million x slower)
Network (same DC): 500,000 nanoseconds (1 million x slower)
Network (cross-continent): 150,000,000 nanoseconds (300 million x slower)
```

**The Revelation:**
If you can serve from a faster tier, you eliminate orders of magnitude of latency. Cache a database query result in Redis:
- **Before**: 50ms database query
- **After**: 0.5ms Redis lookup
- **Speedup**: 100x faster

**The Economic Argument:**
```
Database: $1,000/month for 1000 QPS
Redis: $100/month for 100,000 QPS

90% cache hit rate:
- 900 requests from Redis: cheap
- 100 requests from DB: normal load
- Result: Handle 10x traffic at same cost
```

#### The Cache Hierarchy: Layers Upon Layers

Caching exists at every level of the stack. Understanding where each tier belongs is critical.

##### Browser Cache (Client-Side)
```
User requests logo.png
  ↓
Browser: "I have this from yesterday"
  ↓
Return from disk: 0ms network time
```

**Control via HTTP Headers:**
```http
Cache-Control: max-age=31536000, immutable  # 1 year
Cache-Control: no-cache  # Always validate
Cache-Control: no-store  # Never cache
ETag: "v1.23"  # Version-based validation
```

**Benefits:**
- Zero server load
- Zero network latency
- Scales infinitely (each user caches locally)

**Challenges:**
- Can't invalidate (stuck until expiry)
- Different versions across users
- Wasted bandwidth if user never returns

**Best For:**
- Static assets (CSS, JS, images)
- Infrequently changing content
- User-specific data (after login)

##### CDN Cache (Edge)
```
User in Tokyo requests image
  ↓
CDN Tokyo node: "I have this"
  ↓
Return from edge: 5ms (vs 200ms from US origin)
```

**How It Works:**
1. User requests file
2. CDN edge node checks cache
3. If miss: Fetch from origin, cache, return
4. If hit: Return immediately
5. Subsequent users in region: Served from cache

**Benefits:**
- Geographic proximity (low latency)
- Offloads origin servers (90%+ hit rates)
- Handles traffic spikes (DDoS protection)
- Bandwidth savings (serve from edge)

**Best For:**
- Static assets globally distributed
- Media files (images, videos)
- API responses (with care)
- Software downloads

**Advanced: Dynamic Content Caching**
Modern CDNs cache API responses:
```http
GET /api/products?category=shoes
Cache-Control: max-age=60, s-maxage=300
# Browser caches 60s, CDN caches 300s
```

##### Application Cache (In-Memory)
```
User requests user profile
  ↓
App server: Check Redis
  ↓ (hit)
Return from Redis: 1ms (vs 50ms from DB)
```

**Types:**

**1. Local Cache (In-Process)**
```python
# Cache in application memory
cache = {}

def get_user(user_id):
    if user_id in cache:
        return cache[user_id]  # 100 nanoseconds
    
    user = db.query(user_id)  # 50 milliseconds
    cache[user_id] = user
    return user
```

**Pros:**
- Extremely fast (nanoseconds)
- No network calls
- Simple implementation

**Cons:**
- Limited by server RAM
- Not shared across servers
- Invalidation is complex
- Lost on server restart

**When to Use:**
- Reference data (countries, config)
- Session data (if single server)
- Small datasets

**2. Distributed Cache (Redis, Memcached)**
```python
import redis

cache = redis.Redis()

def get_user(user_id):
    cached = cache.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)  # 1 millisecond
    
    user = db.query(user_id)  # 50 milliseconds
    cache.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user
```

**Pros:**
- Shared across all servers
- Persistent (survives app restarts)
- Large capacity (100s of GB)
- Atomic operations

**Cons:**
- Network latency (1-2ms)
- Additional infrastructure
- Cost

**When to Use:**
- Multi-server deployments
- Large datasets
- Session management
- Rate limiting counters

##### Database Cache (Query Cache)
```sql
SELECT * FROM users WHERE id = 123;
  ↓
DB: "I executed this 1 second ago"
  ↓
Return cached result: 0.1ms (vs 10ms)
```

**Built-in Database Caching:**
- **Query cache**: Cache entire query results
- **Buffer pool**: Cache data pages in RAM
- **Prepared statements**: Cache execution plans

**Limitation:**
Invalidates on ANY write to table (too aggressive)

**Better Approach:**
Manual caching at application layer (more control)

#### The Cache Hierarchy Strategy

**The Cascade Pattern:**
```
Request comes in
  ↓
1. Check local cache (100 nanoseconds)
   Hit: Return
   Miss: ↓
2. Check Redis (1 millisecond)
   Hit: Store in local, return
   Miss: ↓
3. Check database (50 milliseconds)
   Hit: Store in Redis + local, return
   Miss: Return 404
```

**Hit Rate Multiplication:**
```
Local cache: 50% hit rate
Redis cache: 40% hit rate (of local misses)
Database: 10% of requests

Result:
- 50% served in 100ns
- 40% served in 1ms
- 10% served in 50ms
Average: 5.05ms (vs 50ms without caching)
```

### Cache Aside (Lazy Loading)

Application manages cache explicitly.

**Flow:**
1. Check cache
2. If miss, query database
3. Store in cache
4. Return data

**Pros:** Only cache what's needed
**Cons:** Cache misses add latency

### Read Through Strategy

Cache sits between application and database.

**Flow:**
1. Application queries cache
2. Cache manages database fetch on miss
3. Returns data

**Pros:** Simplified application logic
**Cons:** Initial miss penalty

### Write Through Strategy

Write to cache and database simultaneously.

**Pros:** Data consistency
**Cons:** Write latency

### Write Behind (Write Back)

Write to cache first, asynchronously to database.

**Pros:** Fast writes
**Cons:** Risk of data loss

### Write Around

Write directly to database, cache on read.

**Pros:** Reduces cache pollution
**Cons:** Read misses after writes

### Cache Invalidation

Removing stale data from cache.

**Strategies:**
- **TTL (Time To Live)**: Expire after time
- **Event-based**: Invalidate on updates
- **Manual**: Explicit invalidation

**Eviction Policies:**
- **LRU (Least Recently Used)**
- **LFU (Least Frequently Used)**
- **FIFO (First In First Out)**
- **Random**

**Popular Cache Systems:**
- Redis
- Memcached
- Hazelcast
- Ehcache
