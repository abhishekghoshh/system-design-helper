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
```
    Subject (Observable)
         ↓
    [Observer1, Observer2, Observer3]
         ↓
    update() when subject changes
```

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
