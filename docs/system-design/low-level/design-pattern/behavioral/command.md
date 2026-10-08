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
```text
Client → Command Interface
              ↓
         ConcreteCommand → Receiver
              ↓              (execute action)
          Invoker
        (stores & executes)
```
*The invoker triggers command objects that encapsulate both the action and its receiver.*

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

---

### Java Example

*The remote (invoker) triggers command objects, decoupling buttons from the light (receiver).*

```java
interface Command { void execute(); }                // Command interface
class Light { void on() { /* ... */ } void off() { /* ... */ } } // Receiver
class LightOnCommand implements Command {            // Concrete command
    private final Light light;
    LightOnCommand(Light light) { this.light = light; }
    public void execute() { light.on(); }
}
```

---

### Second Java Example: Text Editor with Undo/Redo

*Each keystroke becomes a command object; the editor keeps undo/redo stacks of commands.*

```java
interface EditCommand {                              // Command with undo support
    void execute();
    void undo();
}

class Document {                                     // Receiver: the text buffer
    private final StringBuilder text = new StringBuilder();
    void insert(int pos, String s) { text.insert(pos, s); }
    void delete(int pos, int len) { text.delete(pos, pos + len); }
    String content() { return text.toString(); }
}

class InsertCommand implements EditCommand {         // Concrete command
    private final Document doc;
    private final int pos;
    private final String chunk;
    InsertCommand(Document doc, int pos, String chunk) {
        this.doc = doc; this.pos = pos; this.chunk = chunk;
    }
    public void execute() { doc.insert(pos, chunk); }
    public void undo() { doc.delete(pos, chunk.length()); } // Inverse operation
}

class DeleteCommand implements EditCommand {
    private final Document doc;
    private final int pos;
    private final int len;
    private String removed = "";                     // State needed to undo
    DeleteCommand(Document doc, int pos, int len) {
        this.doc = doc; this.pos = pos; this.len = len;
    }
    public void execute() {
        removed = doc.content().substring(pos, pos + len);
        doc.delete(pos, len);
    }
    public void undo() { doc.insert(pos, removed); }
}

class Editor {                                       // Invoker: owns history stacks
    private final Deque<EditCommand> undo = new ArrayDeque<>();
    private final Deque<EditCommand> redo = new ArrayDeque<>();

    void run(EditCommand cmd) {
        cmd.execute();                               // Do it, then remember it
        undo.push(cmd);
        redo.clear();                                // New branch invalidates redo
    }
    void undo() {
        if (!undo.isEmpty()) {
            EditCommand cmd = undo.pop();
            cmd.undo();
            redo.push(cmd);
        }
    }
    void redo() {
        if (!redo.isEmpty()) {
            EditCommand cmd = redo.pop();
            cmd.execute();
            undo.push(cmd);
        }
    }
}

class EditorDemo {
    public static void main(String[] args) {
        Document doc = new Document();
        Editor editor = new Editor();
        editor.run(new InsertCommand(doc, 0, "hello"));
        editor.run(new InsertCommand(doc, 5, " world"));
        editor.undo();                               // Back to "hello"
        editor.redo();                               // Forward to "hello world"
        editor.run(new DeleteCommand(doc, 5, 6));    // Back to "hello"
        editor.undo();                               // Restores "hello world"
    }
}
```

**Why this domain works:**
- Sender (toolbar buttons, keyboard shortcuts) never touches the `Document` directly.
- Undo/redo, macros, and audit logs all reuse the same command objects.
- Queuing commands also enables async execution and collaborative editing.

---

### Command vs Strategy

| Aspect | Command | Strategy |
|---|---|---|
| Purpose | Encapsulate a request plus its receiver so it can be queued, logged, undone | Encapsulate interchangeable algorithms behind one interface |
| State | Commands often store parameters and history needed to undo | Strategies are usually stateless algorithm implementations |
| Who calls | An invoker (button, scheduler, queue) triggers `execute()` later | A context delegates work to the selected strategy immediately |
| Typical use | Undo/redo, job queues, macro recording, transactional operations | Payment methods, sorting, compression, pricing rules |
| Undo support | Natural fit — each command knows its inverse | Not applicable — strategies just compute a result |

**Rule of thumb:** use Command when you need to defer, queue, or undo a request; use Strategy
when you need to swap how something is computed at runtime.

---

### Interview Questions and Answers

**Q1: How does Command enable undo/redo?**
**A:** Each concrete command stores everything needed to reverse itself (prior text, position,
receiver reference). The invoker pushes executed commands onto an undo stack; undo pops and
calls `undo()`, redo re-executes. Bound the stacks to cap memory.

**Q2: Why not just call receiver methods directly instead of wrapping them in commands?**
**A:** Direct calls hardwire sender to receiver and lose queuing, logging, batching, retries, and
undo. Commands turn calls into objects you can store, serialize, send over the network, or
compose into macros — essential for job queues and collaborative editors.

**Q3: How do you avoid an explosion of tiny command classes?**
**A:** Use lambdas or method references for simple one-shot commands, group related commands with
a shared abstract base, and compose complex commands from simple ones. Only create full classes
when a command carries state, needs undo, or is reused across invokers.

**Q4: When should you avoid the Command pattern?**
**A:** Avoid it for single, immediate, never-repeated calls where a direct method call is clearer.
If you never queue, log, retry, or undo the operation, the extra classes add ceremony without
benefit — a plain method or `Runnable` is enough.

**Key takeaway:** Command turns requests into objects so senders stay decoupled from receivers —
unlocking queues, macros, audit trails, and undo/redo.
