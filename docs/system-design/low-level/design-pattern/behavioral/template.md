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
```text
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
*The template method fixes the algorithm skeleton while subclasses override only the varying steps.*

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

---

### Java Example

*The base class fixes the algorithm skeleton; subclasses only fill the varying step.*

```java
abstract class Report {                              // Abstract class with template
    final void generate() {                          // Template method: fixed order
        header(); body(); footer();
    }
    void header() { /* common */ } void footer() { /* common */ }
    abstract void body();                            // Varying step for subclasses
}
class PdfReport extends Report {
    void body() { /* PDF-specific content */ }
}
```

---

### Second Java Example: Data Import Pipeline (ETL)

*The base importer fixes extract → transform → load order; CSV and API importers fill only the varying steps.*

```java
import java.util.List;

abstract class DataImporter {                        // Abstract class with template
    final void importData() {                        // Template method: fixed skeleton
        List<String> raw = extract();                // Invariant order
        List<String> clean = transform(raw);         // Varying step
        load(clean);                                 // Common step
        onComplete();                                // Hook: optional override
    }
    protected abstract List<String> extract();       // Subclasses provide source
    protected abstract List<String> transform(List<String> raw); // Varying logic
    protected void load(List<String> rows) {         // Shared default
        System.out.println("Loading " + rows.size() + " rows into DB");
    }
    protected void onComplete() { }                  // Hook: do nothing by default
}

class CsvImporter extends DataImporter {             // Concrete class: files
    private final String path;
    CsvImporter(String path) { this.path = path; }
    protected List<String> extract() {
        System.out.println("Reading CSV: " + path);
        return List.of(" a,1 ", " b,2 ");            // Raw rows with whitespace
    }
    protected List<String> transform(List<String> raw) {
        return raw.stream().map(s -> s.trim().toUpperCase()).toList(); // Clean rows
    }
    protected void onComplete() {                    // Hook override: notify
        System.out.println("CSV import finished");
    }
}

class ApiImporter extends DataImporter {             // Concrete class: REST source
    private final String endpoint;
    ApiImporter(String endpoint) { this.endpoint = endpoint; }
    protected List<String> extract() {
        System.out.println("GET " + endpoint);
        return List.of("{\"id\":1}", "{\"id\":2}");  // Raw JSON payloads
    }
    protected List<String> transform(List<String> raw) {
        return raw.stream().map(s -> s.replaceAll("[^0-9]", "")).toList(); // IDs only
    }
    // Inherits default load(); skips onComplete hook.
}

class EtlDemo {
    public static void main(String[] args) {
        new CsvImporter("users.csv").importData();   // Same skeleton, file flavour
        new ApiImporter("https://api/users").importData(); // Same skeleton, API flavour
    }
}
```

**Why this domain works:**
- Step order (extract before load) is enforced once in `final importData()`.
- New sources (S3, Kafka) add one subclass instead of copying pipeline code.
- Hooks (`onComplete`) give optional extension without forcing every subclass to implement them.

---

### Template Method vs Strategy

| Aspect | Template Method | Strategy |
|---|---|---|
| Mechanism | Inheritance: base class fixes skeleton, subclasses fill steps | Composition: context delegates whole algorithm to strategy |
| Flexibility | Rigid order; vary only designated steps | Fully swappable algorithms at runtime |
| Extension | Add a new variant via a new subclass | Add a new variant via a new strategy class |
| Typical use | ETL pipelines, JUnit lifecycle, report generation, game loops | Payments, sorting, routing, compression, pricing |
| Drawback | Hierarchy coupling; base change affects all subclasses | More objects; client must choose the strategy |

**Rule of thumb:** use Template Method when the algorithm skeleton is fixed and only steps vary;
use Strategy when entire algorithms are interchangeable at runtime.

---

### Interview Questions and Answers

**Q1: Why is the template method usually declared final?**
**A:** To lock the algorithm skeleton so subclasses cannot reorder or skip steps. Subclasses
override only the designated abstract steps and hooks. Without final, a subclass could break
invariants (loading before extracting), defeating the pattern's guarantee.

**Q2: What are hook methods and when should you add one?**
**A:** Hooks are optional overridable steps with a default (often empty) implementation, like
`onComplete()`. Add them for discretionary extension points; keep them few and documented.
Too many hooks signals the skeleton is unclear — consider Strategy or composition instead.

**Q3: How do you test a Template Method hierarchy?**
**A:** Test the template once with a stub subclass recording call order (`extract → transform →
load`), test each concrete step in isolation, and test hooks both overridden and default.
Verify subclasses cannot break ordering by keeping the template final and covered.

**Q4: When should you avoid Template Method?**
**A:** Avoid it when steps vary so much the skeleton stops helping, when you need runtime
swapping (use Strategy), or when deep hierarchies form. Favour composition over inheritance if
subclasses override most steps or the base class keeps changing for every new variant.

**Key takeaway:** Template Method fixes the algorithm skeleton once in a base class while
subclasses supply only the varying steps — ideal for pipelines, frameworks, and reports.
