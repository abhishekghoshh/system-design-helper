# Design TikTok

## Blogs and websites


## Medium


## Youtube


## Theory

### Problem Statement
Design a short-form video platform like TikTok that supports video creation, personalized "For You" feed, likes/comments/shares, and content discovery at massive scale.

### Functional Requirements
- Upload short videos (15s–10min) with effects, music, filters
- Personalized "For You" feed (recommendation-driven, not follow-based)
- Follow creators, like, comment, share, duet, stitch
- Search (users, sounds, hashtags)
- Live streaming
- Creator analytics dashboard
- Content moderation

### Non-Functional Requirements
- **Scale**: 1B+ MAU, 500M+ DAU
- **Latency**: Feed loads < 200ms, instant video playback start
- **Storage**: Exabytes of video content
- **Availability**: 99.99%
- **Recommendation**: Feed quality is the core product differentiator

### High-Level Architecture

```
┌──────────┐     ┌──────┐     ┌─────────────────────────────┐
│  Mobile  │◀───▶│  CDN │     │      Service Layer           │
│  App     │     └──────┘     │                              │
└────┬─────┘                  │  ┌─────────────────────────┐ │
     │                        │  │ Video Upload Service     │ │
     ▼                        │  │ Feed / Recommendation Svc│ │
┌──────────┐                  │  │ User Service             │ │
│  API GW  │─────────────────▶│  │ Interaction Service      │ │
└──────────┘                  │  │ Search Service           │ │
                              │  │ Content Moderation Svc   │ │
                              │  └────────────┬────────────┘ │
                              └───────────────┼──────────────┘
                                              │
                        ┌─────────────────────┼─────────────────┐
                        ▼                     ▼                 ▼
                  ┌──────────┐         ┌──────────┐      ┌──────────┐
                  │  Object  │         │ Metadata │      │ ML Model │
                  │  Store   │         │    DB    │      │ Service  │
                  └──────────┘         └──────────┘      └──────────┘
```

### Video Upload & Processing Pipeline

```
Upload → Object Store (raw) → Processing Queue → Workers:
  1. Transcode to multiple resolutions (360p, 720p, 1080p)
  2. Adaptive bitrate packaging (HLS/DASH)
  3. Generate thumbnails
  4. Extract audio fingerprint (music detection)
  5. Content moderation (nudity, violence, copyright)
  6. Feature extraction for recommendation (visual, audio, text)
  
Processed → CDN distribution (multi-region)
Metadata → Database (title, creator, tags, music, duration)
```

### Recommendation Engine ("For You" Feed)

```
TikTok's feed is NOT follow-based. It's entirely recommendation-driven.

Signals:
  - Watch time (most important — did user watch to the end? Replay?)
  - Likes, comments, shares, saves
  - Content features (video embeddings, audio, text/hashtags)
  - User features (interests, device, location, time of day)
  - Creator features (upload frequency, engagement rate)
  - Negative signals (skip, "not interested", report)

Architecture:
  Candidate Generation (broad)
    → 100K videos from millions
    → Collaborative filtering + content-based
  
  Ranking (precise)
    → Deep learning model scores each candidate
    → Predicts P(watch), P(like), P(share)
    → Weighted score = α·P(watch) + β·P(like) + γ·P(share)
  
  Re-ranking (diversity + policy)
    → Deduplicate similar content
    → Inject diverse topics (exploration vs exploitation)
    → Apply content policy rules
    → Final ordered list
```

### Content Moderation

```
Multi-layer approach:
  Layer 1: Automated ML (95%+ of decisions)
    - Image/video classification (nudity, violence)
    - Audio analysis (hate speech, copyright)
    - Text analysis (captions, comments)
  
  Layer 2: Human review (edge cases)
    - Flagged by ML with low confidence
    - Reported by users
    - Appeals from creators
  
  Layer 3: Proactive detection
    - New trending content patterns
    - Misinformation detection
    - Coordinated inauthentic behavior
```

### Key Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Feed model | Recommendation-driven (not follow-based) | Core differentiator, virality |
| Video storage | S3 + multi-region CDN | Global delivery, cost |
| Recommendation | Two-tower deep learning | Balance precision + recall |
| Processing | Async pipeline (Kafka + workers) | Handle upload spikes |
| Moderation | ML-first + human escalation | Scale with accuracy |

### Scaling Considerations
- **Video delivery**: CDN with edge caching, adaptive bitrate
- **Recommendation**: Feature store + model serving on GPU clusters
- **Database**: Shard by user_id and video_id separately
- **Real-time**: Kafka for interaction events → update models online
