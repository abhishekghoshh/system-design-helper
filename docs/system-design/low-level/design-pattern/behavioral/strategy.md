# Strategy Design Pattern

## Blogs and websites

## Medium

## Youtube

- [2. Strategy Design Pattern explanation (Hindi) | LLD System Design | Design pattern in Java](https://www.youtube.com/watch?v=u8DttUrXtEw)

## Theory

### Strategy Pattern

**Theory:** Defines a family of algorithms, encapsulates each one, and makes them interchangeable. Strategy lets the algorithm vary independently from clients that use it.

**Why it's used:**
- To define multiple algorithms for a task
- To make algorithms interchangeable at runtime
- To eliminate conditional statements for algorithm selection
- To hide complex, algorithm-specific data structures

**Diagram:**
```
Context → Strategy Interface
              ↓
    ┌─────────┼─────────┐
StrategyA  StrategyB  StrategyC
(algo1)    (algo2)    (algo3)
```

**Real-Life Examples:**
- **Payment Methods:** Credit Card, PayPal, Crypto payment strategies
- **Sorting Algorithms:** QuickSort, MergeSort, BubbleSort selected at runtime
- **Compression:** ZIP, RAR, 7z compression strategies
- **Route Planning:** Fastest, Shortest, Scenic route algorithms (Google Maps)
- **Pricing Strategies:** Regular, Holiday, Clearance pricing
- **Authentication:** OAuth, JWT, API Key authentication strategies
- **Validation:** Different validation strategies for different user types

**Advantages:**
- Family of algorithms can be swapped at runtime
- Eliminates conditional statements
- Follows Open/Closed Principle
- Algorithm variations isolated in separate classes
- Easy to test algorithms independently

**Disadvantages:**
- Increases number of objects
- Clients must understand different strategies
- Communication overhead between strategy and context
- May be overkill if algorithms rarely change

**When to Use:**
- Multiple related classes differ only in behavior
- You need different variants of an algorithm
- Algorithm uses data clients shouldn't know about
- Class has massive conditional statements for algorithm selection

---

### Pitfalls and Best Practices

**Pitfall:** Clients must know all strategies; overhead for simple algorithms
**Best Practice:** Use factory to select strategy; provide default strategy

---

### Testing Strategy Pattern

- Test each strategy algorithm independently
- Test strategy switching at runtime
- Mock context for strategy testing
- Verify all strategies satisfy interface contract
