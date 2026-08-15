# Design Distributed Locking Service

## Blogs and websites

## Medium

## Youtube

## Theory

### Problem Statement
Design a distributed locking service that provides mutual exclusion across distributed systems, ensuring only one process can access a shared resource at a time — even across multiple servers and data centers.

### Functional Requirements
- Acquire a lock on a named resource
- Release a lock
- Lock with TTL (auto-expire to prevent deadlocks)
- Try-lock (non-blocking attempt)
- Lock renewal (extend TTL while holding)
- Fencing tokens (monotonically increasing tokens to detect stale locks)

### Non-Functional Requirements
- **Safety**: At most one client holds a lock at any time (mutual exclusion)
- **Liveness**: Locks are eventually released (no deadlocks)
- **Fault tolerance**: Survives individual node failures
- **Latency**: Lock acquire/release < 10ms
- **Scale**: Millions of locks, thousands of lock operations/sec

### Why Distributed Locking is Hard

```
Scenario: Leader election with a lock

Process A acquires lock → becomes leader
Process A: long GC pause (30 seconds)
Lock expires (TTL)
Process B acquires lock → becomes leader
Process A wakes up → thinks it's still leader
→ TWO leaders = data corruption

This is the "split-brain" problem. 
Fencing tokens solve this (see below).
```

### Approach 1: Redis-Based (Redlock)

```
Single Redis instance:
  ACQUIRE: SET resource_name my_token NX PX 30000
    NX = only if not exists
    PX = TTL in milliseconds
    my_token = unique per client (UUID)
  
  RELEASE: Lua script
    if redis.call("get", key) == my_token then
      redis.call("del", key)
    end
    → Only release your own lock (compare token)

Problem: Single point of failure

Redlock (multi-node):
  1. Try to acquire lock on N independent Redis nodes (N=5)
  2. If acquired on majority (≥3), lock is held
  3. Lock validity = TTL - time_spent_acquiring
  4. If failed, release on all nodes

Criticism (Martin Kleppmann):
  - Clock drift can violate safety
  - Process pauses can cause split-brain
  - Not suitable for correctness-critical systems
```

### Approach 2: ZooKeeper-Based

```
Uses ZooKeeper's sequential ephemeral nodes:

1. Client creates ephemeral sequential node:
   /locks/resource-1/lock-000000001

2. Client reads all children of /locks/resource-1/
   → If my node is the smallest → I hold the lock

3. Otherwise, watch the node just before mine
   → When it's deleted → check again

4. On client crash → ephemeral node auto-deleted → lock released

Advantages:
  - No TTL needed (ephemeral = session-based)
  - Total ordering via sequential nodes
  - Consensus-based (ZAB protocol) → strong guarantees
  
Disadvantages:
  - Higher latency than Redis (~10-50ms)
  - Session timeout can cause false lock release
```

### Approach 3: etcd-Based

```
Uses etcd's lease mechanism:

  1. Create a lease: etcdctl lease grant 30 → lease_id
  2. Put key with lease: etcdctl put /lock/resource-1 "holder-A" --lease=lease_id
     → Key exists only while lease is alive
  3. Compete: Use etcd transactions (compare-and-swap)
     → If key doesn't exist → put (acquire)
     → If key exists → watch for deletion
  4. Keep-alive: Client sends heartbeats to renew lease
  5. On crash: Lease expires → key deleted → lock released

etcd uses Raft consensus → strong consistency
  → True mutual exclusion (no split-brain from clock drift)
```

### Fencing Tokens

```
Problem: Stale lock holders can corrupt data

Solution: Monotonically increasing fencing token

Lock Service:
  Lock acquired → return token = 34
  Lock expires, re-acquired → return token = 35

Resource (e.g., database):
  Tracks highest token seen
  Request with token 34 arrives AFTER token 35
  → Reject (stale lock holder)

Implementation:
  ZooKeeper: use znode version (czxid)
  etcd: use revision number
  Redis: use a counter key incremented on each lock grant
```

### Architecture

```
┌──────────┐                    ┌─────────────────────────┐
│ Service A │──acquire lock────▶│   Lock Service           │
│           │◀──token: 42──────│                          │
└─────┬─────┘                   │  Backend options:        │
      │                         │   - Redis (Redlock)      │
      │ write with token=42     │   - ZooKeeper            │
      ▼                         │   - etcd                 │
┌──────────┐                    └─────────────────────────┘
│ Database │
│ (checks  │
│  token)  │
└──────────┘
```

### Comparison

| Feature | Redis (Redlock) | ZooKeeper | etcd |
|---------|----------------|-----------|------|
| Latency | ~1-5ms | ~10-50ms | ~5-20ms |
| Safety | Weak (clock-dependent) | Strong (consensus) | Strong (consensus) |
| Liveness | TTL-based | Session-based (ephemeral) | Lease-based |
| Complexity | Simple | Moderate | Moderate |
| Use case | Performance-critical, best-effort | Correctness-critical | Kubernetes ecosystem |

### Key Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Backend | etcd for correctness, Redis for speed | Match safety needs to use case |
| Deadlock prevention | TTL / lease expiration | Crashed clients don't hold locks forever |
| Stale lock protection | Fencing tokens | Prevent data corruption from paused clients |
| Lock granularity | Named resources (/lock/{resource}) | Fine-grained locking |
| Availability | 3-5 node cluster with consensus | Survive minority failures |
