# Design a Chat System

## Blogs and websites

## Medium

## Youtube

- [Build Scaleable Realtime Chat App with NextJS and NodeJS Tutorial](https://www.youtube.com/watch?v=CQQc8QyIGl0)
- [Build Scaleable Realtime Chat App with Kafka and Postgresql](https://www.youtube.com/watch?v=Rat7ORbBDN8)

- [FAANG System Design Interview: Design A Chat System (WhatsApp, Facebook Messenger, Discord, Slack)](https://www.youtube.com/watch?v=okrR1KXNLtA)


- [How WhatsApp Knows You're Online Right Now (Redis Internals)](https://www.youtube.com/watch?v=zcbVrwS8_Ow)

### Whatspp

- [Whatsapp System Design | System Design Chat application | System design of Whatsapp application](https://www.youtube.com/watch?v=a8KUKOh3YXk)

---

## Theory

A chat system (WhatsApp, Messenger, Slack, Discord) delivers messages between users in **near real time**, durably stores conversation history, synchronizes state across a user's devices, and tracks presence — at billions-of-connections scale. The core architectural challenge is maintaining millions of **long-lived persistent connections** and routing messages to whichever server currently holds each recipient's connection, while guaranteeing delivery despite disconnects.

### Important Subtopics

1. Requirements: 1:1 chat, group chat, online/offline/typing indicators, read receipts, delivery guarantees
2. Transport choices: WebSocket vs SSE vs long polling vs gRPC streams
3. Connection management at scale (C10M problem)
4. Message routing: session service / connection registry
5. Message fan-out for groups (fan-out-on-write vs on-read)
6. Delivery semantics: at-least-once, deduplication, ordering per conversation
7. Offline storage and sync (inbox model, cursors)
8. Presence tracking (heartbeat-based, privacy controls)
9. Message store selection (wide-column vs KV vs relational)
10. End-to-end encryption basics (Signal protocol concepts)
11. Push notifications when disconnected
12. Media attachments pipeline
13. Group membership & permission models
14. Multi-device consistency

### Requirements & Scale Estimation

**Functional**: 1:1 text chat; group chats; media sharing; delivery/read receipts; typing indicator; online presence; message history; search (nice-to-have); push when offline.

**Non-functional**: end-to-end latency < 500 ms; ordering guaranteed *per conversation* (not globally); availability > 99.99%; durability — a sent message must never be lost; scale ~500M DAU, ~50 msg/user/day → ~25B msgs/day ≈ ~300K msgs/s average, several × peak.

**Key insight**: the connection tier (long-lived sockets) is the hardest scaling problem — each server holds tens of thousands of open connections; routing requires knowing which server holds whom.

### Transport Options

| Protocol | Direction | Pros | Cons | Used by |
|---|---|---|---|---|
| WebSocket | Full duplex | True realtime, single TCP conn, low overhead | Server must hold conn state; LB complexity | WhatsApp/Messenger class |
| SSE | Server→client only + separate POSTs | Simplicity, HTTP-native, auto-reconnect | No native upstream channel; HTTP/1.1 6-conn limit | Notification-heavy apps |
| Long polling | Emulated duplex | Works everywhere incl. ancient proxies | High overhead, latency spikes | Legacy fallback |
| gRPC bidirectional streaming | Full duplex | Efficient binary, strong contracts | Browser support needs grpc-web proxies | Internal/mobile heavy systems |

Production mobile apps typically use WebSocket with aggressive keepalive tuning plus OS-level push (APNs/FCM) as the offline fallback — battery constraints forbid naive sockets on iOS background.

### Connection Registry (Who Is Where)

The heart of routing: a mapping `userId → {serverId, deviceId[]}` updated as clients connect/disconnect.

- Redis cluster keyed `conn:{userId}` → set of gateway nodes serving that user's devices, TTL-refreshed by heartbeats (~30 s) so crashed gateways auto-expire.
- Gateways register on connect, deregister (or let TTL lapse) on disconnect.
- Senders look up recipients here before dispatching downstream frames.

### Fan-Out Strategies for Groups

For a message to group G:

- **Fan-out-on-write**: deliver copies to every member's inbox/connection at send time. Fast reads (everything pre-delivered); expensive for celebrity-sized groups (one message = 100K deliveries).
- **Fan-out-on-read**: store once; members pull when they open the app. Cheap writes; slow cold opens; needed for very large groups/channels (Discord channels, Telegram megagroups).
- Hybrid (industry standard): small groups (<~100) fan out on write; large groups/channels mark the message available and rely on read-path sync + unread counters.

### Delivery Semantics

- Sender → server: client retries with client-generated `msgId` (UUID); server dedupes.
- Server → recipient: at-least-once over the socket; client dedupes by `msgId`.
- Ordering: monotonic per-conversation sequence number assigned by the conversation's home partition — clients order by `(conversationId, seq)`; cross-conversation ordering is meaningless by design.
- Acknowledgment ladder: `sent → delivered (device acked) → seen (user-visible)` — receipts are themselves lightweight messages.

### Presence

Heartbeats update `presence:{userId}` (online/last-seen). Typing indicators are ephemeral events — never persisted, routed directly over active connections, dropped silently if recipient offline.

### Storage Model

Per-conversation partitioned log of immutable messages + per-user inbox pointers:

```mermaid
erDiagram
    CONVERSATION ||--o{ MESSAGE : contains
    USER ||--o{ PARTICIPANT : joins
    PARTICIPANT }o--|| CONVERSATION : member-of
    USER ||--o{ USER_CONVERSATION_STATE : tracks
    USER_CONVERSATION_STATE }o--|| CONVERSATION : "unread cursor"

    CONVERSATION {
        uuid id PK
        enum type
        int seq_counter
    }
    MESSAGE {
        uuid conv_id PK,FK
        bigint seq PK
        uuid sender_id FK
        string body_ciphertext
        timestamptz created_at
    }
    USER_CONVERSATION_STATE {
        uuid user_id PK,FK
        uuid conv_id PK,FK
        bigint last_read_seq
    }
```

Wide-column/Cassandra-style storage fits naturally (partition = conversation, clustering = seq), giving O(1) appends and efficient range reads for history scroll-back.

---

## Characteristics

- **Persistent connection-centric**: capacity planned in concurrent sockets, not QPS; gateway fleet sized by memory/file-descriptor budgets per node.
- **Asynchronous by nature**: sender success ≠ receiver read; the system bridges arbitrary device states via durable queues.
- **Per-conversation ordering, global concurrency**: strict total order across all conversations is neither needed nor affordable; per-partition sequences suffice.
- **At-least-once + idempotency**: retries everywhere; duplicates eliminated by client-generated IDs rather than expensive exactly-once machinery.
- **Presence is best-effort**: staleness acceptable (last-seen timestamps); never block message flow on presence accuracy.
- **Offline-first UX**: the app must feel instant regardless of connectivity; local DB + sync protocol do the illusion work.
- **Privacy-preserving options**: E2E encryption shifts trust from servers to endpoints; servers route ciphertext they cannot read (metadata remains visible unless mitigated).

---

## Components

- **Gateway / Connection layer**
  *Purpose*: terminate WebSockets/SSE at massive concurrency. *Responsibilities*: handshake/auth on connect, heartbeat tracking, frame encode/decode, backpressure, reconnection handling, forwarding downstream frames to its attached clients. *Relationship*: front tier; talks to routers/services via internal bus or RPC. *Example*: Netty/Erlang-based fleets; Discord's Elixir/gateway architecture.

- **Session/Connection registry**
  *Purpose*: userId → gateway map. *Responsibilities*: TTL bookkeeping, multi-device entries, lookup API for senders. *Example*: Redis cluster with heartbeat refresh (see Theory).

- **Chat/message service**
  *Purpose*: accept messages, assign sequence numbers, persist, trigger fan-out. *Responsibilities*: validation, dedupe, ordering per conversation, write to store + event bus atomically (outbox), handle group fan-out policy. *Relationship*: brain of the write path.

- **Message store**
  *Purpose*: durable conversation logs. *Responsibilities*: append-only writes, range queries for history, TTL/archival policies. *Example*: Cassandra/DynamoDB/HBase; ScyllaDB at Discord scale (see their Trillion Messages posts).

- **Fan-out workers**
  *Purpose*: translate "message persisted" events into per-recipient deliveries. *Responsibilities*: resolve online devices via registry, push frames to gateways, enqueue pushes for offline users, maintain inbox/unread structures. *Example*: Kafka consumers doing the write-side fan-out.

- **Push notification service**
  *Purpose*: reach users with no live connection via APNs/FCM. *Responsibilities*: payload crafting (metadata-only if E2E), rate limiting, receipt tracking. *Example*: every mobile chat ships this; silent pushes also wake apps to sync.

- **Media/blob service**
  *Purpose*: attachment upload/download. *Responsibilities*: presigned uploads, thumbnailing, AV scanning, CDN delivery. *Example*: S3 + CloudFront behind short-TTL signed URLs.

- **Presence service**
  *Purpose*: online status + last-seen. *Responsibilities*: heartbeat ingestion (batched), subscription fanout to interested parties, privacy filtering (nobody/hide-last-seen settings).

```mermaid
flowchart LR
    A[Client A] <-->|WS| GA[Gateway A]
    B[Client B] <-->|WS| GB[Gateway B]
    GA -->|send msg| CS[Chat svc]
    CS --> ST[(Message store)]
    CS --> OB[[Kafka - outbox]]
    OB --> FO[Fan-out workers]
    FO --> REG[(Connection registry)]
    REG -.lookup.-> FO
    FO -->|deliver| GB
    FO -->|offline| PUSH[APNs/FCM]
    FO --> INBOX[(Unread/inbox state)]
    PR[Presence svc] <--> GA
    PR <--> GB
```

---

## Patterns

- **Sticky long connections + registry routing**
  *Problem*: any-to-any message delivery across a dynamic fleet. *How*: registry maps users→gateways; senders/routers consult it. *When*: any socket-based system. *Pros*: direct downstream push, minimal latency. *Cons*: registry is hot — cache aggressively, batch lookups.

- **Transactional outbox**
  *Problem*: persisting the message AND publishing the fan-out event must be atomic. *How*: both written in one DB transaction; relay ships rows to Kafka. *Why*: avoids lost fan-outs on partial failure. Universal pattern worth naming in interviews.

- **Hybrid fan-out** (described above): threshold-based strategy switch.

- **Sequence-number ordering**: conversation partitions own monotonically increasing seq (single-writer per partition makes this trivial); clients detect gaps and issue catch-up sync requests.

- **Sync protocol with cursors**: each device tracks `last_seq` per conversation; on reconnect asks "everything after X" — the same mechanism powers multi-device consistency and offline catch-up.

- **Ephemeral-vs-durable split**: typing/presence events ride direct routes and die with the connection; messages always traverse durable paths. Mixing these up causes either data loss or pointless persistence costs.

- **Backpressure-aware gateways**: bounded outbound buffers; slow consumers get queued to disk or pushed to offline mode instead of OOM-ing the gateway — classic production hardening detail interviewers love.

---

## Benefits

- **True realtime collaboration** unlocks product categories (support, gaming, trading floors).
- **Durability guarantees build trust** — "message sent" means it survives anything except user deletion.
- **Multi-device continuity** is achievable cleanly because state lives server-side with per-device cursors.
- **Elastic scale**: gateways and services scale horizontally; conversations shard naturally.
- **Event spine reuse**: the same Kafka backbone feeds analytics, moderation, ML features (spam detection) without touching the chat path.

---

## Pros

- Sub-second delivery worldwide with modest infra per message.
- Clean horizontal scaling story: shards by conversation, gateways by connections.
- At-least-once + dedup achieves effectively-once UX without exotic protocols.
- Rich feature surface (receipts, presence, reactions) composes atop one transport.

## Cons

- Gateway tier is operationally demanding: file-descriptor limits, GC pauses causing mass reconnect storms, deploy-time connection draining.
- Reconnection stampedes after network blips or deployments can melt registries (mitigate with jittered reconnects, rate-limited reauth).
- E2E encryption forfeits server-side search/moderation capabilities — product trade-off, not just tech.
- Group fan-out costs explode with size; hybrid logic adds code complexity.
- Multi-region presence/messaging introduces latency-vs-consistency decisions (home-region-per-user models).

---

## Challenges

- **Technical**: exactly-once *appearance* under at-least-once plumbing (dedupe windows, ID discipline); sequence-gap repair during partitions; clock skew affecting timestamps display.
- **Scalability**: C10M-class connection counts; Kafka partition hot spots from celebrity group traffic; registry write amplification during mass reconnects.
- **Performance**: p99 latency tail from GC pauses on gateway nodes (ZGC/Shenandoah or off-heap solutions); history pagination for decade-old conversations (index design + archival tiers).
- **Reliability**: regional failover for connections (clients auto-reconnect to healthy region; in-flight messages replayed from store); zero message loss through gateway crashes (ack only after durable persist).
- **Maintainability**: protocol evolution across billions of installed clients — versioned frame schemas, long deprecation tails.
- **Operational**: draining connections during deploys gracefully (send GOAWAY, stagger reconnects); capacity dashboards in connections-per-node terms.
- **Security**: spam/abuse at scale (ML classifiers on metadata+reports since content may be encrypted), phishing link protection, account takeover recovery flows, metadata minimization debates.

---

## Best Practices

- **Ack messages only after durable persistence** — client UI may show optimistic ticks but truth lives server-side.
- **Client-generated UUIDs on every message** — dedupe becomes trivial and retry-safe.
- **Heartbeats with jitter** (±20%) prevent synchronized thundering herds after network recovery.
- **Separate control plane (auth/presence/receipts) from data plane (messages)** — different scaling and failure profiles.
- **Bound everything**: outbound queues, fan-out batch sizes, registry entry TTLs — unbounded buffers are how chat gateways die.
- **Deploy with connection draining**: mark gateway unhealthy → wait N minutes → close with reconnect hints; combined with client exponential backoff+jitter.
- **Design unread counts as first-class state** (`USER_CONVERSATION_STATE.last_read_seq`) — cheap increments beat recount queries.
- **Encrypt in transit always (TLS); evaluate E2E honestly against product needs** (searchability, compliance, moderation duties).
- **Test with chaos**: kill random gateways under load; assert zero message loss and bounded reconnect storm amplitude.

---

## When to Use / Not Use

A bespoke chat backend suits products where messaging is core (marketplaces, telehealth, gaming social). Consider alternatives when:

- Standard business chat → embed Intercom/Stream/Twilio Conversations; building this is weeks of undifferentiated work.
- In-app community features → SDKs (Stream, PubNub) cover 90%.
- Pure broadcast updates → push notifications or SSE suffice; no need for full duplex.

Decision factors: differentiation value of messaging, scale trajectory, compliance/E2E requirements, team bandwidth, budget for the operational burden described above.

---

## Use Cases

- **WhatsApp-class consumer messenger**
  *Problem*: 2B users, E2EE, tiny per-message infrastructure budget. *Solution*: Erlang/OTP-ish connection fleets, Signal-protocol E2EE, sparse metadata storage, phone-number identity. *Trade-off*: no server-side search; backups become client-managed.

- **Slack-class workplace chat**
  *Problem*: deep history search, integrations, threads, enterprise compliance. *Solution*: plaintext-at-rest (with enterprise key management), powerful search indexes, webhook/bot APIs, retention policies. *Trade-off*: E2EE abandoned deliberately for functionality/compliance.

- **Discord-class community platform**
  *Problem*: million-member channels where fan-out-on-write would explode. *Solution*: fan-out-on-read channels + presence-light design + event-driven permission updates. *Trade-off*: slower cold-open sync for lurkers; massively cheaper writes.

---

## High-Level Design

End-to-end message journey:

```mermaid
sequenceDiagram
    participant SA as Sender App
    participant GS as Sender Gateway
    participant CS as Chat Service
    participant K as Kafka (outbox)
    participant ST as Message Store
    participant FO as Fan-out Worker
    participant RG as Registry
    participant GR as Recipient Gateway
    participant RA as Recipient App
    participant PN as Push Svc

    SA->>GS: SEND {convId, clientMsgId, ciphertext}
    GS->>CS: forward frame
    CS->>CS: auth, dedupe(clientMsgId), validate membership
    CS->>ST: append(convId, seq=next, msg)
    CS->>K: publish MessagePersisted (same txn via outbox relay)
    CS-->>SA: ACK {seq}  → sender shows single tick
    K->>FO: consume
    FO->>RG: where are recipients?
    alt recipient online
        RG-->>FO: gateway GR, deviceId
        FO->>GR: DELIVER {msg}
        GR->>RA: push frame
        RA-->>GR: ack → delivered tick propagates back
    else offline
        FO->>PN: notify(metadata)
        Note over PN: FCM/APNs wakes device; app syncs on open
    end
```

Scaling notes: chat-service stateless per request but owns per-conversation sequencing via partitioned writers (hash(convId)); Kafka partitions keyed convId preserve ordering into fan-out; gateways autoscale on connection count; registry = Redis Cluster sharded by userId.

Failure handling: gateway crash → clients reconnect (backoff+jitter), registry TTL expires ghost entries, undelivered-but-persisted messages picked up by device sync on reconnect; regional outage → DNS/anycast shift + clients' region fallback list; Kafka lag → deliveries delayed but never lost (store already committed).

---

## Deep Dive

- **Sequencing internals**: conversation hash → owning chat-service shard keeps `next_seq` in memory with WAL/fenced writes; replicas take over via Raft-group or by re-deriving from store max(seq) during failover fencing. Gap detection on clients triggers `/sync?after=seq`.
- **Dedupe window**: server keeps recent `(senderId, clientMsgId)` LRU per shard; older dupes rejected naturally by unique constraint `(conv_id, sender_id, client_msg_id)` in store — belt and suspenders.
- **Reconnect storm math**: 50K connections/node × 200-node fleet redeployed naively = 10M reconnect burst; fix = rolling drain (5% batches), client jitter 0–30 s, admission-rate-limited handshake tier. This arithmetic impresses interviewers more than any diagram.
- **E2EE overview (Signal-style)**: X3DH key agreement establishes shared secret; Double Ratchet advances keys per message (forward secrecy); servers relay opaque ciphertexts + minimal envelope. Implications: no server dedupe/ordering visibility beyond envelopes, receipts still possible via opaque acks.
- **Observability**: track delivery funnel (sent→persisted→fanned→delivered→seen) with per-stage histograms; alert on fan-out lag (Kafka offset age), registry error rates, per-gateway connection churn; synthetic 1:1 loops probing e2e latency per region continuously.

---

## Java and Spring Boot Implementation

Spring Boot supports WebSockets natively (STOMP) — below, a simplified gateway + service sketch showing the patterns in Java terms:

```java
@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {

    private final ChatHandshakeInterceptor authInterceptor;
    private final ChatFrameHandler chatFrameHandler;

    public WebSocketConfig(ChatHandshakeInterceptor authInterceptor,
                           ChatFrameHandler chatFrameHandler) {
        this.authInterceptor = authInterceptor;
        this.chatFrameHandler = chatFrameHandler;
    }

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(chatFrameHandler, "/ws/chat")
                .addInterceptors(authInterceptor)   // JWT validated at upgrade time
                .setAllowedOrigins("https://app.example.com");
    }
}
```

Connection registry + routing service:

```java
@Service
public class ConnectionRegistry {

    private final StringRedisTemplate redis;

    public ConnectionRegistry(StringRedisTemplate redis) { this.redis = redis; }

    public void register(String userId, String gatewayId, Duration ttl) {
        redis.opsForSet().add("conn:" + userId, gatewayId);
        redis.expire("conn:" + userId, ttl);
    }

    public Set<String> gatewaysFor(String userId) {
        return redis.opsForSet().members("conn:" + userId);
    }

    public void deregister(String userId, String gatewayId) {
        redis.opsForSet().remove("conn:" + userId, gatewayId);
    }
}

@Service
public class ChatService {

    private final ConversationRepository conversations;
    private final MessageRepository messages;
    private final ConnectionRegistry registry;
    private final GatewayDispatcher dispatcher;
    private final OutboxWriter outbox;

    @Transactional
    public long send(String convId, String senderId, String clientMsgId, String body) {
        if (messages.existsByConvIdAndSenderAndClientMsgId(convId, senderId, clientMsgId)) {
            return messages.findSeq(convId, senderId, clientMsgId); // idempotent retry
        }
        long seq = conversations.nextSeq(convId);   // row lock / atomic UPDATE
        messages.persist(new Message(convId, seq, senderId, clientMsgId, body));
        outbox.write(new MessagePersisted(convId, seq, senderId));
        return seq;
    }

    /** Called by fan-out workers after consuming the outbox stream. */
    public void fanOut(String convId, long seq, List<String> recipientIds) {
        for (String userId : recipientIds) {
            var gateways = registry.gatewaysFor(userId);
            if (gateways.isEmpty()) {
                pushNotifier.notifyAsync(userId, convId, seq);
            } else {
                dispatcher.deliver(gateways, userId, convId, seq);
            }
        }
    }
}
```

Controller for REST fallback (media, history):

```java
@RestController
@RequestMapping("/api/v1/conversations/{convId}/messages")
public class HistoryController {

    private final MessageRepository messages;

    @GetMapping
    Page<MessageDto> history(@PathVariable String convId,
                             @RequestParam(defaultValue = "0") long afterSeq,
                             @PageableDefault(size = 50) Pageable page,
                             Authentication who) {
        membershipChecker.assertMember(convId, who.getName());
        return messages.findByConvIdAfterSeqOrderBySeqAsc(convId, afterSeq, page);
    }
}
```

Notes: `@Transactional` covers message-row + outbox-row atomically (the relay publishes to Kafka separately — transactional outbox pattern); `nextSeq` uses `UPDATE ... SET seq = seq + 1 RETURNING seq` for atomic per-conversation ordering; production adds Netty-backed gateways (or spring-websocket with tuned containers), Resilience4j around push calls, and Testcontainers integration tests asserting dedupe + ordering under concurrent sends.

---

## Real-World Examples

- **WhatsApp** — famously ~450+ engineer team supporting billions: Erlang connection efficiency, Signal E2EE default-on, multimedia via encrypted blobs, minimal server metadata philosophy.
- **Facebook Messenger** — Haxl/Orc-style service mesh, hybrid fan-out, AI features (suggestions) riding the message pipe; documented their move to a unified infra with Instagram DMs.
- **Discord** — published extensively: Elixir gateway, ScyllaDB trillion-message storage, their 2023 outage postmortems teaching fan-out and data-tier lessons; Jitsi integration for voice.
- **Slack** — WebSocket RTM API evolution toward event-driven platform; enterprise grid multi-workspace identity federation.

---

## Interview Preparation

### Interview Questions

**Beginner**

1. **WebSocket vs HTTP polling for chat?**
   Polling wastes round-trips and adds latency proportional to poll interval; WebSocket gives persistent full-duplex channel with negligible per-message overhead — necessary for sub-second delivery at scale.
2. **How does a message reach an offline user?**
   Persist immediately (it's durable), then fire a push notification via APNs/FCM; when the user opens the app, the device syncs missed messages using its stored cursor.

**Intermediate**

3. **How do you guarantee message ordering?**
   Per-conversation sequence numbers assigned by the conversation's owning shard; clients order by that. Explicitly reject global ordering as unnecessary — cross-conversation interleaving is unobservable to users. Follow-up: what about ordering between two people typing simultaneously in a group? Same mechanism — server assigns final order at persist time.
4. **Design the connection registry. What breaks first at scale?**
   Redis set-per-user with heartbeat TTLs. First bottleneck: write amplification during mass reconnects — mitigate with batching pipelines, local gateway caching of its own sessions (registry consulted mainly for *other* users), longer TTLs with faster liveness checks done gateway-internally.
5. **Explain fan-out-on-write vs on-read with concrete thresholds.**
   ≤ ~100 members: on-write (precompute deliveries, fast opens). Beyond: on-read (single write, members pull + unread badges maintained incrementally). Numbers vary by product; the reasoning (write cost ∝ members vs read cost amortized) is what matters.

**Advanced**

6. **Walk through delivering a message exactly once to each device without distributed transactions.**
   At-least-once everywhere + idempotent receivers: clientMsgId dedupes sender retries; device-side dedup by msgId; ack-driven cursor advancement for redelivery suppression. Show awareness that true exactly-once delivery semantics is a myth without application-level idempotency — say it explicitly.
7. **A gateway deployment just disconnected 800K users. What happens and how do you survive it?**
   Storm anatomy: simultaneous reconnects overwhelm handshakes and registry writes. Survivors: rolling drains with GOAWAY + drain periods, client backoff with heavy jitter, handshake rate limiting/admission queues, registry batch pipelines, presence updates deferred until stable. Postmortem framing: measure storm half-life, tune constants empirically.

**Senior / system design**

8. **Design WhatsApp-scale chat with E2EE: what changes architecturally?**
   Servers become blind couriers: no content indexing/search/moderation server-side, receipts via opaque acks, media as encrypted blobs with content-addressed keys distributed via the message envelope, key verification UX, multi-device requires per-device curve negotiations. Metadata minimization choices (hide group membership? sealed sender?) discussed as product-policy trade-offs.
9. **Multi-region chat: how do you place conversations and users?**
   Home-region-per-conversation (latency follows geography of participants; cross-region convos pick midpoint or primary-participant home), registry globally replicated (eventually consistent OK — stale gateway hits fall back to store-sync path), DR posture: region loss = conversations homed there temporarily degraded, clients transparently sync from replicas. Trade-offs: cross-region writes for scattered groups vs pinning.

### Common Mistakes

- Global message ordering attempts (pointless, kills throughput).
- Persisting typing indicators or presence as durable events.
- Trusting TCP delivery — process crash after socket write but before disk write loses messages; ack-after-persist fixes it.
- Unbounded gateway buffers letting one slow client OOM a node serving 50K others.
- Forgetting dedupe and double-rendering messages after client retries.

### Expected discussion points

Delivery-semantics vocabulary precision (at-least-once vs effective-once), the economics of connection density (why Erlang/Netty dominate), fan-out threshold reasoning, reconnect-storm arithmetic, and honest E2EE trade-off analysis.
