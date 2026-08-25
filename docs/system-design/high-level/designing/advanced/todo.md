# System Design Docs — Enhancement Progress & Resume Guide

This file is a **checkpoint** for the project to enhance every `<topic>.md` file in this
directory (`docs/system-design/high-level/designing/advanced/`) into a comprehensive,
interview-ready system-design learning resource.

> **Status: IN PROGRESS.** Of the **61** topic files in this directory, **1** is already
> ✅ complete (follows the canonical template end-to-end). The remaining **60** are in
> flight: **23** use the older `### Important Subtopics` format with partial content, and
> **37** are stubs (title + links only, no Theory body). This file is kept as a reference
> and progress tracker — read it to verify any file, understand the canonical structure, or
> resume work on this directory.

---

## 1. Overall Goal (recap of the original prompt)

Transform each topic file into a comprehensive system-design learning resource, preserving all
existing content, for senior Java backend / system design interview preparation. Each file ends
up **~800–2000 lines** of dense, technically accurate content, with **no TODO/TBD placeholders**,
**valid Mermaid diagrams**, and **production-oriented Spring Boot examples as beans**.

---

## 2. Canonical Structure Every File Follows

```
# <Existing Title preserved>
## Blogs and websites / ## Medium / ## Youtube   (ALL existing links preserved exactly)
## Theory

### Topics Covered               — numbered list with anchor links to EVERY subsection below
### Introduction / Problem Statement (with a mermaid diagram)
### Functional Requirements      — detailed, numbered
### Non-Functional Requirements — with numbers (scale, latency, etc.)
### Capacity Estimation          — back-of-envelope, step-by-step math
### Characteristics              — for each: what it means / why it matters / how it works / example
### Components                   — for each: purpose / responsibilities / how it works / relationships / real-world example
### Patterns                     — for each: what / problem solved / how / when to use/not / pros / cons / example
### Benefits                     — each explained, why it matters in production
### Pros                         — detailed, not one-liners
### Cons                         — detailed disadvantages / trade-offs
### Challenges                   — technical / scalability / performance / reliability / maintainability / operational / security
### Best Practices               — explain WHY each is recommended with examples
### When to Use / When Not to Use — appropriateness, alternatives, decision factors
### Use Cases                    — 2-4 realistic scenarios (problem / solution / suitable / how / trade-offs)
### API Design and Contract       — endpoints, methods, realistic JSON request/response, headers, status codes, errors, validation, idempotency, pagination/filtering/sorting, versioning, auth, rate limiting
### Data Modeling                — entities, PK/FK, indexes, constraints, normalization, lifecycle; mermaid erDiagram
### High-Level Design            — components, communication, data/request flow, scaling, failure handling; mermaid flowchart + sequenceDiagram (1-sentence explanation under each diagram)
### Deep Dive                    — 3-6 most important technical aspects for THIS topic
### Java and Spring Boot Implementation Guide — @RestController, @Service beans, repository, DTOs, @Valid, @ControllerAdvice, @Value config, constructor injection; explain the code
### Interview Questions and Answers — 12-15 Q&As: beginner → intermediate → advanced → senior/system-design; detailed answers; follow-ups, common mistakes, trade-offs where useful
```

The files `key-value-store.md` and `vpn.md` (in the basic directory) are good style references.
For the advanced directory, **`key-value-store.md`** is the gold-standard reference.

---

## 3. Taste / Style Rules (HARD REQUIREMENTS)

- **Java 17+ / Spring Boot 3.x.** Code examples are **Spring Boot beans**
  (`@Service` / `@Component` / `@RestController`) — **NOT** plain Java utility classes.
- **External config via `@Value`** (e.g. `@Value("${app.ratelimit.default:60}")`), constructor
  injection, records for DTOs, Bean Validation (`@Valid`, `@NotBlank`, `@DecimalMin`),
  `@ControllerAdvice` exception handling, `@Transactional`, `@Version` for optimistic locking,
  `@Scheduled` for jobs, `@TransactionalEventListener` where events are emitted, JPA entities
  for data-modeling examples.
- Use `BigDecimal` for all money.
- **Explain every code block** — never dump code with no context.
- **Mermaid:** quote labels containing special characters inside node brackets; no unquoted `(` or
  `)` inside `[...]` node labels; valid `erDiagram` (e.g. `BUSINESSES ||--o{ REVIEWS : receives`);
  declare `sequenceDiagram` participants before use. Add a 1-sentence explanation under each
  diagram.
- **Preserve existing content:** the `# Title`, the link sections, and every existing section must
  survive — integrate them into the new structure, correct inaccuracies, elaborate, never delete.
