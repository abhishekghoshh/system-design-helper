# Design Google Maps

## Blogs and websites


## Medium


## Youtube


## Theory

### Problem Statement
Design a mapping and navigation system like Google Maps that supports map rendering, location search, real-time navigation with traffic, and ETA calculation.

### Functional Requirements
- Display interactive maps (pan, zoom, tilt)
- Search for places (address, business name, coordinates)
- Get directions (driving, walking, transit, cycling)
- Real-time navigation with turn-by-turn instructions
- Live traffic data and re-routing
- ETA calculation
- Points of Interest (POI) display
- Offline maps

### Non-Functional Requirements
- **Latency**: Map tile loads < 100ms, route calculation < 1s
- **Scale**: 1B+ monthly users, millions of concurrent navigating users
- **Availability**: 99.99%
- **Storage**: Petabytes of map data, satellite imagery
- **Freshness**: Traffic data updated every 30 seconds

### High-Level Architecture

```
┌──────────┐     ┌──────┐     ┌─────────────────────────────┐
│  Client  │◀───▶│  CDN │     │     Service Layer            │
│  (App)   │     └──────┘     │                              │
└────┬─────┘                  │  ┌────────────────────────┐  │
     │                        │  │ Map Tile Service        │  │
     ▼                        │  │ Search / Geocoding Svc  │  │
┌──────────┐                  │  │ Routing Service         │  │
│  API GW  │─────────────────▶│  │ Traffic Service         │  │
└──────────┘                  │  │ Navigation Service      │  │
                              │  │ ETA Service             │  │
                              │  └───────────┬────────────┘  │
                              └──────────────┼───────────────┘
                                             │
                              ┌──────────────┼──────────────┐
                              ▼              ▼              ▼
                        ┌──────────┐  ┌──────────┐  ┌──────────┐
                        │ Map Data │  │ Graph DB │  │ Traffic  │
                        │ (Tiles)  │  │ (Roads)  │  │ Store    │
                        └──────────┘  └──────────┘  └──────────┘
```

### Map Tile System

```
World divided into tiles at each zoom level:
  Zoom 0:  1 tile (entire world)
  Zoom 1:  4 tiles (2×2)
  Zoom 2:  16 tiles (4×4)
  ...
  Zoom 20: ~1 trillion tiles (very detailed)

Tile addressing: /{zoom}/{x}/{y}.png

Pre-rendered tiles stored in:
  - Object storage (S3) for base tiles
  - CDN for hot tiles (city centers, highways)
  - Client caches recently viewed tiles
```

### Routing Algorithm

```
Road network as weighted graph:
  Nodes = intersections
  Edges = road segments
  Weights = time (distance / speed_limit × traffic_factor)

Algorithm: Modified Dijkstra's + A*

For global routing: Contraction Hierarchies
  - Pre-process: Contract unimportant nodes
  - Query time: O(log N) instead of O(N log N)
  - Cross-continent routes in milliseconds
```

### Traffic System

```
Data sources:
  1. GPS data from active navigation users (anonymized)
  2. Historical traffic patterns by time/day
  3. Incident reports (accidents, construction)
  4. Government traffic sensors

Processing:
  User GPS pings → Kafka → Stream processor (Flink)
    → Aggregate speed per road segment
    → Compare with free-flow speed
    → Color coding: green/yellow/red
    → Update every 30 seconds
```

### ETA Calculation

```
ETA = Σ (segment_length / predicted_speed) for each road segment

predicted_speed = f(
  historical_average_at_this_time,
  current_real_time_traffic,
  weather_conditions,
  special_events
)

ML model trained on billions of historical trips
Re-calculate ETA every minute during navigation
```

### Key Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Map rendering | Pre-rendered vector tiles | Fast loading, smooth zoom |
| Routing | Contraction Hierarchies | Fast global routing |
| Traffic data | Stream processing (Flink) | Real-time aggregation |
| Storage | S3 + CDN (tiles), Graph DB (roads) | Scale + query efficiency |
| Offline maps | Download tile packages + road graph | Navigation without internet |
