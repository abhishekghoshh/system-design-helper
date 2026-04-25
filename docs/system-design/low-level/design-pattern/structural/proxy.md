# Proxy Design Pattern

## Blogs and websites

## Medium

## Youtube

- [13. Proxy Design Pattern Explanation (Hindi) | LLD | System Design Interview Question | Java](https://www.youtube.com/watch?v=9MxHKlVc6ZM)

## Theory

### What is Proxy Pattern?

Provides a surrogate or placeholder for another object to control access to it. Acts as an interface to something else.

**Types of Proxy:**
- **Virtual Proxy:** Delays expensive object creation until actually needed (lazy initialization)
- **Protection Proxy:** Controls access rights to the original object
- **Remote Proxy:** Represents an object in a different address space
- **Smart Proxy:** Performs additional actions when accessing an object (reference counting, caching, etc.)

---

### Diagram

```
      Client
        ↓
   [Subject Interface]
        ↓
    ┌───┴───┐
  Proxy   RealSubject
    ↓
 controls access to
 RealSubject
```

---

### Real-Life Examples

- **Virtual Proxy:** Lazy loading of high-resolution images (thumbnails load first, full image on demand)
- **Protection Proxy:** Role-based access control in enterprise applications (Spring Security)
- **Remote Proxy:** RPC frameworks (gRPC), REST clients representing remote services
- **Cache Proxy:** CDN proxies caching content closer to users (Cloudflare, Akamai)
- **Smart Proxy:** Hibernate lazy loading of database entities
- **Logging Proxy:** AOP proxies in Spring adding logging/monitoring to service calls
- **Nginx/HAProxy:** Reverse proxy controlling access to backend servers

---

### Advantages

- Controls access to the real object (security, lazy initialization)
- Adds functionality without changing the real object
- Provides location transparency for remote objects
- Optimizes resource usage through lazy initialization
- Can add caching, logging, access control transparently

---

### Disadvantages

- Adds extra layer of indirection (slight performance overhead)
- Increases complexity of the codebase
- Response time may increase in some cases
- Can make code harder to debug

---

### When to Use

- You need lazy initialization (virtual proxy)
- You need access control (protection proxy)
- You need local representation of remote object (remote proxy)
- You need additional functionality before/after accessing an object (smart proxy)
- You need caching of expensive operations

---

### Pitfalls and Best Practices

**Pitfall:** Forgetting to implement all methods of the real object's interface
**Best Practice:** Use composition and delegation systematically; consider dynamic proxies (Java)

**Pitfall:** Proxy becoming too complex with mixed responsibilities
**Best Practice:** Keep each proxy focused on one concern (access control OR caching OR logging)

---

### Testing Proxy Pattern

- Test proxy and real object separately
- Verify proxy forwards all operations correctly
- Test proxy-specific behavior (caching, lazy loading, access control)
- Verify proxy doesn't alter the real object's behavior unintentionally

---

### Performance Considerations

| Aspect | Impact |
|--------|--------|
| **Memory** | Low |
| **Runtime Cost** | Low-Medium (depends on proxy type) |
| **Scalability** | High |

**Tip:** Virtual proxy is excellent for deferring expensive operations
