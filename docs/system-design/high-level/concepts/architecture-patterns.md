# Architecture Patterns

## Blogs and websites


## Medium


## Youtube


## Theory

### Monolith Architecture

Single unified codebase and deployment.

**Pros:**
- Simple to develop and deploy
- Easy to test
- Better performance (no network calls)
- Simpler debugging

**Cons:**
- Difficult to scale
- Slower deployment
- Technology lock-in
- Poor fault isolation

**When to Use:**
- Small teams
- Simple applications
- Startups (MVP stage)

### Microservices Architecture

Application composed of small, independent services.

**Characteristics:**
- Single responsibility
- Independent deployment
- Decentralized data
- Technology diversity
- Communication via APIs

**Pros:**
- Independent scaling
- Fault isolation
- Technology flexibility
- Faster deployment
- Team autonomy

**Cons:**
- Complex infrastructure
- Distributed system challenges
- Testing complexity
- Data consistency issues
- Operational overhead

**Best Practices:**
- Domain-driven design
- API versioning
- Centralized logging
- Service mesh
- Circuit breakers

### Event-Driven Architecture

Components communicate through events.

**Components:**
- **Event Producers**: Generate events
- **Event Broker**: Routes events (Kafka, RabbitMQ)
- **Event Consumers**: Process events

**Patterns:**
- **Event Notification**: Alert other systems
- **Event-Carried State Transfer**: Full data in event
- **Event Sourcing**: Store events as source of truth
- **CQRS**: Separate read and write models

**Benefits:**
- Loose coupling
- Scalability
- Asynchronous processing
- Event replay capability

**Challenges:**
- Eventual consistency
- Event ordering
- Debugging difficulty
- Schema evolution

### Serverless Architecture

Run code without managing servers (FaaS).

**Characteristics:**
- Event-driven execution
- Auto-scaling
- Pay-per-use
- Stateless functions
- Managed by cloud provider

**Pros:**
- No server management
- Auto-scaling
- Cost-effective (no idle resources)
- Fast deployment

**Cons:**
- Cold starts
- Vendor lock-in
- Limited execution time
- Debugging challenges
- State management

**Use Cases:**
- API backends
- Data processing
- Scheduled tasks
- Webhooks
