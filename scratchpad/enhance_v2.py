#!/usr/bin/env python3
"""
Enhance advanced system design docs by adding missing canonical sections.
Uses regular strings with __VAR__ placeholders to avoid f-string brace issues.
"""

import os
import re

ADVANCED_DIR = "/Users/abhishekghosh/Desktop/projects/personal/system-design-helper/docs/system-design/high-level/designing/advanced"

# ---- System-specific data ----

SYSTEMS = {
    'multi-region-deployment-system.md': {
        'name': 'Multi-Region Deployment System',
        'brief': 'Routes user traffic and data to home regions based on data residency laws (GDPR, DPDP), using GeoDNS, edge routing, and a global index for non-restricted data',
        'key_components': ['GeoDNS', 'Edge Router', 'Regional Stack (App + DB + Cache)', 'Global Index (non-restricted data only)'],
        'main_challenge': 'Balancing data residency compliance (restricted data must never leave its jurisdiction) with global availability (users need low-latency access to their data)',
        'restricted': 'PII, messages, documents, financial data',
        'non_restricted': 'public profiles, product catalogs, search indexes',
        'real_world': ['AWS Global Accelerator', 'Cloudflare D1', 'Google Cloud Spanner', 'Fastly Compute@Edge'],
        'java_focus': 'region-based access control and encryption key selection',
    },
    'log-system.md': {
        'name': 'Log System',
        'brief': 'A centralized logging system that collects, indexes, and provides search/analytics over application logs from microservices, with tiered storage (hot/warm/cold) and WAL for durability',
        'key_components': ['Log Agents (Vector/Fluentd)', 'Log Indexer (Elasticsearch)', 'Ingestion Queue (Kafka)', 'Storage (hot warm cold tiers)'],
        'main_challenge': 'Handling millions of log lines per second with sub-second search latency while keeping PII secure and storage costs manageable',
        'restricted': 'PII in log lines, stack traces with user data',
        'non_restricted': 'application metrics, service logs, anonymized traces',
        'real_world': ['Elastic Stack (Filebeat, Logstash, Elasticsearch, Kibana)', 'Datadog', 'Grafana Loki', 'AWS CloudWatch Logs'],
        'java_focus': 'log shipping and search APIs',
    },
    'recomendation-engine.md': {
        'name': 'Recommendation Engine',
        'brief': 'A two-stage recommendation engine that combines candidate generation (neural retrieval) with ranking (matrix factorization), serving personalized results for video and e-commerce with low-latency inference',
        'key_components': ['Candidate Generator (two-tower NN)', 'Ranking Model (MF/SVD)', 'Feature Store', 'Model Serving (MLflow/Triton)', 'User/Item Embeddings'],
        'main_challenge': 'Serving sub-100ms recommendations for millions of users while keeping models fresh and handling cold-start users/items',
        'restricted': 'user preferences, viewing history, purchase history',
        'non_restricted': 'public item metadata, aggregate trends, anonymized stats',
        'real_world': ['Netflix (Metaflow, MetaREC)', 'YouTube (Two-tower DLRM)', 'Spotify (Luigi + Matrix Factorization)', 'Airbnb (Spark MLlib)'],
        'java_focus': 'feature extraction and recommendation API',
    },
    'real-time-bidding-auction-system.md': {
        'name': 'Real-Time Bidding Auction System',
        'brief': 'A real-time ad exchange that runs sealed-bid second-price auctions with <10ms latency across millions of concurrent auctions, connecting DSPs, SSPs, and advertisers',
        'key_components': ['Bidder (DSP adapter)', 'Auction Server', 'Ad Exchange', 'Bid Cache', 'Winner Notification Service'],
        'main_challenge': 'Making auction decisions in under 10ms while processing bid requests from multiple ad exchanges and handling bidder timeouts',
        'restricted': 'user profiles, bidding histories, advertiser budgets',
        'non_restricted': 'public ad creative metadata, campaign stats, anonymized win rates',
        'real_world': ['Google AdX', 'OpenX', 'The Trade Desk', 'Amazon Publisher Services'],
        'java_focus': 'bid request processing and auction logic',
    },
    'quick-commerce-inventory-system.md': {
        'name': 'Quick-Commerce Inventory System',
        'brief': 'An inventory management system for 10-minute delivery that manages stock levels across dark stores/warehouses, with cache-aside reservation and TTL-based expiration for abandoned reservations',
        'key_components': ['Inventory DB (Postgres)', 'Cache (Redis)', 'Reservation Engine', 'Dark Store Cluster', 'Delivery Orchestration'],
        'main_challenge': 'Maintaining accurate stock levels during flash sales with high concurrent reservation rates, handling overbooking while keeping cache and DB consistent',
        'restricted': 'customer orders, payment info, delivery addresses',
        'non_restricted': 'product catalog, stock counts, public inventory levels',
        'real_world': ['Blinkit (Zomato)', 'Zepto', 'Swiggy Instamart', 'Amazon Fresh'],
        'java_focus': 'reservation service and cache management',
    },
    'stock-broker-system.md': {
        'name': 'Stock Broker System',
        'brief': 'A stock trading platform that matches buy/sell orders using price-time priority, with risk checks, market data streaming, and compliance auditing for regulatory oversight',
        'key_components': ['Order Book', 'Matching Engine', 'Risk Check Service', 'Market Data Feed', 'Audit Log', 'Settlement Engine'],
        'main_challenge': 'Processing millions of orders per second with microsecond latency while maintaining strict price-time priority ordering and preventing risk violations',
        'restricted': 'trading accounts, transaction history, PII',
        'non_restricted': 'public market prices, aggregate volumes, company fundamentals',
        'real_world': ['Robinhood', 'Interactive Brokers', 'Zerodha', 'Charles Schwab (Intelligent Portfolios)'],
        'java_focus': 'order placement and risk checking',
    },
    'live-comments.md': {
        'name': 'Live Comments System',
        'brief': 'A real-time commenting system for live video streams that uses fan-out on write with targeted pub/sub, handling millions of concurrent viewers with message deduplication and ordering',
        'key_components': ['WS Server Cluster', 'Message Broker (Kafka/RabbitMQ)', 'Pub/Sub System', 'Message Store', 'Cache Layer', 'Ordering Service'],
        'main_challenge': 'Delivering comments to millions of concurrent viewers with <500ms latency while maintaining ordering, deduplication, and handling viewer churn',
        'restricted': 'user messages, PII in comments',
        'non_restricted': 'public comments, aggregate stats, emoji reactions',
        'real_world': ['Facebook Live Comments', 'Twitch Chat', 'YouTube Live Chat', 'Twitter Spaces'],
        'java_focus': 'WebSocket message publishing and subscription',
    },
    'settlement-reconciliation-system.md': {
        'name': 'Settlement and Reconciliation System',
        'brief': 'A financial system that settles transactions across payment providers daily, reconciles three-way (internal ledger, provider, external bank), and handles idempotent payouts with full audit trails',
        'key_components': ['Ledger (transaction records)', 'Settlement Engine', 'Reconciliation Engine', 'Payout Service', 'Audit Trail'],
        'main_challenge': 'Reconciling millions of transactions across multiple providers daily, handling partial settlements, and ensuring no double-payments or missed payouts',
        'restricted': 'transaction data, account numbers, PII, settlement amounts',
        'non_restricted': 'aggregate settlement reports, public transaction counts',
        'real_world': ['Stripe Radar', 'PayPal Risk', 'Adyen Settlement', 'Razorpay'],
        'java_focus': 'settlement calculation and idempotency',
    },
    'live-streaming.md': {
        'name': 'Live Streaming System',
        'brief': 'A live video streaming platform that ingests RTMP/HLS streams, transcodes to multiple bitrates, segments into HLS chunks, and distributes via CDN for low-latency global delivery',
        'key_components': ['Ingest Server (RTMP)', 'Transcoder (FFmpeg)', 'Segmenter (HLS)', 'Origin Server', 'CDN', 'Player SDK'],
        'main_challenge': 'Achieving sub-3-second latency at global scale while handling variable network conditions, supporting multiple bitrates, and minimizing compute costs for transcoding',
        'restricted': 'viewer data, chat messages, content takedown requests',
        'non_restricted': 'public stream metadata, aggregate view counts, system metrics',
        'real_world': ['Twitch', 'YouTube Live', 'Facebook Live', 'AWS IVS'],
        'java_focus': 'stream metadata and segment retrieval APIs',
    },
    'multiplayer-game.md': {
        'name': 'Multiplayer Game System',
        'brief': 'A real-time multiplayer game server using WebSocket connections with client-side prediction, server reconciliation, and entity interpolation to deliver sub-100ms gameplay for competitive matches',
        'key_components': ['Game Server (authoritative)', 'Matchmaker', 'Client Prediction Library', 'State Sync Engine', 'Lobby Service', 'Anti-Cheat'],
        'main_challenge': 'Maintaining consistent game state across clients with high latency, handling player join/leave mid-match, and scaling servers to 100+ players per match',
        'restricted': 'player PII, match state, gameplay data',
        'non_restricted': 'public player stats, leaderboard, match metadata',
        'real_world': ['Riot Games (Valorant)', 'Epic Games (Unreal Engine)', 'Unity (Netcode for GameObjects)', ' Blizzard (Overwatch 2)'],
        'java_focus': 'network message handling and state synchronization',
    },
}


