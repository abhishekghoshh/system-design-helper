# State Design Pattern

## Blogs and websites

## Medium

## Youtube

- [16. Design Vending Machine (Hindi) | LLD of Vending Machine | State Design Pattern | LLD question](https://www.youtube.com/watch?v=wOXs5Z_z0Ew)

## Theory

### State Pattern

**Theory:** Allows an object to alter its behavior when its internal state changes. The object will appear to change its class.

**Why it's used:**
- When object behavior depends on its state
- When operations have large, multipart conditional statements based on state
- To eliminate complex conditional logic
- When state transitions are explicit and well-defined

**Diagram:**
```text
Context → State Interface
              ↓
    ┌─────────┼─────────┐
StateA     StateB    StateC
(behavior) (behavior) (behavior)
```
*The context delegates behavior to its current state object, swapping it on transitions.*

**Real-Life Examples:**
- **Order Processing:** Order states (Pending → Processing → Shipped → Delivered)
- **Connection States:** TCP connection (Closed → Listen → Established → Closing)
- **Document Workflow:** Draft → Review → Approved → Published
- **Vending Machine:** Idle → HasMoney → Dispensing states
- **Media Players:** Playing, Paused, Stopped states
- **Authentication:** Logged Out, Logged In, Session Expired
- **Elevator Control:** Moving Up, Moving Down, Idle, Maintenance

**Advantages:**
- Eliminates complex conditional statements
- Makes state transitions explicit
- Each state encapsulated in separate class
- Follows Single Responsibility and Open/Closed Principles
- Easy to add new states

**Disadvantages:**
- Increases number of classes
- Can be overkill for simple state machines
- State transitions logic might become scattered

**When to Use:**
- Object behavior depends on its state
- Operations have large conditional statements based on state
- State transitions are complex and explicit
- You want to avoid duplicate code in different states

---

### Pitfalls and Best Practices

**Pitfall:** Too many states; unclear transition logic
**Best Practice:** Document state machine; consider state machine libraries; validate transitions

---

### Testing State Pattern

- Test each state independently
- Verify state transitions are correct
- Test invalid transitions rejected
- Verify state-specific behavior

---

### Java Example

*The fan delegates presses to its current state object, which handles the transition.*

```java
interface FanState { FanState next(); }              // State interface
class Off implements FanState {                      // Concrete states
    public FanState next() { return new Low(); }
}
class Low implements FanState {
    public FanState next() { return new Off(); }
}
class Fan {                                          // Context: delegates to state
    private FanState state = new Off();
    public void press() { state = state.next(); }
}
```

---

### Second Java Example: Order Lifecycle

*An order delegates pay/ship/deliver/cancel to its current state; illegal transitions are rejected.*

```java
interface OrderState {                               // State interface
    OrderState pay(Order ctx);
    OrderState ship(Order ctx);
    OrderState deliver(Order ctx);
    OrderState cancel(Order ctx);
    String name();
}

abstract class BaseState implements OrderState {     // Default: reject everything
    public OrderState pay(Order ctx) { return reject("pay"); }
    public OrderState ship(Order ctx) { return reject("ship"); }
    public OrderState deliver(Order ctx) { return reject("deliver"); }
    public OrderState cancel(Order ctx) { return reject("cancel"); }
    private OrderState reject(String action) {
        System.out.println("Cannot " + action + " while " + name());
        return this;                                 // Stay in current state
    }
}

class PendingState extends BaseState {               // Initial state
    public String name() { return "PENDING"; }
    public OrderState pay(Order ctx) { return new PaidState(); }
    public OrderState cancel(Order ctx) { return new CancelledState(); }
}

class PaidState extends BaseState {
    public String name() { return "PAID"; }
    public OrderState ship(Order ctx) { return new ShippedState(); }
    public OrderState cancel(Order ctx) { return new CancelledState(); }
}

class ShippedState extends BaseState {
    public String name() { return "SHIPPED"; }
    public OrderState deliver(Order ctx) { return new DeliveredState(); }
}

class DeliveredState extends BaseState {
    public String name() { return "DELIVERED"; }     // Terminal: all actions rejected
}

class CancelledState extends BaseState {
    public String name() { return "CANCELLED"; }     // Terminal: all actions rejected
}

class Order {                                        // Context: delegates to state
    private OrderState state = new PendingState();
    private void move(OrderState next) {
        System.out.println(state.name() + " -> " + next.name());
        state = next;
    }
    void pay() { move(state.pay(this)); }
    void ship() { move(state.ship(this)); }
    void deliver() { move(state.deliver(this)); }
    void cancel() { move(state.cancel(this)); }
    String status() { return state.name(); }
}

class OrderDemo {
    public static void main(String[] args) {
        Order order = new Order();
        order.pay();                                 // PENDING -> PAID
        order.deliver();                             // Rejected: Cannot deliver while PAID
        order.ship();                                // PAID -> SHIPPED
        order.deliver();                             // SHIPPED -> DELIVERED
        order.cancel();                              // Rejected: terminal state
    }
}
```

**Why this domain works:**
- No sprawling `if (status == PAID && action == SHIP)` conditionals — each state owns its rules.
- Illegal transitions are explicit rejections, easy to log and alert on.
- New states (RETURNED, REFUNDED) are new classes; `Order` stays untouched.

---

### State vs Strategy

| Aspect | State | Strategy |
|---|---|---|
| Purpose | Change behaviour when internal state changes; states trigger transitions | Swap interchangeable algorithms at runtime on demand |
| Who switches | State objects themselves move the context to the next state | Client/context picks the strategy explicitly |
| Transitions | Core concern — explicit state machine (PENDING → PAID → SHIPPED) | No transitions; strategies are independent alternatives |
| Typical use | Orders, TCP connections, vending machines, media players, auth sessions | Payments, sorting, compression, pricing, route planning |
| Structure | Looks identical (context + interface + implementations) but intent differs | Same structure; chosen by caller, not by lifecycle |

**Rule of thumb:** use State when the object lifecycle drives which behaviour is valid; use
Strategy when the caller chooses among peer algorithms.

---

### Interview Questions and Answers

**Q1: State and Strategy look identical in UML — how do you tell them apart?**
**A:** By intent and switching: in State, the current state object decides the next state
(`pay()` returns `PaidState`) and the client just sends events. In Strategy, the client chooses
and swaps the algorithm directly. Ask "who triggers the switch — lifecycle or caller?" to decide.

**Q2: Where should transition logic live — in the context or in the state objects?**
**A:** Prefer states owning their own transitions (each state returns the next), keeping the
context thin. Centralize only when you need a bird's-eye transition table for auditing — then
use an enum transition map or a state-machine library so the full graph is visible in one place.

**Q3: How do you handle invalid transitions like delivering an unpaid order?**
**A:** Reject explicitly: default methods log and return `this`, optionally throwing
`IllegalStateException` for programming errors vs silently ignoring user errors. Add a test per
(state, event) pair and emit metrics on rejected transitions to catch client bugs early.

**Q4: When should you avoid State and use a simple enum switch instead?**
**A:** Avoid State for 2–3 states with trivial behaviour — an enum plus switch is clearer and
fewer files. Graduate to State when transitions multiply, states carry different data, or
conditionals spread across methods; consider a state-machine library past ~8 states.

**Key takeaway:** State replaces state-based conditionals with explicit state objects that own
their transitions — ideal when behaviour and valid actions depend on lifecycle stage.
