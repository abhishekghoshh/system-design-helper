# Design a Simple Attendance Tracking System

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
15. [API Design and API Contract](#api-design-and-api-contract)
16. [Data Modeling](#data-modeling)
17. [High-Level Design](#high-level-design)
18. [Deep Dive](#deep-dive)
19. [Java and Spring Boot Implementation Guide](#java-and-spring-boot-implementation-guide)
20. [Interview Questions and Answers](#interview-questions-and-answers)

---

### Introduction and Problem Statement

Design a simple attendance tracking system for an organization where employees/students check in and check out each day, and admins can view attendance reports.

Attendance tracking sounds trivial — "just store two timestamps" — but it sits at the intersection of several classic system-design problems: write correctness under retries (a double-tap must not create two records), time semantics (timezones, DST, night shifts), trust (server clock vs. client clock, location spoofing), and read/write asymmetry (cheap writes, but reports that aggregate months of rows). It is a favorite "basic" interview question precisely because it tests whether a candidate can find the hidden complexity in a simple-sounding requirement.

**What problem it solves**

- Organizations need a trustworthy record of who was present, when, and for how long, for payroll, compliance, and academic credit.
- Manual registers and spreadsheets are error-prone, easy to manipulate, and impossible to audit.
- Managers need aggregated views (present/absent/late counts, hours worked) without reading raw events one by one.
- HR needs corrections to be possible but always traceable (who changed what, when, and why).

**Real-life use cases**

- **Corporate offices**: employees check in via a mobile app or badge reader; HR exports monthly hours to payroll.
- **Factories and shift work**: kiosk-based punches at the plant gate, including night shifts that cross midnight.
- **Schools and universities**: students check in per class session; faculty view absence reports.
- **Field workforce**: delivery or service staff check in from job sites with GPS coordinates attached.
- **Co-working spaces**: members check in to track usage for billing.

```mermaid
flowchart LR
    Employee["Employee / Student"] -->|"check-in / check-out"| Client["Mobile / Web / Kiosk"]
    Client --> API["Attendance API"]
    API --> DB[("Attendance Store")]
    Admin["Admin / Manager"] --> API
    API --> Reports["Reports and Dashboards"]
```

The diagram shows the core shape of the system: many users produce a small number of write events per day through a single API, while admins consume aggregated read views over the same data.

---

### Functional Requirements

1. **Check-in**: a user records the start of their work/study day. The system stamps the event with the server's time and rejects the request if the user already has an open (not yet checked-out) record for that day.
2. **Check-out**: a user records the end of their day. The system closes the open record and computes worked duration.
3. **View own attendance history**: a user can list their records for a date range, including worked hours and status (present, late, half-day).
4. **Admin views**: an admin can view attendance for a team or the whole organization over a date range.
5. **Manual corrections**: an admin (or a user with approval) can correct a wrong or missing punch; every correction is stored with the old value, new value, reason, and approver.
6. **Basic reports**: per team and date range, present/absent/late counts, average worked hours, and per-user summaries.
7. **Auto-close**: records still open at end of day are closed by a scheduled job and flagged so missed check-outs are visible instead of silently wrong.
8. **Idempotent punches**: retrying a check-in (network retry, double tap) returns the original result instead of creating duplicates or errors.

Out of scope for the basic design (mention as extensions in interviews): leave management integration, shift scheduling, biometric devices, geofencing enforcement, payroll export.

---

### Non-Functional Requirements

- **Scale**: thousands of users per organization; exactly one check-in/check-out event pair per user per day, so the write volume is small and predictable.
- **Write latency**: check-in/check-out acknowledged in < 200 ms at p99 — punches happen in burst windows (8:30–10:00 AM) and users expect instant feedback at the door.
- **Read latency**: own-history reads < 200 ms; team reports < 2 s; reports may hit precomputed aggregates, never raw scans.
- **Consistency**: strong consistency on the "one open record per (user, date)" rule — a user must not be able to check in twice without checking out first. Reports can be eventually consistent (stale by minutes).
- **Availability**: 99.9% for the check-in path; a failed check-in directly blocks employees at the door, so writes matter more than report reads.
- **Durability**: once acknowledged, a punch must never be lost — it feeds payroll. RPO = 0 for punch events.
- **Auditability**: corrections and admin actions are immutably logged for compliance.
- **Security**: authenticated users only; users see only their own records; admins are scoped to their organization (multi-tenancy isolation).

---

### Capacity Estimation

Back-of-envelope math for one mid-size organization; multi-tenant SaaS numbers follow.

**Assumptions**

- 10,000 employees in the organization.
- 2 punch events per user per day (one check-in, one check-out).
- 22 working days per month, ~250 working days per year.

**Write QPS**

- Events per day = 10,000 users × 2 = 20,000 events/day.
- Spread evenly that is ~0.25 QPS, but punches are extremely bursty: 80% of check-ins land in a 90-minute morning window.
- Average in window = 16,000 events / 5,400 s ≈ 3 QPS. Peak (everyone at 9:00 sharp) ≈ 5× average ≈ **15 QPS writes**.
- A single modest application server and one relational database handle this trivially; the design challenge is correctness, not throughput.

**Read QPS**

- Self history: assume 10% of users check history daily → 1,000 reads/day.
- Reports: 50 managers × 10 report views/day = 500 reads/day.
- Peak read load ≈ **5 QPS** — negligible, but report queries must stay fast via precomputed aggregates.

**Storage**

- Record size estimate: UUIDs (16 B × 2), two timestamps (8 B × 2), date (4 B), status/source enums (~10 B), worked minutes (4 B), audit timestamps (16 B) ≈ **~120 B raw, ~250 B with index overhead**.
- Per year: 10,000 users × 250 days × 250 B ≈ **625 MB/year** including indexes.
- Ten years of history ≈ 6 GB — a single relational instance holds it comfortably. Archival is a policy decision, not a capacity necessity.

**Bandwidth**

- A punch request/response is ~1 KB JSON. 20,000 events/day ≈ 40 MB/day of traffic — irrelevant. Even 100 orgs on one platform stay under a few GB/day.

**Multi-tenant SaaS extrapolation**

- 500 organizations × 10,000 users = 5 M users → 10 M events/day, peak ≈ 7,500 QPS writes, ≈ 2.5 TB of records over 10 years.
- This is where partitioning by `org_id` (tenant), read replicas for reports, and queue-based aggregation become necessary. State these numbers in an interview to show you know when the simple design stops being sufficient.

**Conclusion**: for the basic system, one PostgreSQL/MySQL primary with proper unique indexes plus a nightly aggregation job is enough. Invest design effort in correctness (uniqueness, timezones, idempotency) rather than scale machinery.

---

### Characteristics

Each characteristic is explained in detail.

- **Append-oriented event log**
  The system's source of truth is a stream of punch events (or records derived from them). Attendance is fundamentally event data: something happened at a time. Modeling it as events keeps corrections and audits natural, because you never overwrite history — you append compensating entries.

- **Low write volume, high correctness bar**
  Only two writes per user per day, but each one feeds payroll. A lost or duplicated punch has financial and legal consequences, so durability and uniqueness matter more than raw throughput.

- **Bursty traffic pattern**
  Load concentrates in short morning and evening windows. Capacity planning must use peak-window QPS, not daily averages, and the write path must stay simple enough to serve the burst without queueing delays.

- **Time-zone and calendar sensitivity**
  "A day" is a local concept. The system must convert instants to local work dates per organization, survive DST transitions, and handle shifts crossing midnight. This is the most common source of real-world bugs in attendance systems.

- **Trust asymmetry between client and server**
  Clients are untrusted: a user can change their phone clock to backdate a punch. The server clock is the authority; client timestamps are metadata used only for offline reconciliation.

- **Read/write asymmetry**
  Writes are tiny and simple; reads (monthly reports across teams) are aggregations over millions of rows. The design separates the write path from a precomputed reporting path (CQRS-style) so reports never scan raw events.

- **Strong uniqueness invariant**
  At most one open record per user per day. This invariant is enforced by the database (unique constraint), not by application code, because application-level checks race under concurrent requests.

- **Human-in-the-loop corrections**
  Real deployments always need corrections (forgot to check out, kiosk offline). The system treats corrections as first-class, approval-gated, audited operations rather than ad-hoc database edits.

---

### Components

Each component is listed with its purpose, responsibilities, and relationship to other components.

- **Client applications (mobile, web, kiosk)**
  Capture check-in/check-out intent, attach optional context (GPS, device id, client-captured time), and queue punches locally when offline. They never decide the official time; they display what the server confirms. Real-world example: the greytHR or Zoho People mobile apps.

- **API layer / gateway**
  Authenticates requests (JWT/OAuth2), enforces rate limits and input validation, and routes to services. It is the only public entry point, which centralizes auth and tenancy resolution.

- **Attendance service (write path)**
  Owns the punch state machine: validates the request, enforces the one-open-record rule, stamps server time, persists the record transactionally, and emits a domain event. This is the consistency-critical component.

- **Reporting service (read path)**
  Serves history and aggregate reports from precomputed summary tables, never from raw event scans. It scales independently of the write path and can sit behind read replicas.

- **Relational database**
  System of record. Holds `attendance_records`, `attendance_corrections`, and `daily_attendance_summary`. Enforces uniqueness and foreign keys. PostgreSQL is a typical choice.

- **Message queue / event bus**
  Carries `CheckInRecorded`, `CheckOutRecorded`, and `CorrectionApproved` events from the write path to aggregation and notification consumers. Decouples report updates from punch latency. Kafka or RabbitMQ are typical; for the basic system an in-process event or a lightweight queue suffices.

- **Aggregation worker**
  Consumes punch events and incrementally maintains `daily_attendance_summary` (present/absent/late, worked minutes). A nightly batch job recomputes summaries from raw records to self-heal any drift.

- **Scheduler / batch jobs**
  Runs the end-of-day auto-close job (closes stale open records), the late-mark computation, and the nightly summary recomputation. Quartz, Spring `@Scheduled`, or a cron-based runner.

- **Notification service**
  Optional in the basic system: alerts a manager when a team member is absent, or reminds a user about a missed check-out.

- **Admin console**
  UI for corrections, team views, and report exports. Talks to the same APIs with elevated, org-scoped privileges.

```mermaid
flowchart TB
    Client["Clients"] --> Gateway["API Gateway"]
    Gateway --> Write["Attendance Service (write path)"]
    Gateway --> Read["Reporting Service (read path)"]
    Write --> DB[("Relational DB")]
    Write -->|events| Queue["Event Queue"]
    Queue --> Agg["Aggregation Worker"]
    Agg --> Summary[("Summary Tables")]
    Read --> Summary
    Read --> Replica[("Read Replica")]
    Jobs["Scheduler"] --> Write
    Jobs --> Agg
```

---

### Patterns

Relevant design and architectural patterns, each with the problem it solves, how it works, when to use it, advantages, disadvantages, and a real-world example.

- **Transactional uniqueness (database-enforced invariant)**
  - *Problem*: two concurrent check-in requests for the same user and day can both pass an application-level "is there an open record?" check (a read-then-write race).
  - *How it works*: a unique partial index such as `UNIQUE (user_id, work_date) WHERE check_out_at IS NULL` makes the second insert fail at the database; the application translates the violation into a `409 Conflict`.
  - *When to use*: always, for this invariant. *When not*: never skip it — application-only checks are insufficient.
  - *Advantages*: correct under any concurrency; simple code. *Disadvantages*: couples the invariant to the database schema; partial indexes are database-specific syntax.
  - *Real-world example*: PostgreSQL partial unique indexes are the standard way SaaS products enforce "one active session/subscription/punch" rules.

- **Idempotent receiver (idempotency keys)**
  - *Problem*: mobile networks retry; users double-tap; gateways retry on timeouts. A non-idempotent check-in creates 409 storms or duplicates.
  - *How it works*: the client generates a UUID per user intent and sends it as an `Idempotency-Key` header. The server stores the key with the created record; a repeated key returns the original response instead of executing again.
  - *When to use*: any mutating endpoint reachable from unreliable networks. *When not*: pure reads.
  - *Advantages*: safe retries, better UX. *Disadvantages*: requires key storage and lookup on the write path.
  - *Real-world example*: Stripe's `Idempotency-Key` header is the canonical implementation of this pattern.

- **CQRS (Command Query Responsibility Segregation), lite**
  - *Problem*: the write model (punch records) is a poor shape for reports (monthly aggregates), and report scans would slow the write-critical database.
  - *How it works*: writes go to `attendance_records`; events feed an aggregator that maintains `daily_attendance_summary`; reports read only summaries. Full-blown CQRS frameworks are unnecessary — a summary table plus a queue is the pragmatic version.
  - *When to use*: when read shapes diverge from write shapes and aggregation is expensive. *When not*: when `GROUP BY` over a few thousand rows is already fast enough.
  - *Advantages*: fast reports, isolated scaling. *Disadvantages*: eventual consistency between punch and summary; more moving parts.
  - *Real-world example*: every analytics dashboard backed by an operational database uses some form of this pattern.

- **Outbox pattern**
  - *Problem*: "insert record, then publish event" is not atomic — a crash between the two loses the event, and publishing before commit leaks phantom events.
  - *How it works*: the punch and an `outbox` row are written in one transaction; a relay polls the outbox (or tails the WAL) and publishes to the queue.
  - *When to use*: when downstream correctness (summaries, notifications) depends on events not being lost. *When not*: when a missed summary update is acceptable and the nightly job repairs it anyway.
  - *Advantages*: at-least-once delivery with no dual-write inconsistency. *Disadvantages*: extra table and relay process.
  - *Real-world example*: Debezium CDC over a Postgres outbox table is a common production setup.

- **Scheduled batch reconciliation (self-healing summaries)**
  - *Problem*: incremental aggregation can drift (consumer lag, bugs, backfills).
  - *How it works*: a nightly job recomputes each day's summary from raw records and overwrites drifted rows. The incremental path gives freshness; the batch path guarantees eventual correctness.
  - *Advantages*: bounded error, simple recovery. *Disadvantages*: nightly compute cost (tiny at this scale).
  - *Real-world example*: lambda-architecture style "speed layer + batch layer" used by most analytics pipelines.

- **Event sourcing (optional, usually overkill here)**
  - *Problem*: you want a perfect, replayable history of every punch and correction.
  - *How it works*: store immutable `PunchEvent`s and derive records/summaries by folding events.
  - *When to use*: heavy audit/regulatory needs or complex temporal queries. *When not*: for a basic system — a `records + corrections` schema already provides auditability with far less complexity.
  - *Advantages*: complete history, time travel. *Disadvantages*: operational complexity, harder ad-hoc queries.
  - *Real-world example*: financial ledgers use event sourcing; most HR tools do not.

---

### Benefits

- **Trustworthy payroll and compliance data**
  Server-stamped, durable, correction-audited records mean payroll runs and labor-law audits are based on data the organization can defend. This matters in production because attendance disputes and wage audits are common and expensive.

- **Real-time visibility for managers**
  Precomputed summaries let a manager answer "who is late today?" in seconds. Without aggregation, this question is a slow scan that nobody runs, and attendance problems surface only at month end.

- **Fraud and error reduction**
  Server timestamps, uniqueness rules, and audited corrections remove the easy manipulation vectors (backdated punches, duplicate entries, silent edits) that plague spreadsheet-based tracking.

- **Operational simplicity at low scale**
  The basic design runs on one application service and one database. Small organizations get the benefits above without operating distributed infrastructure — an important business property, not just a technical one.

- **Foundation for richer HR workflows**
  Clean attendance events are the input for leave accrual, overtime calculation, shift differential pay, and productivity analytics. Getting the event model right makes every downstream feature cheaper.

---

### Pros

Each advantage explained in detail.

- **Simple, well-understood stack**
  A relational database with unique constraints solves the hardest correctness problems (duplicates, one-open-record) declaratively. There is no distributed consensus, no cache coherence problem on the write path, and few failure modes to reason about.

- **Cheap to operate**
  Capacity math shows megabytes per day and tens of QPS at peak. A single small database instance with a nightly job covers years of growth for one organization, keeping infrastructure cost near zero relative to the business value.

- **Flexible event-based core**
  Storing raw check-in/check-out events (rather than only pre-computed daily statuses) keeps the system open to corrections, reprocessing, and new report types. You can always recompute a summary from events; you cannot reconstruct events from a summary.

- **Strong auditability by design**
  Because corrections are separate rows referencing the original record, the full history of every change is queryable. Auditors get "who changed what when and why" for free instead of through log archaeology.

- **Report reads never endanger the write path**
  The summary-table design isolates expensive aggregation reads from the punch write path, so a heavy month-end report cannot slow down morning check-ins.

---

### Cons

Each disadvantage, limitation, or trade-off explained in detail.

- **Single point of write contention per user-day**
  The uniqueness rule serializes concurrent punches for the same user through one index entry. This is fine at this scale, but hot-row thinking matters if you later add high-frequency features (break punches, per-task tracking) on the same key.

- **Eventual consistency on reports**
  A check-in may not appear in a dashboard for seconds (async aggregation) or until the nightly job (batch-only designs). Stakeholders must accept this, or you must pay for synchronous aggregation on the write path, which adds punch latency and coupling.

- **Timezone complexity is irreducible**
  No amount of infrastructure removes the need to carefully convert instants to local dates per organization, handle DST, and define shift boundaries. Bugs here are subtle, data-corrupting, and often discovered only when an employee disputes a late mark.

- **Corrections add workflow weight**
  Approval-gated corrections require states, notifications, and UI. Skipping the workflow (letting admins edit rows directly) is tempting and destroys auditability — the con is that doing it right costs real feature work.

- **Offline support complicates the client**
  Kiosks and mobile apps in low-connectivity sites need local queues, conflict rules, and reconciliation logic. The server side stays simple, but total system complexity moves to the client.

- **Not a fit for high-frequency telemetry**
  The model assumes two events per user per day. If requirements grow into continuous location or activity tracking, the schema, uniqueness rules, and capacity plan must be redesigned rather than extended.

---

### Challenges

Technical, scalability, performance, reliability, maintainability, operational, and security challenges, each explained.

- **Correctness under concurrency**
  Two requests racing to check in the same user must result in exactly one record. Solving this with application locks does not scale and breaks across instances; the database unique constraint is the only robust tool, and mapping its violation to a clean API response is a detail engineers often get wrong (leaking 500s instead of 409s).

- **Timezone and DST correctness**
  Converting `Instant` to `LocalDate` with the wrong zone misfiles punches by a day; DST transitions can shift late-mark boundaries; night shifts need an explicit "work date" assignment rule (e.g., the date of check-in). These bugs corrupt historical data, which is the worst kind of bug because fixes require backfills.

- **Stale open records**
  Users forget to check out. Without an end-of-day job, open records accumulate, worked-hours computation breaks, and the next day's check-in is blocked by the uniqueness rule. The auto-close job must be idempotent (reruns are safe) and observable (alert if it does not run).

- **Offline and duplicate punches**
  Field staff punch without connectivity and sync later; the server must accept these with client-captured times flagged as such, reconcile them against server-stamped records, and never double-count. Defining conflict precedence (first punch wins vs. server punch wins) is a product decision the design must make explicit.

- **Report performance over growing history**
  A naive `GROUP BY` over years of records degrades linearly. The challenge is keeping reports fast without making the write path heavy: summary tables, covering indexes on `(user_id, work_date)`, and read replicas are the levers.

- **Multi-tenant isolation (when grown into SaaS)**
  One organization's admin must never see another's data. Tenant id must be part of every key, every query, and every unique constraint; missing-tenant-filter bugs are a classic SaaS security incident.

- **Security and privacy**
  Attendance data is personal data (and location data, if GPS is captured). Challenges include access scoping, retention policies, encryption at rest, and compliance with labor and privacy regulations (GDPR right-to-erasure vs. payroll retention obligations is a genuine tension).

- **Operational reliability of the batch tier**
  The nightly aggregation and auto-close jobs are easy to forget because they run when nobody is watching. Missed runs silently produce wrong reports; they need schedules, monitoring, and alerting like any user-facing component.

---

### Best Practices

Detailed and practical, with the reason each is recommended.

- **Always stamp events with the server clock**
  Client clocks are user-controlled; accepting them as authoritative lets anyone backdate a punch. Store the client-captured time as a separate diagnostic column for offline reconciliation, but compute `check_in_at` on the server. Example: `Instant.now(clock)` in the service, with an injected `Clock` bean so tests can control time.

- **Enforce invariants in the database, not in code**
  The one-open-record rule must be a unique partial index. Application checks race; the database does not. Recommended because it is the only mechanism that is correct under retries, concurrent app instances, and ad-hoc scripts.

- **Make every mutating endpoint idempotent**
  Require an `Idempotency-Key` on check-in/check-out and persist it. Recommended because mobile clients retry aggressively, and without idempotency the system either duplicates data or punishes the user with errors for a network problem.

- **Store instants in UTC, derive local dates per tenant**
  Persist `check_in_at` as UTC `timestamptz`, store the organization's IANA timezone on the tenant, and compute `work_date` with that zone. Recommended because mixing local and UTC values in one column is the root cause of nearly all attendance-time bugs.

- **Precompute summaries; never scan raw records for dashboards**
  Maintain `daily_attendance_summary` incrementally and reconcile nightly. Recommended because report latency then stays constant as history grows, and the write path is protected from analytical load.

- **Model corrections as data, not edits**
  A correction is a row with old value, new value, reason, requester, approver. Recommended because it converts a compliance requirement (audit trail) into a queryable feature instead of a log-parsing exercise.

- **Close the day explicitly**
  An end-of-day job auto-closes stale open records with a flag like `AUTO_CLOSED`. Recommended because it keeps the uniqueness invariant usable the next morning and surfaces missed check-outs as data rather than silent corruption.

- **Design indexes around the two real query shapes**
  `(user_id, work_date)` for history and uniqueness, and `(org_id/team_id, work_date)` for admin reports. Recommended because these two cover virtually all traffic; extra indexes only tax the burst-sensitive write path.

- **Scope every query by tenant from day one**
  Even a single-organization deployment should carry `org_id` on every row. Recommended because retrofitting tenancy into schemas, constraints, and queries is one of the most painful migrations in SaaS.

---

### When to Use and When Not to Use

**Use this design when**

- You need reliable, auditable check-in/check-out for hundreds to tens of thousands of users per organization.
- Reports are aggregated daily/weekly/monthly views, not second-by-second analytics.
- Correctness (no duplicates, auditable corrections) matters more than extreme scale.
- The organization wants a system it can run on commodity infrastructure with a small team.

**Consider alternatives when**

- You need continuous location or activity tracking — use a telemetry/time-series architecture (e.g., append to Kafka, store in a time-series or columnar database) because per-day relational records are the wrong granularity.
- You need offline-first operation as the *primary* mode (remote sites with days of disconnection) — a plain request/response API is insufficient; design around local-first storage with CRDT-style or explicit reconciliation sync.
- You need biometric verification at scale — delegate capture and matching to specialized devices/services and treat this system as the record-keeping backend only.
- You already run an HR suite (Workday, SAP SuccessFactors) — integrate via its APIs instead of building; custom builds lose on compliance features.

**Decision factors**: number of tenants, offline requirements, regulatory audit needs, integration surface (payroll, leave), and whether attendance feeds money (payroll) — if it does, bias toward durability and auditability over cleverness.

---

### Use Cases

**Use case 1 — Corporate office attendance with payroll export**

- *Problem*: a 3,000-employee company tracks office attendance for hybrid-work policy compliance and monthly payroll.
- *Proposed solution*: mobile/web check-in with geofence metadata, server-stamped times, unique one-open-record rule, nightly aggregation into team summaries, admin corrections with manager approval.
- *Why this design fits*: write volume is trivial (~6,000 events/day); the hard requirements are exactly the system's strengths — uniqueness, auditability, and fast aggregate reports.
- *How it works*: employees punch in the app; the service stamps and stores; an aggregation worker updates `daily_attendance_summary`; payroll reads a monthly export of worked hours per user.
- *Trade-offs*: eventual-consistency dashboards (up to a minute stale) are accepted in exchange for a fast, simple write path.

**Use case 2 — Factory shift attendance including night shifts**

- *Problem*: a plant runs three shifts; the night shift (22:00–06:00) crosses midnight, and workers punch at gate kiosks that occasionally lose connectivity.
- *Proposed solution*: kiosk client with a local punch queue and idempotency keys; server assigns `work_date` by shift schedule (a 02:00 punch belongs to the previous day's shift); offline punches sync with client-captured times flagged as `source=OFFLINE_SYNC`.
- *Why this design fits*: the explicit work-date assignment rule and offline reconciliation are built into the model rather than patched on.
- *How it works*: kiosk stores punches locally with UUID keys; on reconnect it replays them; the server deduplicates by key and files each punch under the shift's work date.
- *Trade-offs*: more client complexity and a documented conflict-precedence rule (server punch beats conflicting offline punch, flagged for admin review).

**Use case 3 — University class attendance**

- *Problem*: a university needs per-class-session attendance for 20,000 students across hundreds of concurrent sessions.
- *Proposed solution*: extend the model with a `session_id` dimension; uniqueness becomes `(user_id, session_id)`; QR-code check-ins displayed in the lecture hall with short-lived tokens to prevent proxy check-ins from dorm rooms.
- *Why this design fits*: the same event model and uniqueness machinery apply; only the "day" boundary is replaced by "session".
- *How it works*: the lecturer displays a rotating QR token; the student app submits it as proof of presence; the server validates token freshness and records the punch.
- *Trade-offs*: token rotation adds a real-time element and clock-skew tolerance; sessions spike concurrency (500 students punching within 2 minutes of class start), which the burst-capable write path already handles.

---

### API Design and API Contract

REST, JSON over HTTPS, JWT bearer auth, tenant resolved from the token. All mutating endpoints accept an `Idempotency-Key` header. Base path versioned as `/api/v1`.

**Check-in**

```
POST /api/v1/attendance/check-in
Authorization: Bearer <jwt>
Idempotency-Key: 7c9e6679-7425-40de-944b-e07fc1f90ae7
Content-Type: application/json

{
  "clientCapturedAt": "2026-01-15T09:02:11+05:30",
  "source": "MOBILE_APP",
  "location": { "lat": 12.9716, "lng": 77.5946 }
}
```

Success `201 Created` (server time is authoritative; echoed back so the client can display it):

```json
{
  "recordId": "a3f1c2de-3b9a-4c1e-9f2d-8a1b2c3d4e5f",
  "userId": "u-1024",
  "workDate": "2026-01-15",
  "checkInAt": "2026-01-15T03:32:12Z",
  "status": "OPEN"
}
```

Errors: `400` invalid payload (e.g., malformed timestamp), `401` missing/expired token, `409` already checked in (body includes the existing record id), `422` business-rule rejection (e.g., user inactive), `429` rate limited.

**Check-out**

```
POST /api/v1/attendance/check-out
Idempotency-Key: 9b1c... (new key per intent)

{ "clientCapturedAt": "2026-01-15T18:05:44+05:30" }
```

Success `200 OK` returns the closed record including `checkOutAt` and `workedMinutes`. `409` if there is no open record to close.

**Own history** — paginated, filterable:

```
GET /api/v1/attendance/me?from=2026-01-01&to=2026-01-31&page=0&size=20&sort=workDate,desc
```

```json
{
  "content": [
    {
      "workDate": "2026-01-15",
      "checkInAt": "2026-01-15T03:32:12Z",
      "checkOutAt": "2026-01-15T12:35:44Z",
      "workedMinutes": 543,
      "status": "PRESENT",
      "late": false
    }
  ],
  "page": 0,
  "size": 20,
  "totalElements": 21,
  "totalPages": 2
}
```

**Admin report** (org-scoped by token; served from summary tables):

```
GET /api/v1/attendance/reports?team=engineering&from=2026-01-01&to=2026-01-31
```

```json
{
  "team": "engineering",
  "range": { "from": "2026-01-01", "to": "2026-01-31" },
  "present": 412, "absent": 38, "late": 57,
  "averageWorkedMinutesPerDay": 512
}
```

**Manual correction** (admin; creates an auditable correction, never edits in place):

```
POST /api/v1/attendance/records/{recordId}/corrections

{ "newCheckOutAt": "2026-01-15T13:00:00Z", "reason": "Employee forgot to check out; confirmed by manager" }
```

`202 Accepted` with the correction id; the record updates after approval (or immediately for admin self-approval policy — made explicit per tenant).

**Contract rules**

- *Validation*: `clientCapturedAt` must be ISO-8601 with offset; `source` must be a known enum; reject payloads with unknown future enums to fail loudly on version skew.
- *Idempotency*: repeated `Idempotency-Key` returns the stored original response (same status and body), keys retained for 7 days.
- *Pagination*: page/size with a `size` cap of 100; stable `sort` required for deterministic paging.
- *Versioning*: path version `/v1`; additive changes only within a version; breaking changes ship `/v2` with a deprecation window.
- *Rate limiting*: 30 req/min per user on punch endpoints, 300 req/min per admin on reports; `429` includes `Retry-After`.
- *AuthZ*: users may access only their own `/me` resources; report and correction endpoints require `ROLE_ADMIN` and are tenant-scoped server-side.

---

### Data Modeling

Normalized core entities with a deliberately denormalized summary table. The original minimal schema —

```
attendance_records: id (PK), user_id (FK), check_in_at, check_out_at, status, date
```

— is preserved and elaborated with tenancy, idempotency, source metadata, and audit fields.

```mermaid
erDiagram
    ORGANIZATIONS ||--o{ USERS : employs
    ORGANIZATIONS ||--o{ TEAMS : contains
    TEAMS ||--o{ USERS : groups
    USERS ||--o{ ATTENDANCE_RECORDS : records
    ATTENDANCE_RECORDS ||--o{ ATTENDANCE_CORRECTIONS : "corrected by"
    USERS ||--o{ DAILY_ATTENDANCE_SUMMARY : "summarized as"

    ORGANIZATIONS {
        uuid id PK
        string name
        string timezone "IANA zone, drives work_date"
    }
    TEAMS {
        uuid id PK
        uuid org_id FK
        string name
    }
    USERS {
        uuid id PK
        uuid org_id FK
        uuid team_id FK
        string email
        string role "EMPLOYEE or ADMIN"
        boolean active
    }
    ATTENDANCE_RECORDS {
        uuid id PK
        uuid org_id FK
        uuid user_id FK
        date work_date "local date in org timezone"
        timestamp check_in_at "UTC, server clock"
        timestamp check_out_at "UTC, nullable"
        string status "OPEN, COMPLETE, AUTO_CLOSED"
        string source "MOBILE_APP, WEB, KIOSK, OFFLINE_SYNC"
        string idempotency_key
        int worked_minutes
        timestamp created_at
        timestamp updated_at
    }
    ATTENDANCE_CORRECTIONS {
        uuid id PK
        uuid record_id FK
        uuid requested_by FK
        uuid approved_by FK
        timestamp old_value
        timestamp new_value
        string field_changed
        string reason
        string status "PENDING, APPROVED, REJECTED"
        timestamp created_at
    }
    DAILY_ATTENDANCE_SUMMARY {
        uuid org_id FK
        uuid user_id FK
        date work_date
        string status "PRESENT, ABSENT, LATE, HALF_DAY"
        int worked_minutes
        boolean late
        timestamp computed_at
    }
```

**Keys, indexes, and constraints**

- `attendance_records`: PK on `id`; **unique partial index** `UNIQUE (user_id, work_date) WHERE check_out_at IS NULL` (the one-open-record rule); unique index on `(user_id, idempotency_key)` for idempotent retries; reporting index on `(org_id, work_date)`; history index on `(user_id, work_date DESC)`.
- `daily_attendance_summary`: PK on `(user_id, work_date)` — exactly one summary row per user-day, upserted by the aggregator.
- `attendance_corrections`: FK to the record; index on `(record_id)` and on `(status)` for the approval queue.
- FK constraints keep referential integrity; `ON DELETE` is `RESTRICT` for attendance data (you archive, you do not delete, because of payroll/compliance).

**Normalization vs. denormalization**

- `attendance_records` and `attendance_corrections` are normalized (3NF): no derived values stored except `worked_minutes`, which is a *deliberate* denormalization — it is computed once at check-out so reports never recompute durations, and recomputation from timestamps is always possible if rules change.
- `daily_attendance_summary` is fully denormalized by design: it duplicates derivable data to make report reads O(1) per user-day. Drift is bounded by the nightly reconciliation job.

**Data lifecycle and partitioning**

- Hot data (current quarter) lives in the primary table with all indexes; older data can be moved to a monthly range-partitioned layout (`PARTITION BY RANGE (work_date)`) so old partitions are dropped or archived cheaply instead of row-by-row deletes.
- At SaaS scale, partition or shard by `org_id` (hash or list) so one tenant's growth never affects another's query latency.
- Retention: punch records kept for the statutory payroll period (often 3–8 years), then archived to object storage as Parquet/CSV exports.

---

### High-Level Design

The original architecture sketch is preserved as the base design:

```mermaid
flowchart LR
    Client --> API[API Layer]
    API --> AttendanceService[Attendance Service]
    AttendanceService --> DB[(Relational DB)]
    AttendanceService --> ReportService[Reporting Service]
    ReportService --> DB
```

This four-box design is sufficient at single-organization scale: one API layer, a write-oriented attendance service, a read-oriented reporting service, and one relational database serving both. The production version below adds the queue, aggregator, scheduler, and a read replica without changing the fundamental shape.

```mermaid
flowchart TB
    subgraph Clients
        Mobile["Mobile App"]
        Web["Web App"]
        Kiosk["Kiosk"]
    end
    Mobile --> GW["API Gateway + Auth"]
    Web --> GW
    Kiosk --> GW
    GW --> AS["Attendance Service"]
    GW --> RS["Reporting Service"]
    AS --> Primary[("Primary DB")]
    AS -->|punch events| Q["Event Queue"]
    Q --> AGG["Aggregation Worker"]
    AGG --> Primary
    SCH["Scheduler"] -->|"auto-close + recompute"| AS
    RS --> Replica[("Read Replica")]
    Primary -.->|"replication"| Replica
```

*Explanation*: all writes flow through the attendance service to the primary database, which alone enforces uniqueness. Every accepted punch emits an event; the aggregation worker maintains summary tables. Reads for reports go to a read replica so month-end analytics cannot degrade the morning punch burst. The scheduler drives the end-of-day auto-close and the nightly reconciliation.

**Check-in request flow**

```mermaid
sequenceDiagram
    participant C as Client
    participant G as API Gateway
    participant A as Attendance Service
    participant D as Primary DB
    participant Q as Event Queue
    C->>G: POST /check-in with Idempotency-Key
    G->>G: authenticate JWT, resolve tenant, rate limit
    G->>A: forward validated request
    A->>D: SELECT by idempotency key
    alt key seen before
        D-->>A: stored response
        A-->>G: 201 with original record
    else new intent
        A->>D: INSERT open record (server timestamp)
        alt unique violation on open record
            D-->>A: constraint error
            A-->>G: 409 Conflict with existing record id
        else inserted
            A->>Q: publish CheckInRecorded
            A-->>G: 201 Created with server time
        end
    end
    G-->>C: response
```

*Explanation*: the idempotency check runs first so retries are free; the unique partial index is the final arbiter of the one-open-record rule; the event is published only after the insert succeeds (via the outbox in strict deployments), so downstream summaries never observe phantom punches.

**Scaling strategy and failure handling**

- Scale the stateless services horizontally behind the gateway; the primary database scales vertically, then by tenant partitioning.
- If the queue or aggregator is down, punches are unaffected (they only need the primary DB); summaries catch up from the outbox or the nightly job.
- If the read replica lags, reports are stale but correct — never served from the primary under load.
- Database failover uses a managed primary/standby pair with synchronous replication (durability beats write availability here: better to reject a punch than to lose an acknowledged one).

---

### Deep Dive

#### 1. Check-In and Check-Out Event Capture

The punch is the atomic fact of the system, so its capture path deserves the most rigor.

**Server time as authority.** `check_in_at = Instant.now()` evaluated on the server. The client's `clientCapturedAt` is stored only as evidence for offline reconciliation. Inject a `java.time.Clock` into the service so tests can pin time — sprinkling `Instant.now()` through code makes timezone bugs untestable.

**State machine of a record.** A record is `OPEN` after check-in, becomes `COMPLETE` at check-out, or `AUTO_CLOSED` when the end-of-day job finds it still open. Corrections never mutate history silently: they create `attendance_corrections` rows, and on approval the record is updated with `updated_at` bumped and the correction linked.

```mermaid
stateDiagram-v2
    [*] --> NotCheckedIn
    NotCheckedIn --> Open : check-in accepted
    Open --> Complete : check-out accepted
    Open --> AutoClosed : end-of-day job
    Complete --> Corrected : approved correction
    AutoClosed --> Corrected : approved correction
    Corrected --> Complete
```

**Worked minutes.** Computed at check-out as `Duration.between(checkInAt, checkOutAt).toMinutes()` and stored. Breaks, if required later, become child rows rather than complicating the punch pair.

**Why not event sourcing here?** Two events per user-day with a corrections table already yields full auditability. Event sourcing would add replay infrastructure for no additional business guarantee — a good interview point on choosing the *sufficient* pattern.

#### 2. Timezone Handling

The hardest everyday problem in this domain.

**Rules that keep you correct**

1. Persist all instants as UTC (`timestamptz` / `Instant`). Never store local wall-clock timestamps without offset.
2. Store the organization's IANA timezone (`America/New_York`, not `UTC-5` — offsets change with DST).
3. Derive `work_date` at write time: `LocalDate.ofInstant(checkInAt, orgZone)`. Persist the derived date so queries and uniqueness never redo the conversion.
4. For night shifts, assign the work date by *shift schedule* (the date the shift started), not by calendar day of the punch — a 02:00 punch belongs to yesterday's shift.
5. Late-mark logic compares the local check-in time against the policy start time in the org's zone, both derived from the same instant.

**DST edge cases.** On spring-forward, 02:30 may not exist locally; on fall-back it occurs twice. Because all logic runs on `Instant` and only *display* and *date derivation* touch the zone, nonexistent local times cannot be produced by the system — they can only come from admin-entered corrections, which must be validated with `ZonedDateTime.ofLocal(...)` leniency rules (`withEarlierOffsetAtOverlap` etc.).

**Multi-timezone organizations.** A company with offices in New York and Bangalore keeps one org timezone per *location* (or per user assignment); reports bucket by each location's work date, and cross-location rollups state explicitly which zone defined the day.

#### 3. Duplicate Punches, Idempotency and Offline Sync

**Duplicate prevention, layered.** Layer 1 is the idempotency key: a retry with the same key short-circuits to the stored response, so *the same logical punch* can never be applied twice. Layer 2 is the unique partial index: *different* logical punches (user tapped check-in, forgot, tapped again an hour later with a new key) still collapse to one open record, and the second attempt gets a meaningful `409` with the existing record id.

**Why both layers are needed.** Idempotency keys dedupe *retries of one intent*; the unique index enforces the *business invariant*. Neither covers the other's case: a new key defeats layer 1 (it is genuinely a new intent), and a retried key never reaches layer 2.

**Offline sync protocol.** The client queues punches locally with their UUID idempotency keys and client-captured times. On reconnect it replays oldest-first. The server applies each replayed punch through the normal path with `source=OFFLINE_SYNC`; conflicts (server already has an open record from a kiosk punch) are resolved by the documented precedence — first *recorded* punch wins, and the conflicting replay is stored as a rejected sync entry for admin visibility rather than silently dropped. The response per replayed punch tells the client the outcome, so the local queue can be drained entry by entry.

```mermaid
sequenceDiagram
    participant K as Kiosk App (offline queue)
    participant A as Attendance Service
    participant D as DB
    Note over K: connectivity lost, queue punches locally
    K->>A: replay punch 1 with key k1, clientCapturedAt t1
    A->>D: insert with idempotency key k1
    D-->>A: ok
    A-->>K: 201 accepted
    K->>A: replay punch 2 with key k2
    A->>D: insert with key k2
    D-->>A: unique violation on open record
    A-->>K: 409 with existing record; logged as sync conflict
    Note over K: mark punch 2 conflicted, notify admin UI
```

#### 4. Reporting and Aggregation

**The query shapes.** Own history: `WHERE user_id = ? AND work_date BETWEEN ? AND ?` — covered by the history index, always fast. Team report: present/absent/late counts per team per range — over raw records this is a growing `GROUP BY` scan; over the summary table it is a bounded scan of one row per user-day.

**Incremental aggregation.** The aggregator consumes `CheckInRecorded`/`CheckOutRecorded`/`CorrectionApproved` events and upserts `daily_attendance_summary`: create-or-update the row for `(user_id, work_date)`, set `status`, `worked_minutes`, `late`. Upserts are idempotent because each row is a pure function of the underlying record — replaying an event converges to the same row.

**Batch reconciliation.** Nightly, recompute each affected day from raw records and overwrite drifted summary rows. This caps the damage from consumer bugs, backfills, and corrections: worst-case staleness is one day, typical staleness is seconds.

**Absent computation.** Absence is the *nonexistence* of data, so it cannot be derived from punch events alone. The nightly job compares the expected roster (active users with a work schedule for that date) against records and writes `ABSENT` summary rows for the difference. This is why reports run nightly-complete even though present/late are near-real-time.

**Late classification.** `late = checkInAt in org zone > policy start + grace`. The grace (e.g., 15 minutes) is configuration per org, injected via `@Value`, and versioned — changing the grace must not silently rewrite history, so summaries store the *result*, and the policy version used is recorded alongside for auditability.

#### 5. Manual Corrections and Audit Trail

**Workflow.** Requester (employee or admin) → correction row in `PENDING` → approver (manager/HR) → `APPROVED` → record updated, summary invalidated and recomputed, audit entry written. Admins may be granted self-approval by tenant policy, but the correction row is still written — the audit trail is unconditional.

**Why never edit in place.** A direct `UPDATE` destroys the evidence of the original value. Disputes ("I was on time, someone changed my punch") become unanswerable. With corrections-as-data, the answer is one query: `SELECT * FROM attendance_corrections WHERE record_id = ?`.

**Recomputation on approval.** Because summaries are derived, an approved correction must trigger summary recomputation for the affected `(user_id, work_date)` — implemented as just another event into the same aggregation pipeline, which keeps exactly one place where summary logic lives.

---

### Java and Spring Boot Implementation Guide

Production-oriented Spring Boot 3.x / Java 17 implementation of the write path. Every class is a Spring bean; configuration is externalized with `@Value`; dependencies are constructor-injected.

#### 1. JPA entity

```java
import jakarta.persistence.*;
import java.time.Instant;
import java.time.LocalDate;
import java.util.UUID;

@Entity
@Table(name = "attendance_records",
       uniqueConstraints = @UniqueConstraint(
           name = "uq_idempotency", columnNames = {"user_id", "idempotency_key"}),
       indexes = {
           @Index(name = "idx_user_date", columnList = "user_id, work_date"),
           @Index(name = "idx_org_date", columnList = "org_id, work_date")
       })
public class AttendanceRecord {

    @Id
    private UUID id;

    @Column(name = "org_id", nullable = false)
    private UUID orgId;

    @Column(name = "user_id", nullable = false)
    private UUID userId;

    @Column(name = "work_date", nullable = false)
    private LocalDate workDate;

    @Column(name = "check_in_at", nullable = false)
    private Instant checkInAt;

    @Column(name = "check_out_at")
    private Instant checkOutAt;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private AttendanceStatus status; // OPEN, COMPLETE, AUTO_CLOSED

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private PunchSource source; // MOBILE_APP, WEB, KIOSK, OFFLINE_SYNC

    @Column(name = "idempotency_key", nullable = false)
    private String idempotencyKey;

    @Column(name = "worked_minutes")
    private Integer workedMinutes;

    protected AttendanceRecord() {
        // for JPA
    }

    public AttendanceRecord(UUID orgId, UUID userId, LocalDate workDate,
                            Instant checkInAt, PunchSource source, String idempotencyKey) {
        this.id = UUID.randomUUID();
        this.orgId = orgId;
        this.userId = userId;
        this.workDate = workDate;
        this.checkInAt = checkInAt;
        this.source = source;
        this.idempotencyKey = idempotencyKey;
        this.status = AttendanceStatus.OPEN;
    }

    public void checkOut(Instant checkOutAt) {
        if (this.status != AttendanceStatus.OPEN) {
            throw new IllegalStateException("record is not open");
        }
        this.checkOutAt = checkOutAt;
        this.status = AttendanceStatus.COMPLETE;
        this.workedMinutes = (int) java.time.Duration.between(checkInAt, checkOutAt).toMinutes();
    }

    public UUID getId() { return id; }
    public LocalDate getWorkDate() { return workDate; }
    public Instant getCheckInAt() { return checkInAt; }
    public AttendanceStatus getStatus() { return status; }
}
```

The entity keeps invariants close to the state: `checkOut` refuses to close a non-open record, so even a bug in calling code cannot produce an impossible state.

#### 2. Repository

```java
import org.springframework.data.jpa.repository.JpaRepository;
import java.time.LocalDate;
import java.util.Optional;
import java.util.UUID;

public interface AttendanceRepository extends JpaRepository<AttendanceRecord, UUID> {

    Optional<AttendanceRecord> findByUserIdAndIdempotencyKey(UUID userId, String idempotencyKey);

    boolean existsByUserIdAndWorkDateAndCheckOutAtIsNull(UUID userId, LocalDate workDate);

    Optional<AttendanceRecord> findByUserIdAndWorkDateAndCheckOutAtIsNull(UUID userId, LocalDate workDate);
}
```

Derived queries map directly to the access patterns identified in data modeling; the database unique partial index (created by migration, since JPA cannot express `WHERE check_out_at IS NULL`) backs the exists/find pair.

#### 3. DTOs and validation

```java
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.time.Instant;
import java.time.LocalDate;

public record CheckInRequest(
        Instant clientCapturedAt,          // optional, evidence only
        @NotNull PunchSource source) {}

public record AttendanceResponse(
        UUID recordId,
        LocalDate workDate,
        Instant checkInAt,
        Instant checkOutAt,
        Integer workedMinutes,
        String status) {}
```

Records give immutability and concise equals/toString for free; Bean Validation annotations keep the controller thin.

#### 4. Service with externalized configuration

```java
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.UUID;

@Service
public class AttendanceService {

    private final AttendanceRepository repository;
    private final ApplicationEventPublisher events;
    private final Clock clock;
    private final ZoneId orgZone;   // resolved per tenant in production

    public AttendanceService(AttendanceRepository repository,
                             ApplicationEventPublisher events,
                             Clock clock,
                             @Value("${attendance.org-timezone:Asia/Kolkata}") String orgTimezone) {
        this.repository = repository;
        this.events = events;
        this.clock = clock;
        this.orgZone = ZoneId.of(orgTimezone);
    }

    @Transactional
    public AttendanceRecord checkIn(UUID orgId, UUID userId, CheckInRequest request, String idempotencyKey) {
        // Layer 1: idempotent retry — return the original result for a repeated key.
        var existing = repository.findByUserIdAndIdempotencyKey(userId, idempotencyKey);
        if (existing.isPresent()) {
            return existing.get();
        }

        Instant now = Instant.now(clock);              // server clock is authoritative
        LocalDate workDate = LocalDate.ofInstant(now, orgZone);

        var record = new AttendanceRecord(orgId, userId, workDate, now, request.source(), idempotencyKey);
        try {
            var saved = repository.saveAndFlush(record);
            events.publishEvent(new CheckInRecordedEvent(saved.getId(), userId, workDate));
            return saved;
        } catch (DataIntegrityViolationException e) {
            // Layer 2: unique partial index says an open record already exists.
            throw new DuplicateCheckInException(userId, workDate);
        }
    }

    @Transactional
    public AttendanceRecord checkOut(UUID userId, String idempotencyKey) {
        Instant now = Instant.now(clock);
        LocalDate workDate = LocalDate.ofInstant(now, orgZone);
        var open = repository.findByUserIdAndWorkDateAndCheckOutAtIsNull(userId, workDate)
                .orElseThrow(() -> new NoOpenRecordException(userId, workDate));
        open.checkOut(now);
        events.publishEvent(new CheckOutRecordedEvent(open.getId(), userId, workDate));
        return open;
    }
}
```

Key points to explain in an interview: the `Clock` bean makes timezone logic testable; `saveAndFlush` forces the constraint check inside the transaction so the violation maps to a domain exception; events are published from inside the transaction and, in strict deployments, an outbox table would replace direct publishing; the tenant's zone would normally be resolved from the tenant record rather than a single `@Value`, which is shown here to demonstrate externalized configuration.

#### 5. Controller

```java
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/v1/attendance")
public class AttendanceController {

    private final AttendanceService attendanceService;

    public AttendanceController(AttendanceService attendanceService) {
        this.attendanceService = attendanceService;
    }

    @PostMapping("/check-in")
    public ResponseEntity<AttendanceResponse> checkIn(
            @RequestHeader("Idempotency-Key") String idempotencyKey,
            @Valid @RequestBody CheckInRequest request) {
        var principal = SecurityContext.current();   // resolved from JWT by a filter
        var saved = attendanceService.checkIn(principal.orgId(), principal.userId(), request, idempotencyKey);
        return ResponseEntity.status(HttpStatus.CREATED).body(AttendanceMapper.toResponse(saved));
    }

    @PostMapping("/check-out")
    public AttendanceResponse checkOut(@RequestHeader("Idempotency-Key") String idempotencyKey) {
        var principal = SecurityContext.current();
        return AttendanceMapper.toResponse(attendanceService.checkOut(principal.userId(), idempotencyKey));
    }
}
```

The controller contains no business logic: authentication context, header extraction, delegation, and status codes only.

#### 6. Exception handling

```java
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class AttendanceExceptionHandler {

    @ExceptionHandler(DuplicateCheckInException.class)
    public ProblemDetail duplicate(DuplicateCheckInException e) {
        var problem = ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, e.getMessage());
        problem.setTitle("Already checked in");
        return problem;
    }

    @ExceptionHandler(NoOpenRecordException.class)
    public ProblemDetail noOpenRecord(NoOpenRecordException e) {
        var problem = ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, e.getMessage());
        problem.setTitle("No open attendance record");
        return problem;
    }
}
```

RFC 7807 `ProblemDetail` gives clients a stable, machine-readable error contract — interviewers notice when errors are designed rather than leaked as stack traces.

#### 7. Scheduled end-of-day job and aggregation listener

```java
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.transaction.event.TransactionalEventListener;
import org.springframework.transaction.event.TransactionPhase;

@Component
public class AttendanceMaintenanceJobs {

    private final AutoCloseService autoCloseService;

    public AttendanceMaintenanceJobs(AutoCloseService autoCloseService) {
        this.autoCloseService = autoCloseService;
    }

    // 23:55 in the organization timezone; idempotent so reruns are safe.
    @Scheduled(cron = "${attendance.auto-close-cron:0 55 23 * * *}")
    public void autoCloseStaleOpenRecords() {
        autoCloseService.closeAllOpenForToday();
    }
}

@Component
class SummaryProjection {

    private final DailySummaryRepository summaries;

    SummaryProjection(DailySummaryRepository summaries) {
        this.summaries = summaries;
    }

    // Runs only after the punch transaction commits, so the projection never sees phantom data.
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void on(CheckInRecordedEvent event) {
        summaries.upsertPresent(event.userId(), event.workDate());
    }
}
```

`@TransactionalEventListener(AFTER_COMMIT)` is the in-process alternative to a full outbox relay and is exactly the right size for the basic system; mention the upgrade path to a queue-based outbox in interviews.

---

### Interview Questions and Answers

**Q1. What is an attendance tracking system, and what problems does it solve? (Beginner)**

A system that records when people start and end their work or study day and turns those events into histories and aggregate reports. It solves four concrete problems: trustworthy time records for payroll and compliance, real-time visibility for managers (who is present/late/absent), elimination of spreadsheet manipulation through server-stamped, audited data, and a correction workflow for human error. Expected discussion: the difference between the raw event record (source of truth) and derived reports.

**Q2. Walk me through the check-in flow end to end. (Beginner)**

Client sends `POST /attendance/check-in` with a JWT and an idempotency key → gateway authenticates, resolves the tenant, and rate-limits → the service checks the idempotency store for a prior result with this key → if new, it stamps `Instant.now()` on the server, derives the local `work_date` from the org timezone, and inserts an `OPEN` record → the unique partial index guarantees no second open record exists → on success an event is published for the aggregation pipeline → `201` returns the record with the server timestamp. On constraint violation the service returns `409` with the existing record id. Common mistake: describing an application-level "check-then-insert" without the database constraint, which races.

**Q3. Why must the server clock be authoritative? (Beginner/Intermediate)**

Clients are adversarial territory: a user can set their phone back two hours and "arrive on time." Server time is the only clock the organization controls, so it stamps the official instant. The client timestamp is still captured — as evidence for offline reconciliation and clock-skew diagnostics, never as truth. Follow-up: how do you make time logic testable? Inject a `java.time.Clock` bean rather than calling `Instant.now()` statically.

**Q4. How do you guarantee one open record per user per day? (Intermediate)**

With a database-enforced unique partial index: `UNIQUE (user_id, work_date) WHERE check_out_at IS NULL`. Any concurrent or retried insert that would create a second open record fails at commit; the application translates the violation to `409 Conflict`. Application-level existence checks are a read-then-write race across app instances and must never be the enforcement mechanism. Follow-up: what changes for multi-tenancy? Include `org_id` in the constraint and every query. Trade-off: the rule is now schema-coupled, which is fine because the invariant is business-fundamental, not incidental.

**Q5. How is check-in idempotency implemented, and why is the unique constraint not enough? (Intermediate/Advanced)**

The client generates a UUID per user intent and sends it as `Idempotency-Key`; the server stores it with the record and short-circuits repeated keys to the stored response. This dedupes *retries of one intent* (network timeout, double tap). The unique open-record index enforces a *different* rule: the user cannot have two open days even with two distinct intents (new keys). Removing idempotency keys turns every retry into a `409`, which is terrible UX on flaky networks; removing the unique index allows genuinely distinct duplicate punches. Expected discussion: key retention window (days, not forever) and scoping the key per user.

**Q6. How do you handle timezones, work dates, and DST? (Intermediate/Advanced)**

Store UTC instants (`timestamptz`); store the tenant's IANA timezone; derive and persist `work_date` at write time using `LocalDate.ofInstant(instant, zone)`; run late/absent logic in the org zone against the stored instant. DST: because computation happens on instants, spring-forward/fall-back cannot produce ambiguous internal times; only admin-entered local times (corrections) need disambiguation rules. Common mistakes: storing local timestamps without offset, using fixed offsets like `UTC+5:30` instead of IANA zones, and recomputing the work date in queries instead of persisting it (two code paths that can disagree).

**Q7. How do you file punches for a night shift that crosses midnight? (Advanced)**

Calendar-date assignment fails: a 22:00–06:00 shift would split one workday into two dates, breaking hours and late calculations. The fix is *shift-anchored work dates*: the work date is the local date on which the shift started, resolved from the user's shift schedule at punch time. A 02:00 punch on Tuesday belongs to Monday's shift. Expected discussion: where the shift schedule lives (per user/team, versioned), what happens when no schedule exists (fallback to calendar date), and how reports bucket by shift date rather than calendar date.

**Q8. How do you support offline punches from a kiosk or mobile app? (Advanced)**

The client queues punches locally with their idempotency keys and client-captured times; on reconnect it replays oldest-first through the normal API with `source=OFFLINE_SYNC`. The server dedupes by key, applies precedence on conflicts (first recorded punch wins; conflicting replays are stored as rejected sync entries with admin visibility), and returns per-punch outcomes so the client can drain its queue. Trade-offs: server accepts the client-captured time as *claimed* evidence, so fraud review relies on corroborating signals (kiosk network identity, GPS, admin review) rather than trusting the timestamp. Common mistake: silently dropping conflicts, which makes missing punches unexplainable.

**Q9. Design the reporting pipeline. Why not just `GROUP BY` the raw table? (Advanced)**

Reports aggregate months of records per team — a scan that grows linearly with history and competes with the morning write burst. Instead, maintain a `daily_attendance_summary` (one row per user-day) via two mechanisms: incremental upserts from punch events (seconds of staleness) and a nightly recompute from raw records (self-healing, caps drift at one day). Absent rows require the batch path because absence is the *nonexistence* of an event — the nightly job diffs the expected roster against actual records. Trade-off: evental consistency on dashboards in exchange for constant-time report reads and an unburdened write path. This is CQRS in its pragmatic form.

**Q10. How do you design manual corrections so they remain auditable? (Intermediate)**

Corrections are rows, not edits: `(record_id, field, old_value, new_value, reason, requested_by, approved_by, status)`. Approval transitions the correction and updates the record; the original value is never overwritten without a trace. An approval also emits an event so the summary for that user-day is recomputed through the same aggregation path — one place owns summary logic. Expected discussion: self-approval policies for admins (allowed by tenant config, still audited), and why `ON DELETE RESTRICT` + archival beats deleting attendance data (payroll and labor-law retention).

**Q11. How would you scale this from one organization to a multi-tenant SaaS with 5M users? (Senior)**

Capacity: ~10M punches/day, ~7,500 QPS at peak — still modest, but now the concerns change: (1) tenant isolation — `org_id` in every key, constraint, and query; consider schema-per-tenant for large customers; (2) partitioning — range-partition records by `work_date`, and shard or list-partition by `org_id` at the top end; (3) read scaling — reports on read replicas, summaries possibly in a separate store; (4) cross-tenant jobs — the nightly aggregation fans out per tenant with per-tenant timezones, so the scheduler runs "end of day" continuously around the globe, not at one cron instant; (5) noisy-neighbor controls — per-tenant rate limits and resource quotas. The punch write path itself barely changes — a sign the original design was right.

**Q12. What consistency guarantees does the system need, and where is eventual consistency acceptable? (Senior)**

Strong: the one-open-record invariant and idempotency (correctness under concurrency, enforced by the primary database). Also strong: an acknowledged punch is durable (RPO 0 — synchronous replication on the primary pair). Eventually consistent: summaries and dashboards (seconds), cross-service views, notifications. The senior-level point is choosing per-invariant: putting strong consistency on the *write correctness* path where money depends on it, and paying for availability and speed everywhere else with bounded staleness plus nightly reconciliation.

**Q13. How do you detect and deter buddy punching or location spoofing? (Senior)**

Layered signals rather than one silver bullet: geofence metadata validated server-side against office coordinates; device binding (one registered device per user, hardware attestation on managed devices); kiosk network identity for on-premise punches; anomaly detection (impossible travel between consecutive punches, punch-time clustering patterns per user); and for high-assurance sites, delegated biometric capture on the kiosk with this system storing only the verified result. Expected discussion: privacy/consent implications of location data, storing the *minimum* necessary signal, and making every rejection reviewable to avoid punishing legitimate edge cases (VPN locations, travel days).

**Q14. Which indexes do you create and why? (Intermediate)**

`(user_id, work_date)` — own-history reads and the open-record lookups; unique partial `(user_id, work_date) WHERE check_out_at IS NULL` — the invariant; unique `(user_id, idempotency_key)` — retry dedupe; `(org_id, work_date)` — admin/team report scans over summaries or records. Each index costs write throughput on the burst-sensitive punch path, so anything beyond these four needs a measured justification. Follow-up: why a *partial* index? Because the invariant only constrains open records; a full unique index would forbid legitimate history (many closed records per user over time is fine — one *per day*, and only one *open*).

**Q15. A punch was acknowledged but never appears in reports. How do you debug it? (Senior)**

Trace the pipeline in order: (1) is the row in `attendance_records`? If not, the write path lost it — check whether `201` was actually committed or returned before commit; (2) was the event published? With `@TransactionalEventListener`/outbox, check outbox lag and consumer offsets; (3) did the aggregator apply it? Check consumer errors and whether an upsert raced a correction; (4) is the summary row stale? The nightly reconciliation should have fixed it — check the job's last success and its alerting. The systemic answer: this class of bug is why summaries must be *recomputable* from raw records and why the reconciliation job needs monitoring like a user-facing service.

---

[Back to top](#design-a-simple-attendance-tracking-system)