- **Chunked writes:** files were written in ~6-8 edit operations of ≤250 lines each
  (`write_file` first chunk, then `edit_file` appends). A single ~1300-line `write_file` call fails
  on output limits.
- **Anchor links in Topics Covered:** each numbered item links to its `###` subsection via
  `[title](#anchor-slug)` so readers can jump from the overview to each section.

---

## 4. File Status

Legend: ✅ complete — has `### Topics Covered` (covering every other section), a
`### Java and Spring Boot Implementation Guide` section, a dedicated `### Interview Questions and Answers`
section, balanced Mermaid fences (even count), and zero `TODO/TBD` placeholders.
⏳ in-progress — has `### Important Subtopics` with partial body content, needs full restructure to
canonical template. ⏸️ stub — only title + links, needs full enhancement from scratch.

| File | Lines | Topics | Java | Interview | Status |
|---|:---:|:---:|:---:|:---:|:---:|
| key-value-store.md | 1241 | 25 | ✅ | ✅ | ✅ |
| Image-Optimisation-on-the-fly.md | 626 | 12 | ❌ | ❌ | ⏳ |
| distributed-job-scheduler.md | 569 | 12 | ❌ | ❌ | ⏳ |
| distributed-counter.md | 558 | 12 | ❌ | ❌ | ⏳ |
| distributed-locking-service.md | 562 | 12 | ❌ | ❌ | ⏳ |
| distributed-cache.md | 553 | 14 | ❌ | ❌ | ⏳ |
| distributed-transaction-banking-system.md | 543 | 12 | ❌ | ❌ | ⏳ |
| distributed-configuration-management-system.md | 534 | 12 | ❌ | ❌ | ⏳ |
| distributed-messaging-queue.md | 476 | 12 | ❌ | ❌ | ⏳ |
| distributed-rate-limiter.md | 479 | 12 | ❌ | ❌ | ⏳ |
| distributed-geospatial-data-platform.md | 467 | 12 | ❌ | ❌ | ⏳ |
| distributed-rate-limited-api-gateway.md | 464 | 12 | ❌ | ❌ | ⏳ |
| amazon-flipkart.md | 488 | 14 | ❌ | ❌ | ⏳ |
| ecommerce-search-ranking-system.md | 460 | 12 | ❌ | ❌ | ⏳ |
| email-automation-platform.md | 454 | 12 | ❌ | ❌ | ⏳ |
| feature-flag-experimentation-platform.md | 490 | 12 | ❌ | ❌ | ⏳ |
| fault-tolerant-order-processing-system.md | 504 | 12 | ❌ | ❌ | ⏳ |
| facebook.md | 480 | 12 | ❌ | ❌ | ⏳ |
| e-commerce.md | 466 | 12 | ❌ | ❌ | ⏳ |
| ecommerce-checkout.md | 501 | 12 | ❌ | ❌ | ⏳ |
| bookmyshow.md | 467 | 12 | ❌ | ❌ | ⏳ |
| authentication-system.md | 493 | 14 | ❌ | ❌ | ⏳ |
| chat-system.md | 494 | 14 | ❌ | ❌ | ⏳ |
| data-warehouse.md | 451 | 13 | ❌ | ❌ | ⏳ |
| whatspp.md | 227 | 0 | ❌ | ❌ | ⏸️ |
| uber.md | 916 | 0 | ❌ | ❌ | ⏸️ |
| google-docs.md | 167 | 0 | ❌ | ❌ | ⏸️ |
| slack.md | 164 | 0 | ❌ | ❌ | ⏸️ |
| online-code-editor.md | 139 | 0 | ❌ | ❌ | ⏸️ |
| tiktok.md | 133 | 0 | ❌ | ❌ | ⏸️ |
| google-maps.md | 130 | 0 | ❌ | ❌ | ⏸️ |
| instagram.md | 127 | 0 | ❌ | ❌ | ⏸️ |
| video-streaming.md | 83 | 0 | ❌ | ❌ | ⏸️ |
| upi-payments.md | 72 | 0 | ❌ | ❌ | ⏸️ |
| netflix.md | 72 | 0 | ❌ | ❌ | ⏸️ |
| fraud-detection-pipeline.md | 58 | 0 | ❌ | ❌ | ⏸️ |
| multi-region-deployment-system.md | 55 | 0 | ❌ | ❌ | ⏸️ |
| settlement-reconciliation-system.md | 55 | 0 | ❌ | ❌ | ⏸️ |
| quick-commerce-inventory-system.md | 54 | 0 | ❌ | ❌ | ⏸️ |
| real-time-bidding-auction-system.md | 53 | 0 | ❌ | ❌ | ⏸️ |
| flight-booking.md | 147 | 0 | ❌ | ❌ | ⏸️ |
| notification-fanout-service.md | 60 | 0 | ❌ | ❌ | ⏸️ |
| leetcode.md | 28 | 0 | ❌ | ❌ | ⏸️ |
| stock-broker-system.md | 19 | 0 | ❌ | ❌ | ⏸️ |
| live-streaming.md | 14 | 0 | ❌ | ❌ | ⏸️ |
| stripe.md | 13 | 0 | ❌ | ❌ | ⏸️ |
| recomendation-engine.md | 10 | 0 | ❌ | ❌ | ⏸️ |
| food-delivery.md | 9 | 0 | ❌ | ❌ | ⏸️ |
| google-drive.md | 9 | 0 | ❌ | ❌ | ⏸️ |
| hashtag-service.md | 9 | 0 | ❌ | ❌ | ⏸️ |
| large-language-model.md | 9 | 0 | ❌ | ❌ | ⏸️ |
| log-system.md | 9 | 0 | ❌ | ❌ | ⏸️ |
| multiplayer-game.md | 9 | 0 | ❌ | ❌ | ⏸️ |
| payment-gateway.md | 9 | 0 | ❌ | ❌ | ⏸️ |
| redis.md | 9 | 0 | ❌ | ❌ | ⏸️ |
| search-engine.md | 9 | 0 | ❌ | ❌ | ⏸️ |
| social-media.md | 9 | 0 | ❌ | ❌ | ⏸️ |
| spotify.md | 9 | 0 | ❌ | ❌ | ⏸️ |
| twitter.md | 9 | 0 | ❌ | ❌ | ⏸️ |

