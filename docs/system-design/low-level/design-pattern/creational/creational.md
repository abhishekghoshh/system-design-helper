# All Creational Design Patterns 



## Youtube

- [27. All Creational Design Patterns | Prototype, Singleton, Factory, AbstractFactory, Builder Pattern](https://www.youtube.com/watch?v=OuNOyFg942)



## Theory

### What is Creational Pattern?

Creational design patterns are concerned with the way objects are created. They abstract the instantiation process, making systems independent of how their objects are created, composed, and represented. These patterns help make a system independent of how its objects are created, promoting flexibility in deciding which objects need to be created for a given use case.

**Why Creational Patterns are Used:**

- **Control object creation** complexity and hide creation logic
- **Increase flexibility** in deciding which objects to create
- **Reduce coupling** between object creation and usage
- **Enable object reuse** and prevent unnecessary object creation
- **Provide control** over the instantiation process
- **Make systems independent** of how objects are created and composed

**Key Principle:** Creational patterns encapsulate knowledge about which concrete classes the system uses and hide how instances of these classes are created and composed.

---

### Different Creational Patterns

#### 1. Singleton Pattern

**Theory:** Ensures a class has only one instance and provides a global point of access to it. Controls object creation to restrict the number of instances to exactly one.

**Why it's used:**
- When exactly one instance of a class is needed
- To provide controlled access to a single instance
- When the sole instance should be extensible by subclassing
- To manage shared resources (database connections, thread pools, caches)

**Diagram:**
```
Singleton
├─ private static instance
├─ private constructor()
└─ public static getInstance()
      ↓
   returns single instance
```

**Real-Life Examples:**
- **Configuration Management:** Application config loaded once (Spring ApplicationContext, Django settings)
- **Logging:** Single logger instance (Log4j, SLF4J)
- **Database Connection Pools:** HikariCP, C3P0 connection pool managers
- **Thread Pools:** Executor service instances in Java
- **Cache Managers:** Redis client, Memcached client singletons
- **File System:** File system representation in OS
- **Window Manager:** Single window manager in desktop environments
- **Driver Manager:** JDBC DriverManager

**Advantages:**
- Controlled access to sole instance
- Reduced namespace pollution
- Permits refinement through subclassing
- Variable number of instances can be controlled
- Lazy initialization saves resources

**Disadvantages:**
- Global state makes testing difficult
- Violates Single Responsibility Principle (controls creation + business logic)
- Difficult to unit test (tight coupling)
- Thread-safety issues in multithreaded environments
- Can be anti-pattern if overused
- Makes code less flexible

**When to Use:**
- Exactly one instance needed across the system
- Instance needs to be accessible from well-known access point
- Sole instance should be extensible through subclassing
- Managing shared resources (connections, caches, thread pools)

**Thread-Safe Implementation Approaches:**
- **Eager initialization:** Instance created at class loading
- **Lazy initialization with synchronized:** Double-checked locking
- **Bill Pugh Singleton:** Using inner static helper class
- **Enum Singleton:** Java enum (simplest, prevents serialization issues)

---

#### 2. Factory Method Pattern

**Theory:** Defines an interface for creating an object, but lets subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses.

**Why it's used:**
- When a class can't anticipate the type of objects it must create
- When a class wants its subclasses to specify the objects it creates
- To delegate responsibility to helper subclasses
- To provide hooks for subclasses to extend object creation

**Diagram:**
```
Creator (abstract)
├─ factoryMethod() [abstract]
└─ operation() uses factoryMethod()
      ↓
ConcreteCreator
└─ factoryMethod() returns ConcreteProduct
```

**Real-Life Examples:**
- **UI Frameworks:** Dialog/Button creation for different OS (Windows, macOS, Linux)
- **DAO Pattern:** Factory creating DAO objects for different databases
- **Document Readers:** PDF, Word, Excel readers based on file type
- **Logistics:** Truck, Ship transport creation based on delivery type
- **Payment Processing:** PaymentProcessor factory creating Stripe, PayPal processors
- **Notification Services:** Email, SMS, Push notification creators
- **Database Connections:** JDBC drivers creating DB-specific connections
- **Serialization:** Jackson creating serializers for different formats (JSON, XML, YAML)

**Advantages:**
- Avoids tight coupling between creator and concrete products
- Follows Single Responsibility Principle (creation logic separated)
- Follows Open/Closed Principle (easy to add new product types)
- Provides hooks for subclasses
- More flexible than direct object creation

**Disadvantages:**
- Can result in many subclasses
- Clients might need to create subclass just to create product
- Code can become more complicated
- May be overkill for simple object creation

**When to Use:**
- A class can't anticipate the class of objects it must create
- A class wants subclasses to specify objects to create
- Classes delegate responsibility to helper subclasses
- You want to provide library users with hooks to extend internal components

---

#### 3. Abstract Factory Pattern

**Theory:** Provides an interface for creating families of related or dependent objects without specifying their concrete classes. A factory of factories.

**Why it's used:**
- When system needs to be independent of how products are created
- When system should be configured with one of multiple families of products
- When a family of related products is designed to be used together
- To enforce constraints on which products can be used together

**Diagram:**
```
AbstractFactory
├─ createProductA()
└─ createProductB()
      ↓
ConcreteFactory1        ConcreteFactory2
├─ createProductA()     ├─ createProductA()
│  → ProductA1          │  → ProductA2
└─ createProductB()     └─ createProductB()
   → ProductB1             → ProductB2
```

**Real-Life Examples:**
- **UI Toolkits:** Creating consistent UI elements (Button, TextBox, Checkbox) for Windows/Mac/Linux
- **Database Abstraction:** SQL, NoSQL factories creating connections, query builders, transactions
- **Theme Systems:** Light/Dark theme creating colors, fonts, icons as a set
- **Cross-Platform Apps:** Android/iOS factories creating platform-specific UI components
- **Document Generators:** PDF, HTML, Word generators creating headers, paragraphs, tables
- **Cloud Providers:** AWS, Azure, GCP factories creating compute, storage, network resources
- **Game Engines:** Creating related game objects (medieval theme vs sci-fi theme)
- **E-commerce:** Different region factories (US, EU, Asia) creating currency, tax, shipping objects

**Advantages:**
- Isolates concrete classes
- Makes exchanging product families easy
- Promotes consistency among products
- Follows Open/Closed Principle (easy to add new families)
- Enforces constraints on product combinations

**Disadvantages:**
- Supporting new kinds of products is difficult (requires changing interface)
- Increased complexity and abstraction
- More interfaces and classes to manage
- Can be overkill for simple scenarios

**When to Use:**
- System should be independent of how products are created
- System should work with multiple families of products
- Related products must be used together (enforced constraint)
- You want to provide a library of products revealing only interfaces

---

#### 4. Builder Pattern

**Theory:** Separates the construction of a complex object from its representation, allowing the same construction process to create different representations. Constructs complex objects step by step.

**Why it's used:**
- To create complex objects with many optional parameters
- When constructor has too many parameters (telescoping constructor problem)
- To create different representations of an object using same construction process
- To construct objects step-by-step with method chaining
- To make object creation more readable

**Diagram:**
```
Director
└─ construct() uses Builder
      ↓
Builder Interface
├─ buildPartA()
├─ buildPartB()
└─ getResult()
      ↓
ConcreteBuilder
└─ creates Product
```

**Real-Life Examples:**
- **HTTP Clients:** OkHttp, Apache HttpClient request builders
- **StringBuilder/StringBuffer:** Building strings incrementally
- **SQL Query Builders:** Hibernate Criteria, jOOQ, QueryDSL
- **Test Data Builders:** Creating complex test objects (Builder pattern for DTOs)
- **Configuration Objects:** Building complex configurations (Spring Boot builders)
- **Document Builders:** Creating HTML, XML, JSON documents
- **Meal Builders:** Restaurant orders (burger with custom toppings)
- **UI Dialog Builders:** Android AlertDialog.Builder

**Advantages:**
- Constructs objects step-by-step
- Reuses same construction code for different representations
- Isolates complex construction code
- Better control over construction process
- Immutable objects with many parameters
- More readable than telescoping constructors
- Follows Single Responsibility Principle

**Disadvantages:**
- Increases overall complexity (more classes)
- Requires creating separate builder for each product type
- Can be verbose for simple objects
- Mutable builder for immutable product creates complexity

**When to Use:**
- Object has many constructor parameters (especially optional ones)
- Construction process must allow different representations
- Step-by-step construction needed
- You want immutable objects with many fields
- Telescoping constructors become unmanageable

**Modern Variations:**
- **Fluent Builder:** Method chaining for readable construction
- **Lombok @Builder:** Annotation-based builder generation in Java
- **Step Builder:** Type-safe builder ensuring required fields set

---

#### 5. Prototype Pattern

**Theory:** Specifies kinds of objects to create using a prototypical instance and creates new objects by copying this prototype. Clones objects instead of creating from scratch.

**Why it's used:**
- When object creation is expensive (complex initialization, database calls)
- When system should be independent of how products are created
- To avoid building class hierarchies of factories
- When instances of a class can have only a few different state combinations

**Diagram:**
```
Prototype Interface
└─ clone()
      ↓
ConcretePrototype
└─ clone() returns copy of self
      ↓
Client clones instead of creating new
```

**Real-Life Examples:**
- **Object Cloning:** Java Cloneable, JavaScript Object.assign(), spread operator
- **Game Development:** Cloning enemy/character templates with same attributes
- **Document Templates:** Cloning document templates (Google Docs templates)
- **Database Records:** Cloning records with similar data
- **UI Components:** Cloning widgets with default configurations
- **Test Fixtures:** Cloning test data objects
- **Configuration Objects:** Cloning base configurations for different environments
- **Cell Division:** Biological inspiration - cell cloning

**Advantages:**
- Adds/removes products at runtime
- Specifies new objects by varying values
- Reduces subclassing
- Configures application with classes dynamically
- Avoids expensive initialization/construction
- Can be faster than creating from scratch

**Disadvantages:**
- Complex objects with circular references hard to clone
- Deep copy vs shallow copy confusion
- Each subclass must implement clone
- Can be difficult with objects having no copy constructor
- Cloning complex objects may not save time

**When to Use:**
- Object creation is expensive
- Similar objects needed with slight variations
- System should be independent of how products are created
- Avoiding parallel class hierarchies
- Limited number of state combinations for objects

**Implementation Considerations:**
- **Shallow Copy:** Copies object fields, but referenced objects shared
- **Deep Copy:** Recursively copies all referenced objects
- **Copy Constructor:** Alternative to clone method
- **Serialization-based Cloning:** Serialize and deserialize for deep copy

---

### Summary Comparison

| Pattern | Main Purpose | Key Use Case |
|---------|-------------|--------------|
| **Singleton** | One instance | Configuration, logging, connection pools |
| **Factory Method** | Subclass decides creation | Product creation with subclass flexibility |
| **Abstract Factory** | Family of related objects | UI toolkits, cross-platform components |
| **Builder** | Complex object construction | Objects with many parameters, fluent APIs |
| **Prototype** | Clone objects | Expensive object creation, similar objects |

---

### Design Principles in Creational Patterns

Creational patterns embody several key design principles:

**1. Encapsulate What Varies**
- Factory Method, Abstract Factory encapsulate object creation
- Builder encapsulates complex construction process
- Patterns separate creation from usage

**2. Program to an Interface, Not Implementation**
- Abstract Factory, Factory Method return interface types
- Clients work with abstractions, not concrete classes

**3. Dependency Inversion Principle**
- High-level code doesn't depend on low-level object creation
- Both depend on abstractions (factory interfaces)

**4. Open/Closed Principle**
- Factory patterns allow adding new product types
- Systems open for extension, closed for modification

**5. Single Responsibility Principle**
- Creation logic separated from business logic
- Factories handle creation, other classes handle behavior

**6. Don't Repeat Yourself (DRY)**
- Builder reuses construction code
- Prototype reuses existing objects
- Factories centralize creation logic

---

### Pattern Relationships and Combinations

**Patterns Often Used Together:**

1. **Abstract Factory + Factory Method**
   - Abstract Factory often implemented using Factory Methods
   - Each create method is a Factory Method

2. **Abstract Factory + Prototype**
   - Abstract Factory can store prototypes and clone them
   - Reduces number of factory subclasses needed

3. **Builder + Composite**
   - Builder can construct complex Composite structures
   - Example: Building tree-structured documents

4. **Singleton + Factory**
   - Factory can be implemented as Singleton
   - Single factory instance managing object creation

5. **Prototype + Memento**
   - Prototype for cloning objects
   - Memento for saving state snapshots

6. **Abstract Factory + Bridge**
   - Abstract Factory can create platform-specific implementations
   - Bridge separates abstraction from platform

**Key Differences:**

- **Factory Method vs Abstract Factory:** Factory Method creates one product; Abstract Factory creates families
- **Builder vs Factory:** Builder focuses on step-by-step construction; Factory on product selection
- **Prototype vs Factory:** Prototype clones existing; Factory creates new
- **Singleton vs Factory:** Singleton ensures one instance; Factory creates multiple
- **Factory Method vs Template Method:** Both use inheritance, but Factory creates objects; Template defines algorithm

---

### Common Pitfalls and Best Practices

#### Singleton Pattern
**Pitfall:** Overuse leading to global state, testing difficulties
**Best Practice:** Use dependency injection instead; limit to truly single resources; avoid business logic in singleton

**Pitfall:** Thread-safety issues with lazy initialization
**Best Practice:** Use enum singleton (Java), lazy holder idiom, or eager initialization

**Pitfall:** Singleton preventing unit testing
**Best Practice:** Use interfaces, dependency injection; make singleton testable

#### Factory Method Pattern
**Pitfall:** Creating factory subclasses just to instantiate products
**Best Practice:** Use Simple Factory or parameterized factory if no customization needed

**Pitfall:** Too many factory methods
**Best Practice:** Consider Abstract Factory for related products

#### Abstract Factory Pattern
**Pitfall:** Difficulty adding new product types (requires interface change)
**Best Practice:** Design product families carefully upfront; consider if flexibility worth complexity

**Pitfall:** Too many factory implementations
**Best Practice:** Ensure you truly need families of related products

#### Builder Pattern
**Pitfall:** Overuse for simple objects
**Best Practice:** Only use for complex objects with many parameters

**Pitfall:** Not validating object state
**Best Practice:** Validate in build() method; ensure required fields set

**Pitfall:** Mutable builder allowing inconsistent state
**Best Practice:** Consider immutable builders; validate at build time

#### Prototype Pattern
**Pitfall:** Shallow copy when deep copy needed
**Best Practice:** Clearly document copy semantics; implement deep copy when needed

**Pitfall:** Circular references causing clone issues
**Best Practice:** Handle circular references explicitly; document cloning behavior

---

### Decision Guide: Choosing the Right Creational Pattern

**Start with these questions:**

1. **Need exactly one instance of a class?**
   → Use **Singleton** (but consider dependency injection first)

2. **Need to create objects without specifying exact class?**
   - One product type → Use **Factory Method**
   - Family of related products → Use **Abstract Factory**

3. **Object has many constructor parameters (especially optional)?**
   → Use **Builder**

4. **Creating objects is expensive and you need similar copies?**
   → Use **Prototype**

5. **Need to defer instantiation to subclasses?**
   → Use **Factory Method**

**Decision Tree:**
```
How will objects be created?

One instance only?
└─ Yes → SINGLETON

Multiple instances?
├─ Complex construction (many params)?
│  └─ Yes → BUILDER
├─ Clone existing object?
│  └─ Yes → PROTOTYPE
└─ Create based on type/family?
   ├─ Single product type → FACTORY METHOD
   └─ Family of products → ABSTRACT FACTORY
```

**Complexity vs Flexibility Trade-off:**
```
Simple → Complex
Singleton → Factory Method → Abstract Factory
             ↓
          Builder
             ↓
          Prototype
```

---

### Performance Considerations

| Pattern | Memory Impact | Creation Cost | Scalability |
|---------|---------------|---------------|-------------|
| **Singleton** | **Low** (one instance) | One-time only | High |
| **Factory Method** | Low | Medium | High |
| **Abstract Factory** | Low | Medium | High |
| **Builder** | Medium (builder objects) | Medium | High |
| **Prototype** | Medium (prototype storage) | **Low** (cloning) | High |

**Optimization Tips:**

**Singleton:**
- Use lazy initialization for resource-intensive objects
- Consider enum singleton in Java (thread-safe, serialization-safe)
- Avoid business logic in singleton

**Factory Method:**
- Cache created objects if immutable and reusable
- Use object pools for expensive objects
- Consider lazy initialization

**Abstract Factory:**
- Reuse factory instances (often implemented as Singleton)
- Cache created products when appropriate
- Consider prototype-based implementation

**Builder:**
- Reuse builder instances for multiple objects
- Consider object pooling for builders
- Use immutable products to enable caching

**Prototype:**
- Profile to ensure cloning is actually faster
- Implement shallow copy when deep copy not needed
- Consider copy-on-write for large objects
- Cache cloned objects when possible

---

### Creational Patterns in Modern Software Architecture

**Dependency Injection Frameworks:**
- **Singleton:** Spring singleton scope, .NET ServiceLifetime.Singleton
- **Factory:** Provider pattern in Angular, Factory beans in Spring
- **Builder:** Configuration builders in Spring Boot

**Microservices Architecture:**
- **Factory:** Service discovery and client creation
- **Builder:** Request/Response builders in gRPC, GraphQL
- **Singleton:** Shared clients (HTTP clients, message brokers)

**Cloud-Native Applications:**
- **Factory:** Creating cloud resources (AWS SDK factories)
- **Builder:** CloudFormation, Terraform resource builders
- **Singleton:** Cloud client instances (S3Client, BlobServiceClient)

**Frontend Development:**
- **Singleton:** Vuex store, Redux store, Angular services
- **Factory:** Component factories in Angular, React elements
- **Builder:** Query builders (Apollo GraphQL), form builders
- **Prototype:** Object spreading in JavaScript/TypeScript

**Domain-Driven Design:**
- **Factory:** Aggregate factories, Entity factories
- **Builder:** Complex aggregate root construction
- **Prototype:** Cloning value objects

**Test Automation:**
- **Builder:** Test data builders (Mother pattern, Object Mother)
- **Factory:** Test fixture factories
- **Prototype:** Cloning test data templates

---

### Testing Creational Patterns

**Singleton Testing:**
- **Challenge:** Global state makes tests interdependent
- **Solution:** Use dependency injection; provide test doubles
- **Tip:** Reset singleton between tests or use fresh instances

```
// Instead of
MyService service = MySingleton.getInstance();

// Use dependency injection
MyService service = new MyService(injectedDependency);
```

**Factory Method Testing:**
- Test factory method independently
- Mock products to test creation logic
- Verify correct product type returned
- Test all factory variations

**Abstract Factory Testing:**
- Test each concrete factory independently
- Verify all products from same family work together
- Mock products for factory testing
- Test factory switching

**Builder Testing:**
- Test builder with different combinations of parameters
- Verify validation in build() method
- Test required vs optional parameters
- Ensure immutability of built objects

**Prototype Testing:**
- Verify cloned object independent from original
- Test deep copy vs shallow copy behavior
- Test with complex object graphs
- Verify circular reference handling

---

### Anti-Patterns to Avoid

**1. Singleton Abuse**
- Using Singleton for everything (anti-pattern: global variables in disguise)
- Singleton with business logic (violates SRP)
- Hidden dependencies through singletons
**Solution:** Use dependency injection; limit singletons to infrastructure

**2. Simple Factory Misnamed as Factory Method**
- Static factory methods ≠ Factory Method pattern
- Confusion between pattern and implementation
**Solution:** Understand pattern intent; use appropriate pattern

**3. Factory for Everything**
- Creating factories when direct instantiation sufficient
- Over-engineering simple object creation
**Solution:** Only use when flexibility needed; YAGNI principle

**4. Builder Overkill**
- Using Builder for simple objects with 2-3 parameters
- Complex builder hierarchies
**Solution:** Use constructors for simple cases; keep builders simple

**5. God Factory**
- Single factory creating unrelated object types
- Factory knows too much about products
**Solution:** Separate factories for different concerns; cohesive factories

**6. Prototype without Proper Cloning**
- Shallow copy when deep copy needed
- Not handling circular references
- Mutable shared state
**Solution:** Implement cloning correctly; document copy semantics

**7. Leaking Singleton References**
- Returning mutable singleton internals
- Not protecting singleton state
**Solution:** Return defensive copies; immutable singletons

---

### Modern Language Features

**Java:**
```
// Factory Method with static factory
Optional.of(), List.of(), Map.of()

// Builder with Lombok
@Builder annotation

// Singleton with enum
enum Singleton { INSTANCE }
```

**JavaScript/TypeScript:**
```
// Prototype with Object.create()
Object.create(prototype)

// Builder with method chaining
fetch(url).then().catch()

// Factory with factory functions
function createUser(name) { ... }
```

**Python:**
```
// Factory Method with __new__
class Factory:
    def __new__(cls, type):
        ...

// Singleton with decorator
@singleton

// Builder with dataclasses
@dataclass
```

**C#:**
```
// Builder with fluent API
new StringBuilder()
    .Append("Hello")
    .Append("World")

// Factory with generics
Factory<T>.Create()

// Singleton with Lazy<T>
private static readonly Lazy<Singleton> instance
```

---

### Real-World Framework Examples

**Spring Framework:**
- **Singleton:** Default bean scope
- **Factory:** FactoryBean, @Bean methods
- **Builder:** WebClient.builder(), RestTemplate builder
- **Prototype:** Prototype bean scope

**Java Standard Library:**
```
// Factory Method
Calendar.getInstance()
NumberFormat.getInstance()

// Builder
StringBuilder, ProcessBuilder

// Prototype
Object.clone()
```

**Android:**
- **Singleton:** Application class
- **Builder:** AlertDialog.Builder, Notification.Builder
- **Factory:** LayoutInflater for creating views

**.NET Core:**
- **Singleton:** AddSingleton() in DI
- **Factory:** IServiceProvider, Factory pattern with DI
- **Builder:** WebHostBuilder, Configuration builders

**JavaScript/Node.js:**
- **Singleton:** Module pattern (module exports)
- **Factory:** Express() factory, React.createElement()
- **Builder:** Query builders (Knex.js), request builders

**Python Frameworks:**
- **Singleton:** Django settings, Flask app
- **Factory:** SQLAlchemy engine creation, Django model factories
- **Builder:** Django ORM query building

---

### Summary: When to Use Each Pattern

**Use Singleton when:**
- Resource must be shared (connection pool, cache, config)
- Global access point needed
- Exactly one instance required
- **Caution:** Consider dependency injection first

**Use Factory Method when:**
- Class can't anticipate object type to create
- Subclasses should specify objects to create
- Localizing knowledge of which class to create
- **Benefit:** Open for extension without modifying existing code

**Use Abstract Factory when:**
- System independent of product creation
- Multiple families of related products
- Family of products designed to work together
- **Benefit:** Ensures product compatibility within families

**Use Builder when:**
- Complex object with many parameters
- Step-by-step construction needed
- Same construction process, different representations
- **Benefit:** Readable, maintainable object creation

**Use Prototype when:**
- Object creation expensive
- Need objects similar to existing ones
- Avoiding parallel hierarchies of factories
- **Benefit:** Performance gain from cloning vs creating

---

### Best Practices Summary

1. **Prefer Dependency Injection over Singleton** for better testability
2. **Use Builder for 4+ constructor parameters** or optional parameters
3. **Choose Abstract Factory for product families**, Factory Method for single products
4. **Document cloning semantics** clearly when using Prototype
5. **Combine patterns judiciously** (e.g., Singleton + Factory, Abstract Factory + Prototype)
6. **Consider modern alternatives** (DI containers, object pools, functional approaches)
7. **Don't over-engineer** - use simplest solution that works
8. **Make factories stateless** when possible
9. **Validate builder state** before building
10. **Thread-safety is crucial** for Singleton in multithreaded environments