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

```text
    Abstraction ──────→ Implementation
        ↓                      ↓
 RefinedAbstraction    ConcreteImplementation
```
*The abstraction holds a reference to the implementation, letting both hierarchies vary independently.*

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

---

### Java Example

*The remote (abstraction) delegates to a device (implementation), so both vary independently.*

```java
interface Device { void turnOn(); void turnOff(); }      // Implementation interface
class TV implements Device {
    public void turnOn() { /* ... */ } public void turnOff() { /* ... */ }
}
abstract class Remote {                                  // Abstraction holds a Device
    protected Device device;
    Remote(Device device) { this.device = device; }
    abstract void togglePower();
}
```

---

### Real-World Java Example: Notification Senders and Message Types

*Notification systems vary along two axes: the kind of message (alert vs reminder) and the channel (email vs SMS). Bridge keeps these hierarchies separate so adding a new channel never forces changes to message logic.*

```java
// Implementation hierarchy: how a message is delivered
interface NotificationChannel {
    void send(String title, String body);
}

class EmailChannel implements NotificationChannel {
    @Override
    public void send(String title, String body) {
        System.out.println("[EMAIL] " + title + ": " + body);
    }
}

class SmsChannel implements NotificationChannel {
    @Override
    public void send(String title, String body) {
        String text = (title + " " + body);
        System.out.println("[SMS] " + text.substring(0, Math.min(160, text.length())));
    }
}

class PushChannel implements NotificationChannel {
    @Override
    public void send(String title, String body) {
        System.out.println("[PUSH] " + title + " -> " + body);
    }
}

// Abstraction hierarchy: what kind of message it is
abstract class Notification {
    protected final NotificationChannel channel;
    protected Notification(NotificationChannel channel) { this.channel = channel; }
    abstract void notifyUser(String message);
}

class UrgentAlert extends Notification {
    UrgentAlert(NotificationChannel channel) { super(channel); }

    @Override
    void notifyUser(String message) {
        channel.send("URGENT", message + " [priority=high, retry=3x]");
    }
}

class GentleReminder extends Notification {
    GentleReminder(NotificationChannel channel) { super(channel); }

    @Override
    void notifyUser(String message) {
        channel.send("Reminder", message + " [quiet-hours respected]");
    }
}

// Client: combine any message type with any channel at runtime
class NotificationDemo {
    public static void main(String[] args) {
        Notification alert = new UrgentAlert(new SmsChannel());
        alert.notifyUser("Server CPU above 95%");
        Notification reminder = new GentleReminder(new EmailChannel());
        reminder.notifyUser("Your report is due Friday");
    }
}
```

*Why this is a Bridge and not inheritance explosion:*
- Without Bridge you would need `UrgentEmailAlert`, `UrgentSmsAlert`, `ReminderEmail`, `ReminderSms`, and so on for every combination.
- With Bridge, adding `WhatsAppChannel` is one class, and adding `MarketingPromo` is one class; neither touches existing code.
- The abstraction (`Notification`) and implementation (`NotificationChannel`) are injected via composition, so they vary independently.

---

### Bridge vs Adapter

*The two patterns look similar because both sit between a caller and another object, but Bridge is a deliberate up-front split while Adapter is an after-the-fact fix.*

| Aspect | Bridge | Adapter |
|--------|--------|---------|
| **Intent** | Separate abstraction from implementation so each can evolve | Make an incompatible interface usable by the client |
| **Designed when** | Up front, when you foresee two dimensions of change | After the fact, when integrating legacy or third-party code |
| **Structure** | Two stable hierarchies linked by composition | One wrapper translating adaptee calls to the target |
| **Flexibility** | Both sides can be extended independently | Only the adapter is new; adaptee and client are fixed |
| **Typical example** | Message type bridging to delivery channel | Stripe SDK adapted to the app's `PaymentProcessor` interface |

*Rule of thumb: if you control both sides and want to avoid a class explosion, reach for Bridge; if one side is fixed and mismatched, reach for Adapter.*

---

### Interview Questions

**Q1: What problem does Bridge solve that plain inheritance cannot?**

Plain inheritance multiplies combinations: M abstractions times N implementations needs M x N classes. Bridge reduces this to M + N by composing the abstraction with the implementation interface instead of subclassing every pair. In the notification example, 2 message types and 3 channels need 5 classes with Bridge instead of 6 subclasses, and the gap widens as either side grows. It also lets you change one side at runtime by swapping the implementation object.

**Q2: How is Bridge different from Strategy?**

Structurally they both use composition with an injected interface, but their intent differs. Bridge splits a design into two long-lived hierarchies that evolve independently, while Strategy swaps a single algorithm at runtime. A Bridge implementation is usually a family of platform or channel classes the abstraction is built on; a Strategy is an interchangeable behaviour for one specific task. In practice, the channel side of a Bridge is sometimes implemented with Strategy-like injection, which is why interviewers probe the distinction.

**Q3: Give a real framework example of Bridge.**

JDBC is a classic Bridge: the `java.sql` abstraction (`Connection`, `Statement`) stays stable while each database vendor supplies its own driver implementation. AWT versus Swing rendering, and logging facades such as SLF4J binding to Logback or Log4j at deployment time, follow the same idea. In all these cases the application codes against the abstraction and the concrete implementation is chosen by configuration, exactly like passing an `SmsChannel` into an `UrgentAlert`.

**Q4: What are the trade-offs and pitfalls of Bridge?**

The main cost is added indirection and more types to understand: for a tiny system with one abstraction and one implementation, Bridge is over-engineering. Keep the implementation interface narrow and stable, because every implementation must honour it; a chatty or leaky interface forces changes across all channels. Also be careful that the abstraction does not silently depend on a specific implementation's quirks, which would defeat the decoupling. Test every abstraction against every implementation with a matrix test to catch such leaks.
