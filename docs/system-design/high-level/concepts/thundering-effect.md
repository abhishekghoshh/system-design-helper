# Design Book My Show



## Youtube

- [27. Thundering Herd Effect on Ticket Booking App | System Design](https://www.youtube.com/watch?v=1aamH7sA8FY)


## Theory

### Thundering Herd Effect

#### Description

The **Thundering Herd Effect** is a problem that occurs when a large number of processes or threads waiting for an event are awakened simultaneously when that event occurs, but only one or a few can proceed. In the context of ticket booking systems like BookMyShow, this happens when:

1. **High-demand events**: When tickets for a popular movie/concert go on sale, thousands of users try to book simultaneously
2. **Cache expiration**: When cached data expires, multiple requests simultaneously try to regenerate it
3. **Resource locking**: Multiple requests compete for the same limited resources (seats, payment processing)

**Problems caused by Thundering Herd:**
- **Server overload**: Sudden spike in requests can crash the server
- **Database strain**: Concurrent writes/reads overwhelm the database
- **Poor user experience**: Legitimate users face timeouts and errors
- **Resource waste**: System spends resources processing requests that will ultimately fail
- **Cascade failures**: Overload in one component can trigger failures in others

**Real-world example in BookMyShow:**
When tickets for a blockbuster movie open at 12:00 PM:
- 10,000 users click "Book Now" at exactly 12:00:00
- All requests hit the server simultaneously
- Database gets flooded with concurrent seat availability checks
- Lock contention on the same seats causes delays
- Most users get timeout errors even though seats are available

#### Diagram

```
Without Mitigation:
==================

Time: 12:00:00 PM (Ticket Sales Open)
                                    
  User₁ ──┐                         
  User₂ ──┤                         
  User₃ ──┤                         
  User₄ ──┤                         
  User₅ ──┼──► Server ──► Database
  User₆ ──┤       ↓           ↓
  User₇ ──┤    OVERLOAD    DEADLOCK
  User₈ ──┤       ↓           ↓
  User₉ ──┤    CRASH      TIMEOUTS
  User₁₀ ─┘                         

Result: 💥 System Failure


With Exponential Backoff + Jitter:
==================================

Time: 12:00:00 - 12:00:05 PM

  User₁ ──────────────────────►│
  User₂ ────────►               │
  User₃ ──────────────►         │  Requests spread
  User₄ ────►                   │  over time window
  User₅ ──────────────────────► │  (0-5 seconds)
  User₆ ──────────►             │
  User₇ ────────────────►       │  Server handles
  User₈ ──────►                 │  manageable load
  User₉ ────────────►           │
  User₁₀ ──────────────────►    │

Result: ✅ Controlled Load Distribution
```

#### How to Resolve: Exponential Backoff and Jitter

##### 1. Exponential Backoff

**Concept**: When a request fails or needs to retry, wait for an exponentially increasing amount of time before the next attempt.

**Formula**: `wait_time = base_delay × 2^(attempt_number)`

**Example**:
- 1st retry: wait 1 second (1 × 2⁰)
- 2nd retry: wait 2 seconds (1 × 2¹)
- 3rd retry: wait 4 seconds (1 × 2²)
- 4th retry: wait 8 seconds (1 × 2³)
- 5th retry: wait 16 seconds (1 × 2⁴)

**Pseudocode**:
```python
def exponential_backoff(max_retries, base_delay=1):
    for attempt in range(max_retries):
        try:
            response = book_ticket()
            return response  # Success
        except Exception as e:
            if attempt == max_retries - 1:
                raise  # Max retries exceeded
            
            wait_time = base_delay * (2 ** attempt)
            sleep(wait_time)
```

**Problem with pure exponential backoff**: If multiple clients start retrying at the same time, they'll all retry at the same exponentially increasing intervals, causing synchronized "waves" of requests.

##### 2. Jitter (Randomization)

**Concept**: Add randomness to the retry delay to desynchronize retry attempts from different clients.

**Types of Jitter**:

**a) Full Jitter** (Recommended):
```python
wait_time = random(0, base_delay * 2^attempt)
```

**b) Equal Jitter**:
```python
temp = base_delay * 2^attempt
wait_time = temp/2 + random(0, temp/2)
```

**c) Decorrelated Jitter**:
```python
wait_time = random(base_delay, previous_wait_time * 3)
```

##### 3. Complete Implementation

```python
import random
import time

def book_ticket_with_backoff(
    seat_id,
    max_retries=5,
    base_delay=0.1,
    max_delay=32
):
    """
    Book ticket with exponential backoff and full jitter
    """
    for attempt in range(max_retries):
        try:
            # Attempt to book the ticket
            result = api.book_seat(seat_id)
            
            if result.success:
                return result
            
            # If booking failed (seat taken, etc.)
            if result.error_code == "SEAT_TAKEN":
                return None  # Don't retry
            
        except (ConnectionError, TimeoutError) as e:
            if attempt == max_retries - 1:
                raise  # Final attempt failed
            
            # Calculate backoff with full jitter
            exponential_delay = min(
                base_delay * (2 ** attempt),
                max_delay
            )
            
            # Full jitter: random between 0 and exponential_delay
            jittered_delay = random.uniform(0, exponential_delay)
            
            print(f"Retry {attempt + 1}/{max_retries} "
                  f"after {jittered_delay:.2f}s")
            
            time.sleep(jittered_delay)
    
    return None  # All retries exhausted
```

##### 4. Additional Mitigation Strategies

**Rate Limiting**:
```python
# Limit requests per user
@rate_limit(max_requests=5, window=60)  # 5 requests per minute
def book_ticket_endpoint(user_id, seat_id):
    return book_ticket(user_id, seat_id)
```

**Queue-based System**:
```
Client → Load Balancer → API Gateway → Message Queue → Workers
                                            ↓
                                      (Controlled rate)
                                            ↓
                                        Database
```

**Virtual Waiting Room**:
- Place users in a queue before allowing them to book
- Release users gradually to the booking system
- Show estimated wait time to manage expectations

**Caching with Lock**:
```python
def get_seat_availability(show_id):
    cache_key = f"seats:{show_id}"
    
    # Try cache first
    cached = redis.get(cache_key)
    if cached:
        return cached
    
    # Use distributed lock to prevent thundering herd on cache miss
    lock_key = f"lock:{cache_key}"
    
    if redis.set(lock_key, "1", nx=True, ex=5):  # 5 second lock
        try:
            # Only one request regenerates cache
            data = database.get_available_seats(show_id)
            redis.setex(cache_key, 60, data)  # Cache for 60s
            return data
        finally:
            redis.delete(lock_key)
    else:
        # Others wait and retry
        time.sleep(random.uniform(0.01, 0.1))
        return get_seat_availability(show_id)  # Recursive retry
```

**Circuit Breaker**:
- Fail fast when system is overloaded
- Prevent cascading failures
- Allow system to recover

**Summary Table**:

| Strategy | Purpose | Effectiveness |
|----------|---------|---------------|
| Exponential Backoff | Spread retries over time | ⭐⭐⭐ |
| Jitter | Desynchronize clients | ⭐⭐⭐⭐⭐ |
| Rate Limiting | Control request rate | ⭐⭐⭐⭐ |
| Queue System | Sequential processing | ⭐⭐⭐⭐⭐ |
| Virtual Waiting Room | User management | ⭐⭐⭐⭐ |
| Distributed Lock | Prevent cache stampede | ⭐⭐⭐⭐ |
| Circuit Breaker | Fail fast protection | ⭐⭐⭐⭐ |