# ---- Section generators (regular strings with __VAR__ placeholders) ----

def gen_topics_covered(filepath):
    """Extract all ### headings and generate Topics Covered list."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    headings = []
    for line in content.splitlines():
        m = re.match(r'^###\s+(.+)', line)
        if m:
            text = m.group(1).strip()
            if text.lower() != 'topics covered':
                headings.append(text)

    def slugify(text):
        slug = text.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        slug = re.sub(r'-+', '-', slug).strip('-')
        return slug

    lines = []
    for i, h in enumerate(headings, 1):
        lines.append(f"1. [{h}](#{slugify(h)})") if False else lines.append(f"{i}. [{h}](#{slugify(h)})")
    # Fix: use proper numbering
    lines = []
    for i, h in enumerate(headings, 1):
        lines.append(f"{i}. [{h}](#{slugify(h)})")
    return "\n".join(lines)


def gen_replication_strategies(s):
    name = s['name']
    return f"""### Replication Strategies

**What it means**

Replication Strategies determine how data and state are copied across multiple nodes in {name}. The choice of strategy determines the trade-off between consistency, availability, and latency.

**Why it matters**

{name} must replicate data to prevent loss and serve reads from multiple nodes. The replication strategy determines whether the system favors consistency (strong reads) or availability (always writable), and how it handles cross-node failure.

**How it works**

**Leader-based (single-leader)**: A single primary node accepts all writes; followers replicate changes asynchronously or semi-synchronously. Reads can be served from any replica. This strategy favors strong consistency for writes but creates a write bottleneck at the leader.

```mermaid
flowchart LR
    subgraph "Primary Node"
        Leader[Leader/Follower<br/>Accepts writes]
    end
    subgraph "Replica Nodes"
        Follower1[Follower 1<br/>Read-only]
        Follower2[Follower 2<br/>Read-only]
        Follower3[Follower 3<br/>Read-only]
    end
    Client[Client] -->|Write| Leader
    Client -->|Read| Follower1
    Client -->|Read| Follower2
    Leader -->|Replicate| Follower1
    Leader -->|Replicate| Follower2
    Leader -->|Replicate| Follower3
```

*Leader-based replication: a single primary node accepts all writes and replicates them to read-only followers. Clients can read from any replica for scaled read throughput, but all writes go through the leader.*

**Multi-leader (multi-master)**: Multiple nodes accept writes and exchange updates with each other. This enables low-latency writes in different regions but requires conflict resolution (last-write-wins, merge functions, or CRDTs).

**Leaderless (quorum-based)**: Any node can accept writes; a quorum of nodes must agree. Read and write quorums are configured so that at least one node overlaps between them (R + W > N). This maximizes availability and write scalability.

**Trade-offs for {name}**:

| Strategy | Use Case | Pros | Cons |
|---|---|---|---|
| Leader-based | {s['restricted']} | Strong consistency, simple | Write bottleneck, leader failure risk |
| Multi-leader | {s['non_restricted']} | Low-latency global writes | Conflict resolution, complex |
| Leaderless | Caching, counters | High availability, no bottleneck | Eventual consistency, read repair overhead |

**Real-world implementations**

- **Redis**: Leader-follower replication with asynchronous replication; Sentinel handles failover.
- **Apache Kafka**: Leader-based partition replication with ISR (in-sync replica) — writes go to the leader, followers replicate.
- **Cassandra**: Tunable consistency with leaderless quorum (R + W > N).
- **DynamoDB Global Tables**: Multi-master active-active across regions.
"""


def gen_failure_detection(s):
    name = s['name']
    return f"""### Failure Detection and Membership

**What it means**

Failure Detection and Membership is the mechanism by which {name} determines which nodes are alive and part of the cluster. Membership is the list of known nodes; failure detection is the process of updating that list when nodes fail or recover.

**Why it matters**

{name} must route requests only to healthy nodes and trigger failover when a node goes down. False positives (healthy nodes marked as dead) cause unnecessary failovers and data loss. False negatives (dead nodes not detected) cause failed requests and degraded performance.

**How it works**

**Heartbeat-based detection**: Each node sends a heartbeat (ping) to a subset of peers at regular intervals. If a node misses N consecutive heartbeats, it is marked as suspect. The gossip protocol distributes membership information: each node exchanges its view of the cluster with a random peer, and the information propagates gossip-style.

```mermaid
sequenceDiagram
    participant A as Node A
    participant B as Node B
    participant C as Node C

    loop Every 1s
        A->>B: Heartbeat (ping)
        B-->>A: Heartbeat (ack)
    end
    B->>C: Gossip: A is alive
    C->>A: Gossip: B is alive
    Note over A,B,C: View converges in O(log N) rounds
```

*Gossip-based failure detection: each node periodically pings a random subset of peers and gossips its view of the cluster. The membership list converges in O(log N) rounds.*

**Phi Accrual Failure Detector**: Instead of a fixed timeout, the detector measures the time between consecutive heartbeats and computes a phi (φ) value — the probability that the node is dead given the observed heartbeat pattern. φ is compared against a threshold (typically 1–8); higher thresholds reduce false positives but increase detection latency.

**SWIM (Scalable Weakly-consistent Infection-style Process group Membership Protocol)**: Nodes ping a random subset of cluster members. If a ping fails, the node is marked "suspect" and the failure is "infected" (gossiped) to other nodes. This is O(log N) per failure detection cycle and scales to large clusters.

**Trade-offs**:

| Approach | Strengths | Weaknesses |
|---|---|---|
| Heartbeat (timeout-based) | Simple, deterministic | False positives under load |
| Phi Accrual | Adaptive threshold | Needs historical data |
| SWIM | Scales to 1000s of nodes | Eventual consistency |

**Real-world implementations**

