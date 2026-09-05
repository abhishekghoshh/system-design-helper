#!/usr/bin/env python3
"""
Enhance 10 advanced docs files by adding missing canonical sections.
Each section is topic-specific, generated from templates with per-system variables.
"""
import os, re

ADVANCED_DIR = "/Users/abhishekghosh/Desktop/projects/personal/system-design-helper/docs/system-design/high-level/designing/advanced"

# ---- System-specific data for each file ----
SYSTEMS = {
    "multi-region-deployment-system.md": {
        "name": "Multi-Region Deployment System",
        "brief": "routes user traffic and data to home regions based on data residency laws (GDPR, DPDP)",
        "key_components": ["GeoDNS/Edge Router", "Home Region Lookup", "Regional Stack (app servers, DB, cache, backups, logs)", "Global Index (non-restricted data only)"],
        "main_challenge": "data residency compliance while enabling global features",
        "replicas": "Regional database clusters (multi-AZ)",
        "non_restricted": "public profiles, product catalogs, search indexes",
        "restricted": "PII, messages, documents",
        "real_world": ["Cloudflare (300+ PoPs, regional data isolation)", "AWS (regional S3/RDS, cross-region replication opt-in)", "Google Cloud (dual-region buckets, EU-only storage)", "Notion (EU+US data residency)"],
        "java_focus": "region-based routing and global index search",
    },
    "log-system.md": {
        "name": "Log System",
        "brief": "centralized log aggregation, storage, and search across a microservices architecture",
        "key_components": ["Log agents (Vector/Fluentd)", "Log collectors/aggregators", "Kafka/Buffer", "Elasticsearch/Opensearch for storage", "Alerting and dashboards"],
        "main_challenge": "ingesting millions of log lines per second with low latency and high availability",
        "replicas": "log segments across collector nodes",
        "non_restricted": "application metrics, service logs",
        "restricted": "PII in log lines, stack traces with user data",
        "real_world": ["Uber uMonitor (Kafka + ES + uPlot)", "Netflix Atlas (Atlas + Spectator)", "Airbnb Stream (Airflow + ES + Superset)", "LinkedIn Kafka + Pinot", "Shopify Elastic Stack"],
        "java_focus": "log search API and structured logging",
    },
    "recomendation-engine.md": {
        "name": "Recommendation Engine",
        "brief": "provides personalized content recommendations using candidate generation and ML ranking",
        "key_components": ["Candidate Generation (ANN/retrieval)", "Feature Store", "Ranking Model (ML)", "Model Serving (Triton/Seldon)", "Feedback Loop"],
        "main_challenge": "serving real-time recommendations for millions of users from billions of items",
        "replicas": "model replicas and feature store replicas",
        "non_restricted": "public item metadata, product catalogs",
        "restricted": "user interaction history, personalization profiles",
        "real_world": ["Netflix recommendation pipeline (Metaflow + Mantis)", "YouTube Two-Tower retrieval + ranking", "Amazon Personalize (HRNN, SVD)", "Spotify (collaborative filtering + NLP)", "TikTok (multimodal, short-video)"],
        "java_focus": "recommendation API and feature retrieval",
    },
    "real-time-bidding-auction-system.md": {
        "name": "Real-Time Bidding Auction System",
        "brief": "executes ad auctions in <100ms for programmatic advertising",
        "key_components": ["Bidder (DSP)", "Ad Exchange", "SSP", "Auction Server", "Bid Request Router"],
        "main_challenge": "running sub-millisecond auctions with sealed-bid fairness",
        "replicas": "bidder and auction state across geos",
        "non_restricted": "ad creative metadata, campaign info",
        "restricted": "bid prices, user bidding history, publisher revenue",
        "real_world": ["Google AdX (real-time auction)", "Xandr (Microsoft)", "The Trade Desk (DSP)", "AppNexus (SSP)", "Amazon Publisher Services"],
        "java_focus": "bid request processing and winner determination",
    },
    "quick-commerce-inventory-system.md": {
        "name": "Quick-Commerce Inventory System",
        "brief": "manages inventory levels and reservations for hyperlocal 10-min delivery",
        "key_components": ["Inventory DB (Postgres)", "Cache (Redis)", "Reservation Engine", "Warehouse Management System", "Order Service"],
        "main_challenge": "preventing overselling under high concurrent reservation load with low latency",
        "replicas": "inventory snapshots across warehouse nodes",
        "non_restricted": "public product info, stock levels",
        "restricted": "reservation history, customer addresses",
        "real_world": ["Blinkit/Zomato (India)", "Zepto (India)", "Getir (Turkey/Netherlands)", "Gopuff (US)", "Amazon Fresh (US)"],
        "java_focus": "inventory reservation and stock validation",
    },
    "stock-broker-system.md": {
        "name": "Stock Broker System",
        "brief": "executes trades and manages order books for stock trading",
        "key_components": ["Order Management System (OMS)", "Matching Engine", "Risk Management", "Market Data Feed", "Positions/Portfolio Service"],
        "main_challenge": "matching orders with price-time priority under strict fairness and latency requirements",
        "replicas": "order book replicas across trading engines",
        "non_restricted": "public price ticks, market depth",
        "restricted": "order history, account balances, internal positions",
        "real_world": ["Zerodha (India)", "Interactive Brokers (US)", "Upstox (India)", "E*TRADE (US)", "Robinhood (US)"],
        "java_focus": "order management and risk checking",
    },
    "live-comments.md": {
        "name": "Live Comments System",
        "brief": "delivers real-time comments on live-streamed content with ordering guarantees",
        "key_components": ["Comment ingestion service", "Fan-out engine (push/pull)", "WebSocket servers", "DB (sharded by stream)", "Cache"],
        "main_challenge": "delivering millions of comments per second to millions of viewers with ordering and low latency",
        "replicas": "comment shards across stream partitions",
        "non_restricted": "public comments, emoji reactions",
        "restricted": "user IP addresses, moderation flags",
        "real_world": ["Facebook/Twitch Live Comments", "YouTube Live Chat", "Twitter Live (Periscope)", "Reddit Live Threads", "Hotstar Live Comments"],
        "java_focus": "comment ingestion and fan-out service",
    },
    "settlement-reconciliation-system.md": {
        "name": "Settlement and Reconciliation System",
        "brief": "settles payments between merchants and payment providers, then reconciles discrepancies",
        "key_components": ["Settlement Engine", "Ledger Service", "Reconciliation Engine", "Payout Service", "Audit Trail"],
        "main_challenge": "ensuring every cent is accounted for across distributed payment providers with idempotency",
        "replicas": "ledger replicas for audit and recovery",
        "non_restricted": "aggregate settlement reports, public transaction counts",
        "restricted": "merchant bank details, individual transaction amounts",
        "real_world": ["Stripe (merchant payouts)", "PayPal settlement system", "Adyen reconciliation", "Square/Block payouts", "Razorpay settlement"],
        "java_focus": "settlement batch processing and idempotency",
    },
    "live-streaming.md": {
        "name": "Live Streaming System",
        "brief": "ingests, transcodes, and distributes live video to millions of concurrent viewers",
        "key_components": ["Ingest Server (RTMP/SRT)", "Transcoder", "HLS/DASH Packager", "CDN", "Origin Shield"],
        "main_challenge": "delivering low-latency video to millions of viewers with adaptive bitrate",
        "replicas": "stream segments across edge nodes",
        "non_restricted": "public stream metadata, view counts",
        "restricted": "viewer IPs, DRM keys",
        "real_world": ["Twitch (live streaming for gaming)", "YouTube Live (HLS + DASH)", "Netflix (adaptive streaming)", "AWS IVS (interactive live video)", "Cloudflare Stream"],
        "java_focus": "stream metadata API and ingest coordination",
    },
    "multiplayer-game.md": {
        "name": "Multiplayer Game Server",
        "brief": "maintains consistent game state for real-time multiplayer games over WebSocket connections",
        "key_components": ["Game Server (authoritative)", "Matchmaking Service", "Client Prediction", "Lag Compensation", "Region Coordinator"],
        "main_challenge": "synchronizing game state for thousands of concurrent players with sub-50ms latency",
        "replicas": "game server instances across regions (by match)",
        "non_restricted": "public player stats, match results",
        "restricted": "player inputs, session tokens, match internals",
        "real_world": ["PUBG/Valorant servers (Riot)", "Fortnite (Epic/Epic Online Services)", "Minecraft servers", "Roblox game servers", "Call of Duty (Activision)"],
        "java_focus": "game session management and match creation",
    },
}

