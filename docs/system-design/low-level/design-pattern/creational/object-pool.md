# Object Pool Design Pattern

## Blogs and websites

## Medium

## Youtube

- [43. LLD: Object Pool Design Pattern | Creational Design Pattern | Low Level Design](https://www.youtube.com/watch?v=obmc24IHqew)

## Theory

Manages a pool of reusable objects, avoiding the cost of creating and destroying objects repeatedly. Objects are checked out from the pool, used, and returned for reuse.

**Why it's used:**
- When object creation is expensive (time or resources)
- When objects are needed for short periods and then discarded
- To limit the number of instances of a particular type
- To improve performance by reusing objects

**Diagram:**
```text
ObjectPool
├─ available: List<Object>
├─ inUse: List<Object>
├─ acquire() → returns available or creates new
└─ release(obj) → returns to pool
      ↓
Client acquires → uses → releases
```
*Clients check objects out of the pool and return them for reuse instead of creating new ones.*

**Real-Life Examples:**
- **Database Connection Pools:** HikariCP, C3P0, DBCP managing database connections
- **Thread Pools:** Java ExecutorService, .NET ThreadPool
- **HTTP Connection Pools:** Apache HttpClient connection manager
- **Game Development:** Bullet pools, particle effect pools, enemy pools
- **gRPC Channel Pools:** Reusing gRPC channels across requests
- **Socket Pools:** Reusing network sockets

**Advantages:**
- Reduces object creation/destruction overhead
- Controls maximum number of objects
- Improves performance for expensive objects
- Predictable resource usage

**Disadvantages:**
- Increased complexity for pool management
- Objects must be properly reset before reuse
- Pool sizing can be tricky (too small = contention, too large = waste)
- Can mask resource leaks if objects not returned

**When to Use:**
- Object creation is significantly expensive
- Objects are frequently created and destroyed
- Limited number of objects needed at any time
- Objects can be reused after proper reset

---

### Pitfalls and Best Practices

**Pitfall:** Not resetting object state before returning to pool
**Best Practice:** Always clean/reset objects on release; define a clear reset contract

**Pitfall:** Pool sizing issues (too small or too large)
**Best Practice:** Make pool size configurable; monitor usage; auto-scale if possible

**Pitfall:** Resource leaks from unreturned objects
**Best Practice:** Use try-with-resources or finally blocks; implement idle timeout eviction

---

### Testing

- Verify objects are properly reused (not recreated)
- Test pool exhaustion behavior (block vs. create new vs. error)
- Test concurrent access to the pool
- Verify objects are properly reset between uses

---

### Performance Considerations

| Aspect | Detail |
|--------|--------|
| Memory Impact | Medium (pre-allocated pool) |
| Creation Cost | **Low** (reuse) after initial allocation |
| Scalability | High (with proper sizing) |

**Optimization Tips:**
- Pre-warm the pool with minimum instances
- Use idle timeout to shrink pool during low usage
- Monitor pool hit rate and adjust sizing accordingly

---

### Java Example

*Borrowed objects are reset on release so the next borrower gets a clean instance.*

```java
class ConnectionPool {                               // Pool: reuses expensive objects
    private final Deque<Connection> free = new ArrayDeque<>();
    private final int max;
    ConnectionPool(int max) { this.max = max; }
    synchronized Connection acquire() {              // Check out, or create if room
        return free.isEmpty() ? new Connection() : free.pop();
    }
    synchronized void release(Connection c) {        // Return for reuse
        c.reset(); if (free.size() < max) free.push(c);
    }
}
```

---

### Second Java Example: Bullet Pool (Game Server Domain)

A shooter allocates hundreds of bullets per second. Instead of garbage
collecting dead bullets, the pool recycles them: acquire an inactive bullet,
fire it, then release it back when it hits or expires.

```text
BulletPool
├─ free: Deque<Bullet> (inactive, ready to fire)
├─ active: Set<Bullet> (in flight)
├─ acquire(x, y, vx, vy) → reset + activate
└─ release(bullet) → deactivate + return to free
       ↓
GameLoop acquires on shoot → updates active → releases on hit/expiry
```

*The pool bounds memory churn during firefights and makes worst-case
allocation predictable, which matters more than raw throughput here.*

```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashSet;
import java.util.Set;

class Bullet {
    double x, y, vx, vy;
    boolean active;

    void reset(double x, double y, double vx, double vy) {
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.active = true;
    }

    void move() {
        x += vx;
        y += vy;
    }

    void deactivate() {
        active = false;
    }
}

class BulletPool {
    private final Deque<Bullet> free = new ArrayDeque<>();
    private final Set<Bullet> active = new HashSet<>();
    private final int max;

    BulletPool(int max, int prewarm) {
        this.max = max;
        for (int i = 0; i < prewarm; i++) {  // Pre-warm avoids first-fight lag
            free.push(new Bullet());
        }
    }

    synchronized Bullet acquire(double x, double y, double vx, double vy) {
        if (free.isEmpty() && active.size() >= max) {
            return null;                     // Exhausted: caller skips or waits
        }
        Bullet bullet = free.isEmpty() ? new Bullet() : free.pop();
        bullet.reset(x, y, vx, vy);
        active.add(bullet);
        return bullet;
    }

    synchronized void release(Bullet bullet) {
        if (active.remove(bullet)) {
            bullet.deactivate();             // Reset so next shot starts clean
            if (free.size() < max) {
                free.push(bullet);
            }
        }
    }
}

// Usage:
// BulletPool pool = new BulletPool(500, 100);
// Bullet shot = pool.acquire(player.x, player.y, 0, -12);
// ... each tick: shot.move(); on hit: pool.release(shot);
```

*Use this shape for short-lived, high-frequency objects: bullets, particles,
network buffers, or thumbnail workers where allocation rate is the bottleneck.*

### Object Pool vs Flyweight

Both reuse objects, but they solve opposite problems.

| Aspect | Object Pool | Flyweight |
|--------|-------------|-----------|
| Reuse unit | Mutable instances checked out exclusively | Shared immutable intrinsic state |
| Concurrency | One borrower at a time per instance | Many clients share one instance |
| State handling | Must reset on release | Splits intrinsic vs extrinsic state |
| Pool size | Bounded and tuned (max, prewarm, eviction) | Unbounded cache keyed by value |
| Use when | Creation is expensive or rate is extreme | Millions of identical values coexist |

**Rule of thumb:** exclusive short-term checkout points to Object Pool;
simultaneous sharing of identical state points to Flyweight.

### Interview Q&A

**Q1: When does Object Pool actually help in modern Java?**

When object creation holds an expensive resource (sockets, DB connections,
large direct buffers) or when allocation rate triggers GC pauses, as in game
loops. For plain small POJOs the GC is faster than pool bookkeeping, so the
pool only adds contention.

**Q2: How do you handle pool exhaustion?**

Pick one policy and document it: block with timeout, grow temporarily, reject
fast with an error, or degrade (skip the bullet). The bullet pool above fails
fast with null so gameplay never stalls. Connection pools usually block
briefly then time out with a clear metric.

**Q3: What goes wrong if release forgets to reset state?**

The next borrower inherits stale position, credentials, or buffer contents —
a correctness bug and sometimes a security leak. Fix it with a single reset
method called only by the pool (not the borrower), plus a test that acquires,
dirties, releases, and re-acquires to assert clean state.

**Q4: How do you size and monitor the pool?**

Start from peak concurrency plus headroom, prewarm the minimum, and cap the
maximum from memory limits. Track in-use count, wait time, hit rate, and
evictions. Alert on sustained exhaustion and shrink idle objects with a
timeout so low-traffic periods do not hold memory.
