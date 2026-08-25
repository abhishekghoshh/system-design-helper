# Design Distributed Job Scheduler

## Blogs and websites

## Medium

## Youtube

## Theory

### Problem Statement
Design a distributed job scheduler that can reliably schedule, execute, and manage millions of jobs (one-time, recurring, delayed) across a cluster of workers.

### Functional Requirements
- Schedule one-time jobs at a specific time
- Schedule recurring jobs (cron-like)
- Delayed job execution (run after X minutes)
- Job prioritization
- Retry failed jobs with configurable backoff
- Job status tracking (pending, running, completed, failed)
- Job cancellation and pause/resume

### Non-Functional Requirements
- **Reliability**: Every job executes at least once (at-least-once semantics)
- **Scalability**: Handle millions of scheduled jobs
- **Low Latency**: Job fires within 1-2 seconds of scheduled time
- **Fault Tolerance**: No single point of failure, survive node crashes
- **Consistency**: No duplicate execution (ideally exactly-once)

### High-Level Architecture

```
┌──────────┐     ┌─────────────────┐     ┌──────────────────┐
│  Client  │────▶│   API Gateway   │────▶│  Scheduler       │
│  (API/   │     │                 │     │  Service         │
│   UI)    │     └─────────────────┘     │                  │
└──────────┘                             │ ┌──────────────┐ │
                                         │ │ Job Store    │ │
                                         │ │ (metadata)   │ │
                                         │ └──────┬───────┘ │
                                         └────────┼─────────┘
                                                  │
                                         ┌────────▼─────────┐
                                         │   Job Queue       │
                                         │   (Priority Q)    │
                                         └────────┬─────────┘
                                                  │
                              ┌────────────────────┼────────────────────┐
                              ▼                    ▼                    ▼
                        ┌───────────┐        ┌───────────┐       ┌───────────┐
                        │  Worker 1 │        │  Worker 2 │       │  Worker N │
                        └───────────┘        └───────────┘       └───────────┘
```

### Core Components

**1. Job Store (Database)**
```sql
jobs table:
  id, name, type (ONE_TIME | RECURRING), cron_expression,
  scheduled_at, payload, priority, max_retries, retry_count,
  status (PENDING | QUEUED | RUNNING | COMPLETED | FAILED),
  locked_by, locked_at, created_at, updated_at
```

**2. Scheduler (Ticker)**
```
Every second:
  1. Query jobs WHERE scheduled_at <= NOW() AND status = PENDING
  2. Move them to the job queue
  3. For recurring jobs: compute next_run and insert new job row
```

**3. Job Queue**
- Priority queue (Redis Sorted Set or Kafka with priority topics)
- Score = scheduled_time (earlier = higher priority)
- Dequeue guarantees: visibility timeout + acknowledgment

**4. Workers**
- Pull jobs from queue (competing consumers pattern)
- Execute job payload
- Report result (success/failure) back to job store
- Heartbeat to indicate liveness

### Distributed Coordination

**Leader Election (for Scheduler):**
```
Multiple scheduler instances → Only 1 active (leader)
Use: ZooKeeper / etcd / Redis RedLock for leader election
Failover: If leader dies, another takes over within seconds
```

**Preventing Duplicate Execution:**
```
1. Optimistic locking: UPDATE jobs SET locked_by=worker_id
   WHERE id=X AND locked_by IS NULL
2. Visibility timeout: Job invisible to others for N seconds
3. Idempotency: Jobs should be idempotent (safe to retry)
```

### Handling Failures

```
Job fails → Retry with exponential backoff
  Attempt 1: immediate
  Attempt 2: after 1 min
  Attempt 3: after 5 min
  Attempt N: after min(2^N minutes, 1 hour)

After max_retries → Move to Dead Letter Queue (DLQ)
  → Alert operators
  → Manual retry option
```

### Scaling Strategies

| Component | Strategy |
|-----------|----------|
| **Job Store** | Sharded by job_id, partition by scheduled_at |
| **Queue** | Partitioned topics (Kafka) or multiple Redis instances |
| **Workers** | Horizontal scaling, auto-scale based on queue depth |
| **Scheduler** | Active-passive with leader election |

### Tech Choices
- **Job Store**: PostgreSQL (strong consistency) or Cassandra (scale)
- **Queue**: Redis Sorted Sets (simple) or Kafka (durable, high throughput)
- **Coordination**: etcd or ZooKeeper
- **Workers**: Stateless containers (K8s Jobs / ECS Tasks)