def get_system_data(filename):
    return SYSTEMS.get(filename, None)

# ---- Section content generators ----

def gen_replication_strategies(s):
    return f"""### Replication Strategies

**What it means**

Replication Strategies determine how data is copied across multiple nodes to ensure availability, durability, and performance. In a {s['name'].lower()} system, different data classes require different replication approaches: restricted data ({s['restricted']}) must stay within jurisdiction/region boundaries, while non-restricted data ({s['non_restricted']}) may be replicated globally for feature support.

**Why it matters**

{s['name']} must simultaneously provide: (a) high availability within a region (multi-AZ replication), (b) durability against single-node failures, and (c) global consistency for non-restricted data. The wrong replication strategy creates either compliance violations (restricted data crossing borders) or poor performance (over-replicated global data).

**How it works**

**Leader-based (intra-region)**: Each region runs an independent cluster with one leader and N followers across AZs. All writes go to the leader; reads can be served from followers. In {s['name']}, this protects {s['restricted']} — all replicas stay in-region. Common implementations: PostgreSQL streaming replication, MySQL semi-sync, or Raft-based consensus within the region.

```mermaid
flowchart LR
    subgraph "Region A"
        LeaderA["Leader (AZ-1)"]
        FollowerA["Follower (AZ-2)"]
        FollowerA2["Follower (AZ-3)"]
    end
    Client --> LeaderA
    LeaderA -.replicate.-> FollowerA
    LeaderA -.replicate.-> FollowerA2
    LeaderA -->|read| FollowerA
```

*Leader-based intra-region replication: writes go to the leader in AZ-1; followers in AZ-2 and AZ-3 provide read scale and AZ-level failover. All data stays within Region A, satisfying {s['name']} residency requirements.*

**Multi-leader (cross-region for non-restricted data)**: For {s['non_restricted']}, writes are accepted in any region and asynchronously propagated. Conflicts are resolved via LWW (last-write-wins) or CRDTs. This avoids cross-region latency on writes but requires conflict resolution.

**Leaderless (quorum reads/writes)**: For highly available, eventually consistent data, any node can accept writes (e.g., DynamoDB-style quorum). Replication factor 3 across AZs within a region provides availability without cross-region exposure.

**Trade-offs**

| Strategy | Use for | Pros | Cons |
|---|---|---|---|
| Leader-based | Restricted data ({s['restricted']}) | Strong consistency, no conflicts | Single-AZ leader bottleneck |
| Multi-leader | Non-restricted global data ({s['non_restricted']}) | No cross-region write latency | Conflict resolution needed |
| Leaderless | Non-restricted, eventually-ok | High availability, no leader bottleneck | Eventual consistency, read-modify-write complexity |

"""

