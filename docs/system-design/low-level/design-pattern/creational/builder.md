# Builder Design Pattern

## Blogs and websites

## Medium

## Youtube

- [23. Builder Design Pattern with Examples, LLD | Low Level Design Interview Question | System Design](https://www.youtube.com/watch?v=qOLRxN5eVC0)

## Theory

Separates the construction of a complex object from its representation, allowing the same construction process to create different representations. Constructs complex objects step by step.

**Why it's used:**
- To create complex objects with many optional parameters
- When constructor has too many parameters (telescoping constructor problem)
- To create different representations of an object using same construction process
- To construct objects step-by-step with method chaining
- To make object creation more readable

**Diagram:**
```
Director
└─ construct() uses Builder
      ↓
Builder Interface
├─ buildPartA()
├─ buildPartB()
└─ getResult()
      ↓
ConcreteBuilder
└─ creates Product
```

**Real-Life Examples:**
- **HTTP Clients:** OkHttp, Apache HttpClient request builders
- **StringBuilder/StringBuffer:** Building strings incrementally
- **SQL Query Builders:** Hibernate Criteria, jOOQ, QueryDSL
- **Test Data Builders:** Creating complex test objects (Builder pattern for DTOs)
- **Configuration Objects:** Building complex configurations (Spring Boot builders)
- **Document Builders:** Creating HTML, XML, JSON documents
- **Meal Builders:** Restaurant orders (burger with custom toppings)
- **UI Dialog Builders:** Android AlertDialog.Builder

**Advantages:**
- Constructs objects step-by-step
- Reuses same construction code for different representations
- Isolates complex construction code
- Better control over construction process
- Immutable objects with many parameters
- More readable than telescoping constructors
- Follows Single Responsibility Principle

**Disadvantages:**
- Increases overall complexity (more classes)
- Requires creating separate builder for each product type
- Can be verbose for simple objects
- Mutable builder for immutable product creates complexity

**When to Use:**
- Object has many constructor parameters (especially optional ones)
- Construction process must allow different representations
- Step-by-step construction needed
- You want immutable objects with many fields
- Telescoping constructors become unmanageable

**Modern Variations:**
- **Fluent Builder:** Method chaining for readable construction
- **Lombok @Builder:** Annotation-based builder generation in Java
- **Step Builder:** Type-safe builder ensuring required fields set

---

### Pitfalls and Best Practices

**Pitfall:** Overuse for simple objects
**Best Practice:** Only use for complex objects with many parameters

**Pitfall:** Not validating object state
**Best Practice:** Validate in build() method; ensure required fields set

**Pitfall:** Mutable builder allowing inconsistent state
**Best Practice:** Consider immutable builders; validate at build time

---

### Testing

- Test builder with different combinations of parameters
- Verify validation in build() method
- Test required vs optional parameters
- Ensure immutability of built objects

---

### Performance Considerations

| Aspect | Detail |
|--------|--------|
| Memory Impact | Medium (builder objects) |
| Creation Cost | Medium |
| Scalability | High |

**Optimization Tips:**
- Reuse builder instances for multiple objects
- Consider object pooling for builders
- Use immutable products to enable caching

---

### Anti-Patterns to Avoid

- Using Builder for simple objects with 2-3 parameters
- Complex builder hierarchies

**Solution:** Use constructors for simple cases; keep builders simple
