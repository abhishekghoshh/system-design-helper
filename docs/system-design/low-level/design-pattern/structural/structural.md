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

### Different Structural Patterns

#### 1. Adapter Pattern

**Theory:** Converts the interface of a class into another interface that clients expect. Acts as a bridge between two incompatible interfaces.

**Why it's used:**
- When you want to use an existing class but its interface doesn't match what you need
- To create reusable classes that cooperate with unrelated or unforeseen classes
- When working with legacy code that cannot be modified
- To integrate third-party libraries with incompatible interfaces

**Diagram:**
```
    Client
       ↓
   [Target Interface]
       ↓
    Adapter  ──────→  [Adaptee]
   (converts)        (existing class)
```

**Real-Life Examples:**
- **Payment Gateways:** Adapting different payment providers (Stripe, PayPal, Razorpay) to a unified payment interface
- **Database Drivers:** JDBC adapters converting different database APIs (MySQL, PostgreSQL, Oracle) to a common interface
- **Logging Libraries:** SLF4J adapting various logging frameworks (Log4j, Logback, java.util.logging)
- **Cloud Storage:** Adapting AWS S3, Google Cloud Storage, Azure Blob Storage to a common file storage interface
- **Legacy System Integration:** Wrapping SOAP services to work with modern REST APIs

**Advantages:**
- Promotes code reusability without modifying existing code
- Follows Open/Closed Principle (open for extension, closed for modification)
- Increases flexibility when integrating third-party libraries
- Enables single client code to work with multiple incompatible interfaces

**Disadvantages:**
- Increases overall complexity by adding additional classes
- Can impact performance due to extra layer of indirection
- May be difficult to adapt if target interface is significantly different

**When to Use:**
- You need to use a third-party class but its interface doesn't match your requirements
- You want to create a reusable class that works with classes having incompatible interfaces
- You need to integrate legacy systems with modern architectures

---

#### 2. Bridge Pattern

**Theory:** Decouples an abstraction from its implementation so that the two can vary independently. It separates the interface from the implementation by placing them in separate class hierarchies.

**Why it's used:**
- When you want to avoid permanent binding between abstraction and implementation
- When both abstraction and implementation should be extensible through subclassing
- When changes in implementation should not affect clients
- When you want to share implementation among multiple objects

**Diagram:**
```
    Abstraction ──────→ Implementation
        ↓                      ↓
 RefinedAbstraction    ConcreteImplementation
```

**Real-Life Examples:**
- **UI Frameworks:** Separating UI components (Button, Checkbox) from rendering engines (Windows, macOS, Linux)
- **Database Abstraction:** ORM frameworks separating query abstraction from database implementations (Hibernate with MySQL/PostgreSQL)
- **Notification Systems:** Message abstraction separate from delivery channels (Email, SMS, Push, Slack)
- **Device Drivers:** OS abstractions separated from hardware-specific implementations
- **Remoting Frameworks:** Remote objects abstraction independent of communication protocols (HTTP, TCP, gRPC)

**Advantages:**
- Decouples interface from implementation, both can vary independently
- Improves extensibility (can extend abstraction and implementation hierarchies independently)
- Hides implementation details from clients
- Reduces compile-time dependencies

**Disadvantages:**
- Increases complexity with additional abstraction layers
- Can make code harder to understand initially
- May be overkill for simple scenarios

**When to Use:**
- You want to avoid permanent binding between abstraction and implementation
- Both abstractions and implementations need to be extended independently
- Changes in implementation should have no impact on clients
- You want to share implementations across multiple objects

---

#### 3. Composite Pattern

**Theory:** Composes objects into tree structures to represent part-whole hierarchies. It lets clients treat individual objects and compositions uniformly.

**Why it's used:**
- When you want to represent part-whole hierarchies of objects
- When you want clients to ignore the difference between individual objects and compositions
- To build tree-like structures (file systems, UI components, organization charts)
- When you need recursive composition

**Diagram:**
```
        Component
           ↓
    ┌──────┴──────┐
   Leaf        Composite
                   ↓
              [Component, Component, ...]
```

**Real-Life Examples:**
- **File Systems:** Directories containing files and subdirectories (Windows Explorer, macOS Finder)
- **UI Component Trees:** React/Angular component hierarchies (containers with nested components)
- **Organization Charts:** Company hierarchy with departments and employees
- **Graphics Editors:** Grouped shapes in tools like Figma, Adobe Illustrator (group of shapes treated as single shape)
- **Menu Systems:** Nested menus with submenus and menu items (dropdown menus)
- **DOM Structure:** HTML elements containing other elements in web browsers

**Advantages:**
- Simplifies client code by treating individual and composite objects uniformly
- Makes it easy to add new component types
- Provides flexibility in structure composition
- Recursive composition becomes natural and elegant

