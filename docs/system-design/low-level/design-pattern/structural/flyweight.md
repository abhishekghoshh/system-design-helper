# Flyweight Design Pattern

## Blogs and websites

## Medium

## Youtube

- [30. Design Word Processor using Flyweight Design Pattern | Low Level System Design FlyWeight Pattern](https://www.youtube.com/watch?v=Mwm6tB3x1do)

## Theory

### What is Flyweight Pattern?

Uses sharing to support large numbers of fine-grained objects efficiently. Minimizes memory usage by sharing common data between multiple objects.

**Why it's used:**
- When an application uses a large number of similar objects
- When storage costs are high because of the quantity of objects
- When most object state can be made extrinsic (separated from the object)
- When object identity is not important

**Key Concept:** Intrinsic state (shared) vs Extrinsic state (unique to each instance)

---

### Diagram

```text
FlyweightFactory
      ↓
   [Pool of Flyweights]
      ↓
   Flyweight (intrinsic state)
      +
   Context (extrinsic state)
```
*Shared flyweights hold intrinsic state while per-use context supplies the extrinsic state.*

---

### Implementation

Check which are the intrinsic and which are extrinsic properties, move out the extrinsic properties and make intrinsic properties as immutable.

---

### Real-Life Examples

- **Text Editors:** Character objects sharing font, color, style data (intrinsic) with position being extrinsic
- **Game Development:** Particle systems sharing texture, color data for thousands of bullets/particles
- **String Pooling:** Java String interning, Python string interning for memory optimization
- **Database Connection Pools:** Reusing connection objects instead of creating new ones
- **UI Icon Caching:** Sharing icon image data across multiple UI elements
- **Map Rendering:** Google Maps sharing tile images for same locations across multiple views

---

### Advantages

- Significantly reduces memory usage when many similar objects are needed
- Improves performance by reducing object creation overhead
- Centralizes state management for shared objects
- Scalable for large numbers of objects

---

### Disadvantages

- Increases complexity by separating intrinsic and extrinsic state
- Runtime costs for computing/maintaining extrinsic state
- Can make code harder to understand and maintain
- Thread-safety concerns when sharing objects

---

### When to Use

- Application uses large numbers of similar objects
- Storage costs are high due to quantity of objects
- Most object state can be made extrinsic
- Application doesn't depend on object identity
- Memory optimization is a critical requirement

---

### Pitfalls and Best Practices

**Pitfall:** Using flyweight when object count isn't a problem
**Best Practice:** Only apply when profiling shows memory/performance issues with large object counts

**Pitfall:** Incorrectly classifying state as intrinsic vs extrinsic
**Best Practice:** Carefully analyze which state is truly shared and immutable

---

### Testing Flyweight Pattern

- Verify object sharing works correctly
- Test thread-safety for shared objects
- Validate intrinsic vs extrinsic state separation
- Verify memory savings with profiling tools

---

### Performance Considerations

| Aspect | Impact |
|--------|--------|
| **Memory** | **Reduced** (sharing) |
| **Runtime Cost** | Medium (state management) |
| **Scalability** | **Very High** |

---

### Java Example

*The factory shares one glyph per character (intrinsic state); position stays extrinsic.*

```java
class Glyph {                                        // Flyweight: shared intrinsic state
    private final char ch;                           // e.g. character + font
    Glyph(char ch) { this.ch = ch; }
}
class GlyphFactory {
    private final Map<Character, Glyph> pool = new HashMap<>();
    public Glyph get(char ch) {                      // Reuse instead of recreating
        return pool.computeIfAbsent(ch, Glyph::new);
    }
}
```

---

### Real-World Java Example: Forest Rendering with Shared Tree Types

*A game map holds a million trees but only a dozen species. The species data (mesh, texture, colour) is intrinsic and shared, while each tree's coordinates and height are extrinsic and passed in at draw time.*

```java
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

// Flyweight: intrinsic (shared) state for one tree species
class TreeType {
    private final String name;    // e.g. "Oak"
    private final String texture; // heavy shared asset
    private final String colour;

    TreeType(String name, String colour, String texture) {
        this.name = name;
        this.colour = colour;
        this.texture = texture;
    }

    // Extrinsic state (x, y, height) arrives as parameters, never stored here
    void draw(int x, int y, int height) {
        System.out.println("Draw " + name + " at (" + x + "," + y
            + ") h=" + height + " [" + colour + "," + texture + "]");
    }
}

// Flyweight factory: one TreeType instance per species
class TreeTypeFactory {
    private final Map<String, TreeType> pool = new HashMap<>();

    TreeType get(String name, String colour, String texture) {
        String key = name + "|" + colour;
        TreeType existing = pool.get(key);
        if (existing == null) {
            existing = new TreeType(name, colour, texture);
            pool.put(key, existing);
        }
        return existing;
    }

    int speciesCached() { return pool.size(); }
}

// Context: tiny object holding extrinsic state plus a flyweight pointer
class Tree {
    private final int x, y, height;
    private final TreeType type; // shared reference, not a copy

    Tree(int x, int y, int height, TreeType type) {
        this.x = x; this.y = y; this.height = height; this.type = type;
    }

    void draw() { type.draw(x, y, height); } // extrinsic state passed through
}

// Client: a million Tree contexts share a handful of TreeType flyweights
class Forest {
    private final List<Tree> trees = new ArrayList<>();
    private final TreeTypeFactory factory = new TreeTypeFactory();

    void plant(int x, int y, int height, String species,
               String colour, String texture) {
        TreeType type = factory.get(species, colour, texture); // reused
        trees.add(new Tree(x, y, height, type));
    }

    void render() {
        for (Tree t : trees) t.draw();
        System.out.println("Trees=" + trees.size()
            + " species=" + factory.speciesCached());
    }
}
```

*Why the split matters:*
- Storing the texture inside every `Tree` would duplicate megabytes per instance; sharing one `TreeType` per species keeps memory nearly flat as the forest grows.
- `Tree` stays tiny (three ints plus one reference), so a million contexts remain affordable.
- The factory guarantees sharing: callers cannot accidentally create a second "Oak" flyweight with a different texture.

---

### Flyweight vs Singleton

*Both reduce instance counts, but Singleton restricts a class to one global instance while Flyweight maintains a pool of shared instances keyed by intrinsic state.*

| Aspect | Flyweight | Singleton |
|--------|-----------|-----------|
| **Instance count** | Many shared instances, one per distinct key | Exactly one instance per classloader |
| **State split** | Strict intrinsic (shared) vs extrinsic (caller-supplied) | Single global state, often mutable |
| **Lookup** | Factory pool keyed by value (`computeIfAbsent`) | Global accessor (`getInstance()`) |
| **Memory goal** | Support huge object counts by sharing internals | Ensure one coordinator (config, connection pool) |
| **Typical example** | `TreeType` per species, glyph per character | Application config holder, logger instance |

*Rule of thumb: if the question is "how do we hold a million of these cheaply", use Flyweight; if it is "how do we ensure there is only one of these", use Singleton.*

---

### Interview Questions

**Q1: What is intrinsic vs extrinsic state, and why does the split matter?**

Intrinsic state is shareable and context-free (character shape, tree texture), so it lives inside the flyweight. Extrinsic state varies per use (cursor position, tree coordinates), so the caller stores it and passes it into each operation. Getting the split wrong breaks sharing: smuggling position into `TreeType` forces one instance per tree and deletes all memory savings. A good check is whether the field can be a method parameter; if yes, it is probably extrinsic.

**Q2: How does Flyweight differ from a simple cache?**

A cache stores computation results to avoid recomputation and uses eviction when entries go stale. A flyweight pool stores canonical shared objects that define identity: every "Oak" reference points to the same instance for the program's lifetime, with no expiry. Caches optimise time, while flyweights optimise memory at scale. In practice a flyweight factory may use cache-like maps, but entries are never evicted merely for age because sharing is the correctness mechanism.

**Q3: What are the concurrency and mutability pitfalls?**

Flyweights must be immutable (or at least never mutated through the shared reference), because one stray setter corrupts every context using that instance. Make intrinsic fields `final` and perform all mutation on the extrinsic context objects. For thread safety, build the factory pool with `ConcurrentHashMap` and `computeIfAbsent`, or pre-populate it at startup. Also watch key design: a sloppy key (ignoring font size when it affects rendering) merges distinct flyweights and produces visual bugs.

**Q4: How do you prove Flyweight is worth it?**

First measure: profile heap usage with and without sharing over a realistic object count, since flyweight machinery is unjustified for hundreds of small objects. Assert sharing directly in tests by checking reference equality (`factory.get('a') == factory.get('a')`) and by counting pool size after inserting duplicates. Load-test rendering or drawing loops to confirm CPU cost of passing extrinsic state stays acceptable. Finally, verify correctness under sharing: mutate one context's extrinsic state and confirm no sibling context changes.
