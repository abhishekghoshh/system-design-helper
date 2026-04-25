# All Structural Design Patterns

## Blogs and websites

## Medium

## Youtube

- [32. All Structural Design Patterns | Decorator, Proxy, Composite, Adapter, Bridge, Facade, FlyWeight](https://www.youtube.com/watch?v=WxGtmIBZszk)

## Theory

### What is Structural Pattern?

Structural design patterns are concerned with how classes and objects are composed to form larger structures. They focus on the composition of classes or objects to form new structures that are more flexible and efficient. These patterns help ensure that if one part of a system changes, the entire system doesn't need to change.

**Why Structural Patterns are Used:**

- **Simplify relationships** between entities by defining clear ways to compose objects
- **Increase flexibility** by ensuring changes in one part don't break the entire system
- **Promote reusability** by creating components that can be combined in different ways
- **Reduce complexity** by hiding complex structures behind simpler interfaces
- **Enable better scalability** through loosely coupled components

**Key Principle:** Structural patterns use composition and delegation to combine objects and classes into larger structures while keeping these structures flexible and efficient.

---

### Summary Comparison

| Pattern | Main Purpose | Key Use Case |
|---------|-------------|--------------|
| **Adapter** | Interface conversion | Making incompatible interfaces work together |
| **Bridge** | Decouple abstraction from implementation | Independent variation of interface and implementation |
| **Composite** | Tree structures | Treating individual and composite objects uniformly |
| **Decorator** | Add responsibilities | Runtime behavior extension without subclassing |
| **Facade** | Simplified interface | Hiding complexity of subsystems |
| **Flyweight** | Memory optimization | Sharing common state among many objects |
| **Proxy** | Controlled access | Adding a level of indirection for access control |

---

### Design Principles in Structural Patterns

Structural patterns embody several key design principles:

**1. Favor Composition Over Inheritance**
- Decorator, Composite, Bridge all use object composition
- Provides more flexibility than static inheritance hierarchies

**2. Program to an Interface, Not an Implementation**
- All structural patterns define abstract interfaces
- Concrete implementations are hidden behind interfaces

**3. Single Responsibility Principle (SRP)**
- Each pattern focuses on one structural concern
- Decorator: adding responsibilities; Facade: simplifying interface; Proxy: controlling access

**4. Open/Closed Principle**
- Adapter, Decorator allow extending functionality without modifying existing code
- Systems remain open for extension but closed for modification

**5. Dependency Inversion Principle**
- Bridge, Adapter depend on abstractions, not concrete classes
- High-level modules don't depend on low-level modules

**6. Interface Segregation Principle**
- Facade provides focused, client-specific interfaces
- Clients aren't forced to depend on interfaces they don't use

---

### Pattern Relationships and Combinations

**Patterns Often Used Together:**

1. **Composite + Decorator**
   - Decorator can wrap individual or composite objects
   - Example: Adding borders to individual UI components or groups

2. **Facade + Adapter**
   - Facade simplifies subsystem; Adapter converts interfaces
   - Example: E-commerce facade using adapters for different payment gateways

3. **Proxy + Decorator**
   - Both wrap objects, but different intent
   - Proxy controls access; Decorator adds behavior
   - Can be combined: Proxy for lazy loading + Decorator for caching

4. **Bridge + Abstract Factory**
   - Abstract Factory can create platform-specific implementations
   - Bridge separates abstraction from platform-specific code

5. **Flyweight + Composite**
   - Shared leaf nodes in composite structure
   - Example: Character objects (flyweight) in document tree (composite)

**Key Differences:**

- **Adapter vs Bridge:** Adapter makes things work after they're designed; Bridge makes them work before
- **Adapter vs Facade:** Adapter wraps one object; Facade wraps entire subsystem
- **Decorator vs Proxy:** Decorator adds behavior; Proxy controls access
- **Composite vs Decorator:** Composite focuses on aggregation; Decorator on responsibilities

---

### Decision Guide: Choosing the Right Structural Pattern

**Start with these questions:**

1. **Need to make incompatible interfaces work together?**
   → Use **Adapter**

2. **Want abstraction and implementation to vary independently?**
   → Use **Bridge**

3. **Building tree structures where leaf and branch nodes are treated uniformly?**
   → Use **Composite**

4. **Need to add responsibilities to objects dynamically at runtime?**
   → Use **Decorator**

5. **Complex subsystem needs simplified interface?**
   → Use **Facade**

6. **Large number of similar objects causing memory issues?**
   → Use **Flyweight**

7. **Need to control access or add intelligence to object access?**
   → Use **Proxy**

**Decision Tree:**
```
Do you need to change an interface?
├─ Yes → ADAPTER
└─ No → Do you need to simplify complex interfaces?
    ├─ Yes → FACADE
    └─ No → Do you need to add behavior?
        ├─ Yes, dynamically → DECORATOR
        ├─ Yes, with access control → PROXY
        └─ No → Do you work with hierarchies?
            ├─ Yes, tree structures → COMPOSITE
            ├─ Yes, separate abstraction/implementation → BRIDGE
            └─ No, memory optimization needed → FLYWEIGHT
```

---

### Performance Considerations

| Pattern | Memory Impact | Runtime Cost | Scalability |
|---------|---------------|--------------|-------------|
| **Adapter** | Low (single wrapper) | Low | High |
| **Bridge** | Low | Low | High |
| **Composite** | Medium (tree overhead) | Medium (traversal cost) | Medium |
| **Decorator** | Medium (wrapper chain) | Medium (delegation chain) | Medium |
| **Facade** | Low | Low | High |
| **Flyweight** | **Reduced** (sharing) | Medium (state management) | **Very High** |
| **Proxy** | Low | Low-Medium (depends on proxy type) | High |

**Optimization Tips:**
- Flyweight: Best for memory-constrained scenarios with massive object counts
- Proxy: Virtual proxy excellent for deferring expensive operations
- Decorator: Be mindful of deep decorator chains (stack overhead)
- Composite: Cache computed results for expensive tree operations

---

### Structural Patterns in Modern Software Architecture

**Microservices Architecture:**
- **Adapter:** Integrating services with different APIs
- **Facade:** API Gateway pattern
- **Proxy:** Service mesh (Istio, Linkerd)

**Cloud-Native Applications:**
- **Proxy:** Load balancers, reverse proxies
- **Flyweight:** Caching layers (Redis, Memcached)
- **Bridge:** Multi-cloud abstractions

**Frontend Development:**
- **Composite:** Component trees (React, Vue, Angular)
- **Decorator:** Higher-Order Components (HOCs), Hooks
- **Facade:** State management libraries (Redux, Vuex)

**Domain-Driven Design:**
- **Adapter:** Anti-Corruption Layer between bounded contexts
- **Facade:** Application Services simplifying domain complexity
- **Composite:** Aggregate roots containing entities

---

### Structural Patterns in Modern Software Architecture
