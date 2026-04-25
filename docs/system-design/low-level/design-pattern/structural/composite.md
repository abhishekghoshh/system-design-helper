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

```
        Component
           ↓
    ┌──────┴──────┐
   Leaf        Composite
                   ↓
              [Component, Component, ...]
```

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
