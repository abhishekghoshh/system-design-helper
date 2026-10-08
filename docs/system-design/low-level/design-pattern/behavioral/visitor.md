# Visitor Design Pattern

## Blogs and websites

## Medium

## Youtube

- [36. Visitor Design Pattern | Double Dispatch | Low Level Design](https://www.youtube.com/watch?v=pDsz-AuFO0g)

## Theory

### Visitor Pattern

**Theory:** Lets you define a new operation without changing the classes of the elements on which it operates. Separates algorithms from the objects they operate on.

**Why it's used:**
- To add operations to existing class hierarchy without modifying classes
- When many unrelated operations need to be performed on objects
- To keep related operations together
- When class hierarchy is stable but operations change frequently

**Diagram:**
```text
Element Interface → accept(Visitor)
  ↓                      ↓
ConcreteElement → Visitor Interface
                       ↓
                  ConcreteVisitor
                  (operations)
```
*Elements accept the visitor, which carries the new operation across the object structure.*

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

### Pitfalls and Best Practices

**Pitfall:** Hard to add new element types; breaks encapsulation
**Best Practice:** Use only for stable hierarchies; consider alternatives if structure changes often

---

### Testing Visitor Pattern

- Test visitor on each element type
- Test element acceptance of visitor
- Verify visitor accumulates state correctly
- Test with composite structures

---

### Java Example

*Elements accept a visitor, letting new operations be added without changing element classes.*

```java
interface Visitor { void visit(Circle c); }          // Visitor interface
interface Shape { void accept(Visitor v); }          // Element interface
class Circle implements Shape {                      // Concrete element
    public void accept(Visitor v) { v.visit(this); } // Double dispatch
}
class AreaCalculator implements Visitor {            // Concrete visitor: new operation
    public void visit(Circle c) { /* compute area */ }
}
```

---

### Second Java Example: Shopping Cart Tax and Discount

*Cart items accept visitors; tax and discount logic lives in visitors, not in item classes.*

```java
interface CartVisitor {                              // Visitor interface
    void visit(Book b);
    void visit(Electronics e);
}

interface CartItem {                                 // Element interface
    void accept(CartVisitor v);
    double price();
}

class Book implements CartItem {                     // Concrete element
    private final double price;
    Book(double price) { this.price = price; }
    public double price() { return price; }
    public void accept(CartVisitor v) { v.visit(this); } // Double dispatch
}

class Electronics implements CartItem {              // Concrete element
    private final double price;
    Electronics(double price) { this.price = price; }
    public double price() { return price; }
    public void accept(CartVisitor v) { v.visit(this); }
}

class TaxCalculator implements CartVisitor {         // Concrete visitor: tax rules
    double totalTax = 0;
    public void visit(Book b) { totalTax += b.price() * 0.05; } // 5% on books
    public void visit(Electronics e) { totalTax += e.price() * 0.18; } // 18% on gadgets
}

class DiscountApplier implements CartVisitor {       // Concrete visitor: discounts
    double totalDiscount = 0;
    public void visit(Book b) { totalDiscount += b.price() * 0.10; } // 10% off books
    public void visit(Electronics e) { totalDiscount += 0; } // No discount on gadgets
}

class CartDemo {
    public static void main(String[] args) {
        CartItem[] cart = { new Book(500), new Electronics(20000) };
        TaxCalculator tax = new TaxCalculator();
        DiscountApplier discount = new DiscountApplier();
        for (CartItem item : cart) {                 // Same structure, two operations
            item.accept(tax);
            item.accept(discount);
        }
        System.out.println("Tax=" + tax.totalTax + " Discount=" + discount.totalDiscount);
    }
}
```

**Why this domain works:**
- New operations (shipping cost, gift wrap, loyalty points) are new visitors — items untouched.
- Related logic stays together: all tax rules in one class, all discounts in another.
- Visitor accumulates state (`totalTax`) while traversing, unlike a plain loop helper.

---

### Visitor vs Iterator

| Aspect | Visitor | Iterator |
|---|---|---|
| Purpose | Add new operations over a stable element hierarchy | Walk elements one by one hiding storage details |
| Who holds logic | Visitor object carries the operation across elements | Client loop holds per-element logic |
| Dispatch | Double dispatch: element calls back `visitor.visit(this)` | Single loop: `hasNext/next` yields elements |
| Typical use | AST analysis, tax/export over cart, serialization, reports | Collections, cursors, paginated APIs, tree traversal |
| Pain point | Adding an element type breaks every visitor | No help structuring complex per-type operations |

**Rule of thumb:** use Visitor when operations change often but element types are stable; use
Iterator when clients just need uniform sequential access with their own logic.

---

### Interview Questions and Answers

**Q1: What is double dispatch and why does Visitor need it?**
**A:** Single dispatch picks a method by the receiver type only. Visitor needs two types —
element and visitor — so `element.accept(visitor)` dispatches on the element, then
`visitor.visit(this)` overloads on the concrete element type. Together they route to the right
`visit(Book)` vs `visit(Electronics)` without instanceof chains.

**Q2: What is the biggest drawback of Visitor?**
**A:** Adding a new element type breaks every visitor: each `CartVisitor` needs a new `visit()`
overload and every concrete visitor a new implementation. That is why Visitor suits stable
hierarchies with evolving operations — invert to Strategy or plain polymorphism otherwise.

**Q3: How does Visitor affect encapsulation?**
**A:** Negatively — visitors often need element internals (price, AST children), forcing public
getters that expose representation. Mitigate by exposing only what visitors need, keeping
visitors in the same package, or using internal accessor interfaces instead of full public state.

**Q4: When should you avoid the Visitor pattern?**
**A:** Avoid it when element types change frequently, when hierarchies are small (a polymorphic
method is simpler), or when traversal and operation are trivial loops. Visitor pays off for
rich stable structures (ASTs, document models, carts) with many distinct operations.

**Key takeaway:** Visitor separates operations from object structure via double dispatch —
adding operations is cheap, adding element types is expensive.