**Disadvantages:**
- Can make design overly general
- Harder to restrict what components can be added to composites
- Type safety can be compromised if components are too generic

**When to Use:**
- You need to represent part-whole hierarchies of objects
- You want clients to treat individual objects and compositions uniformly
- The structure can have any level of complexity and is recursive in nature

---

#### 4. Decorator Pattern

**Theory:** Attaches additional responsibilities to an object dynamically. Provides a flexible alternative to subclassing for extending functionality.

**Why it's used:**
- To add responsibilities to individual objects dynamically without affecting other objects
- When extension by subclassing is impractical or would create too many subclasses
- When you need to add/remove responsibilities at runtime
- To implement the Single Responsibility Principle by dividing functionality

**Diagram:**
```
    Component
        ↓
    ┌───┴───┐
Concrete  Decorator ──→ wraps Component
Component     ↓
      ConcreteDecorator
```

**Real-Life Examples:**
- **Java I/O Streams:** BufferedInputStream wrapping FileInputStream, adding buffering functionality
- **Middleware in Web Frameworks:** Express.js/Django middleware adding authentication, logging, compression to requests
- **Spring Framework:** @Transactional, @Cacheable annotations decorating methods with additional behavior
- **HTTP Clients:** Adding retry logic, authentication, logging to base HTTP client (OkHttp interceptors)
- **UI Components:** Adding scroll bars, borders, shadows to base components
- **Pizza/Coffee Shop:** Adding toppings/extras to base item with dynamic pricing

**Advantages:**
- More flexible than static inheritance
- Responsibilities can be added/removed at runtime
- Follows Single Responsibility Principle (each decorator handles one concern)
- Avoids feature-laden classes high in the hierarchy
- Enables mixing and matching of behaviors

**Disadvantages:**
- Many small objects can be created, making debugging harder
- Decorators and their components are not identical (instanceof checks fail)
- Can result in complex initialization code
- Order of decorators can matter, leading to potential bugs

**When to Use:**
- You need to add responsibilities to objects dynamically
- Extension by subclassing would result in an explosion of subclasses
- You want to add responsibilities that can be withdrawn
- You need different combinations of behaviors

---

#### 5. Facade Pattern

**Theory:** Provides a unified, simplified interface to a set of interfaces in a subsystem. Makes the subsystem easier to use by providing a higher-level interface.

**Why it's used:**
- To provide a simple interface to a complex subsystem
- To reduce dependencies between clients and subsystem classes
- To layer your subsystems and define entry points to each level
- To make libraries easier to use and understand

**Diagram:**
```
      Client
        ↓
      Facade
        ↓
    ┌───┼───┐
   [A] [B] [C]
 (Complex Subsystem)
```

**Real-Life Examples:**
- **E-commerce Checkout:** OrderService facade hiding payment, inventory, shipping, notification subsystems
- **Spring Boot Starter:** Simplified configuration hiding complex auto-configuration logic
- **AWS SDK:** High-level clients (S3Client) hiding low-level API complexity
- **Video Encoding:** FFmpeg wrappers providing simple API over complex encoding operations
- **Home Automation:** Smart home hub providing unified control over lights, thermostat, security, entertainment
- **Compiler Front-end:** Simple compile() method hiding lexical analysis, parsing, semantic analysis

**Advantages:**
- Shields clients from complex subsystem components
- Promotes weak coupling between subsystems and clients
- Easier to use, understand, and test
- Provides a simple default view that's sufficient for most clients
- Doesn't prevent advanced users from accessing subsystem classes directly

**Disadvantages:**
- Can become a god object coupled to all subsystem classes
- May provide limited functionality if trying to stay simple
- Additional layer may impact performance slightly

**When to Use:**
- You want to provide a simple interface to a complex subsystem
- There are many dependencies between clients and implementation classes
- You want to layer your subsystems
- You need to decouple subsystem from clients and other subsystems

---

#### 6. Flyweight Pattern

**Theory:** Uses sharing to support large numbers of fine-grained objects efficiently. Minimizes memory usage by sharing common data between multiple objects.

**Why it's used:**
- When an application uses a large number of similar objects
- When storage costs are high because of the quantity of objects
- When most object state can be made extrinsic (separated from the object)
- When object identity is not important

**Diagram:**
```
FlyweightFactory
      ↓
   [Pool of Flyweights]
      ↓
   Flyweight (intrinsic state)
      +
   Context (extrinsic state)
```

**Key Concept:** Intrinsic state (shared) vs Extrinsic state (unique to each instance)

**Real-Life Examples:**
- **Text Editors:** Character objects sharing font, color, style data (intrinsic) with position being extrinsic
- **Game Development:** Particle systems sharing texture, color data for thousands of bullets/particles
- **String Pooling:** Java String interning, Python string interning for memory optimization
- **Database Connection Pools:** Reusing connection objects instead of creating new ones
- **UI Icon Caching:** Sharing icon image data across multiple UI elements
- **Map Rendering:** Google Maps sharing tile images for same locations across multiple views

