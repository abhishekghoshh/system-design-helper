# Chain of Responsibility Design Pattern

## Blogs and websites

## Medium

## Youtube

- [10. Design Logging System (Hindi) | Chain of Responsibility Design Pattern | System Design interview](https://www.youtube.com/watch?v=gvIn5QBdGDk)

## Theory

### Chain of Responsibility Pattern

**Theory:** Passes a request along a chain of handlers. Each handler decides either to process the request or to pass it to the next handler in the chain.

**Why it's used:**
- To decouple sender and receiver of a request
- When more than one object can handle a request, and the handler isn't known beforehand
- When you want to issue a request to one of several objects without specifying the receiver explicitly
- When the set of handlers should be specified dynamically

**Diagram:**
```
Client → Handler1 → Handler2 → Handler3 → null
         (process     (process    (process
          or pass)     or pass)    or pass)
```

**Real-Life Examples:**
- **Logging Frameworks:** Log4j, SLF4J filtering log messages through multiple handlers (Console, File, Database)
- **Servlet Filters:** Java Servlet filter chains processing HTTP requests/responses
- **Middleware Chains:** Express.js, ASP.NET Core middleware pipeline
- **Exception Handling:** Try-catch blocks in multiple layers (Controller → Service → DAO)
- **Support Ticket Systems:** L1 → L2 → L3 support escalation
- **Approval Workflows:** Manager → Director → VP → CEO approval chain

**Advantages:**
- Reduces coupling between sender and receiver
- Adds flexibility in assigning responsibilities
- Allows dynamic addition/removal of handlers
- Follows Single Responsibility Principle (each handler has one job)

**Disadvantages:**
- Request might go unhandled if chain not configured properly
- Can be hard to debug (which handler processed the request?)
- Performance overhead from traversing the chain
- No guarantee a request will be handled

**When to Use:**
- More than one object can handle a request
- Handler isn't known at compile time
- You want to decouple request sender from receivers
- Set of handlers should be dynamic

---

### Pitfalls and Best Practices

**Pitfall:** No guarantee request will be handled; chain too long
**Best Practice:** Have default handler at end; keep chain short; log which handler processes

---

### Testing Chain of Responsibility

- Test each handler in isolation
- Test chain configuration and order
- Verify request passes to next handler or terminates
- Test edge cases (empty chain, no handler matches)
