# Mediator Design Pattern

## Blogs and websites

## Medium

## Youtube

- [34. Design Online Auction System with Mediator Design Pattern | Low Level System Design](https://www.youtube.com/watch?v=bKM2lFPPmmY)

## Theory

### Mediator Pattern

**Theory:** Defines an object that encapsulates how a set of objects interact. Promotes loose coupling by keeping objects from referring to each other explicitly.

**Why it's used:**
- To reduce chaotic dependencies between objects
- When object relationships are complex and hard to understand
- When reusing an object is difficult due to tight coupling with many others
- To centralize complex communications and control logic

**Diagram:**
```text
   Component1 ↔→ Mediator ↔→ Component2
                     ↕
                Component3
   (all communicate through mediator)
```
*Components communicate only through the mediator instead of referencing each other directly.*

**Real-Life Examples:**
- **Chat Rooms:** Users send messages through chat room (mediator), not directly to each other
- **Air Traffic Control:** Airplanes communicate through ATC, not with each other
- **UI Dialog Boxes:** Form components interact through dialog controller
- **Event Bus:** Event-driven systems (EventBus in Android, MediatR in .NET)
- **Message Brokers:** Kafka, RabbitMQ mediating between producers and consumers
- **Orchestration Services:** Microservices orchestration (Saga pattern coordinator)
- **Game Controllers:** Game objects interact through game controller

**Advantages:**
- Reduces coupling between components
- Centralizes control logic
- Makes component relationships clearer
- Easier to understand and maintain complex interactions
- Components become more reusable

**Disadvantages:**
- Mediator can become a god object
- Can become complex if handling too many interactions
- May introduce single point of failure

**When to Use:**
- Many objects communicate in complex, well-defined ways
- Reusing objects is difficult due to dependencies
- Behavior distributed between classes should be customizable
- You want to centralize complex communications

---

### Pitfalls and Best Practices

**Pitfall:** Mediator becomes god object doing too much
**Best Practice:** Keep mediator focused; use multiple mediators for different concerns

---

### Testing Mediator Pattern

- Mock components to test mediator logic
- Test each component independently
- Verify mediator coordinates interactions correctly
- Test notification and message routing

---

### Java Example

*Users never reference each other; all messages flow through the chat room mediator.*

```java
class ChatRoom {                                     // Mediator: central hub
    void send(String from, String msg) { /* broadcast to members */ }
}
class User {                                         // Colleague: talks via mediator
    private final ChatRoom room;
    User(ChatRoom room) { this.room = room; }
    void send(String msg) { room.send("me", msg); }
}
```

---

### Second Java Example: Online Auction House

*Bidders never contact each other; all bids flow through the auction house mediator.*

```java
import java.util.ArrayList;
import java.util.List;

class Bid {                                          // Message object between colleagues
    final String bidder;
    final double amount;
    Bid(String bidder, double amount) {
        this.bidder = bidder; this.amount = amount;
    }
}

class AuctionHouse {                                 // Mediator: central coordinator
    private final List<Bidder> bidders = new ArrayList<>();
    private Bid highest = new Bid("none", 0);

    void register(Bidder bidder) { bidders.add(bidder); }

    void placeBid(Bid bid) {
        if (bid.amount <= highest.amount) {          // Central rule enforced once
            notifyBidder(bid.bidder, "Bid too low. Highest is " + highest.amount);
            return;
        }
        highest = bid;                               // Accept and broadcast
        for (Bidder b : bidders) {
            b.onNewHighest(bid);                     // Notify via mediator, not peer-to-peer
        }
    }

    private void notifyBidder(String name, String msg) {
        for (Bidder b : bidders) {
            if (b.name().equals(name)) b.onMessage(msg);
        }
    }

    Bid highest() { return highest; }
}

class Bidder {                                       // Colleague: only knows mediator
    private final String name;
    private final AuctionHouse house;
    Bidder(String name, AuctionHouse house) {
        this.name = name; this.house = house;
        house.register(this);                        // Join through mediator
    }
    String name() { return name; }
    void bid(double amount) { house.placeBid(new Bid(name, amount)); }
    void onNewHighest(Bid bid) { /* update UI, decide next bid */ }
    void onMessage(String msg) { /* private notice from mediator */ }
}

class AuctionDemo {
    public static void main(String[] args) {
        AuctionHouse house = new AuctionHouse();
        Bidder alice = new Bidder("Alice", house);
        Bidder bob = new Bidder("Bob", house);
        alice.bid(100);                              // Broadcast to all via house
        bob.bid(90);                                 // Rejected centrally: too low
        bob.bid(150);                                // New highest, all notified
        System.out.println(house.highest().amount);  // 150
    }
}
```

**Why this domain works:**
- N bidders would need N-to-N links without a mediator; with it each holds one reference.
- Bidding rules (minimum increment, closing time, reserve price) live in one place.
- Adding proxy bidding or sniper protection touches only the mediator, not every bidder.

---

### Mediator vs Observer

| Aspect | Mediator | Observer |
|---|---|---|
| Purpose | Centralize many-to-many communication through one hub | Broadcast one-to-many state changes to dependents |
| Communication | Colleagues talk to each other via the mediator object | Subject pushes updates; observers do not talk back through it |
| Coupling | Colleagues know only the mediator, not each other | Observers know the subject; subject knows only the interface |
| Typical use | Chat rooms, auction houses, ATC, dialog controllers, saga orchestrator | Event listeners, stock tickers, pub/sub, MVC model-to-view |
| Risk | Mediator can grow into a god object | Notification storms and cascading updates |

**Rule of thumb:** use Mediator when peers must interact in complex ways; use Observer when one
source simply notifies many passive listeners.

---

### Interview Questions and Answers

**Q1: How does Mediator reduce coupling compared to direct references?**
**A:** Without it, N components need up to N-squared links. With it, each component holds one
mediator reference and the interaction graph becomes a star. Components become reusable because
they no longer import each other — only the mediator interface.

**Q2: What stops the mediator from becoming a god object?**
**A:** Keep it to coordination only: routing, ordering, and shared rules. Push domain logic back
into colleagues, split by concern (one mediator per workflow: bidding vs payment vs shipping),
and extract policies (minimum increment) into separate strategy objects the mediator calls.

**Q3: Mediator vs Facade — are they the same?**
**A:** No. A Facade simplifies one direction (client → subsystem) with a static front door.
A Mediator manages two-way traffic between peers that know about the mediator. Facade hides
complexity; Mediator coordinates colleagues that would otherwise be tangled together.

**Q4: When should you avoid the Mediator pattern?**
**A:** Avoid it for simple one-to-one or one-to-many notifications where Observer suffices, or
when interactions are stable and few — the extra indirection hides the call flow. If only two
objects talk, let them talk directly; introduce a mediator once the interaction mesh hurts.

**Key takeaway:** Mediator replaces a tangled peer-to-peer mesh with a star topology — peers stay
simple while one coordinator owns the interaction logic.