**Advantages:**
- Significantly reduces memory usage when many similar objects are needed
- Improves performance by reducing object creation overhead
- Centralizes state management for shared objects
- Scalable for large numbers of objects

**Disadvantages:**
- Increases complexity by separating intrinsic and extrinsic state
- Runtime costs for computing/maintaining extrinsic state
- Can make code harder to understand and maintain
- Thread-safety concerns when sharing objects

**When to Use:**
- Application uses large numbers of similar objects
- Storage costs are high due to quantity of objects
- Most object state can be made extrinsic
- Application doesn't depend on object identity
- Memory optimization is a critical requirement

---

#### 7. Proxy Pattern

**Theory:** Provides a surrogate or placeholder for another object to control access to it. Acts as an interface to something else.

**Why it's used:**
- **Virtual Proxy:** To delay expensive object creation until actually needed (lazy initialization)
- **Protection Proxy:** To control access rights to the original object
- **Remote Proxy:** To represent an object in a different address space
- **Smart Proxy:** To perform additional actions when accessing an object (reference counting, caching, etc.)

**Diagram:**
```
      Client
        ↓
   [Subject Interface]
        ↓
    ┌───┴───┐
  Proxy   RealSubject
    ↓
 controls access to
 RealSubject
```

**Real-Life Examples:**
- **Virtual Proxy:** Lazy loading of high-resolution images (thumbnails load first, full image on demand)
- **Protection Proxy:** Role-based access control in enterprise applications (Spring Security)
- **Remote Proxy:** RPC frameworks (gRPC), REST clients representing remote services
- **Cache Proxy:** CDN proxies caching content closer to users (Cloudflare, Akamai)
- **Smart Proxy:** Hibernate lazy loading of database entities
- **Logging Proxy:** AOP proxies in Spring adding logging/monitoring to service calls
- **Nginx/HAProxy:** Reverse proxy controlling access to backend servers

**Advantages:**
- Controls access to the real object (security, lazy initialization)
- Adds functionality without changing the real object
- Provides location transparency for remote objects
- Optimizes resource usage through lazy initialization
- Can add caching, logging, access control transparently

**Disadvantages:**
- Adds extra layer of indirection (slight performance overhead)
- Increases complexity of the codebase
- Response time may increase in some cases
- Can make code harder to debug

**When to Use:**
- You need lazy initialization (virtual proxy)
- You need access control (protection proxy)
- You need local representation of remote object (remote proxy)
- You need additional functionality before/after accessing an object (smart proxy)
- You need caching of expensive operations

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

### Common Pitfalls and Best Practices

#### Adapter Pattern
**Pitfall:** Over-adapting - creating adapters when you could modify the source
**Best Practice:** Only use adapters for code you don't control (third-party libraries, legacy code)

#### Bridge Pattern
**Pitfall:** Premature abstraction when implementation is unlikely to change
**Best Practice:** Use only when you anticipate multiple implementations or platforms

#### Composite Pattern
**Pitfall:** Treating leaf and composite differently in client code defeats the purpose
**Best Practice:** Ensure uniform treatment; use common interface for operations

#### Decorator Pattern
**Pitfall:** Too many small decorator classes, making initialization complex
**Best Practice:** Limit number of decorators; consider builder pattern for complex configurations

#### Facade Pattern
**Pitfall:** Creating a god object that does too much
**Best Practice:** Keep facade focused; multiple facades for different client needs is acceptable

#### Flyweight Pattern
**Pitfall:** Using flyweight when object count isn't a problem
**Best Practice:** Only apply when profiling shows memory/performance issues with large object counts

#### Proxy Pattern
**Pitfall:** Forgetting to implement all methods of the real object's interface
**Best Practice:** Use composition and delegation systematically; consider dynamic proxies (Java)

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

### Testing Structural Patterns

**Adapter Testing:**
- Test that adapted interface works correctly
- Verify edge cases and error handling
- Mock the adaptee for isolated testing

**Bridge Testing:**
- Test abstraction and implementation independently
- Verify all combinations work
- Use dependency injection for testing different implementations

**Composite Testing:**
- Test leaf and composite nodes separately
- Verify recursive operations work correctly
- Test edge cases (empty composites, single children)

**Decorator Testing:**
- Test each decorator in isolation
- Test decorator combinations
- Verify base component still works without decorators

**Facade Testing:**
- Mock subsystem components
- Test facade methods independently
- Verify error propagation from subsystems

**Flyweight Testing:**
- Verify object sharing works correctly
- Test thread-safety for shared objects
- Validate intrinsic vs extrinsic state separation

**Proxy Testing:**
- Test proxy and real object separately
- Verify proxy forwards all operations correctly
- Test proxy-specific behavior (caching, lazy loading, access control)
