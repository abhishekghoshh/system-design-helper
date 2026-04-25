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
```
Client → Iterator Interface
              ↓
        ConcreteIterator ← Aggregate
         (hasNext, next)    (collection)
```

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
