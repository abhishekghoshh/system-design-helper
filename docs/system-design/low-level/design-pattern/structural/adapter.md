# Adapter Design Pattern

## Blogs and websites

## Medium

## Youtube

- [20. Adapter Design Pattern with Examples, LLD | Low Level Design Interview Question | System Design](https://www.youtube.com/watch?v=8wrg7IsILhQ)

## Theory

### What is Adapter Pattern?

Converts the interface of a class into another interface that clients expect. Acts as a bridge between two incompatible interfaces.

**Why it's used:**
- When you want to use an existing class but its interface doesn't match what you need
- To create reusable classes that cooperate with unrelated or unforeseen classes
- When working with legacy code that cannot be modified
- To integrate third-party libraries with incompatible interfaces

---

### Diagram

```text
    Client
       ↓
   [Target Interface]
       ↓
    Adapter  ──────→  [Adaptee]
   (converts)        (existing class)
```
*The adapter implements the target interface and translates each call into the adaptee's interface.*

---

### Real-Life Examples

- **Payment Gateways:** Adapting different payment providers (Stripe, PayPal, Razorpay) to a unified payment interface
- **Database Drivers:** JDBC adapters converting different database APIs (MySQL, PostgreSQL, Oracle) to a common interface
- **Logging Libraries:** SLF4J adapting various logging frameworks (Log4j, Logback, java.util.logging)
- **Cloud Storage:** Adapting AWS S3, Google Cloud Storage, Azure Blob Storage to a common file storage interface
- **Legacy System Integration:** Wrapping SOAP services to work with modern REST APIs

---

### Advantages

- Promotes code reusability without modifying existing code
- Follows Open/Closed Principle (open for extension, closed for modification)
- Increases flexibility when integrating third-party libraries
- Enables single client code to work with multiple incompatible interfaces

---

### Disadvantages

- Increases overall complexity by adding additional classes
- Can impact performance due to extra layer of indirection
- May be difficult to adapt if target interface is significantly different

---

### When to Use

- You need to use a third-party class but its interface doesn't match your requirements
- You want to create a reusable class that works with classes having incompatible interfaces
- You need to integrate legacy systems with modern architectures

---

### Pitfalls and Best Practices

**Pitfall:** Over-adapting - creating adapters when you could modify the source
**Best Practice:** Only use adapters for code you don't control (third-party libraries, legacy code)

**Pitfall:** Creating too many adapters making the codebase hard to navigate
**Best Practice:** Consolidate related adaptations; document adapter purpose clearly

---

### Testing Adapter Pattern

- Test that adapted interface works correctly
- Verify edge cases and error handling
- Mock the adaptee for isolated testing
- Ensure adapter forwards all operations faithfully

---

### Performance Considerations

| Aspect | Impact |
|--------|--------|
| **Memory** | Low (single wrapper) |
| **Runtime Cost** | Low |
| **Scalability** | High |

---

### Java Example

*The adapter implements the interface the client expects and translates each call to the adaptee.*

```java
interface Charger { void charge(); }            // Target: what the client expects
class LegacyPlug { void plugIn() { /* ... */ } }// Adaptee: incompatible interface
class PlugAdapter implements Charger {          // Adapter: converts plugIn() to charge()
    private final LegacyPlug plug = new LegacyPlug();
    @Override public void charge() { plug.plugIn(); }
}
```

---

### Real-World Java Example: Unifying Payment Providers

*Our checkout code depends on one `PaymentProcessor` interface, while Stripe and PayPal SDKs each expose their own incompatible APIs. Two adapters let us swap providers without touching checkout logic.*

```java
// Target: the interface our application code expects
interface PaymentProcessor {
    String pay(double amountInr);
    boolean refund(String transactionId, double amountInr);
}

// Adaptee 1: Stripe SDK with its own method names and types
class StripeGateway {
    String createCharge(long amountPaise) {
        return "stripe_ch_" + amountPaise; // calls Stripe API
    }
    boolean reverseCharge(String chargeId, long amountPaise) {
        return true; // calls Stripe refund API
    }
}

// Adaptee 2: PayPal SDK with yet another API shape
class PayPalClient {
    String sendPayment(double amountUsd) {
        return "paypal_txn_" + amountUsd; // calls PayPal API
    }
    boolean voidPayment(String txnId) {
        return true; // calls PayPal void API
    }
}

// Adapter for Stripe: converts pay()/refund() into Stripe calls
class StripeAdapter implements PaymentProcessor {
    private final StripeGateway stripe = new StripeGateway();

    @Override
    public String pay(double amountInr) {
        long paise = Math.round(amountInr * 100); // unit conversion
        return stripe.createCharge(paise);
    }

    @Override
    public boolean refund(String transactionId, double amountInr) {
        long paise = Math.round(amountInr * 100);
        return stripe.reverseCharge(transactionId, paise);
    }
}

// Adapter for PayPal: converts pay()/refund() into PayPal calls
class PayPalAdapter implements PaymentProcessor {
    private final PayPalClient paypal = new PayPalClient();
    private static final double INR_TO_USD = 0.012;

    @Override
    public String pay(double amountInr) {
        double usd = amountInr * INR_TO_USD; // currency conversion
        return paypal.sendPayment(usd);
    }

    @Override
    public boolean refund(String transactionId, double amountInr) {
        return paypal.voidPayment(transactionId); // full-void semantics
    }
}

// Client: checkout depends only on the target interface
class CheckoutService {
    private final PaymentProcessor payments;
    CheckoutService(PaymentProcessor payments) { this.payments = payments; }

    void checkout(double amount) {
        String txnId = payments.pay(amount);
        System.out.println("Paid, txn=" + txnId);
    }
}
```

*Why this is realistic:*
- Each adapter also handles unit conversion (rupees to paise) and currency conversion, which is exactly the translation work adapters do in production.
- Adding Razorpay later means writing one new `RazorpayAdapter` class; `CheckoutService` stays untouched.
- In tests, `CheckoutService` can be wired to a fake `PaymentProcessor` with no adapter involved.

---

### Adapter vs Bridge

*Both patterns involve an extra layer of indirection, but they solve different problems: Adapter fixes an interface mismatch after the fact, while Bridge is designed up front so two hierarchies can vary independently.*

| Aspect | Adapter | Bridge |
|--------|---------|--------|
| **Intent** | Convert an existing incompatible interface into one the client expects | Decouple an abstraction from its implementation so both can vary |
| **Timing** | Applied retroactively to legacy or third-party code you cannot change | Designed proactively when you foresee multiple dimensions of variation |
| **Number of interfaces** | Adapts one adaptee interface to one target interface | Keeps two parallel hierarchies (abstraction + implementation) |
| **Who knows whom** | Adapter knows the adaptee; client only sees the target | Abstraction holds a reference to the implementation interface |
| **Typical example** | Wrapping Stripe/PayPal SDKs behind `PaymentProcessor` | `Remote` abstraction delegating to `Device` implementations (TV, Radio) |

*Rule of thumb: if you are wrapping code you do not control to make it fit, it is an Adapter; if you are splitting your own design along two axes (e.g. shape vs renderer), it is a Bridge.*

---

### Interview Questions

**Q1: What is the difference between a class adapter and an object adapter?**

A class adapter uses inheritance (extends the adaptee and implements the target), while an object adapter uses composition (holds a reference to the adaptee and delegates). Java favours object adapters because a class can only extend one superclass, and composition keeps the adapter loosely coupled. The payment example above is an object adapter: `StripeAdapter` *has a* `StripeGateway`. Prefer object adapters unless you specifically need to override adaptee behaviour.

**Q2: How does Adapter differ from Facade and Decorator?**

All three wrap other objects, but their intent differs. Adapter changes the interface so incompatible code can work together. Facade simplifies a whole subsystem behind one easy entry point without changing any interfaces. Decorator keeps the same interface and adds behaviour dynamically. A quick test: if the wrapper translates method names or signatures, it is an Adapter; if it hides ten subsystems behind one method, it is a Facade; if it adds features while staying interchangeable, it is a Decorator.

**Q3: When would you NOT use an Adapter?**

Do not create an adapter for code you own and can refactor cleanly, because the extra indirection hides the real design and adds maintenance cost. If the target interface and the adaptee are drifting in very different directions, a thin adapter becomes a bloated translator full of edge cases; that is a sign to redesign the interface or write a proper anti-corruption layer instead. Also avoid stacking adapters on adapters, since debugging through three layers of translation is painful.

**Q4: How do you test Adapter pattern code?**

Test at two levels. First, unit-test each adapter against a mocked adaptee: verify that `pay()` calls the right SDK method with correctly converted arguments, and that return values and exceptions are translated faithfully. Second, test the client (`CheckoutService`) against a stub `PaymentProcessor` so provider details do not leak into checkout tests. Also cover edge cases the translation introduces, such as rounding in currency conversion, null transaction ids, and SDK-specific failures mapped to your domain exceptions.
