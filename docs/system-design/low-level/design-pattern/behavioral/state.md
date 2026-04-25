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
```
Context → State Interface
              ↓
    ┌─────────┼─────────┐
StateA     StateB    StateC
(behavior) (behavior) (behavior)
```

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
