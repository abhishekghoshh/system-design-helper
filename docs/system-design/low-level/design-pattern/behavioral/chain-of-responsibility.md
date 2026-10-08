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
```text
Client → Handler1 → Handler2 → Handler3 → null
         (process     (process    (process
          or pass)     or pass)    or pass)
```
*A request travels down the chain until a handler processes it or the chain ends.*

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

---

### Java Example

*Each logger handles its level or forwards the record down the chain.*

```java
abstract class Logger {                              // Handler: holds next in chain
    protected Logger next;
    void setNext(Logger next) { this.next = next; }
    abstract void log(String level, String msg);
}
class InfoLogger extends Logger {
    void log(String level, String msg) {
        if ("INFO".equals(level)) System.out.println(msg);
        else if (next != null) next.log(level, msg); // Pass along the chain
    }
}
```

---

### Second Java Example: Support Ticket Escalation

*Support tickets escalate L1 → L2 → L3; each level handles what it can and forwards the rest.*

```java
class Ticket {                                       // Request object travelling the chain
    final String severity;                           // LOW, MEDIUM, CRITICAL
    final String description;
    Ticket(String severity, String description) {
        this.severity = severity;
        this.description = description;
    }
}

abstract class SupportHandler {                      // Handler: holds next link
    protected SupportHandler next;
    void setNext(SupportHandler next) { this.next = next; }

    void handle(Ticket ticket) {
        if (canHandle(ticket)) {
            process(ticket);
        } else if (next != null) {
            next.handle(ticket);                     // Pass to next level
        } else {
            System.out.println("Unhandled ticket: " + ticket.description);
        }
    }

    protected abstract boolean canHandle(Ticket ticket);
    protected abstract void process(Ticket ticket);
}

class Level1Support extends SupportHandler {         // Handles LOW tickets
    protected boolean canHandle(Ticket t) { return "LOW".equals(t.severity); }
    protected void process(Ticket t) {
        System.out.println("L1 resolved: " + t.description);
    }
}

class Level2Support extends SupportHandler {         // Handles MEDIUM tickets
    protected boolean canHandle(Ticket t) { return "MEDIUM".equals(t.severity); }
    protected void process(Ticket t) {
        System.out.println("L2 resolved: " + t.description);
    }
}

class Level3Support extends SupportHandler {         // Handles CRITICAL tickets
    protected boolean canHandle(Ticket t) { return "CRITICAL".equals(t.severity); }
    protected void process(Ticket t) {
        System.out.println("L3 (expert) resolved: " + t.description);
    }
}

class HelpdeskDemo {                                 // Client: builds the chain once
    public static void main(String[] args) {
        SupportHandler l1 = new Level1Support();
        SupportHandler l2 = new Level2Support();
        SupportHandler l3 = new Level3Support();
        l1.setNext(l2);                              // Chain: L1 → L2 → L3
        l2.setNext(l3);
        l1.handle(new Ticket("LOW", "Password reset"));
        l1.handle(new Ticket("CRITICAL", "Prod DB down"));
        l1.handle(new Ticket("UNKNOWN", "Mystery bug")); // Falls off the end
    }
}
```

**Why this domain works:**
- Sender (helpdesk UI) knows only the head of the chain, not which level resolves it.
- New levels (for example, a Security team) plug in without touching the client.
- Ordering matters: cheap generalists first, expensive experts last.

---

### Chain of Responsibility vs Decorator

| Aspect | Chain of Responsibility | Decorator |
|---|---|---|
| Purpose | Find one handler to process a request | Add behaviour to an object dynamically |
| How request flows | Stops at first handler that can process it | Passes through every decorator in the stack |
| Link knowledge | Each handler knows only the next link | Each decorator wraps the next component |
| Typical use | Logging pipeline, filters, approvals, escalation | Streams (`BufferedInputStream`), UI borders, middleware enrichment |
| Failure mode | Request may go unhandled if no match | All layers always execute; order changes result |

**Rule of thumb:** use Chain when exactly one link should act; use Decorator when every layer should contribute.

---

### Interview Questions and Answers

**Q1: What happens if no handler in the chain can process the request?**
**A:** By default the request falls off the end and is silently dropped. Prevent this with a default
catch-all handler at the tail (for example, an `UnhandledTicketHandler` that logs and alerts),
plus validation that the chain is non-empty at startup.

**Q2: How is Chain of Responsibility different from a series of if-else statements?**
**A:** Behaviourally similar, but the chain decouples the sender from every receiver, lets you
reorder or add handlers at runtime, and gives each handler a single responsibility. A long
if-else lives in one method and must be edited every time a new case appears.

**Q3: How do you debug "which handler processed my request" in production?**
**A:** Log the handler name with each decision, add a correlation ID to the request object, and
emit a metric per handler. Keep chains short (3–5 links) so traces stay readable, and write a
unit test per handler plus an integration test asserting the order.

**Q4: When should you avoid Chain of Responsibility?**
**A:** Avoid it when every request must be handled deterministically, when ordering is irrelevant,
or when a simple map dispatch would do. A chain adds traversal overhead and makes the handling
path implicit, so prefer explicit dispatch for performance-critical or audit-sensitive paths.

**Key takeaway:** Chain of Responsibility routes one request to one anonymous handler through an
ordered pipeline — ideal for filters, escalation, and middleware.
