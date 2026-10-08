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
```text
Singleton
├─ private static instance
├─ private constructor()
└─ public static getInstance()
      ↓
   returns single instance
```
*Clients access the sole instance through the static accessor instead of constructing it.*

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

```java
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

---

### Java Example

*Prefer the enum form: serialization-safe and thread-safe with no locking.*

```java
enum AppConfig {                                     // Enum singleton
    INSTANCE;
    private String env = "prod";
    public String getEnv() { return env; }
    public void setEnv(String env) { this.env = env; }
}
```

---

### Second Java Example: Metrics Registry (Observability Domain)

A process-wide metrics registry aggregates counters from every service. Lazy
holder initialization defers creating it until first use, stays thread-safe
without locking, and keeps the app-config enum example untouched.

```text
MetricsRegistry
├─ private constructor() — no external new
├─ Holder { static final MetricsRegistry INSTANCE }
└─ public static getInstance() → Holder.INSTANCE
       ↓
OrderService + PaymentService increment the same registry
       ↓
Prometheus scrape reads one snapshot
```

*The JVM creates the holder class exactly once on first access, which gives
lazy thread safety for free with no synchronized block.*

```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.LongAdder;

class MetricsRegistry {
    private final ConcurrentHashMap<String, LongAdder> counters =
        new ConcurrentHashMap<>();

    private MetricsRegistry() { }            // Block external construction

    private static class Holder {            // Loaded once, lazily, safely
        static final MetricsRegistry INSTANCE = new MetricsRegistry();
    }

    static MetricsRegistry getInstance() {
        return Holder.INSTANCE;
    }

    void increment(String name) {
        counters.computeIfAbsent(name, k -> new LongAdder()).increment();
    }

    long count(String name) {
        LongAdder adder = counters.get(name);
        return adder == null ? 0 : adder.sum();
    }
}

class OrderService {
    void placeOrder() {
        MetricsRegistry.getInstance().increment("orders.placed");
    }
}

class PaymentService {
    void charge() {
        MetricsRegistry.getInstance().increment("payments.charged");
    }
}

// Usage:
// MetricsRegistry registry = MetricsRegistry.getInstance();
// registry.increment("orders.placed");
```

*Use this shape for heavyweight shared infrastructure (registries, schedulers,
connection managers) where eager startup cost is unwanted but exactly one
instance must exist.*

### Singleton vs Static Utility Class

Both offer global access, but only one plays well with interfaces and tests.

| Aspect | Singleton | Static utility class |
|--------|-----------|----------------------|
| Instance | Exactly one object instance | No instance, static methods only |
| Interfaces | Can implement interfaces, injectable | Cannot implement interfaces cleanly |
| Lazy init | Possible (holder, enum, double-checked) | Class-load timing, harder to defer |
| Testability | Testable via interface plus test double | Hard to mock, callers bind to class |
| Subclassing | Possible (controlled hierarchies) | Not possible (static dispatch) |

**Rule of thumb:** shared stateful resource with an interface points to
Singleton; pure stateless helpers (`Math.max`, string utils) point to a
static utility class.

### Interview Q&A

**Q1: Why is the enum singleton the default answer in Java?**

The JVM instantiates each enum constant once, so it is thread-safe without
locking, immune to reflection attacks that break private constructors, and
serialization-safe by specification. The holder idiom above matches it for
laziness, but the enum does all three in three lines.

**Q2: What breaks the Singleton guarantee?**

Reflection (`setAccessible` on the constructor), deserialization (new instance
per `readObject` unless `readResolve` is defined), and cloning. The enum form
blocks all three. For non-enum singletons, throw in the constructor if an
instance exists, implement `readResolve`, and refuse `clone()`.

**Q3: Why do reviewers call Singleton an anti-pattern?**

Because it smuggles global mutable state into every caller, hiding
dependencies and coupling tests through execution order. The remedy is to use
it only for truly singular infrastructure, expose it behind an interface, and
inject that interface so tests can substitute a fake registry.

**Q4: Singleton vs dependency-injection container scope?**

A DI container can scope any bean as a singleton while keeping constructors
explicit and testable, which removes most hand-rolled singletons. Hand-roll
only when no container exists (libraries, agents, bootstrapping code) or when
the guarantee must hold regardless of container configuration.
