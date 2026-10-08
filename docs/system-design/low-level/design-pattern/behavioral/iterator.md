# Iterator Design Pattern

## Blogs and websites

## Medium

## Youtube

- [33. Iterator Design Pattern Explained with Example | Low Level Design](https://www.youtube.com/watch?v=X7shKHOaYtU)

## Theory

### Iterator Pattern

**Theory:** Provides a way to access elements of a collection sequentially without exposing its underlying representation.

**Why it's used:**
- To access a collection's elements without exposing its internal structure
- To support multiple traversals of aggregate objects
- To provide a uniform interface for traversing different aggregate structures
- To decouple collection traversal from the collection itself

**Diagram:**
```text
Client → Iterator Interface
              ↓
        ConcreteIterator ← Aggregate
         (hasNext, next)    (collection)
```
*The iterator exposes sequential access while the aggregate keeps its internal structure hidden.*

**Real-Life Examples:**
- **Java Collections:** Iterator interface for List, Set, Map traversal
- **Python Generators:** yield-based iteration over sequences
- **Database Cursors:** ResultSet in JDBC, database query result iteration
- **File System Navigation:** Directory tree traversal
- **Streaming APIs:** Java Stream API, RxJS observables
- **Pagination:** API pagination cursors (GraphQL connections, REST page tokens)
- **DOM Traversal:** NodeIterator, TreeWalker in web browsers

**Advantages:**
- Simplifies aggregate interface (no traversal methods needed)
- Multiple iterators can traverse same aggregate simultaneously
- Supports different traversal algorithms
- Follows Single Responsibility Principle

**Disadvantages:**
- Overkill for simple collections
- Less efficient than direct access for some collections
- Iterator can become invalid if collection is modified during iteration

**When to Use:**
- You need to traverse a collection without exposing its structure
- You need multiple traversal algorithms
- You want a uniform interface for different collection types
- Collection structure might change but traversal code shouldn't

---

### Pitfalls and Best Practices

**Pitfall:** Modifying collection during iteration (ConcurrentModificationException)
**Best Practice:** Use fail-fast iterators; consider copy-on-write for concurrent access

---

### Testing Iterator Pattern

- Test hasNext/next contract
- Verify iteration over empty/single/multiple elements
- Test concurrent modification behavior
- Validate different traversal orders

---

### Java Example

*The collection exposes an iterator so traversal stays decoupled from storage.*

```java
class BookShelf implements Iterable<String> {        // Aggregate
    private final List<String> books = new ArrayList<>();
    public void add(String book) { books.add(book); }
    public Iterator<String> iterator() { return books.iterator(); } // Iterator
}
// Client: for (String book : shelf) { /* ... */ }  // Uniform traversal
```

---

### Second Java Example: Depth-First File Tree Iterator

*Clients walk a directory tree with hasNext/next while the traversal stack stays hidden inside.*

```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;

class FileNode {                                     // Aggregate element
    final String name;
    final boolean directory;
    final List<FileNode> children;                   // Empty for plain files
    FileNode(String name, boolean directory, List<FileNode> children) {
        this.name = name;
        this.directory = directory;
        this.children = children;
    }
    static FileNode file(String name) {
        return new FileNode(name, false, List.of());
    }
    static FileNode dir(String name, FileNode... kids) {
        return new FileNode(name, true, List.of(kids));
    }
}

class DepthFirstIterator implements Iterator<FileNode> { // Concrete iterator
    private final Deque<Iterator<FileNode>> stack = new ArrayDeque<>();
    private FileNode nextFile;                        // Lookahead for hasNext

    DepthFirstIterator(FileNode root) {
        stack.push(List.of(root).iterator());
        advance();                                    // Prime the lookahead
    }

    private void advance() {
        nextFile = null;
        while (!stack.isEmpty()) {                    // Walk until a file found
            Iterator<FileNode> top = stack.peek();
            if (!top.hasNext()) { stack.pop(); continue; }
            FileNode node = top.next();
            if (node.directory) {
                stack.push(node.children.iterator()); // Descend, keep hiding stack
            } else {
                nextFile = node;                      // Found next file to yield
                return;
            }
        }
    }

    public boolean hasNext() { return nextFile != null; }

    public FileNode next() {
        if (nextFile == null) throw new NoSuchElementException();
        FileNode current = nextFile;
        advance();                                    // Move lookahead forward
        return current;
    }
}

class FileSystem implements Iterable<FileNode> {     // Aggregate: exposes iterator
    private final FileNode root;
    FileSystem(FileNode root) { this.root = root; }
    public Iterator<FileNode> iterator() {
        return new DepthFirstIterator(root);
    }
}

class FileDemo {
    public static void main(String[] args) {
        FileNode root = FileNode.dir("root",
            FileNode.file("a.txt"),
            FileNode.dir("sub", FileNode.file("b.txt"), FileNode.file("c.txt")));
        for (FileNode f : new FileSystem(root)) {     // Uniform for-each traversal
            System.out.println(f.name);
        }
    }
}
```

**Why this domain works:**
- Callers never see the stack, recursion, or child lists — just `hasNext/next`.
- Depth-first can be swapped for breadth-first without touching client loops.
- Same interface supports lazy traversal of huge trees or paged API results.

---

### Iterator vs Visitor

| Aspect | Iterator | Visitor |
|---|---|---|
| Purpose | Walk elements one by one without exposing storage | Perform an operation on every element of a structure |
| Client control | Client drives the loop and decides what to do per element | Visitor object carries the operation; elements call back into it |
| Structure knowledge | Knows traversal order, hides collection internals | Knows element types, often traverses via accept() dispatch |
| Typical use | Collections, cursors, paginated APIs, tree traversal | AST analysis, export/serialization, tax over cart items |
| Extensibility | New traversals are new iterator classes | New operations are new visitor classes |

**Rule of thumb:** use Iterator when clients need sequential access with their own logic per
element; use Visitor when the operation itself should travel across a heterogeneous structure.

---

### Interview Questions and Answers

**Q1: How do you make an iterator fail-fast on concurrent modification?**
**A:** Snapshot a `modCount` from the collection when the iterator is created and compare it on
every `next()`; throw `ConcurrentModificationException` on mismatch. Document whether your
iterator is fail-fast, weakly consistent, or snapshot-based so callers know the guarantee.

**Q2: Why prefer an Iterator over exposing the internal list directly?**
**A:** Exposing the list leaks representation (ArrayList today, tree tomorrow), lets callers
mutate internals, and spreads traversal logic everywhere. An iterator hides storage, supports
multiple simultaneous traversals, and lets you change order or laziness without breaking clients.

**Q3: How do you support multiple traversal orders over the same collection?**
**A:** Keep one aggregate with factory methods like `depthFirst()`, `breadthFirst()`, or
`reverse()` each returning a different `Iterator`. Clients pick the order; the collection stays
unchanged and each iterator holds its own cursor state.

**Q4: When should you avoid writing a custom iterator?**
**A:** Avoid it when the standard `Iterable/Iterator`, streams, or generators already cover the
case. Custom iterators pay off for lazy, paged, or tree traversals — for plain in-memory lists
they add ceremony over `list.iterator()` or a for-each loop.

**Key takeaway:** Iterator decouples what is stored from how it is walked — clients loop
uniformly while each iterator owns its traversal strategy.