def gen_failure_detection(s):
    return f"""### Failure Detection and Membership

**What it means**

Failure Detection and Membership determine how a distributed system identifies when nodes fail and maintains a current view of which nodes are alive (membership) and which are not. In {s['name']}, failure detection must operate at multiple levels: individual server health, AZ-level health, and region-level health.

**Why it matters**

{s['main_challenge']} requires the system to quickly detect failures and route around them. A slow failure detector causes prolonged downtime; a false positive causes unnecessary failover. In a multi-region context, region-level failure detection is especially critical — a failed region must be detected and excluded without violating data residency.

**How it works**

**Heartbeat-based detection**: Each component sends a heartbeat to a health-check service every N seconds. If no heartbeat is received within a timeout, the node is marked unhealthy. AWS ELB health checks and Kubernetes liveness probes use this.

**Gossip protocol (SWIM)**: Nodes periodically exchange health information with a few random peers. Information about failures propagates logarithmically through the cluster. Cassandra, Consul, and Elasticsearch use gossip for membership.

**Phi Accrual detector**: Instead of a fixed timeout, the detector calculates the probability that a node is down based on the historical arrival pattern of heartbeats. This adapts to network conditions. Used by Akka and Cassandra.

```mermaid
sequenceDiagram
    participant HB as Health Checker
    participant LB as Load Balancer
    participant Reg as Region Coordinator
    participant Reg2 as Peer Region
    
    HB->>LB: heartbeat every 30s
    alt no response in 90s
        LB->>Reg: mark AZ unhealthy
        Reg->>Reg2: gossip: AZ-X down
        Reg2->>Reg2: remove AZ-X from routing pool
    end
```

*Failure detection flow: a load balancer sends periodic heartbeats; if no response within the timeout, the AZ is marked unhealthy and the information is gossiped to peer regions for membership updates.*

**Real-world implementations**

- **AWS Route 53 Health Checks**: Monitors endpoint health across regions; failed regions are removed from DNS responses.
- **Kubernetes liveness/readiness probes**: HTTP/TCP checks determine pod health; unhealthy pods are evicted.
- **Consul/Serif**: Gossip-based membership and health checking for service discovery.
- **Akka Cluster (phi accrual)**: Adaptive failure detection for JVM-based distributed systems.

"""

def gen_high_availability(s):
    return f"""### High Availability and Scalability

**What it means**

High Availability (HA) and Scalability are the twin pillars of reliability in {s['name']}: HA ensures the system keeps serving requests despite failures, while scalability ensures it can handle growing load by adding resources. In a multi-region design, both operate at multiple levels — within a region (AZ-level) and across regions.

**Why it matters**

Users and operators expect the system to be available even when individual nodes, AZs, or entire regions fail. The HA strategy must account for {s['main_challenge']} while ensuring that failover does not violate data residency or consistency guarantees.

**How it works**

**Multi-AZ within region (primary HA mechanism)**: Each region is deployed across 3+ AZs. Databases use synchronous replication (Postgres streaming, MySQL semi-sync) so a single AZ failure does not lose data. Load balancers route traffic to healthy AZs automatically. This is the first line of defense — regional outages are caught at the AZ level.

**Regional failover (within residency constraints)**: If an entire AZ fails, traffic fails over to other AZs within the same region. If an entire region becomes unavailable, traffic for users whose home region is the failed region cannot be redirected (that would violate residency). Instead, the system degrades gracefully — returning a clear error ("region temporarily unavailable") or serving from a last-known-good cache.

```mermaid
flowchart TD
    subgraph "Region US"
        ALB[Application Load Balancer]
        WebA[Web Server AZ-a]
        WebB[Web Server AZ-b]
        WebC[Web Server AZ-c]
        DBA[(Primary DB<br/>AZ-a)]
        DBrep[(Replica DB<br/>AZ-b)]
    end
    ALB --> WebA
    ALB --> WebB
    ALB -->|health check fail| DownAZ[AZ-c down]
    ALB --> WebC
    DBA -.replicate.-> DBrep
```

*Multi-AZ high availability within a region: the load balancer distributes traffic across 3 AZs. If AZ-c fails health checks, traffic is routed to AZ-a and AZ-b. The database uses synchronous replication so no data is lost.*

**Auto-scaling**: Horizontal pod autoscalers (Kubernetes) or auto-scaling groups (AWS) add/remove compute based on CPU, request rate, or queue depth. In {s['name']}, scaling decisions must respect regional boundaries — a scaling event in one region does not affect others.

**Real-world implementations**

- **Netflix (chaos monkey)**: Continuously kills instances in production to test HA. Multi-region deployment with independent region stacks.
- **Airbnb (cross-region routing)**: Uses GeoDNS + edge routing to direct users to their home region; intra-AZ failover within region on AZ failure.
- **Google (spanner/multi-region)**: Regional configurations provide intra-region HA; multi-region configs provide cross-region HA for non-residency-constrained data.

"""

