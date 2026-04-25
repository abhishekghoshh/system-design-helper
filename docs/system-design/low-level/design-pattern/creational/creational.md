# All Creational Design Patterns 

## Blogs and websites

## Medium

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
