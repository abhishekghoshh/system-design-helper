# Bridge Design Pattern

## Blogs and websites

## Medium

## Youtube

- [26. Bridge Design Pattern | LLD of Bridge Pattern with Example | Low Level Design of Bridge Pattern](https://www.youtube.com/watch?v=SOw1_W0taBg)

## Theory

### What is Bridge Pattern?

Decouples an abstraction from its implementation so that the two can vary independently. It separates the interface from the implementation by placing them in separate class hierarchies.

**Why it's used:**
- When you want to avoid permanent binding between abstraction and implementation
- When both abstraction and implementation should be extensible through subclassing
- When changes in implementation should not affect clients
- When you want to share implementation among multiple objects

---

### Diagram

```
    Abstraction ──────→ Implementation
        ↓                      ↓
 RefinedAbstraction    ConcreteImplementation
```

---

### Real-Life Examples

- **UI Frameworks:** Separating UI components (Button, Checkbox) from rendering engines (Windows, macOS, Linux)
- **Database Abstraction:** ORM frameworks separating query abstraction from database implementations (Hibernate with MySQL/PostgreSQL)
- **Notification Systems:** Message abstraction separate from delivery channels (Email, SMS, Push, Slack)
- **Device Drivers:** OS abstractions separated from hardware-specific implementations
- **Remoting Frameworks:** Remote objects abstraction independent of communication protocols (HTTP, TCP, gRPC)

---

### Advantages

- Decouples interface from implementation, both can vary independently
- Improves extensibility (can extend abstraction and implementation hierarchies independently)
- Hides implementation details from clients
- Reduces compile-time dependencies

---

### Disadvantages

- Increases complexity with additional abstraction layers
- Can make code harder to understand initially
- May be overkill for simple scenarios

---

### When to Use

- You want to avoid permanent binding between abstraction and implementation
- Both abstractions and implementations need to be extended independently
- Changes in implementation should have no impact on clients
- You want to share implementations across multiple objects

---

### Pitfalls and Best Practices

**Pitfall:** Premature abstraction when implementation is unlikely to change
**Best Practice:** Use only when you anticipate multiple implementations or platforms

**Pitfall:** Over-engineering simple problems with unnecessary indirection
**Best Practice:** Start simple; introduce Bridge when a second implementation is needed

---

### Testing Bridge Pattern

- Test abstraction and implementation independently
- Verify all combinations work
- Use dependency injection for testing different implementations
- Mock implementations to isolate abstraction testing

---

### Performance Considerations

| Aspect | Impact |
|--------|--------|
| **Memory** | Low |
| **Runtime Cost** | Low |
| **Scalability** | High |