def gen_performance_optimization(s):
    return f"""### Performance and Optimization

**What it means**

Performance and Optimization in {s['name']} focus on reducing latency, increasing throughput, and minimizing resource waste. These optimizations are applied at every layer: network routing, caching, database queries, and application logic.

**Why it matters**

{s['brief']} operates at scale where milliseconds matter. Sub-second improvements in key paths can reduce infrastructure costs, improve user experience, and increase conversion rates. The optimization strategy must be system-specific — caching patterns for {s['name']} differ from a simple web app.

**How it works**

**Latency optimization**: The primary metric is P95/P99 latency. Key techniques:
- **Edge routing**: GeoDNS routes users to their home region's edge, reducing RTT. Sticky cookies prevent re-resolution on subsequent requests.
- **Caching**: CDN caching for static/non-restricted data ({s['non_restricted']}); regional Redis for session/user data.
- **Connection pooling**: Reuse database connections and TCP connections to downstream services.

**Throughput optimization**:
- **Sharding**: {s['name']} shards by region; within a region, data is sharded by user_id, stream_id, or item_id (depending on the domain).
- **Batching**: Batch operations (e.g., batched writes to Kafka, batched DB inserts) to amortize overhead.
- **Async processing**: Use message queues ({', '.join(s['key_components'][:2])}) to decouple fast-path writes from slow-path processing.

```mermaid
flowchart LR
    User[User Request] --> Edge[Edge Router<br/>GeoDNS + Home Region]
    Edge --> Cache[Regional Redis<br/>Cache-aside]
    Cache -->|miss| DB[(Regional DB<br/>Partitioned)]
    Cache -->|hit| User
    subgraph "Background"
        Kafka[Kafka<br/>Async Processing]
        Worker[Worker Pool]
    end
    DB -.write.-> Kafka
    Kafka --> Worker
```

*Request flow optimization: users are routed to their home region's edge, which checks a regional Redis cache first. Cache misses hit the partitioned regional database. Non-critical writes are queued to Kafka for async processing, keeping the request path fast.*

**Resource optimization**:
- **TTL-based eviction**: Cache entries and reserved resources expire automatically.
- **Right-sizing**: Auto-scaling adjusts compute to actual demand.
- **Compression**: Compress data in transit and at rest.

**Real-world implementations**

- **Netflix**: Uses Atlas for metrics, Zuul for edge routing, and Eureka for service discovery. Edge caching reduces origin load by 80%.
- **Twitch**: HLS + CDN for video; edge cache for chat; Redis for pub/sub with geographic routing.
- **Airbnb**: Multi-region Redis cache; S3 transfer acceleration for cross-region data; CDN for static assets.

"""

def gen_cap_theorem(s):
    return f"""### CAP Theorem and Consistency Trade-offs

**What it means**

The CAP Theorem states that a distributed system can guarantee at most two of: **Consistency** (every read sees the latest write), **Availability** (every request receives a response), and **Partition Tolerance** (the system continues despite network failures). Since partition tolerance is unavoidable in distributed systems, the real choice is between consistency and availability.

**Why it matters**

{s['name']} must make explicit CAP trade-offs per data class. Restricted data ({s['restricted']}) typically prioritizes consistency (CP) to avoid compliance violations, while non-restricted data ({s['non_restricted']}) may prioritize availability (AP) for features like global search.

**How it works**

**CP (Consistency + Partition Tolerance)**: The system sacrifices availability during a partition. In {s['name']}, this applies to {s['restricted']}. During an AZ failure, the system returns errors rather than serving stale data. PostgreSQL with synchronous replication is CP — if the primary fails before replicating, the standby takes over (failover), but there's a brief window of unavailability.

**AP (Availability + Partition Tolerance)**: The system sacrifices strong consistency. Reads may return stale data. In {s['name']}, this applies to {s['non_restricted']} (e.g., global search index, public profiles). Even if a region is down, the global index continues serving stale data from other regions.

**Consistency levels and tunable consistency**:

| Data Class | Trade-off | Consistency Model | Example |
|---|---|---|---|
| {s['restricted']} | CP | Strong consistency (linearizable reads) | PostgreSQL synchronous replication |
| {s['non_restricted']} | AP | Eventual consistency | DynamoDB Global Tables, Elasticsearch cross-region |

**Real-world implementation decisions**

- **Multi-region deployment systems** (like {s['name']}): Use CP within a region (strong consistency for user data) and AP for the global index (eventual consistency for public data). This is the canonical "CP within region, AP cross-region" pattern.
- **Google (Spanner)**: Uses TrueTime to achieve external consistency across regions, effectively providing CP with wide-area replication.
- **AWS DynamoDB**: Offers tunable consistency — strongly consistent reads within a region (CP) and eventually consistent reads across regions (AP).

**Interview Q&A**

- **Q: Can a system be both CP and AP?**
  **A:** Not simultaneously for the same data. But different data classes in the same system can use different trade-offs — e.g., CP for user PII and AP for public content.

- **Q: How does multi-region deployment affect the CAP choice?**
  **A:** Network latency between regions (50-300 ms) makes cross-region strong consistency impractical. Most multi-region systems use CP within a region (for low-latency strong consistency) and AP across regions (for availability).

"""

