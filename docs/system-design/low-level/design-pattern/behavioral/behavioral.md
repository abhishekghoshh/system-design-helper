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

### Different Behavioral Patterns

#### 1. Chain of Responsibility Pattern

**Theory:** Passes a request along a chain of handlers. Each handler decides either to process the request or to pass it to the next handler in the chain.

**Why it's used:**
- To decouple sender and receiver of a request
- When more than one object can handle a request, and the handler isn't known beforehand
- When you want to issue a request to one of several objects without specifying the receiver explicitly
- When the set of handlers should be specified dynamically

**Diagram:**
```
Client → Handler1 → Handler2 → Handler3 → null
         (process     (process    (process
          or pass)     or pass)    or pass)
```

**Real-Life Examples:**
- **Logging Frameworks:** Log4j, SLF4J filtering log messages through multiple handlers (Console, File, Database)
- **Servlet Filters:** Java Servlet filter chains processing HTTP requests/responses
- **Middleware Chains:** Express.js, ASP.NET Core middleware pipeline
- **Exception Handling:** Try-catch blocks in multiple layers (Controller → Service → DAO)
- **Support Ticket Systems:** L1 → L2 → L3 support escalation
- **Approval Workflows:** Manager → Director → VP → CEO approval chain

**Advantages:**
- Reduces coupling between sender and receiver
- Adds flexibility in assigning responsibilities
- Allows dynamic addition/removal of handlers
- Follows Single Responsibility Principle (each handler has one job)

**Disadvantages:**
- Request might go unhandled if chain not configured properly
- Can be hard to debug (which handler processed the request?)
- Performance overhead from traversing the chain
- No guarantee a request will be handled

**When to Use:**
- More than one object can handle a request
- Handler isn't known at compile time
- You want to decouple request sender from receivers
- Set of handlers should be dynamic

---

#### 2. Command Pattern

**Theory:** Encapsulates a request as an object, allowing you to parameterize clients with different requests, queue or log requests, and support undoable operations.

**Why it's used:**
- To parameterize objects with operations
- To queue operations, schedule their execution, or execute them remotely
- To support undo/redo functionality
- To structure a system around high-level operations built on primitive operations
- To decouple objects that invoke operations from objects that perform them

**Diagram:**
```
Client → Command Interface
              ↓
         ConcreteCommand → Receiver
              ↓              (execute action)
          Invoker
        (stores & executes)
```

**Real-Life Examples:**
- **GUI Buttons/Menus:** Button click triggers command object (Copy, Paste, Save commands)
- **Transaction Systems:** Database transactions as command objects with commit/rollback
- **Job Queues:** Background job processing (Celery, RabbitMQ task queues)
- **Undo/Redo:** Text editors, graphic design tools (Photoshop, Figma)
- **Remote Control:** TV remote buttons as commands
- **Macro Recording:** Recording sequence of commands to replay later
- **API Gateway:** Request encapsulation and routing in microservices

**Advantages:**
- Decouples invoker from receiver
- Easy to add new commands (Open/Closed Principle)
- Supports undo/redo operations
- Can assemble complex commands from simpler ones
- Supports logging and auditing of operations

**Disadvantages:**
- Increases number of classes (one per command)
- Can become complex with many command types
- Memory overhead for storing command history

**When to Use:**
- You need to parameterize objects with actions
- You need to queue, log, or support undo of operations
- You need to support transactions
- You want to decouple sender and receiver of requests

---

#### 3. Iterator Pattern

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

#### 4. Mediator Pattern

**Theory:** Defines an object that encapsulates how a set of objects interact. Promotes loose coupling by keeping objects from referring to each other explicitly.

**Why it's used:**
- To reduce chaotic dependencies between objects
- When object relationships are complex and hard to understand
- When reusing an object is difficult due to tight coupling with many others
- To centralize complex communications and control logic

**Diagram:**
```
   Component1 ←→ Mediator ←→ Component2
                     ↕
                Component3
   (all communicate through mediator)
```

**Real-Life Examples:**
- **Chat Rooms:** Users send messages through chat room (mediator), not directly to each other
- **Air Traffic Control:** Airplanes communicate through ATC, not with each other
- **UI Dialog Boxes:** Form components interact through dialog controller
- **Event Bus:** Event-driven systems (EventBus in Android, MediatR in .NET)
- **Message Brokers:** Kafka, RabbitMQ mediating between producers and consumers
- **Orchestration Services:** Microservices orchestration (Saga pattern coordinator)
- **Game Controllers:** Game objects interact through game controller

**Advantages:**
- Reduces coupling between components
- Centralizes control logic
- Makes component relationships clearer
- Easier to understand and maintain complex interactions
- Components become more reusable

**Disadvantages:**
- Mediator can become a god object
- Can become complex if handling too many interactions
- May introduce single point of failure

**When to Use:**
- Many objects communicate in complex, well-defined ways
- Reusing objects is difficult due to dependencies
- Behavior distributed between classes should be customizable
- You want to centralize complex communications

---

#### 5. Memento Pattern