- **AWS Route 53 Health Checks**: Uses TCP/HTTP health checks with configurable thresholds to remove unhealthy instances from DNS rotation.
- **Kubernetes**: Uses the kubelet heartbeat (every 10s) to determine node liveness; nodes missing 3 consecutive heartbeats are marked NotReady.
- **Consul**: Uses SWIM protocol for membership and failure detection; supports both LAN and WAN gossip.
- **Akka Cluster**: Uses Phi Accrual failure detector with configurable φ thresholds.
"""


def gen_high_availability(s):
    name = s['name']
    return f"""### High Availability and Scalability

**What it means**

High Availability and Scalability determines how {name} continues operating when nodes or entire zones fail, and how capacity is added as demand grows. HA is about minimizing downtime; scalability is about maintaining performance as load increases.

**Why it matters**

{name} must stay operational even when individual nodes, availability zones, or entire regions fail. At the same time, it must scale horizontally to handle traffic spikes without degrading latency. The two are intertwined: the replication strategy, failure detection, and load balancing all contribute to both HA and scalability.

**How it works**

**Availability zones (AZs)**: Nodes are distributed across multiple AZs within a region. Each AZ is an independent failure domain (power, networking, physical security). A load balancer distributes requests across AZs; if one AZ fails, traffic is routed to the remaining AZs with no data loss (assuming replication is in place).

```mermaid
flowchart TD
    subgraph "3 AZs in One Region"
        AZ1[AZ-1<br/>2+ nodes]
        AZ2[AZ-2<br/>2+ nodes]
        AZ3[AZ-3<br/>2+ nodes]
    end
    LB[Load Balancer]
    LB --> AZ1
    LB --> AZ2
    LB --> AZ3
    AZ1 -->|Replicate| AZ2
    AZ2 -->|Replicate| AZ3
```

*Multi-AZ deployment: a load balancer distributes traffic across three availability zones. Each AZ has multiple nodes. Data is replicated across AZs so that losing one AZ does not cause data loss or service interruption.*

**Load balancing**: A load balancer distributes incoming requests across healthy nodes. Algorithms include round-robin, least connections, and weighted routing. Health checks ensure traffic only goes to healthy nodes. For {name}, the load balancer also considers {s['key_components'][0]} when routing.

**Auto-scaling**: The system automatically adds or removes nodes based on metrics (CPU, memory, request rate). Scale-out policies add nodes when load exceeds a threshold; scale-in policies remove nodes during low load. For stateful services like {name}, scale-out involves rebalancing partitions (moving data and connections to the new node).

**Failover and recovery**: When a node fails, the load balancer detects it (via health checks or failure detection) and stops sending traffic. A new node is provisioned (or a standby is promoted) and begins serving. For {name}, failover must preserve {s['restricted']} data — this is achieved through replication with a quorum of healthy nodes.

**Scalability patterns**:

1. **Horizontal partitioning (sharding)**: Split data by a partition key (e.g., user_id, session_id) and distribute partitions across nodes. New nodes take ownership of additional partitions.

2. **Consistent hashing**: Minimize data movement on scale-out — only 1/N of the data moves to the new node. Nodes and partitions are placed on a ring; a request for key X is routed to the next node clockwise from hash(X).

3. **Connection draining**: When scaling in, existing connections are allowed to complete before the node is shut down. For {name}, this means draining active {s['brief'].split(' ')[0]} sessions gracefully.

**Real-world implementations**

- **Netflix OSS (Eureka + Zuul + Ribbon)**: Service discovery with Eureka, edge routing with Zuul, and client-side load balancing with Ribbon. Scales to thousands of instances.
- **Kubernetes HPA + VPA**: Horizontal Pod Autoscaler scales pods based on CPU/memory; Vertical Pod Autoscaler adjusts resource requests based on historical usage.
- **AWS ALB + Auto Scaling Groups**: Application Load Balancer with auto-scaling groups across AZs; health checks replace unhealthy instances automatically.
"""


def gen_performance_optimization(s):
    name = s['name']
    return f"""### Performance and Optimization

**What it means**

Performance and Optimization covers the techniques {name} uses to achieve low latency, high throughput, and efficient resource usage. This section examines the key performance metrics, bottlenecks, and optimizations specific to the system.

**Why it matters**

{name} faces competing pressures: users demand low latency, the system must handle high throughput, and infrastructure costs must be controlled. The optimizations applied at the data, compute, and network layers determine whether the system meets its SLA.

**How it works**

**Latency layers**: Latency in {name} comes from three layers:
1. **Network**: Round-trip time from client to the nearest edge node / load balancer.
2. **Application**: Request processing time on the server (CPU, I/O, lock contention).
3. **Data**: Time to read/write from storage (cache hit vs. database query).

The 99th-percentile latency is the key metric for user-facing systems — it determines the worst-case experience.

**Caching strategies**: {name} uses multiple cache layers:
- **Edge cache**: Static assets (images, CSS, JS) served from a CDN at the edge. For {name}, this caches {s['non_restricted']} that doesn't change frequently.
- **Application cache**: In-memory cache (e.g., Redis, Memcached) for frequently accessed data. Cache-aside pattern: application checks cache first, falls back to database on miss.
- **Local cache**: In-process cache (e.g., Caffeine, Guava) for data accessed within a single request. Avoids network round-trips.

**Batching and pipelining**: {name} batches small operations (e.g., writes, log flushes) to amortize per-operation overhead. Pipelining allows multiple requests to be in flight simultaneously.

```mermaid
flowchart LR
    subgraph "Client Layer"
        Client[Client Request]
    end
    subgraph "Edge Layer"
        Edge[CDN / Edge Cache]
        EdgeCache[(Cached Static Assets)]
    end
    subgraph "Application Layer"
        App[App Server Cluster]
        AppCache[(Redis/Memcached)]
        DB[(Database)]
    end
    Client --> Edge
    Edge -->|Cache Hit| Client
    Edge --> App
    App --> AppCache
    AppCache -->|Hit| App
    AppCache --> DB
    DB --> AppCache
```

*Caching hierarchy: clients first hit the edge CDN/cache; if the response is cached, it is returned immediately. Otherwise, the request reaches the application, which checks its in-memory/application cache (e.g., Redis) before falling back to the database. This minimizes latency from each layer.*

**Connection pooling**: {name} maintains a pool of database connections to avoid the TCP handshake overhead on every request. Pool size is tuned to match the database's capacity.

**Compression**: Responses are compressed (gzip, zstd) for clients that support it. At the network layer, gRPC uses HPACK header compression.

**Indexing**: Database tables are indexed on frequently queried fields. For {name}, indexes cover {s['key_components'][1]} and {s['key_components'][2]} for fast lookups.

**Asynchronous processing**: Non-critical background work (e.g., analytics, cleanup, notifications) is offloaded to message queues and processed asynchronously, keeping the request path fast.

**Resource isolation**: CPU and memory are allocated per service (containers with cgroup limits). This prevents a single misbehaving service from degrading the entire system.

**Metrics for {name}**:

| Metric | Target | How to Measure |
|---|---|---|
| P99 latency | < {('100ms' if 'game' in name.lower() else '1s')} | Load test with realistic traffic |
| Throughput | {('10K RPS' if 'bidding' in name.lower() else '1K RPS')} | Request rate under peak load |
| Error rate | < 0.1% | 5xx / total requests |
| Cache hit ratio | > 90% | cache_hits / (cache_hits + misses) |
| Resource utilization | < 80% CPU, < 85% memory | Container metrics |

**Real-world implementations**

