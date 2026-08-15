# Design Autocomplete / Typeahead

## Blogs and websites

## Medium

## Youtube

## Theory

### Problem Statement
Design a search autocomplete (typeahead) system that suggests relevant completions as users type, providing real-time suggestions with low latency.

### Functional Requirements
- Return top-K suggestions as user types each character
- Rank suggestions by popularity/relevance
- Support prefix matching ("goo" → "google maps", "google docs", ...)
- Update suggestions based on trending queries
- Personalized suggestions (optional)
- Handle multi-language input

### Non-Functional Requirements
- **Latency**: < 50ms per keystroke (suggestions must feel instant)
- **Scale**: 10B+ queries/day, 100K+ QPS
- **Freshness**: Trending queries appear within minutes
- **Availability**: 99.99%
- **Storage**: Billions of unique query strings

### Core Data Structure: Trie

```
Trie (prefix tree):

          (root)
         /  |  \
        g   f   a
       /    |    \
      o     a     p
     / \    |     |
    o   l   c     p
    |   |   |     |
    g   f   e     l
    |       |     |
    l      book   e
    |
    e
    
Each node stores:
  - Character
  - Top-K completions with scores (pre-computed)
  - isEndOfWord flag

Query "go" → traverse to 'g' → 'o' → return pre-computed top-K:
  ["google", "google maps", "golang", "gold price", "gopro"]
```

### Two-Layer Architecture

```
┌──────────┐     ┌──────────┐     ┌───────────────────────┐
│  Client  │────▶│  API GW  │────▶│  Suggestion Service    │
│          │     │          │     │                        │
│  Debounce│     └──────────┘     │  ┌──────────────────┐ │
│  (100ms) │                      │  │ In-Memory Trie   │ │
└──────────┘                      │  │ (per server)     │ │
                                  │  └────────┬─────────┘ │
                                  └───────────┼───────────┘
                                              │ periodic sync
                                              ▼
                                  ┌───────────────────────┐
                                  │  Aggregation Service   │
                                  │                        │
                                  │  Kafka → Flink →       │
                                  │  Update query counts   │
                                  │  → Rebuild trie        │
                                  │  → Push to servers     │
                                  └───────────────────────┘
```

### Trie Optimization

```
Problem: Plain trie with billions of strings is too large for memory

Solution 1: Only store top queries
  - Keep top 10M queries (covers 99% of searches)
  - Long-tail handled by fallback to Elasticsearch

Solution 2: Pre-compute top-K at each node
  - Don't traverse subtree at query time
  - Each node already has ["google", "gmail", ...] cached
  - Query = O(prefix_length), not O(subtree_size)

Solution 3: Compressed trie (Patricia trie)
  - Collapse single-child chains: g-o-o-g-l-e → "google"
  - 50%+ memory reduction
```

### Ranking Signals

```
score = α × query_frequency 
      + β × recency_boost 
      + γ × personalization_score
      + δ × trending_bonus

query_frequency: How many times this query was searched
recency_boost: Decay older queries (exponential decay)
personalization: Based on user's search history
trending_bonus: Spike detection → boost rapidly rising queries
```

### Real-Time Trending Updates

```
User searches → Kafka topic → Flink streaming job
  → Sliding window count (last 1 hour)
  → Detect spikes: current_rate / baseline_rate > threshold
  → If trending: inject into trie with bonus score
  → Push updated trie segment to servers

Full trie rebuild: Every 15 minutes (batch)
Hot updates: Every 30 seconds (streaming, trending only)
```

### Client-Side Optimization

```
1. Debounce: Don't send request on every keystroke
   → Wait 100-150ms after last keystroke → then query
   
2. Client-side caching:
   → Cache prefix → results in memory
   → "goo" results cached → "goog" can filter client-side
   
3. Pre-fetch:
   → After showing results for "goo", pre-fetch "goog" in background

4. Cancel in-flight:
   → User types "goo" then quickly "gl"
   → Cancel request for "goo", only use "gl" response
```

### Key Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Data structure | Compressed trie with pre-computed top-K | O(prefix) query, memory efficient |
| Storage | In-memory on each server | < 50ms latency requirement |
| Update | Batch (15min) + streaming (30s for trending) | Freshness vs rebuild cost |
| Client | Debounce + local cache + pre-fetch | Reduce server load, better UX |
| Fallback | Elasticsearch for long-tail queries | Trie only has top queries |

### Scaling Considerations
- **Shard trie by prefix**: Servers A-M on cluster 1, N-Z on cluster 2
- **Replication**: Each shard replicated 3x for availability
- **Geographic**: Regional tries (different trending topics per country)
- **Personalization**: Per-user layer on top of global trie (lightweight)