def gen_encryption(s):
    name = s['name']
    # Get a Java example relevant to the system
    java_focus = s.get('java_focus', 'data access')
    return f"""### Encryption and Key Management

**What it means**

Encryption and Key Management in {name} ensures that data is protected both at rest (stored on disk) and in transit (moving between services). Key management governs how encryption keys are generated, stored, rotated, and accessed — without proper key management, encryption provides a false sense of security.

**Why it matters**

{s['main_challenge']} means that security cannot be an afterthought. {s['restricted']} must be encrypted at rest with per-region keys, and all inter-service communication must use TLS/mTLS. A single key compromise could expose restricted data across the entire system.

**How it works**

**At-rest encryption**: Data stored in {', '.join(s['key_components'][:2])} and regional databases is encrypted using AES-256. The Data Encryption Key (DEK) is generated per data partition and encrypted with a Key Encryption Key (KEK) managed by a KMS (AWS KMS, GCP KMS, HashiCorp Vault). Keys are scoped per region — a region's KMS only holds keys for that region's restricted data.

**In-transit encryption**: All communication between client → edge router, edge → app servers, app → DB, and collector → storage uses TLS 1.3 or mTLS (for service-to-service). Cross-region replication of non-restricted data uses TLS + optional application-level encryption.

**Key hierarchy**:
```
Master Key (HSM-backed, KMS-managed)
  └─ KEK (per region, per service)
     └─ DEK (per data partition, rotated every 90 days)
        └─ Data (encrypted with DEK)
```

**Key rotation**: KEKs rotate annually (automatic); DEKs rotate per object or per 90 days. Applications must handle key version headers transparently.

**Cross-region key sharing**: For non-restricted data that crosses regions, a shared key (imported into each region's KMS) is used. Restricted data NEVER uses cross-region keys.

```mermaid
graph TD
    subgraph "Region EU (KMS Key: eu-key-1)"
        DEK_EU[DEK for EU data]
        DataEU[(Encrypted EU Data<br/>AES-256)]
    end
    subgraph "Region US (KMS Key: us-key-1)"
        DEK_US[DEK for US data]
        DataUS[(Encrypted US Data<br/>AES-256)]
    end
    KMS[(KMS/HSM<br/>Master Key)]
    KMS -->|unwrap| DEK_EU
    KMS -->|unwrap| DEK_US
    DEK_EU --> DataEU
    DEK_US --> DataUS
    subgraph "Global (shared key)"
        DataGlobal[(Non-restricted Global Index<br/>encrypted with shared key)]
        DEKGlobal[Shared DEK]
        KMS -->|unwrap shared| DEKGlobal
        DEKGlobal --> DataGlobal
    end
    TLS[TLS 1.3<br/>Client - Edge Router]
    TLS -->|encrypted| DataEU
    TLS -->|encrypted| DataUS
```

*Encryption key hierarchy: master keys are managed by an HSM-backed KMS and never leave the KMS. Each region has its own KEK. Data encryption keys (DEKs) are generated per partition and encrypted with the regional KEK. Only non-restricted global data uses a shared cross-region key. All client traffic uses TLS 1.3.*

**Java/Spring Boot Implementation**

```java
@Service
@RequiredArgsConstructor
public class RegionalDataEncryptionService {{

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
"""

