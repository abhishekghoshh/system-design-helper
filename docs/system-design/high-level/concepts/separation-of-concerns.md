# Separation of Concerns

## Theory

### What is Separation of Concerns?

**Separation of Concerns (SoC)** is a design principle that divides a system into distinct sections, where each section addresses a specific concern (responsibility). Each part should know as little as possible about the others.

**Core Idea:** A piece of code should do **one thing** and do it well. Changes to one concern should not require changes to unrelated concerns.

### Why It Matters

```
Without SoC (everything mixed together):
  function handleOrder(req) {
    // Validate input
    // Authenticate user
    // Check inventory
    // Process payment
    // Send email
    // Update analytics
    // Return response
  }
  → 500 lines, impossible to test, change, or reuse

With SoC (separated responsibilities):
  validateInput(req)        → Validation layer
  authenticateUser(req)     → Auth middleware
  checkInventory(items)     → Inventory service
  processPayment(order)     → Payment service
  sendConfirmation(email)   → Notification service
  trackEvent(order)         → Analytics service
  → Each is testable, changeable, and reusable independently
```

### Levels of Separation

**1. Code Level — Functions and Classes**
- Single Responsibility Principle (SRP): A class/function has one reason to change
- Example: A `UserValidator` class only validates, a `UserRepository` only handles DB queries

**2. Module/Layer Level — Layered Architecture**
```
Presentation Layer (UI, API endpoints)
        ↓
Business Logic Layer (rules, workflows)
        ↓
Data Access Layer (database queries, ORM)
        ↓
Infrastructure Layer (file system, external APIs)
```
Each layer only talks to the one directly below it.

**3. Service Level — Microservices**
```
User Service       → Manages user accounts
Payment Service    → Handles payments
Notification Service → Sends emails/SMS
Inventory Service  → Tracks stock levels
```
Each service owns its data and logic independently.

**4. System Level — Frontend vs Backend**
```
Frontend (Client):  UI rendering, user interaction, local state
Backend (Server):   Business logic, data persistence, security
Database:           Storage, querying, transactions
```

### Related Principles

**Don't Repeat Yourself (DRY):**
Extract shared logic into reusable components instead of duplicating code.

**Interface Segregation:**
Don't force a module to depend on interfaces it doesn't use. Keep interfaces small and focused.

**Dependency Inversion:**
High-level modules shouldn't depend on low-level modules. Both should depend on abstractions (interfaces).

### Real-World Examples

**MVC Pattern (Model-View-Controller):**
```
Model:      Data and business logic
View:       UI presentation
Controller: Handles input, coordinates Model and View
```

**Clean Architecture:**
```
Entities (core business rules)
  ← Use Cases (application rules)
    ← Interface Adapters (controllers, presenters)
      ← Frameworks & Drivers (DB, web, UI)

Inner layers know nothing about outer layers.
Dependencies point inward only.
```

**API Design:**
```
/api/users      → User concern
/api/products   → Product concern
/api/orders     → Order concern

Each endpoint group handles one domain entity.
```

### Benefits
- **Maintainability**: Change one concern without breaking others
- **Testability**: Test each part in isolation
- **Reusability**: Use the same module in different contexts
- **Team Scalability**: Different teams can own different concerns
- **Debuggability**: Easier to locate bugs when responsibilities are clear

### Anti-Patterns (Violations of SoC)
- **God Object**: One class that does everything
- **Spaghetti Code**: Logic spread across files with no clear boundaries
- **Leaky Abstractions**: Database queries in the UI layer
- **Tight Coupling**: Changing one module forces changes in many others
