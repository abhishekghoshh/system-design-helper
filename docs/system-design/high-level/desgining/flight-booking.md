# Design Flight Booking System

## Blogs and websites


## Medium


## Youtube


## Theory

### Problem Statement
Design a flight booking system like Booking.com or Google Flights that supports flight search, seat selection, booking, and payment processing with inventory management to prevent overbooking.

### Functional Requirements
- Search flights by origin, destination, dates, passengers, class
- View available flights with prices
- Select seats
- Book flights (reserve → pay → confirm)
- Manage bookings (view, cancel, modify)
- Price alerts and fare tracking
- Multi-leg/round-trip bookings

### Non-Functional Requirements
- **Scale**: 100M+ searches/day, 1M+ bookings/day
- **Latency**: Search < 2s, booking < 5s
- **Consistency**: No double-booking of same seat (strong consistency for inventory)
- **Availability**: 99.99% for search, 99.999% for bookings
- **Data**: Millions of flight routes, dynamic pricing

### High-Level Architecture

```
┌──────────┐     ┌──────────┐     ┌─────────────────────────────┐
│  Client  │────▶│  API GW  │────▶│       Service Layer          │
└──────────┘     └──────────┘     │                              │
                                  │  ┌────────────────────────┐  │
                                  │  │ Search Service          │  │
                                  │  │ Booking Service         │  │
                                  │  │ Payment Service         │  │
                                  │  │ Inventory Service       │  │
                                  │  │ Notification Service    │  │
                                  │  │ Pricing Service         │  │
                                  │  └───────────┬────────────┘  │
                                  └──────────────┼───────────────┘
                                                 │
                              ┌──────────────────┼──────────────────┐
                              ▼                  ▼                  ▼
                       ┌────────────┐     ┌────────────┐    ┌────────────┐
                       │ Flight DB  │     │ Booking DB │    │ Search     │
                       │ (inventory)│     │            │    │ Index (ES) │
                       └────────────┘     └────────────┘    └────────────┘
```

### Search Flow

```
User searches: NYC → LON, Dec 15, 2 passengers

Search Service:
  1. Query Elasticsearch for matching flights
     → Filter by route, date, available seats ≥ 2
  2. Fetch prices from Pricing Service
     → Dynamic pricing based on demand, time to departure, competition
  3. Rank results (price, duration, stops, airline rating)
  4. Return paginated results

Optimization:
  - Pre-compute popular routes (cache)
  - Search index updated every few minutes (not real-time)
  - Availability check at booking time (not search time)
```

### Booking Flow (Critical Path)

```
Step 1: Reserve (temporary hold)
  → Inventory Service: SELECT FOR UPDATE seats WHERE flight_id = X
  → Mark seats as "held" with expiry (10 min)
  → Return reservation_id + payment deadline

Step 2: Payment
  → Payment Service: charge customer
  → If payment fails → release reservation
  → If payment succeeds → proceed to confirm

Step 3: Confirm
  → Booking Service: change status "held" → "confirmed"
  → Inventory Service: permanently allocate seats
  → Notification Service: send confirmation email + e-ticket
  → Generate PNR (Passenger Name Record)

Timeout:
  → If payment not received in 10 min → auto-release seats
  → Scheduled job checks expired reservations
```

### Preventing Double-Booking

```
Approach: Pessimistic locking on inventory

BEGIN TRANSACTION;
  SELECT * FROM seats 
    WHERE flight_id = 123 AND seat_number = '12A' AND status = 'available'
    FOR UPDATE;  -- Row-level lock
  
  UPDATE seats SET status = 'held', reservation_id = 'R456', 
    hold_expires_at = NOW() + INTERVAL '10 minutes'
    WHERE flight_id = 123 AND seat_number = '12A';
COMMIT;

If two users try same seat simultaneously:
  → First gets the lock, second waits
  → Second sees status = 'held' → returns "seat unavailable"
```

### Dynamic Pricing

```
price = base_fare × demand_multiplier × time_multiplier × competition_factor

Inputs:
  - Seats remaining (fewer seats → higher price)
  - Days until departure (last minute = expensive)
  - Historical demand for this route/date
  - Competitor prices (scraped or API)
  - Booking class (economy, business, first)
  
Updated: Every few minutes per flight
Stored: Pricing cache (Redis) for fast lookup
```

### Key Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Inventory consistency | Pessimistic locking (SELECT FOR UPDATE) | Prevent double-booking |
| Search | Elasticsearch | Fast full-text + filter queries |
| Reservation | Temporary hold with TTL | Prevent inventory hoarding |
| Pricing | Dynamic, cached in Redis | Real-time pricing at scale |
| Payment | Two-phase (reserve → pay → confirm) | Saga pattern for distributed tx |

### Scaling Considerations
- **Search**: Horizontally scale ES, cache popular routes
- **Inventory**: Shard by flight_id, each flight on one partition
- **Booking**: Idempotency keys to prevent duplicate charges
- **Global**: Multi-region with inventory staying in origin region
