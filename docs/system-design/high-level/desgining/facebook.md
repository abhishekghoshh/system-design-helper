# Design Facebook

## Blogs and websites

## Medium

## Youtube

## Theory

### Problem Statement
Design a social networking platform like Facebook that supports user profiles, friend connections, news feed, posts, reactions, comments, groups, and messaging at billion-user scale.

### Functional Requirements
- User registration, profiles, and friend management
- Create posts (text, images, videos)
- News feed with personalized ranking
- Reactions, comments, and shares
- Groups and pages
- Real-time notifications
- Search (people, posts, groups)

### Non-Functional Requirements
- **Scale**: 2B+ DAU, 100K+ QPS for feed
- **Latency**: Feed loads < 200ms, post creation < 500ms
- **Availability**: 99.99%
- **Consistency**: Eventual for feed, strong for friend graph

### High-Level Architecture

```
┌──────────┐     ┌──────────────┐     ┌─────────────────────┐
│  Client  │────▶│   API GW /   │────▶│  Service Layer       │
│  (App/   │     │   Load       │     │                      │
│   Web)   │◀────│   Balancer   │◀────│  ┌────────────────┐  │
└──────────┘     └──────────────┘     │  │ User Service    │  │
                                      │  │ Post Service    │  │
       ┌──────────────────────────────│  │ Feed Service    │  │
       │  CDN (images, videos, static)│  │ Graph Service   │  │
       │                              │  │ Search Service  │  │
       ▼                              │  │ Notification Svc│  │
  ┌─────────┐                         │  └────────┬───────┘  │
  │  Blob   │                         └───────────┼──────────┘
  │ Storage │                                     │
  └─────────┘                          ┌──────────┼──────────┐
                                       ▼          ▼          ▼
                                 ┌──────────┐ ┌───────┐ ┌────────┐
                                 │ Social   │ │ Post  │ │ Feed   │
                                 │ Graph DB │ │ Store │ │ Cache  │
                                 │ (TAO)   │ │       │ │        │
                                 └──────────┘ └───────┘ └────────┘
```

### News Feed Design

**Two approaches:**

**1. Fan-out on Write (Push model):**
```
User posts → Write to all followers' feed caches
Pro: Fast reads (pre-computed feed)
Con: Celebrity problem (1M+ followers = 1M writes)
```

**2. Fan-out on Read (Pull model):**
```
User requests feed → Query all friends' posts → Rank → Return
Pro: No write amplification
Con: Slow reads, high compute at read time
```

**Hybrid approach (Facebook's model):**
- Push for regular users (< 10K friends)
- Pull for celebrities/pages (millions of followers)
- Pre-compute + merge at read time

**Feed Ranking:**
```
Score = f(affinity, edge_weight, time_decay, engagement_prediction)

affinity:              How close is the poster to the viewer?
edge_weight:           Type of content (video > photo > text)
time_decay:            How recent is the post?
engagement_prediction: ML model predicting interaction probability
```

### Social Graph Storage

```
User A ──friend──▶ User B
       ──follows──▶ Page X
       ──member──▶ Group Y

Storage: TAO (Facebook's graph store)
- Adjacency list per node
- Bidirectional edges for friends
- Sharded by user_id
- Cached in distributed memory cache
```

### Key Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Feed storage | Cache (Memcached/Redis) + MySQL | Fast reads, persistent backup |
| Social graph | Custom graph DB (TAO) | Optimized for edge queries |
| Media storage | Blob store + CDN | Cost-effective, globally distributed |
| Feed ranking | ML-based scoring | Personalization drives engagement |
| Consistency | Eventual (feed), Strong (graph mutations) | Acceptable trade-off |

### Scaling Strategies
- **Sharding**: User-based sharding for profile/post data
- **Caching**: Multi-layer (L1 local, L2 regional, L3 global)
- **CDN**: Static assets + video streaming
- **Async processing**: Post fanout via message queues
- **Read replicas**: Heavy read workload on feed