- **Google's HTTP Load Balancer**: Global load balancing with edge PoPs; routes users to the nearest healthy backend.
- **Cloudflare**: Edge cache with Argo Smart Routing that dynamically routes traffic to avoid congestion.
- **Redis**: Used as an application cache with configurable eviction policies (LRU, LFU, TTL).
"""


def gen_cap_theorem(s):
    name = s['name']
    return f"""### CAP Theorem and Consistency Trade-offs

**What it means**

The CAP Theorem states that in a distributed system, you can only have two of three guarantees: **Consistency** (every read returns the latest write), **Availability** (every request gets a response), and **Partition tolerance** (the system continues to operate despite network partitions). Since network partitions are inevitable in distributed systems like {name}, the real choice is between CP (consistent + partitioned) and AP (available + partitioned).

**Why it matters**

{name} must decide which two guarantees to prioritize. For {s['restricted']} data, strong consistency (CP) is critical — users must see the most recent data. For {s['non_restricted']} data, availability (AP) is more important — the system should remain responsive even during network issues.

**How it works**

**CP (Consistent + Partition-tolerant)**: During a partition, the system trades availability for consistency. Writes are rejected or delayed until the partition heals. Reads return the latest committed value. This is appropriate for {s['restricted']} in {name}.

```mermaid
flowchart TD
    subgraph "CP Mode (during partition)"
        A[Client] -->|write| P1[Primary Node]
        P1 -->|sync| S1[Synchronous Replica]
        S2[Suspended Node<br/>partitioned] -->|Unavailable| Client2[Client 2]
    end
    A -->|read| P1
    A -->|read| S1
```

*CP system during a network partition: writes are rejected on the partitioned node to maintain consistency. Clients are routed to the healthy primary and synchronous replica.*

**AP (Available + Partition-tolerant)**: During a partition, the system trades consistency for availability. Both sides accept writes; conflicts are resolved later (last-write-wins, merge, or application-level conflict resolution). This is appropriate for {s['non_restricted']} in {name}.

**PACELC (extending CAP)**: The PACELC theorem says that even when the network is not partitioned (the "else" case in CAP), you must choose between latency (L) and consistency (C). {name} uses:
- **Racing reads**: Serve from the nearest replica for speed (low latency, eventual consistency).
- **Linearizable reads**: Always read from the primary (high latency, strong consistency).

The choice is made per request based on whether the data is {s['restricted']} (strong consistency) or {s['non_restricted']} (fast reads).

**Trade-offs**:

| System Type | CP Use Cases | AP Use Cases |
|---|---|---|
| {name} | {s['restricted']} | {s['non_restricted']} |

**Real-world implementations**

- **etcd**: CP system using Raft consensus; used for service discovery and configuration in Kubernetes.
- **Cassandra**: AP system with tunable consistency; used for time-series data and user sessions.
- **Google Spanner**: CP with external consistency via TrueTime API; used for global financial transactions.
- **DynamoDB**: AP by default, but supports strongly consistent reads (CP mode) on demand.
"""


def gen_encryption(s):
    name = s['name']
    return f"""### Encryption and Key Management

**What it means**

Encryption and Key Management in {name} ensures that data is protected both at rest (stored on disk) and in transit (moving between services). Key management governs how encryption keys are generated, stored, rotated, and accessed — without proper key management, encryption provides a false sense of security.

**Why it matters**

{name} handles {s['restricted']} that must be encrypted both at rest and in transit. {s['main_challenge']} requires careful key management: keys must be rotated regularly, scoped to prevent cross-contamination, and audited for compliance. A single key compromise could expose sensitive data.

**How it works**

**At-rest encryption**: Data stored in {', '.join(s['key_components'][:2])} and databases is encrypted using AES-256-GCM. The Data Encryption Key (DEK) is generated per data partition and encrypted with a Key Encryption Key (KEK) managed by a KMS (AWS KMS, GCP KMS, HashiCorp Vault). Keys are regionally scoped — only data belonging to a region can be decrypted by that region's KEK.

**In-transit encryption**: All inter-service communication uses TLS 1.3 or mTLS for service-to-service auth. Cross-region communication of {s['non_restricted']} uses TLS + optional application-level encryption. {s['restricted']} is NEVER transmitted in plaintext or across region boundaries.

**Key hierarchy**:
```
Master Key (HSM-backed, KMS-managed)
  └─ KEK (per region, per service)
     └─ DEK (per data partition, rotated every 90 days)
        └─ Data (encrypted with DEK)
```

**Key rotation**: KEKs rotate annually (automatic via KMS); DEKs rotate per object or per 90 days. Applications handle key version headers transparently — a DEK version is stored alongside the encrypted data.

**Cross-region key sharing**: For non-restricted data ({s['non_restricted']}), a shared key is imported into each region's KMS. Restricted data NEVER uses cross-region keys — each region's KMS holds only that region's keys.

```mermaid
graph TD
    subgraph "Region EU KMS"
        DEK_EU[DEK for EU data]
        DataEU[(Encrypted EU Data<br/>AES-256)]
    end
    subgraph "Region US KMS"
        DEK_US[DEK for US data]
        DataUS[(Encrypted US Data<br/>AES-256)]
    end
    KMS[(KMS/HSM<br/>Master Key)]
    KMS -->|unwrap| DEK_EU
    KMS -->|unwrap| DEK_US
    DEK_EU --> DataEU
    DEK_US --> DataUS
    SharedDEK[Shared DEK<br/>for non-restricted global data]
    KMS -->|unwrap shared| SharedDEK
    GlobalData[(Global Index<br/>encrypted with shared key)]
    SharedDEK --> GlobalData
    Client[Client] -->|TLS 1.3| DataEU
    Client -->|TLS 1.3| DataUS
```

*Encryption key hierarchy: master keys are managed by an HSM-backed KMS and never leave the KMS. Each region has its own KEK. Data encryption keys (DEKs) are generated per partition and encrypted with the regional KEK. Only non-restricted global data uses a shared cross-region key. All client traffic uses TLS 1.3.*

**Java/Spring Boot Implementation**

```java
@Service
@RequiredArgsConstructor
public class DataEncryptionService {{

    private final AWSKMS kms;
    @Value("${{app.region}}")
    private String region;
    @Value("${{app.encryption.dek-ttl-minutes:1440}}")
    private int dekTtlMinutes;

    private final Map<String, SecretKey> dekCache = new ConcurrentHashMap<>();

    public EncryptedData encrypt(String plaintext, String partitionId) {{
        SecretKey dek = getOrCreateDek(partitionId);
        byte[] ciphertext = CryptoUtils.encrypt(plaintext.getBytes(StandardCharsets.UTF_8), dek);
        String dekCiphertext = kms.encrypt(EncryptRequest.builder()
            .keyId("arn:aws:kms:" + region + ":master-key")
            .plaintext(SdkBytes.fromByteArray(dek.getEncoded()))
            .build()).ciphertextBlob().asByteArray();
        return new EncryptedData(ciphertext, dekCiphertext, Instant.now());
    }}

    private SecretKey getOrCreateDek(String partitionId) {{
        return dekCache.computeIfAbsent(partitionId, id -> {{
            try {{
                return KeyGenerator.getInstance("AES").generateKey();
            }} catch (NoSuchAlgorithmException e) {{
                throw new IllegalStateException("Cannot generate DEK", e);
            }}
        }});
    }}
}}
```

*Spring Boot encryption service: DEKs are cached per-partition with TTL. Each DEK is encrypted via AWS KMS using a regional master key. The encrypted DEK (ciphertext) is stored alongside the data — only the KMS for that region can decrypt it.*

**Real-world implementations**