### Completion checklist per file (every file must pass)

A file is ✅ when it has ALL of: `### Topics Covered` (covering every other `###` section), a
`### Java and Spring Boot Implementation Guide` section, a dedicated `### Interview Questions and Answers`
section, ≥800 lines, balanced Mermaid fences (even count), and zero `TODO/TBD` placeholders.

---

## 5. Tasks Completed (history of what was done)

1. **key-value-store.md** — first file enhanced in the advanced directory. Restructured from a
   partial older-format stub into the full canonical template (Topic list, all theory sections,
   `### Java and Spring Boot Implementation Guide` with `@Service`/`@RestController`/Redis-backed
   repository/consistent-hashing router, Mermaid `erDiagram` and `flowchart`/`sequenceDiagram`
   diagrams, and inline interview Q&As). Final: 1241 lines. This file now serves as the
   gold-standard reference for the rest of the directory.

---

## 6. Execution Notes / Gotchas

- The **23 intermediate files** use `### Important Subtopics` and contain valuable existing theory
  content. These must be **restructured into the canonical template**, not rewritten — copy the
  algorithm/explanation content into matching new sections and expand around it. Rename the heading
  from `### Important Subtopics` to `### Topics Covered` and ensure the numbered list links to every
  `###` subsection that follows.
- The **37 stub files** only have a title + link sections (`## Blogs and websites`, `## Medium`,
  `## Youtube`) and in some cases a `## Theory` heading. These need full enhancement from scratch:
  create the Topics Covered list, write the theory sections, add Spring Boot code, Mermaid diagrams,
  and interview Q&As.
- After each file, verify: `grep -c '^```'` is **even** (balanced fences), `grep -ci 'tbd'` is 0,
  and `### Topics Covered` lists every other `###` section.
- The two most common regressions: **(a)** an unquoted `(` or `)` inside a Mermaid `[...]` node label,
  and **(b)** stray trailing `---`/blank lines at end of file — both are now clean across all files.
- Sub-agents that each produce ~1 file reliably succeed; a single agent producing multiple 1000+ line
  files in one run tends to be killed by output limits, so prefer **one large file per agent call**
  (write in ≤250-line chunks with `write_file` then `edit_file` append).
- All 61 files are referenced in `mkdocs.yml` (nav), so no nav edits are needed when content changes.
- Note on `key-value-store.md`: it embeds interview Q&As inline within each section rather than in a
  dedicated `### Interview Questions and Answers` heading at the end. When enhancing other files,
  prefer the canonical dedicated section at the bottom (as seen in the basic directory's `vpn.md`).

---

## 7. Reference: Gold-Standard File

Read `docs/system-design/high-level/designing/advanced/key-value-store.md` for the tone, depth, and
structural cadence to match. Its opening (header → Topics Covered numbered list → anchored subsections)
is the model for every file in this directory, and this file is the goal for the remaining 60.
