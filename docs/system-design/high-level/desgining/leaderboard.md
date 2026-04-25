# Design Leaderboard

## Blogs and websites


## Medium


## Youtube


## Theory

### Problem Statement
Design a real-time leaderboard system that ranks millions of players/users by score with support for real-time updates, rank queries, and historical leaderboards.

### Functional Requirements
- Submit/update user scores
- Get global top-K leaderboard (top 10, top 100)
- Get a user's rank and nearby players
- Support multiple leaderboards (daily, weekly, all-time)
- Real-time rank updates
- Historical leaderboard snapshots

### Non-Functional Requirements
- **Latency**: Rank query < 10ms, score update < 50ms
- **Scale**: 100M+ users, 10K+ score updates/second
- **Consistency**: Near real-time (< 1 second lag)
- **Availability**: 99.99%

### High-Level Architecture

```
┌──────────┐     ┌──────────┐     ┌────────────────────────┐
│  Client  │────▶│  API GW  │────▶│  Leaderboard Service   │
└──────────┘     └──────────┘     │                        │
                                  │  ┌──────────────────┐  │
                                  │  │ Score Ingestion   │  │
                                  │  │ Rank Calculator   │  │
                                  │  │ Query Handler     │  │
                                  │  └────────┬─────────┘  │
                                  └───────────┼────────────┘
                                              │
                                  ┌───────────┼───────────┐
                                  ▼                       ▼
                           ┌────────────┐         ┌────────────┐
                           │  Redis     │         │  Database  │
                           │  Sorted    │         │  (persist) │
                           │  Sets      │         └────────────┘
                           └────────────┘
```

### Redis Sorted Set Approach

```
ZADD leaderboard <score> <user_id>       → O(log N) - add/update
ZREVRANK leaderboard <user_id>           → O(log N) - get rank
ZREVRANGE leaderboard 0 9 WITHSCORES    → O(log N + K) - top 10
ZREVRANGE leaderboard rank-5 rank+5     → O(log N + K) - nearby
ZCARD leaderboard                        → O(1) - total users
```

**Why Redis Sorted Sets?**
- Skip list internally → O(log N) for all operations
- Single data structure handles ranking natively
- In-memory → sub-millisecond latency
- Atomic operations → thread-safe score updates

### Multiple Leaderboards

```
Keys:
  leaderboard:global          → all-time scores
  leaderboard:daily:2026-04-25 → daily leaderboard
  leaderboard:weekly:2026-W17  → weekly leaderboard

Daily reset:
  - Create new key each day
  - TTL on old keys (auto-cleanup)
  - Snapshot to DB before expiry (historical)
```

### Scaling Beyond Single Redis

For 100M+ users where one Redis can't hold all data:

```
Option 1: Sharded Redis
  Shard by user_id hash
  Problem: Cross-shard ranking is hard

Option 2: Bucket-based ranking
  Divide score range into buckets
  Each bucket tracks count of users
  Rank = sum of users in higher buckets + position within bucket

Option 3: Approximate ranking
  Use HyperLogLog or Count-Min Sketch for approximate counts
  Acceptable for "You are approximately ranked #1,234,567"
```

### Handling Ties

```
Same score → tiebreaker by timestamp (earlier wins)

Redis: Use composite score
  score = actual_score * 10^10 + (MAX_TIMESTAMP - timestamp)
  → Higher score wins, earlier timestamp wins on tie
```

### Key Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Primary store | Redis Sorted Sets | O(log N) rank queries, in-memory speed |
| Persistence | Redis + PostgreSQL backup | Speed + durability |
| Multiple boards | Separate keys with TTL | Clean separation, auto-cleanup |
| Sharding (at scale) | Bucket-based approach | Enables cross-shard ranking |
| Tie-breaking | Composite score with timestamp | Deterministic ordering |
