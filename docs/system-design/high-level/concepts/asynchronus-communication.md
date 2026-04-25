# Message Queue

## Theory

### Message Queues for Async Tasks

A message queue is a communication mechanism where **producers** send messages to a queue and **consumers** pull messages from it for processing. The queue acts as a buffer between the sender and receiver, enabling **asynchronous** and **decoupled** communication.

**Why Message Queues?**

In a synchronous system, Service A calls Service B directly and waits for a response. If Service B is slow or down, Service A is blocked. Message queues solve this:

```
Synchronous (tightly coupled):
  User → API → Process Video → Return Response
  Problem: User waits 5 minutes for video to process

Asynchronous (with message queue):
  User → API → Push to Queue → Return "Processing..."
                    ↓
              Worker picks up → Process Video → Notify user
  Result: User gets instant response, video processes in background
```

**Core Concepts:**
- **Producer**: Service that creates and sends messages to the queue
- **Consumer/Worker**: Service that reads and processes messages from the queue
- **Queue/Topic**: The channel where messages are stored temporarily
- **Acknowledgment**: Consumer confirms successful processing; if not, message is redelivered
- **Dead Letter Queue (DLQ)**: Where failed messages go after max retries (prevents infinite loops)

**Key Benefits:**
- **Decoupling**: Producer and consumer don't need to know about each other
- **Load Leveling**: Queue absorbs traffic spikes; workers process at their own pace
- **Fault Tolerance**: If a consumer crashes, messages persist in the queue
- **Scalability**: Add more consumers to process faster (horizontal scaling)
- **Retry**: Failed messages can be retried automatically

**Common Patterns:**

1. **Point-to-Point (Queue)**: One message → one consumer
   - Use case: Task processing, job queues
   
2. **Pub/Sub (Topic)**: One message → many consumers
   - Use case: Event broadcasting, notifications

3. **Fan-out**: One event triggers multiple different actions
   - Use case: Order placed → send email + update inventory + notify shipping

**Popular Systems Compared:**

| System | Model | Strength | Use Case |
|--------|-------|----------|----------|
| **Kafka** | Log-based, pub/sub | High throughput, replay | Event streaming, analytics |
| **RabbitMQ** | Queue-based, AMQP | Flexible routing, protocols | Task queues, RPC |
| **AWS SQS** | Managed queue | Zero ops, auto-scale | Serverless, cloud-native |
| **Redis Pub/Sub** | In-memory pub/sub | Ultra-low latency | Real-time, ephemeral messages |
| **NATS** | Lightweight pub/sub | Simple, fast | Microservices, IoT |

**When to Use:**
- Background job processing (video encoding, image resizing)
- Email/notification delivery
- Order processing pipelines
- Log aggregation and analytics
- Event-driven architectures (microservices communication)

---

## Quick Reference

Asynchronous communication pattern for decoupling services.

**Key Concepts:**
- **Producer**: Sends messages
- **Consumer**: Processes messages
- **Queue**: Stores messages
- **Topics**: Categorize messages
- **Dead Letter Queue**: Failed messages

**Popular Systems:**
- **Kafka**: High-throughput, distributed, log-based
- **RabbitMQ**: Feature-rich, supports multiple protocols
- **AWS SQS**: Managed, scalable
- **Redis Pub/Sub**: In-memory, fast

**Benefits:**
- Decoupling services
- Load leveling
- Fault tolerance
- Asynchronous processing
- Scalability

**Use Cases:**
- Order processing
- Email notifications
- Video transcoding
- Log aggregation
- Event-driven architectures

---

# Asynchronus communication related things


## Youtube

### Single Videos

- [Message Queues vs Pub/Sub | System Design](https://www.youtube.com/watch?v=XvnppkWqJbs)


### Playlists

- [Data Architecture Basics with Adam Bellemare](https://www.youtube.com/playlist?list=PLa7VYi0yPIH0QypJnW0OXOnbLvzJRP34C)