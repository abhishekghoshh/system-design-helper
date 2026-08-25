# Design a Simple Expense-Splitting App (Splitwise-like)

## Blogs and websites

## Medium

## Youtube

## Theory

### Topics Covered

1. [Introduction and Problem Statement](#introduction-and-problem-statement)
2. [Functional Requirements](#functional-requirements)
3. [Non-Functional Requirements](#non-functional-requirements)
4. [Capacity Estimation](#capacity-estimation)
5. [Characteristics](#characteristics)
6. [Components](#components)
7. [Patterns](#patterns)
8. [Benefits](#benefits)
9. [Pros](#pros)
10. [Cons](#cons)
11. [Challenges](#challenges)
12. [Best Practices](#best-practices)
13. [When to Use and When Not to Use](#when-to-use-and-when-not-to-use)
14. [Use Cases](#use-cases)
15. [API Design and Contract](#api-design-and-contract)
16. [Data Modeling](#data-modeling)
17. [High-Level Design](#high-level-design)
18. [Deep Dive](#deep-dive)
19. [Java and Spring Boot Implementation Guide](#java-and-spring-boot-implementation-guide)
20. [Interview Questions and Answers](#interview-questions-and-answers)

---

### Introduction and Problem Statement

Design a simple expense-splitting app where a group of users can log shared expenses, split them (equally or by custom shares), and see who owes whom, with a way to settle up. This is the classic "Splitwise" problem: a small-group financial ledger that converts a messy web of IOUs into a minimal set of settlement payments.

The core difficulty is not CRUD — it is **money math done correctly**. Floating-point rounding, unequal splits that must sum exactly to the expense total, concurrent edits, and a debt-simplification algorithm that reduces N² pairwise debts to at most N−1 transactions are where candidates win or lose the interview.

```mermaid
flowchart LR
    Alice["Alice paid $90 dinner"] --> Exp["Expense: $90, split EQUAL among 3"]
    Exp --> S1["Alice share $30"]
    Exp --> S2["Bob share $30"]
    Exp --> S3["Carol share $30"]
    S2 --> D1["Bob owes Alice $30"]
    S3 --> D2["Carol owes Alice $30"]
    D1 --> Settle["Settlement: Bob pays Alice $30"]
    D2 --> Settle
```

**Key terms**

- **Expense** — a single shared purchase with a payer, a total amount, a currency, and a split rule.
- **Split rule** — how the total is divided: `EQUAL`, `EXACT` (absolute amounts), `SHARES` (weighted units), or `PERCENTAGE`.
- **Balance** — the net amount a user is owed (positive) or owes (negative) within one group, derived from the ledger.
- **Settlement** — a recorded payment between two users that zeroes (or partially reduces) a debt.
- **Debt simplification** — a graph-netting algorithm that reassigns who pays whom so the fewest possible payments settle everyone.

**Why this problem matters in interviews**

- It tests ledger modeling (immutable events vs. mutable balances), exact decimal arithmetic, transactional consistency (expense + splits in one write), and a non-trivial algorithm (min-cash-flow / greedy heap netting).
- It is small enough to design end-to-end in 45 minutes yet touches distributed-systems concerns: idempotency on retries, audit trails, and read-model caching.

---

### Functional Requirements

- **Create groups and add members** — a user creates a group (e.g. "Lisbon Trip"), invites members by user id, and can remove members who have no outstanding balance.
- **Add an expense** with an amount, payer, currency, date, optional description, and a split rule — `EQUAL`, `EXACT`, `PERCENTAGE`, or `SHARES` — and the system validates that the splits sum to the total.
- **Edit or delete an expense** — only while no settlement referencing the affected balances has occurred; edits are recorded as new ledger events or guarded versions.
- **Compute simplified balances (who owes whom)** — per-user net balances, pairwise debts, and a minimized settlement plan (fewest transactions) for a group.
- **Record settlements between users** — mark a debt as paid (cash outside the app) with an idempotent write; settlements update balances atomically.
- **Friend-level balances** — view net position with one friend aggregated across all shared groups and non-group expenses.
- **Activity feed** — an audit log of every expense, edit, settlement, and membership change, ordered per group.
- **Multi-currency display (basic)** — store original currency per expense; optionally convert at read time using a stored rate snapshot.

Out of scope for the basic design: in-app payments via bank integrations, receipt scanning/OCR, recurring expenses, comments, and push notifications (noted as extensions).

---

### Non-Functional Requirements

- **Scale**: small groups (friends/roommates/trips), thousands of groups — assume 10M registered users, 2M monthly active users, 5M groups, average 8 members per group, ~40 expenses per group per month.
- **Consistency**: balance calculations must be accurate — strong consistency within a group's ledger; settlement history must never be lost (durable, append-only). Cross-group friend balances may be eventually consistent within a few seconds.
- **Latency**: add expense / view balances < 200ms p99 for the interactive APIs.
- **Availability**: 99.9% for writes, 99.95% for reads (reads can be served from cache/replicas); losing an expense write is worse than rejecting it.
- **Correctness of money math**: all arithmetic in fixed-point decimal (never float); split rounding rules must guarantee `sum(shares) == expense total` exactly.
- **Durability**: ledger events (expenses, splits, settlements) survive instance failure — RPO = 0 via synchronous DB commit plus backups.
- **Auditability**: every mutation produces an immutable activity entry traceable to an actor and a timestamp.
- **Security/privacy**: users see only their own groups and friend balances; financial data encrypted in transit and at rest.

---

### Capacity Estimation

Back-of-envelope numbers to size storage, throughput, and the balance-cache footprint. Assumptions are stated explicitly so they can be re-derived in an interview.

**Step 1 — Users and groups**

- Registered users: 10M; monthly active users (MAU): 2M; daily active users (DAU): ~400K (20% of MAU).
- Groups: 5M total, average 8 members each → 40M group-membership rows.

**Step 2 — Expense write throughput**

- 2M MAU × ~5 expenses/user/month = 10M expenses/month.
- Per second: 10M / (30 × 24 × 3600) ≈ **4 expenses/s average**; with a 20× peak factor (weekends, month-end rent) → **~80 expenses/s peak**.
- Each expense fan-outs to ~8 `expense_shares` rows → ~640 share-rows/s peak. Trivial for a single primary relational DB.

**Step 3 — Read throughput**

- Balance reads dominate: assume 20 reads per write (users open the app to check who owes whom) → **~1,600 reads/s peak** of `GET balances`. This is why balances are cached/materialized rather than recomputed from the raw ledger on every read.

**Step 4 — Storage per year**

- Expense row ≈ 300 B (ids, amount NUMERIC(19,4), currency, FKs, timestamps, description pointer). Shares: 8 × 120 B ≈ 1 KB per expense. Activities + indexes ≈ 1 KB per expense. Total ≈ **2.3 KB per expense**.
- 10M expenses/month × 12 = 120M expenses/year → 120M × 2.3 KB ≈ **276 GB/year** of ledger data. Fits comfortably in one primary with read replicas; partition by `group_id` hash only after multiple terabytes.

**Step 5 — Balance cache footprint**

- Materialized pairwise balances: worst case an 8-member group has 28 pairs; 5M groups × 28 × 80 B ≈ **11 GB** — fits in Redis with room to spare, or simply lives as a `balances` table with a covering index.

**Step 6 — Debt-simplification cost**

- Netting runs over one group's members: 8 nodes, ≤ 28 edges → heap operations are O(E log N) ≈ 28 × 3 ≈ ~84 ops — microseconds. Even a 500-member group is bounded by 499 output payments and runs in < 1 ms. Never a scaling concern; recomputation frequency matters more than the algorithm's cost.

**Key takeaways**

1. This is a **read-heavy, low-QPS, correctness-critical** system — complexity lives in money math and consistency, not in throughput.
2. A single relational primary (PostgreSQL) with read replicas plus a Redis balance cache satisfies all NFRs; sharding is premature at this scale.
3. Storage growth is linear and modest; retention/archival of closed groups can cap hot storage.

---

### Characteristics

Each characteristic shapes the design and is explained with its implication.

- **Ledger-centric (event-sourced flavor)** — Expenses and settlements are immutable ledger events; balances are derived state. Implication: you can always recompute a balance from history, so audits and corrections are safe.
- **Exact decimal arithmetic** — Money uses `NUMERIC`/`BigDecimal` with a fixed scale; IEEE-754 floats are forbidden because `0.1 + 0.2 != 0.3` would silently corrupt balances.
- **Split-sum invariant** — For every expense, `Σ shares == total` must hold exactly; rounding remainder is assigned deterministically (largest remainder, payer-first tie-break) so all nodes/agree on the same split.
- **Group-scoped consistency boundary** — All invariants are per-group, so transactions stay single-aggregate and small; no distributed transactions across groups are needed.
- **Read-heavy and cacheable** — Balances change only on expense/settlement events, so a materialized `balances` table or Redis entry, invalidated/updated in the same transaction, serves the 20:1 read:write ratio.
- **Nettable debt graph** — Debts within a group form a directed weighted graph that can be simplified without changing anyone's net position; this is a presentation-layer optimization, not a ledger change.
- **Idempotent write surface** — Mobile clients retry on flaky networks, so every mutating endpoint accepts a client-generated idempotency key; duplicate retries must be safe.
- **Soft-delete / void semantics** — Financial history is never hard-deleted; expenses are voided with a reversing entry so the audit trail stays complete.
- **Small blast radius per group** — Hot groups (a wedding with 300 guests) are isolated; one group's traffic does not affect others, enabling per-group locking (`SELECT ... FOR UPDATE` on the group row) for serialization.
- **Dual balance views** — Group-level balances (scoped netting) and friend-level balances (cross-group netting) are two projections of the same ledger with different aggregation keys.

---

### Components

Each component lists purpose, responsibilities, how it works, relationships, and a real-world analogue.

#### 1. API Gateway / Edge

- **Purpose:** Single entry point for mobile and web clients.
- **Responsibilities:** TLS termination, JWT authentication, rate limiting per user, request id assignment, routing to services.
- **How it works:** Validates the access token, injects `X-User-Id` and a trace id, enforces token-bucket limits (e.g. 100 req/min/user), forwards to internal services.
- **Relationships:** North-south edge for all services; publishes rate-limit rejections to monitoring.
- **Real-world example:** An AWS API Gateway or Kong fronting Splitwise's REST API.

#### 2. Group Service

- **Purpose:** Owns group lifecycle and membership.
- **Responsibilities:** Create/rename/archive groups, add/remove members (removal blocked when balance ≠ 0), store group settings (simplify-debts toggle).
- **How it works:** Writes to `groups` / `group_members`; removal does a `SELECT ... FOR UPDATE` on the member's balance row and rejects removal when non-zero, so a member in debt can never vanish from a group.
- **Relationships:** Consulted by Expense Service (membership validation) and Balance Service (member list for netting).
- **Real-world example:** Splitwise's group management where "you can't leave until you settle".

#### 3. Expense Service (ledger writer)

- **Purpose:** The write path for expenses — the correctness-critical core.
- **Responsibilities:** Validate split input, compute per-user shares with remainder handling, persist expense + shares atomically, apply idempotency keys, emit activity events.
- **How it works:** In one DB transaction: lock the group row, insert `expenses` (status `ACTIVE`), insert `EXPENSE_SPLITS` computed by the split engine, upsert `idempotency_keys`, insert an `activities` row; then update the materialized balances (or publish an event for the projector).
- **Relationships:** Uses Split Engine, Balance Service/Projector, Activity Service; reads Group Service membership.
- **Real-world example:** Splitwise's "Add expense" — an edit appears instantly in everyone's balances.

#### 4. Split Engine

- **Purpose:** Pure, deterministic split computation.
- **Responsibilities:** Implement `EQUAL`, `EXACT`, `PERCENTAGE`, `SHARES` math with `BigDecimal`; enforce `Σ shares == total`; define rounding-rem remainder assignment (largest-remainder method, deterministic tie-break by user id).
- **How it works:** For EQUAL on $100/3: floor each to $33.33 (total $99.99), distribute the remaining $0.01 to users sorted by (remainder desc, user id asc) — the first user gets $33.34. Same function is used by every layer, guaranteeing agreement.
- **Relationships:** Consumed only by Expense Service (write) and by read-side validators in tests; no DB access.
- **Real-world example:** The shared core library that iOS, Android, and web clients re-implement to show a split preview before submit.

#### 5. Balance Service / Balance Projector

- **Purpose:** Serve fast balance reads and friend-level nets.
- **Responsibilities:** Maintain materialized per-pair balances, compute net per-user balances, answer `GET balances` in < 200ms.
- **How it works:** Two strategies: (a) **synchronous update** in the expense transaction (`UPDATE balances SET amount = amount + ?` upsert), or (b) **asynchronous projector** consuming a ledger event stream and rebuilding read models. Strategy (a) favors read freshness; (b) favors write latency.
- **Relationships:** Reads ledger tables; serves API layer; feeds the Debt Simplifier's input graph.
- **Real-world example:** Splitwise's dashboard that shows "you are owed $45.20" the moment an expense lands.

#### 6. Debt Simplification Engine

- **Purpose:** Minimize the number of settlement transactions within a group.
- **Responsibilities:** Build the net-balance graph for a group and output a minimal payment list (≤ N−1 payments) that zeroes everyone.
- **How it works:** Greedy min-cash-flow: put debtors in a max-heap by owed amount and creditors in a max-heap by owed-to amount; repeatedly match the largest pair, emit a payment of `min(debt, credit)`, reinsert remainders. Produces at most N−1 payments when the graph is connected.
- **Relationships:** Invoked by Balance Service on read (or cached per group version); never mutates the ledger — it is a derived suggestion.
- **Real-world example:** Splitwise's "Simplify group debts" toggle.

#### 7. Settlement Service

- **Purpose:** Record payments between users.
- **Responsibilities:** Validate both parties and group membership, cap or warn on over-settlement, persist settlement idempotently, adjust balances, write the activity entry.
- **How it works:** Same transactional pattern as Expense Service: group lock → insert `settlements` → update balances → insert activity. Over-settlement (paying more than owed) is allowed but flagged so the UI can show "you are now owed the difference".
- **Relationships:** Shares the balances write path with Expense Service; emits events for notifications.
- **Real-world example:** Splitwise's "Settle up" button recording a cash payment made in person.

#### 8. Activity / Audit Service

- **Purpose:** Immutable, ordered history per group and per user.
- **Responsibilities:** Append-only log of expenses, edits, settlements, membership changes; paginated feed reads.
- **How it works:** Every writer inserts an `activities` row in the same transaction as the mutation, so audit can never diverge from state; reads use keyset pagination on `(group_id, id)` descending.
- **Relationships:** Written by Expense, Settlement, Group services; read by clients and by customer-support tooling.
- **Real-world example:** Splitwise's group activity feed ("Priya added 'Taxi' ₹600").

#### 9. Notification Service (optional extension)

- **Purpose:** Tell affected users about new expenses/settlements.
- **Responsibilities:** Fan out push/email on ledger events, respect mute settings, retry with backoff.
- **How it works:** Consumes the activity/ledger event stream via a message queue; sends via FCM/APNs/SMTP; fully asynchronous so it never blocks the 200ms write path.
- **Relationships:** Downstream consumer only — no influence on correctness of balances.
- **Real-world example:** The "Alex added an expense in Goa Trip" push notification.

---

### Patterns

#### Pattern 1: Append-Only Ledger (Event-Sourced Money)

- **What it is:** Store every financial fact (expense, settlement, void) as an immutable event; never update or delete rows that represent money movement.
- **Problem it solves:** Balances must be auditable and recomputation must be possible after bugs or disputes.
- **How it works:** `expenses`, `expense_shares`, and `settlements` are insert-only tables; corrections are new reversing events, not `UPDATE`s.
- **When to use:** Always, for money. Any domain where "what happened" must be provable later.
- **When not to use:** Never skip it for the ledger itself; you may skip full event-sourcing frameworks — plain insert-only tables suffice at this scale.
- **Advantages:** Perfect audit trail; balances are reproducible; simplifies debugging of "why do I owe $12.34?".
- **Disadvantages:** Storage grows unboundedly; reads require either aggregation or a materialized view.

#### Pattern 2: Materialized Balance View (CQRS-lite)

- **What it is:** Maintain a denormalized `balances` table read-optimized for the dashboard, fed by the write-side ledger.
- **Problem it solves:** Recomputing balances from raw ledger rows on every read is O(group history) and violates the < 200ms NFR as groups age.
- **How it works:** In the same transaction that inserts an expense, upsert pair rows: `INSERT ... ON CONFLICT (group_id, debtor, creditor) DO UPDATE SET amount = balances.amount + EXCLUDED.amount`. Version the rows for optimistic concurrency.
- **When to use:** Read:write ratio ≥ ~5:1, or when per-read aggregation cost grows with history.
- **When not to use:** Tiny apps where on-the-fly `SUM()` over a few hundred rows is fast enough and simplicity wins.
- **Advantages:** O(1) balance reads; the original doc's trade-off stands: a denormalized `balances` table trades some write complexity for fast reads.
- **Disadvantages:** Two representations to keep consistent; bugs double-writes (mitigated by same-transaction updates and periodic reconciliation jobs).

#### Pattern 3: Idempotency-Key Writes

- **What it is:** Clients generate a UUID per logical operation; the server stores it and returns the recorded result for duplicate submissions.
- **Problem it solves:** Mobile retries on timeouts would otherwise create duplicate expenses — the worst possible bug in a money app.
- **How it works:** Unique key on `idempotency_keys(key)`; in the write transaction, insert-or-select; on conflict, return the original response body with the original status.
- **When to use:** Every non-GET endpoint that moves money.
- **When not to use:** Pure reads and safely repeatable updates (e.g., rename group).
- **Advantages:** Safe retries; exactly-once semantics at the API level without distributed transactions.
- **Disadvantages:** Extra table and storage; clients must implement key persistence; keys need TTL-based cleanup.

#### Pattern 4: Single-Writer per Group (Aggregate Lock)

- **What it is:** Serialize all mutations of one group through a per-group lock so balance updates never race.
- **Problem it solves:** Two concurrent expenses in the same group both reading balance row X and blind-writing a stale sum.
- **How it works:** `SELECT id FROM groups WHERE id = ? FOR UPDATE` at the start of the expense/settlement transaction; all pair updates then proceed in a canonical (debtor, creditor) order to avoid deadlocks.
- **When to use:** When consistency boundaries are small aggregates — exactly the group here.
- **When not to use:** Cross-group operations (friend netting) — compute those read-side instead of locking many groups.
- **Advantages:** Correct results with simple logic; deadlock-free if lock order is fixed.
- **Disadvantages:** Caps write throughput per group (~hundreds/s — far above the ~80/s global peak), and a hot group can queue writers.

#### Pattern 5: Transactional Outbox (for async consumers)

- **What it is:** Write "event to publish" rows in the same DB transaction as the state change; a relay publishes them to the queue.
- **Problem it solves:** Dual-write problem — you cannot atomically write PostgreSQL and publish to Kafka/SQS.
- **How it works:** An `outbox` table row accompanies the expense insert; a poller/CDC connector publishes and marks it sent; notification and analytics consumers receive at-least-once events.
- **When to use:** Whenever downstream consumers (notifications, search index, analytics) must see every ledger change.
- **When not to use:** If you have no async consumers yet — add it with the first one.
- **Advantages:** No lost events; consumers drive at their own pace.
- **Disadvantages:** At-least-once delivery forces idempotent consumers; relay lag adds seconds of staleness to notifications.

---

### Benefits

- **Correct-by-construction money math** — the ledger + BigDecimal + split-sum invariant make balance disputes answerable with data, not guesses.
- **Minimal settlement friction** — debt simplification cuts a complex IOU web into ≤ N−1 payments, which is the product's core value.
- **Fast, cheap reads** — materialized balances serve the dominant read traffic at O(1) cost without heavy infrastructure.
- **Trust through auditability** — the append-only activity feed lets any member verify how a balance came to be.
- **Graceful growth path** — the design scales from a single PostgreSQL instance to read replicas, Redis caching, and `group_id` hash partitioning without changing the domain model.
- **Safe client behavior** — idempotent APIs tolerate the retries that real mobile networks produce.

---

### Pros

- **Simple, well-understood stack** — relational transactions give ACID where money needs it most.
- **Strong consistency where it matters** — a group ledger is serialized through one lock, eliminating race-induced drift.
- **Recomputable state** — any materialized view can be dropped and rebuilt from the ledger, making recovery cheap.
- **Low operational cost at target scale** — single primary + replicas + optional Redis handles millions of users.
- **Testable core** — split engine and debt simplifier are pure functions, ideal for property-based tests.
- **Clear extension seams** — notifications, OCR receipts, and payments bolt on as event consumers without touching the write path.

---

### Cons

- **Denormalization risk** — ledger vs. balances divergence is possible if any write path bypasses the transactional update; needs reconciliation jobs.
- **Single-primary bottleneck ceiling** — all writes funnel to one primary; fine at this scale, but it is a hard ceiling without sharding.
- **Per-group lock head-of-line blocking** — a burst of concurrent writes in one huge group serializes, adding tail latency.
- **Netting can confuse users** — simplified debts ("you owe Carol, not Alice") require clear UX and an opt-out toggle per group.
- **Multi-currency netting is hard** — a debt graph mixing currencies cannot be netted without picking an FX source and snapshot semantics; the basic design avoids it by netting per-currency only.
- **Idempotency bookkeeping** — extra storage and client complexity that teams often underestimate.

---

### Challenges

- **Technical: exact split rounding** — $100 ÷ 3 has no exact representation in cents; the remainder-distribution rule must be deterministic across all clients or balances drift by cents between platforms.
- **Technical: concurrent edits** — two members editing the same expense simultaneously; last-write-wins silently loses data, so edits need version checks (optimistic locking) or void-and-recreate semantics.
- **Scalability: hot groups** — a 500-member event group concentrates writes on one group lock; mitigation is read-side batching of balance queries and accepting slightly stale nets for display.
- **Scalability: unbounded activity feeds** — a 5-year roommate group accumulates tens of thousands of activities; keyset pagination and archival of closed groups keep reads bounded.
- **Performance: friend-level cross-group netting** — summing a user's position across dozens of groups per read is expensive; it needs its own async projection keyed `(user_a, user_b)`.
- **Performance: serialization round trips** — `BigDecimal` handling in JSON (string vs. number) can silently introduce float parsing on clients; contracts must fix the representation.
- **Reliability: partial failure mid-write** — expense inserted but activity missing corrupts trust; every mutation must be a single DB transaction (or outbox) — never best-effort multi-writes.
- **Reliability: reconciliation drift** — if the materialized `balances` table diverges from the ledger (bug, manual fix, failed deploy), users see wrong numbers; a nightly reconciliation job recomputing balances from the ledger and alerting on deltas is mandatory.
- **Maintainability: split-type explosion** — each new split type (by weight, by income ratio, tiered) multiplies validation and rounding paths; keep the split engine a sealed strategy interface with one rounding-rem implementation.
- **Maintainability of migrations** — changing money column scale (2 → 4 decimals for crypto-ish currencies) requires a full-table rewrite plan; choose `NUMERIC(19,4)` from day one.
- **Operational: time zones and expense dates** — "yesterday's dinner" spans midnight differently for traveling group members; store `expense_date` as a user-supplied calendar date plus UTC `created_at` for ordering.
- **Operational: data residency and deletion** — GDPR deletion requests conflict with append-only financial history; plan crypto-shredding of PII columns while keeping amounts.
- **Security: authorization on every read** — any group member id guess must not leak balances; enforce membership checks in queries (`WHERE group_id IN (SELECT ... memberships)`), not only in controllers.
- **Security: tampering and repudiation** — a payer editing amounts after others settled needs immutable history and edit-attribution so disputes can be resolved.

---

### Best Practices

- **Store money as `NUMERIC(19,4)` and compute with `BigDecimal`** — floats accumulate binary representation error; a single cent drift in a settlement destroys user trust permanently.
- **Enforce the split-sum invariant in the database transaction, not just the controller** — validation-only checks are bypassed by future code paths; a check constraint (`Σ shares` vs. total via trigger or a service-level invariant test) is the last line of defense.
- **Persist the computed shares, not just the split rule** — storing only "EQUAL among 3" makes historical balances change when membership changes; the shares table freezes the truth at write time.
- **Update ledger and balances in one transaction** — anything else creates a window where reads contradict history, which for money is indistinguishable from being hacked.
- **Serialize group writes with a row lock and a fixed update order** — it eliminates an entire class of races for free; the lock is cheap because a group's write rate is tiny.
- **Make every mutating endpoint idempotent with client keys** — retries are a certainty on mobile; exactly-once at the API level is cheaper than a support team resolving duplicates.
- **Version pairs canonically (lower user id = debtor orientation)** — always storing `A owes B` with a sign convention rather than two opposite-direction rows halves the table and removes double-count bugs.
- **Snapshot FX rates at expense creation** — using today's rate for last month's expense rewrites history and confuses settlements; the rate is a fact of the expense.
- **Keep the simplifier pure and derived** — never persist simplified debts as truth; netting is a view, and persisting it makes real payments ambiguous to reconcile.
- **Emit activity rows transactionally and read them with keyset pagination** — `OFFSET` pagination skips/duplicates rows under concurrent inserts, corrupting the audit view users rely on.
- **Write property-based tests for the split engine** — "for random amounts and group sizes, Σ shares == total and no share differs from the ideal by more than one unit" catches rounding regressions that example-based tests miss.
- **Reconcile materialized views nightly against the ledger** — silent drift compounds; an alert on a 1-cent delta lets you fix the bug before users do.

---

### When to Use and When Not to Use

**When to use this design**

- Social finance apps where groups split bills: roommates, trips, dinners, events.
- Any multi-party cost-sharing domain with modest write rates and heavy read dashboards: shared subscriptions, club treasuries, household budgeting.
- Internal tools tracking shared expenses where auditability matters more than throughput (team off-sites, hackathon budgets).

**When not to use this design**

- **Real payment processing** — moving actual money needs PSP integrations, KYC/AML, chargeback handling, and regulatory licensing; this app records obligations, it does not clear funds.
- **High-frequency or merchant-scale ledgers** — thousands of writes/s per account outgrow the single-writer-per-aggregate pattern; look at partitioned ledger databases instead.
- **Multi-currency netting at scale** — FX netting across currencies needs rate-snapshot books and hedging logic; this design nets within a currency only.
- **Anonymous or trustless environments** — the model assumes identified members and human dispute resolution; it has no escrow or smart-contract semantics.

---

### Use Cases

#### Use Case 1: Roommate household expenses

Four roommates log rent ($2,400, EQUAL), utilities (EXACT per usage), and groceries (whoever paid). Monthly, the simplifier collapses ~60 pairwise IOUs into 3 settlements. The group lock is never contended; the activity feed is the shared memory that ends roommate disputes.

#### Use Case 2: Group trip with mixed currencies

Seven friends in Japan log expenses in JPY and a few in USD. Expenses store original currency plus an FX snapshot; netting happens per currency, and the friend-level view shows each user's net converted at display time. Settlements are recorded in the traveler's home currency.

#### Use Case 3: Couple sharing costs without a formal group

Two people use non-group ("friend") expenses. The same ledger tables are used with `group_id = NULL`; friend-level balance nets across everything. This validates the dual-view characteristic: group-scoped netting is just the friend view with an extra aggregation key.

#### Use Case 4: One-off event with unequal shares

A 30-person birthday dinner: the organizer pays, shares weighted by meal tier (SHARES: 2 for drinkers, 1 for non-drinkers). The split engine distributes the per-share remainder deterministically; the simplifier reduces 30 pairwise debts to at most 29 payments — one transfer per guest to the organizer in the common degenerate case, which the max-heap algorithm finds immediately.

#### Use Case 5 (boundary): Freelance collective expense pool

Five freelancers share tooling subscriptions (PERCENTAGE split by agreed ratios) and reconcile quarterly. They rely on the audit feed for tax bookkeeping — illustrating why append-only history and CSV-exportable ledgers are functional requirements, not luxuries, even in a "simple" app.

---

### API Design and Contract

**Conventions**

- **Base URL:** `https://api.splitly.example.com/v1` — the version is in the path (`/v1`); breaking changes ship as `/v2` and run side-by-side.
- **Auth:** `Authorization: Bearer <JWT>` (short-lived access token); the gateway resolves the caller to `X-User-Id` — clients never pass their own user id for identity (only as resource data).
- **Idempotency:** all `POST` endpoints require `Idempotency-Key: <uuid>`; the server stores the key with the response for 24h and replays it on duplicates.
- **Money format:** JSON **strings** for decimals (`"total": "120.50"`) to avoid float parsing; `currency` is ISO-4217.
- **Errors:** RFC 7807 problem JSON: `{ "type", "title", "status", "detail", "code", "traceId" }` with machine codes like `SPLIT_SUM_MISMATCH`.
- **Rate limiting:** token bucket, 100 req/min/user at the gateway; over-limit returns `429` with `Retry-After`.
- **Pagination:** keyset/cursor-based (`?cursor=...&limit=50`), responses carry a `nextCursor`; offset pagination is banned on feeds.
- **Common status codes:** `200/201` success, `400` validation, `401` unauthenticated, `403` not a group member, `404` unknown resource, `409` concurrency/duplicate conflict, `422` business-rule violation, `429` rate limited, `500` server error.

**Endpoint summary** (the original minimal surface, kept and formalized)

| Method & path | Purpose |
|---|---|
| `POST /v1/groups` | Create a group — body `{ name, memberIds[] }` |
| `POST /v1/groups/{groupId}/expenses` | Add an expense — `{ amount, paidBy, splitType, splits[] }` |
| `GET /v1/groups/{groupId}/balances` | Net balances + simplified payment plan |
| `POST /v1/groups/{groupId}/settlements` | Record a settlement — `{ fromUser, toUser, amount }` |
| `GET /v1/groups/{groupId}/expenses` | List expenses (cursor pagination, filters) |
| `GET /v1/groups/{groupId}/activities` | Activity feed (cursor pagination) |
| `GET /v1/users/me/friends/{userId}/balance` | Friend-level net balance across groups |

#### POST /v1/groups — create a group

```http
POST /v1/groups HTTP/1.1
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
Idempotency-Key: 9b3f2c0a-6e0a-4e7c-a1ad-3e5f6a7b8c9d
Content-Type: application/json

{ "name": "Lisbon Trip 2026", "memberIds": ["u_anna", "u_bob", "u_carol"] }
```

```http
HTTP/1.1 201 Created
Location: /v1/groups/g_01JZQ4K7

{ "id": "g_01JZQ4K7", "name": "Lisbon Trip 2026", "members": ["u_anna", "u_bob", "u_carol", "u_me"], "createdAt": "2026-03-14T10:22:31Z" }
```

**Validation:** `name` 1–120 chars (required); `memberIds` ≤ 500, each must exist; creator auto-added. Errors: `400 VALIDATION_FAILED` with `fieldErrors[]`, `409 DUPLICATE_IDEMPOTENCY_KEY` only when the key was used with a *different* payload (same payload replays the stored `201`).

#### POST /v1/groups/{groupId}/expenses — add an expense

```http
POST /v1/groups/g_01JZQ4K7/expenses HTTP/1.1
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
Idempotency-Key: f47ac10b-58cc-4372-a567-0e02b2c3d479
Content-Type: application/json

{
  "description": "Dinner at Ramiro",
  "total": "120.50",
  "currency": "EUR",
  "paidBy": "u_anna",
  "expenseDate": "2026-03-14",
  "splitType": "EXACT",
  "splits": [
    { "userId": "u_anna", "amount": "40.00" },
    { "userId": "u_bob",  "amount": "50.50" },
    { "userId": "u_carol","amount": "30.00" }
  ]
}
```

```http
HTTP/1.1 201 Created

{
  "id": "e_01JZR9M2",
  "groupId": "g_01JZQ4K7",
  "total": "120.50",
  "currency": "EUR",
  "paidBy": "u_anna",
  "splitType": "EXACT",
  "shares": [
    { "userId": "u_anna", "share": "40.00" },
    { "userId": "u_bob",  "share": "50.50" },
    { "userId": "u_carol","share": "30.00" }
  ],
  "createdAt": "2026-03-14T10:31:02Z"
}
```

**Validation and errors:** `total` > 0, scale ≤ 4; `currency` supported ISO code; `paidBy` and every `splits.userId` must be current group members; for `EXACT`, `Σ splits.amount == total` else `422 SPLIT_SUM_MISMATCH`; for `EQUAL`, omit amounts and the server computes them (`splits` = participant list, or default all members); for `PERCENTAGE`, percentages must sum to `100.0000`; unknown `splitType` → `400`. Response echoes the **server-computed authoritative shares** — for `EQUAL` this is how clients learn remainder assignment.

#### GET /v1/groups/{groupId}/balances — balances + simplified plan

```http
GET /v1/groups/g_01JZQ4K7/balances?simplify=true HTTP/1.1
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
```

```http
HTTP/1.1 200 OK
Content-Type: application/json
ETag: "v-8821"

{
  "groupId": "g_01JZQ4K7",
  "currency": "EUR",
  "netBalances": [
    { "userId": "u_anna",  "net": "75.50" },
    { "userId": "u_bob",   "net": "-45.00" },
    { "userId": "u_carol", "net": "-30.50" }
  ],
  "simplifiedPayments": [
    { "from": "u_bob",   "to": "u_anna", "amount": "45.00" },
    { "from": "u_carol", "to": "u_anna", "amount": "30.50" }
  ],
  "asOfVersion": 8821
}
```

Positive `net` = is owed. `simplify=false` returns raw pairwise debts instead. `asOfVersion` is the group ledger version — a client can poll with `If-None-Match` for cheap `304` freshness checks.

#### POST /v1/groups/{groupId}/settlements — record a payment

```http
POST /v1/groups/g_01JZQ4K7/settlements HTTP/1.1
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
Idempotency-Key: 7c9e6679-7425-40de-944b-e07fc1f90ae7

{ "fromUser": "u_bob", "toUser": "u_anna", "amount": "45.00", "currency": "EUR" }
```

```http
HTTP/1.1 201 Created

{ "id": "s_01JZSK1A", "status": "RECORDED", "fromUser": "u_bob", "toUser": "u_anna", "amount": "45.00", "remainingDebt": "0.00", "createdAt": "2026-03-15T09:05:11Z" }
```

Over-payment returns `201` with `status: "OVERPAID"` and the new inverted balance; both users must be members (`403 FORBIDDEN_MEMBER` otherwise).

#### GET /v1/groups/{groupId}/expenses — list with pagination, filtering, sorting

```http
GET /v1/groups/g_01JZQ4K7/expenses?cursor=eyJpZCI6ImVfMDFKWiJ9&limit=20&paidBy=u_anna&from=2026-03-01&to=2026-03-31&sort=-expenseDate HTTP/1.1
```

```json
{
  "data": [
    { "id": "e_01JZR9M2", "description": "Dinner at Ramiro", "total": "120.50", "currency": "EUR", "paidBy": "u_anna", "expenseDate": "2026-03-14" }
  ],
  "nextCursor": "eyJpZCI6ImVfMDFKWSJ9",
  "hasMore": true
}
```

**Contract notes:** filters combine with AND; `sort` whitelist = `expenseDate`, `total`, `createdAt`, prefix `-` for descending; `limit` default 20, max 100. The cursor is an opaque base64 token of the last row's sort key + id — stable under concurrent inserts, unlike offsets.

#### Contract guarantees (interview-ready summary)

1. **Idempotent `POST`s:** replaying with the same key returns the original response; the same key with a different body yields `409`.
2. **Monotonic group version:** every mutation bumps `group_version`; balance responses carry it, enabling optimistic UI refresh and `304` caching.
3. **Authorization in data plane:** group endpoints verify membership inside the query layer.
4. **Backward compatibility:** additive-only field changes within `/v1`; removing/renaming fields requires `/v2`.

---

### Data Modeling

The logical schema (kept from the original design, now formalized):

```
users:          id (PK), email, name
groups:         id (PK), name, version, created_at
group_members:  group_id (FK), user_id (FK), joined_at
expenses:       id (PK), group_id (FK, nullable), amount, currency, paid_by, split_type, expense_date, created_at
expense_splits: expense_id (FK), user_id (FK), share_amount
settlements:    id (PK), group_id (FK), from_user, to_user, amount, currency, created_at
balances:       group_id, debtor_id, creditor_id, amount, version          (materialized pair balances)
activities:     id (PK), group_id, actor_id, type, payload_json, created_at (append-only feed)
idempotency_keys: key (PK), user_id, request_hash, response_json, created_at
```

```mermaid
erDiagram
    USERS ||--o{ GROUP_MEMBERS : "joins"
    GROUPS ||--o{ GROUP_MEMBERS : "has"
    GROUPS ||--o{ EXPENSES : "contains"
    USERS ||--o{ EXPENSES : "pays"
    EXPENSES ||--o{ EXPENSE_SPLITS : "split into"
    USERS ||--o{ EXPENSE_SPLITS : "owes"
    GROUPS ||--o{ SETTLEMENTS : "settles in"
    GROUPS ||--o{ BALANCES : "materialized pairs"
    GROUPS ||--o{ ACTIVITIES : "audited by"
    USERS ||--o{ IDEMPOTENCY_KEYS : "retries with"

    USERS {
        uuid id PK
        string email
        string name
    }
    GROUPS {
        uuid id PK
        string name
        bigint version
        timestamptz created_at
    }
    GROUP_MEMBERS {
        uuid group_id FK
        uuid user_id FK
        timestamptz joined_at
    }
    EXPENSES {
        uuid id PK
        uuid group_id FK "nullable for friend expenses"
        numeric amount "NUMERIC(19,4)"
        char currency "ISO-4217"
        uuid paid_by FK
        string split_type "EQUAL|EXACT|PERCENTAGE|SHARES"
        date expense_date
        timestamptz created_at
    }
    EXPENSE_SPLITS {
        uuid expense_id FK
        uuid user_id FK
        numeric share_amount "NUMERIC(19,4)"
    }
    SETTLEMENTS {
        uuid id PK
        uuid group_id FK
        uuid from_user FK
        uuid to_user FK
        numeric amount
        char currency
        timestamptz created_at
    }
    BALANCES {
        uuid group_id FK
        uuid debtor_id FK
        uuid creditor_id FK
        numeric amount
        bigint version
    }
    ACTIVITIES {
        bigint id PK "monotonic, keyset cursor"
        uuid group_id FK
        uuid actor_id FK
        string type
        jsonb payload
        timestamptz created_at
    }
    IDEMPOTENCY_KEYS {
        string key PK
        uuid user_id FK
        string request_hash
        jsonb response
        timestamptz created_at
    }
```

**Design notes**

- Every expense is stored as **ledger entries (`expense_splits`)** rather than only pre-aggregated balances; the materialized `balances` table is a derived projection updated in the same transaction (or rebuilt on read for tiny groups).
- `BALANCES` rows use a **canonical pair orientation**: `debtor_id < creditor_id` by id order, with signed `amount` — one row per ordered pair, never two.
- `GROUPS.version` increments on every mutation; it drives ETags and detects concurrent edits (`UPDATE ... SET version = version + 1 WHERE version = ?`).
- Key indexes: `expense_splits (expense_id)`, `expenses (group_id, created_at DESC)`, `balances (group_id, debtor_id)`, `activities (group_id, id DESC)` for keyset pagination, unique `idempotency_keys(key)`.
- Non-group (friend) expenses use `group_id = NULL` and net into friend-level projections instead of a group balance.

---

### High-Level Design

```mermaid
flowchart LR
    Client["Mobile / Web Client"] --> API["API Gateway: auth, rate limit, idempotency check"]
    API --> ExpenseService["Expense Service (ledger write path)"]
    API --> BalanceService["Balance Service (read path)"]
    API --> GroupService["Group Service"]
    API --> SettlementService["Settlement Service"]
    ExpenseService --> Split["Split Engine: EQUAL/EXACT/PCT/SHARES + rounding"]
    ExpenseService --> DB[("PostgreSQL primary: ledger + balances (tx)")]
    SettlementService --> DB
    GroupService --> DB
    ExpenseService --> Outbox["Outbox table -> relay"]
    Outbox --> MQ["Message Queue"]
    MQ --> Notify["Notification Service"]
    MQ --> FriendProj["Friend-balance projector"]
    BalanceService --> Cache[("Redis: balances + simplified plan per group version")]
    BalanceService --> Replica[("Read replica")]
    BalanceService --> Simplify["Debt Simplifier: max-heap min-cash-flow"]
    DB --> Replica
```

**Explanation**

Clients hit the gateway, which authenticates, rate limits, and resolves idempotency keys before routing. Writes (expenses, settlements) go through the Expense/Settlement services, which lock the group row, compute shares with the pure Split Engine, and commit ledger rows, balance upserts, an activity row, and an outbox row in **one PostgreSQL transaction** — so state, audit, and events can never diverge. The outbox relay publishes to the queue; asynchronous consumers (notifications, the friend-balance projector) follow. Reads are served by the Balance Service from Redis (keyed by `group_id:version`) or a read replica, with the Debt Simplifier computing the minimal payment plan on demand. This preserves the original architecture — a thin API layer over expense and balance services on a relational DB — while making the consistency story concrete.

#### Write path: adding an expense

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant G as API Gateway
    participant E as Expense Service
    participant S as Split Engine
    participant D as PostgreSQL
    participant O as Outbox Relay
    participant Q as Queue

    C->>G: POST /v1/groups/g1/expenses (Idempotency-Key: k)
    G->>G: Verify JWT, rate limit, lookup idempotency key k
    alt key k already processed
        G-->>C: 201 + stored response (replay)
    else new request
        G->>E: Forward with X-User-Id
        E->>E: Validate members, split inputs
        E->>S: computeShares(total, splitType, splits)
        S-->>E: shares (sum == total, exact decimals)
        E->>D: BEGIN; lock group row FOR UPDATE
        E->>D: INSERT expenses + expense_shares + idempotency_keys + activities + outbox
        E->>D: UPSERT balances (canonical pairs), bump group version
        D-->>E: COMMIT
        E-->>C: 201 Created (expense + authoritative shares)
        O->>D: Poll outbox rows
        O->>Q: Publish ExpenseCreated event (at-least-once)
        Q-->>Notify: Fan out notification
    end
```

**Explanation**

Steps 1–3 make the request safe to retry end to end. Steps 5–6 keep math pure and deterministic: the engine gets validated inputs and returns shares whose sum equals the total exactly. Steps 7–9 are the correctness core: one transaction covers the ledger, the idempotency record, the audit row, the read-model upsert, and the version bump — there is no interleaving where a balance exists without its ledger entry or vice versa. Steps 10–12 move all unreliable side effects (notifications) behind the commit boundary via the outbox.

#### Read path: viewing balances

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant G as API Gateway
    participant B as Balance Service
    participant R as Redis
    participant X as Debt Simplifier
    participant DB as Read Replica

    C->>G: GET /v1/groups/g1/balances?simplify=true
    G->>B: Forward (X-User-Id)
    B->>DB: Authorize: is caller a member of g1?
    B->>R: GET balances:g1:<version>
    alt cache hit
        R-->>B: pairwise balances
    else miss
        B->>DB: SELECT balances WHERE group_id=g1
        B->>R: SET balances:g1:<version> (TTL 5m)
    end
    B->>X: netAndSimplify(pairwise)
    X-->>B: netBalances + minimal payment plan (<= N-1 payments)
    B-->>C: 200 OK (ETag: v-<version>)
```

**Explanation**

Balance reads never touch the write primary. The cache key includes the group version, so **any write automatically invalidates the old entry** — no invalidation race, no stale-after-write windows beyond replica lag. The simplifier runs on read against already-materialized pair balances (≤ a few hundred rows for even the largest realistic groups), so the expensive part of the system is O(group size), not O(group history).

---

### Deep Dive

#### Debt Simplification (Min-Cash-Flow) Algorithm

The most interesting algorithmic problem in this system: given a set of pairwise balances within a group, compute a **minimal set of settlement transactions** that zeroes everyone out.

**Step 1 — net positions.** Collapse all pairwise debts into one net number per person: `net(u) = total u is owed − total u owes`. The nets always sum to zero. Anyone with `net = 0` is already settled.

**Step 2 — greedy matching.** Repeatedly pair the largest creditor with the largest debtor, settle `min(credit, debit)` between them, and reinsert the remainder. A max-heap (or two heaps: creditors and debtors) makes each step O(log n):

```
while creditors not empty:
    c = max creditor, d = max debtor
    pay = min(c.amount, d.amount)
    emit transaction: d pays c `pay`
    c.amount -= pay; d.amount -= pay
    reinsert whichever is still non-zero
```

**Properties worth knowing for interviews:**

- At most `n − 1` transactions for `n` non-zero members (each transaction settles at least one party completely).
- The greedy result is *a* minimal-count solution in practice; the true minimum-transaction problem is NP-hard in general (it reduces to subset-sum style partitioning), but greedy is optimal in the common cases and always within a small factor. For a consumer app, greedy is the right call — deterministic, fast, explainable to users.
- Total money moved is minimized only in count, not in volume; the sum of settled amounts is fixed by the nets.

**When to simplify.** Run simplification **on read** (when a user opens "simplify debts" view) rather than storing simplified balances — the raw pairwise ledger stays the source of truth, and simplification is a pure function of it. This avoids an entire class of consistency bugs where simplified state drifts from the ledger.

#### Rounding and Money Representation

- Store amounts as `NUMERIC(19,4)` / `BigDecimal` — never `double`. A `double` accumulates representation error (`0.1 + 0.2 ≠ 0.3`) which surfaces as groups that "never quite settle".
- Equal splits rarely divide evenly: $100 ÷ 3 = $33.33, $33.33, $33.34. Assign the **remainder cents to the payer** (or rotate the remainder recipient deterministically by user id) so splits always sum exactly to the expense total. Document the rule — users *will* audit it.
- Round half-up at the final share computation only; keep full precision internally until then.
- Multi-currency groups: store the original currency per expense and convert at a recorded FX rate for balance display. Never silently mix currencies in one balance.

#### Concurrency on Balance Updates

Two users adding expenses to the same group concurrently must not corrupt the materialized `balances` rows. Options, in increasing order of strictness:

1. **Atomic upsert**: `INSERT ... ON CONFLICT (group_id, debtor_id, creditor_id) DO UPDATE SET amount = balances.amount + EXCLUDED.amount` — single statement, no read-modify-write race. This is the default choice.
2. **Optimistic locking** on the `groups.version` column: retry the whole expense transaction on version conflict. Simple, but hot groups see retries.
3. **Pessimistic lock** on the group row (`SELECT ... FOR UPDATE`): serializes all writes per group. Correct but limits per-group throughput — acceptable here because a single group's write rate is inherently tiny (humans typing expenses).

The atomic upsert wins because balance deltas are commutative — order doesn't matter, so no serialization is needed at all.

#### Idempotent Expense Creation

Mobile clients retry on flaky networks. Without protection, a retried "Add dinner $60" creates two expenses. The design uses the `idempotency_keys` table: the client generates a UUID per user intent, the server does `INSERT INTO idempotency_keys ... ON CONFLICT DO NOTHING` inside the same transaction as the expense insert, and returns the stored response if the key already exists. The key must be scoped per user and expire (e.g. 24h TTL cleanup job) to bound table growth.

---

### Java and Spring Boot Implementation Guide

The examples below follow the production shape: controllers are thin, services hold the business logic as Spring beans, configuration is externalized with `@Value`, and money is always `BigDecimal`.

#### Domain Entity (JPA)

```java
@Entity
@Table(name = "expenses")
public class Expense {

    @Id
    private UUID id;

    @Column(name = "group_id")
    private UUID groupId;              // nullable: friend-to-friend expense

    @Column(nullable = false, precision = 19, scale = 4)
    private BigDecimal amount;

    @Column(nullable = false, length = 3)
    private String currency;           // ISO-4217, e.g. "USD"

    @Column(name = "paid_by", nullable = false)
    private UUID paidBy;

    @Enumerated(EnumType.STRING)
    @Column(name = "split_type", nullable = false)
    private SplitType splitType;       // EQUAL, EXACT, PERCENTAGE, SHARES

    @Column(name = "expense_date", nullable = false)
    private LocalDate expenseDate;

    @Column(name = "created_at", nullable = false)
    private Instant createdAt;

    protected Expense() {}             // JPA

    // getters, builder-style factory omitted for brevity
}
```

The entity maps the schema 1:1. Note `precision = 19, scale = 4` matching `NUMERIC(19,4)` — the mapping must agree with the DDL or rounding behavior diverges between app and database.

#### Split Calculation Service

```java
@Service
public class SplitCalculator {

    private final RoundingMode rounding;

    public SplitCalculator(@Value("${app.money.rounding:HALF_UP}") RoundingMode rounding) {
        this.rounding = rounding;
    }

    /** Splits {@code total} among {@code members}; remainder cents go to the payer. */
    public Map<UUID, BigDecimal> equalSplit(BigDecimal total, List<UUID> members, UUID payer) {
        int scale = total.scale() >= 2 ? total.scale() : 2;
        BigDecimal share = total.divide(BigDecimal.valueOf(members.size()), scale, rounding);

        Map<UUID, BigDecimal> result = new LinkedHashMap<>();
        BigDecimal assigned = BigDecimal.ZERO;
        for (UUID member : members) {
            result.put(member, share);
            assigned = assigned.add(share);
        }
        // Give the leftover cents to the payer so shares sum exactly to total.
        BigDecimal remainder = total.subtract(assigned);
        if (remainder.signum() != 0) {
            result.merge(payer, remainder, BigDecimal::add);
        }
        return result;
    }
}
```

Why a `@Service` and not a static utility: the rounding mode and scale policy are deployment configuration (a fintech deployment may mandate `HALF_EVEN`), so they arrive via `@Value` and the bean is unit-testable with different policies.

#### Debt Simplification Service

```java
@Service
public class DebtSimplifier {

    public record Settlement(UUID from, UUID to, BigDecimal amount) {}

    /** Greedy min-cash-flow over net positions. At most n-1 transactions. */
    public List<Settlement> simplify(Map<UUID, BigDecimal> netBalances) {
        record Entry(UUID user, BigDecimal amount) {}

        PriorityQueue<Entry> creditors = new PriorityQueue<>(
                (a, b) -> b.amount().compareTo(a.amount()));
        PriorityQueue<Entry> debtors = new PriorityQueue<>(
                (a, b) -> b.amount().compareTo(a.amount()));

        netBalances.forEach((user, net) -> {
            if (net.signum() > 0) creditors.add(new Entry(user, net));
            else if (net.signum() < 0) debtors.add(new Entry(user, net.negate()));
        });

        List<Settlement> result = new ArrayList<>();
        while (!creditors.isEmpty() && !debtors.isEmpty()) {
            Entry creditor = creditors.poll();
            Entry debtor = debtors.poll();
            BigDecimal pay = creditor.amount().min(debtor.amount());
            result.add(new Settlement(debtor.user(), creditor.user(), pay));

            BigDecimal creditLeft = creditor.amount().subtract(pay);
            BigDecimal debtLeft = debtor.amount().subtract(pay);
            if (creditLeft.signum() > 0) creditors.add(new Entry(creditor.user(), creditLeft));
            if (debtLeft.signum() > 0) debtors.add(new Entry(debtor.user(), debtLeft));
        }
        return result;
    }
}
```

Two heaps give O(n log n) overall. The method is a pure function of the materialized pair balances — it runs on read, never mutates the ledger, which is exactly the design decision explained in the Deep Dive.

#### Atomic Balance Update (Repository)

```java
public interface BalanceRepository extends JpaRepository<PairBalance, PairBalanceId> {

    @Modifying
    @Query(value = """
            INSERT INTO balances (group_id, debtor_id, creditor_id, amount, version)
            VALUES (:groupId, :debtor, :creditor, :delta, 1)
            ON CONFLICT (group_id, debtor_id, creditor_id)
            DO UPDATE SET amount = balances.amount + EXCLUDED.amount,
                          version = balances.version + 1
            """, nativeQuery = true)
    void addDelta(UUID groupId, UUID debtor, UUID creditor, BigDecimal delta);
}
```

The upsert makes concurrent expense writes safe without any application-level locking, because balance deltas commute.

#### Expense Creation with Idempotency (Service + Controller)

```java
@Service
public class ExpenseService {

    private final ExpenseRepository expenses;
    private final BalanceRepository balances;
    private final IdempotencyKeyRepository idempotency;
    private final SplitCalculator splitCalculator;
    private final int idempotencyTtlHours;

    public ExpenseService(ExpenseRepository expenses,
                          BalanceRepository balances,
                          IdempotencyKeyRepository idempotency,
                          SplitCalculator splitCalculator,
                          @Value("${app.idempotency.ttl-hours:24}") int idempotencyTtlHours) {
        this.expenses = expenses;
        this.balances = balances;
        this.idempotency = idempotency;
        this.splitCalculator = splitCalculator;
        this.idempotencyTtlHours = idempotencyTtlHours;
    }

    @Transactional
    public ExpenseResponse createExpense(UUID userId, String idempotencyKey, CreateExpenseRequest req) {
        return idempotency.findResponse(userId, idempotencyKey)
                .orElseGet(() -> doCreate(userId, idempotencyKey, req));
    }

    private ExpenseResponse doCreate(UUID userId, String key, CreateExpenseRequest req) {
        Map<UUID, BigDecimal> shares = switch (req.splitType()) {
            case EQUAL -> splitCalculator.equalSplit(req.amount(), req.memberIds(), req.paidBy());
            case EXACT -> req.exactShares();
            default -> throw new UnsupportedOperationException("handled similarly");
        };
        Expense saved = expenses.save(Expense.create(req, shares));
        shares.forEach((debtor, share) -> {
            if (!debtor.equals(req.paidBy())) {
                balances.addDelta(req.groupId(), debtor, req.paidBy(), share);
            }
        });
        ExpenseResponse response = ExpenseResponse.from(saved, shares);
        idempotency.store(userId, key, response, Duration.ofHours(idempotencyTtlHours));
        return response;
    }
}
```

```java
@RestController
@RequestMapping("/api/v1/groups/{groupId}/expenses")
@Validated
public class ExpenseController {

    private final ExpenseService expenseService;

    public ExpenseController(ExpenseService expenseService) {
        this.expenseService = expenseService;
    }

    @PostMapping
    public ResponseEntity<ExpenseResponse> create(
            @PathVariable UUID groupId,
            @RequestHeader("Idempotency-Key") String idempotencyKey,
            @RequestAttribute("userId") UUID userId,
            @Valid @RequestBody CreateExpenseRequest request) {
        ExpenseResponse created = expenseService.createExpense(userId, idempotencyKey, request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
}
```

The whole creation — expense row, share rows, balance deltas, idempotency record — commits in **one transaction**, so a crash mid-way cannot leave a half-recorded expense. The `Idempotency-Key` header pattern mirrors what Stripe popularized.

#### Request Validation and Error Handling

```java
public record CreateExpenseRequest(
        @NotNull UUID groupId,
        @NotNull UUID paidBy,
        @NotNull @DecimalMin(value = "0.01") @Digits(integer = 15, fraction = 4) BigDecimal amount,
        @NotBlank @Size(min = 3, max = 3) String currency,
        @NotNull SplitType splitType,
        @NotEmpty List<UUID> memberIds,
        Map<UUID, BigDecimal> exactShares,     // required only for EXACT
        @NotNull @PastOrPresent LocalDate expenseDate) {}
```

```java
@RestControllerAdvice
public class ApiExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ApiError> validation(MethodArgumentNotValidException ex) {
        List<String> details = ex.getBindingResult().getFieldErrors().stream()
                .map(fe -> fe.getField() + ": " + fe.getDefaultMessage())
                .toList();
        return ResponseEntity.badRequest()
                .body(new ApiError("VALIDATION_FAILED", "Request validation failed", details));
    }

    @ExceptionHandler(GroupNotFoundException.class)
    public ResponseEntity<ApiError> notFound(GroupNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(new ApiError("GROUP_NOT_FOUND", ex.getMessage(), List.of()));
    }
}
```

A consistent error envelope (`code`, `message`, `details`) is what mobile clients key off — never leak stack traces or per-endpoint ad-hoc shapes.

---

### Interview Questions and Answers

**Beginner**

- **Q: How do you represent money in this system?**
  **A:** `BigDecimal` in Java, `NUMERIC(19,4)` in PostgreSQL, never floating point. Floating point cannot represent most decimal fractions exactly, so balances drift by fractions of a cent and groups never settle cleanly. Follow-up: *what rounding mode?* — half-up at the final share computation, full precision internally, and a documented rule for remainder cents (assigned to the payer).

- **Q: What tables do you need at minimum?**
  **A:** `users`, `groups`, `group_members`, `expenses`, `expense_splits`, and `settlements`. Everything else (materialized balances, activities, idempotency keys) is an optimization or operational concern layered on top.

- **Q: How does an equal split of $100 among 3 people work?**
  **A:** Two members get $33.33 and one gets $33.34 — the shares must sum exactly to the expense total. The remainder goes to a deterministic recipient (e.g. the payer) so the rule is explainable and reproducible.

**Intermediate**

- **Q: How do you compute "who owes whom" for a group?**
  **A:** Two levels. Raw level: each expense creates pairwise debts between the payer and each participant (`expense_splits`). Materialized level: an upsert-maintained `balances` table holds the net pairwise amount per (group, debtor, creditor), so reading balances is O(pairs) instead of scanning all expenses. The raw splits remain the source of truth; the materialized table can always be rebuilt from them.

- **Q: How do you prevent a retried API call from creating a duplicate expense?**
  **A:** Client sends an `Idempotency-Key` header (a UUID generated per user action). Server stores the key with the response inside the same transaction as the expense insert; a retry with the same key returns the stored response instead of re-executing. Keys are per-user and expire after ~24h. Follow-up: *why not just a unique constraint on (user, amount, date)?* — because two legitimately identical expenses ("coffee $4" twice in a day) are valid; only the client can distinguish intent, hence the client-generated key.

- **Q: Two users add expenses to the same group at the same time — what breaks and how do you fix it?**
  **A:** A naive read-modify-write on the balance row loses one update (classic lost-update race). Fix with an atomic upsert (`INSERT ... ON CONFLICT DO UPDATE SET amount = amount + delta`) since deltas commute; alternatives are optimistic locking with retry or `SELECT FOR UPDATE` on the group row, both correct but with worse contention behavior.

**Advanced**

- **Q: Explain the debt simplification algorithm and its complexity.**
  **A:** Compute net positions per member (owed minus owing; they sum to zero), then greedily match the largest creditor with the largest debtor using two heaps, settling `min(credit, debit)` per step. O(n log n) time, at most n−1 transactions. Expected discussion: the exact minimum-transaction problem is NP-hard, greedy is the pragmatic choice; simplification runs on read over the materialized balances so the ledger is never rewritten. Common mistake: trying to store simplified balances as the source of truth, which then drifts from the raw ledger on every edit/delete.

- **Q: How do you handle editing or deleting an expense that people have already settled against?**
  **A:** Never mutate history destructively. Model edits as compensating entries (a reversal plus a new expense) so the activity feed and balances stay auditable — the same reason accounting systems use reversing entries. If settlements already happened, the compensating entries naturally produce new residual balances. Trade-off: more rows, but a correct audit trail; the alternative (in-place mutation) makes "what did the balance look like last Tuesday?" unanswerable.

- **Q: How would you scale the balance read path for a group with thousands of members?**
  **A:** Cache the computed balance view keyed by `(group_id, version)`; any write bumps the version, so stale reads are impossible by construction. Reads hit the cache or a read replica, never the write primary. The simplifier itself is O(members log members) on a few thousand rows — milliseconds — so no precomputation is needed.

**Senior / System Design**

- **Q: Design the activity feed. What are the consistency requirements?**
  **A:** Append-only `activities` table written in the same transaction as the business change (or via the transactional outbox if the feed is a separate service). Keyset pagination on a monotonic id — offset pagination skips/duplicates rows under concurrent inserts. Consistency requirement is causal: a user must never see a balance change without the activity that explains it, which the single-transaction write guarantees.

- **Q: Splitwise needs to work offline on mobile. How does that change the design?**
  **A:** The client queues mutations locally with client-generated ids and idempotency keys, then syncs when online. The server treats sync as idempotent creates (the key dedupes) and resolves conflicts last-writer-wins per expense with the activity feed preserving full history. Discussion points: clock skew on `expense_date` (client timestamp is data, server timestamp is truth for ordering), and why CRDTs are overkill here — expenses are independent records, not shared mutable state.

- **Q: What would you do differently at 100M users?**
  **A:** The data model survives; the infrastructure changes. Shard by `group_id` (group is the natural unit of locality — a group's data lives on one shard), move the activity feed to a log (Kafka) with per-group partitions, serve balance reads from Redis with version-stamped keys, and push idempotency checks to a Redis SETNX with TTL in front of the DB. The invariants — atomic upserts, idempotent writes, ledger as source of truth — are exactly what make that scaling path possible without redesign.

- **Q: What are the most common mistakes candidates make on this problem?**
  **A:** (1) Using `double` for money. (2) Storing only simplified balances and losing the raw ledger. (3) Ignoring idempotency on expense creation. (4) Read-modify-write balance updates without atomicity. (5) Offset-paginating the activity feed. (6) Forgetting that equal splits need a remainder rule. Each is a small detail that signals whether the candidate has built money-touching systems.

---
