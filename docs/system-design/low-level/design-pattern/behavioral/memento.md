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
```text
Originator → Memento (state snapshot)
    ↓           ↓
Caretaker (stores mementos)
```
*The caretaker stores opaque snapshots that only the originator can create or restore.*

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

---

### Java Example

*The editor (originator) snapshots state into mementos the history (caretaker) stores.*

```java
class Editor {                                       // Originator
    private String text = "";
    public String save() { return text; }            // Memento: opaque snapshot
    public void restore(String snapshot) { text = snapshot; }
    public void type(String s) { text += s; }
}
class History {                                      // Caretaker: keeps snapshots
    private final Deque<String> stack = new ArrayDeque<>();
    void push(String s) { stack.push(s); }
    String pop() { return stack.pop(); }
}
```

---

### Second Java Example: Game Checkpoint System

*The player (originator) snapshots position, health, and level; the save manager (caretaker) stores them.*

```java
import java.util.ArrayDeque;
import java.util.Deque;

class GameMemento {                                  // Memento: opaque, immutable snapshot
    private final int level;
    private final int health;
    private final String position;
    GameMemento(int level, int health, String position) {
        this.level = level; this.health = health; this.position = position;
    }
    private int level() { return level; }            // Visible only to originator
    private int health() { return health; }
    private String position() { return position; }
    // Caretaker sees only an opaque object: no getters exposed to it.
}

class Player {                                       // Originator: owns the live state
    private int level = 1;
    private int health = 100;
    private String position = "spawn";

    void move(String where) { position = where; }
    void damage(int hp) { health = Math.max(0, health - hp); }
    void levelUp() { level++; health = 100; }

    GameMemento save() {                             // Create snapshot
        return new GameMemento(level, health, position);
    }
    void restore(GameMemento m) {                    // Restore from snapshot
        level = m.level(); health = m.health(); position = m.position();
    }
    public String toString() {
        return "L" + level + " hp=" + health + " @ " + position;
    }
}

class SaveManager {                                  // Caretaker: stores, never inspects
    private final Deque<GameMemento> checkpoints = new ArrayDeque<>();
    private final int maxSaves;
    SaveManager(int maxSaves) { this.maxSaves = maxSaves; }

    void checkpoint(GameMemento m) {
        checkpoints.push(m);
        while (checkpoints.size() > maxSaves) {      // Bound memory: drop oldest
            checkpoints.removeLast();
        }
    }
    GameMemento lastCheckpoint() { return checkpoints.peek(); }
    boolean hasSave() { return !checkpoints.isEmpty(); }
}

class GameDemo {
    public static void main(String[] args) {
        Player player = new Player();
        SaveManager saves = new SaveManager(3);      // Keep last 3 checkpoints
        player.move("forest"); saves.checkpoint(player.save());
        player.damage(80); player.move("cave");
        saves.checkpoint(player.save());
        player.damage(90);                            // Player "dies"
        if (saves.hasSave()) player.restore(saves.lastCheckpoint()); // Respawn at cave
        System.out.println(player);                   // L1 hp=20 @ cave
    }
}
```

**Why this domain works:**
- `SaveManager` never reads health or position, so `Player` internals stay encapsulated.
- Bounded history prevents runaway memory when checkpoints happen every few seconds.
- Same structure powers undo in editors, savepoints in transactions, and config rollback.

---

### Memento vs Command (for Undo)

| Aspect | Memento | Command |
|---|---|---|
| What is stored | Opaque snapshot of the originator's state | Request object with parameters plus its inverse operation |
| Undo mechanism | Restore prior snapshot wholesale | Execute the inverse action (delete inserted text) |
| Encapsulation | Caretaker cannot inspect state at all | Command often needs access to receiver internals |
| Memory profile | Heavy for large state; needs bounding/compression | Light when inverse is small; heavy when it stores copies |
| Typical use | Game saves, editor snapshots, transaction savepoints | Editor undo stacks, job queues, macros, audit logs |

**Rule of thumb:** use Memento when restoring whole state is simpler than inverting an action;
use Command when the inverse operation is cheap and you also want queuing or macros.

---

### Interview Questions and Answers

**Q1: How do you prevent Memento from causing memory bloat?**
**A:** Bound the history (for example, last 50 states), store incremental diffs instead of full
copies, compress or serialize old snapshots to disk, and drop redo branches on new edits.
Measure snapshot size early — a canvas with embedded images needs a different strategy.

**Q2: How does Memento preserve encapsulation if the caretaker holds the state?**
**A:** The memento is opaque to the caretaker: it stores the object but exposes no getters, or
uses a narrow interface (caretaker) vs wide interface (originator only). In Java this means
package-private accessors or an inner class, so only the originator can read or rebuild state.

**Q3: Memento vs serialization — when is a snapshot just `clone()` or JSON?**
**A:** Cloning or serializing is the mechanism; Memento is the discipline around it (who creates,
who stores, who restores). Use serialization when snapshots must persist or cross processes;
use in-memory mementos when undo is session-local and speed matters more than durability.

**Q4: When should you avoid the Memento pattern?**
**A:** Avoid it when state is huge and changes constantly (video frames, large datasets), when a
simple Command inverse is cheaper, or when you need durable history — then use event sourcing
or persistent snapshots instead of an in-memory stack that vanishes on restart.

**Key takeaway:** Memento externalizes state snapshots without breaking encapsulation — ideal for
checkpoints, savepoints, and bounded undo history.
