# Singleton Design Pattern

## Blogs and websites

## Medium

## Youtube

- [28. BUG in Double-Checked Locking of Singleton Pattern & its Fix | Low Level System Design Question](https://www.youtube.com/watch?v=upfrQvOgC24)

## Theory

Ensures a class has only one instance and provides a global point of access to it. Controls object creation to restrict the number of instances to exactly one.

**Why it's used:**
- When exactly one instance of a class is needed
- To provide controlled access to a single instance
- When the sole instance should be extensible by subclassing
- To manage shared resources (database connections, thread pools, caches)

**Diagram:**
```
Singleton
├─ private static instance
├─ private constructor()
└─ public static getInstance()
      ↓
   returns single instance
```

**Real-Life Examples:**
- **Configuration Management:** Application config loaded once (Spring ApplicationContext, Django settings)
- **Logging:** Single logger instance (Log4j, SLF4J)
- **Database Connection Pools:** HikariCP, C3P0 connection pool managers
- **Thread Pools:** Executor service instances in Java
- **Cache Managers:** Redis client, Memcached client singletons
- **File System:** File system representation in OS
- **Window Manager:** Single window manager in desktop environments
- **Driver Manager:** JDBC DriverManager

**Advantages:**
- Controlled access to sole instance
- Reduced namespace pollution
- Permits refinement through subclassing
- Variable number of instances can be controlled
- Lazy initialization saves resources

**Disadvantages:**
- Global state makes testing difficult
- Violates Single Responsibility Principle (controls creation + business logic)
- Difficult to unit test (tight coupling)
- Thread-safety issues in multithreaded environments
- Can be anti-pattern if overused
- Makes code less flexible

**When to Use:**
- Exactly one instance needed across the system
- Instance needs to be accessible from well-known access point
- Sole instance should be extensible through subclassing
- Managing shared resources (connections, caches, thread pools)

**Thread-Safe Implementation Approaches:**
- **Eager initialization:** Instance created at class loading
- **Lazy initialization with synchronized:** Double-checked locking
- **Bill Pugh Singleton:** Using inner static helper class
- **Enum Singleton:** Java enum (simplest, prevents serialization issues)

---

### Pitfalls and Best Practices

**Pitfall:** Overuse leading to global state, testing difficulties
**Best Practice:** Use dependency injection instead; limit to truly single resources; avoid business logic in singleton

**Pitfall:** Thread-safety issues with lazy initialization
**Best Practice:** Use enum singleton (Java), lazy holder idiom, or eager initialization

**Pitfall:** Singleton preventing unit testing
**Best Practice:** Use interfaces, dependency injection; make singleton testable

---

### Testing

- **Challenge:** Global state makes tests interdependent
- **Solution:** Use dependency injection; provide test doubles
- **Tip:** Reset singleton between tests or use fresh instances

```
// Instead of
MyService service = MySingleton.getInstance();

// Use dependency injection
MyService service = new MyService(injectedDependency);
```

---

### Performance Considerations

| Aspect | Detail |
|--------|--------|
| Memory Impact | **Low** (one instance) |
| Creation Cost | One-time only |
| Scalability | High |

**Optimization Tips:**
- Use lazy initialization for resource-intensive objects
- Consider enum singleton in Java (thread-safe, serialization-safe)
- Avoid business logic in singleton

---

### Anti-Patterns to Avoid

- Using Singleton for everything (anti-pattern: global variables in disguise)
- Singleton with business logic (violates SRP)
- Hidden dependencies through singletons
- Returning mutable singleton internals
- Not protecting singleton state

**Solution:** Use dependency injection; limit singletons to infrastructure; return defensive copies; immutable singletons
