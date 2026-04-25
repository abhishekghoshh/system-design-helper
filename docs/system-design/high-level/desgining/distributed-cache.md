# Design Distributed Cache

## Blogs and websites


## Medium


## Youtube


## Theory

### Problem Statement
Design a distributed caching system like Redis or Memcached that provides low-latency key-value storage across multiple nodes with high availability and consistency.

### Functional Requirements
- GET / SET / DELETE operations on key-value pairs
- TTL (time-to-live) expiration
- Support multiple data types (string, list, set, hash, sorted set)
- Pub/Sub messaging
- Atomic operations (INCR, DECR, CAS)
- Cache eviction policies (LRU, LFU, TTL)

### Non-Functional Requirements
- **Latency**: < 1ms for single-node, < 5ms for distributed
- **Throughput**: 100K+ operations/second per node
- **Availability**: 99.99%
- **Scalability**: Horizontal scaling to petabytes
- **Durability**: Optional persistence (AOF, RDB snapshots)

### High-Level Architecture

```
┌──────────┐     ┌──────────────────────────────────────┐
│  Client  │────▶│         Cache Proxy / Router          │
│  (App)   │     │  (Consistent hashing for routing)     │
└──────────┘     └───────────────┬──────────────────────┘
                                 │
                 ┌───────────────┼───────────────┐
                 ▼               ▼               ▼
          ┌────────────┐  ┌────────────┐  ┌────────────┐
          │  Cache     │  │  Cache     │  │  Cache     │
          │  Node 1    │  │  Node 2    │  │  Node 3    │
          │  (Primary) │  │  (Primary) │  │  (Primary) │
          │     │      │  │     │      │  │     │      │
          │     ▼      │  │     ▼      │  │     ▼      │
          │  Replica   │  │  Replica   │  │  Replica   │
          └────────────┘  └────────────┘  └────────────┘
```

### Data Partitioning

**Consistent Hashing:**
```
hash(key) → position on hash ring → find next node clockwise

Virtual nodes: Each physical node = 100-200 virtual nodes
  → Even distribution
  → Minimal rebalancing when nodes join/leave
```

**Key routing:**
```
Client library computes: node = hash(key) % N
  or
Proxy layer routes request to correct shard
```

### Cache Eviction Policies

```
LRU (Least Recently Used):
  Doubly-linked list + HashMap
  - Access: move to head → O(1)
  - Evict: remove tail → O(1)

LFU (Least Frequently Used):
  Frequency counter + min-heap
  - Better for hot/cold data
  - More complex

TTL (Time-To-Live):
  Lazy expiration: check on access
  Active expiration: periodic scan of expiring keys (10% sample)
```

### Replication Strategies

```
1. Leader-Follower (Redis default):
   Write → Primary → async replicate → Replicas
   Read → Any replica (read scaling)
   Failover: Sentinel promotes replica to primary

2. Leaderless (Memcached style):
   No replication — data on single node
   Lost on node failure
   Simple, fast, used when cache-miss is acceptable
```

### Write-Through vs Write-Behind

```
Write-Through:
  App → Cache → DB (synchronous)
  Pro: Cache always consistent
  Con: Higher write latency

Write-Behind (Write-Back):
  App → Cache → (async) → DB
  Pro: Low write latency
  Con: Data loss risk if cache fails before DB write

Cache-Aside (most common):
  Read: App checks cache → miss → read DB → populate cache
  Write: App writes DB → invalidate cache
```

### Handling Failures

| Failure | Solution |
|---------|----------|
| Node crash | Failover to replica (Sentinel/Cluster) |
| Network partition | Split-brain protection (quorum-based) |
| Hot key | Local cache + key replication to multiple nodes |
| Thundering herd | Request coalescing / cache stampede lock |

### Key Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Partitioning | Consistent hashing | Minimal rebalancing |
| Replication | Async leader-follower | Low write latency |
| Eviction | LRU (default) | Simple, effective |
| Persistence | Optional AOF + RDB | Durability when needed |
| Protocol | RESP (Redis protocol) | Simple, fast text protocol |
