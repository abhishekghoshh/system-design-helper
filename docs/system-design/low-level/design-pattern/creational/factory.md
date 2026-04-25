# Factory Design Pattern

## Blogs and websites

## Medium

## Youtube

- [5. Factory Pattern Vs Abstract Factory Pattern Explanation (Hindi) | Low Level System Design](https://www.youtube.com/watch?v=7g9S371qzwM)

## Theory

### Factory Method Pattern

Defines an interface for creating an object, but lets subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses.

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

### Pitfalls and Best Practices (Factory Method)

**Pitfall:** Creating factory subclasses just to instantiate products
**Best Practice:** Use Simple Factory or parameterized factory if no customization needed

**Pitfall:** Too many factory methods
**Best Practice:** Consider Abstract Factory for related products

### Testing (Factory Method)

- Test factory method independently
- Mock products to test creation logic
- Verify correct product type returned
- Test all factory variations

### Performance Considerations (Factory Method)

| Aspect | Detail |
|--------|--------|
| Memory Impact | Low |
| Creation Cost | Medium |
| Scalability | High |

**Optimization Tips:**
- Cache created objects if immutable and reusable
- Use object pools for expensive objects
- Consider lazy initialization

---

### Abstract Factory Pattern

Provides an interface for creating families of related or dependent objects without specifying their concrete classes. A factory of factories.

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

### Pitfalls and Best Practices (Abstract Factory)

**Pitfall:** Difficulty adding new product types (requires interface change)
**Best Practice:** Design product families carefully upfront; consider if flexibility worth complexity

**Pitfall:** Too many factory implementations
**Best Practice:** Ensure you truly need families of related products

### Testing (Abstract Factory)

- Test each concrete factory independently
- Verify all products from same family work together
- Mock products for factory testing
- Test factory switching

### Performance Considerations (Abstract Factory)

| Aspect | Detail |
|--------|--------|
| Memory Impact | Low |
| Creation Cost | Medium |
| Scalability | High |

**Optimization Tips:**
- Reuse factory instances (often implemented as Singleton)
- Cache created products when appropriate
- Consider prototype-based implementation

---

### Factory Method vs Abstract Factory

- **Factory Method** creates one product; **Abstract Factory** creates families
- Factory Method uses inheritance; Abstract Factory uses composition
- Factory Method is simpler; Abstract Factory handles related product groups

---

### Anti-Patterns to Avoid

- **Simple Factory Misnamed as Factory Method:** Static factory methods ≠ Factory Method pattern. Understand pattern intent; use appropriate pattern
- **Factory for Everything:** Creating factories when direct instantiation sufficient. Only use when flexibility needed; YAGNI principle
- **God Factory:** Single factory creating unrelated object types. Separate factories for different concerns; cohesive factories
