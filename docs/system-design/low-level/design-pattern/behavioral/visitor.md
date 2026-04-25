# Visitor Design Pattern

## Blogs and websites

## Medium

## Youtube

- [36. Visitor Design Pattern | Double Dispatch | Low Level Design](https://www.youtube.com/watch?v=pDsz-AuFO0g)

## Theory

### Visitor Pattern

**Theory:** Lets you define a new operation without changing the classes of the elements on which it operates. Separates algorithms from the objects they operate on.

**Why it's used:**
- To add operations to existing class hierarchy without modifying classes
- When many unrelated operations need to be performed on objects
- To keep related operations together
- When class hierarchy is stable but operations change frequently

**Diagram:**
```
Element Interface → accept(Visitor)
  ↓                      ↓
ConcreteElement → Visitor Interface
                       ↓
                  ConcreteVisitor
                  (operations)
```

**Real-Life Examples:**
- **Compiler Design:** Abstract Syntax Tree (AST) traversal for code generation, optimization
- **Tax Calculation:** Different tax visitors for different countries/regions
- **Reporting Systems:** Different export formats (PDF, Excel, HTML) for same data
- **Serialization:** XML, JSON serialization visitors
- **Code Analysis:** Static analysis tools visiting AST nodes
- **Shopping Cart:** Discount calculation, tax calculation visitors
- **File System:** File operation visitors (search, backup, antivirus scan)

**Advantages:**
- Easy to add new operations without modifying elements
- Related operations kept together in visitor
- Can accumulate state while traversing structure
- Follows Single Responsibility and Open/Closed Principles

**Disadvantages:**
- Hard to add new element types (requires changing all visitors)
- Breaks encapsulation (elements expose internal details)
- Can become complex with many visitors and elements
- Circular dependency between visitors and elements

**When to Use:**
- Object structure contains many classes with different interfaces
- Many distinct operations need to be performed on objects
- Object structure rarely changes but operations change frequently
- You want to keep related operations together

---

### Pitfalls and Best Practices

**Pitfall:** Hard to add new element types; breaks encapsulation
**Best Practice:** Use only for stable hierarchies; consider alternatives if structure changes often

---

### Testing Visitor Pattern

- Test visitor on each element type
- Test element acceptance of visitor
- Verify visitor accumulates state correctly
- Test with composite structures