def gen_authentication(s):
    name = s['name']
    return f"""### Authentication and Authorization

**What it means**

Authentication and Authorization (AuthN/AuthZ) in {{name}} control who can access the system and what they can do. Authentication verifies identity; authorization determines permissions. In a multi-region system, auth must work across regions while respecting data residency — a user authenticated in one region should not have their auth tokens or session data replicated to regions where it's not permitted.

**Why it matters**

{{s['main_challenge']}} requires that auth be both global (users can access from any region) and compliant (auth data respects residency). A centralized auth service would become a cross-region bottleneck and potential compliance violation.

**How it works**

**Authentication (who are you?)**:
- **OIDC/SAML with regional endpoints**: Users authenticate through their home region's identity provider endpoint. The region returns a JWT signed by a regional signing key. Tokens are NOT replicated cross-region.
- **mTLS for service-to-service**: Internal services authenticate each other using mutual TLS certificates issued by a per-region CA. No shared secrets cross regions.
- **Token format**: JWT with claims including `iss` (region URL), `sub` (user ID), `home_region` (user's legal region), `exp` (expiry).

**Authorization (what can you do?)**:
- **RBAC (Role-Based Access Control)**: Users are assigned roles (e.g., `region_admin`, `auditor`, `viewer`) per region. Roles are stored in the regional DB and cached locally.
- **ABAC (Attribute-Based Access Control)**: Fine-grained permissions based on attributes (`home_region == request_region AND role == admin`).
- **Region-scoped enforcement**: The authorization service checks both the user's role and whether the requested action violates region boundaries. E.g., an EU admin cannot access US restricted data even if they have the `admin` role.

```mermaid
sequenceDiagram
    participant User as User (Browser)
    participant Edge as Edge Router (Home Region)
    participant Auth as Regional Auth Service
    participant App as App Server
    
    User->>Edge: HTTPS request + cookie
    Edge->>Auth: validate JWT (regional key)
    Auth-->>Edge: valid + claims (home_region, roles)
    Edge->>App: forward + claims
    App->>App: enforce RBAC + region boundary
    App-->>User: response
```

*Authentication and authorization flow: the user connects to their home region's edge. The edge router validates the JWT using the regional signing key and forwards the claims to the app server, which enforces RBAC and checks that the requested data respects the region boundary.*

**Token lifecycle**:
- Tokens are short-lived (15-minute JWT + 1-hour refresh).
- Refresh tokens are region-scoped and never leave the home region.
- Session state is stored in the home region's Redis, not replicated cross-region.

**Java/Spring Boot Implementation**

```java
@Service
@RequiredArgsConstructor
public class RegionalAuthorizationService {{

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
    private final RegionalAuthorizationService authService;

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
"""

def gen_security_threats(s):
    name = s['name']
    return f"""### Security Threats and Mitigations

**Threat model**

The STRIDE threat model for {{name}} identifies the following primary risks:

| Threat | Description | Mitigation |
|---|---|---|
| **Spoofing** | Attacker impersonates a legitimate user or service | Regional JWT signing keys, mTLS for service-to-service auth |
| **Tampering** | Modification of data in transit or at rest | TLS 1.3 for transport, signed tokens, checksum validation |
| **Repudiation** | Actions performed without audit trail | Immutable audit logs, request ID tracing across services |
| **Information Disclosure** | {{s['restricted']}} exposed to unauthorized parties | Field-level encryption, region-scoped access control, data classification |
| **Denial of Service** | Flooding requests to exhaust resources | Rate limiting at edge, auto-scaling, WAF rules |
| **Elevation of Privilege** | Unauthorized access escalation | RBAC with least privilege, region boundary enforcement |

**Common attacks and mitigations**

**Data exfiltration across regions**: An attacker with access to the {{s['non_restricted']}} global index might attempt to extract {{s['restricted']}} data. *Mitigation*: strict data classification — only explicitly non-restricted fields are indexed globally; all other data stays in-region. Network policies enforce no cross-region data transfer for restricted data.

**Token replay**: An attacker steals a JWT and replays it. *Mitigation*: short-lived tokens (15 min), refresh token rotation, token binding (token tied to TLS session), and regional token validation.

**DDoS at the edge**: Attackers flood the edge router with requests. *Mitigation*: CloudFlare/AWS Shield DDoS protection, rate limiting per IP/ASN, challenge-response (CAPTCHA) for suspicious traffic, auto-scaling to absorb burst traffic.

**Cross-site scripting (XSS)**: Attackers inject scripts in user-generated content. *Mitigation*: sanitize all user content (OWASP HTML Sanitizer), Content-Security-Policy headers, HttpOnly cookies, output encoding.

**Privilege escalation**: An authenticated user attempts to access another region's data. *Mitigation*: region-scoped RBAC, ABAC checks (`home_region == request_region`), audit logging of all cross-region access attempts.

**Insider threat**: A legitimate engineer accesses data beyond their clearance. *Mitigation*: least-privilege IAM, just-in-time access (no standing privileges), audit logging of all data access with user attribution.

**Compliance violation detection**: The system must prove data never crosses region boundaries. *Mitigation*: network flow logs, immutable audit trails, automated compliance scanning that alerts on any cross-region data transfer.

```mermaid
graph TD
    Attacker[Attacker] -->|try| Edge[Edge Router<br/>WAF + Rate Limiting]
    Edge -->|suspicious| WAF[Web Application Firewall]
    Edge -->|valid| App[App Server<br/>Home Region Only]
    App -->|check| Auth[Auth Service<br/>Regional RBAC+ABAC]
    Auth -->|allow| DB[(Regional DB<br/>Encrypted at Rest)]
    Auth -->|deny| Audit[Audit Log<br/>Immutable Trail]
    App -->|cross-region?| RegionCheck[Region Boundary<br/>Enforcer]
    RegionCheck -->|violation| Alert[Security Alert]
    RegionCheck -.->|allowed| GlobalIdx[(Global Index<br/>Non-restricted only)]
```

*Threat model: all traffic enters through edge routers with WAF and rate limiting. Authentication is region-scoped (RBAC + ABAC). Data access is logged immutably. Cross-region data transfer is blocked by a region boundary enforcer that only allows explicitly non-restricted data.*

**Interview Q&A**

- **Q: How do you prevent data exfiltration in a multi-region system?**
  **A:** Classify data as restricted vs non-restricted at the schema level. Only non-restricted data enters the global index. Enforce via field-level ACLs, network policies, and automated compliance scanners.

- **Q: What's the difference between RBAC and ABAC in this context?**
  **A:** RBAC assigns static roles (admin, viewer); ABAC evaluates attributes at request time (home_region == request_region). In a multi-region system, ABAC is essential for region-scoping.

"""

