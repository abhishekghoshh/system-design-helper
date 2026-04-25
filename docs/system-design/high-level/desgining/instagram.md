# Design Instagram

## Blogs and websites


## Medium


## Youtube


## Theory

### Problem Statement
Design a photo and video sharing social platform like Instagram supporting uploads, feed, stories, reels, explore, likes, comments, and direct messaging at scale.

### Functional Requirements
- Upload photos/videos with captions and filters
- Follow/unfollow users
- News feed (posts from followed users)
- Stories (24-hour ephemeral content)
- Reels (short-form video)
- Like, comment, share, save posts
- Explore/discover page
- Direct messaging
- Search (users, hashtags, locations)

### Non-Functional Requirements
- **Scale**: 500M+ DAU, 100M+ photos uploaded daily
- **Latency**: Feed loads < 200ms
- **Storage**: Petabytes of media
- **Availability**: 99.99%
- **Consistency**: Eventual for feed/likes, strong for follow graph

### High-Level Architecture

```
┌──────────┐     ┌──────┐     ┌──────────────────────────────┐
│  Mobile  │────▶│  CDN │     │       Service Layer           │
│  App     │     └──┬───┘     │                               │
└────┬─────┘        │         │  ┌──────────┐ ┌────────────┐  │
     │              │         │  │ Post Svc  │ │ Feed Svc   │  │
     ▼              │         │  ├──────────┤ ├────────────┤  │
┌──────────┐        │         │  │ User Svc  │ │ Story Svc  │  │
│  API GW  │────────┼────────▶│  ├──────────┤ ├────────────┤  │
└──────────┘        │         │  │ Media Svc │ │ Search Svc │  │
                    │         │  └─────┬────┘ └─────┬──────┘  │
                    │         └────────┼────────────┼──────────┘
                    │                  │            │
              ┌─────▼─────┐    ┌──────▼───┐  ┌────▼──────┐
              │   Object  │    │ Database │  │ Search    │
              │   Store   │    │ Cluster  │  │ (Elastic) │
              │  (S3)     │    └──────────┘  └───────────┘
              └───────────┘
```

### Media Upload Pipeline

```
Client → Upload Service → S3 (original)
                              │
                              ▼
                    ┌─────────────────┐
                    │  Media Pipeline  │
                    │  (async)         │
                    │  - Resize        │
                    │  - Thumbnails    │
                    │  - Apply filters │
                    │  - Video transcode│
                    │  - Content mod   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  CDN (multiple  │
                    │  resolutions)   │
                    └─────────────────┘
```

### Feed Generation

**Hybrid fan-out (same as Facebook approach):**
- Regular users (< 50K followers): Fan-out on write → push to followers' feed cache
- Celebrities (50K+ followers): Fan-out on read → merge at query time

```
Feed = merge(
  pre_computed_feed_from_cache,    // pushed by regular friends
  pull_celebrity_posts_on_demand,  // pulled at read time
  sponsored_posts                  // ad injection
)
→ Rank by ML model → Return top N
```

### Data Model

```
Users:     id, username, bio, profile_pic, follower_count, following_count
Posts:     id, user_id, media_urls[], caption, location, created_at
Stories:   id, user_id, media_url, expires_at, created_at
Follows:   follower_id, following_id, created_at
Likes:     post_id, user_id, created_at
Comments:  id, post_id, user_id, text, created_at
```

**Storage choices:**
| Data | Store | Reason |
|------|-------|--------|
| User profiles | PostgreSQL | Relational, ACID |
| Posts metadata | PostgreSQL + Cache | Read-heavy, cacheable |
| Follow graph | Graph DB / Cassandra | High fan-out queries |
| Feed cache | Redis | Fast reads, TTL support |
| Media files | S3 + CDN | Cheap, globally distributed |
| Search index | Elasticsearch | Full-text search |

### Stories Architecture

```
Stories expire after 24 hours:
- Write: Store in Redis with TTL=24h + persist to Cassandra
- Read: Fetch active stories from Redis (fast)
- Cleanup: Cassandra TTL auto-deletes expired stories
- Viewing order: Ranked by recency + engagement + closeness
```

### Scaling Considerations
- **Media**: S3 (unlimited scale) + multi-region CDN
- **Database**: Shard by user_id
- **Feed cache**: Partitioned Redis cluster
- **Upload processing**: Auto-scaling worker fleet (Lambda/K8s)
- **Search**: Elasticsearch cluster with sharded indices