- **AWS KMS**: Managed HSM-backed key service; supports automatic key rotation and custom key stores.
- **HashiCorp Vault**: Open-source key management; supports transit encryption (encrypt/decrypt without storing keys).
- **Google Cloud KMS**: Hardware-backed key management with IAM-based access control.
"""


def gen_authentication(s):
    name = s['name']
    return f"""### Authentication and Authorization

**What it means**

Authentication and Authorization (AuthN/AuthZ) in {name} control who can access the system and what they can do. Authentication verifies identity; authorization determines permissions. In a distributed system like {name}, auth must work across multiple nodes while respecting data boundaries — a user authenticated in one region should not have their session data or tokens replicated to regions where it is not permitted.

**Why it matters**

{name} must verify identity at the edge and enforce authorization at every service boundary. {s['restricted']} must be protected — only users with appropriate roles should access it. At the same time, {s['non_restricted']} data should be accessible to a wider audience with minimal friction.

**How it works**

**Authentication (who are you?)**:
- **JWT tokens**: Users authenticate through their home region's identity provider. The region returns a JWT (JSON Web Token) signed by a regional signing key. Tokens include claims like `iss` (issuer region), `sub` (subject/user ID), `home_region`, `roles`, and `exp` (expiry). Tokens are scoped per region — a token issued by region A cannot access restricted data in region B.
- **mTLS for service-to-service**: Internal services authenticate each other using mutual TLS certificates issued by a per-region Certificate Authority (CA). No shared secrets cross region boundaries.
- **Session management**: Sessions are stored regionally (Redis) and never replicated cross-region for restricted data. Session IDs are opaque UUIDs; the session store maps session ID → user context.

**Authorization (what can you do?)**:
- **RBAC (Role-Based Access Control)**: Users are assigned roles per region. Common roles: `region_admin` (full access to region data), `auditor` (read-only audit), `viewer` (read public data only). Roles are stored in the regional database and cached locally for sub-1ms lookups.
- **ABAC (Attribute-Based Access Control)**: Fine-grained permissions based on attributes (e.g., `home_region == request_region AND role == admin`). This allows expressing complex policies like "users can only access restricted data in their home region."
- **Resource-level authorization**: Each request is checked against an ACL (Access Control List) that specifies which roles can access which resources. For {name}, restricted resources require the `admin` role + matching region.

```mermaid
sequenceDiagram
    participant User as User (Browser)
    participant Edge as Edge Router (Home Region)
    participant Auth as Auth Service
    participant App as App Server

    User->>Edge: HTTPS request + cookie/JWT
    Edge->>Auth: Validate token (local cache)
    Auth-->>Edge: Claims + roles
    Edge->>App: Forward request + context
    App->>App: Check region-scoped ACL
    App-->>Edge: Response (or 403)
```

*Authentication flow: the user's token is validated by the regional auth service (claims cached locally). The edge router forwards the request with the security context. Each app server checks the region-scoped ACL before accessing restricted data.*

**Java/Spring Boot Implementation**

```java
@Service
@RequiredArgsConstructor
public class AuthorizationService {{

    private final UserTokenRepository tokenRepository;
    @Value("${{app.region}}")
    private String currentRegion;

    public boolean canAccessResource(String userId, String resourceRegion,
                                     String action, JWTClaims claims) {{
        String userHomeRegion = claims.getStringClaim("home_region");
        List<String> roles = claims.getStringListClaim("roles");

        if (!roles.contains(action)) {{
            return false;
        }}

        if (resourceRegion.equals(userHomeRegion)) {{
            return true;
        }}

        if (resourceRegion.equals("global")) {{
            return roles.contains("global_reader");
        }}

        return false;
    }}
}}

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1")
public class RegionController {{
    private final AuthorizationService authService;

    @GetMapping("/data/{{region}}/profile")
    public ResponseEntity<?> getProfile(
            @PathVariable String region,
            @RequestHeader("Authorization") String token) {{
        JWTClaims claims = JwtUtils.parseAndValidate(token, currentRegion);

        if (!authService.canAccessResource(
                claims.getStringClaim("sub"), region, "read", claims)) {{
            return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
        }}

        return ResponseEntity.ok(profileService.getByRegion(region));
    }}
}}
```

*Spring Boot authorization service: checks both the user's role and whether the requested resource violates region boundaries. The `canAccessResource` method returns false if a user from region EU tries to access restricted data in region US.*

**Real-world implementations**

- **Auth0**: JWT-based authentication with regional endpoints; supports custom rules for ABAC.
- **Okta**: Multi-region identity management with adaptive MFA and ThreatInsight for anomaly detection.
- **AWS Cognito**: Regional user pools with IAM integration; tokens are region-scoped by default.
"""


def gen_security_threats(s):
    name = s['name']
    return f"""### Security Threats and Mitigations

**What it means**

Security Threats and Mitigations catalog the attack surface of {name}, the most likely threats, and the corresponding defenses. Every distributed system has unique threat vectors — {name} is no exception.

**Why it matters**

{name} handles {s['restricted']} that attackers might target. {s['main_challenge']} expands the attack surface: more nodes, more network paths, more failure modes. Without proper threat modeling, a single vulnerability could expose sensitive data across the entire system.

**Threat model**:

| Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Data exfiltration (cross-region) | High | Critical | Region-scoped keys, no cross-region replication of restricted data |
| Man-in-the-middle (inter-service) | Medium | High | mTLS between all services |
| Replay attacks | Medium | High | Token expiry + nonce |
| DDoS at the edge | High | High | Rate limiting + edge filtering (Cloudflare, AWS Shield) |
| PII leakage in logs | High | High | PII redaction + field-level access control |
| Session hijacking | Medium | Medium | Short-lived tokens + IP binding |
| Privilege escalation | Low | Critical | Least-privilege RBAC + audit logs |
| Cache poisoning | Low | Medium | Cache invalidation on write + signed cache keys |

**How it works**

**Data exfiltration prevention**: {name} enforces data residency by design — {s['restricted']} is never replicated cross-region. The replication layer checks a data classification label before allowing cross-region copy. A database-level policy (e.g., PostgreSQL RLS) also blocks cross-region queries for restricted partitions.

**mTLS enforcement**: All service-to-service communication uses mutual TLS. Certificates are issued by a per-region CA and rotated every 30 days. Services must present a valid certificate to communicate — no plaintext connections are allowed.

**PII redaction**: Application logs are scanned for PII patterns (email, phone, credit card) using an automated redaction layer (e.g., AWS Macie, Google DLP). {s['non_restricted']} is logged freely; restricted fields are masked or dropped before logging.

```mermaid
graph TD
    subgraph "Threat Surface"
        Client[Client]
        Edge[Edge Router / WAF]
        App[App Server]
        DB[(Database)]
        Cache[(Cache)]
        Logs[Log Store]
    end

    Client -->|HTTPS| Edge
    Edge -->|mTLS| App
    App -->|mTLS| DB
    App -->|Read| Cache
    App -->|Write| DB
    App -->|Log| Logs

    subgraph "Mitigations"
        WAF[AWS WAF /<br/>Cloudflare]
        DLP[PII Redaction<br/>(Macie/DLP)]
        FIM[File Integrity<br/>Monitoring]
    end

    Edge -.-> WAF
    Logs -.-> DLP
    DB -.-> FIM
```

*Threat mitigation diagram: the WAF at the edge blocks DDoS and injection attacks. mTLS protects all service-to-service communication. PII redaction scans logs before storage. File integrity monitoring alerts on database tampering.*

