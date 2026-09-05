# Design a Recommendation System

## Blogs and websites
- [How Netflix Reinvented High‑Performance Recommendations](https://netflixtechblog.com/@ NetflixEng)
- [How Facebook Enables Machine Learning at Scale](https://ai.facebook.com/blog/)

## Medium
- [Building a Scalable Recommendation System](https://medium.com/@ NetflixEng/recommendation-system- architecture-1234567890)

## Youtube

- [Design an ML Recommendation Engine | System Design](https://www.youtube.com/watch?v=FoSCaue3lcg)
- [YouTube Recommendation Engine: Complete Meltdown Analysis](https://www.youtube.com/watch?v=URI5GsOBznk)

---

## Theory

### Topics Covered

1. [Introduction / Problem Statement](#introduction-problem-statement)
2. [Characteristics](#characteristics)
3. [Components](#components)
4. [Architectural Patterns](#architectural-patterns)
5. [Benefits](#benefits)
6. [Pros](#pros)
7. [Cons](#cons)
8. [Challenges](#challenges)
9. [Best Practices](#best-practices)
10. [When to Use / When Not to Use](#when-to-use-when-not-to-use)
11. [Use Cases](#use-cases)
12. [Architecture](#architecture)
13. [High-Level Design](#high-level-design)
14. [Deep Dive](#deep-dive)
15. [Data Model and API](#data-model-and-api)
16. [Replication Strategies](#replication-strategies)
17. [Failure Detection and Membership](#failure-detection-and-membership)
18. [High Availability and Scalability](#high-availability-and-scalability)
19. [Performance and Optimization](#performance-and-optimization)
20. [CAP Theorem and Consistency Trade-offs](#cap-theorem-and-consistency-trade-offs)
21. [Encryption and Key Management](#encryption-and-key-management)
22. [Authentication and Authorization](#authentication-and-authorization)
23. [Security Threats and Mitigations](#security-threats-and-mitigations)
24. [Observability and Logging](#observability-and-logging)
25. [Replication Strategies](#replication-strategies)
26. [Failure Detection and Membership](#failure-detection-and-membership)
27. [High Availability and Scalability](#high-availability-and-scalability)
28. [Performance and Optimization](#performance-and-optimization)
29. [CAP Theorem and Consistency Trade-offs](#cap-theorem-and-consistency-trade-offs)
30. [Encryption and Key Management](#encryption-and-key-management)
31. [Authentication and Authorization](#authentication-and-authorization)
32. [Security Threats and Mitigations](#security-threats-and-mitigations)
33. [Observability and Logging](#observability-and-logging)
34. [Java and Spring Boot Implementation Guide](#java-and-spring-boot-implementation-guide)
35. [Real-World Implementations](#real-world-implementations)
36. [Interview Questions and Answers](#interview-questions-and-answers)

---
---
### Introduction / Problem Statement

A **recommendation system** is an algorithmic system that predicts user preferences and surfaces relevant items — products, movies, videos, songs, friends — without the user explicitly searching for them. It transforms the "infinite choice" problem (too many options) into a curated, personalized selection.

**Why Does It Exist**

On platforms with millions or billions of items (Netflix: 20,000 movies; YouTube: 500 hours/minute; Amazon: 350M+ products), users cannot discover what they want by browsing. Recommendation systems bridge the gap between available content and user interest, increasing engagement, retention, and revenue.

**What Problem Does It Solve**

* **Discovery**: Help users find relevant content in an oversaturated catalog.
* **Engagement**: Personalized recommendations increase session time and interaction.
* **Conversion**: Relevant product recommendations drive sales (Amazon's 35% of revenue).
* **Retention**: Fresh, personalized content keeps users returning.
* **Cold start**: New users/items with no interaction history — recommend based on profiles or popular items.


### Characteristics

| Characteristic | What it means | Why it matters | How it works |
|---|---|---|---|
| **Implicit feedback** | User behavior (watch, click, like) as implicit rating | Most interactions are implicit (no star ratings) | Click-through rate, watch time, dwell time as proxy for preference |
| **Two-stage pipeline** | Candidate generation (100s) → ranking (top 10) | Scales to billions of items | Approximate methods (ANN, LSH) for candidates; ML model for ranking |
| **Exploration** | Occasionally show non-personalized or random items | Prevents filter bubble; collects data | ε-greedy, Thompson sampling, multi-armed bandits |
| **Serendipity** | Surprising but relevant recommendations | Increases user delight + engagement | Diversification, novelty scores |
| **Freshness** | New/viral content gets recommended | Keeps content ecosystem healthy | Time-decay features, recency weighting |
| **Real-time** | Recommendations reflect very recent activity | "Because you watched X just now" | Streaming feature updates; online model serving |
| **Cold start handling** | New users/items with no history | Prevents poor early experience | Popular items for new users; content features for new items |

### Components

| Component | Purpose | Responsibilities | Relationship | Real-world Example |
|---|---|---|---|---|
| **Event Tracker** | Collect user interactions | Log views, clicks, likes, shares, watch time | Client → Event Pipeline | Kafka, Snowplow |
| **Feature Store** | Compute + serve features | User features, item features, interaction features, context | Feeds candidate gen + ranking | Feast, Hopsworks |
| **Candidate Generator** | Find ~100-1000 candidate items | Fast retrieval of potentially relevant items | Uses user/item features | Approximate Nearest Neighbors |
| **Ranking Model** | Score + rank candidates | Predict P(interaction) per candidate | Receives candidates → outputs ranked list | GBDT, DeepFM, Two-tower NN |
| **Explainer** | Explain why items recommended | "Because you watched X" / "Similar to Y" | Post-ranking | Amazon "Frequently bought together" |
| **A/B Test Framework** | Measure recommendation quality | Split users, compare metrics | Multiple ranking models | OptaForce, PlanOut |
| **Model Trainer** | Train recommendation models | Offline training on historical data | Uses Feature Store + Event Log | Spark MLlib, TensorFlow |
| **Online Learner** | Update models in real-time | Incorporate new interactions immediately | Streams from Event Tracker | Vowpal Wabbit, parameter server |

### Architectural Patterns

#### Two-Stage Pipeline (Candidate Generation + Ranking)

* **What**: Split recommendation into two stages: (1) Candidate generation — retrieve 100-1000 potentially relevant items fast (using approximate methods); (2) Ranking — score candidates with an ML model and select top 10.
* **Problem solved**: Scoring all 10M items for every user is too slow. Generate a small candidate set fast, then rank precisely.
* **How it works**: (1) Candidate generation: "Find 1000 videos similar to what the user watched" — uses collaborative filtering (item embeddings) or content-based filtering (tag/title matching). Methods: Approximate Nearest Neighbor (ANN), Locality-Sensitive Hashing (LSH), sampling. (2) Ranking: Take 1000 candidates → compute 100-1000 features per user-item pair → feed to ML model (GBDT, deep neural net) → predict P(click/watch/purchase) → rank → return top 10.
* **When to use**: Catalogs with millions+ items; when ranking all items is computationally infeasible.
* **When not to use**: Small catalogs (< 10K items) — direct ranking is fast enough.
* **Advantages**: Scales to billions of items; can use expensive ML models for ranking without performance issues.
* **Disadvantages**: Two systems to maintain; candidate generation can miss good items (recall problem).
* **Real-world example**: Netflix (ANN for candidates → deep ranking model), YouTube (candidate generation via deep candidate generation network → ranking via deep neural network).

#### Matrix Factorization (SVD)

* **What**: Decompose the user-item interaction matrix into low-dimensional user and item embedding vectors. The dot product predicts the interaction.
* **Problem solved**: Collaborative filtering at scale — predict how much user U will like item I based on patterns from similar users/items.
* **How it works**: Given an R (users × items) matrix with known ratings (and missing entries for unwatched items), factorize R ≈ U × V^T where U (users × k) and V (items × k) are latent factor matrices. Train using Stochastic Gradient Descent (SGD) or Alternating Least Squares (ALS — parallelizable, good for implicit feedback). Prediction: ŷ_ui = μ + b_u + b_i + q_i^T p_u.
* **When to use**: Explicit ratings (Netflix ratings, movie scores); moderate catalog size (< 1M items).
* **When not to use**: Implicit feedback only (most real systems); billions of items (use deep models instead).
* **Advantages**: Simple, interpretable; works well with explicit feedback; parallelizable (ALS).
* **Disadvantages**: Cold start (no row/column for new user/item); not suitable for rich feature data (click context, user demographics).
* **Java/Spring Boot example**:
```java
// Simplified SGD-based matrix factorization
public class MatrixFactorization {
    private double[][] userFactors;  // userFactors[u][k]
    private double[][] itemFactors;  // itemFactors[i][k]
    private double[] userBias;
    private double[] itemBias;

    public void train(List<Rating> ratings, int factors, int epochs, double lr, double reg) {
        // Initialize random factors
        Random rand = new Random(42);
        for (int u = 0; u < numUsers; u++)
            for (int k = 0; k < factors; k++)
                userFactors[u][k] = rand.nextGaussian() * 0.1;

        // SGD training
        for (int epoch = 0; epoch < epochs; epoch++) {
            for (Rating r : ratings) {
                int u = r.userId, i = r.itemId;
                double prediction = predict(u, i);
                double err = r.rating - prediction;

                // Update factors
                for (int k = 0; k < factors; k++) {
                    double pu = userFactors[u][k];
                    userFactors[u][k] += lr * (err * itemFactors[i][k] - reg * pu);
                    itemFactors[i][k] += lr * (err * pu - reg * itemFactors[i][k]);
                }
                userBias[u] += lr * (err - reg * userBias[u]);
                itemBias[i] += lr * (err - reg * itemBias[i]);
            }
        }
    }

    public double predict(int userId, int itemId) {
        return globalMean + userBias[userId] + itemBias[itemId] +
               dot(userFactors[userId], itemFactors[itemId]);
    }
}
```
* **Real-world example**: Netflix (SVD for movie recommendations), Amazon (item-to-item collaborative filtering).

### Benefits

* **Increased engagement**: Personalized content keeps users on the platform longer.
* **Higher conversion**: Relevant product recommendations increase purchase rates.
* **Better discovery**: Helps content creators/items surface to interested users.
* **Scalable personalization**: Can personalize at scale without manual curation.
* **Data-driven insights**: Reveals user preferences → product decisions.

### Pros

* **Improved metric**: 10-30% increase in engagement/click-through on recommended content.
* **Scalable**: Can serve billions of recommendations per day.
* **Multiple algorithms**: Ensemble of collaborative, content-based, and deep learning models.
* **Real-time updates**: Online learning + feature store → fresh recommendations.
* **A/B testing**: Continuous improvement via experiments.

### Cons

* **Filter bubbles**: Users see only what the algorithm thinks they want → reduced diversity of exposure.
* **Cold start**: New users/items get poor recommendations; requires fallback strategies.
* **Feedback loops**: Recommendations influence future behavior → may amplify biases.
* **Computation cost**: Training deep models requires significant GPU resources + time.
* **Quality metrics**: Offline metrics (precision@k) don't always correlate with user satisfaction.

### Challenges

#### Technical Challenges

* **Feature engineering**: Combining 1000+ features (user demographics, item metadata, context, historical behavior) into a model-friendly format.
* **Model serving latency**: Ranking 1000 candidates × 100 features each < 50 ms → requires optimized serving infrastructure.
* **Online vs. batch**: Real-time recommendations (latest click) vs. batch (daily retrain) — balancing freshness and computational cost.
* **Scalability**: Candidate generation over billions of items → approximate methods (ANN, LSH) introduce recall loss.

#### Scalability Challenges

* **Catalog size**: Millions of items → candidate generation must be approximate; ranking must be efficient.
* **User base**: Billions of users → feature store must serve P99 < 10 ms; model serving must scale horizontally.
* **Training data volume**: 100M+ users × 1000 items/day = 10B interactions/day → distributed training (Horovod, Ray).
* **Feature freshness**: Real-time features (last click, current session) → streaming feature pipeline (Kafka Streams + Redis).

#### Performance Challenges

* **Latency**: End-to-end recommendation (candidate gen + ranking + serving) < 50 ms for interactive feeds.
* **Ranking throughput**: 100K+ ranking requests/second → need model serving clusters (TF Serving, Triton).
* **ANN index rebuild**: Rebuilding the approximate nearest neighbor index over 100M item embeddings takes hours → incremental updates.

#### Reliability Challenges

* **Model drift**: Recommendation quality degrades as user behavior changes → continuous online learning + A/B monitoring.
* **Data pipeline failures**: Corrupted feature data → poor recommendations → impact business metrics → need data quality checks + rollback.
* **Cold start recovery**: New users → fallback to popular/trending; new items → content-based until enough interactions.

#### Maintainability Challenges

* **Algorithm evolution**: Moving from collaborative filtering → deep learning → two-tower models → transformer-based retrievers.
* **Feature versioning**: 1000+ features change over time → need feature store with versioning.
* **A/B test analysis**: 100+ concurrent experiments → need robust stats + guardrail metrics.

#### Operational Challenges

* **Model monitoring**: Track offline metrics (precision/recall) + online metrics (CTR, watch time, engagement) + input distribution drift + prediction distribution drift.
* **Retraining cadence**: Daily batch retrain + hourly incremental updates → pipeline orchestration (Airflow).
* **Infrastructure**: GPU clusters for training; CPU inference servers; Redis for feature serving; Kafka for streaming.

#### Security Concerns

* **Privacy**: User behavior patterns are sensitive → differential privacy, GDPR compliance.
* **Manipulation**: Users/bots may try to game the algorithm (fake likes, viewbots) → anomaly detection.
* **Bias amplification**: Algorithm may reinforce societal biases (e.g., showing high-paying jobs only to men) → bias auditing.

### Best Practices

* **Two-stage pipeline**: Candidate generation (fast, approximate) → ranking (precise ML model). Don't rank over all items.
* **Feature store**: Centralize feature computation — single source of truth; offline (batch) + online (real-time) features.
* **A/B test everything**: Every algorithmic change → A/B test with guardrail metrics (CTR, watch time, retention, satisfaction).
* **Cold start strategy**: New user → popular items in their region; new item → content-based (similar items) until enough interactions.
* **Exploration**: ε-greedy or multi-armed bandits → 5-10% of impressions go to non-personalized items.
* **Model monitoring**: Track offline metrics (precision@k, recall, NDCG), online metrics (CTR, engagement), and input/output drift.
* **Approximate search**: Use FAISS or Annoy for ANN in candidate generation — trade 5-10% recall for 100x speedup.
* **Incremental retraining**: Daily full retrain + hourly incremental updates + real-time online learning.

### When to Use / When Not to Use

#### Appropriate

* E-commerce product recommendations (Amazon, Shopify).
* Video/music streaming (Netflix, Spotify, YouTube).
* Social media feed ranking (Facebook, Instagram, TikTok).
* News aggregation (Google News, Flipboard).
* Job matching (LinkedIn, Indeed).

#### Not Appropriate

* When users know exactly what they want → search is better.
* Small catalogs (< 1000 items) → manual curation or simple rules suffice.
* When serendipity is more important than relevance (e.g., "discover weekly" mode).

#### Alternatives

* **Search**: When users have a specific query.
* **Manual curation**: Editorial picks (used by Netflix for homepage rows).
* **Popularity-based**: Show trending/popular items (works for new users).
* **Random**: Pure exploration (ε-greedy).

#### Decision Factors

* **Catalog size**: Millions+ → recommendation system; thousands → simpler approaches.
* **User behavior**: Browsing behavior → recommendations; specific intent → search.
* **Business goal**: Engagement → recommendations; conversion → search.
* **Data availability**: Rich interaction data → ML models; no data → popularity-based.

### Use Cases

#### Video Streaming (Netflix)

* **Problem**: 20,000+ videos; users can't browse all → need personalized discovery.
* **Solution**: Two-stage pipeline: (1) Candidate generation: 1000s of candidate videos via collaborative filtering + content-based (genre, cast, director) + popularity. (2) Ranking: deep neural network scoring 100+ features (user history, viewing context, video metadata) → top 10 recommendations per row.
* **Why suitable**: Massive catalog; rich user behavior data; engagement-driven business.
* **How it works**: (1) Every interaction (play, pause, skip, rewatch) → Kafka → feature store. (2) Offline: daily retrain candidate model + ranking model on Spark. (3) Online: candidate gen via ANN (FAISS); ranking via TensorFlow Serving. (4) Real-time: online learner updates user embeddings from session events.
* **Trade-offs**: Personalization vs. diversity; model complexity vs. latency; offline accuracy vs. online engagement.

#### E-commerce (Amazon)

* **Problem**: 350M+ products; need to surface relevant items at the right moment (homepage, product page, cart).
* **Solution**: Item-to-item collaborative filtering + "frequently bought together" + session-based recommendations. Uses real-time behavioral signals (cart adds, page views).
* **Why suitable**: High-volume transactions; strong signal (purchases); revenue-driven.
* **How it works**: (1) Build item-item similarity matrix (co-occurrence within sessions). (2) For a given item/page → look up top-K similar items → rank by predicted conversion. (3) Real-time: session features (items viewed in this session) → boost relevant items. (4) Offline: ALS matrix factorization on Spark → 10M×10M matrix → item embeddings.
* **Trade-offs**: Accuracy vs. serendipity; cold start for new products; attribution of revenue to recommendations.

### Architecture

A production recommendation system has a **two-stage pipeline**: (1) **Candidate generation** — fast retrieval of 100-1000 potentially relevant items using approximate methods (collaborative filtering, content-based, popularity); (2) **Ranking** — a machine learning model scores and ranks candidates. **Feature stores** (Feast, Hopsworks) centralize feature computation for training and serving. **Online learning** updates models from real-time events. **A/B testing** frameworks evaluate changes. The system uses **batch processing** (Spark, Flink) for training and **streaming** (Kafka Streams, Flink) for real-time features. Model serving uses low-latency inference servers (TensorFlow Serving, Triton).

```mermaid
graph TD
  subgraph "Data Sources"
    Events[User Events<br/>Views, Clicks, Purchases]
    Catalog[Item Catalog<br/>Metadata, Content]
    Context[Context<br/>Time, Device, Location]
  end
  subgraph "Data Pipeline"
    Kafka[Kafka<br/>Event Stream]
    FeatureStore[Feature Store<br/>Feast/Hopsworks]
    Warehouse[(Data Warehouse<br/>Spark/BigQuery)]
  end
  subgraph "Model Training"
    CGenModel[Candidate Gen Model<br/>ALS/ANN]
    RankModel[Ranking Model<br/>GBDT/Deep NN]
  end
  subgraph "Online Serving"
    OnlineFeat[Online Features<br/>Redis/Serving]
    CGen[Candidate Generator<br/>FAISS/Annoy]
    Ranker[Ranking Service<br/>TF Serving/Triton]
    Explainer[Explainer Service]
  end
  subgraph "Clients"
    App[App/Web]
  end
  Events --> Kafka
  Catalog --> Kafka
  Context --> Kafka
  Kafka --> FeatureStore
  Kafka --> Warehouse
  FeatureStore --> CGenModel
  Warehouse --> RankModel
  CGenModel --> CGen
  RankModel --> Ranker
  FeatureStore --> OnlineFeat
  CGen -->|100-1000 items| Ranker
  OnlineFeat --> Ranker
  Ranker -->|Top 10 items| Explainer
  Explainer --> App
  App -->|Feedback| Kafka
```

#### Architecture Structure

* **Data ingestion**: Kafka collects user events (views, clicks, purchases), item catalog updates, and contextual data.
* **Batch layer**: Spark/Flink processes events for offline model training (feature engineering, matrix factorization).
* **Speed layer**: Kafka Streams + Redis provides real-time features (session context, latest events).
* **Feature store**: Feast or custom — unified batch + online feature serving.
* **Model serving**: TensorFlow Serving / Triton for deep models; custom servers for lightweight models.
* **Candidate serving**: FAISS index in Redis or a dedicated ANN service for fast candidate retrieval.

#### Communication

* **Batch → Training**: Spark reads from data warehouse; writes models to artifact store (S3).
* **Streaming → Features**: Kafka → Flink → Redis (real-time feature serving).
* **Online → Ranking**: App → candidate generator → ranking service → return recommendations.

#### Data Flow

1. **Events**: User interactions → Kafka → feature store (offline) + Redis (online).
2. **Training** (daily): Spark computes features → trains candidate model (ALS) + ranking model (GBDT/NN) → saves to artifact store.
3. **Candidate generation**: ANN index (FAISS) loaded into serving service; 1000 candidates retrieved for user.
4. **Ranking**: 1000 candidates × 100 features → ML model → top 10 recommendations.
5. **Explaining**: Why each item was recommended ("because you watched X").
6. **A/B test**: Split traffic across model variants; measure engagement.

#### Scaling Strategy

* **Feature store**: Redis cluster for online features; S3 + Spark for batch features.
* **Candidate serving**: FAISS index sharded by item partition; replicated for availability.
* **Ranking**: TensorFlow Serving with autoscaled inference servers.
* **Training**: Spark clusters; distributed (Horovod for deep models).

#### Failure Handling

* **Feature unavailability**: Use default/zero features → model still serves with degraded quality.
* **Candidate service failure**: Fall back to popularity-based candidates.
* **Ranking model failure**: Use a simpler baseline model (linear model) with cached features.
* **A/B test framework failure**: Default to control variant.

### High-Level Design

```mermaid
flowchart LR
  U[User] -->|Request recommendations| App[Mobile/Web App]
  App --> APIGW[API Gateway]
  APIGW --> RecAPI[Recommendation API]
  RecAPI -->|Resolve user features| FeatureStore[(Feature Store)]
  RecAPI -->|Get candidates| ANN[(ANN Index<br/>FAISS in Redis)]
  RecAPI --> Ranker[Ranking Model<br/>TF Serving]
  RecAPI --> Explainer[Explainer Service]
  Ranker -->|Rank and return| RecAPI
  RecAPI -->|Top 10| App
  App -->|Click/Watch Feedback| Stream[Kafka]
  Stream -->|Update features| FeatureStore
  Stream -->|Train daily| Batch[(Spark Cluster)]
  Batch -->|Update models| ModelStore[(Model Store)]
  ModelStore --> Ranker
  ModelStore --> ANN
```

### Deep Dive

#### Two-Tower Neural Retrieval Model (YouTube-style)

YouTube's recommendation system uses a two-tower deep neural network:
* **User tower**: Embeds user features (search history, watch history, demographics, context) into a dense vector.
* **Item tower**: Embeds video features (title, description, metadata, category, video ID) into a dense vector.
* **Retrieval**: User vector compared against all candidate item vectors → dot product → top match.
* **Training**: Softmax over candidate items in the batch. Uses negative sampling for efficiency.

```java
// Simplified two-tower model in pseudocode
class TwoTowerModel {
    UserTower: user_features -> user_embedding (128-dim)
    ItemTower: item_features -> item_embedding (128-dim)
    
    // Training: maximize dot(user_emb, item_emb) for positive pairs
    loss = -log(softmax(dot(user_emb, positive_item_emb) / temperature))
           + sum(softmax(dot(user_emb, negative_items_emb) / temperature))
}
```

**Key design points**:
* Candidate generation happens via ANN search over item tower embeddings (100M+ items).
* Negative sampling: sample items the user didn't interact with (from the same batch) for training efficiency.
* Softmax temperature: lower temperature → sharper distribution (more confident top picks).
* Distributed training: model sharded across 100+ GPU/TPU cores; each machine handles subset of candidates.

#### Candidate Generation with Approximate Nearest Neighbor

For 100M+ candidate items, exact nearest neighbor search is O(N) — too slow. Use FAISS:
```python
# FAISS index for candidate retrieval
index = faiss.IndexIVFFlat(d=128, nlist=10000, metric=faiss.METRIC_L2)
# d = embedding dimension, nlist = number of Voronoi cells
index.train(item_embeddings)  # k-means to create Voronoi cells
index.add(item_embeddings)    # add item vectors
# Search: O(nlist + nnprobe * items_per_cell) instead of O(N)
D, I = index.search(user_embedding, k=1000)  # 1000 nearest items
```

#### Matrix Factorization for Collaborative Filtering

The most classical recommendation algorithm — decompose user-item interaction matrix into latent factors:
* **User factors** U ∈ ℝ^(m×k): each user mapped to a k-dimensional latent space.
* **Item factors** V ∈ ℝ^(n×k): each item mapped to the same k-dimensional space.
* **Prediction**: r_ui ≈ μ + b_u + b_i + q_i^T p_u (global mean + user bias + item bias + latent factor dot product).
* **Training**: ALS (Alternating Least Squares) or SGD — solve for U and V alternately.
* **Scaling**: Distributed (Spark MLlib ALS) — handle 100M users × 10M items.

### Data Model and API

* **API purpose**: Serve personalized recommendations to client applications.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/recommendations` | Get personalized recommendations for a user |
| GET | `/api/v1/recommendations/similar` | Get similar items to a given item (item-based) |
| GET | `/api/v1/recommendations/trending` | Get trending/popular items |
| POST | `/api/v1/events` | Record a user interaction event |
| GET | `/api/v1/user/{userId}/features` | Get computed user features (for debugging) |

**Query parameters (GET /recommendations)**:
| Parameter | Type | Default | Description |
|---|---|---|---|
| `user_id` | string | required | User identifier |
| `count` | int | 10 | Number of items to return |
| `channel` | string | home | Context: home, search, cart, email |
| `locale` | string | en-US | Language/locale |
| `surface` | string | `web` | Client: web, ios, android |
| `model_version` | string | latest | A/B test model variant |

**Response**:
```json
{
  "user_id": "user_123",
  "recommendations": [
    {
      "item_id": "prod_456",
      "score": 0.843,
      "reason": "frequently bought together with item_789",
      "metadata": {
        "title": "Wireless Headphones",
        "price": "$99.99",
        "image_url": "https://...",
        "category": "electronics"
      }
    }
  ],
  "model_version": "rank-v3-202501",
  "cache_ttl": 300
}
```

**Error responses**:
```json
{"error": "unauthorized", "message": "Invalid API key", "code": 401}
{"error": "not_found", "message": "User not found", "code": 404}
{"error": "invalid_request", "message": "Missing user_id parameter", "code": 400}
{"error": "rate_limited", "message": "Too many requests", "code": 429}
```

**Authentication**: API key in `Authorization: Bearer <key>` or `X-API-Key` header. Internal service-to-service via mTLS.

**Rate limiting**: 1000 req/sec per API key; 100 req/sec per user_id (prevent cache-busting).


```mermaid
erDiagram
  USER ||--o{ INTERACTION : "has"
  ITEM ||--o{ INTERACTION : "received"
  USER ||--o{ USER_FEATURE : "has"
  ITEM ||--o{ ITEM_FEATURE : "has"
  INTERACTION ||--o{ EVENT : "derived from"

  USER {
    string user_id PK
    string email
    string signup_date
    string country
    string locale
  }
  ITEM {
    string item_id PK
    string title
    string description
    string category
    float price
    string image_url
    datetime created_at
  }
  INTERACTION {
    string interaction_id PK
    string user_id FK
    string item_id FK
    enum type view, click, like, purchase
    float value
    datetime timestamp
    json context
  }
  USER_FEATURE {
    string user_id FK
    json features
    datetime updated_at
  }
  ITEM_FEATURE {
    string item_id PK
    json features
    datetime updated_at
  }

```

**Data lifecycle**: User/item features refreshed daily (batch) + updated in real-time (streaming). Interaction events archived after 2 years. User features TTL = 30 days (stale → recompute).

**Sharding**: Users sharded by user_id hash (1000 shards); items by item_id hash. Interaction events sharded by date + user_id.

**Consistency**: Strong consistency for recent interactions (last 24h) for real-time recommendations; eventual consistency for historical features.

### Replication Strategies

**What it means**

Replication Strategies determine how data and state are copied across multiple nodes in Recommendation Engine. The choice of strategy determines the trade-off between consistency, availability, and latency.

**Why it matters**

Recommendation Engine must replicate data to prevent loss and serve reads from multiple nodes. The replication strategy determines whether the system favors consistency (strong reads) or availability (always writable), and how it handles cross-node failure.

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

**Trade-offs for Recommendation Engine**:

| Strategy | Use Case | Pros | Cons |
|---|---|---|---|
| Leader-based | user preferences, viewing history, purchase history | Strong consistency, simple | Write bottleneck, leader failure risk |
| Multi-leader | public item metadata, aggregate trends, anonymized stats | Low-latency global writes | Conflict resolution, complex |
| Leaderless | Caching, counters | High availability, no bottleneck | Eventual consistency, read repair overhead |

**Real-world implementations**

- **Redis**: Leader-follower replication with asynchronous replication; Sentinel handles failover.
- **Apache Kafka**: Leader-based partition replication with ISR (in-sync replica) — writes go to the leader, followers replicate.
- **Cassandra**: Tunable consistency with leaderless quorum (R + W > N).
- **DynamoDB Global Tables**: Multi-master active-active across regions.

### Failure Detection and Membership

**What it means**

Failure Detection and Membership is the mechanism by which Recommendation Engine determines which nodes are alive and part of the cluster. Membership is the list of known nodes; failure detection is the process of updating that list when nodes fail or recover.

**Why it matters**

Recommendation Engine must route requests only to healthy nodes and trigger failover when a node goes down. False positives (healthy nodes marked as dead) cause unnecessary failovers and data loss. False negatives (dead nodes not detected) cause failed requests and degraded performance.

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

### High Availability and Scalability

**What it means**

High Availability and Scalability determines how Recommendation Engine continues operating when nodes or entire zones fail, and how capacity is added as demand grows. HA is about minimizing downtime; scalability is about maintaining performance as load increases.

**Why it matters**

Recommendation Engine must stay operational even when individual nodes, availability zones, or entire regions fail. At the same time, it must scale horizontally to handle traffic spikes without degrading latency. The two are intertwined: the replication strategy, failure detection, and load balancing all contribute to both HA and scalability.

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

**Load balancing**: A load balancer distributes incoming requests across healthy nodes. Algorithms include round-robin, least connections, and weighted routing. Health checks ensure traffic only goes to healthy nodes. For Recommendation Engine, the load balancer also considers Candidate Generator (two-tower NN) when routing.

**Auto-scaling**: The system automatically adds or removes nodes based on metrics (CPU, memory, request rate). Scale-out policies add nodes when load exceeds a threshold; scale-in policies remove nodes during low load. For stateful services like Recommendation Engine, scale-out involves rebalancing partitions (moving data and connections to the new node).

**Failover and recovery**: When a node fails, the load balancer detects it (via health checks or failure detection) and stops sending traffic. A new node is provisioned (or a standby is promoted) and begins serving. For Recommendation Engine, failover must preserve user preferences, viewing history, purchase history data — this is achieved through replication with a quorum of healthy nodes.

**Scalability patterns**:

1. **Horizontal partitioning (sharding)**: Split data by a partition key (e.g., user_id, session_id) and distribute partitions across nodes. New nodes take ownership of additional partitions.

2. **Consistent hashing**: Minimize data movement on scale-out — only 1/N of the data moves to the new node. Nodes and partitions are placed on a ring; a request for key X is routed to the next node clockwise from hash(X).

3. **Connection draining**: When scaling in, existing connections are allowed to complete before the node is shut down. For Recommendation Engine, this means draining active A sessions gracefully.

**Real-world implementations**

- **Netflix OSS (Eureka + Zuul + Ribbon)**: Service discovery with Eureka, edge routing with Zuul, and client-side load balancing with Ribbon. Scales to thousands of instances.
- **Kubernetes HPA + VPA**: Horizontal Pod Autoscaler scales pods based on CPU/memory; Vertical Pod Autoscaler adjusts resource requests based on historical usage.
- **AWS ALB + Auto Scaling Groups**: Application Load Balancer with auto-scaling groups across AZs; health checks replace unhealthy instances automatically.

### Performance and Optimization

**What it means**

Performance and Optimization covers the techniques Recommendation Engine uses to achieve low latency, high throughput, and efficient resource usage. This section examines the key performance metrics, bottlenecks, and optimizations specific to the system.

**Why it matters**

Recommendation Engine faces competing pressures: users demand low latency, the system must handle high throughput, and infrastructure costs must be controlled. The optimizations applied at the data, compute, and network layers determine whether the system meets its SLA.

**How it works**

**Latency layers**: Latency in Recommendation Engine comes from three layers:
1. **Network**: Round-trip time from client to the nearest edge node / load balancer.
2. **Application**: Request processing time on the server (CPU, I/O, lock contention).
3. **Data**: Time to read/write from storage (cache hit vs. database query).

The 99th-percentile latency is the key metric for user-facing systems — it determines the worst-case experience.

**Caching strategies**: Recommendation Engine uses multiple cache layers:
- **Edge cache**: Static assets (images, CSS, JS) served from a CDN at the edge. For Recommendation Engine, this caches public item metadata, aggregate trends, anonymized stats that doesn't change frequently.
- **Application cache**: In-memory cache (e.g., Redis, Memcached) for frequently accessed data. Cache-aside pattern: application checks cache first, falls back to database on miss.
- **Local cache**: In-process cache (e.g., Caffeine, Guava) for data accessed within a single request. Avoids network round-trips.

**Batching and pipelining**: Recommendation Engine batches small operations (e.g., writes, log flushes) to amortize per-operation overhead. Pipelining allows multiple requests to be in flight simultaneously.

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

**Connection pooling**: Recommendation Engine maintains a pool of database connections to avoid the TCP handshake overhead on every request. Pool size is tuned to match the database's capacity.

**Compression**: Responses are compressed (gzip, zstd) for clients that support it. At the network layer, gRPC uses HPACK header compression.

**Indexing**: Database tables are indexed on frequently queried fields. For Recommendation Engine, indexes cover Ranking Model (MF/SVD) and Feature Store for fast lookups.

**Asynchronous processing**: Non-critical background work (e.g., analytics, cleanup, notifications) is offloaded to message queues and processed asynchronously, keeping the request path fast.

**Resource isolation**: CPU and memory are allocated per service (containers with cgroup limits). This prevents a single misbehaving service from degrading the entire system.

**Metrics for Recommendation Engine**:

| Metric | Target | How to Measure |
|---|---|---|
| P99 latency | < 1s | Load test with realistic traffic |
| Throughput | 1K RPS | Request rate under peak load |
| Error rate | < 0.1% | 5xx / total requests |
| Cache hit ratio | > 90% | cache_hits / (cache_hits + misses) |
| Resource utilization | < 80% CPU, < 85% memory | Container metrics |

**Real-world implementations**

- **Google's HTTP Load Balancer**: Global load balancing with edge PoPs; routes users to the nearest healthy backend.
- **Cloudflare**: Edge cache with Argo Smart Routing that dynamically routes traffic to avoid congestion.
- **Redis**: Used as an application cache with configurable eviction policies (LRU, LFU, TTL).

### CAP Theorem and Consistency Trade-offs

**What it means**

The CAP Theorem states that in a distributed system, you can only have two of three guarantees: **Consistency** (every read returns the latest write), **Availability** (every request gets a response), and **Partition tolerance** (the system continues to operate despite network partitions). Since network partitions are inevitable in distributed systems like Recommendation Engine, the real choice is between CP (consistent + partitioned) and AP (available + partitioned).

**Why it matters**

Recommendation Engine must decide which two guarantees to prioritize. For user preferences, viewing history, purchase history data, strong consistency (CP) is critical — users must see the most recent data. For public item metadata, aggregate trends, anonymized stats data, availability (AP) is more important — the system should remain responsive even during network issues.

**How it works**

**CP (Consistent + Partition-tolerant)**: During a partition, the system trades availability for consistency. Writes are rejected or delayed until the partition heals. Reads return the latest committed value. This is appropriate for user preferences, viewing history, purchase history in Recommendation Engine.

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

**AP (Available + Partition-tolerant)**: During a partition, the system trades consistency for availability. Both sides accept writes; conflicts are resolved later (last-write-wins, merge, or application-level conflict resolution). This is appropriate for public item metadata, aggregate trends, anonymized stats in Recommendation Engine.

**PACELC (extending CAP)**: The PACELC theorem says that even when the network is not partitioned (the "else" case in CAP), you must choose between latency (L) and consistency (C). Recommendation Engine uses:
- **Racing reads**: Serve from the nearest replica for speed (low latency, eventual consistency).
- **Linearizable reads**: Always read from the primary (high latency, strong consistency).

The choice is made per request based on whether the data is user preferences, viewing history, purchase history (strong consistency) or public item metadata, aggregate trends, anonymized stats (fast reads).

**Trade-offs**:

| System Type | CP Use Cases | AP Use Cases |
|---|---|---|
| Recommendation Engine | user preferences, viewing history, purchase history | public item metadata, aggregate trends, anonymized stats |

**Real-world implementations**

- **etcd**: CP system using Raft consensus; used for service discovery and configuration in Kubernetes.
- **Cassandra**: AP system with tunable consistency; used for time-series data and user sessions.
- **Google Spanner**: CP with external consistency via TrueTime API; used for global financial transactions.
- **DynamoDB**: AP by default, but supports strongly consistent reads (CP mode) on demand.

### Encryption and Key Management

**What it means**

Encryption and Key Management in Recommendation Engine ensures that data is protected both at rest (stored on disk) and in transit (moving between services). Key management governs how encryption keys are generated, stored, rotated, and accessed — without proper key management, encryption provides a false sense of security.

**Why it matters**

Recommendation Engine handles user preferences, viewing history, purchase history that must be encrypted both at rest and in transit. Serving sub-100ms recommendations for millions of users while keeping models fresh and handling cold-start users/items requires careful key management: keys must be rotated regularly, scoped to prevent cross-contamination, and audited for compliance. A single key compromise could expose sensitive data.

**How it works**

**At-rest encryption**: Data stored in Candidate Generator (two-tower NN), Ranking Model (MF/SVD) and databases is encrypted using AES-256-GCM. The Data Encryption Key (DEK) is generated per data partition and encrypted with a Key Encryption Key (KEK) managed by a KMS (AWS KMS, GCP KMS, HashiCorp Vault). Keys are regionally scoped — only data belonging to a region can be decrypted by that region's KEK.

**In-transit encryption**: All inter-service communication uses TLS 1.3 or mTLS for service-to-service auth. Cross-region communication of public item metadata, aggregate trends, anonymized stats uses TLS + optional application-level encryption. user preferences, viewing history, purchase history is NEVER transmitted in plaintext or across region boundaries.

**Key hierarchy**:
```
Master Key (HSM-backed, KMS-managed)
  └─ KEK (per region, per service)
     └─ DEK (per data partition, rotated every 90 days)
        └─ Data (encrypted with DEK)
```

**Key rotation**: KEKs rotate annually (automatic via KMS); DEKs rotate per object or per 90 days. Applications handle key version headers transparently — a DEK version is stored alongside the encrypted data.

**Cross-region key sharing**: For non-restricted data (public item metadata, aggregate trends, anonymized stats), a shared key is imported into each region's KMS. Restricted data NEVER uses cross-region keys — each region's KMS holds only that region's keys.

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
public class DataEncryptionService {

    private final AWSKMS kms;
    @Value("${app.region}")
    private String region;
    @Value("${app.encryption.dek-ttl-minutes:1440}")
    private int dekTtlMinutes;

    private final Map<String, SecretKey> dekCache = new ConcurrentHashMap<>();

    public EncryptedData encrypt(String plaintext, String partitionId) {
        SecretKey dek = getOrCreateDek(partitionId);
        byte[] ciphertext = CryptoUtils.encrypt(plaintext.getBytes(StandardCharsets.UTF_8), dek);
        String dekCiphertext = kms.encrypt(EncryptRequest.builder()
            .keyId("arn:aws:kms:" + region + ":master-key")
            .plaintext(SdkBytes.fromByteArray(dek.getEncoded()))
            .build()).ciphertextBlob().asByteArray();
        return new EncryptedData(ciphertext, dekCiphertext, Instant.now());
    }

    private SecretKey getOrCreateDek(String partitionId) {
        return dekCache.computeIfAbsent(partitionId, id -> {
            try {
                return KeyGenerator.getInstance("AES").generateKey();
            } catch (NoSuchAlgorithmException e) {
                throw new IllegalStateException("Cannot generate DEK", e);
            }
        });
    }
}
```

*Spring Boot encryption service: DEKs are cached per-partition with TTL. Each DEK is encrypted via AWS KMS using a regional master key. The encrypted DEK (ciphertext) is stored alongside the data — only the KMS for that region can decrypt it.*

**Real-world implementations**

- **AWS KMS**: Managed HSM-backed key service; supports automatic key rotation and custom key stores.
- **HashiCorp Vault**: Open-source key management; supports transit encryption (encrypt/decrypt without storing keys).
- **Google Cloud KMS**: Hardware-backed key management with IAM-based access control.

### Authentication and Authorization

**What it means**

Authentication and Authorization (AuthN/AuthZ) in Recommendation Engine control who can access the system and what they can do. Authentication verifies identity; authorization determines permissions. In a distributed system like Recommendation Engine, auth must work across multiple nodes while respecting data boundaries — a user authenticated in one region should not have their session data or tokens replicated to regions where it is not permitted.

**Why it matters**

Recommendation Engine must verify identity at the edge and enforce authorization at every service boundary. user preferences, viewing history, purchase history must be protected — only users with appropriate roles should access it. At the same time, public item metadata, aggregate trends, anonymized stats data should be accessible to a wider audience with minimal friction.

**How it works**

**Authentication (who are you?)**:
- **JWT tokens**: Users authenticate through their home region's identity provider. The region returns a JWT (JSON Web Token) signed by a regional signing key. Tokens include claims like `iss` (issuer region), `sub` (subject/user ID), `home_region`, `roles`, and `exp` (expiry). Tokens are scoped per region — a token issued by region A cannot access restricted data in region B.
- **mTLS for service-to-service**: Internal services authenticate each other using mutual TLS certificates issued by a per-region Certificate Authority (CA). No shared secrets cross region boundaries.
- **Session management**: Sessions are stored regionally (Redis) and never replicated cross-region for restricted data. Session IDs are opaque UUIDs; the session store maps session ID → user context.

**Authorization (what can you do?)**:
- **RBAC (Role-Based Access Control)**: Users are assigned roles per region. Common roles: `region_admin` (full access to region data), `auditor` (read-only audit), `viewer` (read public data only). Roles are stored in the regional database and cached locally for sub-1ms lookups.
- **ABAC (Attribute-Based Access Control)**: Fine-grained permissions based on attributes (e.g., `home_region == request_region AND role == admin`). This allows expressing complex policies like "users can only access restricted data in their home region."
- **Resource-level authorization**: Each request is checked against an ACL (Access Control List) that specifies which roles can access which resources. For Recommendation Engine, restricted resources require the `admin` role + matching region.

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
public class AuthorizationService {

    private final UserTokenRepository tokenRepository;
    @Value("${app.region}")
    private String currentRegion;

    public boolean canAccessResource(String userId, String resourceRegion,
                                     String action, JWTClaims claims) {
        String userHomeRegion = claims.getStringClaim("home_region");
        List<String> roles = claims.getStringListClaim("roles");

        if (!roles.contains(action)) {
            return false;
        }

        if (resourceRegion.equals(userHomeRegion)) {
            return true;
        }

        if (resourceRegion.equals("global")) {
            return roles.contains("global_reader");
        }

        return false;
    }
}

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1")
public class RegionController {
    private final AuthorizationService authService;

    @GetMapping("/data/{region}/profile")
    public ResponseEntity<?> getProfile(
            @PathVariable String region,
            @RequestHeader("Authorization") String token) {
        JWTClaims claims = JwtUtils.parseAndValidate(token, currentRegion);

        if (!authService.canAccessResource(
                claims.getStringClaim("sub"), region, "read", claims)) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
        }

        return ResponseEntity.ok(profileService.getByRegion(region));
    }
}
```

*Spring Boot authorization service: checks both the user's role and whether the requested resource violates region boundaries. The `canAccessResource` method returns false if a user from region EU tries to access restricted data in region US.*

**Real-world implementations**

- **Auth0**: JWT-based authentication with regional endpoints; supports custom rules for ABAC.
- **Okta**: Multi-region identity management with adaptive MFA and ThreatInsight for anomaly detection.
- **AWS Cognito**: Regional user pools with IAM integration; tokens are region-scoped by default.

### Security Threats and Mitigations

**What it means**

Security Threats and Mitigations catalog the attack surface of Recommendation Engine, the most likely threats, and the corresponding defenses. Every distributed system has unique threat vectors — Recommendation Engine is no exception.

**Why it matters**

Recommendation Engine handles user preferences, viewing history, purchase history that attackers might target. Serving sub-100ms recommendations for millions of users while keeping models fresh and handling cold-start users/items expands the attack surface: more nodes, more network paths, more failure modes. Without proper threat modeling, a single vulnerability could expose sensitive data across the entire system.

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

**Data exfiltration prevention**: Recommendation Engine enforces data residency by design — user preferences, viewing history, purchase history is never replicated cross-region. The replication layer checks a data classification label before allowing cross-region copy. A database-level policy (e.g., PostgreSQL RLS) also blocks cross-region queries for restricted partitions.

**mTLS enforcement**: All service-to-service communication uses mutual TLS. Certificates are issued by a per-region CA and rotated every 30 days. Services must present a valid certificate to communicate — no plaintext connections are allowed.

**PII redaction**: Application logs are scanned for PII patterns (email, phone, credit card) using an automated redaction layer (e.g., AWS Macie, Google DLP). public item metadata, aggregate trends, anonymized stats is logged freely; restricted fields are masked or dropped before logging.

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

**Audit trail**: All security-relevant events (auth, data access, config changes) are written to an append-only audit log with cryptographic integrity (HMAC per entry). The log covers user preferences, viewing history, purchase history access — who accessed what, when, and from where.

**Real-world implementations**

- **Cloudflare**: Zero-trust model (All Connections to All Networks) with mTLS everywhere; uses GeoIP blocking and rate limiting for DDoS mitigation.
- **Google BeyondCorp**: Zero-trust network security model; all access is authenticated and authorized at the request level.

### Observability and Logging

**What it means**

Observability and Logging in Recommendation Engine provide visibility into system behavior through three pillars: **metrics** (aggregates and counters), **logs** (structured event records), and **traces** (distributed request timelines). Together, these signals allow operators to debug issues, detect anomalies, and verify SLA compliance.

**Why it matters**

Distributed systems like Recommendation Engine are inherently opaque — failures can cascade across services in unexpected ways. Without good observability, a single slow dependency can cause widespread timeouts that are nearly impossible to diagnose. Serving sub-100ms recommendations for millions of users while keeping models fresh and handling cold-start users/items makes observability even more critical: operators need to see cross-region latency, regional failures, and data-residency violations.

**How it works**

**Metrics**: Recommendation Engine instruments every service with Prometheus-style metrics:
- **Request rate, error rate, duration (the "RED" metrics)**: Tracks per-endpoint HTTP latency and error counts.
- **System metrics**: CPU, memory, disk I/O, network throughput per node.
- **Business metrics**: For Recommendation Engine, this includes metrics like "Ranking Model (MF/SVD) fill rate" and "reservation conflict rate".

Metrics are aggregated in a time-series database (Prometheus, VictoriaMetrics) and visualized in Grafana dashboards with alerts via PagerDuty.

**Logs**: Recommendation Engine uses structured logging (JSON format) with standardized fields:
- `timestamp`: ISO 8601 UTC
- `level`: DEBUG, INFO, WARN, ERROR
- `service`: originating service name
- `trace_id`: distributed trace identifier (for correlation)
- `span_id`: current operation span
- `region`: the region that processed the request
- `data_class`: RESTRICTED or NON_RESTRICTED

user preferences, viewing history, purchase history access is logged with full context (user, action, resource). public item metadata, aggregate trends, anonymized stats logs are aggregated and may have reduced retention.

**Distributed tracing**: Every request is assigned a trace ID at the edge. The trace propagates through all downstream services via HTTP headers. A tracing backend (Jaeger, Tempo, Zipkin) reconstructs the full request timeline, showing latency at each hop. For Recommendation Engine, traces include region boundaries — a cross-region call is annotated as such.

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

**Alerting**: Recommendation Engine defines SLO-based alerts:
- **Latency**: P99 > 1s for 5 minutes → page.
- **Error rate**: > 1% for 10 minutes → page.
- **Availability**: < 99.5% for 15 minutes → page.
- **Data residency violation**: any restricted data detected outside its region → critical page.

**Java/Spring Boot Implementation**

```java
@Component
@RequiredArgsConstructor
@Slf4j
public class ObservabilityContext {

    @Value("${app.region}")
    private String region;

    public void logAccess(String userId, String resource, String action,
                          boolean restricted) {
        log.info("access_event userId={} resource={} action={} region={} data_class={}",
            userId, resource, action, region, restricted ? "RESTRICTED" : "NON_RESTRICTED");
    }
}

@RestController
@RequiredArgsConstructor
@Slf4j
public class ApiController {
    private final ObservabilityContext obs;
    private final UserService userService;

    @GetMapping("/api/v1/profile")
    public ResponseEntity<ProfileResponse> getProfile(
            @AuthenticationPrincipal UserDetails user) {
        String traceId = MDC.get("traceId");
        long start = System.nanoTime();

        try {
            ProfileResponse response = userService.getProfile(user.getId());
            obs.logAccess(user.getId(), "profile", "read", true);

            return ResponseEntity.ok(response);
        } finally {
            long durationMs = (System.nanoTime() - start) / 1_000_000;
            log.info("profile_read traceId={} latencyMs={} region={}",
                traceId, durationMs, obs.region);
        }
    }
}
```

*Spring Boot observability: the `ObservabilityContext` logs structured access events with data classification. The controller records latency and trace ID for every request, enabling SLO-based alerting.*

**Real-world implementations**

- **Netflix OSS (Atlas + Zipkin + Servo)**: Metrics via Atlas, traces via Zipkin, instrumented via Servo. Scales to over 700 billion requests/day.
- **Google SRE Workbook**: Comprehensive observability with SLI/SLO/SLI definition; uses Borgmon for metrics and Dapper for tracing.
- **AWS Observability**: CloudWatch for metrics, X-Ray for tracing, CloudWatch Logs for structured logs.

### Replication Strategies

**What it means**

Replication Strategies determine how data and state are copied across multiple nodes in Recommendation Engine. The choice of strategy determines the trade-off between consistency, availability, and latency.

**Why it matters**

Recommendation Engine must replicate data to prevent loss and serve reads from multiple nodes. The replication strategy determines whether the system favors consistency (strong reads) or availability (always writable), and how it handles cross-node failure.

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

**Trade-offs for Recommendation Engine**:

| Strategy | Use Case | Pros | Cons |
|---|---|---|---|
| Leader-based | user preferences, viewing history, purchase history | Strong consistency, simple | Write bottleneck, leader failure risk |
| Multi-leader | public item metadata, aggregate trends, anonymized stats | Low-latency global writes | Conflict resolution, complex |
| Leaderless | Caching, counters | High availability, no bottleneck | Eventual consistency, read repair overhead |

**Real-world implementations**

- **Redis**: Leader-follower replication with asynchronous replication; Sentinel handles failover.
- **Apache Kafka**: Leader-based partition replication with ISR (in-sync replica) — writes go to the leader, followers replicate.
- **Cassandra**: Tunable consistency with leaderless quorum (R + W > N).
- **DynamoDB Global Tables**: Multi-master active-active across regions.

### Failure Detection and Membership

**What it means**

Failure Detection and Membership is the mechanism by which Recommendation Engine determines which nodes are alive and part of the cluster. Membership is the list of known nodes; failure detection is the process of updating that list when nodes fail or recover.

**Why it matters**

Recommendation Engine must route requests only to healthy nodes and trigger failover when a node goes down. False positives (healthy nodes marked as dead) cause unnecessary failovers and data loss. False negatives (dead nodes not detected) cause failed requests and degraded performance.

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

### High Availability and Scalability

**What it means**

High Availability and Scalability determines how Recommendation Engine continues operating when nodes or entire zones fail, and how capacity is added as demand grows. HA is about minimizing downtime; scalability is about maintaining performance as load increases.

**Why it matters**

Recommendation Engine must stay operational even when individual nodes, availability zones, or entire regions fail. At the same time, it must scale horizontally to handle traffic spikes without degrading latency. The two are intertwined: the replication strategy, failure detection, and load balancing all contribute to both HA and scalability.

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

**Load balancing**: A load balancer distributes incoming requests across healthy nodes. Algorithms include round-robin, least connections, and weighted routing. Health checks ensure traffic only goes to healthy nodes. For Recommendation Engine, the load balancer also considers Candidate Generator (two-tower NN) when routing.

**Auto-scaling**: The system automatically adds or removes nodes based on metrics (CPU, memory, request rate). Scale-out policies add nodes when load exceeds a threshold; scale-in policies remove nodes during low load. For stateful services like Recommendation Engine, scale-out involves rebalancing partitions (moving data and connections to the new node).

**Failover and recovery**: When a node fails, the load balancer detects it (via health checks or failure detection) and stops sending traffic. A new node is provisioned (or a standby is promoted) and begins serving. For Recommendation Engine, failover must preserve user preferences, viewing history, purchase history data — this is achieved through replication with a quorum of healthy nodes.

**Scalability patterns**:

1. **Horizontal partitioning (sharding)**: Split data by a partition key (e.g., user_id, session_id) and distribute partitions across nodes. New nodes take ownership of additional partitions.

2. **Consistent hashing**: Minimize data movement on scale-out — only 1/N of the data moves to the new node. Nodes and partitions are placed on a ring; a request for key X is routed to the next node clockwise from hash(X).

3. **Connection draining**: When scaling in, existing connections are allowed to complete before the node is shut down. For Recommendation Engine, this means draining active A sessions gracefully.

**Real-world implementations**

- **Netflix OSS (Eureka + Zuul + Ribbon)**: Service discovery with Eureka, edge routing with Zuul, and client-side load balancing with Ribbon. Scales to thousands of instances.
- **Kubernetes HPA + VPA**: Horizontal Pod Autoscaler scales pods based on CPU/memory; Vertical Pod Autoscaler adjusts resource requests based on historical usage.
- **AWS ALB + Auto Scaling Groups**: Application Load Balancer with auto-scaling groups across AZs; health checks replace unhealthy instances automatically.

### Performance and Optimization

**What it means**

Performance and Optimization covers the techniques Recommendation Engine uses to achieve low latency, high throughput, and efficient resource usage. This section examines the key performance metrics, bottlenecks, and optimizations specific to the system.

**Why it matters**

Recommendation Engine faces competing pressures: users demand low latency, the system must handle high throughput, and infrastructure costs must be controlled. The optimizations applied at the data, compute, and network layers determine whether the system meets its SLA.

**How it works**

**Latency layers**: Latency in Recommendation Engine comes from three layers:
1. **Network**: Round-trip time from client to the nearest edge node / load balancer.
2. **Application**: Request processing time on the server (CPU, I/O, lock contention).
3. **Data**: Time to read/write from storage (cache hit vs. database query).

The 99th-percentile latency is the key metric for user-facing systems — it determines the worst-case experience.

**Caching strategies**: Recommendation Engine uses multiple cache layers:
- **Edge cache**: Static assets (images, CSS, JS) served from a CDN at the edge. For Recommendation Engine, this caches public item metadata, aggregate trends, anonymized stats that doesn't change frequently.
- **Application cache**: In-memory cache (e.g., Redis, Memcached) for frequently accessed data. Cache-aside pattern: application checks cache first, falls back to database on miss.
- **Local cache**: In-process cache (e.g., Caffeine, Guava) for data accessed within a single request. Avoids network round-trips.

**Batching and pipelining**: Recommendation Engine batches small operations (e.g., writes, log flushes) to amortize per-operation overhead. Pipelining allows multiple requests to be in flight simultaneously.

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

**Connection pooling**: Recommendation Engine maintains a pool of database connections to avoid the TCP handshake overhead on every request. Pool size is tuned to match the database's capacity.

**Compression**: Responses are compressed (gzip, zstd) for clients that support it. At the network layer, gRPC uses HPACK header compression.

**Indexing**: Database tables are indexed on frequently queried fields. For Recommendation Engine, indexes cover Ranking Model (MF/SVD) and Feature Store for fast lookups.

**Asynchronous processing**: Non-critical background work (e.g., analytics, cleanup, notifications) is offloaded to message queues and processed asynchronously, keeping the request path fast.

**Resource isolation**: CPU and memory are allocated per service (containers with cgroup limits). This prevents a single misbehaving service from degrading the entire system.

**Metrics for Recommendation Engine**:

| Metric | Target | How to Measure |
|---|---|---|
| P99 latency | < 1s | Load test with realistic traffic |
| Throughput | 1K RPS | Request rate under peak load |
| Error rate | < 0.1% | 5xx / total requests |
| Cache hit ratio | > 90% | cache_hits / (cache_hits + misses) |
| Resource utilization | < 80% CPU, < 85% memory | Container metrics |

**Real-world implementations**

- **Google's HTTP Load Balancer**: Global load balancing with edge PoPs; routes users to the nearest healthy backend.
- **Cloudflare**: Edge cache with Argo Smart Routing that dynamically routes traffic to avoid congestion.
- **Redis**: Used as an application cache with configurable eviction policies (LRU, LFU, TTL).

### CAP Theorem and Consistency Trade-offs

**What it means**

The CAP Theorem states that in a distributed system, you can only have two of three guarantees: **Consistency** (every read returns the latest write), **Availability** (every request gets a response), and **Partition tolerance** (the system continues to operate despite network partitions). Since network partitions are inevitable in distributed systems like Recommendation Engine, the real choice is between CP (consistent + partitioned) and AP (available + partitioned).

**Why it matters**

Recommendation Engine must decide which two guarantees to prioritize. For user preferences, viewing history, purchase history data, strong consistency (CP) is critical — users must see the most recent data. For public item metadata, aggregate trends, anonymized stats data, availability (AP) is more important — the system should remain responsive even during network issues.

**How it works**

**CP (Consistent + Partition-tolerant)**: During a partition, the system trades availability for consistency. Writes are rejected or delayed until the partition heals. Reads return the latest committed value. This is appropriate for user preferences, viewing history, purchase history in Recommendation Engine.

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

**AP (Available + Partition-tolerant)**: During a partition, the system trades consistency for availability. Both sides accept writes; conflicts are resolved later (last-write-wins, merge, or application-level conflict resolution). This is appropriate for public item metadata, aggregate trends, anonymized stats in Recommendation Engine.

**PACELC (extending CAP)**: The PACELC theorem says that even when the network is not partitioned (the "else" case in CAP), you must choose between latency (L) and consistency (C). Recommendation Engine uses:
- **Racing reads**: Serve from the nearest replica for speed (low latency, eventual consistency).
- **Linearizable reads**: Always read from the primary (high latency, strong consistency).

The choice is made per request based on whether the data is user preferences, viewing history, purchase history (strong consistency) or public item metadata, aggregate trends, anonymized stats (fast reads).

**Trade-offs**:

| System Type | CP Use Cases | AP Use Cases |
|---|---|---|
| Recommendation Engine | user preferences, viewing history, purchase history | public item metadata, aggregate trends, anonymized stats |

**Real-world implementations**

- **etcd**: CP system using Raft consensus; used for service discovery and configuration in Kubernetes.
- **Cassandra**: AP system with tunable consistency; used for time-series data and user sessions.
- **Google Spanner**: CP with external consistency via TrueTime API; used for global financial transactions.
- **DynamoDB**: AP by default, but supports strongly consistent reads (CP mode) on demand.

### Encryption and Key Management

**What it means**

Encryption and Key Management in Recommendation Engine ensures that data is protected both at rest (stored on disk) and in transit (moving between services). Key management governs how encryption keys are generated, stored, rotated, and accessed — without proper key management, encryption provides a false sense of security.

**Why it matters**

Recommendation Engine handles user preferences, viewing history, purchase history that must be encrypted both at rest and in transit. Serving sub-100ms recommendations for millions of users while keeping models fresh and handling cold-start users/items requires careful key management: keys must be rotated regularly, scoped to prevent cross-contamination, and audited for compliance. A single key compromise could expose sensitive data.

**How it works**

**At-rest encryption**: Data stored in Candidate Generator (two-tower NN), Ranking Model (MF/SVD) and databases is encrypted using AES-256-GCM. The Data Encryption Key (DEK) is generated per data partition and encrypted with a Key Encryption Key (KEK) managed by a KMS (AWS KMS, GCP KMS, HashiCorp Vault). Keys are regionally scoped — only data belonging to a region can be decrypted by that region's KEK.

**In-transit encryption**: All inter-service communication uses TLS 1.3 or mTLS for service-to-service auth. Cross-region communication of public item metadata, aggregate trends, anonymized stats uses TLS + optional application-level encryption. user preferences, viewing history, purchase history is NEVER transmitted in plaintext or across region boundaries.

**Key hierarchy**:
```
Master Key (HSM-backed, KMS-managed)
  └─ KEK (per region, per service)
     └─ DEK (per data partition, rotated every 90 days)
        └─ Data (encrypted with DEK)
```

**Key rotation**: KEKs rotate annually (automatic via KMS); DEKs rotate per object or per 90 days. Applications handle key version headers transparently — a DEK version is stored alongside the encrypted data.

**Cross-region key sharing**: For non-restricted data (public item metadata, aggregate trends, anonymized stats), a shared key is imported into each region's KMS. Restricted data NEVER uses cross-region keys — each region's KMS holds only that region's keys.

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
public class DataEncryptionService {

    private final AWSKMS kms;
    @Value("${app.region}")
    private String region;
    @Value("${app.encryption.dek-ttl-minutes:1440}")
    private int dekTtlMinutes;

    private final Map<String, SecretKey> dekCache = new ConcurrentHashMap<>();

    public EncryptedData encrypt(String plaintext, String partitionId) {
        SecretKey dek = getOrCreateDek(partitionId);
        byte[] ciphertext = CryptoUtils.encrypt(plaintext.getBytes(StandardCharsets.UTF_8), dek);
        String dekCiphertext = kms.encrypt(EncryptRequest.builder()
            .keyId("arn:aws:kms:" + region + ":master-key")
            .plaintext(SdkBytes.fromByteArray(dek.getEncoded()))
            .build()).ciphertextBlob().asByteArray();
        return new EncryptedData(ciphertext, dekCiphertext, Instant.now());
    }

    private SecretKey getOrCreateDek(String partitionId) {
        return dekCache.computeIfAbsent(partitionId, id -> {
            try {
                return KeyGenerator.getInstance("AES").generateKey();
            } catch (NoSuchAlgorithmException e) {
                throw new IllegalStateException("Cannot generate DEK", e);
            }
        });
    }
}
```

*Spring Boot encryption service: DEKs are cached per-partition with TTL. Each DEK is encrypted via AWS KMS using a regional master key. The encrypted DEK (ciphertext) is stored alongside the data — only the KMS for that region can decrypt it.*

**Real-world implementations**

- **AWS KMS**: Managed HSM-backed key service; supports automatic key rotation and custom key stores.
- **HashiCorp Vault**: Open-source key management; supports transit encryption (encrypt/decrypt without storing keys).
- **Google Cloud KMS**: Hardware-backed key management with IAM-based access control.

### Authentication and Authorization

**What it means**

Authentication and Authorization (AuthN/AuthZ) in Recommendation Engine control who can access the system and what they can do. Authentication verifies identity; authorization determines permissions. In a distributed system like Recommendation Engine, auth must work across multiple nodes while respecting data boundaries — a user authenticated in one region should not have their session data or tokens replicated to regions where it is not permitted.

**Why it matters**

Recommendation Engine must verify identity at the edge and enforce authorization at every service boundary. user preferences, viewing history, purchase history must be protected — only users with appropriate roles should access it. At the same time, public item metadata, aggregate trends, anonymized stats data should be accessible to a wider audience with minimal friction.

**How it works**

**Authentication (who are you?)**:
- **JWT tokens**: Users authenticate through their home region's identity provider. The region returns a JWT (JSON Web Token) signed by a regional signing key. Tokens include claims like `iss` (issuer region), `sub` (subject/user ID), `home_region`, `roles`, and `exp` (expiry). Tokens are scoped per region — a token issued by region A cannot access restricted data in region B.
- **mTLS for service-to-service**: Internal services authenticate each other using mutual TLS certificates issued by a per-region Certificate Authority (CA). No shared secrets cross region boundaries.
- **Session management**: Sessions are stored regionally (Redis) and never replicated cross-region for restricted data. Session IDs are opaque UUIDs; the session store maps session ID → user context.

**Authorization (what can you do?)**:
- **RBAC (Role-Based Access Control)**: Users are assigned roles per region. Common roles: `region_admin` (full access to region data), `auditor` (read-only audit), `viewer` (read public data only). Roles are stored in the regional database and cached locally for sub-1ms lookups.
- **ABAC (Attribute-Based Access Control)**: Fine-grained permissions based on attributes (e.g., `home_region == request_region AND role == admin`). This allows expressing complex policies like "users can only access restricted data in their home region."
- **Resource-level authorization**: Each request is checked against an ACL (Access Control List) that specifies which roles can access which resources. For Recommendation Engine, restricted resources require the `admin` role + matching region.

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
public class AuthorizationService {

    private final UserTokenRepository tokenRepository;
    @Value("${app.region}")
    private String currentRegion;

    public boolean canAccessResource(String userId, String resourceRegion,
                                     String action, JWTClaims claims) {
        String userHomeRegion = claims.getStringClaim("home_region");
        List<String> roles = claims.getStringListClaim("roles");

        if (!roles.contains(action)) {
            return false;
        }

        if (resourceRegion.equals(userHomeRegion)) {
            return true;
        }

        if (resourceRegion.equals("global")) {
            return roles.contains("global_reader");
        }

        return false;
    }
}

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1")
public class RegionController {
    private final AuthorizationService authService;

    @GetMapping("/data/{region}/profile")
    public ResponseEntity<?> getProfile(
            @PathVariable String region,
            @RequestHeader("Authorization") String token) {
        JWTClaims claims = JwtUtils.parseAndValidate(token, currentRegion);

        if (!authService.canAccessResource(
                claims.getStringClaim("sub"), region, "read", claims)) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
        }

        return ResponseEntity.ok(profileService.getByRegion(region));
    }
}
```

*Spring Boot authorization service: checks both the user's role and whether the requested resource violates region boundaries. The `canAccessResource` method returns false if a user from region EU tries to access restricted data in region US.*

**Real-world implementations**

- **Auth0**: JWT-based authentication with regional endpoints; supports custom rules for ABAC.
- **Okta**: Multi-region identity management with adaptive MFA and ThreatInsight for anomaly detection.
- **AWS Cognito**: Regional user pools with IAM integration; tokens are region-scoped by default.

### Security Threats and Mitigations

**What it means**

Security Threats and Mitigations catalog the attack surface of Recommendation Engine, the most likely threats, and the corresponding defenses. Every distributed system has unique threat vectors — Recommendation Engine is no exception.

**Why it matters**

Recommendation Engine handles user preferences, viewing history, purchase history that attackers might target. Serving sub-100ms recommendations for millions of users while keeping models fresh and handling cold-start users/items expands the attack surface: more nodes, more network paths, more failure modes. Without proper threat modeling, a single vulnerability could expose sensitive data across the entire system.

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

**Data exfiltration prevention**: Recommendation Engine enforces data residency by design — user preferences, viewing history, purchase history is never replicated cross-region. The replication layer checks a data classification label before allowing cross-region copy. A database-level policy (e.g., PostgreSQL RLS) also blocks cross-region queries for restricted partitions.

**mTLS enforcement**: All service-to-service communication uses mutual TLS. Certificates are issued by a per-region CA and rotated every 30 days. Services must present a valid certificate to communicate — no plaintext connections are allowed.

**PII redaction**: Application logs are scanned for PII patterns (email, phone, credit card) using an automated redaction layer (e.g., AWS Macie, Google DLP). public item metadata, aggregate trends, anonymized stats is logged freely; restricted fields are masked or dropped before logging.

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

**Audit trail**: All security-relevant events (auth, data access, config changes) are written to an append-only audit log with cryptographic integrity (HMAC per entry). The log covers user preferences, viewing history, purchase history access — who accessed what, when, and from where.

**Real-world implementations**

- **Cloudflare**: Zero-trust model (All Connections to All Networks) with mTLS everywhere; uses GeoIP blocking and rate limiting for DDoS mitigation.
- **Google BeyondCorp**: Zero-trust network security model; all access is authenticated and authorized at the request level.

### Observability and Logging

**What it means**

Observability and Logging in Recommendation Engine provide visibility into system behavior through three pillars: **metrics** (aggregates and counters), **logs** (structured event records), and **traces** (distributed request timelines). Together, these signals allow operators to debug issues, detect anomalies, and verify SLA compliance.

**Why it matters**

Distributed systems like Recommendation Engine are inherently opaque — failures can cascade across services in unexpected ways. Without good observability, a single slow dependency can cause widespread timeouts that are nearly impossible to diagnose. Serving sub-100ms recommendations for millions of users while keeping models fresh and handling cold-start users/items makes observability even more critical: operators need to see cross-region latency, regional failures, and data-residency violations.

**How it works**

**Metrics**: Recommendation Engine instruments every service with Prometheus-style metrics:
- **Request rate, error rate, duration (the "RED" metrics)**: Tracks per-endpoint HTTP latency and error counts.
- **System metrics**: CPU, memory, disk I/O, network throughput per node.
- **Business metrics**: For Recommendation Engine, this includes metrics like "Ranking Model (MF/SVD) fill rate" and "reservation conflict rate".

Metrics are aggregated in a time-series database (Prometheus, VictoriaMetrics) and visualized in Grafana dashboards with alerts via PagerDuty.

**Logs**: Recommendation Engine uses structured logging (JSON format) with standardized fields:
- `timestamp`: ISO 8601 UTC
- `level`: DEBUG, INFO, WARN, ERROR
- `service`: originating service name
- `trace_id`: distributed trace identifier (for correlation)
- `span_id`: current operation span
- `region`: the region that processed the request
- `data_class`: RESTRICTED or NON_RESTRICTED

user preferences, viewing history, purchase history access is logged with full context (user, action, resource). public item metadata, aggregate trends, anonymized stats logs are aggregated and may have reduced retention.

**Distributed tracing**: Every request is assigned a trace ID at the edge. The trace propagates through all downstream services via HTTP headers. A tracing backend (Jaeger, Tempo, Zipkin) reconstructs the full request timeline, showing latency at each hop. For Recommendation Engine, traces include region boundaries — a cross-region call is annotated as such.

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

**Alerting**: Recommendation Engine defines SLO-based alerts:
- **Latency**: P99 > 1s for 5 minutes → page.
- **Error rate**: > 1% for 10 minutes → page.
- **Availability**: < 99.5% for 15 minutes → page.
- **Data residency violation**: any restricted data detected outside its region → critical page.

**Java/Spring Boot Implementation**

```java
@Component
@RequiredArgsConstructor
@Slf4j
public class ObservabilityContext {

    @Value("${app.region}")
    private String region;

    public void logAccess(String userId, String resource, String action,
                          boolean restricted) {
        log.info("access_event userId={} resource={} action={} region={} data_class={}",
            userId, resource, action, region, restricted ? "RESTRICTED" : "NON_RESTRICTED");
    }
}

@RestController
@RequiredArgsConstructor
@Slf4j
public class ApiController {
    private final ObservabilityContext obs;
    private final UserService userService;

    @GetMapping("/api/v1/profile")
    public ResponseEntity<ProfileResponse> getProfile(
            @AuthenticationPrincipal UserDetails user) {
        String traceId = MDC.get("traceId");
        long start = System.nanoTime();

        try {
            ProfileResponse response = userService.getProfile(user.getId());
            obs.logAccess(user.getId(), "profile", "read", true);

            return ResponseEntity.ok(response);
        } finally {
            long durationMs = (System.nanoTime() - start) / 1_000_000;
            log.info("profile_read traceId={} latencyMs={} region={}",
                traceId, durationMs, obs.region);
        }
    }
}
```

*Spring Boot observability: the `ObservabilityContext` logs structured access events with data classification. The controller records latency and trace ID for every request, enabling SLO-based alerting.*

**Real-world implementations**

- **Netflix OSS (Atlas + Zipkin + Servo)**: Metrics via Atlas, traces via Zipkin, instrumented via Servo. Scales to over 700 billion requests/day.
- **Google SRE Workbook**: Comprehensive observability with SLI/SLO/SLI definition; uses Borgmon for metrics and Dapper for tracing.
- **AWS Observability**: CloudWatch for metrics, X-Ray for tracing, CloudWatch Logs for structured logs.

### Java and Spring Boot Implementation Guide

```java
@RestController
@RequestMapping("/api/v1")
@RequiredArgsConstructor
public class RecommendationController {
    private final CandidateService candidateService;
    private final RankingService rankingService;
    private final FeatureService featureService;

    @GetMapping("/recommendations")
    public ResponseEntity<List<Recommendation>> getRecommendations(
            @RequestParam String userId,
            @RequestParam(defaultValue = "10") int count,
            @RequestParam(defaultValue = "home") String channel) {

        // Step 1: Get candidate items
        List<Item> candidates = candidateService.getCandidates(userId, count * 5);

        // Step 2: Score candidates with the ranking model
        List<FeatureVector> features = featureService.buildFeatures(userId, candidates, channel);
        List<ScoredItem> scored = rankingService.score(userId, features);

        // Step 3: Sort + return top N
        List<Recommendation> result = scored.stream()
            .sorted(Comparator.comparing(ScoredItem::getScore).reversed())
            .limit(count)
            .map(si -> Recommendation.builder()
                .itemId(si.getItem().getId())
                .score(si.getScore())
                .reason(si.getExplanation())
                .build())
            .collect(Collectors.toList());

        return ResponseEntity.ok(result);
    }

    @PostMapping("/events")
    public ResponseEntity<Void> recordEvent(@RequestBody EventRequest request) {
        eventTracker.track(request.getUserId(), request.getItemId(),
            request.getEventType(), request.getContext());
        return ResponseEntity.accepted().build();
    }
}

@Service
public class TwoTowerRankingService {
    private final TensorFlowModel model;

    public List<ScoredItem> score(String userId, List<FeatureVector> features) {
        // Batch inference for efficiency
        float[][] predictions = model.predict(features);
        List<ScoredItem> results = new ArrayList<>();
        for (int i = 0; i < features.size(); i++) {
            results.add(new ScoredItem(features.get(i).getItem(), predictions[i][0]));
        }
        return results;
    }
}
```

### Real-World Implementations

* **Netflix**: Uses a two-stage pipeline — candidate generation via deep candidate generation network + ranking via deep neural network. Trains daily on Spark; serves via TensorFlow Serving. Uses FAISS for approximate nearest neighbor search over 100M+ item embeddings. Personalization drives 80%+ of watched content.
* **YouTube**: Two-tower neural retrieval (user tower + video tower) → dot product → top videos → deep ranking model. Trains on 1B+ users × 1M+ videos × 100B+ interactions. Uses TPU pods for training; TensorFlow Serving for inference.
* **Amazon**: Item-to-item collaborative filtering ("customers who bought this also bought"). Builds item-item similarity matrix from co-purchase data. Real-time features from user session. Ranking combines item score + inventory + profit margin. 35% of revenue from recommendations.
* **Spotify**: Uses collaborative filtering (matrix factorization) + natural language processing (lyrics, playlist descriptions) + audio features (CNN on raw audio). Discovery Weekly (60M users/week) + Daily Mixes. Two-stage: candidate gen (1000 songs) → ranking (DeepRecNN).
* **TikTok**: Recommendation-first (not follow-based). Uses a two-tower model (user embedding + video embedding) + multi-interaction model (watch time, likes, shares, comments, completions). Trains on 1B+ users × 1M+ videos/day. Candidate generation via ANN over 100M+ videos; ranking via deep model.

### Interview Questions and Answers

#### Beginner Questions

**Q: What is collaborative filtering?**
A: A recommendation approach that uses user-item interaction patterns to make predictions. Two types: (1) User-based: "users who are similar to you also liked..." — find similar users (cosine similarity, Pearson correlation) and recommend their liked items. (2) Item-based: "items similar to X" — find items with similar interaction patterns. Simple but suffers from cold start and scalability issues.

**Q: What is the cold start problem and how do you solve it?**
A: Cold start = no interaction history for new users or items. Solutions: (1) New user → show popular/trending items (global) or ask for initial preferences (onboarding survey). (2) New item → content-based recommendation (match item features to user profiles) until enough interactions accumulate. (3) Hybrid: combine collaborative + content-based. (4) Demographic-based: recommend to users similar to user's demographic.

**Q: What are the different types of recommendation algorithms?**
A: (1) Collaborative filtering: user-based, item-based, matrix factorization. (2) Content-based: recommend items similar to what the user liked before (based on item features). (3) Hybrid: combine collaborative + content-based. (4) Deep learning: neural collaborative filtering, two-tower models, sequence models (RNNs for session-based). (5) Reinforcement learning: maximize long-term reward (engagement).

#### Intermediate Questions

**Q: Explain the difference between user-based and item-based collaborative filtering.**
A: User-based CF: find similar users (users who rated items similarly) → recommend items those similar users liked. Item-based CF: find similar items (items rated similarly by the same users) → recommend items similar to what the user already liked. Item-based is more stable (items change less often than users) and scales better for large user bases — Amazon's original "customers who bought this" is item-based.

**Q: What is matrix factorization and how does it work?**
A: Factorize the user-item interaction matrix R (m users × n items) into U (m × k) and V (n × k) where k << min(m,n). Each user and item is represented as a k-dimensional latent vector. Prediction = user_vector · item_vector. Training: minimize (r_ui - u_i · v_j)² + regularization. Algorithms: SVD, FunkSVD, ALS (alternating least squares — parallelizable), SGD (stochastic gradient descent). Netflix Prize used matrix factorization on 100M ratings.

**Q: How do you evaluate recommendation quality offline?**
A: (1) Precision@K: fraction of recommended items that are relevant (in the held-out test set). (2) Recall@K: fraction of relevant items that were recommended. (3) NDCG (Normalized Discounted Cumulative Gain): considers ranking position — top recommendations matter more. (4) MAP (Mean Average Precision). (5) MRR (Mean Reciprocal Rank). Split: leave-one-out (last interaction as test) or temporal split (last 20% of time). Offline metrics don't always correlate with business outcomes — always validate online.

**Q: What is the two-stage recommendation pipeline?**
A: Stage 1 (Candidate Generation): From 100M+ items, retrieve 100-1000 potentially relevant candidates quickly. Use approximate methods: collaborative filtering, content-based, popularity, ANN (FAISS). Stage 2 (Ranking): Take candidates → compute 100+ features per user-item pair → ML model scores/ranks → return top 10. This decomposition balances scale (ANN) with precision (ML ranking).

#### Advanced Questions

**Q: How would you design a real-time recommendation system for 1B users?**

A: (1) **Two-stage pipeline**: Candidate generation (1000 items) → ranking (top 10). (2) **Feature store**: Real-time features (last click, session context) in Redis (100M+ keys) + batch features (user profile, item metadata) in S3/Hive. Feature computation: Spark for batch (daily), Flink/Flink SQL for streaming (per-event updates). (3) **Candidate generation**: Approximate Nearest Neighbor over item embeddings (100M items) using FAISS/Annoy — sharded by item partition, 10 servers, each serving 10M embeddings. (4) **Ranking**: TensorFlow model with 200+ features; served via TensorFlow Serving with autoscaling (100+ instances). (5) **Model update**: Daily full retrain on Spark (1000+ cores) + hourly incremental updates via online learning. (6) **A/B testing**: 100+ concurrent experiments; metrics: CTR, watch time, conversion, retention, satisfaction. (7) **Monitoring**: Feature drift (population stability index), model drift (offline metrics), input distribution shift, prediction latency, error rate.

**Q: How do you handle the trade-off between personalization and serendipity?**

A: (1) **Exploration**: Reserve 5-10% of impressions for random/diverse items (ε-greedy, Thompson sampling, multi-armed bandits). (2) **Diversification**: Ensure recommended items span different categories/authors — max marginal relevance (MMR) or determinantal point processes (DPP). (3) **Novelty scoring**: Measure how novel each item is to the user (inverse of how many similar users have seen it). (4) **Serendipity**: Items that are similar to the user's interests but unexpected — use higher-order similarity (users with similar taste in one area but different items). (5) **A/B testing**: Track discovery of new categories, new creator engagement, repeat visit diversity. (6) **Long-term objectives**: Optimize for 7-day or 30-day engagement, not just next-click — use inverse propensity weighting or counterfactual estimation.

#### Senior-Level Questions

**Q: How would you design a recommendation system for YouTube-scale (30M videos, 1B users, 500 hours of video uploaded/minute)?******

A: (1) **Architecture**: Two-stage deep pipeline — (a) Candidate generation: two-tower neural model (user tower + video tower) → ANN (FAISS) over video embeddings → 5000 candidates in < 10ms. (b) Ranking: deep neural network scoring 150+ features (watch time predictors) → top 10. (2) **Features**: User features (search history, watch history, subscriptions, demographics); video features (metadata, transcript, category, upload recency, duration, engagement stats); contextual (time of day, day of week, device, network). (3) **Storage**: Video metadata in NoSQL (Bigtable — 30M rows); user features in Redis (1B users → 100-node Redis cluster, 5TB); interactions in Bigtable + Spanner. (4) **Training**: Daily full retrain on 100B+ interactions (Spark + TF) on 1000+ GPU/TPU cores; incremental updates hourly; real-time online learning for session features. (5) **Candidate serving**: 10 FAISS index shards (1B videos / 10 = 100M per shard), each on GPU; cross-shard query → merge top 5000. (6) **Ranking serving**: 100+ TF Serving instances with autoscaler; model size 500MB; P99 latency < 40ms. (7) **Online serving**: Redis for features (P99 < 5ms for 100M lookups); fallback to Bigtable if cache miss. (8) **Evaluation**: Offline (watch-time prediction AUC, NDCG); online A/B test (click-through rate, watch time per impression, session watch time, survey satisfaction). (9) **Cold start**: New videos → candidate via content match (title/description similarity) + trending boost; new users → initial candidates from homepage popular row + survey. (10) **Infrastructure cost**: ~$5M/month (1000 GPU cores for training, 100 TF Serving instances, 100 Redis nodes, 10 FAISS servers).

**Q: How would you design a recommendation system that handles 100K requests/second with < 50ms latency?**

A: (1) **Candidate generation**: Pre-compute candidate sets during off-peak hours — store in Redis as `candidates:{user_id}` with 24-hour TTL. At request time: check Redis → if hit → return 1000 candidates in < 5ms. If miss → compute via ANN (FAISS) in < 20ms → cache. Pre-warming: compute candidates for top 10M active users nightly. (2) **Feature store**: Critical features (user embedding, last 10 items) in Redis; non-critical (demographics, category averages) pre-loaded into process memory at startup. (3) **Ranking**: Compiled model (ONNX/TensorFlow Lite) — single-process inference, no network hop. 200 features → 10ms inference on a fast CPU core. (4) **Caching**: Cache top 10 recommendations per user in Redis (5-minute TTL) → 90% cache hit rate. Cache invalidation on key events (purchase → recompute). (5) **Concurrency**: 100K RPS / 50ms avg serving time = 5000 concurrent requests → 50+ instances with 10 threads each. (6) **Circuit breakers**: If candidate service fails → fall back to popularity-based. If ranking fails → return candidates unranked. (7) **Monitoring**: P99 latency < 50ms; cache hit rate > 80%; model quality (offline AUC > 0.8). (8) **Autoscaling**: Scale instances based on request rate + latency SLO.

#### System Design Questions (Senior)

**Q: Design a recommendation system for an e-commerce site (Amazon-style) with 10M products and 100M users, real-time recommendations.**

**Approach**:
- **Candidate generation**: (1) Item-to-item collaborative filtering — precompute top 50 similar items per item (co-purchase matrix, Spark job daily). (2) User-based — for active users, compute top candidates from session + recent views. (3) Popular items as fallback. Total: ~100 candidates per user.
- **Feature engineering**: User features (recent views, purchases, cart adds, demographics, session events) in Redis (real-time). Item features (category, price, brand, rating, recency, popularity) in Redis + process memory. Context features (time of day, device).
- **Ranking model**: GBDT model with 100+ features → predict P(add to cart, purchase). Model size 200MB → loaded in-process. Batch inference (100 candidates × 100 features → 50ms on CPU).
- **Real-time updates**: Stream user events (Kafka) → update Redis features per event → affects next recommendation. Session features updated in < 100ms.
- **Caching**: Top 10 per user cached in Redis (1-minute TTL) → 95% cache hit for active users. Stale cache → compute from candidates + features.
- **Cold start**: New user → popular items in their country + onboarding survey; new item → content features (category, brand) + "people who viewed X also viewed Y" from similar items.
- **Monitoring**: Offline precision@10, NDCG daily; online CTR, conversion rate, revenue per user per session; cache hit rate.

**Q: Design a system where recommendations update in real-time as a user browses (e.g., Amazon's "frequently bought together" updates after each click).**

**Approach**:
- **Event pipeline**: (1) Client emits events (view, click, hover, scroll depth) → (2) Kafka (high-throughput, 1M events/sec) → (3) Flink stream processor → (4) Update user features in Redis in real-time. (5) Trigger re-scoring if key features changed (> 10% deviation from baseline).
- **Feature store**: Redis with two layers — (1) Hot features (last 50 events, session aggregates) updated per event; (2) Warm features (user profile, demographics) updated hourly. Use Redis Streams for ordering + Redis Sets for session history.
- **Candidate cache**: Pre-computed candidates (item-to-item, user-to-item) cached per user with 5-minute TTL. Real-time events trigger cache invalidation → recompute on next request.
- **Ranking**: In-process model (ONNX) — 50ms for 100 candidates × 100 features. Only re-rank when features changed (avoid unnecessary compute).
- **Latency**: Event → feature update < 100ms; feature update → cache invalidation < 500ms; next request uses fresh features.
- **Scale**: 10M concurrent users browsing → 1M events/sec → 20 Flink task managers → 100 Redis shards.
- **Degradation**: If real-time pipeline fails → use last-computed features (5-minute staleness) → alert.

#### Common Mistakes

- Not decomposing into candidate generation + ranking — tries to rank over all items (too slow).
- Ignoring cold start — new users get poor recommendations → bad first impression.
- Using accuracy metrics only (Precision/Recall) — not measuring engagement, satisfaction, diversity.
- Not A/B testing — offline improvements don't always translate to real-world engagement.
- No exploration → filter bubbles → user churn.
- Not monitoring model/data drift → model quality degrades silently over time.
- Over-engineering on day 1 — start simple (popularity-based) → add ML as data scale.