def gen_observability(s):
    name = s['name']
    # For log-system.md, this section is already covered by "Observability of the Log System"
    return f"""### Observability and Logging

**What it means**

Observability and Logging in {name} provide visibility into system behavior through metrics, logs, and traces. Observability lets operators understand why the system is behaving a certain way (not just that it's broken), while logging provides an auditable record of events and errors.

**Why it matters**

{s['main_challenge']}. Without proper observability, failures and performance degradation are detected reactively (by users), not proactively. In a multi-region system, observability must also respect data residency — logs containing {s['restricted']} must stay in-region.

**How it works**

**Metrics**: Prometheus-compatible metrics exported by each service (via Micrometer in Spring Boot). Key metrics:
- Request latency (P50/P95/P99), rate, error rate per endpoint
- Regional routing accuracy (how often users are correctly routed to home region)
- Cross-region data transfer volume (should be 0 for restricted data)
- Cache hit rate, DB query latency, Kafka consumer lag
- Compliance metrics (e.g., cross-region access violations, audit log completeness)

**Logs**: Structured logging (JSON) with correlation IDs. All log lines include:
- `trace_id` (unique per request, propagated across services)
- `span_id` (for distributed tracing)
- `region` (the region where the log was generated)
- `data_class` (restricted or non-restricted tag on the log entry)

Log agents ship to {', '.join(s['key_components'][:1])} which buffers in Kafka before storage in Elasticsearch. Restricted logs stay in regional ES clusters — no cross-region log shipping.

**Traces**: OpenTelemetry instrumentation traces request flows across services. In a multi-region system, traces help debug cross-region feature latency (e.g., global search query that fans out to multiple regions).

**Alerting**:
- Regional outage (5xx rate > 5% for 5 min) → page on-call
- Data residency violation (cross-region transfer detected) → immediate alert + auto-block
- Latency degradation (> 2x P95) → create incident ticket
- Kafka consumer lag > 10 min → scale consumers

```mermaid
graph TD
    App1[App Server EU] -- metrics --> PromEU[Prometheus EU]
    App2[App Server US] -- metrics --> PromUS[Prometheus US]
    PromEU --> Grafana[Global Grafana<br/>Read-only, no restricted data]
    PromUS --> Grafana
    App1 -.span.--> OTEL[OpenTelemetry Collector]
    App2 -.span.--> OTEL2[OpenTelemetry Collector 2]
    OTEL --> Tempo[Tempo (EU traces)]
    OTEL2 --> TempoUS[Tempo (US traces)]
    App1 - log -> Vector1[Vector/Log Agent (EU)]
    App2 - log -> Vector2[Vector/Log Agent (US)]
    Vector1 -> KafkaEU[Kafka (EU region)]
    Vector2 -> KafkaUS[Kafka (US region)]
    KafkaEU -> ESEU[Elasticsearch (EU only)]
    KafkaUS -> ESUS[Elasticsearch (US only)]
```

*Observability architecture: metrics are aggregated globally (Prometheus + Grafana, no restricted data in dashboards). Traces are region-scoped (Tempo). Logs stay in-region (Vector → Kafka → Elasticsearch, never cross regions). All components export structured logs with trace IDs for correlation.*

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
"""

# ---- Main ----

