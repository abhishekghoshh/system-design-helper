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
```text
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
*The director drives the builder interface while each concrete builder assembles its own product.*

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

---

### Java Example

*The builder collects optional fields step by step, then validates once in build().*

```java
class User {                                         // Product: immutable result
    private final String email, name;
    private User(Builder b) { email = b.email; name = b.name; }
    static class Builder {                           // Builder: fluent setters
        private final String email; private String name = "";
        Builder(String email) { this.email = email; }
        Builder name(String n) { name = n; return this; }
        User build() { return new User(this); }      // Validate required fields here
    }
}
// Usage: User u = new User.Builder("a@x.com").name("Asha").build();
```

---

### Second Java Example: HTTP Request Builder (Networking Domain)

An HTTP client needs two required fields (method, URL) plus many optional ones
(headers, timeout, retries, body). The builder keeps the call site readable
and validates once at build time.

```text
HttpRequest.Builder
├─ required: method, url (constructor)
├─ optional: header(k,v), timeout(ms), retries(n), body(s)
└─ build() → validates → immutable HttpRequest
       ↓
HttpClient.send(request) — never sees a half-built request
```

*Required fields ride the builder constructor so they cannot be forgotten;
optional fields chain fluently and defaults live in one place.*

```java
import java.util.HashMap;
import java.util.Map;

class HttpRequest {
    private final String method;
    private final String url;
    private final Map<String, String> headers;
    private final int timeoutMs;
    private final int retries;
    private final String body;

    private HttpRequest(Builder builder) {
        this.method = builder.method;
        this.url = builder.url;
        this.headers = Map.copyOf(builder.headers);
        this.timeoutMs = builder.timeoutMs;
        this.retries = builder.retries;
        this.body = builder.body;
    }

    static class Builder {
        private final String method;         // Required
        private final String url;            // Required
        private final Map<String, String> headers = new HashMap<>();
        private int timeoutMs = 5_000;       // Sensible defaults
        private int retries = 1;
        private String body = "";

        Builder(String method, String url) {
            this.method = method;
            this.url = url;
        }

        Builder header(String key, String value) {
            headers.put(key, value);
            return this;
        }

        Builder timeoutMs(int timeoutMs) {
            this.timeoutMs = timeoutMs;
            return this;
        }

        Builder retries(int retries) {
            this.retries = retries;
            return this;
        }

        Builder body(String body) {
            this.body = body;
            return this;
        }

        HttpRequest build() {                // Single validation gate
            if (method == null || method.isBlank()) {
                throw new IllegalStateException("method is required");
            }
            if (url == null || url.isBlank()) {
                throw new IllegalStateException("url is required");
            }
            if (timeoutMs <= 0) {
                throw new IllegalStateException("timeout must be positive");
            }
            if (!body.isEmpty() && method.equals("GET")) {
                throw new IllegalStateException("GET must not carry a body");
            }
            return new HttpRequest(this);
        }
    }
}

// Usage:
// HttpRequest req = new HttpRequest.Builder("POST", "https://api.shop/orders")
//     .header("Authorization", "Bearer tok")
//     .timeoutMs(8000).retries(3).body("{\"id\":7}")
//     .build();
```

*Use this shape for any call with two required plus many optional parameters:
HTTP requests, S3 puts, email sends, or Kubernetes pod specs.*

### Builder vs Factory Method

Both create objects, but they divide the work differently.

| Aspect | Builder | Factory Method |
|--------|---------|----------------|
| Problem | Too many parameters, many optional | Subclass decides which type to create |
| Call shape | One type, step-by-step configuration | One call, hierarchy picks the type |
| Validation | Once in build() before freezing | In each product constructor |
| Immutability | Natural fit: mutable builder, frozen product | Depends on the product class |
| Cost | Extra builder class per product | Extra subclass per variant |

**Rule of thumb:** many optional fields on one type point to Builder; a family
of subtypes picked by context points to Factory Method. They compose well: a
factory can return a builder for each subtype.

### Interview Q&A

**Q1: What problem does Builder solve that constructors cannot?**

Telescoping constructors explode combinatorially once optional parameters
appear, and boolean-plus-int overloads become unreadable at call sites. The
builder names every argument (`timeoutMs(8000)`), holds defaults centrally,
and validates the whole object once, so adding a field never breaks existing
callers.

**Q2: Where should validation live?**

In `build()`, not in each setter. Setters stay lenient so chaining order does
not matter; `build()` checks cross-field rules (GET must not carry a body)
and required fields together. Fail fast with a clear message naming the
missing or inconsistent field.

**Q3: How do you enforce required vs optional fields?**

Pass required fields through the builder constructor (method plus URL above)
so the code cannot compile without them, and keep optional fields as chained
methods with defaults. For stronger guarantees, use a step builder where each
interface exposes only the next legal call.

**Q4: Does Builder hurt performance or thread safety?**

The cost is one short-lived builder per product, which the GC handles easily;
reuse a builder only by clearing it explicitly. The built product is immutable
(defensive copy of headers above), so it is freely shareable. Keep the builder
itself single-threaded and document that it is not thread-safe.