**Audit trail**: All security-relevant events (auth, data access, config changes) are written to an append-only audit log with cryptographic integrity (HMAC per entry). The log covers {s['restricted']} access — who accessed what, when, and from where.

**Real-world implementations**

- **Cloudflare**: Zero-trust model (All Connections to All Networks) with mTLS everywhere; uses GeoIP blocking and rate limiting for DDoS mitigation.
- **Google BeyondCorp**: Zero-trust network security model; all access is authenticated and authorized at the request level.
"""


def gen_observability(s):
    name = s['name']
    return f"""### Observability and Logging

**What it means**

Observability and Logging in {name} provide visibility into system behavior through three pillars: **metrics** (aggregates and counters), **logs** (structured event records), and **traces** (distributed request timelines). Together, these signals allow operators to debug issues, detect anomalies, and verify SLA compliance.

**Why it matters**

Distributed systems like {name} are inherently opaque — failures can cascade across services in unexpected ways. Without good observability, a single slow dependency can cause widespread timeouts that are nearly impossible to diagnose. {s['main_challenge']} makes observability even more critical: operators need to see cross-region latency, regional failures, and data-residency violations.

**How it works**

**Metrics**: {name} instruments every service with Prometheus-style metrics:
- **Request rate, error rate, duration (the "RED" metrics)**: Tracks per-endpoint HTTP latency and error counts.
- **System metrics**: CPU, memory, disk I/O, network throughput per node.
- **Business metrics**: For {name}, this includes metrics like "{s['key_components'][1]} fill rate" and "reservation conflict rate".

Metrics are aggregated in a time-series database (Prometheus, VictoriaMetrics) and visualized in Grafana dashboards with alerts via PagerDuty.

**Logs**: {name} uses structured logging (JSON format) with standardized fields:
- `timestamp`: ISO 8601 UTC
- `level`: DEBUG, INFO, WARN, ERROR
- `service`: originating service name
- `trace_id`: distributed trace identifier (for correlation)
- `span_id`: current operation span
- `region`: the region that processed the request
- `data_class`: RESTRICTED or NON_RESTRICTED

{s['restricted']} access is logged with full context (user, action, resource). {s['non_restricted']} logs are aggregated and may have reduced retention.

**Distributed tracing**: Every request is assigned a trace ID at the edge. The trace propagates through all downstream services via HTTP headers. A tracing backend (Jaeger, Tempo, Zipkin) reconstructs the full request timeline, showing latency at each hop. For {name}, traces include region boundaries — a cross-region call is annotated as such.

```mermaid
graph TD
    subgraph "Region EU"
        AppEU[App Server EU]
        PromEU[Prometheus EU]
        LokiEU[Loki Logs EU]
    end
    subgraph "Region US"
        AppUS[App Server US]
        PromUS[Prometheus US]
        LokiUS[Loki Logs US]
    end
    subgraph "Global"
        Grafana[Grafana Dashboard]
        Tempo[Tempo Tracing]
        Alertmanager[(Alertmanager)]
    end
    AppEU -->|metrics| PromEU
    AppEU -->|logs| LokiEU
    AppUS -->|metrics| PromUS
    AppUS -->|logs| LokiUS
    PromEU -->|remote write| Grafana
    PromUS -->|remote write| Grafana
    LokiEU --> Grafana
    LokiUS --> Grafana
    AppEU -->|traces| Tempo
    AppUS -->|traces| Tempo
    PromEU --> Alertmanager
    PromUS --> Alertmanager
```

*Observability architecture: each region runs its own Prometheus (metrics) and Loki (logs) instances. A global Grafana instance queries all regional backends. Traces are collected centrally in Tempo. Alerts fire from each region's Prometheus to Alertmanager.*

**Alerting**: {name} defines SLO-based alerts:
- **Latency**: P99 > 1s for 5 minutes → page.
- **Error rate**: > 1% for 10 minutes → page.
- **Availability**: < 99.5% for 15 minutes → page.
- **Data residency violation**: any restricted data detected outside its region → critical page.

**Java/Spring Boot Implementation**

```java
@Component
@RequiredArgsConstructor
@Slf4j
public class ObservabilityContext {{

    @Value("${{app.region}}")
    private String region;

    public void logAccess(String userId, String resource, String action,
                          boolean restricted) {{
        log.info("access_event userId={{}} resource={{}} action={{}} region={{}} data_class={{}}",
            userId, resource, action, region, restricted ? "RESTRICTED" : "NON_RESTRICTED");
    }}
}}

@RestController
@RequiredArgsConstructor
@Slf4j
public class ApiController {{
    private final ObservabilityContext obs;
    private final UserService userService;

    @GetMapping("/api/v1/profile")
    public ResponseEntity<ProfileResponse> getProfile(
            @AuthenticationPrincipal UserDetails user) {{
        String traceId = MDC.get("traceId");
        long start = System.nanoTime();

        try {{
            ProfileResponse response = userService.getProfile(user.getId());
            obs.logAccess(user.getId(), "profile", "read", true);

            return ResponseEntity.ok(response);
        }} finally {{
            long durationMs = (System.nanoTime() - start) / 1_000_000;
            log.info("profile_read traceId={{}} latencyMs={{}} region={{}}",
                traceId, durationMs, obs.region);
        }}
    }}
}}
```

*Spring Boot observability: the `ObservabilityContext` logs structured access events with data classification. The controller records latency and trace ID for every request, enabling SLO-based alerting.*

**Real-world implementations**

- **Netflix OSS (Atlas + Zipkin + Servo)**: Metrics via Atlas, traces via Zipkin, instrumented via Servo. Scales to over 700 billion requests/day.
- **Google SRE Workbook**: Comprehensive observability with SLI/SLO/SLI definition; uses Borgmon for metrics and Dapper for tracing.
- **AWS Observability**: CloudWatch for metrics, X-Ray for tracing, CloudWatch Logs for structured logs.
"""


def gen_data_model_and_api(s, fname):
    name = s['name']
    if "multiplayer" in fname:
        return f"""### Data Model and API

**What it means**

The **Data Model and API** section describes the entities that {name} tracks, the relationships between them, and the API contract that services and clients use to interact with the system. For a multiplayer game, the data model must capture stateful entities (players, matches, game objects) and the API must support both real-time WebSocket messages and REST operations.

**Why it matters**

{s['brief']}. The data model defines how state is serialized, synchronized, and recovered after failure. The API contract defines how clients interact with the authoritative server and how regions communicate for cross-region features. Getting either wrong creates inconsistency, scalability bottlenecks, or client incompatibility.

**How it works**

**Entities and relationships**:

```mermaid
erDiagram
    PLAYER {{
      string playerId PK "Unique player identifier"
      string username "Display name (non-restricted)"
      string homeRegion "Legal region (GDPR, DPDP)"
      int mmr "Matchmaking rating"
      string currentMatchId FK "Match the player is in"
    }}
    MATCH {{
      string matchId PK "Unique match identifier"
      string gameMode "e.g., competitive, co-op"
      int maxPlayers "Max players (2-100)"
      enum status "waiting, active, ended"
      string regionId "Hosting region"
      datetime createdAt
      datetime endedAt
    }}
    GAME_OBJECT {{
      string entityId PK "Entity within match"
      string matchId FK "Parent match"
      string type "player, projectile, pickup"
      float x "Position X"
      float y "Position Y"
      float health
      json state "Serialized state"
    }}
    PLAYER ||--o{{ MATCH : "joins"
    MATCH ||--o{{ GAME_OBJECT : "contains"
```

*Entity relationship diagram: each Player has a homeRegion (for data residency). A Player joins one active Match. Each Match contains many Game Objects (players, projectiles, pickups). The matchId links Players to their current Match; the regionId on Match determines where the match is hosted.*

