# Strategy Design Pattern

## Blogs and websites

## Medium

## Youtube

- [2. Strategy Design Pattern explanation (Hindi) | LLD System Design | Design pattern in Java](https://www.youtube.com/watch?v=u8DttUrXtEw)

## Theory

### Strategy Pattern

**Theory:** Defines a family of algorithms, encapsulates each one, and makes them interchangeable. Strategy lets the algorithm vary independently from clients that use it.

**Why it's used:**
- To define multiple algorithms for a task
- To make algorithms interchangeable at runtime
- To eliminate conditional statements for algorithm selection
- To hide complex, algorithm-specific data structures

**Diagram:**
```text
Context → Strategy Interface
              ↓
    ┌─────────┼─────────┐
StrategyA  StrategyB  StrategyC
(algo1)    (algo2)    (algo3)
```
*The context delegates work to the selected strategy, which can be swapped at runtime.*

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

### Pitfalls and Best Practices

**Pitfall:** Clients must know all strategies; overhead for simple algorithms
**Best Practice:** Use factory to select strategy; provide default strategy

---

### Testing Strategy Pattern

- Test each strategy algorithm independently
- Test strategy switching at runtime
- Mock context for strategy testing
- Verify all strategies satisfy interface contract

---

### Java Example

*The checkout (context) delegates payment to the selected strategy at runtime.*

```java
interface PayStrategy { void pay(double amount); }   // Strategy interface
class CardPayment implements PayStrategy {           // Concrete strategies
    public void pay(double amount) { /* charge card */ }
}
class UpiPayment implements PayStrategy {
    public void pay(double amount) { /* UPI transfer */ }
}
class Checkout {                                     // Context: uses a strategy
    private PayStrategy strategy;
    void setStrategy(PayStrategy s) { strategy = s; }
    void pay(double amount) { strategy.pay(amount); }
}
```

---

### Second Java Example: Route Planning (Maps)

*The navigator (context) delegates route computation to the selected travel-mode strategy.*

```java
import java.util.Map;

interface RouteStrategy {                            // Strategy interface
    String route(String from, String to);
}

class DrivingRoute implements RouteStrategy {        // Concrete strategy: fastest roads
    public String route(String from, String to) {
        return "Driving " + from + " -> " + to + " via highway";
    }
}

class WalkingRoute implements RouteStrategy {        // Concrete strategy: sidewalks
    public String route(String from, String to) {
        return "Walking " + from + " -> " + to + " via parks";
    }
}

class TransitRoute implements RouteStrategy {        // Concrete strategy: bus + metro
    public String route(String from, String to) {
        return "Transit " + from + " -> " + to + " via metro line 2";
    }
}

class Navigator {                                    // Context: delegates to strategy
    private RouteStrategy strategy;
    private static final Map<String, RouteStrategy> MODES = Map.of(
        "driving", new DrivingRoute(),
        "walking", new WalkingRoute(),
        "transit", new TransitRoute()
    );
    Navigator(String mode) { setMode(mode); }        // Default strategy at construction
    void setMode(String mode) {                      // Swappable at runtime
        strategy = MODES.getOrDefault(mode.toLowerCase(), MODES.get("driving"));
    }
    String navigate(String from, String to) { return strategy.route(from, to); }
}

class MapsDemo {
    public static void main(String[] args) {
        Navigator nav = new Navigator("driving");
        System.out.println(nav.navigate("Home", "Office"));
        nav.setMode("transit");                      // Rush hour: swap algorithm
        System.out.println(nav.navigate("Home", "Office"));
        nav.setMode("walking");                      // Weekend stroll
        System.out.println(nav.navigate("Home", "Park"));
    }
}
```

**Why this domain works:**
- Adding cycling or EV-charging routes means one new class, zero changes to `Navigator`.
- A factory/map hides strategy selection so the UI passes only a mode string.
- Each algorithm is independently testable with fixed origin-destination pairs.

---

### Strategy vs State

| Aspect | Strategy | State |
|---|---|---|
| Purpose | Swap interchangeable algorithms on demand | Change behaviour as internal lifecycle state changes |
| Who switches | Client/context picks explicitly (`setMode("transit")`) | Current state object triggers the transition itself |
| Transitions | None — strategies are independent peers | Core concern — explicit machine (PENDING → PAID → SHIPPED) |
| Typical use | Payments, routing, sorting, compression, pricing | Orders, TCP connections, vending machines, auth sessions |
| Client knowledge | Client must know the options to choose | Client sends events; states decide validity |

**Rule of thumb:** use Strategy when the caller chooses among peer algorithms; use State when the
object lifecycle dictates which behaviour is valid.

---

### Interview Questions and Answers

**Q1: How do you stop clients from needing to know every strategy?**
**A:** Hide selection behind a factory or registry: client passes a key (`"upi"`, `"transit"`)
and the factory returns the strategy, with a sensible default. Document each strategy's
trade-offs so callers choose by intent, not by reading implementations.

**Q2: Strategy vs simple if-else — when does the pattern pay off?**
**A:** It pays off at three or more algorithms, when algorithms change independently, or when you
need runtime swapping and isolated testing. For one or two stable branches, if-else is clearer —
refactor to Strategy once conditionals spread or violate Open/Closed.

**Q3: How do you share data between context and strategy without leaking internals?**
**A:** Pass only what the algorithm needs as method parameters (amount, route endpoints), keep
strategies stateless where possible, and inject shared services (pricing config, HTTP client)
via constructor. Avoid giving strategies a back-reference to the full context object.

**Q4: When should you avoid the Strategy pattern?**
**A:** Avoid it when algorithms rarely vary, when clients should not choose (use State or a rule
engine), or when strategies differ only by a value — then a parameter, enum, or lambda beats a
class hierarchy. Extra classes without independent evolution are just ceremony.

**Key takeaway:** Strategy encapsulates each algorithm behind one interface so contexts stay
stable while behaviours swap at runtime — ideal for payments, routing, and pricing.
