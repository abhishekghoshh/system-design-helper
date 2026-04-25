# Design Text Storage Service like Pastebin

## Blogs and websites


## Medium


## Youtube


## Theory

### Problem Statement
Design a text storage and sharing service like Pastebin where users can store text snippets, get a unique URL, and share them. Supports optional expiration, syntax highlighting, and access control.

### Functional Requirements
- Create a paste (text content) and get a unique short URL
- Read a paste by URL
- Optional: set expiration time (1 hour, 1 day, 1 week, never)
- Optional: password-protect a paste
- Syntax highlighting for code
- User accounts (optional) to manage pastes
- API access for programmatic use

### Non-Functional Requirements
- **Scale**: 10M+ pastes/day, 100M+ reads/day (read-heavy 10:1)
- **Latency**: Create < 200ms, Read < 100ms
- **Availability**: 99.9%
- **Storage**: Text pastes (avg 10KB), retention based on TTL
- **Durability**: Pastes must not be lost before expiration

### High-Level Architecture

```
┌──────────┐     ┌──────────┐     ┌────────────────────────────┐
│  Client  │────▶│  API GW  │────▶│    Application Layer        │
│          │     └──────────┘     │                             │
└──────────┘                      │  ┌───────────────────────┐  │
                                  │  │ Paste Service          │  │
                                  │  │  - Create paste        │  │
                                  │  │  - Read paste          │  │
                                  │  │  - Generate short URL  │  │
                                  │  └──────────┬────────────┘  │
                                  └─────────────┼───────────────┘
                                                │
                                  ┌─────────────┼─────────────┐
                                  ▼                           ▼
                           ┌────────────┐             ┌────────────┐
                           │  Metadata  │             │  Content   │
                           │  DB        │             │  Store     │
                           │ (MySQL)    │             │ (S3/Blob)  │
                           └────────────┘             └────────────┘
```

### URL Generation

```
Short URL = Base62 encode of unique ID

Option 1: Auto-increment ID → Base62
  ID: 1000000 → Base62: "4c92"
  Pro: Simple, sequential
  Con: Predictable (security concern)

Option 2: Random 6-8 char string
  62^6 = 56 billion combinations
  Pro: Not guessable
  Con: Collision check needed

Option 3: Pre-generated key service
  Background service generates keys → stores in DB
  On paste creation → take next available key
  Pro: Fast, no collision, no computation at write time
```

### Data Model

```
pastes table:
  id (PK), short_url (unique), content_key (S3 path),
  user_id (nullable), title, language, 
  password_hash (nullable), expires_at (nullable),
  created_at, view_count

Storage split:
  Metadata (small): MySQL/PostgreSQL
  Content (large):  Object storage (S3)
    → Cheaper for large text blobs
    → Content-addressable for deduplication
```

### Read Path (Optimized)

```
Client → CDN (cache popular pastes)
  ↓ cache miss
API GW → Paste Service
  → Check Redis cache (hot pastes)
    ↓ cache miss
  → Query metadata DB (get S3 key)
  → Fetch content from S3
  → Populate cache
  → Return to client
```

### Expiration & Cleanup

```
Lazy deletion: Check expires_at on read → return 404 if expired
Active cleanup: Cron job deletes expired pastes
  - Scan: WHERE expires_at < NOW() (batched)
  - Delete metadata from DB
  - Delete content from S3
  - Run every hour
```

### Key Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| URL generation | Pre-generated key service | Fast, no collision |
| Content storage | S3 (separate from metadata) | Cost-effective for blobs |
| Caching | CDN + Redis | Popular pastes served from edge |
| Expiration | Lazy + active cleanup | Minimal read latency + eventual cleanup |
| Deduplication | SHA-256 hash of content | Same content → same S3 key |
