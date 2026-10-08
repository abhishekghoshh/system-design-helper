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

```text
    Component
        ↓
    ┌───┴───┐
Concrete  Decorator ──→ wraps Component
Component     ↓
      ConcreteDecorator
```
*Each decorator wraps a component, stacking behaviors at runtime without subclassing.*

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

---

### Java Example

*Each decorator wraps a component and adds one behavior, so combinations stay flexible.*

```java
interface Coffee { double cost(); }                  // Component
class BasicCoffee implements Coffee {                // Concrete component
    public double cost() { return 2.0; }
}
class MilkDecorator implements Coffee {              // Decorator: wraps a Coffee
    private final Coffee coffee;
    MilkDecorator(Coffee coffee) { this.coffee = coffee; }
    public double cost() { return coffee.cost() + 0.5; }
}
```

---

### Real-World Java Example: Notification Pipeline with Stackable Features

*Alerting pipelines need optional SMS, Slack, encryption, and retry behaviour in any combination. Subclassing every mix is hopeless; decorators let us stack exactly the features each alert needs at runtime.*

```java
// Component: the minimal notification contract
interface Notifier {
    void send(String message);
}

// Concrete component: plain email delivery
class EmailNotifier implements Notifier {
    @Override
    public void send(String message) {
        System.out.println("EMAIL: " + message);
    }
}

// Base decorator: holds a wrapped notifier and delegates by default
abstract class NotifierDecorator implements Notifier {
    protected final Notifier wrapped;
    protected NotifierDecorator(Notifier wrapped) { this.wrapped = wrapped; }

    @Override
    public void send(String message) { wrapped.send(message); }
}

// Concrete decorator 1: also posts to Slack
class SlackDecorator extends NotifierDecorator {
    SlackDecorator(Notifier wrapped) { super(wrapped); }

    @Override
    public void send(String message) {
        super.send(message); // keep earlier behaviour
        System.out.println("SLACK: " + message);
    }
}

// Concrete decorator 2: encrypts before delegating
class EncryptionDecorator extends NotifierDecorator {
    EncryptionDecorator(Notifier wrapped) { super(wrapped); }

    @Override
    public void send(String message) {
        super.send("[encrypted]" + message);
    }
}

// Concrete decorator 3: adds retry around the whole chain
class RetryDecorator extends NotifierDecorator {
    RetryDecorator(Notifier wrapped) { super(wrapped); }

    @Override
    public void send(String message) {
        int attempts = 0;
        while (true) {
            try {
                super.send(message);
                return;
            } catch (RuntimeException e) {
                if (++attempts >= 3) throw e;
            }
        }
    }
}

// Client: compose the pipeline in one line, reorder freely
class AlertingDemo {
    public static void main(String[] args) {
        Notifier pipeline = new RetryDecorator(
            new EncryptionDecorator(
                new SlackDecorator(new EmailNotifier())));
        pipeline.send("DB latency above 2s");
    }
}
```

*Why decorators beat inheritance here:*
- Three optional features would need 8 subclasses; decorators need 3 small classes plus any ordering.
- Order is meaningful and explicit: encrypt-then-send differs from send-then-encrypt, and the nesting shows it.
- Each decorator has one job, so testing `EncryptionDecorator` never involves Slack or retry logic.

---

### Decorator vs Proxy

*Both wrap another object with the same interface, but Decorator adds features the client asked for, while Proxy controls access to the real object on the client's behalf.*

| Aspect | Decorator | Proxy |
|--------|-----------|-------|
| **Intent** | Add responsibilities dynamically at runtime | Control access (lazy load, guard, cache, log) |
| **Who builds the chain** | Client composes decorators explicitly | Client usually does not know the proxy is there |
| **Interface** | Same interface; stacking many decorators is normal | Same interface; typically one proxy per concern |
| **Lifetime** | Wrapping is part of object construction | Proxy often manages the real object's lifecycle |
| **Typical example** | `EncryptionDecorator` around a notifier | Virtual proxy lazy-loading a heavy image |

*Rule of thumb: if the caller deliberately stacks toppings, it is a Decorator; if the wrapper secretly guards or defers the real thing, it is a Proxy.*

---

### Interview Questions

**Q1: Why is Decorator preferable to subclassing for optional features?**

Subclassing multiplies: N optional features need 2^N subclasses to cover every mix, and each new feature doubles the tree. Decorators need only N classes because features compose at runtime instead of compile time. Decorators also respect the Open/Closed Principle: new behaviour arrives as a new wrapper without editing existing notifiers. The trade-off is more small objects and longer construction lines, which builder or factory helpers can tame.

**Q2: How do Java I/O streams demonstrate Decorator?**

`java.io` is the textbook example: `FileInputStream` is the concrete component, while `BufferedInputStream`, `GZIPInputStream`, and `DataInputStream` are decorators that wrap any `InputStream`. Nesting them (`new BufferedInputStream(new GZIPInputStream(new FileInputStream(...)))`) stacks buffering, decompression, and typed reads in any order. Each decorator honours the `InputStream` contract, so downstream code cannot tell how many layers exist.

**Q3: What goes wrong with deep or misordered decorator chains?**

Deep chains add per-call delegation overhead and longer stack traces that are harder to debug; keep chains shallow or fuse hot paths when profiling demands it. Order bugs are subtler: encrypting after logging leaks plaintext, and retrying outside encryption retries cleanly while retrying inside may resend ciphertext incorrectly. Mitigate with clear naming, documented ordering constraints, and integration tests for each supported ordering rather than assuming all permutations work.

**Q4: How do you test Decorator chains?**

Test each decorator in isolation against a stub component: assert `EncryptionDecorator` transforms the message exactly once and delegates exactly once. Then test representative compositions (email plus Slack, full pipeline) to lock ordering semantics. Mock the wrapped notifier to verify delegation counts, which is how `RetryDecorator` tests assert three attempts on failure. Finally, confirm the outermost object still satisfies the `Notifier` contract so it can substitute for any plain notifier.
