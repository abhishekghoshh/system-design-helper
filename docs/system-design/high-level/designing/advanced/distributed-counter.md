# Design Distributed Counter

## Blogs and websites

## Medium

## Youtube

## Theory

### Problem Statement
Design a distributed counter system that can accurately count events (likes, views, clicks) at massive scale with high throughput and acceptable consistency trade-offs.

### Functional Requirements
- Increment/decrement a counter by any value
- Read current counter value
- Support millions of distinct counters (per-post likes, per-video views)
- Reset counter
- Get counter value within a time window

### Non-Functional Requirements
- **Throughput**: 1M+ increments/second per counter (viral content)
- **Latency**: Write < 5ms, Read < 10ms
- **Consistency**: Eventually consistent (reads may lag by a few seconds)
- **Durability**: No permanent count loss
- **Scale**: Billions of counters

### The Problem with Naive Counting

```
Simple approach: UPDATE counters SET value = value + 1 WHERE id = X

Problem at scale:
  - Single row = single lock = bottleneck
  - 1M writes/sec to same row → massive contention
  - Database becomes the bottleneck
```

### Solution: Sharded Counters

```
Instead of 1 counter → N sub-counters (shards)

Counter "post:123:likes" → 
  shard_0: 1,234
  shard_1: 1,189
  shard_2: 1,301
  ...
  shard_N: 1,276

Write: increment random shard → no contention
Read:  SUM(all shards) → total count

Shard count adapts to write rate:
  Low traffic:  1 shard
  High traffic: 100+ shards (auto-scale)
```

### Architecture

```
┌──────────┐     ┌──────────┐     ┌──────────────────────┐
│  Client  │────▶│  API GW  │────▶│  Counter Service      │
└──────────┘     └──────────┘     │                       │
                                  │  ┌─────────────────┐  │
                                  │  │ Write Path:      │  │
                                  │  │  hash(request)   │  │
                                  │  │  → pick shard    │  │
                                  │  │  → increment     │  │
                                  │  ├─────────────────┤  │
                                  │  │ Read Path:       │  │
                                  │  │  sum all shards  │  │
                                  │  │  or read cache   │  │
                                  │  └────────┬────────┘  │
                                  └───────────┼───────────┘
                                              │
                                  ┌───────────┼───────────┐
                                  ▼                       ▼
                           ┌────────────┐         ┌────────────┐
                           │  Redis     │         │  Database  │
                           │  (shards)  │         │  (durable) │
                           └────────────┘         └────────────┘
```

### Write-Optimized Approaches

**1. In-Memory Buffering:**
```
Client → Buffer in local memory → Batch flush every N seconds → DB
  Pro: Extremely fast writes
  Con: Risk of count loss on crash
```

**2. Redis INCR (per-shard):**
```
INCR counter:post:123:shard:7
  → Atomic, O(1), in-memory
  → Periodic persistence to DB
```

**3. Kafka + Stream Processing:**
```
Events → Kafka → Flink/Spark → Aggregate → Write to DB
  → Handles burst traffic
  → Exactly-once with Kafka transactions
```

### Read Path Optimization

```
Problem: SUM across 100 shards is expensive if done per request

Solution: Materialized view / Read cache
  - Background job aggregates shards every 1-5 seconds
  - Writes aggregated total to a read-optimized cache
  - Reads hit the cache → O(1)
  - Display: "1.2M likes" (approximate, not exact)
```

### Consistency Trade-offs

| Approach | Consistency | Throughput | Use Case |
|----------|-------------|------------|----------|
| Single counter (DB) | Strong | Low | Financial transactions |
| Sharded counter | Eventual (~seconds) | Very High | Likes, views |
| Buffered + batch | Eventual (~minutes) | Extreme | Analytics counters |

### Key Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Write path | Sharded Redis counters | High throughput, low latency |
| Read path | Periodically aggregated cache | Fast reads, acceptable lag |
| Persistence | Async flush to PostgreSQL | Durability without write penalty |
| Shard count | Auto-scale based on write rate | Adapt to traffic patterns |
| Display | Approximate ("1.2M") for large counts | Users don't need exact numbers |
