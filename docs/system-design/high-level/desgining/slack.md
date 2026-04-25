# Design Slack

## Blogs and websites


## Medium


## Youtube


## Theory

### Problem Statement
Design a team messaging platform like Slack that supports real-time messaging in channels and DMs, file sharing, threads, search, and integrations at enterprise scale.

### Functional Requirements
- Workspaces with channels (public/private) and direct messages
- Real-time messaging (text, emoji, reactions)
- Threaded replies
- File/image sharing
- Message search (full-text)
- User presence (online/away/DND)
- Notifications (push, email, desktop)
- Message editing and deletion
- Integrations and bots (webhooks, slash commands)

### Non-Functional Requirements
- **Latency**: Message delivery < 200ms
- **Scale**: 10M+ concurrent users, 1B+ messages/day
- **Availability**: 99.99%
- **Storage**: Petabytes of messages and files
- **Ordering**: Messages must appear in correct order per channel
- **Sync**: Seamless across mobile, desktop, web

### High-Level Architecture

```
┌──────────┐     WebSocket      ┌────────────────────────────────┐
│  Client  │◀══════════════════▶│       Gateway Service           │
│  (Web/   │                    │  (WebSocket connection manager) │
│  Mobile) │                    └────────────┬───────────────────┘
└──────────┘                                 │
                                             ▼
                              ┌──────────────────────────────┐
                              │       Service Layer           │
                              │                               │
                              │  ┌─────────────────────────┐  │
                              │  │ Channel Service          │  │
                              │  │ Message Service          │  │
                              │  │ Presence Service         │  │
                              │  │ Search Service           │  │
                              │  │ File Service             │  │
                              │  │ Notification Service     │  │
                              │  └──────────┬──────────────┘  │
                              └─────────────┼─────────────────┘
                                            │
                        ┌───────────────────┼───────────────────┐
                        ▼                   ▼                   ▼
                 ┌────────────┐      ┌────────────┐     ┌────────────┐
                 │ Message DB │      │ Search     │     │  File      │
                 │ (Vitess/   │      │ (Elastic-  │     │  Store     │
                 │  CockroachDB)│    │  search)   │     │  (S3)      │
                 └────────────┘      └────────────┘     └────────────┘
```

### Real-Time Message Delivery

```
Send message flow:
  1. Client sends message via WebSocket → Gateway
  2. Gateway → Message Service
  3. Message Service:
     a. Validate (permissions, rate limit)
     b. Persist to Message DB
     c. Publish to channel's Kafka topic
  4. Gateway subscribes to channels for all connected users
  5. Gateway pushes message to all online members via WebSocket
  6. Offline members → queue for push notification

Channel subscription model:
  Each Gateway server maintains:
    channel_id → Set<connection_ids>
  
  On message publish:
    → Kafka consumer on each Gateway server
    → Check local connections for that channel
    → Push to matching WebSocket connections
```

### Message Storage & Ordering

```
Schema (sharded by workspace_id):
  messages:
    id (Snowflake ID — time-ordered)
    channel_id
    thread_ts (nullable — for threaded replies)
    user_id
    content (text)
    attachments (JSON array)
    edited_at
    created_at

Ordering: Snowflake IDs ensure global time ordering
  → No need for sequence numbers per channel
  → ID = timestamp(41 bits) + worker(10 bits) + sequence(12 bits)

Pagination: Load messages by channel_id + cursor (message_id)
  → "Load more" fetches older messages
```

### Presence System

```
User states: online, away, DND, offline

Heartbeat approach:
  - Client sends heartbeat every 30 seconds via WebSocket
  - Presence Service updates Redis: user_id → {status, last_seen}
  - If no heartbeat for 60s → mark as away
  - If no heartbeat for 5min → mark as offline

Broadcasting presence:
  - Don't broadcast to entire workspace (too expensive)
  - Only broadcast to users who have the "away" user visible
  - Client requests presence for visible users in sidebar
  - Subscribe to presence changes for those users only
```

### Search

```
Messages → Kafka → Elasticsearch indexing pipeline

Index fields:
  - content (full-text, analyzed)
  - channel_id (filter)
  - user_id (filter)
  - workspace_id (routing key for sharding)
  - timestamp (sort/filter)
  - file names and content (attachments)

Query: "deployment failed" in:#engineering from:@alice
  → Parse into structured query
  → ES query with filters + full-text match
  → Return ranked results with context snippets
```

### Key Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Transport | WebSocket (persistent connections) | Real-time bidirectional |
| Message ordering | Snowflake IDs | Time-ordered, globally unique |
| Message bus | Kafka (topic per channel group) | Decouple producers/consumers |
| DB | Vitess (sharded MySQL) | Proven at Slack's scale |
| Search | Elasticsearch | Full-text + filters |
| Presence | Redis + heartbeat | Fast reads, ephemeral data |
| Files | S3 + CDN | Cost-effective, global delivery |

### Scaling Considerations
- **Gateway**: Horizontally scale WebSocket servers, sticky by user
- **Message DB**: Shard by workspace_id (all channels in a workspace co-located)
- **Kafka**: Partition by channel_id for ordering guarantees
- **Search**: Shard ES by workspace_id, replicate for read scale
- **Large channels**: Channels with 10K+ members → fan-out via Kafka, not WebSocket broadcast