def insert_sections(filename, sections_content):
    filepath = os.path.join(ADVANCED_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the Java section and insert before it
    java_marker = '### Java and Spring Boot Implementation Guide'
    idx = content.find(java_marker)
    if idx == -1:
        print(f"ERROR: Cannot find Java section in {{filename}}")
        return False

    # Find the start of the line before Java
    # Go back to the end of the previous section
    before_java = content[:idx]
    
    # Find the blank line(s) before Java section
    # We want to insert after the last content line and before \n\n### Java
    # The pattern is usually: ...content\n\n### Java
    insert_point = before_java.rstrip() + '\n\n'
    new_content = insert_point + sections_content + content[idx:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def regenerate_topics_covered(filename):
    """Re-read the file and regenerate Topics Covered to include all ### sections."""
    filepath = os.path.join(ADVANCED_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract all ### headings (exclude Topics Covered itself)
    headings = []
    for line in content.splitlines():
        m = re.match(r'^###\s+(.+)', line)
        if m:
            text = m.group(1).strip()
            if text.lower() != 'topics covered':
                headings.append(text)

    if not headings:
        print(f"  WARNING: No ### headings found in {{filename}}")
        return

    # Generate new Topics Covered
    topics_lines = []
    for i, h in enumerate(headings, 1):
        slug = re.sub(r'[^\w\s-]', '', h.lower()).strip()
        slug = re.sub(r'[\s]+', '-', slug)
        slug = re.sub(r'-+', '-', slug).strip('-')
        topics_lines.append(f"{{i}}. [{{h}}](#{{slug}})")
    topics_covered = "\n".join(topics_lines)

    # Find the Topics Covered section and replace its content
    tc_start = content.find('### Topics Covered')
    if tc_start == -1:
        print(f"  WARNING: No Topics Covered found in {{filename}}")
        return

    # Find end: next --- separator or next ### heading
    tc_end_match = re.search(r'\n\n---\n', content[tc_start:])
    if tc_end_match:
        tc_end = tc_start + tc_end_match.start()
    else:
        next_section = content.find('\n### ', tc_start + 20)
        if next_section == -1:
            tc_end = len(content)
        else:
            tc_end = next_section

    new_tc = f"### Topics Covered\n\n{{topics_covered}}\n\n---\n"
    content = content[:tc_start] + new_tc + content[tc_end:].lstrip("\n")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Regenerated Topics Covered: {{len(headings)}} items")

def gen_data_model_and_api(s, fname):
    """Generate the Data Model and API section. Content is specific to the file."""
    name = s['name']
    if "multiplayer" in fname:
        return f"""### Data Model and API

**What it means**

The **Data Model and API** section describes the entities that {{name}} tracks, the relationships between them, and the API contract that services and clients use to interact with the system. For a {{name.lower()}}, the data model must capture stateful entities (players, matches, game objects) and the API must support both real-time WebSocket messages and REST operations.

**Why it matters**

{{s['brief']}}. The data model defines how state is serialized, synchronized, and recovered after failure. The API contract defines how clients interact with the authoritative server and how regions communicate for cross-region features. Getting either wrong creates inconsistency, scalability bottlenecks, or client incompatibility.

**How it works**

**Entities and relationships**:

```mermaid
erDiagram
    PLAYER {{
      string playerId PK "Unique player identifier"
      string username "Player display name"
      string homeRegion "Legal region (GDPR, DPDP)"
      int mmr "Matchmaking rating"
      string currentMatchId FK "Match player is in"
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

*Entity relationship diagram: each Player belongs to a home region and can join one active Match at a time. Each Match contains many Game Objects (players, projectiles, pickups). The matchId links Players to their current Match; the regionId on Match determines where the match is hosted.*

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

**Log entry schema**:

```mermaid
erDiagram
    LOG_ENTRY {{
      string logId PK "Unique per log line (hash)"
      datetime timestamp "ISO 8601, UTC"
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

*Log entry schema: each log line is a LOG_ENTRY with a unique ID, timestamp, service name, distributed tracing context, and structured metadata. A boolean piiFlag marks entries containing restricted data — these are masked before storage in the global index, and the raw version is only retained in-region.*

**Index structure**: Logs are indexed by `timestamp` (primary sort key for time-range queries), `service` (for service-level views), `level` (for filtering), and `traceId` (for distributed tracing correlation). Text fields are analyzed with an inverted index for full-text search; numeric fields use BKD trees for range queries.

**API contract**:

1. **Ingest API** (agent → collector):
   - `POST /api/v1/logs/batch` — bulk insert log entries (JSON array)
   - `PUT /api/v1/logs/raw` — stream raw log lines (protobuf/gzip)
   - Headers: `X-Region`, `X-Trace-Id`, `Content-Encoding: gzip`

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
        # Generic fallback for files that need Data Model and API
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

**Real-world implementations**

- **Netflix**: Uses GraphQL for some services, REST for others; schema-first API design.
- **Spotify**: Backend for Frontend (BFF) pattern with per-client API views.
- **Airbnb**: GraphQL for flexible querying; REST for critical paths.

"""

# ---- Process each system ----

FILES_TO_ENHANCE = [
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

for fname in FILES_TO_ENHANCE:
    s = get_system_data(fname)
    if s is None:
        print(f"ERROR: No system data for {fname}")
        continue
    
    # Determine which sections to add
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
        # Add Data Model and API for these files
        sections.insert(0, gen_data_model_and_api(s, fname))
    
    sections_content = "\n\n".join(s.rstrip() for s in sections) + "\n\n"
    
    print(f"Processing {fname}...")
    success = insert_sections(fname, sections_content)
    if success:
        regenerate_topics_covered(fname)
        # Count lines
        filepath = os.path.join(ADVANCED_DIR, fname)
        with open(filepath, 'r', encoding='utf-8') as f:
            line_count = len(f.readlines())
        print(f"  Done. Total lines: {line_count}")
    else:
        print(f"  FAILED")

