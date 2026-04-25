# Template Method Design Pattern

## Blogs and websites

## Medium

## Youtube

- [39. Template Method Design Pattern Explanation in Java | Concept and Coding LLD | Low Level Design](https://www.youtube.com/watch?v=kwy-G1DEm0M)

## Theory

### Template Method Pattern

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

### Pitfalls and Best Practices

**Pitfall:** Too many hook methods; rigid inheritance hierarchy
**Best Practice:** Limit hooks to essential variations; consider Strategy for more flexibility

---

### Testing Template Method Pattern

- Test template method with different subclass implementations
- Verify invariant steps execute in correct order
- Test hook methods called at right time
- Validate abstract methods implemented correctly
