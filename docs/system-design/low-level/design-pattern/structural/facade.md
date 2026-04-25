# Facade Design Pattern

## Blogs and websites

## Medium

## Youtube

- [25. Facade Design Pattern with Example | Facade Low Level Design Pattern | Facade Pattern LLD Java](https://www.youtube.com/watch?v=GYaBXK54eLo)

## Theory

### What is Facade Pattern?

Provides a unified, simplified interface to a set of interfaces in a subsystem. Makes the subsystem easier to use by providing a higher-level interface.

**Why it's used:**
- To provide a simple interface to a complex subsystem
- To reduce dependencies between clients and subsystem classes
- To layer your subsystems and define entry points to each level
- To make libraries easier to use and understand

---

### Diagram

```
      Client
        ↓
      Facade
        ↓
    ┌───┼───┐
   [A] [B] [C]
 (Complex Subsystem)
```

---

### Real-Life Examples

- **E-commerce Checkout:** OrderService facade hiding payment, inventory, shipping, notification subsystems
- **Spring Boot Starter:** Simplified configuration hiding complex auto-configuration logic
- **AWS SDK:** High-level clients (S3Client) hiding low-level API complexity
- **Video Encoding:** FFmpeg wrappers providing simple API over complex encoding operations
- **Home Automation:** Smart home hub providing unified control over lights, thermostat, security, entertainment
- **Compiler Front-end:** Simple compile() method hiding lexical analysis, parsing, semantic analysis

---

### Advantages

- Shields clients from complex subsystem components
- Promotes weak coupling between subsystems and clients
- Easier to use, understand, and test
- Provides a simple default view that's sufficient for most clients
- Doesn't prevent advanced users from accessing subsystem classes directly

---

### Disadvantages

- Can become a god object coupled to all subsystem classes
- May provide limited functionality if trying to stay simple
- Additional layer may impact performance slightly

---

### When to Use

- You want to provide a simple interface to a complex subsystem
- There are many dependencies between clients and implementation classes
- You want to layer your subsystems
- You need to decouple subsystem from clients and other subsystems

---

### Pitfalls and Best Practices

**Pitfall:** Creating a god object that does too much
**Best Practice:** Keep facade focused; multiple facades for different client needs is acceptable

**Pitfall:** Facade hiding too much, making debugging difficult
**Best Practice:** Allow direct access to subsystem classes when needed

---

### Testing Facade Pattern

- Mock subsystem components
- Test facade methods independently
- Verify error propagation from subsystems
- Test that facade correctly orchestrates subsystem calls

---

### Performance Considerations

| Aspect | Impact |
|--------|--------|
| **Memory** | Low |
| **Runtime Cost** | Low |
| **Scalability** | High |
