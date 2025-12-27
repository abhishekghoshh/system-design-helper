# Distributed Cache and Caching Strategies


## Youtube

- [19. System Design: Distributed Cache and Caching Strategies | Cache-Aside, Write-Through, Write-Back](https://www.youtube.com/watch?v=RtOyBwBICRs)


## Theory

### What is Caching?

**Caching** is a technique to store frequently accessed data in a fast-access storage layer (cache) to reduce latency and improve application performance. Instead of repeatedly fetching data from slow data sources (database, external API, disk), the application retrieves it from the cache.

**Key Benefits:**
- **Reduced Latency**: Cache reads are 10-100x faster than database queries
- **Lower Database Load**: Fewer database queries reduce CPU, memory, and I/O usage
- **Improved Scalability**: Handle more requests with same infrastructure
- **Cost Savings**: Reduce expensive database or API calls
- **Better User Experience**: Faster page loads and responses

**Cache Hierarchy:**
```
Fastest ↑
--------
CPU Cache (L1, L2, L3) - Nanoseconds
RAM (Application Cache) - Microseconds
Distributed Cache (Redis, Memcached) - Milliseconds (1-5ms)
Database - Tens of milliseconds (10-100ms)
Disk - Milliseconds to seconds
Network/API - Hundreds of milliseconds to seconds
--------
Slowest ↓
```

### Distributed Cache

A **distributed cache** is a caching system that spans multiple servers/nodes, allowing cached data to be shared across multiple application instances in a cluster.

#### Why Distributed Cache?

**Problem with Local Cache:**
```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│  App Server │       │  App Server │       │  App Server │
│      1      │       │      2      │       │      3      │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ Local Cache │       │ Local Cache │       │ Local Cache │
│ user:1=John │       │ user:1=John │       │ user:1=Jane │ ← Inconsistent!
└─────────────┘       └─────────────┘       └─────────────┘
       ↓                     ↓                     ↓
   ┌──────────────────────────────────────────────────┐
   │              Database                             │
   │              user:1 = Jane (updated)              │
   └──────────────────────────────────────────────────┘

Problem: After update, Server 1 and 2 have stale data!
```

**Solution with Distributed Cache:**
```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│  App Server │       │  App Server │       │  App Server │
│      1      │       │      2      │       │      3      │
└──────┬──────┘       └──────┬──────┘       └──────┬──────┘
       │                     │                     │
       └─────────────────────┼─────────────────────┘
                             ↓
              ┌──────────────────────────┐
              │  Distributed Cache       │
              │  (Redis / Memcached)     │
              │  user:1 = Jane           │ ← Single source of truth
              └────────────┬─────────────┘
                           ↓
                  ┌─────────────────┐
                  │    Database     │
                  │  user:1 = Jane  │
                  └─────────────────┘

All servers read from same cache - Always consistent!
```

#### Characteristics of Distributed Cache

1. **Shared**: All application instances access the same cache
2. **Scalable**: Can add more cache nodes to increase capacity
3. **Highly Available**: Replication ensures no single point of failure
4. **Fast**: In-memory storage for microsecond latency
5. **Consistent**: All servers see same cached data
6. **Partitioned**: Data distributed across multiple nodes (sharding)

#### Popular Distributed Cache Systems

**1. Redis**
- In-memory data structure store
- Supports strings, hashes, lists, sets, sorted sets
- Persistence options (RDB, AOF)
- Pub/Sub messaging
- Lua scripting
- Clustering and replication built-in
- **Use case**: Session store, real-time analytics, leaderboards

**2. Memcached**
- Simple key-value store
- Multi-threaded (better CPU utilization)
- No persistence
- LRU eviction
- Very fast for simple caching
- **Use case**: Pure caching layer, session storage

**3. Amazon ElastiCache**
- Managed Redis or Memcached
- Auto-scaling, backup, monitoring
- **Use case**: AWS cloud deployments

**4. Hazelcast**
- In-memory data grid (IMDG)
- Distributed Java data structures
- Compute grid capabilities
- **Use case**: Java applications, distributed computing

**5. Apache Ignite**
- Distributed database and cache
- SQL support
- ACID transactions
- **Use case**: Hybrid transactional/analytical processing

### Cache Architecture Patterns

#### 1. Single-Node Cache

```
┌──────────────┐
│ Application  │
├──────────────┤
│ Local Cache  │  ← In-process (e.g., dict, LRU cache)
└──────────────┘
```

**Pros**: Fastest access, no network latency
**Cons**: Not shared, limited by single server memory

#### 2. Centralized Cache

```
┌─────────┐    ┌─────────┐    ┌─────────┐
│  App 1  │    │  App 2  │    │  App 3  │
└────┬────┘    └────┬────┘    └────┬────┘
     │              │              │
     └──────────────┼──────────────┘
                    ↓
            ┌───────────────┐
            │  Cache Server │  ← Single Redis/Memcached
            └───────────────┘
```

**Pros**: Shared cache, consistency
**Cons**: Single point of failure, limited capacity

#### 3. Distributed Cache Cluster (Recommended)

```
┌─────────┐    ┌─────────┐    ┌─────────┐
│  App 1  │    │  App 2  │    │  App 3  │
└────┬────┘    └────┬────┘    └────┬────┘
     │              │              │
     └──────────────┼──────────────┘
                    ↓
     ┌──────────────────────────────────┐
     │      Cache Cluster               │
     │  ┌────────┐  ┌────────┐  ┌────┐ │
     │  │ Node 1 │  │ Node 2 │  │ N3 │ │
     │  │Shard A │  │Shard B │  │... │ │
     │  └────────┘  └────────┘  └────┘ │
     └──────────────────────────────────┘
```

**Pros**: High availability, scalable, fault-tolerant
**Cons**: Complex setup, network overhead

### Caching Strategies (Cache Patterns)

Caching strategies determine **when** and **how** data is written to and read from the cache.

---

### 1. Cache-Aside (Lazy Loading)

**Description**: 

Cache-Aside, also known as **Lazy Loading**, is the most common and straightforward caching pattern where the application code is responsible for managing both the cache and the database. The cache sits "aside" the main data flow, and the application explicitly checks the cache before querying the database.

**Key Concept**: The cache is only populated **on-demand** when data is actually requested (lazy), not during write operations. This means data is loaded into the cache only when it's needed, avoiding unnecessary caching of data that may never be accessed.

**How the pattern works conceptually**:
- The **application owns the caching logic** - it must explicitly check cache, handle misses, and update cache
- On **reads**: Application tries cache first → if miss, query database → store in cache → return data
- On **writes**: Application updates database → invalidates (or updates) relevant cache entries
- The cache is **passive** - it doesn't know about the database; only the application knows both

**When cache is empty (cold start)**: Every request is a cache miss initially, gradually warming up as requests come in. This "lazy" approach means you only cache what's actually used, which is memory-efficient but has initial performance cost.

**Flow Diagram:**
```
Read Request:
┌─────────────┐
│ Application │
└──────┬──────┘
       │ 1. Read(key)
       ↓
┌─────────────┐
│    Cache    │
└──────┬──────┘
       │
       ├─ 2a. CACHE HIT? → Return value to app
       │
       └─ 2b. CACHE MISS?
           │
           ↓
       ┌─────────────┐
       │  Database   │
       └──────┬──────┘
              │
              └─ 3. App reads from DB
                 4. App writes to cache
                 5. Return to user

Write Request:
┌─────────────┐
│ Application │
└──────┬──────┘
       │ 1. Write(key, value)
       ↓
┌─────────────┐
│  Database   │  ← Write to DB first
└──────┬──────┘
       │
       └─ 2. Invalidate cache (or update)
          3. Next read will fetch fresh data
```

**Python Implementation:**
```python
import redis
import psycopg2

class CacheAside:
    def __init__(self):
        self.cache = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.db = psycopg2.connect("dbname=mydb user=postgres")
    
    def get_user(self, user_id):
        """Cache-Aside Read"""
        cache_key = f"user:{user_id}"
        
        # 1. Try to get from cache
        cached_value = self.cache.get(cache_key)
        
        if cached_value:
            print(f"CACHE HIT for user {user_id}")
            return cached_value
        
        # 2. Cache miss - fetch from database
        print(f"CACHE MISS for user {user_id}")
        cursor = self.db.cursor()
        cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        
        if result:
            user_name = result[0]
            
            # 3. Populate cache (with TTL of 1 hour)
            self.cache.setex(cache_key, 3600, user_name)
            
            return user_name
        
        return None
    
    def update_user(self, user_id, new_name):
        """Cache-Aside Write"""
        cache_key = f"user:{user_id}"
        
        # 1. Write to database
        cursor = self.db.cursor()
        cursor.execute("UPDATE users SET name = %s WHERE id = %s", (new_name, user_id))
        self.db.commit()
        
        # 2. Invalidate cache (cache will be repopulated on next read)
        self.cache.delete(cache_key)
        
        print(f"Updated user {user_id} and invalidated cache")

# Usage
cache_aside = CacheAside()
print(cache_aside.get_user(1))  # CACHE MISS - loads from DB
print(cache_aside.get_user(1))  # CACHE HIT - from cache
cache_aside.update_user(1, "Jane")  # Invalidates cache
print(cache_aside.get_user(1))  # CACHE MISS - loads fresh data
```

**Advantages:**
- ✅ Cache only what's needed (lazy loading)
- ✅ Cache misses don't break the application (DB is source of truth)
- ✅ Application has full control over caching logic
- ✅ Works well for read-heavy workloads

**Disadvantages:**
- ❌ First request always misses cache (cold start)
- ❌ Cache miss penalty (3 round trips: check cache → read DB → write cache)
- ❌ Potential for stale data if cache isn't invalidated
- ❌ Application code manages cache explicitly (more complex)

**When to Use:**
- Read-heavy applications
- Unpredictable data access patterns
- When you want application control over cache

**Common Pitfalls & Solutions:**

1. **Cache Stampede (Thundering Herd)**
   - **Problem**: When cache expires, multiple requests hit DB simultaneously
   - **Solution**: Use cache locking or probabilistic early expiration

```python
def get_user_with_lock(self, user_id):
    """Prevent cache stampede with distributed lock"""
    cache_key = f"user:{user_id}"
    lock_key = f"lock:{cache_key}"
    
    cached_value = self.cache.get(cache_key)
    if cached_value:
        return cached_value
    
    # Try to acquire lock
    lock_acquired = self.cache.set(lock_key, "1", nx=True, ex=10)
    
    if lock_acquired:
        # This thread loads from DB
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            
            if result:
                user_name = result[0]
                self.cache.setex(cache_key, 3600, user_name)
                return user_name
        finally:
            self.cache.delete(lock_key)
    else:
        # Other threads wait and retry
        time.sleep(0.1)
        return self.get_user_with_lock(user_id)
```

2. **Stale Data After Update**
   - **Problem**: Cache not invalidated after DB update
   - **Solution**: Always invalidate or update cache after DB write

```python
def update_user_safe(self, user_id, new_name):
    """Ensure cache consistency with DB transaction"""
    cache_key = f"user:{user_id}"
    
    try:
        # Start DB transaction
        cursor = self.db.cursor()
        cursor.execute("UPDATE users SET name = %s WHERE id = %s", (new_name, user_id))
        self.db.commit()
        
        # Only invalidate cache if DB write succeeds
        self.cache.delete(cache_key)
        print(f"Updated user {user_id} - cache invalidated")
    except Exception as e:
        self.db.rollback()
        print(f"Update failed: {e}. Cache unchanged.")
        raise
```

**Real-World Example: E-commerce Product Details**

```python
import json
from typing import Optional, Dict

class ProductCacheAside:
    def __init__(self):
        self.cache = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.db = psycopg2.connect("dbname=ecommerce user=postgres")
    
    def get_product_details(self, product_id: int) -> Optional[Dict]:
        """Get product with reviews, inventory, and pricing"""
        cache_key = f"product:details:{product_id}"
        
        # Try cache first
        cached_data = self.cache.get(cache_key)
        if cached_data:
            print(f"✓ Cache HIT: Product {product_id}")
            return json.loads(cached_data)
        
        # Cache miss - fetch from multiple tables
        print(f"✗ Cache MISS: Product {product_id} - querying database")
        
        cursor = self.db.cursor()
        
        # Complex query joining multiple tables
        cursor.execute("""
            SELECT p.id, p.name, p.price, p.description,
                   i.stock_count, i.warehouse_location,
                   AVG(r.rating) as avg_rating, COUNT(r.id) as review_count
            FROM products p
            LEFT JOIN inventory i ON p.id = i.product_id
            LEFT JOIN reviews r ON p.id = r.product_id
            WHERE p.id = %s
            GROUP BY p.id, i.stock_count, i.warehouse_location
        """, (product_id,))
        
        result = cursor.fetchone()
        if not result:
            return None
        
        product_data = {
            'id': result[0],
            'name': result[1],
            'price': float(result[2]),
            'description': result[3],
            'stock': result[4],
            'warehouse': result[5],
            'avg_rating': float(result[6]) if result[6] else 0,
            'review_count': result[7]
        }
        
        # Cache for 1 hour (product details don't change often)
        self.cache.setex(cache_key, 3600, json.dumps(product_data))
        
        return product_data
    
    def update_product_price(self, product_id: int, new_price: float):
        """Update price and invalidate all related cache entries"""
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "UPDATE products SET price = %s WHERE id = %s",
                (new_price, product_id)
            )
            self.db.commit()
            
            # Invalidate multiple related cache keys
            keys_to_invalidate = [
                f"product:details:{product_id}",
                f"product:price:{product_id}",
                "products:featured",  # May include this product
                "products:on_sale"    # Price change may affect this list
            ]
            
            for key in keys_to_invalidate:
                self.cache.delete(key)
            
            print(f"Updated product {product_id} price to ${new_price}")
            print(f"Invalidated {len(keys_to_invalidate)} cache entries")
            
        except Exception as e:
            self.db.rollback()
            raise

# Usage Example
product_cache = ProductCacheAside()

# First request - queries DB (expensive join)
product = product_cache.get_product_details(123)
print(f"Product: {product['name']}, Stock: {product['stock']}")

# Subsequent requests - served from cache (< 1ms)
product = product_cache.get_product_details(123)

# Update price - invalidates cache
product_cache.update_product_price(123, 99.99)

# Next read - cache miss, fresh data loaded
product = product_cache.get_product_details(123)
```

**Performance Metrics:**
```
Without Cache:
- Database query time: 50-100ms (complex joins)
- Requests per second: ~20-50

With Cache-Aside:
- Cache hit time: <1ms
- Cache miss time: 50-100ms (same as DB)
- Cache hit ratio: 85-95% (typical)
- Requests per second: 1000+ (mostly cache hits)
- Database load reduction: 90%+
```

---

### 2. Write-Through Cache

**Description**: 

Write-Through is a caching pattern where every write operation goes through the cache to the database **synchronously**. The cache acts as the primary interface for writes, ensuring the cache and database are always perfectly synchronized.

**Key Concept**: **Write operations are never completed until both cache and database are updated**. This guarantees that the cache is always a reliable, up-to-date representation of the database state - no stale data exists in the cache.

**How the pattern works conceptually**:
- On **writes**: Application → Cache (update) → Cache synchronously writes to Database → Confirm to application
- On **reads**: Application → Cache (always returns fresh data, rarely needs to touch database)
- The cache is **active/smart** - it knows about the database and handles persistence
- **Strong consistency**: At any given moment, cache exactly mirrors the database

**Trade-off**: Write latency increases because every write waits for both cache and database operations to complete. However, this cost is often acceptable because reads (which are typically more frequent) become extremely fast since data is guaranteed to be in cache.

**Difference from Cache-Aside**: In Cache-Aside, writes go to DB first and cache may be invalidated. In Write-Through, cache is the write interface and it propagates to DB. This means Write-Through guarantees cache population on write, while Cache-Aside may leave cache empty after a write.

**Flow Diagram:**
```
Write Request:
┌─────────────┐
│ Application │
└──────┬──────┘
       │ 1. Write(key, value)
       ↓
┌─────────────┐
│    Cache    │  ← Write to cache first
└──────┬──────┘
       │ 2. Cache writes to DB synchronously
       ↓
┌─────────────┐
│  Database   │
└─────────────┘
       │
       └─ 3. Confirm write to app

Read Request:
┌─────────────┐
│ Application │
└──────┬──────┘
       │ 1. Read(key)
       ↓
┌─────────────┐
│    Cache    │  ← Always returns fresh data (no DB query)
└─────────────┘
```

**Python Implementation:**
```python
class WriteThrough:
    def __init__(self):
        self.cache = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.db = psycopg2.connect("dbname=mydb user=postgres")
    
    def get_user(self, user_id):
        """Read from cache (always up-to-date)"""
        cache_key = f"user:{user_id}"
        
        # Try cache first
        cached_value = self.cache.get(cache_key)
        if cached_value:
            print(f"CACHE HIT for user {user_id}")
            return cached_value
        
        # If not in cache, load from DB and cache it
        print(f"CACHE MISS for user {user_id}")
        cursor = self.db.cursor()
        cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        
        if result:
            user_name = result[0]
            self.cache.set(cache_key, user_name)
            return user_name
        
        return None
    
    def create_user(self, user_id, name):
        """Write-Through: Write to cache AND database"""
        cache_key = f"user:{user_id}"
        
        # 1. Write to cache
        self.cache.set(cache_key, name)
        
        # 2. Write to database synchronously
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO users (id, name) VALUES (%s, %s)", (user_id, name))
        self.db.commit()
        
        print(f"Created user {user_id} in both cache and database")
    
    def update_user(self, user_id, new_name):
        """Write-Through: Update cache AND database"""
        cache_key = f"user:{user_id}"
        
        # 1. Update cache
        self.cache.set(cache_key, new_name)
        
        # 2. Update database synchronously
        cursor = self.db.cursor()
        cursor.execute("UPDATE users SET name = %s WHERE id = %s", (new_name, user_id))
        self.db.commit()
        
        print(f"Updated user {user_id} in both cache and database")

# Usage
write_through = WriteThrough()
write_through.create_user(1, "John")
print(write_through.get_user(1))  # CACHE HIT - always in cache
write_through.update_user(1, "Jane")
print(write_through.get_user(1))  # CACHE HIT - updated data
```

**Advantages:**
- ✅ Cache and database always consistent
- ✅ No stale data
- ✅ Read performance is excellent (always hits cache)
- ✅ Simplifies read logic (cache is source of truth for reads)

**Disadvantages:**
- ❌ Write latency increases (writes to cache AND DB)
- ❌ Every write goes to both cache and DB (even if data never read)
- ❌ Wasted cache space for rarely accessed data
- ❌ Higher write load on cache

**When to Use:**
- Applications requiring strong consistency
- Read-heavy workloads with predictable write patterns
- When data must always be cached after write

**Implementation Considerations:**

1. **Write Latency Impact**
   - Every write waits for both cache AND database
   - Use connection pooling to minimize latency
   - Consider async replication for non-critical data

2. **Transaction Handling**
   - Ensure atomicity between cache and DB writes
   - Rollback cache if DB write fails

```python
def create_user_with_transaction(self, user_id, name, email):
    """Write-Through with proper transaction handling"""
    cache_key = f"user:{user_id}"
    user_data = json.dumps({'name': name, 'email': email})
    
    try:
        # Write to cache first (faster)
        self.cache.set(cache_key, user_data)
        
        # Write to database
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO users (id, name, email) VALUES (%s, %s, %s)",
            (user_id, name, email)
        )
        self.db.commit()
        
        print(f"✓ User {user_id} created in cache and DB")
        
    except Exception as e:
        # Rollback: Remove from cache if DB write failed
        self.cache.delete(cache_key)
        self.db.rollback()
        print(f"✗ Write failed: {e}. Cache rolled back.")
        raise
```

**Real-World Example: Session Management**

```python
import json
import uuid
from datetime import datetime, timedelta

class SessionStore:
    """Write-Through cache for user sessions - always consistent"""
    
    def __init__(self):
        self.cache = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.db = psycopg2.connect("dbname=sessions user=postgres")
    
    def create_session(self, user_id: int, ip_address: str) -> str:
        """Create new session - Write-Through ensures immediate consistency"""
        session_id = str(uuid.uuid4())
        session_data = {
            'user_id': user_id,
            'ip_address': ip_address,
            'created_at': datetime.now().isoformat(),
            'last_accessed': datetime.now().isoformat()
        }
        
        cache_key = f"session:{session_id}"
        
        try:
            # 1. Write to cache (fast access for all requests)
            self.cache.setex(
                cache_key,
                86400,  # 24 hour expiry
                json.dumps(session_data)
            )
            
            # 2. Write to database (persistence, analytics)
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO sessions (id, user_id, ip_address, created_at, last_accessed)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                session_id,
                user_id,
                ip_address,
                session_data['created_at'],
                session_data['last_accessed']
            ))
            self.db.commit()
            
            print(f"✓ Session {session_id} created for user {user_id}")
            return session_id
            
        except Exception as e:
            # Cleanup on failure
            self.cache.delete(cache_key)
            self.db.rollback()
            raise
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session - always from cache (guaranteed to be there)"""
        cache_key = f"session:{session_id}"
        
        cached_data = self.cache.get(cache_key)
        if cached_data:
            print(f"✓ Session {session_id[:8]}... found in cache")
            return json.loads(cached_data)
        
        # Should rarely happen (only if cache was cleared)
        print(f"⚠ Session {session_id[:8]}... not in cache, checking DB")
        
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT user_id, ip_address, created_at, last_accessed FROM sessions WHERE id = %s",
            (session_id,)
        )
        result = cursor.fetchone()
        
        if result:
            # Re-populate cache
            session_data = {
                'user_id': result[0],
                'ip_address': result[1],
                'created_at': result[2].isoformat(),
                'last_accessed': result[3].isoformat()
            }
            self.cache.setex(cache_key, 86400, json.dumps(session_data))
            return session_data
        
        return None
    
    def update_session_activity(self, session_id: str):
        """Update last accessed time - Write-Through keeps everything in sync"""
        cache_key = f"session:{session_id}"
        
        # Get current session data
        cached_data = self.cache.get(cache_key)
        if not cached_data:
            return False
        
        session_data = json.loads(cached_data)
        session_data['last_accessed'] = datetime.now().isoformat()
        
        try:
            # Update cache
            self.cache.setex(cache_key, 86400, json.dumps(session_data))
            
            # Update database
            cursor = self.db.cursor()
            cursor.execute(
                "UPDATE sessions SET last_accessed = %s WHERE id = %s",
                (session_data['last_accessed'], session_id)
            )
            self.db.commit()
            
            return True
            
        except Exception as e:
            # If DB update fails, revert cache to old value
            self.cache.setex(cache_key, 86400, cached_data)
            self.db.rollback()
            raise

# Usage Example
session_store = SessionStore()

# Create session - written to both cache and DB
session_id = session_store.create_session(user_id=42, ip_address="192.168.1.1")

# Get session - always from cache (fast)
session = session_store.get_session(session_id)
print(f"User: {session['user_id']}, IP: {session['ip_address']}")

# Update activity - both cache and DB updated
session_store.update_session_activity(session_id)
```

**Why Write-Through for Sessions?**
- ✅ **Consistency**: Cache and DB always in sync
- ✅ **Read Performance**: Every session read is a cache hit (< 1ms)
- ✅ **Reliability**: Sessions persisted to DB (survive cache restart)
- ✅ **Analytics**: DB has all session data for reporting
- ⚠️ **Write Cost**: Acceptable because session creates/updates are infrequent compared to reads

**Performance Comparison:**
```
Session Reads (per request):
- Without cache: 10-20ms (DB query)
- With Write-Through cache: <1ms (cache hit)
- Improvement: 10-20x faster

Session Writes:
- Write-Through: 15-25ms (cache + DB)
- Cache-Aside: 10-20ms (DB only)
- Trade-off: Slightly slower writes for much faster reads
```

---

### 3. Write-Behind (Write-Back) Cache

**Description**: 

Write-Behind, also called **Write-Back**, is a high-performance caching pattern where write operations complete as soon as data is written to cache, and the database write happens **asynchronously** in the background. This decouples the application from database write latency.

**Key Concept**: The cache becomes the **primary data store** from the application's perspective, and the database is updated "eventually" through background processes. This provides blazing-fast write performance but introduces eventual consistency and potential data loss risks.

**How the pattern works conceptually**:
- On **writes**: Application → Cache (immediate update) → Return success immediately → Background process writes to DB later
- The database write happens in a **separate thread/process** - often batched with other writes
- **Write coalescing**: Multiple writes to same key can be collapsed into single DB operation
- **Eventual consistency**: Cache has latest data, but database lags behind temporarily (milliseconds to seconds)

**Asynchronous mechanisms**:
- **Time-based batching**: Flush to DB every N seconds (e.g., every 5 seconds)
- **Size-based batching**: Flush when N writes accumulate (e.g., every 100 writes)
- **Hybrid**: Flush based on time OR size, whichever comes first

**Critical consideration**: If cache fails before background write completes, data in the queue is lost. This makes it unsuitable for critical data (financial transactions, user accounts) but perfect for high-volume, less-critical data (analytics, logs, game scores).

**Performance benefit**: Can handle 10-100x more writes than Write-Through because application isn't blocked by slow database operations. Database load is also reduced through batching and coalescing.

**Flow Diagram:**
```
Write Request:
┌─────────────┐
│ Application │
└──────┬──────┘
       │ 1. Write(key, value)
       ↓
┌─────────────┐
│    Cache    │  ← Write to cache (fast response)
└──────┬──────┘
       │ 2. Return immediately to app
       │
       └─ 3. Asynchronously write to DB later
          (batched or delayed)
          ↓
┌─────────────┐
│  Database   │
└─────────────┘

Read Request:
┌─────────────┐
│ Application │
└──────┬──────┘
       │ 1. Read(key)
       ↓
┌─────────────┐
│    Cache    │  ← Always returns data (may not be in DB yet)
└─────────────┘
```

**Python Implementation:**
```python
import threading
import time
from queue import Queue

class WriteBehind:
    def __init__(self):
        self.cache = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.db = psycopg2.connect("dbname=mydb user=postgres")
        self.write_queue = Queue()
        
        # Background thread for async DB writes
        self.writer_thread = threading.Thread(target=self._background_writer, daemon=True)
        self.writer_thread.start()
    
    def _background_writer(self):
        """Background thread that writes to DB asynchronously"""
        while True:
            # Batch writes every 5 seconds or when queue has 100 items
            time.sleep(5)
            
            writes = []
            while not self.write_queue.empty() and len(writes) < 100:
                writes.append(self.write_queue.get())
            
            if writes:
                # Batch write to database
                cursor = self.db.cursor()
                for user_id, name in writes:
                    cursor.execute(
                        "INSERT INTO users (id, name) VALUES (%s, %s) "
                        "ON CONFLICT (id) DO UPDATE SET name = %s",
                        (user_id, name, name)
                    )
                self.db.commit()
                print(f"Batch wrote {len(writes)} records to database")
    
    def get_user(self, user_id):
        """Read from cache"""
        cache_key = f"user:{user_id}"
        cached_value = self.cache.get(cache_key)
        
        if cached_value:
            print(f"CACHE HIT for user {user_id}")
            return cached_value
        
        # Fallback to DB if not in cache
        print(f"CACHE MISS for user {user_id}")
        cursor = self.db.cursor()
        cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        
        if result:
            return result[0]
        return None
    
    def update_user(self, user_id, new_name):
        """Write-Behind: Update cache immediately, DB later"""
        cache_key = f"user:{user_id}"
        
        # 1. Write to cache immediately (fast!)
        self.cache.set(cache_key, new_name)
        
        # 2. Queue DB write for later (async)
        self.write_queue.put((user_id, new_name))
        
        print(f"Updated user {user_id} in cache (DB write queued)")
        # Return immediately without waiting for DB write!

# Usage
write_behind = WriteBehind()
write_behind.update_user(1, "John")  # Returns immediately
print(write_behind.get_user(1))  # CACHE HIT - instant
time.sleep(6)  # Wait for background writer
# Check DB - data should be there now
```

**Advantages:**
- ✅ Extremely fast writes (cache-only latency)
- ✅ Reduced database load (batched writes)
- ✅ Better performance for write-heavy workloads
- ✅ Can consolidate multiple writes (write coalescing)

**Disadvantages:**
- ❌ Risk of data loss if cache fails before DB write
- ❌ Complex implementation (background writers, queues)
- ❌ Eventual consistency (DB lags behind cache)
- ❌ Difficult to debug (async writes)

**When to Use:**
- Write-heavy applications (logging, analytics, gaming leaderboards)
- When write latency is critical
- Systems that can tolerate some data loss
- High-throughput data ingestion

**Critical Considerations:**

1. **Data Loss Risk**
   - Cache can fail before DB write completes
   - Use persistence (Redis AOF/RDB) to minimize loss
   - Not suitable for financial transactions or critical data

2. **Write Coalescing**
   - Multiple writes to same key can be collapsed into one DB write
   - Dramatically reduces database load

```python
def background_writer_with_coalescing(self):
    """Batch writer that coalesces duplicate writes"""
    while True:
        time.sleep(5)
        
        # Use dict to coalesce - last write wins
        writes_dict = {}
        
        while not self.write_queue.empty():
            user_id, name = self.write_queue.get()
            writes_dict[user_id] = name  # Overwrites previous value
        
        if writes_dict:
            cursor = self.db.cursor()
            
            # Batch insert/update
            for user_id, name in writes_dict.items():
                cursor.execute(
                    "INSERT INTO users (id, name) VALUES (%s, %s) "
                    "ON CONFLICT (id) DO UPDATE SET name = %s",
                    (user_id, name, name)
                )
            
            self.db.commit()
            print(f"Batch wrote {len(writes_dict)} records (coalesced from queue)")
```

**Real-World Example: Gaming Leaderboard**

```python
import time
import threading
from queue import Queue
from typing import List, Tuple
import json

class LeaderboardCache:
    """Write-Behind for high-frequency score updates in gaming"""
    
    def __init__(self):
        self.cache = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.db = psycopg2.connect("dbname=gaming user=postgres")
        self.write_queue = Queue()
        self.running = True
        
        # Start background writer
        self.writer_thread = threading.Thread(
            target=self._batch_writer,
            daemon=True
        )
        self.writer_thread.start()
    
    def update_score(self, player_id: int, score: int, game_id: str):
        """Update player score - Write-Behind for ultra-fast response"""
        leaderboard_key = f"leaderboard:{game_id}"
        player_key = f"player:{player_id}:score"
        
        # 1. Update cache immediately (FAST!)
        # Use Redis sorted set for automatic ranking
        self.cache.zadd(leaderboard_key, {player_id: score})
        self.cache.set(player_key, score)
        
        # 2. Queue for async DB write
        self.write_queue.put(('score_update', player_id, score, game_id))
        
        print(f"⚡ Player {player_id} score updated to {score} (instant response)")
        # Returns immediately - player sees instant feedback!
    
    def record_game_event(self, player_id: int, event_type: str, data: dict):
        """Record game events - high volume, write-behind"""
        event_key = f"events:{player_id}:latest"
        
        # Cache latest event for quick access
        self.cache.setex(event_key, 300, json.dumps(data))
        
        # Queue for DB persistence
        self.write_queue.put(('event', player_id, event_type, json.dumps(data)))
    
    def get_leaderboard(self, game_id: str, top_n: int = 10) -> List[Tuple[int, int]]:
        """Get top players - always from cache (real-time)"""
        leaderboard_key = f"leaderboard:{game_id}"
        
        # Get top N players with scores (descending order)
        top_players = self.cache.zrevrange(
            leaderboard_key,
            0,
            top_n - 1,
            withscores=True
        )
        
        leaderboard = [(int(player_id), int(score)) for player_id, score in top_players]
        
        print(f"✓ Leaderboard for {game_id}: {len(leaderboard)} players")
        return leaderboard
    
    def get_player_rank(self, player_id: int, game_id: str) -> Tuple[int, int]:
        """Get player's rank and score - instant from cache"""
        leaderboard_key = f"leaderboard:{game_id}"
        
        # Get rank (0-based, so add 1)
        rank = self.cache.zrevrank(leaderboard_key, player_id)
        score = self.cache.zscore(leaderboard_key, player_id)
        
        if rank is not None and score is not None:
            return (rank + 1, int(score))
        
        return (None, None)
    
    def _batch_writer(self):
        """Background thread - writes to DB in batches every 10 seconds"""
        while self.running:
            time.sleep(10)  # Batch every 10 seconds
            
            # Collect writes with coalescing
            score_updates = {}  # player_id -> (score, game_id)
            events = []
            
            batch_size = 0
            while not self.write_queue.empty() and batch_size < 1000:
                item = self.write_queue.get()
                
                if item[0] == 'score_update':
                    _, player_id, score, game_id = item
                    # Coalesce: keep only latest score per player
                    score_updates[player_id] = (score, game_id)
                    
                elif item[0] == 'event':
                    _, player_id, event_type, data = item
                    events.append((player_id, event_type, data))
                
                batch_size += 1
            
            if score_updates or events:
                try:
                    cursor = self.db.cursor()
                    
                    # Batch update scores
                    if score_updates:
                        for player_id, (score, game_id) in score_updates.items():
                            cursor.execute("""
                                INSERT INTO player_scores (player_id, game_id, score, updated_at)
                                VALUES (%s, %s, %s, NOW())
                                ON CONFLICT (player_id, game_id)
                                DO UPDATE SET score = %s, updated_at = NOW()
                            """, (player_id, game_id, score, score))
                    
                    # Batch insert events
                    if events:
                        for player_id, event_type, data in events:
                            cursor.execute("""
                                INSERT INTO game_events (player_id, event_type, data, created_at)
                                VALUES (%s, %s, %s, NOW())
                            """, (player_id, event_type, data))
                    
                    self.db.commit()
                    
                    print(f"💾 Batch wrote to DB: {len(score_updates)} scores, {len(events)} events")
                    
                except Exception as e:
                    self.db.rollback()
                    print(f"❌ Batch write failed: {e}")
                    # Could re-queue failed writes or log to error queue

# Usage Example
leaderboard = LeaderboardCache()

# High-frequency score updates (1000s per second)
for i in range(1000):
    player_id = i % 100  # 100 players
    score = 1000 + i
    leaderboard.update_score(player_id, score, "fortnite_match_123")
    # Each update returns in < 1ms!

# Real-time leaderboard access
top_10 = leaderboard.get_leaderboard("fortnite_match_123", top_n=10)
for rank, (player_id, score) in enumerate(top_10, 1):
    print(f"Rank {rank}: Player {player_id} - {score} points")

# Check player rank instantly
rank, score = leaderboard.get_player_rank(42, "fortnite_match_123")
print(f"Player 42: Rank #{rank}, Score: {score}")

# Wait for background writer
time.sleep(11)
print("Scores now persisted to database!")
```

**Performance Benefits:**

```
Without Write-Behind:
- Score update latency: 10-20ms (DB write)
- Max updates/second: ~50-100 per DB connection
- Database CPU: 80-100% under load

With Write-Behind:
- Score update latency: <1ms (cache only)
- Max updates/second: 10,000+ (cache limited)
- Database CPU: 10-20% (batched writes)
- Write coalescing: 1000 cache writes → 100 DB writes (10x reduction)
```

**Data Loss Mitigation:**

```python
class LeaderboardWithPersistence:
    """Write-Behind with Redis persistence for safety"""
    
    def __init__(self):
        # Configure Redis with AOF (Append-Only File) persistence
        self.cache = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True
        )
        
        # Enable AOF persistence via redis.conf:
        # appendonly yes
        # appendfsync everysec  # Flush to disk every second
        
        # Maximum data loss: 1-2 seconds of writes (vs minutes without persistence)
```

**When NOT to Use Write-Behind:**
- ❌ Financial transactions (require immediate persistence)
- ❌ Critical user data (passwords, personal info)
- ❌ Inventory management (risk of overselling)
- ❌ Regulatory compliance data (must be immediately persisted)

---

### 4. Read-Through Cache

**Description**: 

Read-Through is a caching pattern where the cache itself is responsible for loading data from the database on cache misses, making the database completely **transparent** to the application. The application only ever talks to the cache, never directly to the database.

**Key Concept**: The cache acts as an **intelligent proxy** that abstracts away the database layer. When data isn't in cache, the cache automatically retrieves it from the database, stores it, and returns it to the application - all without application involvement.

**How the pattern works conceptually**:
- On **reads**: Application → Cache → (if miss) Cache internally queries Database → Cache stores data → Cache returns to application
- The application is **database-agnostic** - it only knows about the cache interface
- The cache has **built-in data loading logic** - knows how to fetch from database on misses
- Similar to Cache-Aside but with **inverted responsibility**: cache manages DB interaction, not application

**Implementation approaches**:
- **Cache framework/library**: Tools like Spring Cache, Guava Cache provide read-through support
- **Custom cache layer**: Build a service that wraps both cache and database
- **Cache proxy pattern**: Cache implements same interface as data layer

**Difference from Cache-Aside**:
- **Cache-Aside**: Application checks cache → if miss, app reads DB → app writes to cache
- **Read-Through**: Application reads from cache → cache handles everything (transparent to app)

**Advantages**: Cleaner application code (no cache management logic), centralized caching behavior, easier to change cache strategy without touching application code.

**Limitation**: Requires cache system or framework that supports automatic data loading, or custom implementation of the proxy pattern. Not all caching systems provide this out-of-the-box.

**Flow Diagram:**
```
Read Request:
┌─────────────┐
│ Application │
└──────┬──────┘
       │ 1. Read(key) - only talks to cache
       ↓
┌─────────────┐
│    Cache    │  ← Smart cache
└──────┬──────┘
       │
       ├─ 2a. CACHE HIT? → Return value
       │
       └─ 2b. CACHE MISS?
           │ Cache automatically loads from DB
           ↓
       ┌─────────────┐
       │  Database   │
       └──────┬──────┘
              │
              └─ 3. Cache populates itself
                 4. Cache returns value to app

Application doesn't know about DB!
```

**Python Implementation (with Proxy Pattern):**
```python
class ReadThroughCache:
    def __init__(self):
        self.cache = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.db = psycopg2.connect("dbname=mydb user=postgres")
    
    def get(self, key):
        """Read-Through: Cache handles DB loading automatically"""
        # 1. Check cache
        cached_value = self.cache.get(key)
        
        if cached_value:
            print(f"CACHE HIT for {key}")
            return cached_value
        
        # 2. Cache miss - load from DB (cache does this, not app)
        print(f"CACHE MISS for {key} - loading from DB")
        value = self._load_from_db(key)
        
        if value:
            # 3. Populate cache
            self.cache.setex(key, 3600, value)
            return value
        
        return None
    
    def _load_from_db(self, key):
        """Internal method - cache loads from DB"""
        # Parse key (e.g., "user:1" -> table=user, id=1)
        parts = key.split(":")
        if parts[0] == "user":
            user_id = int(parts[1])
            cursor = self.db.cursor()
            cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            return result[0] if result else None
        return None

# Usage - Application only interacts with cache
cache = ReadThroughCache()
print(cache.get("user:1"))  # Cache loads from DB automatically
print(cache.get("user:1"))  # Cache hit
```

**Advantages:**
- ✅ Application code simplified (only talks to cache)
- ✅ Automatic cache population
- ✅ Cache misses are transparent to application
- ✅ Centralized caching logic

**Disadvantages:**
- ❌ Requires cache library/framework support
- ❌ Cold start penalty still exists
- ❌ Less flexible than cache-aside

**When to Use:**
- When using caching frameworks (Spring Cache, etc.)
- Want to abstract database from application
- Microservices with data access layer

---

### 5. Refresh-Ahead Cache

**Description**: 

Refresh-Ahead is an advanced, **proactive** caching pattern where the cache automatically refreshes data in the background **before** it expires, ensuring frequently accessed data is always fresh and never requires a cache miss. This is the opposite of lazy loading.

**Key Concept**: Instead of waiting for data to expire and serving a cache miss, the cache **predicts** which data will be needed soon (based on access patterns or TTL thresholds) and refreshes it in advance. This creates a "perpetually warm" cache for hot data.

**How the pattern works conceptually**:
- Cache tracks **TTL (Time-To-Live)** and access frequency for each entry
- When TTL falls below a threshold (e.g., 50% remaining) AND data is frequently accessed: trigger background refresh
- **Background process** asynchronously fetches fresh data from database and updates cache
- User requests **always hit cache** with fresh data - no waiting for DB queries

**Refresh strategies**:
1. **TTL-based**: Refresh when TTL < threshold (e.g., less than 30 minutes remaining on 1-hour TTL)
2. **Access-based**: Refresh only if data accessed recently (prevents wasting refreshes on stale data)
3. **Predictive**: Use machine learning to predict which data will be accessed soon
4. **Periodic**: Refresh hot data at fixed intervals (every 10 minutes for homepage data)

**Smart refresh logic**:
```
if (data_accessed_recently AND ttl_remaining < threshold):
    return cached_data  # Fast response to user
    trigger_async_refresh()  # Update cache in background
```

**Benefits over Cache-Aside/Read-Through**:
- **No cache miss penalty** for popular data - always served from cache
- **Predictable latency** - no occasional slow requests due to cache misses
- **Reduced database load** during traffic spikes (cache is pre-warmed)

**Drawbacks**:
- **Wasted refreshes**: May refresh data that won't be accessed again
- **Implementation complexity**: Needs access tracking, TTL monitoring, background workers
- **Requires good access pattern prediction**: Works best when you can identify "hot" data

**Perfect for**: E-commerce homepages, trending content, game leaderboards, stock prices, sports scores - any scenario where specific data is accessed very frequently and staleness is unacceptable.

**Flow Diagram:**
```
┌─────────────┐
│ Application │
└──────┬──────┘
       │ Read(key)
       ↓
┌─────────────┐
│    Cache    │
└──────┬──────┘
       │ Check TTL
       │
       ├─ If TTL > 50% remaining → Return value
       │
       └─ If TTL < 50% remaining → 
          1. Return cached value (fast)
          2. Trigger async refresh from DB
          ↓
       ┌─────────────┐
       │  Database   │  ← Refresh happens in background
       └─────────────┘
```

**Python Implementation:**
```python
import time
import threading

class RefreshAhead:
    def __init__(self):
        self.cache = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.db = psycopg2.connect("dbname=mydb user=postgres")
        self.ttl = 3600  # 1 hour
        self.refresh_threshold = 0.5  # Refresh when 50% of TTL remains
    
    def get_user(self, user_id):
        """Refresh-Ahead Read"""
        cache_key = f"user:{user_id}"
        
        # Get value and TTL
        cached_value = self.cache.get(cache_key)
        
        if cached_value:
            # Check remaining TTL
            ttl_remaining = self.cache.ttl(cache_key)
            
            if ttl_remaining < self.ttl * self.refresh_threshold:
                # TTL below threshold - trigger async refresh
                print(f"CACHE HIT for user {user_id} - triggering refresh")
                threading.Thread(target=self._refresh_cache, args=(cache_key, user_id)).start()
            else:
                print(f"CACHE HIT for user {user_id}")
            
            return cached_value
        
        # Cache miss - load and cache
        print(f"CACHE MISS for user {user_id}")
        return self._load_and_cache(user_id)
    
    def _refresh_cache(self, cache_key, user_id):
        """Background refresh"""
        print(f"Refreshing cache for user {user_id}")
        cursor = self.db.cursor()
        cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        
        if result:
            self.cache.setex(cache_key, self.ttl, result[0])
    
    def _load_and_cache(self, user_id):
        """Load from DB and cache"""
        cursor = self.db.cursor()
        cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        
        if result:
            cache_key = f"user:{user_id}"
            self.cache.setex(cache_key, self.ttl, result[0])
            return result[0]
        return None

# Usage
refresh_ahead = RefreshAhead()
print(refresh_ahead.get_user(1))  # CACHE MISS - loads from DB
time.sleep(1900)  # Wait ~30 minutes (> 50% of 1 hour TTL)
print(refresh_ahead.get_user(1))  # CACHE HIT - triggers background refresh
```

**Advantages:**
- ✅ Popular data never expires (always fresh)
- ✅ No cache miss penalty for frequently accessed data
- ✅ Predictable low latency
- ✅ Reduced database load during peak times

**Disadvantages:**
- ❌ Complex implementation
- ❌ Wasted refreshes for data that won't be accessed again
- ❌ Requires prediction of popular data
- ❌ Additional database load for refreshes

**When to Use:**
- High-traffic applications with hot data
- When cache misses are unacceptable (gaming, real-time apps)
- Predictable access patterns

---

### 6. Write-Around Cache

**Description**: 

Write-Around is an optimization of the Cache-Aside pattern specifically designed to prevent **cache pollution** from write-heavy workloads. Write operations completely bypass the cache and go directly to the database, ensuring cache space is reserved only for data that's actually being read.

**Key Concept**: Writes are **excluded from caching** because many write operations are for data that will rarely or never be read (logs, audit trails, bulk imports). By skipping cache on writes, you avoid wasting precious cache memory on data that doesn't benefit from caching.

**How the pattern works conceptually**:
- On **writes**: Application → Database directly (cache is never touched or is invalidated)
- On **reads**: Application → Cache → (if miss) load from Database → store in Cache
- The pattern assumes: **Write-once, read-rarely (or never)** access pattern
- Cache is populated **only by reads**, ensuring only accessed data uses cache space

**Cache pollution scenario (that Write-Around solves)**:
```
Scenario: Logging system writing 10,000 log entries per second

With Write-Through:
- All 10,000 logs/sec written to cache (using 100MB+ cache space)
- Only 10 logs/sec are ever read (for debugging)
- Result: 99.9% of cache space wasted on unread data

With Write-Around:
- 10,000 logs/sec written to DB only (cache bypassed)
- Only the 10 logs/sec that are read get cached
- Result: Cache space used efficiently for actually-read data
```

**Pattern variations**:
1. **Write-Around with Invalidation**: Write to DB, invalidate cache entry if exists
2. **Write-Around Pure**: Write to DB, don't touch cache at all (read will populate if needed)

**Difference from Cache-Aside**: Cache-Aside may optionally cache on write; Write-Around explicitly never caches on write.

**Perfect for**:
- **Bulk data imports**: Loading millions of records (most never accessed)
- **Logging/Audit systems**: High write volume, rare reads
- **Archive systems**: Write-once, read-rarely patterns
- **ETL pipelines**: Writing processed data that's queried infrequently

**Trade-off**: First read after write always misses cache (cold read), which is acceptable when reads are rare or happen much later than writes.

**Flow Diagram:**
```
Write Request:
┌─────────────┐
│ Application │
└──────┬──────┘
       │ 1. Write(key, value)
       ↓
┌─────────────┐
│  Database   │  ← Write directly to DB, skip cache
└─────────────┘
       │
       └─ Cache is NOT updated
          (Data will be cached on first read)

Read Request:
┌─────────────┐
│ Application │
└──────┬──────┘
       │ 1. Read(key)
       ↓
┌─────────────┐
│    Cache    │
└──────┬──────┘
       │
       ├─ 2a. CACHE HIT? → Return value
       │
       └─ 2b. CACHE MISS?
           │ Load from DB and cache it
           ↓
       ┌─────────────┐
       │  Database   │
       └──────┬──────┘
              │
              └─ 3. Cache the value
                 4. Return to app
```

**Python Implementation:**
```python
class WriteAround:
    def __init__(self):
        self.cache = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.db = psycopg2.connect("dbname=mydb user=postgres")
    
    def get_user(self, user_id):
        """Read with cache-aside logic"""
        cache_key = f"user:{user_id}"
        
        # 1. Try cache first
        cached_value = self.cache.get(cache_key)
        
        if cached_value:
            print(f"CACHE HIT for user {user_id}")
            return cached_value
        
        # 2. Cache miss - load from database
        print(f"CACHE MISS for user {user_id}")
        cursor = self.db.cursor()
        cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        
        if result:
            user_name = result[0]
            
            # 3. Cache the value for future reads
            self.cache.setex(cache_key, 3600, user_name)
            
            return user_name
        
        return None
    
    def create_user(self, user_id, name):
        """Write-Around: Write to DB only, bypass cache"""
        # Write directly to database (NO cache write)
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO users (id, name) VALUES (%s, %s)", (user_id, name))
        self.db.commit()
        
        print(f"Created user {user_id} in database (cache bypassed)")
        # Cache is NOT populated - will be cached on first read
    
    def update_user(self, user_id, new_name):
        """Write-Around: Update DB and invalidate cache"""
        cache_key = f"user:{user_id}"
        
        # 1. Write to database only
        cursor = self.db.cursor()
        cursor.execute("UPDATE users SET name = %s WHERE id = %s", (new_name, user_id))
        self.db.commit()
        
        # 2. Invalidate cache (if exists)
        # Data will be cached on next read
        self.cache.delete(cache_key)
        
        print(f"Updated user {user_id} in database and invalidated cache")

# Usage
write_around = WriteAround()

# Write - goes to DB, not cached
write_around.create_user(1, "John")

# First read - cache miss, loads from DB
print(write_around.get_user(1))  # CACHE MISS

# Second read - cache hit
print(write_around.get_user(1))  # CACHE HIT

# Update - writes to DB, invalidates cache
write_around.update_user(1, "Jane")

# Next read - cache miss (loads fresh data)
print(write_around.get_user(1))  # CACHE MISS
```

**Comparison with Cache-Aside:**
```python
# Cache-Aside: Can optionally cache on write
def update_user_cache_aside(user_id, new_name):
    db.update(user_id, new_name)
    cache.set(f"user:{user_id}", new_name)  # ← Cache updated

# Write-Around: Never cache on write
def update_user_write_around(user_id, new_name):
    db.update(user_id, new_name)
    cache.delete(f"user:{user_id}")  # ← Cache invalidated only
```

**Advantages:**
- ✅ Prevents cache pollution from write-heavy operations
- ✅ No wasted cache space for data that's rarely/never read
- ✅ Fast writes (only DB write, no cache overhead)
- ✅ Good for write-once-read-rarely scenarios
- ✅ Simple to implement

**Disadvantages:**
- ❌ First read after write always misses cache
- ❌ Higher read latency immediately after writes
- ❌ Not suitable for read-after-write patterns
- ❌ Poor cache hit rate for recently written data

**When to Use:**
- **Write-heavy workloads with infrequent reads**
  - Example: Logging, audit trails, archival data
- **Large data writes that won't be read immediately**
  - Example: Batch data imports, bulk uploads
- **When cache space is limited**
  - Avoid caching data that may never be read
- **Preventing cache pollution**
  - One-time writes, temporary data

**Real-World Use Cases:**

1. **Log Aggregation System:**
```python
class LogStorage:
    def write_log(self, log_id, log_data):
        """Logs are written but rarely read - use write-around"""
        # Write to database (no cache)
        self.db.insert_log(log_id, log_data)
        # Don't cache - logs are rarely queried
    
    def read_log(self, log_id):
        """Only cache if actually read"""
        cached = self.cache.get(f"log:{log_id}")
        if cached:
            return cached
        
        # Load from DB and cache
        log_data = self.db.get_log(log_id)
        self.cache.setex(f"log:{log_id}", 300, log_data)
        return log_data
```

2. **Batch Data Import:**
```python
class DataImporter:
    def import_bulk_data(self, data_list):
        """Bulk writes bypass cache - use write-around"""
        # Write thousands of records to DB
        for record in data_list:
            self.db.insert(record)
        
        # DON'T cache - most records won't be read
        # Only frequently accessed records will be cached on read
```

3. **User Activity Tracking:**
```python
class ActivityTracker:
    def track_event(self, user_id, event_type):
        """Write-around: Track events without caching"""
        # Store event in database
        self.db.insert_event(user_id, event_type, timestamp=now())
        
        # Don't cache individual events
        # Analytics queries will access DB directly
```

**Write-Around vs Other Strategies:**

| Aspect | Write-Around | Cache-Aside | Write-Through |
|--------|-------------|-------------|---------------|
| **Write to Cache** | ❌ No | Optional | ✅ Yes |
| **Write to DB** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Read After Write** | Cache miss | Cache hit (if cached) | Cache hit |
| **Cache Pollution** | Low | Medium | High |
| **Best For** | Rare reads | Frequent reads | Frequent reads |

---

### Caching Strategy Comparison

| Strategy | Read Performance | Write Performance | Consistency | Complexity | Best For |
|----------|-----------------|-------------------|-------------|------------|----------|
| **Cache-Aside** | Good (miss penalty) | Fast | Eventual | Low | General purpose, read-heavy |
| **Write-Through** | Excellent | Slow | Strong | Medium | Read-heavy, need consistency |
| **Write-Behind** | Excellent | Excellent | Eventual | High | Write-heavy, can tolerate loss |
| **Write-Around** | Good (miss after write) | Fast | Eventual | Low | Write-heavy, rare reads |
| **Read-Through** | Good (miss penalty) | N/A | Eventual | Medium | Abstraction, frameworks |
| **Refresh-Ahead** | Excellent | N/A | Eventual | High | Hot data, predictable patterns |

### Cache Eviction Policies

When cache is full, eviction policies determine which data to remove:

**1. LRU (Least Recently Used)**
- Evicts data not accessed for longest time
- Good for most use cases
- Commonly used default

**2. LFU (Least Frequently Used)**
- Evicts data accessed least often
- Good for long-term popular data
- Requires frequency tracking

**3. FIFO (First In, First Out)**
- Evicts oldest data first
- Simple but not optimal
- Ignores access patterns

**4. TTL (Time To Live)**
- Data expires after fixed time
- Prevents stale data
- Requires setting appropriate TTL values

**5. Random**
- Evicts random entry
- Very simple, unpredictable
- Rarely used in practice

### Cache Invalidation Strategies

Keeping cache in sync with database:

**1. Time-Based (TTL)**
```python
# Set TTL of 1 hour
cache.setex("user:1", 3600, "John")
```

**2. Event-Based (Active Invalidation)**
```python
# On update, delete cache
def update_user(user_id, new_name):
    db.update(user_id, new_name)
    cache.delete(f"user:{user_id}")  # Invalidate
```

**3. Cache Versioning**
```python
# Include version in key
cache.set("user:1:v2", "John")  # Version 2
```

**4. Publisher-Subscriber**
```python
# Use Redis pub/sub to invalidate across servers
def update_user(user_id, new_name):
    db.update(user_id, new_name)
    redis.publish("invalidate", f"user:{user_id}")

# Subscribers delete from their local cache
```

### Best Practices

1. **Set Appropriate TTLs**
   - Short TTL for frequently changing data (minutes)
   - Long TTL for static data (hours/days)
   - No TTL for permanent data

2. **Monitor Cache Performance**
   - Track hit rate (hits / total requests)
   - Target: 80%+ hit rate
   - Monitor latency (p50, p95, p99)

3. **Handle Cache Failures**
   - Always have database fallback
   - Use circuit breakers
   - Degrade gracefully

4. **Avoid Thundering Herd**
   - When cache expires, many requests hit DB
   - Solution: Refresh before expiry, use locks

5. **Cache Compression**
   - Compress large objects to save memory
   - Trade CPU for memory

6. **Security**
   - Don't cache sensitive data (passwords, credit cards)
   - Encrypt cached data if needed
   - Use authentication for cache access

### Complete Example: E-commerce Product Cache

```python
import redis
import psycopg2
import json
import hashlib
from datetime import datetime, timedelta

class ProductCache:
    def __init__(self):
        self.cache = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.db = psycopg2.connect("dbname=ecommerce user=postgres")
    
    def get_product(self, product_id):
        """Cache-Aside pattern for product retrieval"""
        cache_key = f"product:{product_id}"
        
        # Try cache first
        cached_data = self.cache.get(cache_key)
        if cached_data:
            print(f"✓ Cache HIT: product {product_id}")
            return json.loads(cached_data)
        
        # Cache miss - fetch from database
        print(f"✗ Cache MISS: product {product_id}")
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT id, name, price, stock, description 
            FROM products 
            WHERE id = %s
        """, (product_id,))
        
        result = cursor.fetchone()
        if not result:
            return None
        
        product = {
            'id': result[0],
            'name': result[1],
            'price': float(result[2]),
            'stock': result[3],
            'description': result[4]
        }
        
        # Cache for 1 hour
        self.cache.setex(cache_key, 3600, json.dumps(product))
        
        return product
    
    def update_product_price(self, product_id, new_price):
        """Write-Through pattern for price update"""
        cache_key = f"product:{product_id}"
        
        # Update database
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE products SET price = %s WHERE id = %s",
            (new_price, product_id)
        )
        self.db.commit()
        
        # Invalidate cache (next read will refresh)
        self.cache.delete(cache_key)
        
        print(f"Updated product {product_id} price to ${new_price}")
    
    def get_popular_products(self, category, limit=10):
        """Cache popular products with shorter TTL"""
        cache_key = f"popular:{category}:{limit}"
        
        cached_data = self.cache.get(cache_key)
        if cached_data:
            print(f"✓ Cache HIT: popular products in {category}")
            return json.loads(cached_data)
        
        print(f"✗ Cache MISS: popular products in {category}")
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT id, name, price 
            FROM products 
            WHERE category = %s 
            ORDER BY sales_count DESC 
            LIMIT %s
        """, (category, limit))
        
        products = [
            {'id': row[0], 'name': row[1], 'price': float(row[2])}
            for row in cursor.fetchall()
        ]
        
        # Cache for only 5 minutes (popular products change frequently)
        self.cache.setex(cache_key, 300, json.dumps(products))
        
        return products
    
    def record_view(self, product_id):
        """Write-Behind pattern for analytics (async)"""
        # Increment view count in cache immediately
        cache_key = f"views:{product_id}"
        new_count = self.cache.incr(cache_key)
        
        # Batch update to DB every 100 views
        if new_count % 100 == 0:
            cursor = self.db.cursor()
            cursor.execute(
                "UPDATE products SET view_count = view_count + 100 WHERE id = %s",
                (product_id,)
            )
            self.db.commit()
            print(f"Flushed 100 views for product {product_id} to database")
    
    def get_cache_stats(self):
        """Monitor cache performance"""
        info = self.cache.info('stats')
        hits = int(info.get('keyspace_hits', 0))
        misses = int(info.get('keyspace_misses', 0))
        total = hits + misses
        
        if total > 0:
            hit_rate = (hits / total) * 100
            print(f"Cache Hit Rate: {hit_rate:.2f}% ({hits} hits, {misses} misses)")
        else:
            print("No cache statistics available yet")

# Usage Example
product_cache = ProductCache()

# First access - cache miss
product = product_cache.get_product(123)
print(product)

# Second access - cache hit
product = product_cache.get_product(123)

# Update price - invalidates cache
product_cache.update_product_price(123, 29.99)

# Next access - cache miss (refreshed)
product = product_cache.get_product(123)

# Popular products
popular = product_cache.get_popular_products("electronics", 5)

# Track views (write-behind)
for i in range(150):
    product_cache.record_view(123)  # Flushes to DB at 100 and 200

# Check performance
product_cache.get_cache_stats()
```

### Summary

**Distributed Cache** solves the problem of sharing cached data across multiple application instances, ensuring consistency and scalability.

**Caching Strategies:**
- **Cache-Aside**: Application controls caching, best for general use
- **Write-Through**: Strong consistency, good for reads
- **Write-Behind**: High performance writes, eventual consistency
- **Write-Around**: Bypass cache on writes, prevents pollution, good for rare reads
- **Read-Through**: Abstraction, cache handles DB
- **Refresh-Ahead**: Proactive refresh, best for hot data

**Choose based on:**
- Read vs write ratio
- Consistency requirements
- Performance needs
- Complexity tolerance