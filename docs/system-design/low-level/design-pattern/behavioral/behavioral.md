# Behavioral Design Pattern

## Blogs and websites

## Medium

## Youtube

- [41. All Behavioral Design Patterns | Strategy, Observer, State, Template, Command, Visitor, Memento](https://www.youtube.com/watch?v=DBDnUkTobaE)

## Theory

### What is Behavioral Pattern?

Behavioral design patterns are concerned with algorithms, assignment of responsibilities between objects, and communication patterns between them. They focus on how objects interact and communicate with each other, defining the patterns of communication and control flow in the system. These patterns help make complex control flows more readable and maintainable.

**Why Behavioral Patterns are Used:**

- **Define clear communication** protocols between objects
- **Encapsulate behavior** and make it more flexible and reusable
- **Reduce coupling** between interacting objects
- **Make algorithms interchangeable** without affecting clients
- **Capture complex control flows** in readable patterns
- **Enable runtime behavior changes** without modifying object structure

**Key Principle:** Behavioral patterns use object composition and delegation to distribute responsibilities and define how objects collaborate to accomplish complex tasks.

---

### Summary Comparison

| Pattern | Main Purpose | Key Use Case |
|---------|-------------|--------------|
| **Chain of Responsibility** | Pass request along chain | Logging, middleware, approval workflows |
| **Command** | Encapsulate requests | Undo/redo, transactions, job queues |
| **Iterator** | Sequential access | Collection traversal without exposing structure |
| **Mediator** | Centralize interactions | Chat rooms, event buses, complex UI dialogs |
| **Memento** | Save/restore state | Undo/redo, snapshots, version control |
| **Observer** | Notify dependents | Event systems, MVC, reactive programming |
| **State** | Change behavior with state | Workflow, connection states, order processing |
| **Strategy** | Interchangeable algorithms | Payment methods, sorting, routing algorithms |
| **Template Method** | Algorithm skeleton | Testing frameworks, build systems, ETL pipelines |
| **Visitor** | Operations on object structure | Compilers, reporting, serialization |
| **Interpreter** | Interpret language | DSL, regex, expression evaluators |

---

### Design Principles in Behavioral Patterns

Behavioral patterns embody several key design principles:

**1. Encapsulate What Varies**
- Strategy, State encapsulate varying algorithms/behaviors
- Template Method encapsulates invariant algorithm structure

**2. Program to an Interface**
- All behavioral patterns define abstract protocols
- Concrete implementations hidden behind interfaces

**3. Favor Composition Over Inheritance**
- Strategy, Command use composition instead of inheritance
- More flexible than Template Method's inheritance approach

**4. Loose Coupling**
- Mediator, Observer reduce coupling between objects
- Chain of Responsibility decouples senders from receivers

**5. Single Responsibility Principle**
- Each pattern focuses on one behavioral concern
- Command: encapsulation; Observer: notification; State: state-dependent behavior

**6. Open/Closed Principle**
- Strategy, Command easy to extend with new implementations
- Visitor allows new operations without modifying elements

**7. Hollywood Principle ("Don't call us, we'll call you")**
- Template Method, Observer follow this principle
- Framework calls application code, not vice versa

---

### Pattern Relationships and Combinations

**Patterns Often Used Together:**

1. **Command + Memento**
   - Store command history for undo/redo
   - Memento saves state before command execution

2. **Observer + Mediator**
   - Mediator can use Observer to notify components
   - Example: MVC where mediator uses observer pattern

3. **State + Strategy**
   - Similar structure but different intent
   - State: behavior changes with internal state
   - Strategy: client chooses algorithm

4. **Iterator + Composite**
   - Iterate over composite structures
   - Example: Traversing file system trees

5. **Chain of Responsibility + Command**
   - Commands passed along chain
   - Example: Middleware processing command requests

6. **Visitor + Composite**
   - Visitor operates on composite structures
   - Example: Operations on tree-structured data

7. **Template Method + Strategy**
   - Template Method uses Strategy for varying steps
   - Combines inheritance and composition

**Key Differences:**

- **State vs Strategy:** State changes automatically; Strategy set by client
- **Command vs Strategy:** Command encapsulates request; Strategy encapsulates algorithm
- **Chain of Responsibility vs Decorator:** Chain can break; Decorator always delegates
- **Mediator vs Observer:** Mediator centralizes; Observer distributes communication
- **Memento vs Command:** Memento saves state; Command saves operations

---\n\n### Decision Guide: Choosing the Right Behavioral Pattern

**Start with these questions:**

1. **Need to pass request through a series of handlers?**
   → Use **Chain of Responsibility**

2. **Need to encapsulate requests as objects (undo/redo, queuing)?**
   → Use **Command**

3. **Need to traverse a collection without exposing structure?**
   → Use **Iterator**

4. **Need to coordinate communication between many objects?**
   → Use **Mediator**

5. **Need to save and restore object state?**
   → Use **Memento**

6. **Need to notify multiple objects of state changes?**
   → Use **Observer**

7. **Object behavior changes based on internal state?**
   → Use **State**

8. **Need to select algorithm at runtime?**
   → Use **Strategy**

9. **Need to define algorithm structure with varying steps?**
   → Use **Template Method**

10. **Need to add operations to stable object hierarchy?**
    → Use **Visitor**

11. **Need to interpret/evaluate a language or expressions?**
    → Use **Interpreter**

**Decision Tree:**
```
What's your primary need?

Communication between objects?
├─ One-to-many notification → OBSERVER
├─ Centralized coordination → MEDIATOR
└─ Sequential processing → CHAIN OF RESPONSIBILITY

Algorithm/Behavior variation?
├─ Runtime algorithm selection → STRATEGY
├─ State-dependent behavior → STATE
└─ Algorithm skeleton with hooks → TEMPLATE METHOD

Request handling?
├─ Encapsulate as objects → COMMAND
└─ Sequential handlers → CHAIN OF RESPONSIBILITY

Data structure operations?
├─ Traverse elements → ITERATOR
├─ Operations on stable hierarchy → VISITOR
└─ Interpret expressions → INTERPRETER

State management?
├─ Save/restore state → MEMENTO
└─ Behavior based on state → STATE
```

---

### Performance Considerations

| Pattern | Memory Impact | Runtime Cost | Scalability |
|---------|---------------|--------------|-------------|
| **Chain of Responsibility** | Low | Medium (traversal) | Medium |
| **Command** | Medium (command objects) | Low | High |
| **Iterator** | Low | Low | High |
| **Mediator** | Low | Low | High |
| **Memento** | **High** (state storage) | Medium | Medium |
| **Observer** | Medium (observer list) | Medium (notifications) | Medium-High |
| **State** | Low | Low | High |
| **Strategy** | Low | Low | High |
| **Template Method** | Low | Low | High |
| **Visitor** | Low | Low-Medium | High |
| **Interpreter** | Medium | **High** (interpretation) | Low |

**Optimization Tips:**
- **Observer:** Use weak references; batch notifications; implement priority observers
- **Memento:** Incremental snapshots; compress old states; limit history depth
- **Command:** Reuse command objects; use flyweight for similar commands
- **Chain:** Keep chain short; cache successful handler for repeated requests
- **Interpreter:** Cache parsed expressions; use compiler techniques for hot paths

---

### Behavioral Patterns in Modern Software Architecture

**Microservices Architecture:**
- **Chain of Responsibility:** API Gateway filter chains
- **Command:** CQRS (Command Query Responsibility Segregation)
- **Observer:** Event-driven microservices (Kafka, EventBridge)
- **Mediator:** Service mesh, orchestration services

**Reactive Programming:**
- **Observer:** Foundation of reactive streams (RxJS, Project Reactor)
- **Iterator:** Asynchronous iteration over streams
- **Command:** Action/event objects in state management (Redux)

**Frontend Development:**
- **Observer:** React hooks (useState, useEffect), Vue reactivity
- **Command:** Redux actions, Vuex mutations
- **State:** UI state machines (XState)
- **Strategy:** Rendering strategies, validation strategies
- **Mediator:** Event buses, state management stores

**Domain-Driven Design:**
- **Command:** CQRS commands
- **Observer:** Domain events
- **Strategy:** Domain service strategies
- **Memento:** Event sourcing snapshots

**Cloud-Native Applications:**
- **Chain of Responsibility:** Cloud function chains, Step Functions
- **Command:** Serverless functions as commands
- **Observer:** SNS/SQS pub/sub, CloudWatch Events
- **State:** Step Functions state machines

---

### Anti-Patterns to Avoid

**1. Observer Pattern Abuse**
- Creating deep notification chains causing cascading updates
- Not cleaning up observers leading to memory leaks
- Using Observer when simple callback would suffice

**2. State Pattern Overuse**
- Using State for simple if/else conditions
- Creating states for every possible condition combination
- Not documenting state transitions clearly

**3. Strategy Pattern Misuse**
- Using Strategy when behavior never changes
- Creating too many similar strategies
- Client knowing too much about strategy selection logic

**4. Command Pattern Overengineering**
- Creating command classes for trivial operations
- Complex command hierarchies when simple functions work
- Not implementing undo when it's the main reason for using Command

**5. Mediator as God Object**
- Mediator handling too many responsibilities
- Mediator knowing too much about components
- Using one mediator for entire application

**6. Chain Too Long**
- Chains with 10+ handlers causing performance issues
- No visibility into which handler processes request
- Difficult to debug and maintain

---

### Real-World Framework Examples

**Spring Framework:**
- **Template Method:** JdbcTemplate, RestTemplate
- **Observer:** ApplicationEvent, ApplicationListener
- **Strategy:** TransactionManager implementations
- **Chain of Responsibility:** Filter chains in Spring Security
- **Command:** @Transactional, AOP method interceptors

**React/Redux:**
- **Observer:** React hooks, component re-rendering
- **Command:** Redux actions
- **Mediator:** Redux store
- **State:** Component state management

**Express.js:**
- **Chain of Responsibility:** Middleware pipeline
- **Command:** Route handlers as commands
- **Observer:** Event emitters

**Android:**
- **Observer:** LiveData, Observable
- **Command:** Intent system
- **Mediator:** EventBus
- **State:** Fragment/Activity lifecycle states

**ASP.NET Core:**
- **Chain of Responsibility:** Middleware pipeline
- **Template Method:** Controller action filters
- **Mediator:** MediatR library for CQRS
- **Observer:** INotifyPropertyChanged, IObservable
