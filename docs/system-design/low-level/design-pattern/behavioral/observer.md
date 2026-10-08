# Observer Design Pattern

## Blogs and websites

## Medium

## Youtube

- [3. Observer Design Pattern Explanation (Hindi) | Design Interview Question | LLD System Design](https://www.youtube.com/watch?v=Ep9_Zcgst3U)

## Theory

### Observer Pattern

**Theory:** Defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

**Why it's used:**
- To maintain consistency between related objects
- When changes to one object require changing others
- When an object should notify others without knowing who they are
- To implement event handling systems

**Diagram:**
```text
    Subject (Observable)
         ↓
    [Observer1, Observer2, Observer3]
         ↓
    update() when subject changes
```
*The subject pushes updates to all registered observers when its state changes.*

**Real-Life Examples:**
- **Event Listeners:** DOM events (click, scroll) in JavaScript
- **Reactive Programming:** RxJS, React hooks, Vue reactivity
- **MVC Architecture:** Model notifies views of data changes
- **Pub/Sub Systems:** Message queues (Redis Pub/Sub, AWS SNS)
- **Social Media:** Followers notified when you post
- **Stock Market Apps:** Price change notifications to multiple dashboards
- **Newsletter Subscriptions:** Subscribers notified of new content

**Advantages:**
- Establishes loose coupling between subject and observers
- Supports broadcast communication
- Can add/remove observers dynamically
- Follows Open/Closed Principle

**Disadvantages:**
- Observers notified in random order
- Can cause memory leaks if observers not properly unsubscribed
- Can trigger unwanted cascading updates
- Hard to debug when many observers exist

**When to Use:**
- Changes to one object require changing others
- An object should notify others without knowing who they are
- You need broadcast-style communication
- You're implementing event-driven systems

---

### Pitfalls and Best Practices

**Pitfall:** Memory leaks from not unsubscribing; notification storms
**Best Practice:** Use weak references; implement unsubscribe; batch notifications

---

### Testing Observer Pattern

- Test subscribe/unsubscribe mechanisms
- Verify all observers notified
- Test notification order if relevant
- Check for memory leaks (unsubscribe)
- Mock observers for subject testing

---

### Java Example

*Observers register once and get pushed updates whenever the subject changes.*

```java
interface Observer { void update(double price); }    // Observer interface
class StockTicker {                                  // Subject (observable)
    private final List<Observer> observers = new ArrayList<>();
    public void subscribe(Observer o) { observers.add(o); }
    public void priceChanged(double price) {         // Notify all dependents
        for (Observer o : observers) o.update(price);
    }
}
```

---

### Second Java Example: Order Tracking Notifications

*An order (subject) pushes status changes; customer app, seller dashboard, and warehouse all observe.*

```java
import java.util.ArrayList;
import java.util.List;

interface OrderObserver {                            // Observer interface
    void onStatus(String orderId, String status);
}

class Order {                                        // Subject (observable)
    private final String orderId;
    private String status = "PLACED";
    private final List<OrderObserver> observers = new ArrayList<>();

    Order(String orderId) { this.orderId = orderId; }

    void subscribe(OrderObserver o) { observers.add(o); }
    void unsubscribe(OrderObserver o) { observers.remove(o); } // Avoid memory leaks

    void advance(String newStatus) {                 // State change triggers broadcast
        status = newStatus;
        for (OrderObserver o : observers) {
            o.onStatus(orderId, status);             // Push update to all dependents
        }
    }
    String status() { return status; }
}

class CustomerApp implements OrderObserver {         // Concrete observer: buyer UI
    public void onStatus(String orderId, String status) {
        System.out.println("SMS to customer: order " + orderId + " is " + status);
    }
}

class SellerDashboard implements OrderObserver {     // Concrete observer: seller view
    public void onStatus(String orderId, String status) {
        System.out.println("Dashboard refresh: " + orderId + " -> " + status);
    }
}

class WarehouseSystem implements OrderObserver {     // Concrete observer: logistics
    public void onStatus(String orderId, String status) {
        if ("PAID".equals(status)) System.out.println("Warehouse: pick items for " + orderId);
        if ("CANCELLED".equals(status)) System.out.println("Warehouse: restock " + orderId);
    }
}

class OrderDemo {
    public static void main(String[] args) {
        Order order = new Order("ORD-101");
        CustomerApp app = new CustomerApp();
        order.subscribe(app);                        // Dynamic subscribe
        order.subscribe(new SellerDashboard());
        order.subscribe(new WarehouseSystem());
        order.advance("PAID");                       // All three notified
        order.advance("SHIPPED");                    // All three notified again
        order.unsubscribe(app);                      // Customer mutes updates
        order.advance("DELIVERED");                  // Only seller + warehouse notified
    }
}
```

**Why this domain works:**
- Order never knows which UIs or services listen — new observers (fraud check, analytics)
  subscribe without touching `Order`.
- Push model keeps dashboards consistent without polling the database.
- Unsubscribe is explicit, preventing the classic observer memory leak.

---

### Observer vs Mediator

| Aspect | Observer | Mediator |
|---|---|---|
| Purpose | Broadcast state change from one subject to many dependents | Coordinate two-way interaction between many peers |
| Communication | One-way push: subject to observers | Many-to-many via central hub |
| Who knows whom | Subject knows only observer interface; observers know subject | Colleagues know only mediator; mediator knows all colleagues |
| Typical use | Stock tickers, order tracking, event listeners, MVC updates | Chat rooms, auction houses, ATC, dialog controllers |
| Risk | Notification storms, cascading updates, leaks | Mediator grows into a god object |

**Rule of thumb:** use Observer when one source notifies passive listeners; use Mediator when
peers need to talk back and forth through shared rules.

---

### Interview Questions and Answers

**Q1: How do you prevent memory leaks with observers?**
**A:** Always provide `unsubscribe` and call it on teardown (activity destroy, socket close),
use weak references (`WeakHashMap` or weak listeners) for UI observers, and bound the observer
list. In code review, every `subscribe` should have a visible matching `unsubscribe`.

**Q2: Push vs pull observer — which should you use?**
**A:** Push (subject sends the new price/status) is simpler and avoids extra queries, but couples
observers to the payload shape. Pull (subject sends "changed", observer queries state) is more
flexible when observers need different slices. Push for small payloads, pull for rich state.

**Q3: How do you handle an observer that throws during notification?**
**A:** Isolate failures: wrap each `update` call in try-catch so one bad observer cannot break the
loop, log and optionally auto-unsubscribe repeat offenders, and never hold locks while notifying.
For critical observers, queue notifications and retry asynchronously.

**Q4: When should you avoid Observer in favour of a message queue?**
**A:** Avoid in-process Observer when publishers and subscribers live in different services, need
durability, or must scale independently — then use SNS/Kafka/RabbitMQ. Observer is for
in-memory broadcast; queues add persistence, retries, and cross-process delivery.

**Key takeaway:** Observer keeps one subject loosely coupled to many dependents through push
updates — ideal for events, feeds, and reactive UIs when unsubscribe discipline is kept.
