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
```
ObjectPool
├─ available: List<Object>
├─ inUse: List<Object>
├─ acquire() → returns available or creates new
└─ release(obj) → returns to pool
      ↓
Client acquires → uses → releases
```

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
