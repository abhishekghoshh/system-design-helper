# Adapter Design Pattern

## Blogs and websites

## Medium

## Youtube

- [20. Adapter Design Pattern with Examples, LLD | Low Level Design Interview Question | System Design](https://www.youtube.com/watch?v=8wrg7IsILhQ)

## Theory

### What is Adapter Pattern?

Converts the interface of a class into another interface that clients expect. Acts as a bridge between two incompatible interfaces.

**Why it's used:**
- When you want to use an existing class but its interface doesn't match what you need
- To create reusable classes that cooperate with unrelated or unforeseen classes
- When working with legacy code that cannot be modified
- To integrate third-party libraries with incompatible interfaces

---

### Diagram

```
    Client
       ↓
   [Target Interface]
       ↓
    Adapter  ──────→  [Adaptee]
   (converts)        (existing class)
```

---

### Real-Life Examples

- **Payment Gateways:** Adapting different payment providers (Stripe, PayPal, Razorpay) to a unified payment interface
- **Database Drivers:** JDBC adapters converting different database APIs (MySQL, PostgreSQL, Oracle) to a common interface
- **Logging Libraries:** SLF4J adapting various logging frameworks (Log4j, Logback, java.util.logging)
- **Cloud Storage:** Adapting AWS S3, Google Cloud Storage, Azure Blob Storage to a common file storage interface
- **Legacy System Integration:** Wrapping SOAP services to work with modern REST APIs

---

### Advantages

- Promotes code reusability without modifying existing code
- Follows Open/Closed Principle (open for extension, closed for modification)
- Increases flexibility when integrating third-party libraries
- Enables single client code to work with multiple incompatible interfaces

---

### Disadvantages

- Increases overall complexity by adding additional classes
- Can impact performance due to extra layer of indirection
- May be difficult to adapt if target interface is significantly different

---

### When to Use

- You need to use a third-party class but its interface doesn't match your requirements
- You want to create a reusable class that works with classes having incompatible interfaces
- You need to integrate legacy systems with modern architectures

---

### Pitfalls and Best Practices

**Pitfall:** Over-adapting - creating adapters when you could modify the source
**Best Practice:** Only use adapters for code you don't control (third-party libraries, legacy code)

**Pitfall:** Creating too many adapters making the codebase hard to navigate
**Best Practice:** Consolidate related adaptations; document adapter purpose clearly

---

### Testing Adapter Pattern

- Test that adapted interface works correctly
- Verify edge cases and error handling
- Mock the adaptee for isolated testing
- Ensure adapter forwards all operations faithfully

---

### Performance Considerations

| Aspect | Impact |
|--------|--------|
| **Memory** | Low (single wrapper) |
| **Runtime Cost** | Low |
| **Scalability** | High |