**Theory:** Captures and externalizes an object's internal state without violating encapsulation, allowing the object to be restored to this state later.

**Why it's used:**
- To implement undo/redo functionality
- To save and restore object state
- To provide snapshots of object state
- To maintain encapsulation while saving state

**Diagram:**
```
Originator → Memento (state snapshot)
    ↓           ↓
Caretaker (stores mementos)
```

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

#### 6. Observer Pattern

**Theory:** Defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

**Why it's used:**
- To maintain consistency between related objects
- When changes to one object require changing others
- When an object should notify others without knowing who they are
- To implement event handling systems

**Diagram:**
```
    Subject (Observable)
         ↓
    [Observer1, Observer2, Observer3]
         ↓
    update() when subject changes
```

**Real-Life Examples:**
- **Event Listeners:** DOM events (click, scroll) in JavaScript
- **Reactive Programming:** RxJS, React hooks, Vue reactivity
- **MVC Architecture:** Model notifies views of data changes
- **Pub/Sub Systems:** Message queues (Redis Pub/Sub, AWS SNS)
- **Social Media:** Followers notified when you post
- **Stock Market Apps:** Price change notifications to multiple dashboards
- **Newsletter Subscriptions:** Subscribers notified of new content

**Advantages:**
- Establishes loose coupling between subject and observers
- Supports broadcast communication
- Can add/remove observers dynamically
- Follows Open/Closed Principle

**Disadvantages:**
- Observers notified in random order
- Can cause memory leaks if observers not properly unsubscribed
- Can trigger unwanted cascading updates
- Hard to debug when many observers exist

**When to Use:**
- Changes to one object require changing others
- An object should notify others without knowing who they are
- You need broadcast-style communication
- You're implementing event-driven systems

---

#### 7. State Pattern

**Theory:** Allows an object to alter its behavior when its internal state changes. The object will appear to change its class.

**Why it's used:**
- When object behavior depends on its state
- When operations have large, multipart conditional statements based on state
- To eliminate complex conditional logic
- When state transitions are explicit and well-defined

**Diagram:**
```
Context → State Interface
              ↓
    ┌─────────┼─────────┐
StateA     StateB    StateC
(behavior) (behavior) (behavior)
```

**Real-Life Examples:**
- **Order Processing:** Order states (Pending → Processing → Shipped → Delivered)
- **Connection States:** TCP connection (Closed → Listen → Established → Closing)
- **Document Workflow:** Draft → Review → Approved → Published
- **Vending Machine:** Idle → HasMoney → Dispensing states
- **Media Players:** Playing, Paused, Stopped states
- **Authentication:** Logged Out, Logged In, Session Expired
- **Elevator Control:** Moving Up, Moving Down, Idle, Maintenance

**Advantages:**
- Eliminates complex conditional statements
- Makes state transitions explicit
- Each state encapsulated in separate class
- Follows Single Responsibility and Open/Closed Principles
- Easy to add new states

**Disadvantages:**
- Increases number of classes
- Can be overkill for simple state machines
- State transitions logic might become scattered

**When to Use:**
- Object behavior depends on its state
- Operations have large conditional statements based on state
- State transitions are complex and explicit
- You want to avoid duplicate code in different states

---

#### 8. Strategy Pattern

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

#### 9. Template Method Pattern

**Theory:** Defines the skeleton of an algorithm in a method, deferring some steps to subclasses. Lets subclasses redefine certain steps without changing the algorithm's structure.

**Why it's used:**
- To implement the invariant parts of an algorithm once
- To let subclasses implement varying behavior
- To control subclass extensions (hook methods)
- To avoid code duplication by extracting common code

**Diagram:**
```
AbstractClass
  ↓
templateMethod() {
  step1()
  step2() [abstract]
  step3()
}
  ↓
ConcreteClass (implements step2)
```

**Real-Life Examples:**
- **Testing Frameworks:** JUnit setUp(), test(), tearDown() template
- **Web Frameworks:** Django class-based views, Spring Template classes
- **Data Processing:** ETL pipelines (Extract → Transform → Load with varying Transform)
- **Build Systems:** Maven lifecycle phases (compile → test → package)
- **Game Loops:** Initialize → Update → Render template
- **HTTP Clients:** RestTemplate in Spring (connect → send → receive → close)
- **Cooking Recipes:** Prepare ingredients → Cook → Serve (cooking varies)

**Advantages:**
- Reuses common code in base class
- Controls what subclasses can override
- Follows Don't Repeat Yourself (DRY) principle
- Enforces algorithm structure
- Easy to understand workflow

**Disadvantages:**
- Inheritance-based (less flexible than composition)
- Can violate Liskov Substitution Principle
- More classes to maintain
- Changes to template affect all subclasses

**When to Use:**
- Multiple classes have common algorithm structure
- Common behavior should be in one place
- You want to control extension points
- You need to avoid code duplication in similar algorithms

---

#### 10. Visitor Pattern

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

#### 11. Interpreter Pattern

**Theory:** Defines a grammatical representation for a language and an interpreter to interpret sentences in the language.

