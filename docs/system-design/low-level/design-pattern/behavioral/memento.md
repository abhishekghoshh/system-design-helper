# Memento Design Pattern

## Blogs and websites

## Medium

## Youtube

- [38. Memento Design Pattern explanation | LLD System Design | Design pattern explanation in Java](https://www.youtube.com/watch?v=nTo7e2lpGZ4)

## Theory

### Memento Pattern

**Theory:** Captures and externalizes an object's internal state without violating encapsulation, allowing the object to be restored to this state later.

**Why it's used:**
- To implement undo/redo functionality
- To save and restore object state
- To provide snapshots of object state
- To maintain encapsulation while saving state

**Diagram:**
```
Originator → Memento (state snapshot)
    ↓           ↓
Caretaker (stores mementos)
```

**Real-Life Examples:**
- **Text Editors:** Undo/redo functionality (VS Code, Word)
- **Database Transactions:** Savepoints and rollback
- **Version Control:** Git commits storing file states
- **Game Save States:** Checkpoints in video games
- **Browser History:** Back/forward navigation
- **Form Auto-save:** Saving form state in browsers
- **Configuration Management:** Snapshots of system configuration

**Advantages:**
- Preserves encapsulation (internal state not exposed)
- Simplifies originator by delegating state storage
- Easy to implement undo/redo
- Provides state history

**Disadvantages:**
- Memory overhead for storing states
- Caretaker might not know when to delete old mementos
- Can be expensive if state is large
- Copying state might be costly

**When to Use:**
- You need to save/restore object state
- Direct interface to state would violate encapsulation
- You need undo/redo functionality
- You need snapshots of state at specific points

---

### Pitfalls and Best Practices

**Pitfall:** Memory bloat from storing too many states
**Best Practice:** Limit history size; implement incremental snapshots; compress old states

---

### Testing Memento Pattern

- Verify state saved and restored correctly
- Test multiple save/restore cycles
- Verify encapsulation (caretaker can't access state)
- Test memory limits for large states
