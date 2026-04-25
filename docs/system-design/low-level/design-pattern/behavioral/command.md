# Command Design Pattern

## Blogs and websites

## Medium

## Youtube

- [31. Design Undo, Redo feature with Command Pattern | Command Design Pattern| Low Level System Design](https://www.youtube.com/watch?v=E1lce5CWhE0)

## Theory

### Command Pattern

**Theory:** Encapsulates a request as an object, allowing you to parameterize clients with different requests, queue or log requests, and support undoable operations.

**Why it's used:**
- To parameterize objects with operations
- To queue operations, schedule their execution, or execute them remotely
- To support undo/redo functionality
- To structure a system around high-level operations built on primitive operations
- To decouple objects that invoke operations from objects that perform them

**Diagram:**
```
Client → Command Interface
              ↓
         ConcreteCommand → Receiver
              ↓              (execute action)
          Invoker
        (stores & executes)
```

**Real-Life Examples:**
- **GUI Buttons/Menus:** Button click triggers command object (Copy, Paste, Save commands)
- **Transaction Systems:** Database transactions as command objects with commit/rollback
- **Job Queues:** Background job processing (Celery, RabbitMQ task queues)
- **Undo/Redo:** Text editors, graphic design tools (Photoshop, Figma)
- **Remote Control:** TV remote buttons as commands
- **Macro Recording:** Recording sequence of commands to replay later
- **API Gateway:** Request encapsulation and routing in microservices

**Advantages:**
- Decouples invoker from receiver
- Easy to add new commands (Open/Closed Principle)
- Supports undo/redo operations
- Can assemble complex commands from simpler ones
- Supports logging and auditing of operations

**Disadvantages:**
- Increases number of classes (one per command)
- Can become complex with many command types
- Memory overhead for storing command history

**When to Use:**
- You need to parameterize objects with actions
- You need to queue, log, or support undo of operations
- You need to support transactions
- You want to decouple sender and receiver of requests

---

### Pitfalls and Best Practices

**Pitfall:** Too many command classes; complex command hierarchies
**Best Practice:** Use lambda expressions where possible; compose simple commands for complex ones

---

### Testing Command Pattern

- Test command execution separately from invoker
- Mock receiver for isolated command testing
- Test undo/redo functionality
- Verify command state and parameters
