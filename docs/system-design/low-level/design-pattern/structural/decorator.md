# Decorator Design Pattern

## Blogs and websites

## Medium

## Youtube

- [4. Decorator Design Pattern Explanation with Java Coding (Hindi) | LLD System Design](https://www.youtube.com/watch?v=w6a9MXUwcfY)

## Theory

### What is Decorator Pattern?

Attaches additional responsibilities to an object dynamically. Provides a flexible alternative to subclassing for extending functionality.

**Why it's used:**
- To add responsibilities to individual objects dynamically without affecting other objects
- When extension by subclassing is impractical or would create too many subclasses
- When you need to add/remove responsibilities at runtime
- To implement the Single Responsibility Principle by dividing functionality

---

### Diagram

```
    Component
        ↓
    ┌───┴───┐
Concrete  Decorator ──→ wraps Component
Component     ↓
      ConcreteDecorator
```

---

### Real-Life Examples

- **Java I/O Streams:** BufferedInputStream wrapping FileInputStream, adding buffering functionality
- **Middleware in Web Frameworks:** Express.js/Django middleware adding authentication, logging, compression to requests
- **Spring Framework:** @Transactional, @Cacheable annotations decorating methods with additional behavior
- **HTTP Clients:** Adding retry logic, authentication, logging to base HTTP client (OkHttp interceptors)
- **UI Components:** Adding scroll bars, borders, shadows to base components
- **Pizza/Coffee Shop:** Adding toppings/extras to base item with dynamic pricing

---

### Advantages

- More flexible than static inheritance
- Responsibilities can be added/removed at runtime
- Follows Single Responsibility Principle (each decorator handles one concern)
- Avoids feature-laden classes high in the hierarchy
- Enables mixing and matching of behaviors

---

### Disadvantages

- Many small objects can be created, making debugging harder
- Decorators and their components are not identical (instanceof checks fail)
- Can result in complex initialization code
- Order of decorators can matter, leading to potential bugs

---

### When to Use

- You need to add responsibilities to objects dynamically
- Extension by subclassing would result in an explosion of subclasses
- You want to add responsibilities that can be withdrawn
- You need different combinations of behaviors

---

### Pitfalls and Best Practices

**Pitfall:** Too many small decorator classes, making initialization complex
**Best Practice:** Limit number of decorators; consider builder pattern for complex configurations

**Pitfall:** Order-dependent decorators causing subtle bugs
**Best Practice:** Document decorator ordering requirements; use factory methods for standard combinations

---

### Testing Decorator Pattern

- Test each decorator in isolation
- Test decorator combinations
- Verify base component still works without decorators
- Test order sensitivity of decorators

---

### Performance Considerations

| Aspect | Impact |
|--------|--------|
| **Memory** | Medium (wrapper chain) |
| **Runtime Cost** | Medium (delegation chain) |
| **Scalability** | Medium |

**Tip:** Be mindful of deep decorator chains (stack overhead)
