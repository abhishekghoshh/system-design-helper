# Design a CDN

## Blogs and websites


## Medium


## Youtube


## Theory

### Problem Statement
Design a Content Delivery Network (CDN) that distributes content to users from geographically close edge servers, reducing latency, offloading origin servers, and improving availability.

### Functional Requirements
- Serve static content (images, videos, JS, CSS) from edge servers
- Cache content at Points of Presence (PoPs) worldwide
- Cache invalidation (purge specific content)
- Support origin pull and push models
- SSL/TLS termination at edge
- Custom caching rules (TTL, headers, query string handling)
- Real-time analytics (hit rate, bandwidth, latency)

### Non-Functional Requirements
- **Latency**: < 50ms for cached content from nearest PoP
- **Scale**: 100+ Tbps aggregate bandwidth, millions of requests/sec
- **Availability**: 99.999%
- **Cache hit ratio**: > 95% for popular content
- **Global**: 200+ PoPs across 50+ countries

### High-Level Architecture

```
┌──────────┐     DNS resolves to     ┌────────────────────────┐
│  Client  │────nearest PoP─────────▶│  Edge Server (PoP)     │
└──────────┘                          │  ┌──────────────────┐  │
                                      │  │ Cache (SSD/RAM)  │  │
                                      │  └────────┬─────────┘  │
                                      └───────────┼────────────┘
                                                  │ cache miss
                                                  ▼
                                      ┌────────────────────────┐
                                      │  Mid-Tier / Shield     │
                                      │  (Regional Cache)      │
                                      └───────────┬────────────┘
                                                  │ cache miss
                                                  ▼
                                      ┌────────────────────────┐
                                      │  Origin Server         │
                                      │  (Customer's server)   │
                                      └────────────────────────┘
```

### Request Routing (How clients reach the nearest PoP)

```
Method 1: DNS-based routing
  Client → DNS query for cdn.example.com
  → CDN's authoritative DNS returns IP of nearest PoP
  → Based on client IP geolocation
  → TTL = 60s (allows re-routing)

Method 2: Anycast
  Multiple PoPs advertise same IP via BGP
  Internet routing naturally sends packets to nearest PoP
  → Fastest routing, handles failover automatically

Method 3: HTTP redirect
  Initial request → central load balancer → 302 redirect to nearest PoP
  → More control but adds a round trip
```

### Cache Hierarchy

```
Layer 1: Edge PoP (200+ locations)
  - Closest to user
  - Stores hot content (popular items)
  - SSD + RAM cache
  - Cache capacity: 10-100 TB per PoP

Layer 2: Regional Shield (10-20 locations)
  - Aggregates cache misses from nearby PoPs
  - Reduces load on origin
  - Larger cache capacity
  - One shield per region

Layer 3: Origin
  - Customer's actual server
  - Only hit on shield cache miss
  - Protected from traffic spikes
```

### Cache Invalidation

```
1. TTL-based expiration
   Cache-Control: max-age=3600 → expire after 1 hour
   Most common, simple, eventual consistency

2. Purge API
   POST /purge {"urls": ["https://cdn.example.com/image.jpg"]}
   → Propagate to all PoPs → delete from cache
   → Takes 1-5 seconds globally

3. Soft purge (stale-while-revalidate)
   Mark as stale → serve stale content while fetching fresh copy
   → No downtime during revalidation

4. Tag-based invalidation
   Purge all content tagged "product-123"
   → Useful for e-commerce (product update → purge all related assets)
```

### Cache Key Design

```
Default key: scheme + host + path + query string
  https://cdn.example.com/img/hero.jpg?v=2

Customization:
  - Ignore query string (for same content with tracking params)
  - Include headers (Accept-Encoding, Accept-Language)
  - Include cookies (per-user content — rare, defeats caching)
  - Custom key via edge logic (Cloudflare Workers, Lambda@Edge)
```

### Key Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Routing | Anycast + DNS fallback | Fastest path, automatic failover |
| Cache layers | 3-tier (edge → shield → origin) | Protect origin, high hit rate |
| Invalidation | TTL + purge API | Simple default + instant when needed |
| Storage | SSD (bulk) + RAM (hot objects) | Cost vs performance balance |
| TLS | Terminate at edge | Reduce latency (no TLS to origin internally) |

### Scaling Considerations
- **PoP deployment**: Add PoPs where user density is high
- **Hot content**: Replicate across all PoPs proactively (push model)
- **Long-tail content**: Only cache at shield layer, not every PoP
- **Video**: Chunk-based caching (HLS/DASH segments cached independently)
- **DDoS**: Edge absorbs attack traffic before reaching origin