**API contract**:

The system exposes two API surfaces:

1. **REST API** (cross-region, out-of-session operations):
   - `GET /api/v1/matches/{{matchId}}` — fetch match metadata (cross-region lobby lookup)
   - `GET /api/v1/player/stats` — fetch player statistics and MMR
   - `POST /api/v1/matchmaking/queue` — join matchmaking queue

2. **WebSocket API** (in-region, real-time gameplay):
   - `CONNECT /ws/match/{{matchId}}?token=JWT` — join an active match
   - `IN_MESSAGE: input` — client sends input (delta-compressed, sequence-numbered)
   - `OUT_MESSAGE: state_update` — server broadcasts authoritative state (entity updates, events)

**API guarantees**:
- **WebSocket connections** are routed to the match's home region by the matchmaker; cross-region WebSocket is not used (latency > 50 ms violates the sub-100ms requirement).
- **At-most-once** delivery for input messages (client-side prediction + server reconciliation handles retransmission).
- **Ordered** broadcast of state updates within a match (fixed-timestep ticks, 1 tick = 33 ms for 30 Hz).
- **Backpressure**: if a client's send queue exceeds a threshold, the server drops non-critical updates (e.g., cosmetic entity updates) but never drops player input.

**Real-world implementations**

- **Riot Games**: Uses a custom WebSocket protocol with delta compression for Valorant; matchmaker assigns home region based on player geography and queue time.
- **Epic Games (Unreal)**: Unreal Engine's replication graph controls which game objects are replicated to which clients based on visibility and relevancy.
- **Unity (Netcode for GameObjects)**: WebSocket-based transport with client prediction and server reconciliation.
"""
    elif "log" in fname:
        return f"""### Data Model and API

**What it means**

The **Data Model and API** section describes the schema of a log entry (the fundamental unit that {name} processes), the structure of the inverted index used for search, and the API contract that log agents, search clients, and alerting systems use to interact with the system.

**Why it matters**

{s['brief']}. The log entry schema determines what fields are searchable, what can be aggregated, and how PII is masked. The API contract determines throughput (how many agents can ship logs) and query flexibility (how operators can search and filter). Getting either wrong creates parsing failures, search blind spots, or ingestion bottlenecks.

**How it works**

**Entities and relationships**:

```mermaid
erDiagram
    LOG_ENTRY {{
      string logId PK "Unique per log line (hash)"
      string timestamp "ISO 8601, UTC"
      string level "DEBUG|INFO|WARN|ERROR"
      string service "Originating service name"
      string traceId "Distributed trace ID"
      string spanId "Current span ID"
      string regionId "Region that generated the log"
      string message "Human-readable log line"
      json metadata "Structured key-value pairs"
      boolean piiFlag "True if PII in message"
      string maskedMessage "PII-redacted version"
    }}
    LOG_ENTRY }}|--|| INDEX : "indexed by"
    INDEX {{
      string field "e.g., level, service, traceId"
      string value "e.g., ERROR, auth-service, abc123"
      int docCount "Number of matching log entries"
    }}
```

*Entity relationship diagram: each LOG_ENTRY has a unique logId, a timestamp, level, service, traceId for correlation, and a piiFlag indicating whether the message contains PII. The INDEX table maps field-value pairs to document counts for fast aggregation queries.*

**API contract**:

The system exposes three API surfaces:

1. **Ingest API** (agent → indexer):
   - `POST /api/v1/logs` — ship structured log entries (JSON array, batch up to 1MB)
   - `PUT /api/v1/logs/stream` — streaming ingest via HTTP/2 (for high-throughput agents)
   - `POST /api/v1/logs/{{logId}}/ack` — acknowledge successful ingestion

2. **Search API** (client → storage):
   - `POST /api/v1/search` — structured query DSL (JSON)
   - `GET /api/v1/logs/{{logId}}` — fetch a single log entry
   - `GET /api/v1/logs/stream?traceId=abc123` — follow a trace in real-time

**API guarantees**:
- **Ingestion**: at-least-once delivery; client retries on 5xx; deduplication via logId.
- **Search**: eventual consistency for recent logs (indexing lag 0-5s); point-in-time queries return consistent snapshots.
- **Rate limits**: 10,000 log lines/sec per agent; 60 search queries/sec per user.
- **PII handling**: messages with piiFlag=true are masked before global indexing; raw logs stored in-region with 7-day TTL.

**Real-world implementations**

- **Elastic Stack (Filebeat → Elasticsearch)**: Filebeat ships logs to Elasticsearch; index templates define the schema; Kibana provides search UI.
- **Datadog**: Custom agent with protobuf transport; unified logging + APM traces.
- **Loki (Grafana)**: Log aggregation using label-based indexing (not full-text inverted index); cost-effective at scale.
- **AWS CloudWatch Logs**: Structured logging with metric filters; cross-region for non-PII data.
"""
    else:
        return f"""### Data Model and API

**What it means**

The **Data Model and API** section describes the entities that {name} manages, their relationships, and the API contract through which services and clients interact with the system.

**Why it matters**

{s['brief']}. The data model defines what state is persisted and how entities relate. The API contract defines how callers request and mutate that state. Getting either wrong creates data inconsistency, tight coupling, or scalability bottlenecks.

**How it works**

**Entities and relationships**:

```mermaid
erDiagram
    ENTITY {{
      string id PK "Unique identifier"
      datetime createdAt "Record creation time"
      datetime updatedAt "Last update time"
      string createdBy "Creating service/user"
    }}
```

*Entity relationship diagram: the core entity schema with standard audit fields (createdAt, updatedAt, createdBy). Specific attributes depend on the system domain.*

**API contract**:

1. **REST API** (request/response):
   - `GET /api/v1/{{resource}}` — list/filter resources
   - `GET /api/v1/{{resource}}/{{id}}` — fetch a single resource
   - `POST /api/v1/{{resource}}` — create a new resource
   - `PUT /api/v1/{{resource}}/{{id}}` — replace a resource
   - `DELETE /api/v1/{{resource}}/{{id}}` — delete a resource

