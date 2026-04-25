# Database Fundamentals

## Blogs and websites


## Medium


## Youtube


## Theory

### Transactions and ACID Overview

A **transaction** is a logical unit of work that consists of one or more database operations (reads/writes) that must be treated as a single, indivisible operation. Either all operations succeed, or none of them take effect.

**Why Transactions Matter:**
```
Bank Transfer: Move $100 from Account A to Account B

Step 1: Debit Account A by $100
Step 2: Credit Account B by $100

What if the system crashes after Step 1 but before Step 2?
  → Without transactions: $100 disappears (money lost!)
  → With transactions: Both steps roll back (money safe)
```

### ACID Properties — The Four Guarantees

**Atomicity** — All or Nothing
- A transaction is treated as a single unit. If any part fails, the entire transaction is rolled back.
- Example: In a bank transfer, if the credit fails, the debit is reversed.

**Consistency** — Valid State to Valid State
- A transaction takes the database from one valid state to another. All constraints (foreign keys, unique constraints, checks) must be satisfied after the transaction.
- Example: If a column has a `NOT NULL` constraint, no transaction can leave it NULL.

**Isolation** — Concurrent Transactions Don't Interfere
- Multiple transactions running simultaneously behave as if they run sequentially. One transaction cannot see the partial results of another.
- **Isolation Levels** (from weakest to strongest):
  - **Read Uncommitted**: Can see uncommitted data (dirty reads)
  - **Read Committed**: Only sees committed data (default in PostgreSQL)
  - **Repeatable Read**: Same query returns same results within a transaction (default in MySQL InnoDB)
  - **Serializable**: Full isolation, transactions appear sequential (slowest, safest)

**Durability** — Committed Data Survives Crashes
- Once a transaction is committed, the data persists even if the system crashes, power goes out, or hardware fails.
- Achieved through Write-Ahead Logging (WAL) — changes are written to a log before being applied.

### ACID vs BASE

| Property | ACID (SQL) | BASE (NoSQL) |
|----------|-----------|---------------|
| **Focus** | Correctness | Availability |
| **Consistency** | Strong (immediate) | Eventual |
| **Transactions** | Full ACID support | Limited or none |
| **Scale** | Vertical (scale up) | Horizontal (scale out) |
| **Use case** | Banking, inventory | Social feeds, analytics |

**BASE** stands for:
- **Basically Available**: System responds to every request (may be stale)
- **Soft State**: State can change without new input (replication lag)
- **Eventually Consistent**: Given enough time, all nodes converge

**When to Choose:**
- Use ACID when data correctness is critical (financial, medical, booking)
- Use BASE when availability and scale matter more than instant consistency (social media, IoT)

---

### Quick Reference

Organized collection of structured data.

**ACID Properties:**
- **Atomicity**: All or nothing transactions
- **Consistency**: Data integrity maintained
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed data persists

**BASE (NoSQL alternative):**
- **Basically Available**: System available most of the time
- **Soft state**: State may change over time
- **Eventual consistency**: System becomes consistent eventually
