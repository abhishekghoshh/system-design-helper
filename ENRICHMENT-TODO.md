# Enrichment Backlog — stub/thin files → interview-ready

HLD `designing/basic` (30 files) and `designing/advanced` (61 files) are COMPLETE
per their own `todo.md` checkpoints — verified this session (Topics + Java +
Interview present, fences even, TBD hits are false positives like `toDocument`).
Do NOT touch them except small defect fixes.

## Canonical templates for remaining areas

### LLD designing (`docs/system-design/low-level/designing/`)
```
# <Title preserved> + links preserved
## Theory
### Topics Covered (numbered anchor list of every ### below)
### Problem Statement (+ mermaid flowchart/classDiagram)
### Functional / Non-Functional Requirements
### Core Entities & Class Design (+ mermaid classDiagram, quoted labels)
### Key Design Decisions & Patterns Used
### Concurrency & Edge Cases
### Java 17 Implementation (full classes, explained, patterns named)
### Interview Questions and Answers (10-12, beginner → senior)
```
Target 600–1200 lines. Plain Java + OOP patterns (NOT Spring beans — LLD is OOP).

### Security (`docs/security/`)
```
# <Title> + links preserved
## Theory
### Topics Covered / What & Why / How It Works (+ mermaid sequence/flow)
### Code / Config Examples (explained) / Threats & Mitigations (table)
### Best Practices / Interview Q&A (10-12)
```
Target 500–1000 lines. Big files (oauth/jwt/encryption) already rich — leave.

### AI (`docs/ai/`) and Basics (`docs/basics/`)
```
# <Title> + links preserved
## Theory (scope note → full guide)
### Topics Covered / Concepts / How It Works (+ mermaid where apt)
### Code Example (python, explained) / Tools & Ecosystem / Use Cases
### Interview Q&A (8-10)
```
Target 400–800 lines.

## Hard rules (all areas)
- Preserve `# Title` and ALL link sections exactly. Never delete existing content.
- Chunked writes: ≤250 lines per edit (`write_file` first chunk, `edit_file` appends).
- Mermaid: quote labels with special chars, valid erDiagram/flowchart/sequenceDiagram/classDiagram, 1-sentence explanation under each.
- Explain every code block. Balanced fences (`grep -c '^ *```'` even). Zero TODO/TBD.
- One large file per agent call (multi-file single runs get killed by output limits).

## Backlog status — COMPLETE (all boxes checked this session)

- [x] LLD designing (22/22): parking-lot 854, atm 762, elevator 734, vending-machine 700, tic-tac-toe 909, chess 746, splitwise 743, cache 670, snake-ladder 698, logging 734, inventory 737, locker 756, meeting 798, car-rental 785, cricbuzz 914, payment-gateway 840, stock-exchange 741, access-mgmt 823, account-balance 792, air-traffic 952, apply-coupons 848, bookmyshow 840
- [x] LLD concepts (4/4): hashmap 607, solid 716, mvc 433, null-object 400
- [x] LLD patterns (24 expanded): structural ×7 (~230-250), behavioral ×11 (~200-220), creational abstract-factory 177 / prototype 170 / object-pool 249 / builder 287 / singleton 255, index design-pattern.md 336
- [x] Security (19/19 enriched or verified rich): introduction 511, rbac 509, sso 381, ssl 423, ssh 422, firewall 422, auth-authz 362, devsecops 512, env-vars 454, reverse-proxy intro 375, nginx 447, haproxy 436, reverse-engineering 347, certificate intro 453 / CA 417 / server 420 / client 440 / self-signed 335 (+ oauth/jwt/encryption already rich; certificate/links.md untouched per rules)
- [x] AI (12/12): RAG 495, agentic-ai 548, gen-ai 532, vector-embeddings 435, MCP 459, langchain 577, llm-wiki 399, ai 517, vibe-coding 385, skills 546, courses 435, ai-tools 446
- [x] Basics (8/8): cpu 525, pointers 336, maths 520, software-architect 458, wisdom 469, behavioural 421, developer-experiences 373, open-source-tools 420
- [x] Extras: interview playbook 564, devops index 406 (deployment-strategies 427 already solid)

Remaining thin files are navigational by design (link lists / section indexes):
index.md, low-level 0-introduction/index/0-introduction-designing, links/udemy, certificate/links.md (untouched per rules), books.md, courses.md.

Global verification: 270 files, all fences even, zero TODO/TBD/FIXME markers.
