# Consistency

## Theory

In distributed systems, **consistency** refers to whether all nodes in the system see the same data at the same time. It's one of the most important (and most misunderstood) concepts in system design.

**The Core Problem:**
When data is replicated across multiple servers (for availability and performance), writes happen on one node first and must propagate to others. The question is: *how quickly must all nodes agree?*

```
Write: "user.name = Alice" → Node A (primary)
                              ↓ replication
                        Node B (replica) → still sees "Bob" for a brief moment

Strong Consistency:  Node B blocks reads until it has "Alice"
Eventual Consistency: Node B returns "Bob" now, "Alice" later (after replication)
```

**Why It Matters:**
- **Bank balance**: You must see the correct balance after a transfer → strong consistency
- **Social media likes**: Seeing 999 vs 1000 for a few seconds is fine → eventual consistency
- **Inventory count**: Can't oversell → strong consistency
- **News feed order**: Slightly stale is OK → eventual consistency

**The Trade-off (CAP / PACELC):**
You can't have perfect consistency AND perfect availability in a distributed system. Stronger consistency = higher latency and lower availability during network issues.

**Consistency Models Spectrum:**
```
Strongest ←————————————————————————————————→ Weakest

Linearizable → Sequential → Causal → Eventual
  (safest)                              (fastest)
```

- **Linearizable**: All operations appear instantaneous and ordered. Most expensive.
- **Sequential**: All nodes see operations in the same order (but not necessarily real-time).
- **Causal**: Causally related operations are seen in order; concurrent operations may differ.
- **Eventual**: Given enough time, all replicas converge. No ordering guarantees during propagation.

---

## Quick Reference

**Strong Consistency:**
- Read returns most recent write
- All nodes see same data at same time
- Higher latency
- Example: SQL databases

**Eventual Consistency:**
- System becomes consistent over time
- Temporary inconsistency allowed
- Lower latency, higher availability
- Example: DynamoDB, Cassandra

**Consistency Levels (Cassandra example):**
- ONE: Any single node
- QUORUM: Majority of nodes
- ALL: All nodes