**Why it's used:**
- To implement domain-specific languages (DSL)
- When grammar is simple and efficiency is not critical
- To interpret and evaluate expressions
- For scripting and configuration languages

**Diagram:**
```
AbstractExpression
  ↓
┌─────────┼─────────┐
Terminal  NonTerminal
Expression Expression
```

**Real-Life Examples:**
- **SQL Parsers:** SQL query interpretation
- **Regular Expressions:** Regex pattern matching
- **Configuration Files:** Spring SpEL, JSP Expression Language
- **Mathematical Expressions:** Calculator apps parsing "2 + 3 * 4"
- **Rule Engines:** Business rule evaluation
- **Query Languages:** GraphQL, MongoDB query language
- **Scripting Languages:** Embedded scripting (Lua, JavaScript engines)

**Advantages:**
- Easy to change and extend grammar
- Grammar is explicit in code structure
- Easy to implement simple grammars
- Adding new expressions is straightforward

**Disadvantages:**
- Complex grammars become hard to maintain
- Performance issues (use parser generators for complex grammars)
- Can result in large number of classes
- Not suitable for complex languages

**When to Use:**
- Grammar is simple and well-defined
- Efficiency is not a critical concern
- You need to interpret domain-specific languages
- You're building expression evaluators or rule engines

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

---

### Common Pitfalls and Best Practices

#### Chain of Responsibility
**Pitfall:** No guarantee request will be handled; chain too long
**Best Practice:** Have default handler at end; keep chain short; log which handler processes

#### Command
**Pitfall:** Too many command classes; complex command hierarchies
**Best Practice:** Use lambda expressions where possible; compose simple commands for complex ones

#### Iterator
**Pitfall:** Modifying collection during iteration (ConcurrentModificationException)
**Best Practice:** Use fail-fast iterators; consider copy-on-write for concurrent access

#### Mediator
**Pitfall:** Mediator becomes god object doing too much
**Best Practice:** Keep mediator focused; use multiple mediators for different concerns

#### Memento
**Pitfall:** Memory bloat from storing too many states
**Best Practice:** Limit history size; implement incremental snapshots; compress old states

#### Observer
**Pitfall:** Memory leaks from not unsubscribing; notification storms
**Best Practice:** Use weak references; implement unsubscribe; batch notifications

#### State
**Pitfall:** Too many states; unclear transition logic
**Best Practice:** Document state machine; consider state machine libraries; validate transitions

#### Strategy
**Pitfall:** Clients must know all strategies; overhead for simple algorithms
**Best Practice:** Use factory to select strategy; provide default strategy

#### Template Method
**Pitfall:** Too many hook methods; rigid inheritance hierarchy
**Best Practice:** Limit hooks to essential variations; consider Strategy for more flexibility

#### Visitor
**Pitfall:** Hard to add new element types; breaks encapsulation
**Best Practice:** Use only for stable hierarchies; consider alternatives if structure changes often

#### Interpreter
**Pitfall:** Performance issues; maintenance nightmare for complex grammars
**Best Practice:** Use parser generators (ANTLR) for complex grammars; cache parsed results

---

### Decision Guide: Choosing the Right Behavioral Pattern

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

### Testing Behavioral Patterns

**Chain of Responsibility Testing:**
- Test each handler in isolation
- Test chain configuration and order
- Verify request passes to next handler or terminates
- Test edge cases (empty chain, no handler matches)

**Command Testing:**
- Test command execution separately from invoker
- Mock receiver for isolated command testing
- Test undo/redo functionality
- Verify command state and parameters

**Iterator Testing:**
- Test hasNext/next contract
- Verify iteration over empty/single/multiple elements
- Test concurrent modification behavior
- Validate different traversal orders

**Mediator Testing:**
- Mock components to test mediator logic
- Test each component independently
- Verify mediator coordinates interactions correctly
- Test notification and message routing

**Memento Testing:**
- Verify state saved and restored correctly
- Test multiple save/restore cycles
- Verify encapsulation (caretaker can't access state)
- Test memory limits for large states

**Observer Testing:**
- Test subscribe/unsubscribe mechanisms
- Verify all observers notified
- Test notification order if relevant
- Check for memory leaks (unsubscribe)
- Mock observers for subject testing

**State Testing:**
- Test each state independently
- Verify state transitions are correct
- Test invalid transitions rejected
- Verify state-specific behavior

**Strategy Testing:**
- Test each strategy algorithm independently
- Test strategy switching at runtime
- Mock context for strategy testing
- Verify all strategies satisfy interface contract

**Template Method Testing:**
- Test template method with different subclass implementations
- Verify invariant steps execute in correct order
- Test hook methods called at right time
- Validate abstract methods implemented correctly

**Visitor Testing:**
- Test visitor on each element type
- Test element acceptance of visitor
- Verify visitor accumulates state correctly
- Test with composite structures

**Interpreter Testing:**
- Test grammar rules individually
- Test expression parsing and evaluation
- Verify complex expressions
- Test error handling for invalid syntax

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
