# Composite Design Pattern

## Blogs and websites

## Medium

## Youtube

- [19. Design File System using Composite Design Pattern | Low Level Design Interview Question | LLD](https://www.youtube.com/watch?v=FLkCkUY7Wu0)

## Theory

### What is Composite Pattern?

Composes objects into tree structures to represent part-whole hierarchies. It lets clients treat individual objects and compositions uniformly.

**Why it's used:**
- When you want to represent part-whole hierarchies of objects
- When you want clients to ignore the difference between individual objects and compositions
- To build tree-like structures (file systems, UI components, organization charts)
- When you need recursive composition

---

### Diagram

```text
        Component
           ↓
    ┌──────┴──────┐
   Leaf        Composite
                   ↓
              [Component, Component, ...]
```
*Clients use the shared component interface, treating leaf and composite objects identically.*

---

### Real-Life Examples

- **File Systems:** Directories containing files and subdirectories (Windows Explorer, macOS Finder)
- **UI Component Trees:** React/Angular component hierarchies (containers with nested components)
- **Organization Charts:** Company hierarchy with departments and employees
- **Graphics Editors:** Grouped shapes in tools like Figma, Adobe Illustrator (group of shapes treated as single shape)
- **Menu Systems:** Nested menus with submenus and menu items (dropdown menus)
- **DOM Structure:** HTML elements containing other elements in web browsers

---

### Advantages

- Simplifies client code by treating individual and composite objects uniformly
- Makes it easy to add new component types
- Provides flexibility in structure composition
- Recursive composition becomes natural and elegant

---

### Disadvantages

- Can make design overly general
- Harder to restrict what components can be added to composites
- Type safety can be compromised if components are too generic

---

### When to Use

- You need to represent part-whole hierarchies of objects
- You want clients to treat individual objects and compositions uniformly
- The structure can have any level of complexity and is recursive in nature

---

### Pitfalls and Best Practices

**Pitfall:** Treating leaf and composite differently in client code defeats the purpose
**Best Practice:** Ensure uniform treatment; use common interface for operations

**Pitfall:** Unrestricted tree depth causing stack overflow in recursive operations
**Best Practice:** Set reasonable depth limits; use iterative traversal for very deep trees

---

### Testing Composite Pattern

- Test leaf and composite nodes separately
- Verify recursive operations work correctly
- Test edge cases (empty composites, single children)
- Validate tree traversal operations with various depths

---

### Performance Considerations

| Aspect | Impact |
|--------|--------|
| **Memory** | Medium (tree overhead) |
| **Runtime Cost** | Medium (traversal cost) |
| **Scalability** | Medium |

---

### Java Example

*Leaf and composite share one interface, so clients treat files and directories uniformly.*

```java
interface FileNode { int size(); }                 // Component: common interface
class File implements FileNode {                   // Leaf
    public int size() { return 1; }
}
class Directory implements FileNode {              // Composite: holds children
    private final List<FileNode> children = new ArrayList<>();
    public void add(FileNode node) { children.add(node); }
    public int size() { return children.stream().mapToInt(FileNode::size).sum(); }
}
```

---

### Real-World Java Example: Company Org Chart and Payroll

*HR software treats individual contributors and teams uniformly when computing headcount or payroll cost. A `Developer` is a leaf, a `Team` is a composite holding engineers and sub-teams, and finance code simply calls `monthlyCost()` on either.*

```java
import java.util.ArrayList;
import java.util.List;

// Component: common interface for leaves and composites
interface OrgUnit {
    double monthlyCost();
    int headcount();
    void print(String indent);
}

// Leaf: an individual employee with no reports
class Developer implements OrgUnit {
    private final String name;
    private final double salary;

    Developer(String name, double salary) {
        this.name = name;
        this.salary = salary;
    }

    @Override public double monthlyCost() { return salary; }
    @Override public int headcount() { return 1; }

    @Override
    public void print(String indent) {
        System.out.println(indent + "- " + name + " ($" + salary + ")");
    }
}

// Composite: a team that can hold developers AND sub-teams
class Team implements OrgUnit {
    private final String name;
    private final List<OrgUnit> members = new ArrayList<>();

    Team(String name) { this.name = name; }

    public void add(OrgUnit unit) { members.add(unit); }
    public void remove(OrgUnit unit) { members.remove(unit); }

    @Override
    public double monthlyCost() {
        double total = 0;
        for (OrgUnit m : members) total += m.monthlyCost();
        return total;
    }

    @Override
    public int headcount() {
        int total = 0;
        for (OrgUnit m : members) total += m.headcount();
        return total;
    }

    @Override
    public void print(String indent) {
        System.out.println(indent + "+ Team " + name);
        for (OrgUnit m : members) m.print(indent + "  ");
    }
}

// Client: finance treats a person and a whole org identically
class PayrollDemo {
    public static void main(String[] args) {
        Team backend = new Team("Backend");
        backend.add(new Developer("Asha", 9000));
        backend.add(new Developer("Ravi", 8000));

        Team platform = new Team("Platform");
        platform.add(backend); // nesting composites inside composites
        platform.add(new Developer("Mei", 9500));

        System.out.println("Headcount: " + platform.headcount());
        System.out.println("Burn: $" + platform.monthlyCost());
        platform.print("");
    }
}
```

*Why this fits Composite:*
- `PayrollDemo` never checks `instanceof`; it calls the same methods on leaves and teams.
- Nesting is free: a `Team` inside a `Team` just works, mirroring directories inside directories.
- Operations like cost roll-up, headcount, and pretty-printing are implemented once per level and recurse naturally.

---

### Composite vs Decorator

*Both use recursive composition, but Composite builds part-whole trees where children are peers, while Decorator stacks wrappers where each layer adds behaviour to a single object.*

| Aspect | Composite | Decorator |
|--------|-----------|-----------|
| **Intent** | Treat individual objects and groups uniformly in a tree | Add responsibilities to one object dynamically |
| **Structure** | One composite holds many children of the same interface | One decorator wraps exactly one component |
| **Method behaviour** | Composite aggregates results across children (sum, count) | Decorator delegates to the wrapped object then adds its bit |
| **Depth meaning** | Depth means nesting of groups (team within team) | Depth means layers of features (milk + sugar + foam) |
| **Typical example** | Org chart, file system, UI menu tree | Coffee condiments, `BufferedInputStream` over `FileInputStream` |

*Rule of thumb: if the client should ignore whether it holds one thing or a group of things, use Composite; if each wrapper should enrich the same single thing, use Decorator.*

---

### Interview Questions

**Q1: What is the difference between a safe Composite and a transparent Composite?**

A transparent Composite puts child-management methods (`add`, `remove`) on the shared component interface so clients treat everything uniformly, at the cost that leaves must implement meaningless methods (often by throwing). A safe Composite exposes `add`/`remove` only on the composite class, so leaves stay clean but clients must downcast to build the tree. Prefer the safe style in typed codebases, and use the transparent style when client uniformity matters more than leaf purity.

**Q2: How do you handle operations that only make sense for leaves or composites?**

Keep shared queries (cost, size, render) on the component interface, and push management operations to the composite class. If a transparent interface is required, have leaf implementations throw `UnsupportedOperationException` with a clear message rather than failing silently. Document which methods aggregate (composite sums children) versus which are leaf-local, so callers are not surprised when calling `headcount()` on a 500-person team triggers a full traversal.

**Q3: What are the performance and memory concerns with deep Composite trees?**

Every traversal visits the whole subtree, so repeated `monthlyCost()` calls on a huge org are O(n); cache aggregates or maintain running totals if reads dominate writes. Deep nesting also risks stack overflow in naive recursion, so consider iterative traversal for very deep trees. Memory overhead comes from child lists and parent pointers, which is usually fine but worth measuring when trees hold millions of leaves, as in scene graphs or document models.

**Q4: How do you test Composite structures?**

Test leaves in isolation first (a `Developer` returns its own salary and headcount 1). Then test composites with mixed children: empty team, team of only leaves, and nested teams three levels deep. Verify aggregation math, add/remove behaviour, and traversal order for `print()`. Finally, test degenerate cases: removing a missing child, very deep nesting, and null children if your API permits them, plus confirm the client never needs `instanceof` to get correct results.
