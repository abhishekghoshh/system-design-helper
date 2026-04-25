# CAP Theorem

## Blogs and websites


## Medium


## Youtube

- [2. CAP Theorem (Hindi) | High Level Design for Beginners | CAP Partition Tolerance explained](https://www.youtube.com/watch?v=3qRBeZsUa18)
- [CAP Theorem (English Dubbed) | Better with 1.25x playback speed](https://www.youtube.com/watch?v=SckoiQefVEE)

## Theory

### The Immutable Law of Distributed Systems

The CAP Theorem is not a guideline or best practice—it's a **fundamental law of physics** for distributed systems, as immutable as the laws of thermodynamics. Formulated by Eric Brewer in 2000 and proven by Seth Gilbert and Nancy Lynch in 2002, it states an impossible choice:

**In a distributed system, you can guarantee at most TWO of the following three properties simultaneously:**

1. **Consistency (C)**: All nodes see the same data at the same time
2. **Availability (A)**: Every request receives a response (success or failure)
3. **Partition Tolerance (P)**: System continues operating despite network failures

### The Deep Theory: Why CAP is Inevitable

**The Impossibility Proof (Simplified):**

Imagine a distributed database with two nodes, N1 and N2.

**Scenario: Network Partition**
```
N1 (New York)  |  NETWORK PARTITION  |  N2 (London)
   X = 10      |      (no communication)     |    X = 10
```

**User A writes to N1:**
```
N1: X = 20  |  PARTITION  |  N2: X = 10
```

N1 cannot tell N2 about the update. Now User B reads from N2.

**The Impossible Choice:**

**Option 1: Choose Consistency (CP)**
```
N2: "I can't guarantee I have the latest value"
N2: Returns ERROR or TIMEOUT
Result: Not Available (❌ A)
```

**Option 2: Choose Availability (AP)**
```
N2: "I'll return my value: X = 10"
Result: Inconsistent (wrong value!) (❌ C)
```

**Option 3: Choose CA (Ignore partitions)**
```
Assume network never fails
Result: System breaks during partition (❌ P)
```

**The Revelation:**
There is **no fourth option**. Network partitions will happen (hardware fails, cables cut, routers crash). Therefore, P is not optional—you must tolerate partitions. The real choice is **C vs A during a partition**.

### The Three Properties: Deep Dive

#### Consistency (C)

**Formal Definition:**
Linearizability—every read receives the most recent write or an error.

**What It Means:**
```
Write(X = 5) completes at time T
  ⇓
Any Read(X) starting at or after T returns 5
  ⇓
All nodes agree on the value at any given time
```

**The Guarantee:**
- System behaves like a single, atomic unit
- No client ever sees stale data
- Operations appear to happen in a total order

**The Cost:**
- Must coordinate across nodes (slow)
- Blocks during partition (unavailable)
- Limited by speed of light (can't make network faster)

**Example: Banking**
```python
balance = 100
withdraw(50)  # Must coordinate
read_balance()  # Must see 50
```
Wrong balance = overdraft = lost money. Consistency is mandatory.

#### Availability (A)

**Formal Definition:**
Every request receives a response, without guarantee it contains the most recent write.

**What It Means:**
```
Any non-failing node must respond
  ⇓
No timeouts, no errors (except when node truly dead)
  ⇓
System stays up even during partition
```

**The Guarantee:**
- Always get an answer
- Low latency (no waiting for coordination)
- System stays operational during network issues

**The Cost:**
- Might return stale data
- Different nodes might disagree
- Must handle conflicts

**Example: Social Media Feed**
```python
post_tweet("Hello")
read_feed()  # Might not see "Hello" yet
```
Missing a tweet briefly = acceptable. Being down = unacceptable.

#### Partition Tolerance (P)

**Formal Definition:**
System continues operating despite arbitrary message loss between nodes.

**What It Means:**
```
Network can drop/delay any messages
  ⇓
System still functions (maybe degraded)
  ⇓
No assumption of reliable network
```

**The Reality:**
Partitions are not theoretical—they happen:
- Switch failure: 100s of times/year
- Fiber cut: 10s of times/year  
- Datacenter network failure: Multiple times/year
- Cross-datacenter partition: Rare but catastrophic

**The Conclusion:**
Partition tolerance is **not optional** in distributed systems. Networks fail. You must handle it.

### The Real Choice: CP vs AP

Since P is mandatory, you choose between C and A **during a partition**.

#### CP Systems (Consistency over Availability)

**Philosophy**: "Better to be unavailable than wrong."

**Behavior During Partition:**
```
Write request arrives at partitioned node
  ↓
Node: "Can't reach other nodes to coordinate"
  ↓
Returns ERROR (503 Service Unavailable)
  ↓
Client knows operation didn't complete
```

**Characteristics:**
- Sacrifice availability during partition
- Always return correct (or no) answer
- Coordinate writes across majority
- Use consensus protocols (Paxos, Raft)

**Examples:**
- **HBase**: Requires ZooKeeper quorum
- **MongoDB** (with write concern majority): Waits for replica acknowledgment
- **Consul**: Requires consensus for writes
- **etcd**: Raft-based, requires quorum

**When to Choose CP:**
- Financial transactions (can't lose money)
- Inventory systems (can't oversell)
- Booking systems (can't double-book)
- Any system where correctness > uptime

**Real Example: Bank ATM**
```
Partition occurs
  ↓
ATM can't reach central database
  ↓
ATM displays: "Service temporarily unavailable"
  ↓
Better than dispensing cash twice or showing wrong balance
```

#### AP Systems (Availability over Consistency)

**Philosophy**: "Better to be approximately right than unavailable."

**Behavior During Partition:**
```
Write request arrives at partitioned node
  ↓
Node: "Can't reach others, but I'll accept anyway"
  ↓
Returns SUCCESS (202 Accepted)
  ↓
Will sync with others later (eventual consistency)
```

**Characteristics:**
- Always available (as long as any node works)
- Accept temporary inconsistency
- Use conflict resolution (last-write-wins, vector clocks, CRDTs)
- Eventual consistency model

**Examples:**
- **Cassandra**: Multi-master, always writable
- **DynamoDB**: Eventually consistent reads by default
- **Riak**: Anti-entropy for reconciliation
- **CouchDB**: Master-master replication

**When to Choose AP:**
- Social media (stale likes tolerable)
- Shopping cart (brief inconsistency OK)
- Analytics (approximate counts fine)
- Any system where uptime > perfect accuracy

**Real Example: Shopping Cart**
```
Partition occurs
  ↓
User adds item to cart
  ↓
Local node accepts: "Added to cart"
  ↓
Items might appear differently on different nodes briefly
  ↓
Eventually syncs (user doesn't notice)
```

### CA Systems: The Myth

**Traditional RDBMS (Single Node):**
- **C**: Strong ACID guarantees
- **A**: Always responds (if node is up)
- **P**: Not tolerant (there's only one node)

**The Truth:**
CA systems are **not distributed**. They're single nodes. The moment you add a second node, you must choose CP or AP.

**CA Distributed Systems Don't Exist in Real Networks:**
If you try to build one, any partition breaks it entirely.

### The Spectrum: It's Not Binary

Real systems don't make a hard choice—they offer **tunable consistency**.

#### Cassandra: The Exemplar

**Tunable Consistency Levels:**

**Write Consistency:**
```
ANY:  Success if any node acknowledges (even hinted handoff)
ONE:  Success if one replica acknowledges (AP)
QUORUM: Success if majority acknowledges (CP)
ALL:  Success if all replicas acknowledge (CP, slower)
```

**Read Consistency:**
```
ONE:  Return from first replica (fast, might be stale)
QUORUM: Read from majority, return newest (slower, consistent)
ALL:  Read from all replicas (slowest, most consistent)
```

**The Magic Formula:**
```
If (Write_Replicas + Read_Replicas) > Replication_Factor:
    Guaranteed to see latest write (Strong Consistency)

Example:
Replication = 3
Write = QUORUM (2)
Read = QUORUM (2)
2 + 2 > 3 ✓ (overlap guaranteed)
```

**Per-Request Tunability:**
```python
# Strong consistency (CP behavior)
session.execute(query, consistency_level=QUORUM)

# High availability (AP behavior)
session.execute(query, consistency_level=ONE)
```

**The Power:**
Choose C vs A **per request**:
- User login: QUORUM (security-critical)
- View post: ONE (speed matters)
- Write post: QUORUM (data important)
- Page view count: ONE (approximate OK)

### PACELC: The CAP Extension

**CAP Only Discusses Partitions. What About Normal Operation?**

PACELC Theorem (Daniel Abadi, 2012):
```
If Partition:
    Choose between Availability and Consistency
Else (no partition):
    Choose between Latency and Consistency
```

**The Addition:**
Even without partitions, there's a trade-off:
- **High Consistency**: Coordinate across nodes (higher latency)
- **Low Latency**: Don't coordinate (eventual consistency)

**System Classification:**
- **PA/EL**: Available during partition, Low latency normally (Cassandra, DynamoDB)
- **PA/EC**: Available during partition, Consistent normally (???—rare)
- **PC/EL**: Consistent during partition, Low latency normally (???—rare)  
- **PC/EC**: Consistent during partition, Consistent normally (Traditional DBs)

### Real-World Examples: Who Chose What?

**Google Spanner (PC/EC):**
- CP during partitions
- Strong consistency always
- Uses atomic clocks for global time
- **Trade-off**: High latency (10-100ms), complex infrastructure

**Amazon DynamoDB (PA/EL):**
- AP during partitions  
- Eventually consistent reads by default
- **Trade-off**: Can read stale data, simpler, faster

**MongoDB (PC/EC with tuning):**
- CP during partitions (write concern = majority)
- Can tune to AP (write concern = 1)
- **Trade-off**: Flexible but requires understanding

**Cassandra (PA/EL with tuning):**
- AP by default
- Can achieve CP with QUORUM reads/writes
- **Trade-off**: Maximum flexibility, maximum complexity

### The Wisdom: How to Choose

**Ask These Questions:**

1. **What happens if I show stale data?**
   - Lost money? → CP
   - User confusion? → AP

2. **What happens if system is down?**
   - Lost sales? → AP
   - Wrong transaction? → CP

3. **Can I handle conflicts?**
   - Yes (last write wins, CRDTs) → AP
   - No (needs coordination) → CP

4. **What's more expensive: downtime or incorrectness?**
   - Downtime → AP
   - Incorrectness → CP

**Domain Examples:**

| Domain | Choice | Reason |
|--------|--------|--------|
| Banking | CP | Money can't be wrong |
| Social Media | AP | Brief staleness OK |
| E-commerce | AP | Cart inconsistency tolerable |
| Inventory | CP | Can't oversell |
| Analytics | AP | Approximate counts fine |
| DNS | AP | Eventual consistency acceptable |
| Booking | CP | No double-bookings |
| Likes/Views | AP | Exact count not critical |

**The Modern Approach: Hybrid**

Don't choose system-wide. Choose per-data-type:
```python
# Strong consistency for critical data
db.users.update(query, write_concern="majority")

# Eventual consistency for less critical
db.page_views.insert(data, write_concern="acknowledged")
```

### The Fundamental Insight

CAP is not about databases or technologies—it's about **the nature of distributed systems**. It's a consequence of:
- The finite speed of light
- The impossibility of perfectly reliable networks  
- The fundamental trade-off between coordination and independence

You can't engineer around CAP. You can only make informed choices about which trade-offs suit your use case.

**The Meta-Lesson:**
*"In distributed systems, you can't have everything. Understanding what you can sacrifice is the key to good design."*

### PACELC Theorem

Extension of CAP:
- **If Partition**: Choose between Availability and Consistency
- **Else**: Choose between Latency and Consistency

---

### CAP Theorm

### *Introduction:*

- Discusses the concept of CAP Theorem (Consistency, Availability, Partition Tolerance) and its relevance in distributed systems.
- Emphasizes the importance of considering CAP constraints early in system design to avoid costly changes later.

### *CAP Theorem:*

- *CAP:* Stands for Consistency, Availability, Partition Tolerance.
- *Desired Properties of Distributed Systems:* These three properties are desirable in a distributed system.
- *CAP Trade-off:* You cannot have all three properties simultaneously. You must choose two out of the three.
- *Example:*
    - Consider a distributed database with nodes in India and the US.
    - A user's data is replicated across both locations.
    - A distributed system should ideally be consistent (same data everywhere), available (responding to requests), and tolerant to partitions (network disruptions).

### *Understanding Each Property:*

- *Consistency:* Ensures that all nodes have the same, up-to-date data at any given time.
- *Availability:* Guarantees that every request is successfully processed by at least one node.
- *Partition Tolerance:* Allows the system to continue functioning even if communication between nodes is disrupted.

### *Why CAP Properties Cannot Co-Exist:*

- *Case 1: CA (Consistency and Availability) - Not possible with Partition Tolerance*
    - *Scenario:* A partition occurs, separating nodes A and B.
    - *Conflict:* Node A writes updated data, but node B cannot access it due to the partition.
    - *Result:* Inconsistency between nodes.
- *Case 2: CP (Consistency and Partition Tolerance) - Not possible with Availability*
    - *Scenario:* A partition occurs, separating nodes A and B.
    - *Strategy:* To maintain consistency, only one node (A) is allowed to process writes.
    - *Result:* Node B becomes unavailable for writes during the partition.
- *Case 3: AP (Availability and Partition Tolerance) - Not possible with Consistency*
    - *Scenario:* A partition occurs, separating nodes A and B.
    - *Strategy:* To maintain availability, both nodes can process writes.
    - *Result:* Potential for inconsistent data between nodes.

### *CAP Trade-off in Real-world Systems:*

- *Importance of Partition Tolerance:* In today's distributed systems, network disruptions are common.
- *Choosing between CP and AP:*
    - *CP:* Choose this option for systems where consistency is critical, even if it means some temporary downtime.
    - *AP:* Choose this option for systems where availability is paramount, even if it means some data inconsistency.

### *Key Takeaways:*

- *Understanding CAP is crucial for effective distributed system design.*
- *Early consideration of CAP constraints can prevent costly changes later.*
- *The choice between CP and AP depends on the specific needs of your system.*
- *Partition tolerance is a key factor in modern distributed systems.*