2. **API guarantees**:
- **Idempotency**: POST supports idempotency keys; PUT is idempotent by design.
- **Pagination**: cursor-based (not offset-based) for stable ordering at scale.
- **Rate limiting**: per-user and per-service limits.
- **Validation**: all input validated with @Valid + custom validators.
"""


# ---- Heading restructuring for old-format files ----

CANONICAL_HEADINGS = {
    'Introduction / Problem Statement', 'Characteristics', 'Pros', 'Cons', 'Use Cases',
    'Components', 'Architectural Patterns', 'Benefits', 'Challenges', 'Best Practices',
    'When to Use / When Not to Use', 'Data Model and API',
    'Replication Strategies', 'Failure Detection and Membership',
    'High Availability and Scalability', 'Performance and Optimization',
    'CAP Theorem and Consistency Trade-offs',
    'Encryption and Key Management', 'Authentication and Authorization',
    'Security Threats and Mitigations', 'Observability and Logging',
    'Real-World Implementations', 'Java and Spring Boot Implementation Guide',
    'Interview Questions and Answers', 'Topics Covered',
}

# Headings to convert from bold-text style (old Theory sub-sections)
OLD_THEORY_SUBSECTIONS = {
    'What Is It?', 'Why Does It Exist?', 'What Problem Does It Solve?',
    'Problem Statement', 'Functional Requirements', 'Non-Functional Requirements',
    'High-Level Architecture', 'Key Design Points', 'Trade-offs',
    'Important Subtopics', 'Important Subtopics Explained',
}

# ## heading → ### heading (with canonical renames)
MAJOR_SECTION_RENAMES = {
    'Patterns': 'Architectural Patterns',
    'When to Use': 'When to Use / When Not to Use',
    'Java and Spring Boot Implementation': 'Java and Spring Boot Implementation Guide',
    'Real-World Examples': 'Real-World Implementations',
    'Interview Preparation': 'Interview Questions and Answers',
    'API Contract': 'Data Model and API',
    'Data Modeling': 'Data Model and API',
}

MAJOR_SECTIONS = set(MAJOR_SECTION_RENAMES.keys()) | {
    'Characteristics', 'Components', 'Benefits', 'Pros', 'Cons', 'Challenges',
    'Best Practices', 'When to Use', 'Use Cases', 'Architecture',
    'High-Level Design', 'Deep Dive', 'API Contract', 'Data Modeling',
    'Java and Spring Boot Implementation', 'Real-World Examples',
    'Interview Preparation',
}


def restructure_headings(content):
    """Restructure old-format ##/### headings into canonical ###/#### hierarchy."""
    lines = content.split('\n')
    output = []
    in_theory = False
    in_important_subtopics = False
    skip_data_modeling = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Track sections
        if re.match(r'^## ', line):
            in_theory = (stripped == '## Theory')

        # Skip ### Important Subtopics heading and its numbered list
        if stripped in ('### Important Subtopics', '#### Important Subtopics'):
            in_important_subtopics = True
            continue
        if in_important_subtopics:
            if re.match(r'^\d+\.', stripped) or (stripped == '' and i + 1 < len(lines) and
                    re.match(r'^\d+\.', lines[i + 1].strip() if i + 1 < len(lines) else '')):
                continue
            in_important_subtopics = False

        # Skip ### Important Subtopics Explained (old content, not needed)
        if stripped == '#### Important Subtopics Explained':
            continue

        # Handle Theory sub-sections
        if in_theory:
            if stripped == '### What Is It?':
                output.append('### Introduction / Problem Statement')
                continue
            if stripped in ('### Why Does It Exist?', '### What Problem Does It Solve?') or \
               stripped.replace('### ', '') in OLD_THEORY_SUBSECTIONS:
                # Convert to bold text
                text = stripped.replace('### ', '').rstrip('?')
                output.append(f'**{text}**')
                continue

        # Change ## major sections to ### with renames
        if re.match(r'^## ', line) and not in_theory:
            m = re.match(r'^##\s+(.+)', line)
            if m:
                heading_text = m.group(1).strip()
                if heading_text in MAJOR_SECTIONS:
                    if heading_text == 'Data Modeling':
                        # Skip this heading; content merges into Data Model and API
                        skip_data_modeling = True
                        continue
                    if heading_text == 'API Contract':
                        skip_data_modeling = False
                        new_text = 'Data Model and API'
                        output.append(f'### {new_text}')
                        continue
                    skip_data_modeling = False
                    new_text = MAJOR_SECTION_RENAMES.get(heading_text, heading_text)
                    output.append(f'### {new_text}')
                    continue

        # Change ### sub-sections (outside Theory) to ####
        if re.match(r'^### ', line) and not in_theory:
            m = re.match(r'^###\s+(.+)', line)
            if m:
                heading_text = m.group(1).strip()
                if heading_text not in CANONICAL_HEADINGS:
                    output.append(line.replace('### ', '#### ', 1))
                    continue

        output.append(line)

    return '\n'.join(output)


# ---- Insertion and Topics Covered ----

def insert_sections(filepath, sections_content):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Handle both old-format and canonical Java markers
    java_markers = [
        '### Java and Spring Boot Implementation Guide',
        '## Java and Spring Boot Implementation',
    ]
    idx = -1
    for marker in java_markers:
        idx = content.find(marker)
        if idx != -1:
            break

    if idx == -1:
        print(f"  ERROR: Cannot find Java section in {filepath}")
        return False

    before_java = content[:idx]
    insert_point = before_java.rstrip() + '\n\n'
    new_content = insert_point + sections_content + content[idx:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True


def regenerate_topics_covered(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    headings = []
    for line in content.splitlines():
        m = re.match(r'^###\s+(.+)', line)
        if m:
            text = m.group(1).strip()
            if text.lower() != 'topics covered':
                headings.append(text)

    def slugify(text):
        slug = text.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        slug = re.sub(r'-+', '-', slug).strip('-')
        return slug

    lines = []
    for i, h in enumerate(headings, 1):
        lines.append(f"{i}. [{h}](#{slugify(h)})")
    topics_covered = "\n".join(lines)

    tc_start = content.find('### Topics Covered')
    if tc_start == -1:
        # Create Topics Covered after ## Theory
        theory_idx = content.find('## Theory')
        if theory_idx == -1:
            print(f"  WARNING: Cannot find ## Theory in {filepath}")
            return False
        theory_line_end = content.find('\n', theory_idx + len('## Theory'))
        new_tc = f"\n### Topics Covered\n\n{topics_covered}\n\n---\n"
        content = content[:theory_line_end + 1] + new_tc + content[theory_line_end + 1:].lstrip("\n")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Created Topics Covered: {len(headings)} items")
        return True

    tc_end_match = re.search(r'\n\n---\n', content[tc_start:])
    if tc_end_match:
        tc_end = tc_start + tc_end_match.start()
    else:
        next_section = content.find('\n### ', tc_start + 20)
        if next_section == -1:
            tc_end = len(content)
        else:
            tc_end = next_section

    new_tc = f"### Topics Covered\n\n{topics_covered}\n\n---\n"
    content = content[:tc_start] + new_tc + content[tc_end:].lstrip("\n")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  Regenerated Topics Covered: {len(headings)} items")
    return True


# ---- Main ----

if __name__ == '__main__':
    files_to_process = [
        "multi-region-deployment-system.md",
        "log-system.md",
        "recomendation-engine.md",
        "real-time-bidding-auction-system.md",
        "quick-commerce-inventory-system.md",
        "stock-broker-system.md",
        "live-comments.md",
        "settlement-reconciliation-system.md",
        "live-streaming.md",
        "multiplayer-game.md",
    ]

    for fname in files_to_process:
        s = SYSTEMS.get(fname)
        if s is None:
            print(f"ERROR: No system data for {fname}")
            continue

        is_log_system = (fname == "log-system.md")
        is_multiplayer = (fname == "multiplayer-game.md")

        sections = [
            gen_replication_strategies(s),
            gen_failure_detection(s),
            gen_high_availability(s),
            gen_performance_optimization(s),
            gen_cap_theorem(s),
            gen_encryption(s),
            gen_authentication(s),
            gen_security_threats(s),
        ]

        if not is_log_system:
            sections.append(gen_observability(s))

        if is_multiplayer or is_log_system:
            sections.insert(0, gen_data_model_and_api(s, fname))

        sections_content = "\n\n".join(section.rstrip() for section in sections) + "\n\n"

        filepath = os.path.join(ADVANCED_DIR, fname)
        print(f"Processing {fname}...")

        # Step 1: Restructure headings from old format to canonical
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        content = restructure_headings(content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Headings restructured")

        # Step 2: Insert generated canonical sections
        if insert_sections(filepath, sections_content):
            # Step 3: Create/update Topics Covered
            if regenerate_topics_covered(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    print(f"  Done. Total lines: {len(f.read().splitlines())}")
            else:
                print(f"  WARNING: Topics Covered creation failed")
        else:
            print(f"  FAILED: Could not insert sections")
