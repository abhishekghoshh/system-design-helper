# Design Autocomplete / Typeahead

## Blogs and websites

## Medium

## Youtube

## Theory

### Topics Covered

1. [Introduction and Problem Statement](#introduction-and-problem-statement)
2. [Functional Requirements](#functional-requirements)
3. [Non-Functional Requirements](#non-functional-requirements)
4. [Capacity Estimation (Back-of-Envelope)](#capacity-estimation-back-of-envelope)
5. [Characteristics](#characteristics)
6. [Components](#components)
7. [Autocomplete Patterns](#autocomplete-patterns)
8. [Benefits](#benefits)
9. [Pros](#pros)
10. [Cons](#cons)
11. [Challenges](#challenges)
12. [Best Practices](#best-practices)
13. [When to Use Autocomplete and When Not To](#when-to-use-autocomplete-and-when-not-to)
14. [Use Cases](#use-cases)
15. [API Design and Contract](#api-design-and-contract)
16. [Data Modeling](#data-modeling)
17. [High-Level Design](#high-level-design)
18. [Deep Dive](#deep-dive)
19. [Java and Spring Boot Implementation Guide](#java-and-spring-boot-implementation-guide)
20. [Interview Questions and Answers](#interview-questions-and-answers)

---

### Introduction and Problem Statement

Design a search autocomplete (typeahead) system that suggests relevant completions as users type, providing real-time suggestions with low latency.

Autocomplete looks simple — "return a few strings that start with the typed prefix" — but at search-engine scale it is one of the most latency-sensitive systems in existence. A user types 10-20 characters per query; every keystroke is an opportunity to help or to annoy. The system must return the *right* 5-10 suggestions from a corpus of billions of historical queries, ranked by what this user most likely means *right now*, fast enough that the dropdown is already painted before the next key lands.

**The problem autocomplete solves**

- **Typing is slow and error-prone**, especially on mobile. Google has reported that autocomplete saves users roughly 25% of keystrokes, and on mobile the savings are higher because typing on glass is painful. Every saved keystroke is a saved opportunity for a typo, an abandoned search, or a frustrated user.
- **Users do not know the exact vocabulary of the corpus.** A shopper searching a marketplace may not remember whether the product is listed as "running shoes" or "jogging shoes". Suggestions bridge the gap between the user's intent and the site's actual inventory and popular phrasing.
- **Search quality is bounded by query quality.** A well-formed query retrieves better results. Steering users toward historically successful queries ("google maps" rather than "google mapss") directly improves downstream search relevance and conversion.
- **Suggestions are a discovery surface.** Trending suggestions ("oscars 2026 winners") teach users what *can* be searched, driving engagement they would not have had otherwise.

**Why it is hard**

- **Latency budget is brutal.** The entire round trip — network, gateway, lookup, ranking, serialization — must complete in well under 100 ms, with the server-side lookup itself in low single-digit milliseconds. A database `LIKE 'prefix%'` query or a subtree scan at query time cannot meet this.
- **The corpus is enormous and skewed.** Billions of unique historical queries, but popularity follows a Zipf (power-law) distribution: a tiny head serves most traffic, and a gigantic long tail is barely ever needed.
- **Rankings change with time.** Query popularity decays, news causes spikes ("trending"), and each user has personal context. A static index goes stale within minutes during breaking news.
- **Every keystroke is a request.** Without client-side cooperation (debouncing, caching), autocomplete traffic is several times larger than search traffic itself.

```mermaid
flowchart LR
    U["User types g-o-o"] -->|"debounced keystroke"| GW["API Gateway"]
    GW --> SS["Suggestion Service"]
    SS -->|"O prefix length lookup"| TR["In-Memory Trie with cached Top-K"]
    TR --> SS
    SS --> GW
    GW -->|"Top-K suggestions in under 100 ms"| U
    QL["Search click and query events"] --> K["Kafka"]
    K --> FL["Stream and Batch Aggregation"]
    FL -->|"rebuilt trie snapshot plus trending updates"| SS
```

**Real-life examples**

- **Google Search**: suggestions appear per keystroke, mixing global popularity, trends, and your own history.
- **Amazon**: suggestions are product-oriented and often include categories ("apple — in Electronics"), because the goal is purchase conversion, not just search.
- **YouTube / Netflix**: suggestions mix title matches with entity matches (channels, actors).
- **IDEs and code editors**: IntelliJ and VS Code run the same fundamental algorithm locally over symbols in your project.

**Interview questions and answers**

- **Q: What is autocomplete in one sentence?**
  **A:** A read-optimized, latency-critical ranking system that maps every possible query prefix to its top-K most likely completions, usually served from an in-memory trie with pre-computed suggestions per node.

- **Q: Why can't you just run `SELECT ... WHERE query LIKE 'goo%' ORDER BY count DESC LIMIT 10`?**
  **A:** Three reasons: latency (even indexed `LIKE 'goo%'` scans thousands of rows and sorts at query time, blowing the millisecond budget), throughput (hundreds of thousands of QPS would crush the database), and ranking (popularity alone is not the ranking function — you need recency, trends, and personalization blended in, which is a precompute job, not a SQL `ORDER BY`).

---

### Functional Requirements

1. **Return top-K suggestions as the user types each character.** Given a prefix of one or more characters, return the K best completions (typically K = 5-10) ordered by relevance. The suggestion list must update on every keystroke (subject to client-side debouncing).
2. **Rank suggestions by popularity and relevance.** Historical query frequency is the primary signal, blended with recency, trending boosts, and optionally personalization. Ranking must be deterministic and explainable enough to debug.
3. **Support prefix matching.** "goo" must return completions like "google maps", "google docs", "golang". Multi-word completions are required — suggestions are full queries, not single tokens.
4. **Update suggestions based on trending queries.** A query spiking right now ("super bowl score" during the game) must enter the suggestion set within tens of seconds to a few minutes, without waiting for a full index rebuild.
5. **Personalized suggestions (optional but expected at scale).** A user's own past queries and interests should re-rank or inject suggestions, e.g. a user who often searches chess content sees "chess openings" for "che" rather than "cheap flights".
6. **Handle multi-language and multi-locale input.** Suggestions must be locale-aware (different trending topics per country) and support non-Latin scripts (CJK, Cyrillic, Arabic), including IME-composed input where a "keystroke" is not one character.
7. **Report telemetry.** The system should record which suggestions were shown and which were clicked (impression and click events), because click-through rate is the ground truth for ranking quality.
8. **Degrade gracefully.** If personalization or the trending pipeline is down, the service still returns globally popular suggestions. Suggestions must never block the actual search.

Out of scope for the core design (call this out in interviews): spell *correction* of the final submitted query ("did you mean"), full search result retrieval, and semantic/embedding-based suggestions — each is a system of its own, though we touch on typo *tolerance* in the Deep Dive.

---

### Non-Functional Requirements

- **Latency**: under 50 ms server-side per keystroke (suggestions must feel instant) and under 100 ms end-to-end including network. Slower than ~100 ms and the dropdown visibly lags behind typing, which users perceive as a broken page. The trie lookup itself should be single-digit milliseconds; the budget is mostly network.
- **Scale**: 10B+ autocomplete requests per day, 100K+ QPS average, with peaks several times higher during global events. Autocomplete request volume is a multiple of search volume because one search session generates many prefix requests.
- **Freshness**: trending queries appear within minutes (target: 30-60 seconds for hot updates via the streaming path; full ranking refresh every 15 minutes via batch).
- **Availability**: 99.99% (about 52 minutes of downtime per year). Autocomplete is on the critical path of the search experience, but it is strictly read-only and cacheable, which makes very high availability achievable with replication and stale-tolerant fallbacks.
- **Storage**: billions of unique query strings in the raw query log; the *serving* index holds only the head (tens of millions of queries) in memory.
- **Consistency**: eventual. A suggestion index a few minutes stale is perfectly acceptable; there is no correctness requirement, only a quality one. This freedom is what permits aggressive caching and precomputation.
- **Cost efficiency**: the serving tier must be cheap per QPS — suggestions generate no direct revenue, so the system should be dominated by memory and bandwidth costs, not per-request compute.

---

### Capacity Estimation (Back-of-Envelope)

Back-of-envelope math justifies the two-layer architecture (in-memory serving + offline aggregation) and drives memory sizing. Assume a large consumer search property.

**Step 1 — Request volume**

- Searches per day: 5 billion (5 × 10^9).
- Autocomplete requests per search session: a typical query is ~15 characters; with 100-150 ms debouncing and client-side prefix caching, only about 1 in 3-5 keystrokes actually hits the server → roughly 3-4 server requests per session, call it ~3.
- Autocomplete requests per day: 5B searches × ~2 (many sessions are abandoned mid-typing and never become searches) × 3 requests ≈ **10-30B requests/day**. Use 10^10 (10B) to be conservative, matching the NFR.
- Average QPS: 10^10 / 86,400 s ≈ **116,000 QPS**.
- Peak-to-average ratio of ~3x for a global consumer product (evening overlap of US/Europe/India): **~350,000 QPS peak**.

**Step 2 — Serving index size (the number that decides the architecture)**

- Raw unique queries ever seen: billions, but Zipf's law applies — the top ~10 million queries cover roughly 99% of search volume. Keep only the head in the trie: **10M queries**.
- Average query length: ~30 characters. Naive storage: 10M × 30 chars = 300M character slots, but prefixes are shared — "google", "google maps", and "google docs" share the "google" path. Empirically a trie of N strings of average length L has far fewer than N×L nodes; assume ~3-5 unique nodes per query on average after prefix sharing: **~40M nodes**.
- Per-node cost: sparse child map (a few pointers, ~24-40 bytes amortized), pre-computed top-K list of K=10 references to strings (10 × 8 bytes = 80 bytes), flags and metadata (~16 bytes) → roughly **120-150 bytes per node**.
- Serving index: 40M nodes × ~150 B ≈ **6 GB**. Add the string pool (10M × ~40 B = 400 MB) and per-node scores → **~7-8 GB total**.
- Conclusion: the whole head index fits comfortably in the RAM of one modern server (or a few GB per shard if sharded). This is *why* in-memory serving is feasible and why we pre-compute top-K at build time instead of scanning at query time.

**Step 3 — Memory cost of naive alternatives (why we pre-compute and prune)**

- Storing all 1B unique queries instead of the 10M head: ~100x more → 600-800 GB. Not in-memory-feasible on one node; forces sharding complexity for almost zero quality gain, because long-tail prefixes are essentially never asked.
- *Not* pre-computing top-K per node: memory drops slightly, but query time becomes "collect all terminal nodes in the subtree, then sort" — for the prefix "g" that is millions of candidates and a sort per keystroke. Unacceptable. The 80 bytes/node top-K cache is the best memory-to-latency trade in the design.

**Step 4 — Bandwidth**

- Response size: 8 suggestions × ~40 bytes of text + JSON envelope ≈ **0.5-1 KB** per response.
- Egress: 116K QPS × 1 KB ≈ 116 MB/s ≈ **~1 Gbps average**, ~3 Gbps peak. Trivial for a load-balanced cluster; bandwidth is not the constraint — QPS and memory are.

**Step 5 — Offline pipeline throughput**

- Raw query/click events: ~5B searches/day plus ~10B autocomplete impressions/day ≈ 15B events/day ≈ **~175K events/second** into Kafka. Comfortable for a small Kafka cluster (a single modern broker handles 100K+ msg/s), but worth stating because it sizes the streaming tier.
- Full trie rebuild every 15 minutes: recompute counts over a sliding window (e.g. last 7 days with exponential decay) and rebuild 6-8 GB of index — a batch job over a few hundred million aggregated records, well within a small Spark/Flink batch cluster's 15-minute window.

**Rules of thumb to quote in interviews**: popularity is Zipf-distributed so the top ~1% of queries serve ~99% of traffic; the serving index is sized by the *head of the distribution*, not by the raw corpus; and autocomplete QPS is a multiple of search QPS, which is why the client must debounce and cache.

---

### Characteristics

Each characteristic: what it means, why it matters, and how it shapes the design.

- **Read-heavy, write-never at serving time**
  The serving path is 100% reads against an immutable snapshot. All writes (new query counts, trending boosts) happen offline and are published as new snapshots or small deltas. This separation is what allows lock-free, cache-friendly reads at hundreds of thousands of QPS.

- **Latency-dominated, not throughput-dominated**
  The system is optimized for p99 latency in the low tens of milliseconds end-to-end. Every design decision — in-memory index, pre-computed top-K, no disk on the hot path, client debouncing — trades something (freshness, memory, completeness) for latency.

- **Zipf-skewed workload**
  Query popularity follows a power law. A small head (top ~10M queries) covers ~99% of traffic, so the serving index deliberately ignores the long tail and falls back to a secondary system (e.g. Elasticsearch) for the rare miss.

- **Prefix-addressable**
  Every request is a prefix lookup. This is what makes a trie (or FST) the natural data structure: the prefix itself is the access path, and all completions hang below one node.

- **Approximate and quality-driven, not correctness-driven**
  There is no "wrong" answer, only better or worse rankings. This permits approximation everywhere: top-K truncation, sampled telemetry, decayed counts, stale snapshots — none of which a transactional system could tolerate.

- **Time-decaying signals**
  A query's popularity from 6 months ago matters less than last hour's spike. Ranking signals incorporate exponential decay and spike detection, so the index is continuously rebuilt rather than appended to.

- **Stateless serving, stateful offline**
  Suggestion servers hold an immutable index in memory and can be killed and replaced freely; all state (query history, counts, models) lives in the offline pipeline and snapshot store. This is what makes 99.99% availability cheap.

- **Client-participating**
  Debouncing, prefix caching, pre-fetching, and request cancellation on the client are part of the system design, not afterthoughts — they cut server load by 3-5x and define the perceived latency.

- **Multi-tenant across locales**
  Rankings differ by language and country. The index is effectively one trie per locale (or a locale-tagged trie), sized independently.

---

### Components

The autocomplete system consists of these components. Each is listed with its purpose, responsibilities, how it works, how it relates to the others, and a real-world example.

- **Client (browser / mobile app)**
  *Purpose:* capture keystrokes and render suggestions without flooding the backend. *Responsibilities:* debounce input (wait 100-150 ms after the last keystroke before sending), cache prefix→results locally (results for "goo" can be filtered client-side for "goog"), pre-fetch likely next prefixes, cancel in-flight requests that are superseded by newer input, and render the dropdown with keyboard navigation. *How it works:* a small state machine around the input field; on response it caches by prefix and re-renders. *Relationships:* talks only to the API gateway; emits impression/click events to the telemetry endpoint. *Real-world example:* Google's search box cancels the in-flight `complete/search` XHR whenever a newer prefix exists.

- **API Gateway / Load Balancer**
  *Purpose:* single entry point for suggestion and telemetry traffic. *Responsibilities:* TLS termination, authentication token validation, rate limiting (per client, with `429` + `Retry-After`), request validation (prefix length, K bounds), and routing to the correct suggestion shard. *How it works:* L7 routing on path and prefix; consistent-hash or range-based shard mapping for prefix sharding. *Relationships:* fronts the suggestion service cluster; publishes rate-limit headers used by clients to back off. *Real-world example:* Envoy or NGINX fronting a suggestion fleet, or AWS API Gateway for smaller systems.

- **Suggestion Service (stateless, in-memory)**
  *Purpose:* answer prefix → top-K suggestions in single-digit milliseconds. *Responsibilities:* hold the immutable trie snapshot in RAM, execute prefix lookup, optionally blend in a personalization overlay, and hot-swap to a new snapshot atomically on rebuild. *How it works:* lookup is O(prefix length): walk one node per character, return the pre-computed top-K list cached at the final node — no subtree traversal, no sorting at query time. *Relationships:* loads snapshots from the snapshot store; receives hot trending deltas from the streaming updater; serves the gateway. *Real-world example:* a Spring Boot service holding a `TrieIndex` bean whose root reference is swapped via `volatile`/atomic reference.

- **Trie Snapshot Store**
  *Purpose:* durable, versioned distribution point for rebuilt indexes. *Responsibilities:* store immutable trie snapshots (serialized node arrays + string pool), expose metadata (version, build time, locale, checksum), and serve bulk downloads to suggestion servers. *How it works:* object storage with a `latest` pointer per locale; servers poll or are notified, download, verify checksum, then atomically swap. *Relationships:* written by the batch aggregation job; read by every suggestion server. *Real-world example:* S3/GCS bucket with versioned objects; Google has described distributing serving indexes to thousands of replicas in exactly this pull-based fashion.

- **Query Log / Event Collector (Kafka)**
  *Purpose:* capture the raw signal that drives ranking. *Responsibilities:* ingest search queries, autocomplete impressions, and suggestion clicks at ~175K events/s; retain them for the aggregation window (days). *How it works:* partitioned topics keyed by locale or query hash so aggregation is parallel and ordered per key. *Relationships:* fed by the gateway/telemetry endpoint; consumed by both the batch and streaming jobs. *Real-world example:* Kafka (or Kinesis/PubSub) — the standard firehose for clickstream at this scale.

- **Batch Aggregation Job (Spark / Flink batch)**
  *Purpose:* compute the authoritative ranking and rebuild the full index. *Responsibilities:* aggregate query counts over a decaying time window (e.g. 7 days with exponential decay), blend ranking signals, prune to the top-N queries, build the compressed trie with per-node top-K, and publish a new snapshot. *How it works:* scheduled every ~15 minutes; output is an immutable, checksummed snapshot. *Relationships:* reads Kafka/long-term storage; writes the snapshot store. *Real-world example:* a scheduled Spark job writing to S3, triggered by Airflow.

- **Streaming Trending Updater (Flink)**
  *Purpose:* make breaking trends visible within a minute, far faster than the 15-minute batch cycle. *Responsibilities:* maintain sliding-window counts (e.g. last 1 hour), detect spikes (`current_rate / baseline_rate > threshold`), and push small hot-update deltas into serving. *How it works:* a Flink job with event-time windows; deltas are published to a low-latency channel (Redis pub/sub or a compacted Kafka topic) that suggestion servers subscribe to and apply to their in-memory copy. *Relationships:* reads Kafka; pushes deltas to suggestion servers. *Real-world example:* Google's trends pipeline and Twitter/X trending topics use the same spike-detection-over-baseline approach.

- **Personalization Service**
  *Purpose:* re-rank or inject suggestions using per-user context. *Responsibilities:* store a compact per-user profile (recent queries, topic affinities), expose a fast lookup (single-digit ms), and merge personal candidates with global top-K. *How it works:* user profile in Redis keyed by hashed user id; the suggestion service fetches it in parallel with the trie lookup and re-ranks. *Relationships:* called by the suggestion service; feeds from the same event stream. *Real-world example:* Google's "based on your recent searches" suggestions.

- **Fallback Search Service (Elasticsearch / OpenSearch)**
  *Purpose:* answer long-tail prefixes not covered by the head trie. *Responsibilities:* prefix/completion queries over a much larger corpus with relaxed latency (tens of ms is acceptable for a rare path). *How it works:* an Elasticsearch completion suggester or edge-n-gram index. *Relationships:* consulted by the suggestion service only on trie miss or empty result. *Real-world example:* Elasticsearch's completion suggester is explicitly documented as the built-in way to build autocomplete on an ES cluster.

- **Monitoring and Analytics**
  *Purpose:* keep a quality-driven system honest. *Responsibilities:* track p50/p99 latency per stage, zero-result rate, suggestion click-through rate (CTR), snapshot age, and shard skew; alert on regressions. *Relationships:* consumes metrics from every component. *Real-world example:* Prometheus + Grafana dashboards with CTR fed from the telemetry topic into a warehouse.

---

### Autocomplete Patterns

Each pattern: what it is, the problem it solves, how it works, when to use it, when not to, advantages, disadvantages, and a real-world example.

#### Pattern 1: Pre-computed Top-K per Trie Node

- **What:** every trie node stores the K best completions of its subtree, computed at build time.
- **Problem:** finding the top-K completions of a prefix requires scanning every terminal node in the subtree and sorting — far too slow at query time (the prefix "g" may have millions of candidates).
- **How it works:** during index construction, insert all queries with their weights, then run a bottom-up pass: each node merges its children's top-K lists with its own terminal entry (if any), keeping the K highest scores. Query time becomes "walk one node per character, return the cached list" — O(prefix length), independent of corpus size.
- **When to use:** always, for latency-critical autocomplete. It is the single most important optimization in this design.
- **When not to use:** if K must be dynamic per request (the cache fixes K at build time; serve `limit <= K` from the cached list and build with the maximum K you support).
- **Advantages:** single-digit-ms lookups; query cost independent of index size; trivially cacheable at CDN/gateway level for popular prefixes.
- **Disadvantages:** ~80 bytes/node memory overhead; a ranking change requires rebuilding affected lists (i.e., a new snapshot); personalized entries cannot live in the shared cache.
- **Real-world example:** every large search engine's typeahead uses precomputed-per-prefix candidate lists; Elasticsearch's completion suggester does the analogous thing inside an FST.

#### Pattern 2: Two-Layer Update — Batch Rebuild + Streaming Hot Updates

- **What:** a slow, authoritative batch pipeline rebuilds the full index periodically, while a fast streaming pipeline patches hot trends in between.
- **Problem:** full recomputation of counts, decay, and ranking is expensive and takes minutes, but news-driven spikes cannot wait minutes.
- **How it works:** batch job rebuilds the complete trie snapshot every ~15 minutes and publishes it immutably; a Flink streaming job computes sliding-window rates, detects spikes versus baseline, and pushes small deltas ("inject 'oscars 2026' with bonus score under prefix o-s-c") to serving nodes over pub/sub, which apply them to their in-memory copy.
- **When to use:** whenever freshness matters but full recomputation is expensive — the classic lambda-architecture split.
- **When not to use:** for small corpora where a full rebuild takes seconds; just rebuild on every change and skip the streaming layer.
- **Advantages:** combines correctness (batch is authoritative and self-healing — the next snapshot wipes any bad deltas) with freshness (trends in ~30-60 s).
- **Disadvantages:** two pipelines to operate; deltas and snapshots can briefly disagree; delta application must be idempotent.
- **Real-world example:** Google Trends-powered suggestions; the same batch+speed layering appears in ads pacing and news ranking systems.

#### Pattern 3: Immutable Snapshots with Atomic Swap (Copy-on-Write Serving)

- **What:** suggestion servers serve from an immutable in-memory index and switch to a newly built one by swapping a single reference.
- **Problem:** rebuilding or mutating a live trie under 100K+ QPS would require locking, causing latency spikes and complexity.
- **How it works:** the new trie is constructed entirely off to the side (downloaded snapshot or applied rebuild); when ready and checksum-verified, a `volatile`/`AtomicReference` root pointer is flipped. Old requests finish on the old snapshot; garbage collection reclaims it afterward.
- **When to use:** any read-mostly in-memory index that is periodically refreshed — autocomplete, feature flags, ML model artifacts, geo databases.
- **When not to use:** when updates are continuous and fine-grained (a per-user editable structure) — copy-on-write then costs more than it saves.
- **Advantages:** lock-free reads, no torn states, trivial rollback (swap back to the previous snapshot), simple reasoning about concurrency.
- **Disadvantages:** peak memory is up to 2x index size during a swap; every swap is all-or-nothing (no partial updates, which is why the streaming delta layer exists).
- **Real-world example:** Lucene segment refreshes and Netflix's Hollow dataset distribution use the same immutable-snapshot-with-swap model.

#### Pattern 4: Client-Side Debounce, Cache, Pre-fetch, and Cancel

- **What:** the client is a load-reduction and latency component of the system.
- **Problem:** a request per raw keystroke would multiply server load 3-5x and race itself (responses arriving out of order).
- **How it works:** debounce 100-150 ms after the last keystroke; cache prefix→results in memory and reuse/filter them for longer prefixes; pre-fetch the most likely next prefix after showing results; abort superseded in-flight requests (AbortController / RxJS `switchMap`) so stale responses never render.
- **When to use:** every autocomplete deployment, without exception.
- **When not to use:** for server-driven UIs where input is not per-keystroke (voice, paste-heavy flows) — debounce alone suffices there.
- **Advantages:** 3-5x fewer requests; perceived latency near zero for cached prefixes; no out-of-order rendering bugs.
- **Disadvantages:** more client complexity; cached results are stale by a few minutes; aggressive pre-fetch can waste bandwidth.
- **Real-world example:** Google's search box caches per prefix and cancels in-flight requests; React autocomplete libraries all ship `switchMap`-style cancellation.

#### Pattern 5: Prefix Sharding with Replication

- **What:** partition the trie by prefix ranges across servers, and replicate each shard.
- **Problem:** a single server's RAM and NIC eventually cap out; also one node's failure cannot be allowed to take down a letter range.
- **How it works:** shard by first-character ranges (A-M / N-Z) or by consistent hashing on the 1-2 character prefix; the gateway routes by prefix. Each shard is replicated 3x behind the balancer. Hot shards (e.g. the shard holding "f" for "facebook…", "weather…" locales) are split further.
- **When to use:** when the index outgrows one node or when QPS per node exceeds its network/CPU budget.
- **When not to use:** when the whole index fits on one machine with headroom — replication alone is simpler and every node can answer every prefix.
- **Advantages:** linear horizontal scaling of memory and QPS; isolates hot-key blast radius.
- **Disadvantages:** a routing layer must know the shard map; cross-shard rebalancing is operationally painful; popularity is not uniform across letters, so shards skew.
- **Real-world example:** prefix-sharded suggestion fleets at search engines; the same idea as range-partitioned key-value stores like HBase region servers.

#### Pattern 6: Head Index + Long-Tail Fallback

- **What:** serve the top ~10M queries from the in-memory trie and delegate everything rarer to a secondary system.
- **Problem:** the full corpus (billions of unique queries) cannot fit in memory, but dropping it entirely would return zero suggestions for rare prefixes.
- **How it works:** if the trie returns empty (or too few results) for a prefix, the suggestion service issues a fallback query to an Elasticsearch completion-suggester/edge-n-gram index and merges results. The fallback is latency-budgeted and rate-limited because it should trigger on well under 1% of traffic.
- **When to use:** any Zipf-skewed serving problem — cache the head, compute the tail.
- **When not to use:** if quality requirements demand head-only answers (fallback results can be odd because tail queries are noisy and uncurated).
- **Advantages:** 100x memory reduction for ~1% quality cost; the fallback system doubles as the spell-tolerant path.
- **Disadvantages:** two systems to keep consistent; tail latency for fallback hits; risk of surfacing low-quality or unsafe tail suggestions (needs filtering).
- **Real-world example:** search engines falling back from typeahead to full query suggestions; CDNs falling back from edge cache to origin is the same shape of idea.

---

### Benefits

- **Dramatically better user experience.** Fewer keystrokes (~25% saved by Google's measurements), fewer typos, and less cognitive load — users pick from a list instead of composing a query from memory.
- **Higher search success and conversion.** Suggestions steer users toward historically successful, well-formed queries, which improves result relevance and, on commerce sites, directly increases purchase conversion.
- **A discovery and engagement surface.** Trending and popular suggestions teach users what is searchable and what is happening now, driving sessions that would not otherwise exist.
- **Cheaper than it looks.** Because the workload is Zipf-skewed and read-only, the entire head index fits in a few GB of RAM; the marginal cost per autocomplete request is fractions of a millisecond of CPU.
- **Defensive value for the search backend.** Client-side filtering and head caching absorb traffic; every search completed via a good suggestion is one less malformed, expensive query hitting the search index.
- **Telemetry goldmine.** Impression/click data per suggestion is a clean, high-volume relevance signal that improves ranking everywhere else in search.

---

### Pros

- **Single-digit-millisecond lookups.** Pre-computed top-K makes query cost O(prefix length), independent of corpus size.
- **Horizontally scalable.** Stateless serving nodes behind a balancer scale linearly; prefix sharding scales memory when needed.
- **Highly available by construction.** Read-only immutable snapshots + replication + stale-tolerant fallback make 99.99% cheap to achieve.
- **Fresh enough.** The batch+streaming split delivers both authoritative rankings and sub-minute trending.
- **Memory efficient for its coverage.** Top-10M-head pruning plus compressed tries/FSTs serve ~99% of traffic from single-digit GB.
- **Degrades gracefully.** Loss of personalization, trending, or even the fallback service still leaves globally popular suggestions; users are never blocked from searching.
- **Simple operational model.** Immutable versioned snapshots make deploys, rollbacks, and A/B tests of ranking trivial.

---

### Cons

- **Ranking is only as good as the pipeline.** Stale snapshots mean stale suggestions; a broken trending job during a major news event is user-visible within minutes.
- **Memory-heavy per replica.** Every serving node holds the full shard in RAM; replicas multiply the footprint, and snapshot swaps transiently double it.
- **Personalization is architecturally awkward.** The shared pre-computed top-K cannot contain per-user entries, so personalization is always an add-on merge layer with its own latency and consistency costs.
- **Long-tail quality is poor.** The fallback path returns noisy, uncurated suggestions and needs explicit safety filtering.
- **Abuse and embarrassment surface.** Suggestions reflect real user behavior — including offensive, private, or manipulated queries ("suggestion bombing"). Mitigation (PII stripping, blocklists, human review) is an ongoing operational cost.
- **Client complexity leaks everywhere.** Debounce/cancel/cache logic must be reimplemented correctly on web, Android, and iOS; bugs manifest as flicker, stale dropdowns, or doubled traffic.
- **Skew defeats naive sharding.** Letter ranges have wildly unequal popularity ("s" vs "x"), so prefix sharding needs continuous hot-shard management.
- **Freshness vs. cost tension.** Rebuilding more frequently improves freshness linearly in cost; there is no free lunch between the 15-minute batch and the streaming patch layer.

---

### Challenges

Organized by category; each includes the concrete failure mode and the standard mitigation.

**Technical**

- *Subtree explosion at query time.* Naive tries require scanning the whole subtree under a prefix. Mitigation: pre-computed top-K per node (Pattern 1) — non-negotiable.
- *Memory blow-up.* Billions of queries cannot fit. Mitigation: keep only the head (top ~10M), compress the trie (Patricia/radix compression collapses single-child chains, cutting memory 50%+), or move to an FST.
- *Ranking correctness.* Frequency alone ranks "facebook" above a breaking-news query. Mitigation: blend decayed frequency, spike detection, and personalization; make the score formula explicit and tunable.

**Scalability**

- *Keystroke-multiplied QPS.* Autocomplete traffic is a multiple of search traffic. Mitigation: client debounce/cache/pre-fetch (3-5x reduction) plus edge caching of ultra-popular prefixes.
- *Hot prefixes and hot shards.* During events, prefixes like "election" hammer specific nodes/shards. Mitigation: replicate hot shards, cache top prefixes at the gateway/CDN, split hot ranges.
- *Snapshot distribution fan-out.* Pushing a 6-8 GB snapshot to hundreds of replicas every 15 minutes is ~TB-class egress per cycle. Mitigation: pull-based distribution from object storage with CDN-like caching, delta snapshots, or rolling waves.

**Performance**

- *Tail latency from GC pauses.* Multi-GB heaps with frequent large allocations (snapshot swaps) invite long GC pauses that blow the p99 budget. Mitigation: off-heap or serialized-flat index layouts, G1/ZGC with tuned pause targets, and swap-then-drain during low-traffic windows.
- *Personalization on the hot path.* A slow profile lookup adds directly to p99. Mitigation: fetch the profile in parallel with the trie lookup, race them with a hard timeout (e.g. 5 ms), and fall back to global results on timeout.

**Reliability**

- *Bad snapshot poisoning the fleet.* A corrupt or low-quality build served everywhere at once. Mitigation: checksums, canary rollout (one shard first), quality gates (zero-result rate, size delta checks), and one-click rollback to the previous snapshot.
- *Streaming deltas drifting from snapshots.* Hot updates applied for hours can skew rankings. Mitigation: the next batch snapshot is authoritative and wipes deltas; deltas are idempotent and TTL-bounded.

**Maintainability**

- *Two pipelines to reason about.* Batch and streaming must agree on scoring semantics or suggestions flicker between updates. Mitigation: share the ranking code as a library used by both jobs.
- *Locale explosion.* Each locale is its own index, pipeline partition, and on-call surface. Mitigation: per-locale config as data, identical code paths everywhere.

**Operational**

- *Deploy/swap coordination.* Snapshot swap during peak can double memory and trigger alerts. Mitigation: stagger swaps across the fleet, schedule in troughs, monitor swap-induced GC.
- *Observability of a quality metric.* Latency dashboards don't catch "suggestions got worse". Mitigation: track suggestion CTR and zero-result rate as first-class SLIs.

**Security and privacy**

- *PII leakage into suggestions.* Users paste emails, names, and even passwords into search boxes; frequency-based suggestion could resurface them to everyone. Mitigation: strip/quarantine PII patterns in the ingestion pipeline, require minimum global frequency thresholds, and never suggest personalized-only queries to other users.
- *Suggestion bombing / manipulation.* Coordinated bots searching a phrase to inject it into suggestions. Mitigation: per-user and per-IP anomaly filtering in aggregation, velocity caps on brand-new queries entering the index.
- *Abuse of the endpoint.* Autocomplete endpoints are high-QPS and unauthenticated by nature — prime scraping/DoS targets. Mitigation: gateway rate limiting with `429` + `Retry-After`, bot detection, and response-size caps.

---

### Best Practices

Each practice includes *why* it matters, not just what to do.

1. **Pre-compute top-K at every trie node, at build time.** *Why:* it converts query time from "scan and sort a subtree" to "read a list", which is the difference between meeting and missing the 50 ms budget. There is no cheaper latency win in the entire design.
2. **Keep only the head of the distribution in memory.** *Why:* popularity is Zipf-distributed; the top ~10M queries serve ~99% of traffic. Storing the tail costs ~100x memory for ~1% of requests — spend that effort on a fallback service instead.
3. **Make the serving index immutable and swap atomically.** *Why:* lock-free reads eliminate tail-latency jitter under 100K+ QPS, and versioned snapshots give you instant rollback when a bad build ships — the two properties you need most during an incident.
4. **Debounce, cache, and cancel on the client.** *Why:* the client is the cheapest "capacity" you have: 3-5x fewer requests for a few lines of JavaScript, plus it eliminates the out-of-order-response rendering bug class entirely.
5. **Split freshness into batch (authoritative) + streaming (hot).** *Why:* a single pipeline cannot be both cheap and fresh; the batch rebuild guarantees self-healing correctness while the streaming layer delivers the sub-minute trends users expect during breaking news.
6. **Blend ranking signals explicitly — frequency, decay, trending, personalization.** *Why:* pure frequency ranking fossilizes last year's interests; explicit, tunable weights (`score = α·frequency + β·recency + γ·personalization + δ·trending`) make quality regressions debuggable instead of mysterious.
7. **Strip PII and enforce minimum-frequency thresholds at ingestion.** *Why:* suggestions are user-generated content reflected back at all users; once a password or email appears in a dropdown, the incident is public. Prevention at ingestion is the only reliable point of control.
8. **Race personalization with a hard timeout.** *Why:* personalization improves CTR but must never be allowed to blow the latency budget; a 5 ms race with fallback to global results captures most of the benefit at none of the tail risk.
9. **Instrument quality SLIs, not just latency.** *Why:* autocomplete can be fast and wrong; suggestion CTR, zero-result rate, and snapshot age are the metrics that detect ranking regressions before users tweet about them.
10. **Cap K and validate inputs at the gateway.** *Why:* `limit=10000` or a 500-character prefix is an abuse vector and a memory-amplification attack; validate `1 <= limit <= Kmax` and prefix length bounds before any trie work happens.
11. **Cache ultra-popular prefixes at the edge/gateway.** *Why:* a tiny set of prefixes ("w" → weather, "n" → news) carries disproportionate QPS; a short-TTL edge cache shaves real load for near-zero staleness cost.
12. **Roll snapshots out as a canary with quality gates.** *Why:* a bad ranking build served to 100% of users is a visible product incident; canary + automatic checks (size delta, zero-result delta) convert it into a non-event.

---

### When to Use Autocomplete and When Not To

**Use autocomplete when:**

- **The corpus has stable, popular phrasings** — search queries, product names, locations, commands — so prefix completions genuinely predict intent.
- **Input is expensive or error-prone** — mobile keyboards, long technical terms, non-native languages — where saved keystrokes measurably help.
- **You have (or can collect) usage frequency data.** Ranking needs a popularity signal; without historical queries, suggestions are guesses.
- **Latency budget allows a network round trip** (~100 ms) or you can run the index client-side (IDEs ship the symbol trie locally for this reason).
- **Discovery is valuable** — trends, categories, and popular items are part of the product, not just text entry.

**Do not use autocomplete (or use something else) when:**

- **Inputs are unique or near-unique** — order IDs, UUIDs, exact emails, password fields. There is no meaningful prefix distribution; suggestions are noise and a security hazard. Use exact-match lookup instead.
- **The corpus churns faster than you can rebuild** — if items live for seconds, a snapshot-based index is always stale; query a live index (database/Elasticsearch) directly and accept the latency.
- **Intent is semantic, not lexical** — "something like a thriller but funny" is not a prefix problem; use semantic search/LLM-based assistance.
- **Traffic is tiny.** Below thousands of QPS, a single PostgreSQL `pg_trgm` index or an Elasticsearch completion suggester is simpler, fresher, and cheaper to operate than a custom trie pipeline. Build the trie architecture when latency or scale forces you to.
- **Privacy forbids aggregation** — if query logs cannot legally be collected (certain health/finance contexts), popularity-based suggestions cannot be built; fall back to curated static suggestion lists.

---

### Use Cases

Four realistic use cases, each with the problem, the solution, why autocomplete is suitable, how it works end to end, and the trade-offs.

#### Use Case 1: E-commerce Search Box (Amazon-style)

- **Problem:** shoppers mistype product names, don't know catalog vocabulary, and abandon searches that return nothing. Mobile typing makes all three worse.
- **Solution:** autocomplete over past purchase-driving queries and product titles, ranked by conversion-weighted frequency, with category annotations ("apple — in Electronics").
- **Why suitable:** query vocabulary is stable and Zipf-skewed (the head covers almost everything), and every saved keystroke is measurable revenue — e-commerce has the clearest ROI of any autocomplete deployment.
- **How it works:** clickstream and purchase events feed the aggregation pipeline; query scores weight purchases and add-to-carts higher than raw frequency; suggestions are rebuilt every 15 minutes; the client debounces at 100 ms and caches per prefix; personalization re-ranks toward the user's browsed categories.
- **Trade-offs:** conversion-weighted ranking can bury new products (no history) — mitigated by injecting curated "new arrival" candidates; category annotations lengthen responses slightly; personalization raises privacy review requirements.

#### Use Case 2: IDE / Code Editor Symbol Completion (IntelliJ, VS Code)

- **Problem:** developers cannot remember exact symbol names across thousands of files; hunting through the codebase destroys flow.
- **Solution:** a local trie (or Patricia trie) over all identifiers in the project, updated incrementally as files change, with fuzzy subsequence matching ("psvm" → `public static void main`).
- **Why suitable:** the corpus is small enough (millions of symbols) to run entirely client-side, eliminating network latency altogether — proof that the trie pattern works without any distributed system when the data fits on one machine.
- **How it works:** the indexer walks source files, extracts identifiers, and maintains an in-memory trie keyed by symbol characters; on each keystroke the editor walks the trie, applies fuzzy scoring (camelCase humps, recency of use), and renders within a frame budget (~16 ms).
- **Trade-offs:** incremental index updates on every file save add background CPU cost; fuzzy matching expands the candidate set far beyond prefix matching and needs heavier scoring; memory competes with the user's own applications.

#### Use Case 3: Maps / Location Search (Google Maps)

- **Problem:** place names are long, multilingual, and ambiguous ("springfield" exists in dozens of states); users type fragments and expect the right place on top.
- **Solution:** autocomplete over a place corpus ranked by popularity *and* geographic proximity to the user's viewport/location, blending text prefix match with distance decay.
- **Why suitable:** place names are a closed, curated corpus (no PII risk, no bombing risk at query-log scale), and the geo signal is a powerful re-ranker that pure query-frequency systems lack.
- **How it works:** prefix match runs over a per-region trie/FST of place names; candidates are re-scored by distance to the map center and by global popularity; results include structured metadata (city, country) so the user can disambiguate visually.
- **Trade-offs:** geo re-ranking requires the user's location (privacy consent, and wrong-location results when VPN'd); per-region indexes complicate the pipeline; popularity and proximity sometimes conflict (a famous far place vs. an obscure near one) and the blend needs constant tuning.

#### Use Case 4: Help Center / Documentation Search

- **Problem:** users don't know the terminology of your docs ("billing cycle" vs. "subscription period"), file support tickets for answered questions, and churn.
- **Solution:** autocomplete over documentation titles, headings, and historically successful support queries, with suggestions linking directly to articles.
- **Why suitable:** the corpus is small (thousands of articles), curated, and changes slowly — a case where you should *not* build the full distributed pipeline: an Elasticsearch completion suggester or even a build-time-generated trie shipped to the client is enough.
- **How it works:** docs are indexed at publish time; the suggester serves prefix matches over titles and keywords; zero-result queries are logged and reviewed weekly by the docs team to close terminology gaps.
- **Trade-offs:** scale is trivial, so the trade-off is purely editorial — suggestions must be curated to avoid surfacing outdated articles; analytics review is manual but cheap at this volume.

---

### API Design and Contract

The public surface is deliberately small: one suggestion endpoint, one telemetry endpoint. All examples assume base URL `https://api.example.com`, versioned by URL prefix (`/v1`).

#### GET /v1/suggestions

Returns the top-K completions for a prefix.

**Request**

```
GET /v1/suggestions?q=goo&limit=8&locale=en-US HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
X-Client-Id: web-search
X-Session-Id: 01JZQ7K2M4
Accept: application/json
```

| Parameter | Type | Required | Validation | Description |
|-----------|------|----------|------------|-------------|
| `q` | string | yes | 1-100 chars after trim; Unicode NFC-normalized | The prefix typed so far |
| `limit` | integer | no | 1-20, default 8 | Max suggestions; server caps at the build-time K |
| `locale` | string | no | BCP-47 tag, default from account/geo | Selects the locale-specific index |
| `sessionId` | string | no | opaque, <= 64 chars | Joins impressions to clicks for telemetry |
| `personalize` | boolean | no | default true for authenticated users | Opt out of personalization |

**Success response — 200 OK**

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Cache-Control: public, max-age=300
ETag: "trie-v2026.02.14.15-loc-enUS"
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 118
X-RateLimit-Reset: 1739793660
X-Index-Version: 2026.02.14.15
```

```json
{
  "query": "goo",
  "locale": "en-US",
  "suggestions": [
    { "text": "google maps", "type": "QUERY", "score": 0.9821 },
    { "text": "google docs", "type": "QUERY", "score": 0.9510 },
    { "text": "google flights", "type": "QUERY", "score": 0.9233 },
    { "text": "goodrx", "type": "QUERY", "score": 0.8712 },
    { "text": "google scholar", "type": "PERSONALIZED", "score": 0.8601 }
  ],
  "tookMs": 3,
  "personalized": true,
  "indexVersion": "2026.02.14.15"
}
```

Notes on headers:

- `Cache-Control: public, max-age=300` — popular prefixes are shared across users, so gateway/CDN caching is safe *only* when `personalize=false`; personalized responses must return `Cache-Control: private, no-store`.
- `X-RateLimit-*` — standard IETF-style rate-limit headers so clients can self-throttle before hitting 429.
- `X-Index-Version` / `ETag` — lets clients and support correlate results with the exact snapshot that produced them (invaluable when debugging "why did X show up?").

**Rate-limited response — 429 Too Many Requests**

```
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 2
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1739793660
```

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Suggestion rate limit exceeded. Back off and retry after the indicated delay.",
    "retryAfterSeconds": 2
  }
}
```

Clients must honor `Retry-After` and apply exponential backoff with jitter on repeated 429s (see the client-side strategies discussion in the rate limiter doc, which this system depends on for protection).

**Validation failure — 400 Bad Request**

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Parameter 'limit' must be between 1 and 20.",
    "field": "limit"
  }
}
```

Also returned for empty `q` (`""` after trim) and over-long prefixes (> 100 chars). **401 Unauthorized** is returned for missing/invalid bearer tokens on personalized requests; anonymous access is allowed at a lower rate limit with `personalize` forced off. **503 Service Unavailable** with `Retry-After` is returned only if no index snapshot is loaded at all (startup); once serving, the service degrades to global suggestions rather than erroring.

#### POST /v1/suggestions/events

Records impressions and clicks; the ground truth for ranking quality.

```json
{
  "sessionId": "01JZQ7K2M4",
  "events": [
    { "type": "IMPRESSION", "prefix": "goo", "shown": ["google maps", "google docs"], "ts": "2026-02-17T10:15:30.120Z" },
    { "type": "CLICK", "prefix": "goo", "selected": "google maps", "position": 0, "ts": "2026-02-17T10:15:31.004Z" }
  ]
}
```

Response: **202 Accepted** (fire-and-forget into Kafka; never block the UI on telemetry). Validation failures return **400** with per-event error details. This endpoint requires authentication or a signed anonymous token to prevent click-fraud poisoning of the ranking pipeline.

#### Versioning and compatibility

- URI versioning (`/v1`); additive JSON fields are always permitted, so clients must ignore unknown fields.
- Breaking changes (renamed fields, changed ranking semantics exposed in the contract) ship as `/v2` with `/v1` maintained for a deprecation window announced via the `Sunset` response header.
- Auth: OAuth2 bearer tokens for personalized traffic; API keys for partner/anonymous tiers; the telemetry endpoint additionally validates a session signature to resist forged click streams.

---

### Data Modeling

Three models matter: the serving structure (trie/FST), the raw signal schema (query events), and the snapshot metadata.

#### Serving structure: trie with per-node top-K cache

The core serving data structure is a trie (prefix tree):

```mermaid
flowchart TD
    R["root"] --> G["g"]
    R --> F["f"]
    R --> A["a"]
    G --> O["o"]
    F --> FA["a"]
    A --> AP["p"]
    O --> OO["o"]
    O --> OL["l"]
    FA --> FC["c"]
    AP --> APP["p"]
    OO --> OG["g"]
    OL --> OLF["f"]
    FC --> FCE["e"]
    APP --> APPL["l"]
    OG --> OGL["l"]
    FCE --> BOOK["book"]
    APPL --> APPLE["e"]
    OGL --> OGLE["e"]
```

This trie encodes the words "google", "golf", "face", "facebook", and "apple". Each node stores:

- **Character** (or a compressed edge label, in a radix trie).
- **Top-K completions with scores, pre-computed** — the K highest-scored terminal strings in this node's subtree, computed once at build time. This is the crucial field: it makes queries O(prefix length).
- **Terminal flag** (`isEndOfWord`) plus the query's own score if the path to this node is itself a complete query.
- **Children map** — sparse; in memory a small hash map or sorted array, in serialized form an offset table.

Query walkthrough: query "go" → traverse root → 'g' → 'o' → return the pre-computed top-K list cached at that node, e.g. `["google", "google maps", "golang", "gold price", "gopro"]` — no subtree traversal, no sorting.

**Alternative serving structure — FST (Finite State Transducer):** a minimal acyclic deterministic automaton that shares *suffixes* as well as prefixes, typically 3-10x smaller than an equivalent trie at the cost of being immutable and harder to update incrementally. Lucene/Elasticsearch's completion suggester is built on FSTs. Model an FST as: states, labeled arcs, and outputs (weights) attached to final states; lookup is likewise O(prefix length). Choose a trie when you need in-place hot updates and simpler code; choose an FST when memory is the binding constraint and you rebuild wholesale anyway (which our batch pipeline does — a legitimate reason to pick FST).

#### Query event schema (the ranking input)

Stored in Kafka, then aggregated. One row per event:

| Field | Type | Purpose |
|-------|------|---------|
| `event_type` | enum(QUERY, IMPRESSION, CLICK) | distinguishes raw searches from suggestion interactions |
| `query_text` | string (Unicode NFC, PII-scrubbed) | the ranking key |
| `ts` | timestamp (event time) | decay and windowing |
| `user_id_hash` | string (salted hash) | personalization and abuse detection; never raw ids |
| `session_id` | string | joins impressions to clicks |
| `locale` | string | per-locale index building |
| `position` | int, nullable | click position for CTR analysis |

Aggregated model per (locale, query): `count_7d_decayed`, `count_1h`, `ctr`, `last_seen`. The score stored in the trie is derived from these.

#### Snapshot metadata

| Field | Purpose |
|-------|---------|
| `version` (timestamp-based, e.g. `2026.02.14.15`) | ordering and rollback |
| `locale` | per-locale indexes |
| `query_count`, `node_count`, `size_bytes` | sanity/quality gates |
| `source_window` (e.g. `7d decayed + 1h hot`) | provenance |
| `checksum` (SHA-256) | corruption detection before swap |
| `min_supported_client` | contract compatibility |

---

### High-Level Design

The architecture has two planes that meet only at the serving nodes: a **read plane** optimized for single-digit-ms lookups, and a **write/aggregation plane** that continuously rebuilds the index offline. Nothing on the read path ever waits on the write path.

```mermaid
flowchart TB
    subgraph ReadPlane["Read plane - latency critical"]
        C["Client: debounce, cache, prefetch, cancel"] -->|"HTTPS GET /v1/suggestions"| GW["API Gateway: auth, rate limit, validate, shard routing"]
        GW --> S1["Suggestion Service shard A-M"]
        GW --> S2["Suggestion Service shard N-Z"]
        S1 --> T1["In-memory trie replica 1"]
        S2 --> T2["In-memory trie replica 2"]
        PS["Personalization Service backed by Redis"] -->|"parallel lookup, 5 ms race"| S1
        PS --> S2
        S1 -->|"trie miss only"| FB["Fallback: Elasticsearch completion suggester"]
        S2 --> FB
    end
    subgraph WritePlane["Write plane - offline aggregation"]
        C -->|"impression and click events"| TEL["Telemetry endpoint"]
        TEL --> K["Kafka: query and click topics"]
        K --> BATCH["Batch job, Spark or Flink: decayed counts, prune top-N, build trie"]
        K --> STREAM["Streaming job, Flink: 1 h sliding window, spike detection"]
        BATCH -->|"immutable snapshot every 15 min"| SNAP["Snapshot store, S3 or GCS, versioned"]
        SNAP -->|"pull, verify checksum, atomic swap"| T1
        SNAP --> T2
        STREAM -->|"hot trending deltas, about every 30 s"| PUB["Redis pub/sub delta channel"]
        PUB --> T1
        PUB --> T2
    end
```

**How the pieces communicate**

- Client ↔ gateway: HTTPS/JSON (HTTP/2 or HTTP/3 to cut connection setup on mobile). Responses for non-personalized popular prefixes carry `Cache-Control` and may be edge-cached.
- Gateway → suggestion service: internal HTTP/gRPC; routing by prefix shard (range map or consistent hash on 1-2 characters).
- Serving nodes ↔ snapshot store: pull model — each node polls a `latest` pointer (or receives a notification), downloads, verifies the checksum, loads into memory off to the side, then atomically swaps its root reference. Pull (not push) keeps slow or restarting nodes from blocking the rollout.
- Streaming updater → serving nodes: pub/sub deltas, applied in place to the hot copy; deltas are idempotent and carry a TTL so they expire if the next snapshot is delayed.
- Everything → monitoring: latency per stage, snapshot age, CTR, zero-result rate.

**Data flow: one keystroke**

```mermaid
sequenceDiagram
    autonumber
    participant CL as Client
    participant GW as API Gateway
    participant SS as Suggestion Service
    participant TR as Trie Snapshot
    participant PZ as Personalization Service
    participant TEL as Telemetry Kafka

    CL->>CL: debounce 100-150 ms, check prefix cache
    CL->>GW: GET /v1/suggestions?q=goo&limit=8
    GW->>GW: auth, rate limit check, validate q and limit
    GW->>SS: route to shard for prefix g
    par parallel lookups
        SS->>TR: walk g -> o -> o, read cached top-K
        TR-->>SS: candidate list, under 1 ms
        SS->>PZ: fetch user profile, hard 5 ms timeout
        PZ-->>SS: personal candidates or timeout
    end
    SS->>SS: merge and re-rank, truncate to limit
    SS-->>GW: 200 OK plus suggestions plus X-Index-Version
    GW-->>CL: JSON, Cache-Control when not personalized
    CL->>TEL: async impression and later click events
    CL->>CL: cache results, prefetch likely next prefix
```

The sequence diagram shows the two latency-critical tricks: the trie read is a single cached-list fetch, and personalization runs **in parallel** with a race timeout so it can improve but never delay the response.

**Data flow: index refresh**

```mermaid
sequenceDiagram
    autonumber
    participant K as Kafka
    participant B as Batch Job
    participant ST as Stream Job
    participant SNAP as Snapshot Store
    participant PUB as Delta Channel
    participant SRV as Suggestion Servers

    loop every 15 minutes
        K->>B: consume query and click window
        B->>B: aggregate, decay, rank, prune to top-N
        B->>SNAP: publish trie snapshot vN plus checksum
        SNAP-->>SRV: latest pointer updated
        SRV->>SNAP: pull snapshot, verify checksum
        SRV->>SRV: load beside live index, atomic swap root
    end
    loop every 30 seconds
        K->>ST: consume recent events
        ST->>ST: sliding window rate, spike vs baseline
        ST->>PUB: publish hot deltas, idempotent, TTL
        PUB-->>SRV: apply deltas to in-memory copy
    end
```

The batch loop is authoritative — each new snapshot wipes the accumulated deltas, so the streaming layer can never permanently poison rankings.

**Scaling**

- **Stateless serving tier**: scale suggestion servers horizontally behind the balancer; every replica of a shard is interchangeable.
- **Shard trie by prefix** when one node's RAM or NIC is exceeded: servers A-M on cluster 1, N-Z on cluster 2; split further (A-E, F-M …) as hot ranges emerge. Each shard replicated 3x for availability.
- **Geographic**: run per-region/per-locale tries — trending topics differ by country, and regional serving keeps RTTs low.
- **Aggregation tier**: Kafka partitioning by (locale, query-hash) lets the batch and streaming jobs scale out by adding consumers.

**Failure handling**

- Suggestion node dies → balancer routes to replicas; the restarted node pulls `latest` snapshot and rejoins. No data loss — the index is reproducible from the store.
- Snapshot store unavailable → serving continues on the current snapshot (stale but valid); rollout retries with backoff.
- Streaming job down → trending freshness degrades to the 15-minute batch cadence; no serving impact.
- Personalization down → 5 ms race times out; responses fall back to global rankings silently.
- Kafka backlog → batch window widens; quality gates on the snapshot (size and zero-result deltas vs. previous version) catch pathological builds before fleet rollout.
- Bad snapshot → canary shard detects quality-gate regression; automatic rollback to the previous version pointer.

---

### Deep Dive

This section goes under the hood of the decisions that make or break the system: the trie itself, sharding, update cadence, personalization, typo tolerance, the latency budget, and the serious alternatives to a trie.

#### 1. Trie optimization: making a planet-scale index fit and fly

The naive problems and the standard fixes:

```
Problem: Plain trie with billions of strings is too large for memory

Solution 1: Only store top queries
  - Keep top 10M queries (covers ~99% of searches, by Zipf's law)
  - Long-tail handled by fallback to Elasticsearch

Solution 2: Pre-compute top-K at each node
  - Don't traverse subtree at query time
  - Each node already has ["google", "gmail", ...] cached
  - Query = O(prefix_length), not O(subtree_size)

Solution 3: Compressed trie (Patricia trie)
  - Collapse single-child chains: g-o-o-g-l-e -> "google"
  - 50%+ memory reduction
```

All three stack: a Patricia-compressed trie of the top-10M queries with per-node top-K caches lands at the ~6-8 GB figure from the capacity estimation — one machine's RAM, serving the head of a planet-scale query distribution.

#### 2. Trie with top-K cached per node: construction and query in Java

The serving index as a Spring-managed bean. Two ideas do all the work: **insert with weight, then a bottom-up merge pass** computes every node's top-K; and the **root reference is volatile** so a rebuilt trie swaps in atomically (Pattern 3).

```java
package com.example.autocomplete.index;

/** A single autocomplete suggestion with its ranking score. */
public record ScoredSuggestion(String text, double score) {
}
```

```java
package com.example.autocomplete.index;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** Mutable during build; treated as immutable once published. */
final class TrieNode {
    final Map<Character, TrieNode> children = new HashMap<>();
    final List<ScoredSuggestion> topK = new ArrayList<>();
    String terminalText;      // non-null if a complete query ends here
    double terminalScore;
}
```

```java
package com.example.autocomplete.index;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;

/**
 * In-memory autocomplete index.
 *
 * Reads are lock-free: query() walks the currently published snapshot.
 * publish() atomically swaps in a freshly built trie (copy-on-write serving).
 */
@Component
public class TrieIndex {

    private final int topK;
    private volatile TrieNode root = new TrieNode();

    public TrieIndex(@Value("${autocomplete.top-k:10}") int topK) {
        this.topK = topK;
    }

    /** O(prefix length): walk one node per char, return the cached list. */
    public List<ScoredSuggestion> query(String prefix, int limit) {
        TrieNode node = root;
        for (int i = 0; i < prefix.length(); i++) {
            node = node.children.get(Character.toLowerCase(prefix.charAt(i)));
            if (node == null) {
                return List.of();          // head miss -> caller may use fallback
            }
        }
        return node.topK.size() <= limit
                ? List.copyOf(node.topK)
                : List.copyOf(node.topK.subList(0, limit));
    }

    /** Build a complete new trie off to the side, then swap it in atomically. */
    public void publish(Map<String, Double> weightedQueries) {
        TrieNode newRoot = new TrieNode();
        weightedQueries.forEach((query, weight) -> insert(newRoot, query, weight));
        computeTopK(newRoot);
        this.root = newRoot;               // single volatile write: readers never see a partial index
    }

    private void insert(TrieNode newRoot, String query, double weight) {
        TrieNode node = newRoot;
        for (char c : query.toLowerCase().toCharArray()) {
            node = node.children.computeIfAbsent(c, k -> new TrieNode());
        }
        node.terminalText = query;
        node.terminalScore = weight;
    }

    /** Bottom-up: each node merges its own terminal entry with its children's top-K. */
    private List<ScoredSuggestion> computeTopK(TrieNode node) {
        PriorityQueue<ScoredSuggestion> best =
                new PriorityQueue<>(Comparator.comparingDouble(ScoredSuggestion::score));
        if (node.terminalText != null) {
            best.add(new ScoredSuggestion(node.terminalText, node.terminalScore));
        }
        for (TrieNode child : node.children.values()) {
            best.addAll(computeTopK(child));
        }
        while (best.size() > topK) {
            best.poll();                   // drop the lowest scores, keep top-K
        }
        List<ScoredSuggestion> merged = new ArrayList<>(best);
        merged.sort(Comparator.comparingDouble(ScoredSuggestion::score).reversed());
        node.topK.clear();
        node.topK.addAll(merged);
        return merged;
    }
}
```

Why this shape: `query()` touches exactly `prefix.length()` nodes and copies a small list — typically under 1 ms — regardless of how many millions of queries the index holds. `publish()` does all expensive work (insertion, merging, sorting) on a private structure that no reader can see, then flips one reference. Complexity: build is O(total characters + nodes × K log K); memory is O(nodes × K); query is O(prefix length).

#### 3. Trie sharding by prefix

- **Why shard at all:** a single replica holds ~6-8 GB — fine. You shard when (a) per-node QPS exceeds CPU/NIC, (b) the index outgrows one heap (multi-locale deployments), or (c) you want failure isolation per range.
- **Scheme:** range-shard on the first 1-2 characters (`a-m`, `n-z`, or finer like `aa-cz`). The gateway holds a small routing table. Consistent hashing on the prefix also works and rebalances less painfully, but range sharding keeps shard maps human-readable, which matters at 3 a.m.
- **Hot shards:** popularity per letter is wildly unequal. Split hot ranges (`f` alone may deserve a shard in en-US because of "facebook…", "fox news…"), replicate them more, and consider caching the hottest prefixes at the gateway so they never reach the trie fleet.
- **Replication:** 3 replicas per shard behind the balancer; any replica can answer any query for its range, so failure handling is just health-checked load balancing.
- **Resharding:** build the new partition's trie offline from the same aggregated data, publish it, then flip the gateway's routing table — never try to split a live trie in place.

#### 4. Update and rebuild frequency

```
User searches -> Kafka topic -> Flink streaming job
  -> Sliding window count (last 1 hour)
  -> Detect spikes: current_rate / baseline_rate > threshold
  -> If trending: inject into trie with bonus score
  -> Push updated trie segment to servers

Full trie rebuild: Every 15 minutes (batch)
Hot updates: Every 30 seconds (streaming, trending only)
```

The reasoning behind the numbers: a 15-minute batch cycle keeps each rebuild cheap (a few hundred million aggregated records) while bounding worst-case staleness for *ordinary* ranking drift to 15 minutes — fine, because non-trending popularity moves slowly. The 30-second streaming path exists solely for *spikes*, where 15 minutes is an eternity (breaking news). Baselines come from the same time-of-day window over prior days, so "election results" at 9 p.m. is compared against typical 9 p.m. volume, not against the daily average. Deltas carry a TTL and are wiped by the next authoritative snapshot, so a misfired spike detection self-heals within one batch cycle.

#### 5. Ranking signals

```
score = alpha × query_frequency
      + beta  × recency_boost
      + gamma × personalization_score
      + delta × trending_bonus

query_frequency: How many times this query was searched (decayed over the window)
recency_boost:   Decay older queries (exponential decay over the aggregation window)
personalization: Based on the user's search history
trending_bonus:  Spike detection -> boost rapidly rising queries
```

Keep the formula linear, explicit, and shared as a library between the batch and streaming jobs. Linear blends are debuggable ("which term moved this suggestion?") and tunable by non-specialists; exotic ML rankers can come later as an additional feature inside the same blend, but the day-one system should be one you can reason about during an incident.

#### 6. Personalization layer

- **Where it lives:** *outside* the shared trie. The per-node top-K cache is global by construction — per-user entries would explode memory (K entries per node per user is absurd) and leak one user's history into another's suggestions.
- **Design:** a compact per-user profile (last N queries, topic affinity vector) in Redis, keyed by salted user hash. At query time the suggestion service fires the trie lookup and the profile fetch **in parallel**, races them with a ~5 ms budget, then re-ranks: personal candidates matching the prefix are blended into the global top-K with weight `gamma`, and the merged list is truncated to `limit`.
- **Freshness:** the profile updates from the same Kafka stream with seconds-level lag, which is plenty — personal intent changes slowly within a session.
- **Privacy rules:** never let a query that appears *only* in a user's personal history surface to other users (enforce a minimum global frequency before anything enters the shared trie); honor `personalize=false` and deletion requests by dropping the profile.
- **Failure mode:** profile lookup timeout or Redis outage silently degrades to global suggestions — by design; personalization must never take down the serving path.

#### 7. Typo tolerance

Pure prefix matching fails on the first typo ("resturant" suggests nothing). Standard mitigations, in increasing cost order:

1. **Edit-distance-1 prefix expansion (online).** For short prefixes, also probe the trie with one deletion/insertion/substitution/transposition applied to the last character or two ("restu…" also probes "resta…"). Constant-factor more lookups (alphabet-size × positions), still microsecond-cheap, catches the majority of fat-finger errors. Only enable after a minimum prefix length (~3 chars) to bound the fan-out.
2. **Fuzzy FST (Levenshtein automaton).** Lucene-style: intersect the query's edit-distance automaton with the index FST — elegantly O(1) per candidate, but read-only and build-time only.
3. **SymSpell-style deletion index (offline-built).** Precompute all distance-1 deletions of each dictionary term ("restaurant" → "estaurant", "rstaurant", …) into a hash map from deletion → original terms; at query time generate deletions of the prefix and look them up. Very fast, moderate memory, excellent for head queries.
4. **Fallback path.** Rare/garbled prefixes fall through to Elasticsearch, whose `fuzzy` matching and edge-n-grams handle them at relaxed latency.

Guardrail: typo-tolerant candidates should be appended *below* exact-prefix results and marked, never silently interleaved — a wrong "correction" is more annoying than no suggestion.

#### 8. Latency budget breakdown

Where the <100 ms end-to-end budget goes (typical p99, user on a good connection to a nearby PoP):

| Stage | Budget | Notes |
|-------|--------|-------|
| Client debounce | 100-150 ms | deliberate wait; *not* counted against the service budget but dominates perceived latency design |
| Network RTT (edge-terminated TLS) | 10-30 ms | TLS resumption/HTTP3 keeps handshake near zero for repeat visitors |
| Gateway: auth, rate limit, validation | 2-5 ms | token verify cached; rate limit check is a Redis Lua round trip |
| Shard routing | <1 ms | routing table lookup |
| Trie lookup | 0.5-2 ms | O(prefix length), cached top-K, warm CPU caches |
| Personalization race | 0-5 ms | parallel; hard timeout, silently dropped on expiry |
| Serialization + egress | 1-2 ms | ~1 KB JSON |
| **Server total (p99)** | **<25 ms** | comfortably inside the 50 ms server-side NFR |
| **End-to-end (p99)** | **<100 ms** | network dominates; this is why edge termination matters |

Two implications: first, *server work is nearly free in this budget* — the fight is against network distance and client behavior, which is why edge PoPs, HTTP/3, and client caching appear in a "data structure" design. Second, anything that adds a *serial* network hop to the hot path (a synchronous personalization call, a fallback query on every request) must justify itself against this table.

#### 9. Alternatives to the trie — honest comparison

| Approach | Lookup cost | Memory | Mutable? | Ranking flexibility | When it wins |
|----------|-------------|--------|----------|--------------------|--------------|
| Trie + per-node top-K (this design) | O(prefix len) | ~120-150 B/node; ~7 GB for 10M queries | yes (rebuild/swap; deltas in place) | full control of score blend | maximum control, sub-ms latency, custom ranking |
| FST (Lucene-style) | O(prefix len) | 3-10x smaller (shares suffixes) | no — rebuild only | weights baked in at build | memory-bound, rebuild-anyway pipelines |
| N-gram inverted index | posting-list intersection, tens of ms | moderate | easy incremental updates | per-document scoring, BM25-ish | when you already run a search engine and QPS is modest |
| Elasticsearch completion suggester | O(prefix len) over an FST | low (FST in heap/off-heap) | near-real-time via indexing | contexts for boosting/filtering; less custom logic | teams that want production-grade autocomplete without building it |

**Recommendation logic:** below ~10K QPS or without a dedicated team, use Elasticsearch's completion suggester — it is an FST with context boosting, near-real-time updates, and ops you already know. Build the custom trie pipeline when you need single-digit-ms p99 at 100K+ QPS, exotic ranking blends, or per-node memory control that ES cannot give you. Many real systems do both: trie for the head, ES for the long tail (Pattern 6).

#### 10. Key design decisions (summary)

| Decision | Choice | Reason |
|----------|--------|--------|
| Data structure | Compressed trie with pre-computed top-K | O(prefix) query, memory efficient |
| Storage | In-memory on each server | < 50 ms latency requirement |
| Update | Batch (15 min) + streaming (30 s for trending) | Freshness vs rebuild cost |
| Client | Debounce + local cache + pre-fetch | Reduce server load, better UX |
| Fallback | Elasticsearch for long-tail queries | Trie only has top queries |

#### 11. Scaling considerations (recap with rationale)

- **Shard trie by prefix**: servers A-M on cluster 1, N-Z on cluster 2 — scales memory and isolates hot ranges; reshard offline, never in place.
- **Replication**: each shard replicated 3x for availability — reads are stateless, so replicas need no coordination.
- **Geographic**: regional tries (different trending topics per country) — freshness and RTT both improve with locale-local indexes.
- **Personalization**: per-user layer on top of global trie (lightweight) — a parallel Redis-backed re-rank, never inside the shared structure.

---

### Java and Spring Boot Implementation Guide

A complete, production-shaped implementation of the serving tier using Spring Boot 3.x and Java 17+. The offline pipeline (Spark/Flink) is out of process by design; this guide covers everything on the read path plus snapshot loading.

#### Project layout

```
com.example.autocomplete
├── AutocompleteApplication.java
├── config/AutocompleteProperties.java
├── index/TrieIndex.java                 (from Deep Dive)
├── index/ScoredSuggestion.java
├── index/TrieNode.java
├── service/SuggestionService.java
├── service/SnapshotLoader.java
├── service/PersonalizationClient.java
├── web/SuggestionController.java
└── web/dto/SuggestionDtos.java
```

#### Externalized configuration

Never hardcode tuning knobs; they change per environment and during incidents.

```java
package com.example.autocomplete.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "autocomplete")
public record AutocompleteProperties(
        int topK,                 // suggestions cached per trie node
        int maxLimit,             // API cap for the limit parameter
        int maxPrefixLength,      // abuse guard
        String snapshotUri,       // e.g. s3://bucket/trie/en-US/latest
        long reloadIntervalMs     // snapshot poll cadence
) {
}
```

```yaml
autocomplete:
  top-k: 10
  max-limit: 20
  max-prefix-length: 100
  snapshot-uri: s3://acme-trie-snapshots/en-US/latest
  reload-interval-ms: 60000
```

Enable it in the application class:

```java
package com.example.autocomplete;

import com.example.autocomplete.config.AutocompleteProperties;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;
import org.springframework.scheduling.annotation.EnableScheduling;

@EnableScheduling
@ConfigurationPropertiesScan(basePackageClasses = AutocompleteProperties.class)
@SpringBootApplication
public class AutocompleteApplication {
    public static void main(String[] args) {
        SpringApplication.run(AutocompleteApplication.class, args);
    }
}
```

#### Suggestion service

Constructor-injected, stateless apart from the `TrieIndex` bean it delegates to; personalization is raced with a timeout and silently dropped on failure.

```java
package com.example.autocomplete.service;

import com.example.autocomplete.config.AutocompleteProperties;
import com.example.autocomplete.index.ScoredSuggestion;
import com.example.autocomplete.index.TrieIndex;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

@Service
public class SuggestionService {

    private static final Logger log = LoggerFactory.getLogger(SuggestionService.class);

    private final TrieIndex trieIndex;
    private final PersonalizationClient personalization;
    private final AutocompleteProperties props;

    public SuggestionService(TrieIndex trieIndex,
                             PersonalizationClient personalization,
                             AutocompleteProperties props) {
        this.trieIndex = trieIndex;
        this.personalization = personalization;
        this.props = props;
    }

    public SuggestionResult suggest(String rawPrefix, int limit, String userIdHash, boolean personalize) {
        String prefix = normalize(rawPrefix);
        List<ScoredSuggestion> global = trieIndex.query(prefix, props.topK());

        if (!personalize || userIdHash == null) {
            return new SuggestionResult(truncate(global, limit), false);
        }
        // Race personalization against a hard budget: it may improve, never delay.
        CompletableFuture<List<ScoredSuggestion>> personal =
                CompletableFuture.supplyAsync(() -> personalization.candidatesFor(userIdHash, prefix))
                        .completeOnTimeout(List.of(), 5, TimeUnit.MILLISECONDS)
                        .exceptionally(ex -> {
                            log.warn("personalization failed, falling back to global: {}", ex.toString());
                            return List.of();
                        });
        List<ScoredSuggestion> merged = mergeAndRerank(global, personal.join());
        return new SuggestionResult(truncate(merged, limit), true);
    }

    private String normalize(String raw) {
        String trimmed = raw == null ? "" : raw.trim();
        if (trimmed.isEmpty() || trimmed.length() > props.maxPrefixLength()) {
            throw new IllegalArgumentException("prefix length must be 1.." + props.maxPrefixLength());
        }
        return java.text.Normalizer.normalize(trimmed, java.text.Normalizer.Form.NFC);
    }

    private List<ScoredSuggestion> mergeAndRerank(List<ScoredSuggestion> global,
                                                  List<ScoredSuggestion> personal) {
        List<ScoredSuggestion> merged = new ArrayList<>(global.size() + personal.size());
        merged.addAll(global);
        personal.stream()
                .filter(p -> global.stream().noneMatch(g -> g.text().equalsIgnoreCase(p.text())))
                .forEach(merged::add);
        merged.sort(Comparator.comparingDouble(ScoredSuggestion::score).reversed());
        return merged;
    }

    private List<ScoredSuggestion> truncate(List<ScoredSuggestion> list, int limit) {
        return list.size() <= limit ? list : List.copyOf(list.subList(0, limit));
    }

    public record SuggestionResult(List<ScoredSuggestion> suggestions, boolean personalized) {
    }
}
```

#### Snapshot loader (scheduled, atomic swap)

```java
package com.example.autocomplete.service;

import com.example.autocomplete.config.AutocompleteProperties;
import com.example.autocomplete.index.TrieIndex;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.Map;

/**
 * Polls the snapshot store and hot-swaps the serving trie.
 * Quality gates refuse pathological builds so a bad snapshot never reaches the fleet.
 */
@Service
public class SnapshotLoader {

    private static final Logger log = LoggerFactory.getLogger(SnapshotLoader.class);
    private static final double MAX_SIZE_DELTA_RATIO = 3.0;

    private final TrieIndex trieIndex;
    private final SnapshotStoreClient store;     // thin client over S3/GCS
    private final AutocompleteProperties props;
    private volatile String currentVersion = "";

    public SnapshotLoader(TrieIndex trieIndex, SnapshotStoreClient store, AutocompleteProperties props) {
        this.trieIndex = trieIndex;
        this.store = store;
        this.props = props;
    }

    @Scheduled(fixedDelayString = "${autocomplete.reload-interval-ms:60000}")
    public void refreshIfNeeded() {
        try {
            SnapshotMeta meta = store.latestMeta(props.snapshotUri());
            if (meta.version().equals(currentVersion)) {
                return;
            }
            Map<String, Double> weightedQueries = store.downloadAndVerify(meta); // checksum verified here
            if (weightedQueries.size() < meta.queryCount() / MAX_SIZE_DELTA_RATIO
                    || weightedQueries.size() > meta.queryCount() * MAX_SIZE_DELTA_RATIO) {
                log.error("refusing snapshot {}: size delta vs manifest too large", meta.version());
                return;
            }
            trieIndex.publish(weightedQueries);   // atomic swap; old snapshot GC'd after drain
            currentVersion = meta.version();
            log.info("serving trie snapshot {} with {} queries", meta.version(), weightedQueries.size());
        } catch (Exception e) {
            // Keep serving the current (stale but valid) snapshot; alert via metrics.
            log.error("snapshot refresh failed, continuing on {}", currentVersion, e);
        }
    }
}
```

#### Controller with DTO records, headers, and status codes

```java
package com.example.autocomplete.web;

import com.example.autocomplete.index.ScoredSuggestion;
import com.example.autocomplete.service.SuggestionService;
import org.springframework.http.CacheControl;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.concurrent.TimeUnit;

@RestController
@RequestMapping("/v1/suggestions")
public class SuggestionController {

    private final SuggestionService suggestions;

    public SuggestionController(SuggestionService suggestions) {
        this.suggestions = suggestions;
    }

    @GetMapping
    public ResponseEntity<SuggestionResponse> suggest(
            @RequestParam("q") String q,
            @RequestParam(defaultValue = "8") int limit,
            @RequestParam(defaultValue = "true") boolean personalize,
            @RequestHeader(value = "X-User-Hash", required = false) String userHash) {

        if (limit < 1 || limit > 20) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                    "limit must be between 1 and 20");
        }
        long start = System.nanoTime();
        SuggestionService.SuggestionResult result;
        try {
            result = suggestions.suggest(q, limit, userHash, personalize);
        } catch (IllegalArgumentException e) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, e.getMessage());
        }
        long tookMs = TimeUnit.NANOSECONDS.toMillis(System.nanoTime() - start);

        List<SuggestionItem> items = result.suggestions().stream()
                .map(s -> new SuggestionItem(s.text(), "QUERY", s.score()))
                .toList();

        CacheControl cache = result.personalized()
                ? CacheControl.noStore()                       // per-user data: never shared-cache
                : CacheControl.maxAge(5, TimeUnit.MINUTES).cachePublic();

        return ResponseEntity.ok()
                .cacheControl(cache)
                .header("X-Index-Version", "2026.02.14.15")   // inject from SnapshotLoader in real code
                .body(new SuggestionResponse(q, items, tookMs, result.personalized()));
    }

    public record SuggestionItem(String text, String type, double score) {
    }

    public record SuggestionResponse(String query, List<SuggestionItem> suggestions,
                                     long tookMs, boolean personalized) {
    }
}
```

#### Production checklist for this service

- **Rate limiting:** enforce per-client quotas in a gateway filter or a Spring `HandlerInterceptor` backed by Redis before requests reach this controller, returning `429` with `Retry-After` and `X-RateLimit-*` headers (the full implementation, including the Lua script, is covered in the rate-limiter doc in this series).
- **GC tuning:** the heap holds a multi-GB immutable index plus swap-time doubling; use ZGC or G1 with a pause target ≤ 10 ms and size the heap at ≥ 2.5x index size.
- **Metrics:** export lookup latency histograms, snapshot age, and fallback rate via Micrometer; alert on snapshot age > 2× the batch interval.
- **Testing:** unit-test `TrieIndex.publish/query` for correctness and atomicity under concurrent reads; load-test p99 with production-size snapshots, not toy data; contract-test the API against the JSON shapes in the API Design section.

---

### Interview Questions and Answers

Progressive: warm-ups first, senior-level depth later. Each answer includes what a strong candidate adds, follow-ups you should expect, and common mistakes.

**Q1 (beginner): What is autocomplete and why is it a distinct system design problem?**

A: Autocomplete maps every possible query prefix to its top-K most likely completions, served per keystroke. It is distinct because it combines an extreme latency budget (perceived instant, <100 ms end-to-end), QPS that is a multiple of search traffic (one search = many prefix requests), and a ranking problem (popularity + recency + trends + personalization) that must be resolved *before* query time, not during it.
*Strong candidates add:* it is read-only and approximation-tolerant, which licenses precomputation and caching everywhere.
*Common mistake:* treating it as "just a database query with a LIKE clause".

**Q2 (beginner): What data structure would you use and why?**

A: A trie (prefix tree): the prefix itself is the access path, and all completions of a prefix hang under one node. Augment every node with a pre-computed top-K list so query time is O(prefix length) — walk K characters, read a cached list.
*Follow-up:* why not a hash map of prefix→list? It works but stores every prefix of every query explicitly (memory blow-up and no sharing); the trie shares prefixes structurally and compresses well.
*Common mistake:* proposing a plain trie without the top-K cache — that reintroduces subtree scans at query time.

**Q3 (beginner): How do you rank the suggestions?**

A: Start with historical query frequency aggregated over a decaying window (recent counts weigh more). Then blend: `score = α·frequency + β·recency + γ·personalization + δ·trending`. Keep the blend linear and explicit so quality regressions are debuggable.
*Follow-up:* where does personalization live? Outside the shared trie, as a per-user re-rank layer merged at query time — per-user data cannot go into a shared pre-computed cache.
*Common mistake:* ranking by raw all-time frequency, which fossilizes old popular queries and misses trends entirely.

**Q4 (mid): Walk me through the latency budget for one keystroke.**

A: Network RTT to a nearby edge PoP (10-30 ms) dominates; gateway auth/rate-limit/validation 2-5 ms; trie lookup 0.5-2 ms because top-K is cached per node; personalization raced in parallel with a ~5 ms timeout; serialization ~1 ms. Server total <25 ms p99, end-to-end <100 ms. The design fights network distance (edge termination, HTTP/3) and client chatter (debounce, cache), not server compute.
*Common mistake:* quoting only the trie lookup time and ignoring network and gateway stages — interviewers read that as "has never run a user-facing system".

**Q5 (mid): How do you keep suggestions fresh? How do trending queries get in?**

A: Two layers. Batch: every ~15 minutes, recompute decayed counts from the query log, rebuild the full trie, publish an immutable snapshot that servers pull and atomically swap in. Streaming: a Flink job maintains 1-hour sliding-window rates, detects spikes against time-of-day baselines, and pushes hot deltas (with TTLs) to serving nodes every ~30 seconds. The next snapshot wipes deltas, so the streaming layer can never permanently corrupt rankings.
*Follow-up:* why not rebuild every minute? Cost and distribution fan-out — rebuilding 7 GB across hundreds of replicas every minute wastes compute and egress for ranking drift that, outside spikes, barely moves in 15 minutes.
*Trade-off:* freshness vs. rebuild/distribution cost; the lambda split buys both.

**Q6 (mid): How does the system scale to hundreds of thousands of QPS?**

A: (1) Client reduces requests 3-5x via debounce/cache/pre-fetch/cancel. (2) Serving is stateless in-memory reads — add replicas linearly. (3) Shard by prefix range when one node's RAM/QPS caps out; replicate each shard 3x; split hot ranges. (4) Cache ultra-popular prefixes at the gateway/edge. (5) The aggregation tier scales via Kafka partitioning.
*Common mistake:* reaching for sharding immediately. The head index fits one heap; replicate first, shard only when measured memory or NIC limits demand it.

**Q7 (mid): Estimate the memory for the serving index.**

A: Keep the top 10M queries (Zipf: they cover ~99% of traffic). Average 30 chars, heavy prefix sharing → ~40M trie nodes. Each node: sparse child pointers (~30 B), top-10 list of references (~80 B), flags/scores (~16 B) → ~130-150 B. Total ≈ 6 GB + string pool ≈ 7-8 GB — one server. All billion unique queries would be ~100x that; hence head-only + fallback.
*Follow-up:* how to shrink further? Patricia compression (50%+), or an FST (3-10x, sharing suffixes too) if you accept build-only immutability.

**Q8 (mid): How do you handle personalization without blowing the latency budget?**

A: Per-user profile (recent queries, topic affinities) in Redis, fetched *in parallel* with the trie lookup under a hard ~5 ms race; merge personal prefix-matching candidates into the global top-K with weight γ and truncate. On timeout or outage, silently serve global results. Personal-only queries must never leak into the shared index (minimum global frequency threshold).
*Trade-off:* personalization lifts CTR but adds a serial merge step and a privacy surface; the race pattern caps its worst-case cost at 5 ms.

**Q9 (senior): The batch job publishes a bad snapshot (garbage rankings). Walk through your defenses.**

A: Prevention: checksum verification, manifest cross-checks (query/node counts within a sane delta of the previous build), and automated quality gates (zero-result rate and CTR on a replayed query sample) before the `latest` pointer moves. Containment: canary rollout to one shard first with automatic rollback triggers. Recovery: snapshots are versioned and immutable — flip the pointer back; serving nodes re-pull. Because serving is read-only and every snapshot is reproducible from the query log, the blast radius is bounded and recovery is minutes, not a restore-from-backup ordeal.
*Common mistake:* having no quality gate between "job finished" and "fleet serves it" — completion is not correctness.

**Q10 (senior): Compare trie, FST, n-gram index, and Elasticsearch's completion suggester. When do you choose each?**

A: Trie+top-K: full ranking control, mutable-ish (swap + deltas), sub-ms; choose at high QPS with custom ranking. FST: same O(prefix) lookup at 3-10x less memory but build-only; choose when memory-bound and you rebuild wholesale anyway (we do). N-gram inverted index: easy incremental updates and fuzzy matching but tens-of-ms lookups; fine at modest QPS. ES completion suggester: production-ready FST with contexts and near-real-time indexing; choose it when you lack the team/traffic to justify a custom pipeline — and as the long-tail fallback even when you have one.
*Common mistake:* religious attachment to the trie; the honest senior answer includes "don't build this if ES already meets your SLOs".

**Q11 (senior): How do you make the system resilient to abuse — scraping, DoS, suggestion bombing, PII leakage?**

A: Endpoint: gateway rate limiting with 429 + Retry-After, input caps (prefix length, K), bot detection. Ranking pipeline: per-user/IP velocity filters so coordinated searching can't inject phrases; minimum global-frequency thresholds before anything enters the shared index; blocklists plus human review for sensitive categories. Privacy: PII pattern scrubbing at ingestion, salted user hashes, personalized-only queries never shared, deletion honored by profile purge and next-snapshot rebuild.
*Follow-up:* why scrub at ingestion rather than at serving? Serving-time filtering is too late — the PII is already persisted and replicated through snapshots; ingestion is the only single point of control.

**Q12 (senior): How would you support multiple languages and locales?**

A: One index per locale, driven off the same pipeline code with locale as config: Kafka partitioned by locale, per-locale snapshots and routing. Unicode handling: NFC normalization at ingestion and query time; case folding where scripts have case; segmentation for scripts without spaces (CJK) so multi-word suggestions tokenize correctly; IME awareness on the client (composition events are not keystrokes — debounce must wait for composition end). Trends are computed per locale because topics differ by country.
*Trade-off:* locale-per-index multiplies snapshots, shards, and operational surface — justified by ranking quality and regional latency.

**Q13 (senior): What metrics tell you autocomplete is healthy — beyond latency?**

A: Quality SLIs: suggestion CTR (the ground truth), zero-result rate per locale, position-of-click distribution (are users picking #1?). Freshness: snapshot age, streaming lag. Efficiency: cache hit rates (client/gateway), fallback rate (should be <1%), QPS per search session (client debounce effectiveness). Reliability: swap duration, GC p99 during swaps. A latency-green / CTR-red state is the classic "fast but broken" failure that pure infra monitoring misses.

**Q14 (system design): Design the end-to-end system in 45 minutes — what order do you present?**

A: (1) Requirements: functional (top-K per prefix, ranked, trending, personalization) and non-functional (<100 ms E2E, 100K+ QPS, 99.99%, minutes-level freshness). (2) Capacity: 10B req/day → ~116K QPS avg / 350K peak; top-10M head → ~7 GB index. (3) Core data structure: trie + per-node top-K; query O(prefix). (4) HLD: client debounce → gateway → stateless suggestion tier (sharded, replicated) → fallback ES; Kafka → batch rebuild (15 min, snapshots, atomic swap) + streaming trending (30 s deltas). (5) Deep dives per interviewer interest: ranking blend, personalization race, sharding, abuse handling, typo tolerance. (6) Trade-offs and metrics. This order front-loads the decisions that constrain everything else (latency budget and index size) before component plumbing.
*Common mistake:* drawing boxes for 20 minutes before stating the latency and memory numbers — the numbers *are* the design here.

**Q15 (system design): What would you deliberately simplify for a first production version, and what would you never cut?**

A: Simplify: single locale, no personalization (global ranking only), no streaming layer (15-minute batch only), no sharding (replicated single index), ES as both head and tail if QPS allows. Never cut: per-node top-K precomputation (it *is* the latency story), immutable snapshots with atomic swap (rollback is your incident plan), client debounce/cancel (cheap and multiplies capacity), PII scrubbing and rate limiting (security incidents are not iteration-friendly), and CTR telemetry (you cannot improve ranking you cannot measure).
