# Proxy Design Pattern

## Blogs and websites

## Medium

## Youtube

- [13. Proxy Design Pattern Explanation (Hindi) | LLD | System Design Interview Question | Java](https://www.youtube.com/watch?v=9MxHKlVc6ZM)

## Theory

### What is Proxy Pattern?

Provides a surrogate or placeholder for another object to control access to it. Acts as an interface to something else.

**Types of Proxy:**
- **Virtual Proxy:** Delays expensive object creation until actually needed (lazy initialization)
- **Protection Proxy:** Controls access rights to the original object
- **Remote Proxy:** Represents an object in a different address space
- **Smart Proxy:** Performs additional actions when accessing an object (reference counting, caching, etc.)

---

### Diagram

```text
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
*Clients talk to the proxy through the subject interface while it controls access to the real object.*

---

### Real-Life Examples

- **Virtual Proxy:** Lazy loading of high-resolution images (thumbnails load first, full image on demand)
- **Protection Proxy:** Role-based access control in enterprise applications (Spring Security)
- **Remote Proxy:** RPC frameworks (gRPC), REST clients representing remote services
- **Cache Proxy:** CDN proxies caching content closer to users (Cloudflare, Akamai)
- **Smart Proxy:** Hibernate lazy loading of database entities
- **Logging Proxy:** AOP proxies in Spring adding logging/monitoring to service calls
- **Nginx/HAProxy:** Reverse proxy controlling access to backend servers

---

### Advantages

- Controls access to the real object (security, lazy initialization)
- Adds functionality without changing the real object
- Provides location transparency for remote objects
- Optimizes resource usage through lazy initialization
- Can add caching, logging, access control transparently

---

### Disadvantages

- Adds extra layer of indirection (slight performance overhead)
- Increases complexity of the codebase
- Response time may increase in some cases
- Can make code harder to debug

---

### When to Use

- You need lazy initialization (virtual proxy)
- You need access control (protection proxy)
- You need local representation of remote object (remote proxy)
- You need additional functionality before/after accessing an object (smart proxy)
- You need caching of expensive operations

---

### Pitfalls and Best Practices

**Pitfall:** Forgetting to implement all methods of the real object's interface
**Best Practice:** Use composition and delegation systematically; consider dynamic proxies (Java)

**Pitfall:** Proxy becoming too complex with mixed responsibilities
**Best Practice:** Keep each proxy focused on one concern (access control OR caching OR logging)

---

### Testing Proxy Pattern

- Test proxy and real object separately
- Verify proxy forwards all operations correctly
- Test proxy-specific behavior (caching, lazy loading, access control)
- Verify proxy doesn't alter the real object's behavior unintentionally

---

### Performance Considerations

| Aspect | Impact |
|--------|--------|
| **Memory** | Low |
| **Runtime Cost** | Low-Medium (depends on proxy type) |
| **Scalability** | High |

**Tip:** Virtual proxy is excellent for deferring expensive operations

---

### Java Example

*The proxy stands in for the real image and loads it only on first display.*

```java
interface Image { void display(); }                  // Subject interface
class RealImage implements Image {                   // Expensive real object
    public void display() { /* load + render */ }
}
class ImageProxy implements Image {                  // Virtual proxy: lazy loads
    private RealImage real;
    public void display() {
        if (real == null) real = new RealImage();
        real.display();
    }
}
```

---

### Real-World Java Example: Protection Proxy for Bank Account Access

*Branch software must check the teller's role before allowing withdrawals on an account. A protection proxy enforces the policy in one place so the real account class stays focused purely on balances.*

```java
// Subject: what both the real object and the proxy implement
interface BankAccount {
    void deposit(double amount);
    boolean withdraw(double amount);
    double balance();
}

// RealSubject: pure ledger logic with no security concerns
class RealBankAccount implements BankAccount {
    private double balance;

    RealBankAccount(double opening) { this.balance = opening; }

    @Override public void deposit(double amount) { balance += amount; }

    @Override
    public boolean withdraw(double amount) {
        if (amount > balance) return false;
        balance -= amount;
        return true;
    }

    @Override public double balance() { return balance; }
}

// Minimal role model for the demo
enum Role { TELLER, MANAGER }

// Protection proxy: authorises before delegating to the real account
class AccountProtectionProxy implements BankAccount {
    private final BankAccount real;
    private final Role caller;
    private static final double TELLER_LIMIT = 10_000;

    AccountProtectionProxy(BankAccount real, Role caller) {
        this.real = real;
        this.caller = caller;
    }

    @Override
    public void deposit(double amount) {
        real.deposit(amount); // deposits need no approval here
        System.out.println("AUDIT deposit $" + amount + " by " + caller);
    }

    @Override
    public boolean withdraw(double amount) {
        if (caller == Role.TELLER && amount > TELLER_LIMIT) {
            System.out.println("DENIED: teller limit is $" + TELLER_LIMIT);
            return false; // real object never touched
        }
        boolean ok = real.withdraw(amount);
        System.out.println("AUDIT withdraw $" + amount + " by " + caller + " ok=" + ok);
        return ok;
    }

    @Override
    public double balance() {
        return real.balance(); // read-through, could add masking here
    }
}

// Client: same interface, different power depending on the role
class BranchDemo {
    public static void main(String[] args) {
        BankAccount account = new RealBankAccount(50_000);
        BankAccount teller = new AccountProtectionProxy(account, Role.TELLER);
        BankAccount manager = new AccountProtectionProxy(account, Role.MANAGER);
        teller.withdraw(25_000);   // denied by the proxy
        manager.withdraw(25_000);  // allowed and audited
    }
}
```

*Why a proxy fits better than inline checks:*
- Security and auditing live in one class; `RealBankAccount` never imports roles or logging.
- The branch UI depends only on `BankAccount`, so swapping in the proxy requires no caller changes.
- Tests can exercise overdraft math on the real account and authorisation rules on the proxy independently.

---

### Proxy vs Decorator

*Both share the subject's interface and delegate to a wrapped object, but Proxy guards or optimises access while Decorator openly adds features the client composes.*

| Aspect | Proxy | Decorator |
|--------|-------|-----------|
| **Intent** | Control access to the real object (guard, defer, cache) | Add behaviour dynamically by stacking wrappers |
| **Transparency** | Client ideally cannot tell the proxy is present | Client deliberately builds the decorator chain |
| **Typical layering** | One proxy per concern, often created by a framework | Many decorators nested by hand in any order |
| **Lifecycle role** | May create, cache, or synchronise the real object | Never manages the wrapped object's lifecycle |
| **Typical example** | `AccountProtectionProxy` enforcing teller limits | `EncryptionDecorator` stacked onto a notifier |

*Rule of thumb: if the wrapper says "you may not" or "not yet", it is a Proxy; if it says "and also", it is a Decorator.*

---

### Interview Questions

**Q1: What are the four classic proxy types, and when is each used?**

A virtual proxy defers expensive creation until first use, like the lazy image loader. A protection proxy enforces access rights, like the teller-limit guard above. A remote proxy stands in for an object in another process or machine, as with gRPC stubs. A smart or cache proxy adds bookkeeping such as reference counting, copy-on-write, or result caching around each call. Choose by naming the problem: cost, permission, distance, or bookkeeping.

**Q2: How do static proxies differ from Java dynamic proxies?**

A static proxy is a hand-written class implementing the subject interface, which is simple but requires a new class per interface. A dynamic proxy (`java.lang.reflect.Proxy`) generates the wrapper at runtime from an `InvocationHandler`, so one handler can proxy any interface for cross-cutting concerns like logging or transactions. Frameworks such as Spring AOP build on dynamic proxies and bytecode generation (CGLIB) for exactly this reason. Prefer dynamic proxies when the logic is generic; write static proxies when the policy is domain-specific.

**Q3: What are the pitfalls of overusing proxies?**

Each proxy adds indirection that slows calls slightly and lengthens stack traces, which hurts latency-sensitive paths and debuggability. Stacking caching, security, and logging proxies can also produce surprising interactions, such as cached denials or unaudited cache hits. Keep one concern per proxy, document the intended ordering, and measure before placing a proxy on a hot path. Make sure every proxy method delegates faithfully so new interface methods do not silently bypass the guard.

**Q4: How do you test proxy behaviour?**

Test the real subject alone for domain correctness (deposits, overdrafts, balances). Then test the proxy with a stubbed or real subject: verify allowed calls delegate with identical results, denied calls never reach the real object, and side effects such as audit logs fire exactly once. For virtual proxies, assert the expensive object is created lazily and only once; for cache proxies, assert hit and miss paths plus invalidation. Finally, test through the subject interface so the test proves the proxy is truly substitutable.
