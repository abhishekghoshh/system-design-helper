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
```
   Component1 ↔→ Mediator ↔→ Component2
                     ↕
                Component3
   (all communicate through mediator)
```

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
