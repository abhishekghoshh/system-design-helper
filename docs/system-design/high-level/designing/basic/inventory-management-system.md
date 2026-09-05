# Design a Basic Inventory Management System

## Blogs and websites

## Medium

## Youtube

## Theory

### Topics Covered

1. [Introduction / Problem Statement](#introduction-problem-statement)
2. [Functional Requirements](#functional-requirements)
3. [Non-Functional Requirements](#non-functional-requirements)
4. [Capacity Estimation](#capacity-estimation)
5. [Characteristics](#characteristics)
6. [Components](#components)
7. [Architectural Patterns](#architectural-patterns)
8. [Benefits](#benefits)
9. [Pros](#pros)
10. [Cons](#cons)
11. [Challenges](#challenges)
12. [Best Practices](#best-practices)
13. [When to Use / When Not to Use](#when-to-use-when-not-to-use)
14. [Use Cases](#use-cases)
15. [Data Model and APIAPI Design](#data-model-and-apiapi-design)
16. [High-Level Design](#high-level-design)
17. [Deep Dive](#deep-dive)
18. [Replication Strategies](#replication-strategies)
19. [Failure Detection and Membership](#failure-detection-and-membership)
20. [High Availability and Scalability](#high-availability-and-scalability)
21. [Performance and Optimization](#performance-and-optimization)
22. [Encryption and Key Management](#encryption-and-key-management)
23. [Authentication and Authorization](#authentication-and-authorization)
24. [Security Threats and Mitigations](#security-threats-and-mitigations)
25. [Observability and Logging](#observability-and-logging)
26. [Real-World Implementations](#real-world-implementations)
27. [Java and Spring Boot Implementation Guide](#java-and-spring-boot-implementation-guide)
28. [Interview Questions and Answers](#interview-questions-and-answers)

---
---
---

### Introduction / Problem Statement

Design a basic inventory management system for a single warehouse/store that tracks stock levels for products, supports stock in/out operations, and alerts when items run low.

An inventory system is the canonical "counter under concurrency" problem. The data volumes are modest and the CRUD is trivial; the design value lives in three places: (1) **correctness of a shared counter** — the same SKU is decremented by many concurrent sales, and the system must never sell stock it does not have (overselling) nor lose stock it does have (phantom decrements); (2) **auditability** — every unit that enters or leaves must be traceable to a reason, an actor, and a reference (order, purchase order, adjustment), because inventory discrepancies are discovered weeks later during cycle counts and must be explainable; and (3) **time- and threshold-driven behavior** — low-stock alerts, reservation expiries, and reorder triggers fire without any user request.

**Why this problem exists**

- Physical stock is finite and shared across channels (storefront, web, wholesale); without a single system of record, each channel oversells the others.
- Money and goods move together: a stock-out that is not recorded is either theft, damage, or a receiving error — the ledger is how you tell which.
- Customers tolerate "out of stock" but not "you charged me and then cancelled"; overselling is a trust-destroying failure, so availability must be strongly consistent at the point of sale.
- Purchasing is a lead-time problem: by the time a human notices an empty shelf, the reorder is already late; the system must raise the alert at the reorder point, not at zero.

**Real-life use cases**

- **Retail and e-commerce**: Shopify, Zoho Inventory, and the inventory cores of Amazon/Flipkart seller platforms are this design scaled up.
- **Warehousing and 3PL**: receiving against purchase orders, putaway, pick/pack/ship, cycle counting.
- **Manufacturing (light)**: raw-material and finished-goods tracking with adjustments for scrap.
- **Food and pharma**: the same model plus lot/expiry tracking — an extension of the movement ledger, not a different design.

```mermaid
flowchart LR
    Seller["Store / Seller App"] -->|"stock-in, adjustments"| API["Inventory API"]
    Buyer["Checkout Service"] -->|"reserve, confirm, release"| API
    API --> DB[("Inventory Store")]
    API -->|"async events"| Q[("Event Queue")]
    Q --> ALERT["Low-Stock Alert Worker"]
    ALERT -->|"reorder notification"| Buyer
    JOB["Reservation Expiry Job"] -->|"release expired holds"| DB
```

The diagram shows the three actors on the system: interactive writers (seller app, checkout) on a synchronous API, the database as the source of truth, and time/threshold-driven workers (expiry job, alert worker) that act without user traffic.

---

### Functional Requirements

1. **Product catalog management**
   - Add/update products (SKU, name, price, category, low-stock threshold, reorder point); deactivate products without deleting history.
2. **Stock-in (receiving)**
   - Increase stock for a SKU with a reason and reference (purchase order, return, correction); every receipt is recorded as a movement.
3. **Stock-out (sale/dispatch)**
   - Decrease stock atomically; reject the operation if insufficient stock — the quantity must never go negative.
4. **Reservations**
   - Reserve stock for an open order (`RESERVED` state) so it cannot be sold twice; confirm (convert reservation to a sale) or release (return to available) with an expiry for abandoned checkouts.
5. **Stock visibility**
   - View current stock per SKU split into `on_hand`, `reserved`, and `available = on_hand - reserved`; view per-warehouse breakdown when multiple locations exist.
6. **Low-stock alerts**
   - When `available` drops to or below the reorder point, emit an alert event (asynchronously) for purchasing; alert once per threshold crossing, not on every subsequent sale.
7. **Adjustments and cycle counts**
   - Record manual corrections (damage, theft, count variance) with mandatory reason codes; adjustments are movements like any other, never silent overwrites.
8. **Movement history and reporting**
   - Append-only log of every stock change (delta, reason, reference, actor, timestamp); current quantity must be reconcilable by summing the log.

---

### Non-Functional Requirements

- **Scale**: single store/warehouse up to tens of thousands of SKUs; thousands of stock operations per day; all data fits on one relational primary. (Multi-warehouse allocation is covered in the Deep Dive as the growth path.)
- **Consistency**: stock counts must be strongly consistent — no overselling and no negative quantities under any concurrency. This is the hard requirement; catalog reads and reports may be eventually consistent by seconds.
- **Latency**: stock read and stock-in/out under 200 ms at p99 (checkout is latency-sensitive); availability lookups under 100 ms at p99 since they sit on the product-page path.
- **Availability**: 99.9% for the write path during business hours; alert delivery may lag but must be at-least-once with deduplication.
- **Durability and auditability**: no acknowledged stock change is ever lost; every change is traceable to a reason and reference for at least the financial retention period (typically 7 years).
- **Security**: role-based access (viewer vs stock clerk vs admin); adjustments above a threshold require elevated privilege; rate limiting on public availability endpoints.

---

### Capacity Estimation

Back-of-envelope math for a single-warehouse merchant with a web storefront. The point of the exercise is to show *how small* the numbers are — which licenses choosing correctness (one relational primary, row-level locking) over distributed-systems machinery.

**Catalog and stock**

- SKUs: 20,000 active products.
- Warehouses: 1 (growth path: 5) → stock-level rows: 20,000–100,000. Trivially indexed.
- Average units per SKU: 50 → ~1M physical units tracked, but only one counter row per (SKU, warehouse).

**Throughput (QPS)**

- Sales: 5,000 orders/day, ~1.5 line items each → 7,500 stock-outs/day. Concentrated in ~12 waking hours → average **0.17 stock-outs/second**, peak ~10× during a flash sale ≈ **2/second**. Stock-ins (receiving) are ~10% of that.
- Reservations: one per checkout attempt, ~2× the completed-order rate → peak **~4 writes/second** on the reservation path.
- Availability reads: the dominant load. 50,000 product-page views/day × 1 availability check ≈ **0.6/second average**, peak **~10/second**; a read replica or a short-TTL cache absorbs this entirely.
- Total write load peaks around **10 QPS**; total read load around **20 QPS**. A single modest application node and one PostgreSQL primary have 100× headroom.

**Storage**

- `products`: 20,000 rows × ~500 bytes ≈ **10 MB**.
- `stock_levels`: 100,000 rows × ~100 bytes ≈ **10 MB**.
- `stock_movements` (the append-only ledger — the only table that grows): 8,000 movements/day × ~200 bytes ≈ **1.6 MB/day ≈ 0.6 GB/year**. Seven-year retention ≈ **4 GB** — no partitioning required at this scale; a monthly partition is a cheap insurance policy.
- Reservations: a few thousand active rows at any time; expired/confirmed rows are pruned or partitioned monthly.

**Bandwidth**

- Negligible: even at peak, request/response payloads of ~1 KB × 30 QPS ≈ **30 KB/s**.

**Conclusion**: the entire hot path is a handful of indexed row updates per second. Spend the design budget on *concurrency correctness and auditability*, not on scale-out.

---

### Characteristics

Each characteristic is explained in detail.

- **Strongly consistent counters**
  Stock quantities are decremented under concurrency by many independent actors. The system guarantees the invariant `on_hand >= 0` and `available = on_hand - reserved` at all times, enforced in the database, not in application code.

- **Append-only movement ledger**
  Every change to stock is recorded as an immutable movement row. The current quantity is a *derived* value; the ledger is the truth. This makes discrepancies explainable and audits possible.

- **Reservation lifecycle**
  Stock moves through `AVAILABLE → RESERVED → SOLD` (or back to `AVAILABLE` on release/expiry). Reservations decouple "a customer is paying" from "the unit shipped", which is what makes checkout safe without holding database locks across a payment call.

- **Threshold-driven alerting**
  Low-stock detection is a side effect of writes, evaluated asynchronously. The system alerts on the *crossing* of the reorder point, once, rather than on every sale below it.

- **Idempotent write operations**
  Every mutating operation accepts a client-supplied idempotency key (or a unique reference such as an order ID), so retries from clients, queues, and flaky networks cannot double-receive or double-dispatch stock.

- **Single-writer simplicity**
  One relational primary owns all stock writes. There is no distributed consensus, no CRDT, no multi-master conflict — correctness comes from row locks and conditional updates.

- **Time-driven background behavior**
  Reservation expiry and (optionally) reorder-point re-evaluation run as scheduled jobs that scan time-based predicates — naturally re-runnable and self-healing after downtime.

- **Read/write asymmetry**
  Reads (availability on product pages) outnumber writes by ~10× and can tolerate seconds of staleness; writes cannot tolerate any. The design exploits this with read replicas/caching for reads and a single strongly consistent write path.

- **Auditability and traceability**
  Every movement carries `reason`, `reference_id` (order/PO/adjustment), and `actor`. A cycle-count variance can be walked back through the ledger to the exact operations that caused it.

- **Graceful degradation**
  If the alert pipeline or the expiry job is down, the write path is unaffected; reservations simply live longer and alerts arrive late. Core selling never depends on auxiliary workers.

---

### Components

- **API layer (REST service)**
  Purpose: exposes catalog management, stock-in/out, reservations, availability queries, and movement history.
  Responsibilities: authentication, role-based authorization (viewer vs clerk vs admin), request validation, idempotency-key handling, and orchestrating the atomic stock transactions.
  How it works: stateless Spring Boot service; all stock invariants are enforced in the service + database, never in the client.
  Relationship: the only writer of stock state; emits domain events via the outbox.
  Real-world example: the inventory microservice behind Shopify's admin and checkout, or the "Inventory Service" box in every e-commerce reference architecture.

- **Inventory store (relational database)**
  Purpose: durable source of truth for products, stock levels, reservations, the movement ledger, and the outbox.
  Responsibilities: transactional guarantees for stock operations; constraint enforcement (non-negative quantities via conditional updates, unique idempotency keys, unique active reservation per order line).
  Relationship: read by the API and read replicas; scanned by the expiry job.
  Real-world example: PostgreSQL — the default choice for inventory cores at this scale (Zoho Inventory, most ERP inventory modules).

- **Reservation service (module)**
  Purpose: the transactional core of checkout safety — reserve, confirm, release in one place.
  Responsibilities: atomic `available` check-and-decrement, reservation row creation with expiry timestamp, confirmation (reservation → sale movement), release (reservation → available), and idempotency on order IDs.
  Relationship: called by the API; writes reservations, movements, and outbox events in single transactions; scanned by the expiry job.
  Real-world example: the "inventory allocation" step inside every order-management system (OMS) — Salesforce OMS and commercetools both model exactly this reserve/confirm/release triad.

- **Stock movement ledger**
  Purpose: append-only record of every unit that enters or leaves, with reason, reference, and actor.
  Responsibilities: provide the audit trail; serve as the reconciliation source when a cycle count disagrees with the counter; optionally serve as the event-sourced source of truth (see Deep Dive 4).
  Relationship: written inside every stock transaction; read by reporting and dispute workflows.
  Real-world example: the "stock moves" table in Odoo/ERPNext — in those systems the ledger *is* the model and quantities are computed from it.

- **Low-stock alert pipeline (outbox → queue → worker)**
  Purpose: notify purchasing when a SKU crosses its reorder point.
  Responsibilities: evaluate the threshold after each stock-out (inside the transaction, write an outbox row only on a crossing); deliver the alert asynchronously; dedupe so one crossing produces one alert.
  Relationship: downstream of every stock write; never on the synchronous path.
  Real-world example: reorder-point notifications in TradeGecko/QuickBooks Commerce; a Kafka consumer emailing a purchasing Slack channel is the same shape.

- **Reservation expiry job**
  Purpose: release reservations whose checkout never completed (payment abandoned, session timed out).
  Responsibilities: scan `WHERE status = 'ACTIVE' AND expires_at < now()` with `FOR UPDATE SKIP LOCKED`, release each in its own transaction, emit release events.
  How it works: batched poller; time-based predicates make reruns idempotent and self-healing after downtime.
  Real-world example: the "abandoned cart inventory release" job every e-commerce platform runs; ticket-booking systems (BookMyShow seat holds) use the identical mechanism.

- **Availability read path (replica + optional cache)**
  Purpose: serve high-volume "is it in stock" reads without touching the write primary.
  Responsibilities: project `available` per SKU to a read replica or a short-TTL (1–5 s) cache; tolerate bounded staleness.
  Relationship: read-only; invalidated or refreshed on stock events.
  Real-world example: product-detail-page inventory badges ("Only 3 left") are almost always served from a cached, slightly stale projection — the authoritative check happens at reserve time.

- **Warehouse allocation service (growth path)**
  Purpose: choose which warehouse fulfills an order when multiple locations hold the SKU.
  Responsibilities: rank candidate warehouses by stock availability, distance to the customer, and split-shipment cost; execute the reservation against the chosen warehouse's stock row.
  Relationship: sits between the API and the reservation service; reads per-warehouse stock levels.
  Real-world example: the "sourcing/fulfillment optimizer" in an OMS; see Deep Dive 3.

```mermaid
flowchart TB
    Admin["Seller Admin App"] --> LB["Load Balancer"]
    Checkout["Checkout Service"] --> LB
    PDP["Product Page Reads"] --> Cache["Availability Cache"]
    LB --> API["Inventory API Service"]
    API --> DB[("PostgreSQL: products, stock_levels, reservations, stock_movements, outbox")]
    Cache --> Replica[("Read Replica")]
    RELAY["Outbox Relay"] -->|"poll unpublished"| DB
    RELAY --> Q[("Queue")]
    Q --> ALERT["Low-Stock Alert Worker"]
    ALERT --> Notify["Email / Slack / Webhook"]
    JOB["Reservation Expiry Job"] -->|"claim expired holds"| DB
    JOB -->|"release events"| Q
```

At this scale every box except PostgreSQL can be one process; the architecture is drawn distributed so the *growth* story (more warehouses, more channels, an events feed) requires no redesign — only deployment changes.

---

### Architectural Patterns

- **Atomic conditional update (database compare-and-set)**
  What it is: `UPDATE stock_levels SET on_hand = on_hand - :qty WHERE sku = :sku AND on_hand - reserved >= :qty`, then check the affected-row count.
  Problem it solves: two concurrent checkouts of the last unit must not both succeed; read-modify-write in application code has a check-then-act race.
  How it works: the predicate is evaluated under the row lock inside the update itself; exactly one of two racing updates can observe sufficient availability for the final unit.
  When to use: counters and capacity columns under concurrency. When not: when you need to read related state and make a multi-step decision under the same lock (use pessimistic locking — see Deep Dive 2).
  Advantages: no pessimistic locking across think-time, no distributed locks, single round-trip. Disadvantages: all contention for a SKU funnels onto one row — fine at this scale; a hot SKU in a flash sale serializes on that row (mitigations in Deep Dive 2).
  Real-world example: ticket inventory, seat maps, and stock decrement systems all use this primitive.

- **Optimistic locking with retry (`@Version`)**
  What it is: a version column on the stock row; JPA increments it per update and throws `OptimisticLockException` on a stale write; the service retries the whole unit of work a bounded number of times.
  Problem it solves: lost updates when a transaction reads a row, computes, and writes back — without holding a lock across the computation.
  When to use: low-to-moderate contention where retries are rare and cheap. When not: hot rows where retries amplify load (a flash-sale SKU would livelock).
  Advantages: no lock held during think-time, no deadlock risk. Disadvantages: wasted work under contention; retry logic must be bounded and jittered.
  Real-world example: Deep Dive 2 shows both this and the pessimistic alternative with trade-offs.

- **Pessimistic locking (`SELECT ... FOR UPDATE`)**
  What it is: the transaction takes the row lock up front via JPA `@Lock(PESSIMISTIC_WRITE)`; all other writers queue until commit.
  Problem it solves: multi-step invariants (check availability, check reservation limits, write movement, write outbox) that must observe a stable row throughout.
  When to use: high contention on a specific row, or when the read-then-write decision is complex. When not: across external calls (payment gateways) — never hold a database lock over a network call; that is what reservations exist for.
  Advantages: no wasted work, simple mental model. Disadvantages: lock queueing adds latency; deadlock risk if multiple rows are locked in inconsistent order (always lock in a canonical order, e.g. sorted by SKU).

- **Reservation with expiry (two-phase commit substitute)**
  What it is: split "sell" into `reserve` (fast, synchronous, holds the units) and `confirm`/`release` (after payment), with a TTL on the hold.
  Problem it solves: you cannot hold a database transaction open across a payment-gateway call, yet you must not sell the reserved units to anyone else in the meantime.
  How it works: reserve decrements `available` (moves units to `reserved`) and writes a reservation row with `expires_at`; confirm converts it to a `SALE` movement; the expiry job releases abandoned holds.
  When to use: any flow with a slow, fallible middle step (payment, fraud check). When not: instant, single-step operations (in-store cash sale) — just do a direct stock-out.
  Advantages: no distributed transaction, no lock across the network, automatic recovery from abandoned checkouts. Disadvantages: stock is temporarily unavailable while reserved (overselling is traded for occasional under-selling); requires the expiry job to be reliable.
  Real-world example: airline seat holds, BookMyShow seat selection timers, Shopify checkout inventory reservation.

- **Transactional Outbox**
  What it is: the stock transaction and a "stock changed / low-stock crossed" event row commit together; a relay publishes to the queue.
  Problem it solves: the dual-write problem — a stock-out that commits but whose low-stock alert never publishes (or publishes for a rolled-back stock-out).
  Advantages: atomicity without distributed transactions. Disadvantages: at-least-once delivery, so consumers must dedupe.
  Real-world example: Debezium CDC streaming an outbox table to Kafka.

- **Event sourcing for stock movements (optional, see Deep Dive 4)**
  What it is: the append-only `stock_events` ledger is the source of truth; `stock_levels` is a materialized projection rebuilt by summing events.
  Problem it solves: perfect auditability, temporal queries ("what was the stock of SKU-9 last Tuesday?"), and the ability to rebuild derived state after a bug.
  When to use: regulated domains, heavy dispute/audit load, or when many read models need the same history. When not: a simple single-store system where a counter + audit log already satisfies the auditors — event sourcing adds real complexity.
  Advantages: complete history, replayable projections. Disadvantages: eventual consistency between event write and projection; snapshotting needed for fast current-state reads.

- **Idempotent Consumer**
  What it is: consumers of order events record `(event_id)` under a unique constraint and skip duplicates.
  Problem it solves: at-least-once queues plus retries must not double-decrement stock when an `OrderCreated` event is delivered twice.
  Advantages: exactly-once effect from at-least-once transport. Disadvantages: an extra write per event; a bounded residual duplicate window on consumer crash (named and accepted). See Deep Dive 6.

- **Polling Publisher with row claiming (scheduled jobs)**
  What it is: `SELECT ... WHERE status = 'ACTIVE' AND expires_at < now() FOR UPDATE SKIP LOCKED LIMIT N` on a schedule.
  Problem it solves: reservation expiry must run with no user traffic and survive restarts and multiple app instances.
  Advantages: self-healing, horizontally scalable without a lock service. Disadvantages: detection granularity equals the poll interval — fine for minute-scale reservation TTLs.

---

### Benefits

- **No overselling, by construction**: the conditional update and the reservation state machine make the bad state (negative stock, double-sold units) unrepresentable, not just unlikely — support tickets about cancelled paid orders disappear.
- **Complete audit trail**: the movement ledger answers "where did the units go" months later, which is the difference between a solvable shrinkage problem and a write-off.
- **Checkout safety without distributed transactions**: reservations give payment flows a safe two-phase shape with automatic recovery from abandonment, using only one database.
- **Purchasing lead time**: reorder-point alerts fire when there is still time to restock, converting stockouts from surprises into planned purchase orders.
- **Operational visibility**: on-hand, reserved, and available per SKU per warehouse, plus movement history, are all simple queries — the data model doubles as the reporting model at this scale.
- **Safe retries everywhere**: idempotency keys on every mutation mean clients, queues, and cron jobs can retry freely after timeouts without corrupting stock — the most common real-world inventory bug class is eliminated.
- **Growth without redesign**: the outbox, the per-warehouse stock rows, and the reservation model are already the shapes the multi-warehouse, multi-channel version needs.

---

### Pros

- **Simplicity**: one relational primary, one service, well-understood primitives (row locks, conditional updates). A small team can operate it.
- **Strong correctness**: invariants enforced in the database hold under application bugs, retries, and manual SQL fixes.
- **Low latency**: single-row updates are sub-millisecond inside the database; the 200 ms p99 budget is mostly network and framework overhead.
- **Cheap to run**: the capacity math shows 100× headroom on a single modest node; no Kafka, no cache cluster, no coordination service is *required* at this scale.
- **Debuggability**: every state change is a row in a ledger with a reason; "why is this number what it is" is a SQL query, not a log-grep across ten services.
- **Testability**: the concurrency-critical code paths are small and deterministic; race conditions can be exercised with plain multi-threaded integration tests against a real database.

---

### Cons

- **Single-primary write ceiling**: all writes for a SKU serialize on one row of one database. A viral flash-sale SKU can create a lock queue; the fixes (inventory splitting, async claim queues) add complexity.
- **Reservation-induced under-selling**: units held by abandoned checkouts are temporarily unsellable; aggressive TTLs hurt conversion, lax TTLs hurt availability — a real business trade-off, not a bug.
- **Staleness on the read path**: cached availability can say "in stock" for a unit that just sold; the authoritative check at reserve time must handle the resulting failures gracefully (this is unavoidable — it is the price of read scale).
- **Operational jobs are load-bearing**: if the expiry job silently stops, reserved stock leaks and availability drifts down; jobs need the same monitoring as the API.
- **Ledger growth**: the movement table grows forever; without partitioning/archival discipline, queries and backups degrade over years.
- **Not a WMS**: this design tracks *how many*, not *where in the building* (bins, pick paths, lot/expiry, serial numbers). Those are deliberate scope cuts; bolting them on later is a data-model migration, not a config change.

---

### Challenges

- **Technical — the check-then-act race**: the naive `SELECT quantity; if (quantity >= n) UPDATE quantity = quantity - n` loses updates under concurrency because the check and the write are not atomic. Every stock mutation must be a single conditional statement, an optimistic-lock retry loop, or a pessimistically locked critical section — there is no fourth option, and choosing none is the most common beginner bug.
- **Technical — the dual-write problem**: a stock change and its downstream effects (alert, search-index update, analytics event) cannot be committed atomically to two systems. The outbox pattern is the standard answer; skipping it produces phantom alerts and missed reorders.
- **Scalability — hot-SKU contention**: a flash sale concentrates thousands of decrements on one row, which serializes at the row lock. Mitigations: split the SKU's stock into N sub-rows (inventory sharding) and decrement any one of them; or accept oversell-tolerant queuing with post-payment reconciliation. Both are complexity you add only when measurement demands it.
- **Scalability — multi-warehouse fan-out**: once stock lives in many locations, "do we have it" is a multi-row question and "where do we ship from" is an optimization problem. The per-(SKU, warehouse) row design keeps each write single-row, but allocation logic must handle partial availability and split shipments (Deep Dive 3).
- **Performance — read-path pressure**: availability sits on the product-page path with 10× the write volume. Serving it from the write primary wastes the primary's headroom; serving it from a cache introduces staleness that must be bounded and must fail safe at reserve time.
- **Reliability — the expiry job is load-bearing**: a stopped expiry job leaks reserved stock and slowly zeroes availability. It needs heartbeats, alerting on "no releases in N minutes during traffic", and a catch-up-safe design (time-based predicates, not in-memory state).
- **Reliability — exactly-once illusion**: queues deliver at-least-once; networks time out after the server committed. Without idempotency keys and consumer dedupe, retries double-receive and double-dispatch stock — the single most common production inventory bug.
- **Maintainability — invariant drift**: as features accrete (bundles, backorders, pre-orders, returns-to-stock), each new write path must re-implement or reuse the same invariants. Keeping *all* stock mutation behind one service module (never direct table writes from other features) is what keeps the system correct at year three.
- **Operational — reconciliation**: physical stock drifts from recorded stock (damage, theft, mis-picks). The system needs cycle-count workflows and adjustment movements with reason codes; a counter that cannot be corrected becomes a counter nobody trusts.
- **Security — adjustment abuse**: manual adjustments are the fraud vector (a clerk "adjusts" stock down and walks out with units). Adjustments need role gating, amount thresholds, mandatory reason codes, and an immutable audit trail with the actor's identity.

---

### Best Practices

- **Enforce invariants in the database, not just the service.** A conditional `UPDATE ... WHERE available >= :qty` and a `CHECK (on_hand >= 0)` constraint hold under application bugs, future services, and manual SQL fixes. Application-only checks are one race window away from negative stock.
- **Never hold a database lock across a network call.** Payment gateways take seconds and fail often; a row lock held across that call queues every other buyer of the SKU behind a flaky third party. Reservations exist precisely to convert "hold a lock" into "hold a row state with a TTL".
- **Make every mutation idempotent from day one.** Require an idempotency key (or a natural unique reference like `order_id`) on stock-in, stock-out, reserve, confirm, and release, enforced by a unique constraint. Retrofitting idempotency after the first double-dispatch incident means reconciling corrupted stock; building it in costs one column.
- **Append movements; never overwrite quantities silently.** An adjustment is a movement with a reason, not an `UPDATE` to the counter alone. When the cycle count disagrees with the system — and it will — the ledger is the only way to explain the gap.
- **Alert on threshold crossings, not on states.** Emit the low-stock event when `available` transitions from above to at-or-below the reorder point, and record that it fired. Alerting on every sale below the threshold spams purchasing into ignoring the channel; alerting once per crossing keeps the signal meaningful.
- **Keep the write path free of auxiliary work.** Notification delivery, search reindexing, and analytics are outbox consumers, not inline calls. A slow email provider must never add latency to a checkout.
- **Lock in a canonical order.** When a transaction touches multiple stock rows (a multi-line order), lock them sorted by SKU. Inconsistent lock ordering across concurrent transactions is how you get deadlocks; canonical ordering makes them structurally impossible.
- **Bound and jitter every retry.** Optimistic-lock retries and queue redeliveries must have a cap and exponential backoff with jitter; unbounded retries turn a hot row into a retry storm that looks exactly like a DDoS.
- **Monitor the counters, not just the service.** Alert on negative-available attempts (rejected stock-outs spike = overselling pressure or a bug), reservation leak rate (active reservations older than 2× TTL), and ledger-vs-counter drift. The numbers *are* the health of an inventory system.
- **Treat time as data.** Store `expires_at`, `created_at`, and `occurred_at` explicitly and let jobs scan them; in-memory timers and "run at" schedulers die with the process and are the classic source of leaked reservations after a deploy.

---

### When to Use / When Not to Use

**Use this design when:**

- You operate one or a few warehouses/stores with up to ~100k SKUs and up to thousands of stock operations per day — the single-primary model has orders of magnitude of headroom.
- Overselling is unacceptable (paid orders, regulated goods) and you need strong consistency at the point of sale.
- You need a defensible audit trail: finance, disputes, or shrinkage investigations require every unit movement to be explainable.
- Checkout involves a slow middle step (payment, fraud review) that needs the reserve/confirm/release shape.
- Your team is small and should be spending its complexity budget on the product, not on operating distributed infrastructure.

**Do not use this design (as-is) when:**

- You are a marketplace or quick-commerce platform with hundreds of warehouses and tens of thousands of decrements per second on hot SKUs — you need sharded inventory, per-warehouse services, and possibly oversell-tolerant async claiming (the advanced real-time variant).
- You need full warehouse-management features: bin locations, pick-path optimization, lot/serial/expiry tracking, wave picking — that is a WMS; this design is the inventory *core* a WMS would sit beside.
- You sell purely digital, effectively infinite goods (software licenses without seat limits) — a counter with strong consistency is overkill; a simple entitlement check suffices.
- You need multi-region active-active writes with sub-100 ms latency on every continent — a single primary cannot do that; you would need per-region inventory partitioning (each region owns its stock) rather than this design.

---

### Use Cases

- **E-commerce checkout reservation**: a shopper checks out; the system reserves the units for 15 minutes while payment runs; payment success confirms the sale, failure or timeout releases the units. The reservation TTL balances conversion (longer holds) against availability (shorter holds).
- **Receiving against a purchase order**: a warehouse clerk scans a delivery; stock-in movements reference the PO, and a partial receipt leaves the PO open — the ledger shows exactly what arrived when.
- **Flash sale on a hot SKU**: 500 units, 10,000 would-be buyers. The conditional update admits exactly 500 successful reservations; everyone else gets a fast, honest "sold out" instead of a cancelled order the next day.
- **Cycle count and shrinkage adjustment**: a weekly count finds 3 units missing; an adjustment movement with reason `CYCLE_COUNT_VARIANCE` and the clerk's identity corrects the counter, and the ledger preserves the discrepancy for the shrinkage report.
- **Reorder-point purchasing**: the 400th sale of a SKU crosses its reorder point; exactly one alert goes to purchasing with current available, average daily sales, and supplier lead time — early enough that the replenishment arrives before stockout.
- **Multi-warehouse order routing**: an order for 5 units can be fulfilled from warehouse A (3 units) and B (2 units); the allocation service either splits the shipment or routes whole to the warehouse that has all 5, per cost policy (Deep Dive 3).
- **Return to stock**: a customer return is inspected and restocked as a `RETURN` movement; a damaged return is a movement to a quarantine bucket instead — both keep the ledger complete without inflating sellable stock.
- **Oversell incident forensics**: after a bug, support asks "how did SKU-9 go negative for 4 minutes?" The movement ledger, with references to order IDs, answers it in one query — the difference between a postmortem and a guess.

---

### Data Model and APIAPI Design

REST over JSON, versioned by URL prefix (`/api/v1`). All mutating endpoints require an `Idempotency-Key` header; the server stores `(key, endpoint, actor) → response` for 24 hours and replays the stored response on duplicate keys. Authenticated via OAuth2 client-credentials (service-to-service) or JWT bearer (admin UI); roles: `VIEWER`, `CLERK`, `ADMIN`.

**Endpoints**

| Method | Path | Purpose | Role |
|---|---|---|---|
| POST | `/api/v1/products` | Create product | ADMIN |
| GET | `/api/v1/products/{sku}` | Product + availability | VIEWER |
| GET | `/api/v1/products?category=&cursor=&limit=&sort=` | List/search products | VIEWER |
| POST | `/api/v1/inventory/{sku}/stock-in` | Receive stock | CLERK |
| POST | `/api/v1/inventory/{sku}/stock-out` | Direct sale/dispatch | CLERK |
| POST | `/api/v1/inventory/{sku}/adjustments` | Cycle-count/damage correction | ADMIN |
| POST | `/api/v1/reservations` | Reserve stock for an order | CLERK (service) |
| POST | `/api/v1/reservations/{id}/confirm` | Convert reservation to sale | CLERK (service) |
| POST | `/api/v1/reservations/{id}/release` | Cancel reservation | CLERK (service) |
| GET | `/api/v1/inventory/low-stock` | SKUs at/below reorder point | VIEWER |
| GET | `/api/v1/inventory/{sku}/movements?cursor=&limit=` | Movement history | VIEWER |

**Create product**

```http
POST /api/v1/products HTTP/1.1
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
Idempotency-Key: 9b3f0c2e-7a1d-4f2a-9c55-2f0d1a2b3c4d
Content-Type: application/json

{
  "sku": "WIDGET-001",
  "name": "Standard Widget",
  "price": { "amount": 1299, "currency": "USD" },
  "category": "widgets",
  "reorderPoint": 25,
  "lowStockThreshold": 10
}
```

```http
HTTP/1.1 201 Created
Location: /api/v1/products/WIDGET-001

{
  "sku": "WIDGET-001",
  "name": "Standard Widget",
  "price": { "amount": 1299, "currency": "USD" },
  "category": "widgets",
  "reorderPoint": 25,
  "lowStockThreshold": 10,
  "active": true,
  "createdAt": "2026-01-15T10:30:00Z"
}
```

**Stock-in (receiving)**

```http
POST /api/v1/inventory/WIDGET-001/stock-in HTTP/1.1
Idempotency-Key: po-8842-receipt-1

{ "quantity": 100, "reason": "PURCHASE_ORDER_RECEIPT", "referenceId": "PO-8842", "warehouseId": "WH-1" }
```

```http
HTTP/1.1 200 OK

{ "sku": "WIDGET-001", "warehouseId": "WH-1", "onHand": 100, "reserved": 0, "available": 100, "movementId": "mv_01J..." }
```

**Reserve stock (checkout)**

```http
POST /api/v1/reservations HTTP/1.1
Idempotency-Key: order-55123-line-1

{ "orderId": "ORD-55123", "sku": "WIDGET-001", "quantity": 2, "warehouseId": "WH-1", "ttlSeconds": 900 }
```

```http
HTTP/1.1 201 Created

{ "reservationId": "rsv_01J9Z...", "orderId": "ORD-55123", "sku": "WIDGET-001", "quantity": 2, "status": "ACTIVE", "expiresAt": "2026-01-15T10:45:00Z" }
```

Insufficient stock is a domain failure, not a server error:

```http
HTTP/1.1 409 Conflict

{ "error": "INSUFFICIENT_STOCK", "message": "Requested 2, available 1", "sku": "WIDGET-001", "available": 1 }
```

**Confirm / release**

```http
POST /api/v1/reservations/rsv_01J9Z.../confirm
Idempotency-Key: order-55123-confirm
→ 200 OK { "reservationId": "rsv_01J9Z...", "status": "CONFIRMED", "movementId": "mv_01JA..." }

POST /api/v1/reservations/rsv_01J9Z.../release
Idempotency-Key: order-55123-release
→ 200 OK { "reservationId": "rsv_01J9Z...", "status": "RELEASED" }
```

Confirming an expired reservation returns `410 Gone` (`RESERVATION_EXPIRED`) — the units may have been resold; the order flow must re-attempt reservation.

**Availability read**

```http
GET /api/v1/products/WIDGET-001
→ 200 OK
{ "sku": "WIDGET-001", "name": "Standard Widget", "availability": { "onHand": 98, "reserved": 5, "available": 93 }, "lowStock": false }
```

**Movement history with pagination, filtering, sorting**

```http
GET /api/v1/inventory/WIDGET-001/movements?reason=SALE&from=2026-01-01&sort=occurredAt:desc&limit=50&cursor=eyJpZCI6...
→ 200 OK
{
  "data": [
    { "movementId": "mv_01JA...", "delta": -2, "reason": "SALE", "referenceId": "ORD-55123", "actor": "checkout-service", "occurredAt": "2026-01-15T10:46:02Z" }
  ],
  "page": { "limit": 50, "nextCursor": "eyJpZCI6Im12XzAxSi4uLiJ9", "hasMore": true }
}
```

**Contract rules**

- **Validation**: `quantity` must be a positive integer ≤ 1,000,000; `sku` must match `^[A-Z0-9-]{3,32}$`; unknown fields are rejected. Validation failures return `400` with a field-level error list: `{ "error": "VALIDATION_FAILED", "fields": [{ "field": "quantity", "issue": "must be positive" }] }`.
- **Status codes**: `201` creates; `200` success; `400` validation; `401/403` auth; `404` unknown SKU/reservation; `409` domain conflict (insufficient stock, duplicate active reservation for the order line); `410` expired reservation; `422` state-machine violation (confirming a released reservation); `429` rate limited; `5xx` retryable server faults.
- **Idempotency**: duplicate `Idempotency-Key` returns the original response with an `Idempotent-Replay: true` header and performs no state change. Keys are scoped per endpoint and actor.
- **Pagination**: cursor-based (`cursor` + `limit`, max 200) for movements and product lists — offset pagination skips/duplicates rows under concurrent writes, and the movement ledger is always being written.
- **Filtering/sorting**: allowlisted fields only (`reason`, `from`, `to`, `sort=occurredAt:asc|desc`); arbitrary sort fields are rejected to prevent unindexed scans.
- **Versioning**: URL prefix `/api/v1`; breaking changes ship as `/api/v2` alongside v1 for one deprecation window; additive fields are not versioned.
- **Rate limiting**: token bucket per client identity — 100 req/s for service accounts, 20 req/s for admin UI tokens; `429` responses include `Retry-After` and `X-RateLimit-Remaining` headers.
- **Auth**: every request carries a JWT; the `sub` claim is recorded as the `actor` on every movement — the audit trail is only as good as its attribution.

---

#### Data Modeling

```mermaid
erDiagram
    PRODUCTS ||--o{ STOCK_LEVELS : "stocked as"
    WAREHOUSES ||--o{ STOCK_LEVELS : "holds"
    PRODUCTS ||--o{ STOCK_MOVEMENTS : "tracked by"
    WAREHOUSES ||--o{ STOCK_MOVEMENTS : "location of"
    STOCK_LEVELS ||--o{ RESERVATIONS : "held against"
    PRODUCTS ||--o{ RESERVATIONS : "reserved as"
    PRODUCTS ||--o{ IDEMPOTENCY_KEYS : "scoped to"

    PRODUCTS {
        string sku PK
        string name
        int price_amount
        string price_currency
        string category
        int reorder_point
        int low_stock_threshold
        boolean active
        timestamp created_at
    }
    WAREHOUSES {
        string warehouse_id PK
        string name
        string region
    }
    STOCK_LEVELS {
        string sku PK,FK
        string warehouse_id PK,FK
        int on_hand
        int reserved
        int version
        timestamp updated_at
    }
    RESERVATIONS {
        string reservation_id PK
        string sku FK
        string warehouse_id FK
        string order_id
        int quantity
        string status
        timestamp expires_at
        timestamp created_at
    }
    STOCK_MOVEMENTS {
        string movement_id PK
        string sku FK
        string warehouse_id FK
        int delta
        string reason
        string reference_id
        string actor
        timestamp occurred_at
    }
    IDEMPOTENCY_KEYS {
        string key PK
        string endpoint
        string actor
        string response_body
        timestamp created_at
    }
```

**Design notes**

- `STOCK_LEVELS` is keyed by `(sku, warehouse_id)` — the composite key is what makes the multi-warehouse growth path a data change, not a schema change. `available` is *derived* (`on_hand - reserved`), never stored, so it cannot drift.
- `STOCK_LEVELS.version` backs optimistic locking (Deep Dive 2); a `CHECK (on_hand >= 0 AND reserved >= 0 AND reserved <= on_hand)` constraint makes invalid states unrepresentable.
- `RESERVATIONS.status` is `ACTIVE | CONFIRMED | RELEASED | EXPIRED`; a partial unique index `ON reservations (order_id, sku) WHERE status = 'ACTIVE'` makes duplicate active reservations for one order line impossible at the database level.
- `STOCK_MOVEMENTS` is append-only (no `UPDATE`/`DELETE` granted to the application role). `delta` is signed: receipts positive, sales negative. `reason` is an enum: `PURCHASE_ORDER_RECEIPT`, `SALE`, `RESERVATION_CONFIRM`, `RESERVATION_RELEASE`, `RETURN`, `CYCLE_COUNT_VARIANCE`, `DAMAGE`, `CORRECTION`.
- Indexes: `stock_movements (sku, occurred_at DESC)` for history; `stock_movements (reference_id)` for order-level forensics; `reservations (status, expires_at)` for the expiry job's scan; `products (category)` for listing.
- The current quantity is always reconcilable: `SELECT sku, SUM(delta) FROM stock_movements GROUP BY sku` must equal `stock_levels.on_hand` (plus/minus reserved accounting); a nightly job verifies this and alerts on drift.

---

### High-Level Design

```mermaid
flowchart TB
    subgraph Clients
        AdminUI["Seller Admin UI"]
        CheckoutSvc["Checkout / Order Service"]
        PDP["Product Page (reads)"]
    end

    subgraph Edge["Edge"]
        LB["Load Balancer + WAF"]
    end

    subgraph App["Application Tier (stateless)"]
        API["Inventory API Service"]
        ExpiryJob["Reservation Expiry Job"]
        Relay["Outbox Relay"]
    end

    subgraph Data["Data Tier"]
        Primary[("PostgreSQL Primary")]
        Replica[("Read Replica")]
        Cache["Availability Cache (TTL 1-5s)"]
        Queue[("Message Queue")]
    end

    subgraph Workers["Async Workers"]
        AlertWorker["Low-Stock Alert Worker"]
        Projector["Availability Projector"]
    end

    AdminUI --> LB
    CheckoutSvc --> LB
    LB --> API
    PDP --> Cache
    Cache --> Replica
    API --> Primary
    Primary --> Replica
    ExpiryJob -->|"claim expired reservations"| Primary
    Relay -->|"poll unpublished outbox rows"| Primary
    Relay --> Queue
    Queue --> AlertWorker
    Queue --> Projector
    Projector -->|"refresh availability"| Cache
    AlertWorker --> Notify["Email / Slack / Webhook"]
```

**How the pieces fit**: all writes flow through the API service to the single primary — there is exactly one write path, which is what makes the invariants enforceable. Reads split by consistency need: checkout-critical reads hit the primary; product-page reads hit the cache/replica and tolerate seconds of staleness. Everything downstream (alerts, cache projection) is driven by the outbox, so a slow or dead consumer never affects the write path. The expiry job is the only component that writes without a client request.

**Reservation sequence (the critical flow)**

```mermaid
sequenceDiagram
    autonumber
    participant C as Checkout Service
    participant API as Inventory API
    participant DB as PostgreSQL
    participant P as Payment Gateway
    participant J as Expiry Job

    C->>API: POST /reservations (orderId, sku, qty, Idempotency-Key)
    API->>DB: BEGIN; UPDATE stock_levels SET reserved = reserved + qty WHERE sku AND on_hand - reserved >= qty
    alt affected rows = 1
        API->>DB: INSERT reservation (ACTIVE, expires_at = now + ttl); INSERT outbox; COMMIT
        API-->>C: 201 reservationId, expiresAt
        C->>P: charge customer
        alt payment success
            C->>API: POST /reservations/{id}/confirm
            API->>DB: BEGIN; reservation ACTIVE->CONFIRMED; on_hand -= qty, reserved -= qty; INSERT movement (SALE); COMMIT
            API-->>C: 200 CONFIRMED
        else payment failed or timeout
            C->>API: POST /reservations/{id}/release
            API->>DB: BEGIN; reservation ACTIVE->RELEASED; reserved -= qty; INSERT movement (RELEASE); COMMIT
            API-->>C: 200 RELEASED
        end
    else affected rows = 0
        API-->>C: 409 INSUFFICIENT_STOCK (available: n)
    end
    Note over J,DB: if the customer abandons checkout
    J->>DB: SELECT ... WHERE status='ACTIVE' AND expires_at < now() FOR UPDATE SKIP LOCKED
    J->>DB: per row: EXPIRED; reserved -= qty; INSERT movement (RELEASE); COMMIT
```

**Why this shape**: the payment call (steps 6–8) happens *outside* any database transaction — the reservation row, not a lock, protects the units. Every state transition is a small, fast transaction. The expiry job guarantees the `ACTIVE` state is always temporary, so abandoned checkouts cannot permanently remove stock from sale. Confirming is idempotent on the reservation's state machine: a duplicate confirm sees `CONFIRMED` and returns success without a second movement.

---

### Deep Dive

#### 1. Stock reservation flow: reserve → confirm → release with expiry

The reservation lifecycle is a state machine: `ACTIVE → CONFIRMED` (sale), `ACTIVE → RELEASED` (explicit cancel), `ACTIVE → EXPIRED` (TTL elapsed). Terminal states are final; every transition writes a movement.

```mermaid
stateDiagram-v2
    [*] --> ACTIVE : reserve (available >= qty)
    ACTIVE --> CONFIRMED : payment success
    ACTIVE --> RELEASED : explicit cancel
    ACTIVE --> EXPIRED : expiry job (ttl elapsed)
    CONFIRMED --> [*] : movement SALE
    RELEASED --> [*] : movement RELEASE
    EXPIRED --> [*] : movement RELEASE
```

Key invariants:

- **Reserve** is one conditional statement: `UPDATE stock_levels SET reserved = reserved + :qty WHERE sku = :sku AND warehouse_id = :wh AND on_hand - reserved >= :qty`. Zero affected rows → `409`. No application-level check precedes it.
- **Confirm** transitions the reservation and adjusts both counters in one transaction: `reserved -= qty` and `on_hand -= qty`, plus the `SALE` movement. It validates the reservation is `ACTIVE` and unexpired; an expired reservation returns `410` and the order flow must re-reserve (the units may have been resold — that is correct behavior, not an error).
- **Release** (explicit or via the expiry job) does `reserved -= qty` plus a `RELEASE` movement. It is idempotent: releasing a `RELEASED` reservation is a no-op returning success.
- **Expiry** is a batch job, not a timer per reservation: `SELECT reservation_id FROM reservations WHERE status = 'ACTIVE' AND expires_at < now() ORDER BY expires_at LIMIT 500 FOR UPDATE SKIP LOCKED`. `SKIP LOCKED` lets multiple app instances run the job concurrently without double-processing; each row is released in its own short transaction so one poison row cannot block the batch.
- **TTL choice** is a business knob: 10–15 minutes for checkout holds. Too short loses conversions (slow payment methods); too long under-sells stock. Measure abandonment vs. reservation-driven stockouts to tune it.

#### 2. Overselling prevention: optimistic vs pessimistic locking

Both approaches are correct; they differ in *where* the conflict cost is paid. The conditional `UPDATE` from Deep Dive 1 is actually a third option — the cheapest — but it only works when the entire decision fits in one SQL predicate. When the service must read state, apply logic, and write (e.g. confirm a reservation: check status, check expiry, adjust two counters, write a movement), you need a locking strategy.

**Optimistic locking (`@Version` + retry)** — assume conflicts are rare; detect them at write time and retry:

```java
@Entity
@Table(name = "stock_levels")
public class StockLevel {

    @EmbeddedId
    private StockLevelId id;          // (sku, warehouseId)

    private int onHand;
    private int reserved;

    @Version
    private int version;              // JPA increments and checks on every UPDATE

    public void reserve(int qty) {
        if (onHand - reserved < qty) {
            throw new InsufficientStockException(id.getSku(), onHand - reserved);
        }
        reserved += qty;
    }
    // confirm(), release() analogous — domain logic on the entity
}
```

```java
@Service
public class OptimisticReservationService {

    private static final int MAX_ATTEMPTS = 3;

    private final StockLevelRepository stockLevels;
    private final ReservationRepository reservations;

    public OptimisticReservationService(StockLevelRepository stockLevels,
                                        ReservationRepository reservations) {
        this.stockLevels = stockLevels;
        this.reservations = reservations;
    }

    public Reservation reserve(String sku, String warehouseId, String orderId, int qty) {
        int attempt = 0;
        while (true) {
            try {
                return doReserve(sku, warehouseId, orderId, qty);
            } catch (ObjectOptimisticLockingFailureException e) {
                if (++attempt >= MAX_ATTEMPTS) {
                    throw new ConcurrentStockUpdateException(sku, e);
                }
                backoffWithJitter(attempt);   // e.g. 10ms * 2^attempt +/- jitter
            }
        }
    }

    @Transactional
    protected Reservation doReserve(String sku, String warehouseId, String orderId, int qty) {
        StockLevel level = stockLevels.findById(new StockLevelId(sku, warehouseId))
                .orElseThrow(() -> new UnknownSkuException(sku));
        level.reserve(qty);                       // throws InsufficientStockException if short
        Reservation r = Reservation.active(sku, warehouseId, orderId, qty, Duration.ofMinutes(15));
        reservations.save(r);
        return r;                                 // @Version checked at flush/commit
    }
}
```

Trade-offs: no lock is held while the transaction does its work, so throughput is high when conflicts are rare; but under a flash sale on one SKU, most transactions lose the version race and retry, multiplying load exactly when the system is busiest. Retries must be bounded (3 attempts) and jittered, and the final failure must surface as a clean `409`, not a `500`.

**Pessimistic locking (`SELECT ... FOR UPDATE` via JPA `@Lock`)** — take the row lock up front; conflicts queue instead of retrying:

```java
public interface StockLevelRepository extends JpaRepository<StockLevel, StockLevelId> {

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT s FROM StockLevel s WHERE s.id = :id")
    Optional<StockLevel> findByIdForUpdate(@Param("id") StockLevelId id);

    @Modifying
    @Query("""
            UPDATE StockLevel s SET s.reserved = s.reserved + :qty
            WHERE s.id = :id AND s.onHand - s.reserved >= :qty
            """)
    int tryReserve(@Param("id") StockLevelId id, @Param("qty") int qty);
}
```

```java
@Service
public class PessimisticReservationService {

    private final StockLevelRepository stockLevels;
    private final ReservationRepository reservations;

    public PessimisticReservationService(StockLevelRepository stockLevels,
                                         ReservationRepository reservations) {
        this.stockLevels = stockLevels;
        this.reservations = reservations;
    }

    @Transactional
    public Reservation reserve(String sku, String warehouseId, String orderId, int qty) {
        StockLevel level = stockLevels.findByIdForUpdate(new StockLevelId(sku, warehouseId))
                .orElseThrow(() -> new UnknownSkuException(sku));
        level.reserve(qty);                       // safe: row is locked until commit
        Reservation r = Reservation.active(sku, warehouseId, orderId, qty, Duration.ofMinutes(15));
        return reservations.save(r);
    }
}
```

Trade-offs: no wasted work — a contending transaction waits (bounded by `lock_timeout`, e.g. 2 s) instead of retrying, which is the right behavior for hot rows; but throughput on that row is capped at `1 / avg_transaction_time`, long transactions queue everyone behind them, and multi-row transactions must lock in canonical (sorted) order to avoid deadlocks.

**Choosing**: default to the single conditional `UPDATE` (no entity read at all) for simple decrements; use pessimistic locking for multi-step invariants like confirm/release; use optimistic locking for low-contention, read-heavy aggregates (product catalog edits). Never mix optimistic and pessimistic writers on the same row without a version check in the pessimistic path — a blind `UPDATE` would silently overwrite an optimistic writer's change.

#### 3. Multi-warehouse allocation

With stock in N warehouses, "reserve 5 units of SKU-9" becomes an *allocation* decision. The design keeps each write single-row (per `(sku, warehouse_id)`) and puts the decision in an allocation service:

1. **Candidate selection**: query all warehouses with `available > 0` for the SKU, joined with warehouse metadata (region, shipping cost to the destination, cutoff times).
2. **Ranking policy** (configurable, in priority order): prefer a single warehouse that can fulfill the *whole* order (split shipments cost 1.5–2× in postage and support load); among those, nearest to the customer; tie-break by highest available stock (keeps small remnants from being stranded).
3. **Atomic claim**: attempt the conditional reserve against the top candidate. If it returns zero rows (a race — someone else took the units between selection and claim), fall through to the next candidate. The selection read is *advisory*; the conditional update is *authoritative* — this read-then-race-then-retry shape is unavoidable and correct because the claim re-validates.
4. **Split fallback**: if no single warehouse has the full quantity and policy allows splits, reserve greedily from ranked warehouses, each reservation its own transaction, compensating (releasing) earlier reservations if a later line fails — a mini-saga scoped to one order.

```java
@Service
public class AllocationService {

    private final StockLevelRepository stockLevels;
    private final ReservationService reservationService;

    public AllocationService(StockLevelRepository stockLevels,
                             ReservationService reservationService) {
        this.stockLevels = stockLevels;
        this.reservationService = reservationService;
    }

    public Reservation allocate(String sku, String orderId, int qty, String destinationRegion) {
        List<StockLevel> candidates = stockLevels
                .findAvailableBySkuOrderByRegionPreference(sku, qty, destinationRegion);
        for (StockLevel candidate : candidates) {
            try {
                return reservationService.reserve(sku, candidate.getId().getWarehouseId(), orderId, qty);
            } catch (InsufficientStockException raced) {
                // another order claimed the units between selection and claim; try next warehouse
            }
        }
        throw new InsufficientStockException(sku, 0);
    }
}
```

The important property: allocation never decrements across warehouses in one distributed transaction — each warehouse's stock row is claimed independently, and failure compensation is explicit release calls.

#### 4. Event sourcing for stock movements

In the base design, `stock_levels` is the truth and `stock_movements` is an audit log. The event-sourced variant inverts this: **`stock_events` is the only source of truth**, and `stock_levels` is a disposable projection.

- **Write path**: every operation appends an immutable event — `StockReceived(sku, wh, qty, poRef)`, `StockReserved`, `StockReservationConfirmed`, `StockReleased`, `StockAdjusted` — with a monotonically increasing sequence per `(sku, warehouse)` stream. Concurrency control moves to the stream: appending with an expected version (`INSERT ... WHERE current_version = expected`) is the optimistic concurrency check; a conflict means re-read the stream and re-decide.
- **Read path**: current availability is a projection — either maintained transactionally alongside the event insert (the pragmatic choice: event + counter update in one transaction, giving you both strong consistency *and* full history) or rebuilt asynchronously by a projector (the purist choice, with eventual-consistency lag on reads).
- **What you gain**: perfect temporal queries ("stock of SKU-9 at 2026-01-01T00:00Z" is `SUM(delta) WHERE occurred_at <= :t`), trivial new read models (rebuild a reporting table by replaying), and an audit trail that cannot be incomplete because the audit trail *is* the state.
- **What you pay**: every current-state read needs the projection (never sum the whole stream per request — snapshot); schema evolution becomes event-versioning (old events must be upcast or handled forever); and the team must understand the model — event sourcing imposed on a team that doesn't need it is a net negative. For a single-store system, the counter + audit log is usually sufficient; adopt full event sourcing when auditors, disputes, or many downstream projections justify it.

#### 5. Low-stock and reorder-point alerts

The naive implementation — "after every stock-out, if available < threshold, send an alert" — spams purchasing with one email per sale. The correct implementation alerts on the **crossing**, once:

1. Inside the stock-out transaction, capture availability *before* and *after* the decrement (the conditional `UPDATE ... RETURNING on_hand, reserved` gives both in one statement).
2. If `before > reorderPoint AND after <= reorderPoint`, insert a `LOW_STOCK_CROSSED` event into the outbox in the same transaction. No crossing, no row — the write path pays nothing in the common case.
3. The alert worker consumes the event, enriches it (average daily sales from the movement ledger, supplier lead time from config), and delivers one notification. Deduplication is structural: the crossing can only happen once per replenishment cycle because a restock moves availability back above the point, re-arming the trigger.
4. **Re-arm discipline**: a restock that lands *below* the reorder point (partial replenishment) must not re-fire the alert — track `alerted` state per SKU, cleared only when availability rises above the reorder point. Otherwise every subsequent sale re-alerts.
5. Two thresholds with different semantics: `reorder_point` (act now: lead time × daily sales + safety stock) drives purchasing alerts; `low_stock_threshold` (warn: shelf looks thin) drives a dashboard badge. Conflating them either pages purchasing for cosmetic lows or hides real reorder urgency.

#### 6. Idempotent order-event consumption

When inventory consumes order events from a queue (e.g. `OrderCreated` → reserve, `OrderCancelled` → release), at-least-once delivery makes duplicates a certainty, not an edge case. The consumer must be idempotent:

```java
@Service
public class OrderEventConsumer {

    private final ProcessedEventRepository processedEvents;
    private final ReservationService reservationService;

    public OrderEventConsumer(ProcessedEventRepository processedEvents,
                              ReservationService reservationService) {
        this.processedEvents = processedEvents;
        this.reservationService = reservationService;
    }

    @Transactional
    public void onOrderCreated(OrderCreatedEvent event) {
        // Unique constraint on processed_events(event_id) is the dedupe mechanism.
        if (!processedEvents.tryInsert(event.eventId(), "OrderCreated")) {
            return;   // duplicate delivery: already handled, acknowledge and skip
        }
        for (OrderLine line : event.lines()) {
            reservationService.reserve(line.sku(), event.warehouseId(),
                                       event.orderId(), line.quantity());
        }
        // Both the dedupe row and the reservations commit in ONE transaction:
        // a crash before commit means the event is redelivered and retried cleanly.
    }
}
```

The critical detail is that the dedupe record and the business effect commit **atomically** — recording "processed" in a separate store (or after commit) reopens the duplicate window. Natural idempotency keys reinforce this: `reserve` is keyed on `(order_id, sku)` with the partial unique index from the data model, so even a consumer bug that skips the dedupe check cannot create two active reservations for one order line. Defense in depth: unique constraints at the database are the last line, idempotent consumers are the first.

---

### Replication Strategies

**What it means**

Replication Strategies determine how data and state are copied across multiple nodes in Basic Inventory Management System. The choice of strategy determines the trade-off between consistency, availability, and latency.

**Why it matters**

Basic Inventory Management System must replicate data to prevent loss and serve reads from multiple nodes. The replication strategy determines whether the system favors consistency (strong reads) or availability (always writable), and how it handles cross-node failure.

**How it works**

**Leader-based (single-leader)**: A single primary node accepts all writes; followers replicate changes asynchronously or semi-synchronously. Reads can be served from any replica. This strategy favors strong consistency for writes but creates a write bottleneck at the leader.

```mermaid
flowchart LR
    subgraph "Primary Node"
        Leader[Leader/Follower<br/>Accepts writes]
    end
    subgraph "Replica Nodes"
        Follower1[Follower 1<br/>Read-only]
        Follower2[Follower 2<br/>Read-only]
        Follower3[Follower 3<br/>Read-only]
    end
    Client[Client] -->|Write| Leader
    Client -->|Read| Follower1
    Client -->|Read| Follower2
    Leader -->|Replicate| Follower1
    Leader -->|Replicate| Follower2
    Leader -->|Replicate| Follower3
```

*Leader-based replication: a single primary node accepts all writes and replicates them to read-only followers. Clients can read from any replica for scaled read throughput, but all writes go through the leader.*

**Multi-leader (multi-master)**: Multiple nodes accept writes and exchange updates with each other. This enables low-latency writes in different regions but requires conflict resolution (last-write-wins, merge functions, or CRDTs).

**Leaderless (quorum-based)**: Any node can accept writes; a quorum of nodes must agree. Read and write quorums are configured so that at least one node overlaps between them (R + W > N). This maximizes availability and write scalability.

**Trade-offs for Basic Inventory Management System**:

| Strategy | Use Case | Pros | Cons |
|---|---|---|---|
| Leader-based | inventory counts, pricing data, supplier info | Strong consistency, simple | Write bottleneck, leader failure risk |
| Multi-leader | public product info, anonymized restock metrics | Low-latency global writes | Conflict resolution, complex |
| Leaderless | Caching, counters | High availability, no bottleneck | Eventual consistency, read repair overhead |

**Real-world implementations**

- **Redis**: Leader-follower replication with asynchronous replication; Sentinel handles failover.
- **Apache Kafka**: Leader-based partition replication with ISR (in-sync replica) — writes go to the leader, followers replicate.
- **Cassandra**: Tunable consistency with leaderless quorum (R + W > N).
- **DynamoDB Global Tables**: Multi-master active-active across regions.

### Failure Detection and Membership

**What it means**

Failure Detection and Membership is the mechanism by which Basic Inventory Management System determines which nodes are alive and part of the cluster. Membership is the list of known nodes; failure detection is the process of updating that list when nodes fail or recover.

**Why it matters**

Basic Inventory Management System must route requests only to healthy nodes and trigger failover when a node goes down. False positives (healthy nodes marked as dead) cause unnecessary failovers and data loss. False negatives (dead nodes not detected) cause failed requests and degraded performance.

**How it works**

**Heartbeat-based detection**: Each node sends a heartbeat (ping) to a subset of peers at regular intervals. If a node misses N consecutive heartbeats, it is marked as suspect. The gossip protocol distributes membership information: each node exchanges its view of the cluster with a random peer, and the information propagates gossip-style.

```mermaid
sequenceDiagram
    participant A as Node A
    participant B as Node B
    participant C as Node C

    loop Every 1s
        A->>B: Heartbeat (ping)
        B-->>A: Heartbeat (ack)
    end
    B->>C: Gossip: A is alive
    C->>A: Gossip: B is alive
    Note over A,B,C: View converges in O(log N) rounds
```

*Gossip-based failure detection: each node periodically pings a random subset of peers and gossips its view of the cluster. The membership list converges in O(log N) rounds.*

**Phi Accrual Failure Detector**: Instead of a fixed timeout, the detector measures the time between consecutive heartbeats and computes a phi (φ) value — the probability that the node is dead given the observed heartbeat pattern. φ is compared against a threshold (typically 1–8); higher thresholds reduce false positives but increase detection latency.

**SWIM (Scalable Weakly-consistent Infection-style Process group Membership Protocol)**: Nodes ping a random subset of cluster members. If a ping fails, the node is marked "suspect" and the failure is "infected" (gossiped) to other nodes. This is O(log N) per failure detection cycle and scales to large clusters.

**Trade-offs**:

| Approach | Strengths | Weaknesses |
|---|---|---|
| Heartbeat (timeout-based) | Simple, deterministic | False positives under load |
| Phi Accrual | Adaptive threshold | Needs historical data |
| SWIM | Scales to 1000s of nodes | Eventual consistency |

**Real-world implementations**

- **AWS Route 53 Health Checks**: Uses TCP/HTTP health checks with configurable thresholds to remove unhealthy instances from DNS rotation.
- **Kubernetes**: Uses the kubelet heartbeat (every 10s) to determine node liveness; nodes missing 3 consecutive heartbeats are marked NotReady.
- **Consul**: Uses SWIM protocol for membership and failure detection; supports both LAN and WAN gossip.
- **Akka Cluster**: Uses Phi Accrual failure detector with configurable φ thresholds.

### High Availability and Scalability

**What it means**

High Availability and Scalability determines how Basic Inventory Management System continues operating when nodes or entire zones fail, and how capacity is added as demand grows. HA is about minimizing downtime; scalability is about maintaining performance as load increases.

**Why it matters**

Basic Inventory Management System must stay operational even when individual nodes, availability zones, or entire regions fail. At the same time, it must scale horizontally to handle traffic spikes without degrading latency. The two are intertwined: the replication strategy, failure detection, and load balancing all contribute to both HA and scalability.

**How it works**

**Availability zones (AZs)**: Nodes are distributed across multiple AZs within a region. Each AZ is an independent failure domain (power, networking, physical security). A load balancer distributes requests across AZs; if one AZ fails, traffic is routed to the remaining AZs with no data loss (assuming replication is in place).

```mermaid
flowchart TD
    subgraph "3 AZs in One Region"
        AZ1[AZ-1<br/>2+ nodes]
        AZ2[AZ-2<br/>2+ nodes]
        AZ3[AZ-3<br/>2+ nodes]
    end
    LB[Load Balancer]
    LB --> AZ1
    LB --> AZ2
    LB --> AZ3
    AZ1 -->|Replicate| AZ2
    AZ2 -->|Replicate| AZ3
```

*Multi-AZ deployment: a load balancer distributes traffic across three availability zones. Each AZ has multiple nodes. Data is replicated across AZs so that losing one AZ does not cause data loss or service interruption.*

**Load balancing**: A load balancer distributes incoming requests across healthy nodes. Algorithms include round-robin, least connections, and weighted routing. Health checks ensure traffic only goes to healthy nodes. For Basic Inventory Management System, the load balancer also considers **API layer (REST service)**
  Purpose: exposes catalog management, stock-in/out when routing.

**Auto-scaling**: The system automatically adds or removes nodes based on metrics (CPU, memory, request rate). Scale-out policies add nodes when load exceeds a threshold; scale-in policies remove nodes during low load. For stateful services like Basic Inventory Management System, scale-out involves rebalancing partitions (moving data and connections to the new node).

**Failover and recovery**: When a node fails, the load balancer detects it (via health checks or failure detection) and stops sending traffic. A new node is provisioned (or a standby is promoted) and begins serving. For Basic Inventory Management System, failover must preserve inventory counts, pricing data, supplier info data — this is achieved through replication with a quorum of healthy nodes.

**Scalability patterns**:

1. **Horizontal partitioning (sharding)**: Split data by a partition key (e.g., user_id, session_id) and distribute partitions across nodes. New nodes take ownership of additional partitions.

2. **Consistent hashing**: Minimize data movement on scale-out — only 1/N of the data moves to the new node. Nodes and partitions are placed on a ring; a request for key X is routed to the next node clockwise from hash(X).

3. **Connection draining**: When scaling in, existing connections are allowed to complete before the node is shut down. For Basic Inventory Management System, this means draining active 1. sessions gracefully.

**Real-world implementations**

- **Netflix OSS (Eureka + Zuul + Ribbon)**: Service discovery with Eureka, edge routing with Zuul, and client-side load balancing with Ribbon. Scales to thousands of instances.
- **Kubernetes HPA + VPA**: Horizontal Pod Autoscaler scales pods based on CPU/memory; Vertical Pod Autoscaler adjusts resource requests based on historical usage.
- **AWS ALB + Auto Scaling Groups**: Application Load Balancer with auto-scaling groups across AZs; health checks replace unhealthy instances automatically.

### Performance and Optimization

**What it means**

Performance and Optimization covers the techniques Basic Inventory Management System uses to achieve low latency, high throughput, and efficient resource usage. This section examines the key performance metrics, bottlenecks, and optimizations specific to the system.

**Why it matters**

Basic Inventory Management System faces competing pressures: users demand low latency, the system must handle high throughput, and infrastructure costs must be controlled. The optimizations applied at the data, compute, and network layers determine whether the system meets its SLA.

**How it works**

**Latency layers**: Latency in Basic Inventory Management System comes from three layers:
1. **Network**: Round-trip time from client to the nearest edge node / load balancer.
2. **Application**: Request processing time on the server (CPU, I/O, lock contention).
3. **Data**: Time to read/write from storage (cache hit vs. database query).

The 99th-percentile latency is the key metric for user-facing systems — it determines the worst-case experience.

**Caching strategies**: Basic Inventory Management System uses multiple cache layers:
- **Edge cache**: Static assets (images, CSS, JS) served from a CDN at the edge. For Basic Inventory Management System, this caches public product info, anonymized restock metrics that doesn't change frequently.
- **Application cache**: In-memory cache (e.g., Redis, Memcached) for frequently accessed data. Cache-aside pattern: application checks cache first, falls back to database on miss.
- **Local cache**: In-process cache (e.g., Caffeine, Guava) for data accessed within a single request. Avoids network round-trips.

**Batching and pipelining**: Basic Inventory Management System batches small operations (e.g., writes, log flushes) to amortize per-operation overhead. Pipelining allows multiple requests to be in flight simultaneously.

```mermaid
flowchart LR
    subgraph "Client Layer"
        Client[Client Request]
    end
    subgraph "Edge Layer"
        Edge[CDN / Edge Cache]
        EdgeCache[(Cached Static Assets)]
    end
    subgraph "Application Layer"
        App[App Server Cluster]
        AppCache[(Redis/Memcached)]
        DB[(Database)]
    end
    Client --> Edge
    Edge -->|Cache Hit| Client
    Edge --> App
    App --> AppCache
    AppCache -->|Hit| App
    AppCache --> DB
    DB --> AppCache
```

*Caching hierarchy: clients first hit the edge CDN/cache; if the response is cached, it is returned immediately. Otherwise, the request reaches the application, which checks its in-memory/application cache (e.g., Redis) before falling back to the database. This minimizes latency from each layer.*

**Connection pooling**: Basic Inventory Management System maintains a pool of database connections to avoid the TCP handshake overhead on every request. Pool size is tuned to match the database's capacity.

**Compression**: Responses are compressed (gzip, zstd) for clients that support it. At the network layer, gRPC uses HPACK header compression.

**Indexing**: Database tables are indexed on frequently queried fields. For Basic Inventory Management System, indexes cover **Inventory store (relational database)**
  Purpose: durable source of truth for and **Reservation service (module)**
  Purpose: the transactional core of checkout s for fast lookups.

**Asynchronous processing**: Non-critical background work (e.g., analytics, cleanup, notifications) is offloaded to message queues and processed asynchronously, keeping the request path fast.

**Resource isolation**: CPU and memory are allocated per service (containers with cgroup limits). This prevents a single misbehaving service from degrading the entire system.

**Metrics for Basic Inventory Management System**:

| Metric | Target | How to Measure |
|---|---|---|
| P99 latency | < 1s | Load test with realistic traffic |
| Throughput | 1K RPS | Request rate under peak load |
| Error rate | < 0.1% | 5xx / total requests |
| Cache hit ratio | > 90% | cache_hits / (cache_hits + misses) |
| Resource utilization | < 80% CPU, < 85% memory | Container metrics |

**Real-world implementations**

- **Google's HTTP Load Balancer**: Global load balancing with edge PoPs; routes users to the nearest healthy backend.
- **Cloudflare**: Edge cache with Argo Smart Routing that dynamically routes traffic to avoid congestion.
- **Redis**: Used as an application cache with configurable eviction policies (LRU, LFU, TTL).

### Encryption and Key Management

**What it means**

Encryption and Key Management in Basic Inventory Management System ensures that data is protected both at rest (stored on disk) and in transit (moving between services). Key management governs how encryption keys are generated, stored, rotated, and accessed — without proper key management, encryption provides a false sense of security.

**Why it matters**

Basic Inventory Management System handles inventory counts, pricing data, supplier info that must be encrypted both at rest and in transit. Scaling Basic Inventory Management System to handle increasing load while maintaining data consistency, low latency, and fault tolerance requires careful key management: keys must be rotated regularly, scoped to prevent cross-contamination, and audited for compliance. A single key compromise could expose sensitive data.

**How it works**

**At-rest encryption**: Data stored in **API layer (REST service)**
  Purpose: exposes catalog management, stock-in/out, **Inventory store (relational database)**
  Purpose: durable source of truth for and databases is encrypted using AES-256-GCM. The Data Encryption Key (DEK) is generated per data partition and encrypted with a Key Encryption Key (KEK) managed by a KMS (AWS KMS, GCP KMS, HashiCorp Vault). Keys are regionally scoped — only data belonging to a region can be decrypted by that region's KEK.

**In-transit encryption**: All inter-service communication uses TLS 1.3 or mTLS for service-to-service auth. Cross-region communication of public product info, anonymized restock metrics uses TLS + optional application-level encryption. inventory counts, pricing data, supplier info is NEVER transmitted in plaintext or across region boundaries.

**Key hierarchy**:
```
Master Key (HSM-backed, KMS-managed)
  └─ KEK (per region, per service)
     └─ DEK (per data partition, rotated every 90 days)
        └─ Data (encrypted with DEK)
```

**Key rotation**: KEKs rotate annually (automatic via KMS); DEKs rotate per object or per 90 days. Applications handle key version headers transparently — a DEK version is stored alongside the encrypted data.

**Cross-region key sharing**: For non-restricted data (public product info, anonymized restock metrics), a shared key is imported into each region's KMS. Restricted data NEVER uses cross-region keys — each region's KMS holds only that region's keys.

```mermaid
graph TD
    subgraph "Region EU KMS"
        DEK_EU[DEK for EU data]
        DataEU[(Encrypted EU Data<br/>AES-256)]
    end
    subgraph "Region US KMS"
        DEK_US[DEK for US data]
        DataUS[(Encrypted US Data<br/>AES-256)]
    end
    KMS[(KMS/HSM<br/>Master Key)]
    KMS -->|unwrap| DEK_EU
    KMS -->|unwrap| DEK_US
    DEK_EU --> DataEU
    DEK_US --> DataUS
    SharedDEK[Shared DEK<br/>for non-restricted global data]
    KMS -->|unwrap shared| SharedDEK
    GlobalData[(Global Index<br/>encrypted with shared key)]
    SharedDEK --> GlobalData
    Client[Client] -->|TLS 1.3| DataEU
    Client -->|TLS 1.3| DataUS
```

*Encryption key hierarchy: master keys are managed by an HSM-backed KMS and never leave the KMS. Each region has its own KEK. Data encryption keys (DEKs) are generated per partition and encrypted with the regional KEK. Only non-restricted global data uses a shared cross-region key. All client traffic uses TLS 1.3.*

**Java/Spring Boot Implementation**

```java
@Service
@RequiredArgsConstructor
public class DataEncryptionService {

    private final AWSKMS kms;
    @Value("${app.region}")
    private String region;
    @Value("${app.encryption.dek-ttl-minutes:1440}")
    private int dekTtlMinutes;

    private final Map<String, SecretKey> dekCache = new ConcurrentHashMap<>();

    public EncryptedData encrypt(String plaintext, String partitionId) {
        SecretKey dek = getOrCreateDek(partitionId);
        byte[] ciphertext = CryptoUtils.encrypt(plaintext.getBytes(StandardCharsets.UTF_8), dek);
        String dekCiphertext = kms.encrypt(EncryptRequest.builder()
            .keyId("arn:aws:kms:" + region + ":master-key")
            .plaintext(SdkBytes.fromByteArray(dek.getEncoded()))
            .build()).ciphertextBlob().asByteArray();
        return new EncryptedData(ciphertext, dekCiphertext, Instant.now());
    }

    private SecretKey getOrCreateDek(String partitionId) {
        return dekCache.computeIfAbsent(partitionId, id -> {
            try {
                return KeyGenerator.getInstance("AES").generateKey();
            } catch (NoSuchAlgorithmException e) {
                throw new IllegalStateException("Cannot generate DEK", e);
            }
        });
    }
}
```

*Spring Boot encryption service: DEKs are cached per-partition with TTL. Each DEK is encrypted via AWS KMS using a regional master key. The encrypted DEK (ciphertext) is stored alongside the data — only the KMS for that region can decrypt it.*

**Real-world implementations**

- **AWS KMS**: Managed HSM-backed key service; supports automatic key rotation and custom key stores.
- **HashiCorp Vault**: Open-source key management; supports transit encryption (encrypt/decrypt without storing keys).
- **Google Cloud KMS**: Hardware-backed key management with IAM-based access control.

### Authentication and Authorization

**What it means**

Authentication and Authorization (AuthN/AuthZ) in Basic Inventory Management System control who can access the system and what they can do. Authentication verifies identity; authorization determines permissions. In a distributed system like Basic Inventory Management System, auth must work across multiple nodes while respecting data boundaries — a user authenticated in one region should not have their session data or tokens replicated to regions where it is not permitted.

**Why it matters**

Basic Inventory Management System must verify identity at the edge and enforce authorization at every service boundary. inventory counts, pricing data, supplier info must be protected — only users with appropriate roles should access it. At the same time, public product info, anonymized restock metrics data should be accessible to a wider audience with minimal friction.

**How it works**

**Authentication (who are you?)**:
- **JWT tokens**: Users authenticate through their home region's identity provider. The region returns a JWT (JSON Web Token) signed by a regional signing key. Tokens include claims like `iss` (issuer region), `sub` (subject/user ID), `home_region`, `roles`, and `exp` (expiry). Tokens are scoped per region — a token issued by region A cannot access restricted data in region B.
- **mTLS for service-to-service**: Internal services authenticate each other using mutual TLS certificates issued by a per-region Certificate Authority (CA). No shared secrets cross region boundaries.
- **Session management**: Sessions are stored regionally (Redis) and never replicated cross-region for restricted data. Session IDs are opaque UUIDs; the session store maps session ID → user context.

**Authorization (what can you do?)**:
- **RBAC (Role-Based Access Control)**: Users are assigned roles per region. Common roles: `region_admin` (full access to region data), `auditor` (read-only audit), `viewer` (read public data only). Roles are stored in the regional database and cached locally for sub-1ms lookups.
- **ABAC (Attribute-Based Access Control)**: Fine-grained permissions based on attributes (e.g., `home_region == request_region AND role == admin`). This allows expressing complex policies like "users can only access restricted data in their home region."
- **Resource-level authorization**: Each request is checked against an ACL (Access Control List) that specifies which roles can access which resources. For Basic Inventory Management System, restricted resources require the `admin` role + matching region.

```mermaid
sequenceDiagram
    participant User as User (Browser)
    participant Edge as Edge Router (Home Region)
    participant Auth as Auth Service
    participant App as App Server

    User->>Edge: HTTPS request + cookie/JWT
    Edge->>Auth: Validate token (local cache)
    Auth-->>Edge: Claims + roles
    Edge->>App: Forward request + context
    App->>App: Check region-scoped ACL
    App-->>Edge: Response (or 403)
```

*Authentication flow: the user's token is validated by the regional auth service (claims cached locally). The edge router forwards the request with the security context. Each app server checks the region-scoped ACL before accessing restricted data.*

**Java/Spring Boot Implementation**

```java
@Service
@RequiredArgsConstructor
public class AuthorizationService {

    private final UserTokenRepository tokenRepository;
    @Value("${app.region}")
    private String currentRegion;

    public boolean canAccessResource(String userId, String resourceRegion,
                                     String action, JWTClaims claims) {
        String userHomeRegion = claims.getStringClaim("home_region");
        List<String> roles = claims.getStringListClaim("roles");

        if (!roles.contains(action)) {
            return false;
        }

        if (resourceRegion.equals(userHomeRegion)) {
            return true;
        }

        if (resourceRegion.equals("global")) {
            return roles.contains("global_reader");
        }

        return false;
    }
}

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1")
public class RegionController {
    private final AuthorizationService authService;

    @GetMapping("/data/{region}/profile")
    public ResponseEntity<?> getProfile(
            @PathVariable String region,
            @RequestHeader("Authorization") String token) {
        JWTClaims claims = JwtUtils.parseAndValidate(token, currentRegion);

        if (!authService.canAccessResource(
                claims.getStringClaim("sub"), region, "read", claims)) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
        }

        return ResponseEntity.ok(profileService.getByRegion(region));
    }
}
```

*Spring Boot authorization service: checks both the user's role and whether the requested resource violates region boundaries. The `canAccessResource` method returns false if a user from region EU tries to access restricted data in region US.*

**Real-world implementations**

- **Auth0**: JWT-based authentication with regional endpoints; supports custom rules for ABAC.
- **Okta**: Multi-region identity management with adaptive MFA and ThreatInsight for anomaly detection.
- **AWS Cognito**: Regional user pools with IAM integration; tokens are region-scoped by default.

### Security Threats and Mitigations

**What it means**

Security Threats and Mitigations catalog the attack surface of Basic Inventory Management System, the most likely threats, and the corresponding defenses. Every distributed system has unique threat vectors — Basic Inventory Management System is no exception.

**Why it matters**

Basic Inventory Management System handles inventory counts, pricing data, supplier info that attackers might target. Scaling Basic Inventory Management System to handle increasing load while maintaining data consistency, low latency, and fault tolerance expands the attack surface: more nodes, more network paths, more failure modes. Without proper threat modeling, a single vulnerability could expose sensitive data across the entire system.

**Threat model**:

| Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Data exfiltration (cross-region) | High | Critical | Region-scoped keys, no cross-region replication of restricted data |
| Man-in-the-middle (inter-service) | Medium | High | mTLS between all services |
| Replay attacks | Medium | High | Token expiry + nonce |
| DDoS at the edge | High | High | Rate limiting + edge filtering (Cloudflare, AWS Shield) |
| PII leakage in logs | High | High | PII redaction + field-level access control |
| Session hijacking | Medium | Medium | Short-lived tokens + IP binding |
| Privilege escalation | Low | Critical | Least-privilege RBAC + audit logs |
| Cache poisoning | Low | Medium | Cache invalidation on write + signed cache keys |

**How it works**

**Data exfiltration prevention**: Basic Inventory Management System enforces data residency by design — inventory counts, pricing data, supplier info is never replicated cross-region. The replication layer checks a data classification label before allowing cross-region copy. A database-level policy (e.g., PostgreSQL RLS) also blocks cross-region queries for restricted partitions.

**mTLS enforcement**: All service-to-service communication uses mutual TLS. Certificates are issued by a per-region CA and rotated every 30 days. Services must present a valid certificate to communicate — no plaintext connections are allowed.

**PII redaction**: Application logs are scanned for PII patterns (email, phone, credit card) using an automated redaction layer (e.g., AWS Macie, Google DLP). public product info, anonymized restock metrics is logged freely; restricted fields are masked or dropped before logging.

```mermaid
graph TD
    subgraph "Threat Surface"
        Client[Client]
        Edge[Edge Router / WAF]
        App[App Server]
        DB[(Database)]
        Cache[(Cache)]
        Logs[Log Store]
    end

    Client -->|HTTPS| Edge
    Edge -->|mTLS| App
    App -->|mTLS| DB
    App -->|Read| Cache
    App -->|Write| DB
    App -->|Log| Logs

    subgraph "Mitigations"
        WAF[AWS WAF /<br/>Cloudflare]
        DLP[PII Redaction<br/>(Macie/DLP)]
        FIM[File Integrity<br/>Monitoring]
    end

    Edge -.-> WAF
    Logs -.-> DLP
    DB -.-> FIM
```

*Threat mitigation diagram: the WAF at the edge blocks DDoS and injection attacks. mTLS protects all service-to-service communication. PII redaction scans logs before storage. File integrity monitoring alerts on database tampering.*

**Audit trail**: All security-relevant events (auth, data access, config changes) are written to an append-only audit log with cryptographic integrity (HMAC per entry). The log covers inventory counts, pricing data, supplier info access — who accessed what, when, and from where.

**Real-world implementations**

- **Cloudflare**: Zero-trust model (All Connections to All Networks) with mTLS everywhere; uses GeoIP blocking and rate limiting for DDoS mitigation.
- **Google BeyondCorp**: Zero-trust network security model; all access is authenticated and authorized at the request level.

### Observability and Logging

**What it means**

Observability and Logging in Basic Inventory Management System provide visibility into system behavior through three pillars: **metrics** (aggregates and counters), **logs** (structured event records), and **traces** (distributed request timelines). Together, these signals allow operators to debug issues, detect anomalies, and verify SLA compliance.

**Why it matters**

Distributed systems like Basic Inventory Management System are inherently opaque — failures can cascade across services in unexpected ways. Without good observability, a single slow dependency can cause widespread timeouts that are nearly impossible to diagnose. Scaling Basic Inventory Management System to handle increasing load while maintaining data consistency, low latency, and fault tolerance makes observability even more critical: operators need to see cross-region latency, regional failures, and data-residency violations.

**How it works**

**Metrics**: Basic Inventory Management System instruments every service with Prometheus-style metrics:
- **Request rate, error rate, duration (the "RED" metrics)**: Tracks per-endpoint HTTP latency and error counts.
- **System metrics**: CPU, memory, disk I/O, network throughput per node.
- **Business metrics**: For Basic Inventory Management System, this includes metrics like "**Inventory store (relational database)**
  Purpose: durable source of truth for fill rate" and "reservation conflict rate".

Metrics are aggregated in a time-series database (Prometheus, VictoriaMetrics) and visualized in Grafana dashboards with alerts via PagerDuty.

**Logs**: Basic Inventory Management System uses structured logging (JSON format) with standardized fields:
- `timestamp`: ISO 8601 UTC
- `level`: DEBUG, INFO, WARN, ERROR
- `service`: originating service name
- `trace_id`: distributed trace identifier (for correlation)
- `span_id`: current operation span
- `region`: the region that processed the request
- `data_class`: RESTRICTED or NON_RESTRICTED

inventory counts, pricing data, supplier info access is logged with full context (user, action, resource). public product info, anonymized restock metrics logs are aggregated and may have reduced retention.

**Distributed tracing**: Every request is assigned a trace ID at the edge. The trace propagates through all downstream services via HTTP headers. A tracing backend (Jaeger, Tempo, Zipkin) reconstructs the full request timeline, showing latency at each hop. For Basic Inventory Management System, traces include region boundaries — a cross-region call is annotated as such.

```mermaid
graph TD
    subgraph "Region EU"
        AppEU[App Server EU]
        PromEU[Prometheus EU]
        LokiEU[Loki Logs EU]
    end
    subgraph "Region US"
        AppUS[App Server US]
        PromUS[Prometheus US]
        LokiUS[Loki Logs US]
    end
    subgraph "Global"
        Grafana[Grafana Dashboard]
        Tempo[Tempo Tracing]
        Alertmanager[(Alertmanager)]
    end
    AppEU -->|metrics| PromEU
    AppEU -->|logs| LokiEU
    AppUS -->|metrics| PromUS
    AppUS -->|logs| LokiUS
    PromEU -->|remote write| Grafana
    PromUS -->|remote write| Grafana
    LokiEU --> Grafana
    LokiUS --> Grafana
    AppEU -->|traces| Tempo
    AppUS -->|traces| Tempo
    PromEU --> Alertmanager
    PromUS --> Alertmanager
```

*Observability architecture: each region runs its own Prometheus (metrics) and Loki (logs) instances. A global Grafana instance queries all regional backends. Traces are collected centrally in Tempo. Alerts fire from each region's Prometheus to Alertmanager.*

**Alerting**: Basic Inventory Management System defines SLO-based alerts:
- **Latency**: P99 > 1s for 5 minutes → page.
- **Error rate**: > 1% for 10 minutes → page.
- **Availability**: < 99.5% for 15 minutes → page.
- **Data residency violation**: any restricted data detected outside its region → critical page.

**Java/Spring Boot Implementation**

```java
@Component
@RequiredArgsConstructor
@Slf4j
public class ObservabilityContext {

    @Value("${app.region}")
    private String region;

    public void logAccess(String userId, String resource, String action,
                          boolean restricted) {
        log.info("access_event userId={} resource={} action={} region={} data_class={}",
            userId, resource, action, region, restricted ? "RESTRICTED" : "NON_RESTRICTED");
    }
}

@RestController
@RequiredArgsConstructor
@Slf4j
public class ApiController {
    private final ObservabilityContext obs;
    private final UserService userService;

    @GetMapping("/api/v1/profile")
    public ResponseEntity<ProfileResponse> getProfile(
            @AuthenticationPrincipal UserDetails user) {
        String traceId = MDC.get("traceId");
        long start = System.nanoTime();

        try {
            ProfileResponse response = userService.getProfile(user.getId());
            obs.logAccess(user.getId(), "profile", "read", true);

            return ResponseEntity.ok(response);
        } finally {
            long durationMs = (System.nanoTime() - start) / 1_000_000;
            log.info("profile_read traceId={} latencyMs={} region={}",
                traceId, durationMs, obs.region);
        }
    }
}
```

*Spring Boot observability: the `ObservabilityContext` logs structured access events with data classification. The controller records latency and trace ID for every request, enabling SLO-based alerting.*

**Real-world implementations**

- **Netflix OSS (Atlas + Zipkin + Servo)**: Metrics via Atlas, traces via Zipkin, instrumented via Servo. Scales to over 700 billion requests/day.
- **Google SRE Workbook**: Comprehensive observability with SLI/SLO/SLI definition; uses Borgmon for metrics and Dapper for tracing.
- **AWS Observability**: CloudWatch for metrics, X-Ray for tracing, CloudWatch Logs for structured logs.

### Real-World Implementations

**Basic Inventory Management System in production**

- **Basic Inventory Management System platforms**: widely used basic inventory management system platform

**Key takeaways**

- Scalability patterns proven in production at scale
- Common pitfalls and how to avoid them
- Integration with existing infrastructure and monitoring

### Java and Spring Boot Implementation Guide

Spring Boot 3.x, Java 17+, Spring Data JPA on PostgreSQL. Constructor injection everywhere; DTOs are records; configuration via `@Value`.

**Configuration**

```java
@Configuration
public class InventoryConfig {

    @Value("${inventory.reservation-ttl:PT15M}")
    private Duration reservationTtl;

    @Value("${inventory.expiry-job.batch-size:500}")
    private int expiryBatchSize;

    @Bean
    public Duration reservationTtl() {
        return reservationTtl;
    }

    @Bean
    public int expiryBatchSize() {
        return expiryBatchSize;
    }
}
```

**Entities**

```java
@Embeddable
public record StockLevelId(String sku, String warehouseId) implements Serializable {
}

@Entity
@Table(name = "stock_levels")
public class StockLevel {

    @EmbeddedId
    private StockLevelId id;

    @Column(nullable = false)
    private int onHand;

    @Column(nullable = false)
    private int reserved;

    @Version
    private int version;

    protected StockLevel() {
    }

    public StockLevel(StockLevelId id) {
        this.id = id;
    }

    public int available() {
        return onHand - reserved;
    }

    public void receive(int qty) {
        if (qty <= 0) throw new IllegalArgumentException("qty must be positive");
        onHand += qty;
    }

    public void reserve(int qty) {
        if (available() < qty) {
            throw new InsufficientStockException(id.sku(), available());
        }
        reserved += qty;
    }

    public void confirmReservation(int qty) {
        if (reserved < qty) throw new IllegalStateException("reserved < qty");
        reserved -= qty;
        onHand -= qty;
    }

    public void releaseReservation(int qty) {
        if (reserved < qty) throw new IllegalStateException("reserved < qty");
        reserved -= qty;
    }

    public StockLevelId getId() {
        return id;
    }
}

@Entity
@Table(name = "reservations")
public class Reservation {

    @Id
    private String reservationId;

    @Column(nullable = false)
    private String sku;

    @Column(nullable = false)
    private String warehouseId;

    @Column(nullable = false)
    private String orderId;

    @Column(nullable = false)
    private int quantity;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Status status;

    @Column(nullable = false)
    private Instant expiresAt;

    @Column(nullable = false)
    private Instant createdAt;

    public enum Status { ACTIVE, CONFIRMED, RELEASED, EXPIRED }

    protected Reservation() {
    }

    public static Reservation active(String sku, String warehouseId, String orderId,
                                     int qty, Duration ttl) {
        Reservation r = new Reservation();
        r.reservationId = "rsv_" + UUID.randomUUID();
        r.sku = sku;
        r.warehouseId = warehouseId;
        r.orderId = orderId;
        r.quantity = qty;
        r.status = Status.ACTIVE;
        r.createdAt = Instant.now();
        r.expiresAt = r.createdAt.plus(ttl);
        return r;
    }

    public void confirm() {
        if (status != Status.ACTIVE) {
            throw new ReservationStateException(reservationId, status, Status.CONFIRMED);
        }
        if (Instant.now().isAfter(expiresAt)) {
            throw new ReservationExpiredException(reservationId);
        }
        status = Status.CONFIRMED;
    }

    public void release(Status terminal) {
        if (status != Status.ACTIVE) {
            return;   // idempotent: releasing a terminal reservation is a no-op
        }
        status = terminal;
    }

    public boolean isActive() {
        return status == Status.ACTIVE;
    }

    // getters omitted for brevity
}
```

**DTOs (records) and validation**

```java
public record CreateProductRequest(
        @NotBlank @Pattern(regexp = "^[A-Z0-9-]{3,32}$") String sku,
        @NotBlank String name,
        @NotNull @Positive Money price,
        @NotBlank String category,
        @PositiveOrZero int reorderPoint,
        @PositiveOrZero int lowStockThreshold) {
}

public record Money(@Positive long amount, @Size(min = 3, max = 3) String currency) {
}

public record StockChangeRequest(
        @Positive int quantity,
        @NotBlank String reason,
        @NotBlank String referenceId,
        String warehouseId) {
}

public record ReserveRequest(
        @NotBlank String orderId,
        @NotBlank String sku,
        @Positive int quantity,
        @NotBlank String warehouseId,
        @PositiveOrZero Integer ttlSeconds) {
}

public record AvailabilityResponse(
        String sku, String warehouseId, int onHand, int reserved, int available) {
}

public record ReservationResponse(
        String reservationId, String orderId, String sku,
        int quantity, String status, Instant expiresAt) {
}
```

**Repository and core reservation service**

```java
public interface StockLevelRepository extends JpaRepository<StockLevel, StockLevelId> {

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT s FROM StockLevel s WHERE s.id = :id")
    Optional<StockLevel> findByIdForUpdate(@Param("id") StockLevelId id);

    @Modifying
    @Query("""
            UPDATE StockLevel s SET s.reserved = s.reserved + :qty
            WHERE s.id = :id AND s.onHand - s.reserved >= :qty
            """)
    int tryReserve(@Param("id") StockLevelId id, @Param("qty") int qty);

    @Query("""
            SELECT s FROM StockLevel s
            JOIN Product p ON p.sku = s.id.sku
            WHERE s.onHand - s.reserved <= p.reorderPoint AND p.active = true
            """)
    List<StockLevel> findAllBelowReorderPoint();
}

@Service
public class ReservationService {

    private final StockLevelRepository stockLevels;
    private final ReservationRepository reservations;
    private final MovementRepository movements;
    private final OutboxRepository outbox;
    private final Duration reservationTtl;

    public ReservationService(StockLevelRepository stockLevels,
                              ReservationRepository reservations,
                              MovementRepository movements,
                              OutboxRepository outbox,
                              Duration reservationTtl) {
        this.stockLevels = stockLevels;
        this.reservations = reservations;
        this.movements = movements;
        this.outbox = outbox;
        this.reservationTtl = reservationTtl;
    }

    @Transactional
    public Reservation reserve(String sku, String warehouseId, String orderId, int qty) {
        var existing = reservations.findActiveByOrderIdAndSku(orderId, sku);
        if (existing.isPresent()) {
            return existing.get();   // idempotent replay for a duplicate order event
        }
        StockLevelId id = new StockLevelId(sku, warehouseId);
        int updated = stockLevels.tryReserve(id, qty);   // atomic compare-and-set
        if (updated == 0) {
            int available = stockLevels.findById(id).map(StockLevel::available).orElse(0);
            throw new InsufficientStockException(sku, available);
        }
        Reservation r = Reservation.active(sku, warehouseId, orderId, qty, reservationTtl);
        movements.append(sku, warehouseId, 0, "RESERVATION_CREATED", orderId);
        return reservations.save(r);
    }

    @Transactional
    public Reservation confirm(String reservationId) {
        Reservation r = reservations.findById(reservationId)
                .orElseThrow(() -> new ReservationNotFoundException(reservationId));
        if (r.getStatus() == Reservation.Status.CONFIRMED) {
            return r;   // idempotent duplicate confirm
        }
        r.confirm();    // validates ACTIVE + unexpired, else throws
        StockLevel level = stockLevels
                .findByIdForUpdate(new StockLevelId(r.getSku(), r.getWarehouseId()))
                .orElseThrow();
        level.confirmReservation(r.getQuantity());
        movements.append(r.getSku(), r.getWarehouseId(), -r.getQuantity(), "SALE", r.getOrderId());
        maybeEmitLowStock(r.getSku(), level);
        return r;
    }

    @Transactional
    public Reservation release(String reservationId, Reservation.Status terminal) {
        Reservation r = reservations.findById(reservationId)
                .orElseThrow(() -> new ReservationNotFoundException(reservationId));
        if (!r.isActive()) {
            return r;   // idempotent
        }
        StockLevel level = stockLevels
                .findByIdForUpdate(new StockLevelId(r.getSku(), r.getWarehouseId()))
                .orElseThrow();
        level.releaseReservation(r.getQuantity());
        r.release(terminal);
        movements.append(r.getSku(), r.getWarehouseId(), 0, "RESERVATION_RELEASED", r.getOrderId());
        return r;
    }

    private void maybeEmitLowStock(String sku, StockLevel level) {
        // alert on the crossing only; re-armed when stock rises above the point again
        if (level.available() <= products.reorderPointOf(sku) && !alerts.isAlerted(sku)) {
            outbox.append(new LowStockCrossed(sku, level.getId().warehouseId(), level.available()));
            alerts.markAlerted(sku);
        }
    }
}
```

**REST controller and global error handling**

```java
@RestController
@RequestMapping("/api/v1")
public class InventoryController {

    private final ReservationService reservationService;
    private final StockService stockService;

    public InventoryController(ReservationService reservationService, StockService stockService) {
        this.reservationService = reservationService;
        this.stockService = stockService;
    }

    @PostMapping("/inventory/{sku}/stock-in")
    public AvailabilityResponse stockIn(@PathVariable String sku,
                                        @Valid @RequestBody StockChangeRequest request,
                                        @RequestHeader("Idempotency-Key") String idempotencyKey) {
        return stockService.stockIn(sku, request, idempotencyKey);
    }

    @PostMapping("/reservations")
    public ResponseEntity<ReservationResponse> reserve(@Valid @RequestBody ReserveRequest request,
                                                       @RequestHeader("Idempotency-Key") String key) {
        Reservation r = reservationService.reserve(
                request.sku(), request.warehouseId(), request.orderId(), request.quantity());
        return ResponseEntity.status(HttpStatus.CREATED).body(ReservationResponse.from(r));
    }

    @PostMapping("/reservations/{id}/confirm")
    public ReservationResponse confirm(@PathVariable String id,
                                       @RequestHeader("Idempotency-Key") String key) {
        return ReservationResponse.from(reservationService.confirm(id));
    }

    @PostMapping("/reservations/{id}/release")
    public ReservationResponse release(@PathVariable String id,
                                       @RequestHeader("Idempotency-Key") String key) {
        return ReservationResponse.from(
                reservationService.release(id, Reservation.Status.RELEASED));
    }
}

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(InsufficientStockException.class)
    public ResponseEntity<ApiError> insufficientStock(InsufficientStockException e) {
        return ResponseEntity.status(HttpStatus.CONFLICT)
                .body(new ApiError("INSUFFICIENT_STOCK", e.getMessage()));
    }

    @ExceptionHandler(ReservationExpiredException.class)
    public ResponseEntity<ApiError> expired(ReservationExpiredException e) {
        return ResponseEntity.status(HttpStatus.GONE)
                .body(new ApiError("RESERVATION_EXPIRED", e.getMessage()));
    }

    @ExceptionHandler(ReservationStateException.class)
    public ResponseEntity<ApiError> badState(ReservationStateException e) {
        return ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY)
                .body(new ApiError("INVALID_STATE_TRANSITION", e.getMessage()));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ApiError> validation(MethodArgumentNotValidException e) {
        List<FieldIssue> fields = e.getBindingResult().getFieldErrors().stream()
                .map(f -> new FieldIssue(f.getField(), f.getDefaultMessage()))
                .toList();
        return ResponseEntity.badRequest().body(new ApiError("VALIDATION_FAILED", fields));
    }

    public record ApiError(String error, Object details) {
    }

    public record FieldIssue(String field, String issue) {
    }
}
```

**Expiry job and low-stock worker**

```java
@Component
public class ReservationExpiryJob {

    private final ReservationRepository reservations;
    private final ReservationService reservationService;
    private final int batchSize;

    public ReservationExpiryJob(ReservationRepository reservations,
                                ReservationService reservationService,
                                int expiryBatchSize) {
        this.reservations = reservations;
        this.reservationService = reservationService;
        this.batchSize = expiryBatchSize;
    }

    @Scheduled(fixedDelayString = "${inventory.expiry-job.interval:PT1M}")
    public void releaseExpired() {
        // FOR UPDATE SKIP LOCKED inside this query: safe to run on every app instance
        List<String> expiredIds = reservations.findExpiredActiveIds(Instant.now(), batchSize);
        for (String id : expiredIds) {
            try {
                reservationService.release(id, Reservation.Status.EXPIRED);
            } catch (Exception e) {
                // one poison row must not block the batch; it will be retried next run
                log.warn("Failed to expire reservation {}", id, e);
            }
        }
    }
}
```

Key implementation rules: every public service method that mutates stock is `@Transactional`; the expiry job's release is per-row so a crash mid-batch leaves the rest for the next run; `findExpiredActiveIds` uses `FOR UPDATE SKIP LOCKED` so horizontally scaled instances do not fight over the same rows; and all amounts, TTLs, and batch sizes come from `@Value`/config — never hard-coded.

---

### Interview Questions and Answers

**Beginner**

- **Q: What is the difference between stock on hand and available-to-promise (ATP)?**
  **A:** Stock on hand is the physical count physically present. ATP is what you can still promise to customers: `on_hand − allocated − queued + inbound_in_window`. They differ because of reservations — stock may read 100 but ATP is near zero if 95 units are reserved. The trap is treating them as the same and overselling.

- **Q: How do you prevent selling stock you don't have?**
  **A:** Reserve before you confirm, atomically. The sale flow: `SELECT FOR UPDATE` the SKU row, assert `quantity_available ≥ qty`, insert a reservation row that decrements available and increments allocated, commit. The check and reservation are one transaction; nothing can slip in between. Common mistake: only a `SELECT` of the balance and trusting that nothing else sells in the 5 ms before your insert.

- **Q: What is an optimistic lock (`@Version`) good for here?**
  **A:** It lets multiple transactions update stock concurrently and detects conflicts after the fact: each transaction writes `WHERE version = oldVersion`; if the row changed, the update affects 0 rows and you retry. Good for low-contention SKUs (the 99% of catalog that isn't a limited drop).

**Intermediate**

- **Q: Compare optimistic and pessimistic locking for oversell prevention.**
  **A:** Optimistic (`@Version` + retry) is cheap and scales on low-contention items but turns into a retry storm under a flash sale. Pessimistic (`SELECT ... FOR UPDATE`) serializes sellers on the row — safe, but throughput is capped at what one locked transaction at a time can do. Choice depends on contention: most catalog → optimistic; lottery tickets / limited drops → pessimistic. Expected follow-up: *why not always pessimistic?* — because it serializes even uncontended sales, throttling the common case to protect the rare one.

- **Q: How do you handle reservation expiry so stock isn't locked forever?**
  **A:** Every reservation carries a TTL. A scheduled `FOR UPDATE SKIP LOCKED` job scans `WHERE expires_at < now() AND status = 'ACTIVE'` and releases matched reservations back to available. `SKIP LOCKED` is the correctness detail — without it, concurrent worker instances re-select and double-release the same rows. The job is idempotent per row (release is a no-op if already released).

- **Q: Walk the purchase flow from "add to cart" through shipment.**
  **A:** Add-to-cart does *nothing* to inventory (the cart is not a reservation). At checkout, a `ReservationService.reserve(orderItems)` runs in a transaction: check ATP, insert reservations, decrement ATP by the reserved qty. Reservations hold the stock for a TTL. When warehouse confirms the pick, `reserve → confirm` decrements allocated and, on shipment, frees it. If the pick can't fulfill, the reservation is released and the customer is notified. The key invariant: committed stock is only decremented at shipment, not at cart.

- **Q: Why use a read replica, and what's the hazard?**
  **A:** For catalog browsing and balance reads that tolerate seconds of lag, offloading the primary. The hazard is read-after-write on the critical path: a customer buys the last unit, refreshes the catalog from the replica, and still sees it "in stock" — an oversell-by-lag. Mitigation: read-your-writes routing for authenticated sessions near checkout, or always re-check ATP against the primary at the moment of purchase (the only place stale reads are dangerous).

**Advanced**

- **Q: Design allocation across multiple warehouses.**
  **A:** Given `Qty 5` and stock spread (WH-A: 3, WH-B: 2), the allocator returns `(WH-A, 3), (WH-B, 2)` and creates a reservation in each warehouse's shard. Inputs: stock per warehouse, shipping distance/cost, capacity, policy. Single-source minimizes shipping cost; split-source minimizes delivery time. Allocations are batched per pick wave for throughput; availability is re-checked at pick time and short-ships are possible. Expected discussion: the race where a concurrent order wins stock — resolved by idempotent reserve-at-promise plus re-check-at-pick.

- **Q: When do you need lot/batch and expiry tracking?**
  **A:** For FIFO/LIFO rotation and for industries where expiry matters (food, pharma, cosmetics). The model adds `lots(lot_id, sku_id, qty, expires_at, received_at)`; FIFO allocation picks the oldest non-expired lot first. This is a business/finance requirement that forces per-lot tracking — a system that tracks only aggregate SKU quantities cannot satisfy it, and that's a design failure, not a feature gap.

- **Q: How do you run a flash sale of 100,000 limited items without overselling under thundering-herd traffic?**
  **A:** Pre-create the 100,000 reservations in one transaction before the sale — the stock is *already* reserved, never check-and-take at request time. The sale endpoint then does an atomic, idempotent decrement guarded by a Lua script: `if redis.call("GET", stock) >= 0 then return redis.call("DECR", stock) else return -1 end`, returning sold-out when -1. The decrement is the only hot path, and it's lock-free. Discussion points: why a bare `DECR` that goes negative is the failure mode, why idempotency keys prevent double-buy on retry, and why the durable DB reservation is the source of truth (Redis is just the rate-limit gate).

**Senior / System Design**

- **Q: Design a global inventory platform. How do you partition the data?**
  **A:** Keep the invariants: atomic reservation per SKU, no cross-warehouse overselling, graceful degradation. Regional inventory services, each owning SKU-hash shards for its geography, with a global coordination layer (strongly consistent store or a dedicated reservation service) for cross-region allocation and the shared reserved total. Partitioning by SKU hash gives even distribution; hot SKUs are isolated or rate-limited. Expected discussion: CAP — a global flash sale chooses consistency and may turn a region away rather than oversell; regional write models stay eventually consistent with the global reserved ledger, updated in the same transaction as the local reservation.

- **Q: Single global stock table vs per-warehouse table with a materialized total — trade-offs?**
  **A:** A single global table is simple and consistent but is one write shard that caps throughput (one hot row per SKU under load). Per-warehouse rows plus a materialized total is write-scalable (warehouses update independently) but requires reconciliation (totals are rebuildable from warehouse rows; drift is a scheduled job alert). Default recommendation: per-warehouse-per-SKU as source of truth, materialized totals as an invalidated cache — and never allow direct updates to the cached total.

- **Q: How do you observe and alert on inventory health day-to-day?**
  **A:** Reservation success rate vs. stockouts (business truth), reservation expiry rate (a spike means checkout is hanging), oversell attempts blocked at the check (correctness), reconciliation drift between `current_stock` and the event-stream fold (data integrity — must be zero, always alert), and warehouse pick variance vs. reserved (operational). The reconciliation job is the one metric that must be continuously zero — every other signal can be gamed, but "stock according to events" does not lie.

- **Q: What are the most common mistakes candidates make on this problem?**
  **A:** (1) Confusing stock on hand with ATP. (2) Check-then-reserve with no atomicity — the classic oversell race. (3) No reservation expiry so stock is locked forever into abandoned carts. (4) Reading stock from a replica right after writing it and trusting it for availability. (5) Offset pagination on pick lists (skips/duplicates under concurrent picks). (6) No lot/batch or expiry tracking where the domain requires FIFO/rotation. (7) Storing the current count as source of truth instead of deriving it from events (kills the audit trail).

---
