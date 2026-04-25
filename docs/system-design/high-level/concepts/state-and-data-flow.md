# State and Data Flow

## Theory

### What is State and Data Flow?

**State** is any data that can change over time and affects how a system behaves or what it renders. **Data flow** describes how that state moves between components, services, or layers of a system.

Understanding state management and data flow is critical because most bugs, performance issues, and architectural complexity come from managing state incorrectly.

### What is State?

State is the current condition of a system at any point in time:
```
Examples of state:
  - Is the user logged in?           → Authentication state
  - What items are in the cart?       → Application state
  - What page is the user viewing?    → UI/navigation state
  - What data came from the server?   → Server/remote state
  - What did the user type in a form? → Local/form state
```

### Types of State

**Client-Side State:**
- **UI State**: Which modal is open, which tab is active, scroll position
- **Form State**: Input values, validation errors
- **Application State**: Shopping cart, user preferences, auth tokens
- **Cache/Server State**: Data fetched from APIs, cached locally

**Server-Side State:**
- **Session State**: User session data (stored in Redis, DB, or memory)
- **Database State**: Persistent application data
- **In-Memory State**: Caches, rate limit counters, connection pools

### Data Flow Patterns

**1. Unidirectional Data Flow (One-Way)**
```
  State → View → Action → State (updated) → View (re-renders)

  Example (React/Redux):
    Store (state)
      ↓
    Component (renders based on state)
      ↓
    User clicks button (dispatches action)
      ↓
    Reducer (updates state)
      ↓
    Store (new state) → Component re-renders
```
- **Predictable**: Data flows in one direction, easier to debug
- **Used by**: React, Vue, Redux, Flux

**2. Bidirectional Data Flow (Two-Way Binding)**
```
  Model ←→ View

  Example (Angular):
    Input field changes → Model updates automatically
    Model changes → Input field updates automatically
```
- **Convenient**: Less boilerplate for forms
- **Risk**: Harder to track what changed what (can create cycles)
- **Used by**: Angular, Svelte (with bind:)

**3. Request-Response (Client-Server)**
```
  Client                         Server
    |── GET /api/users ──────────→|
    |                              |── Query DB
    |←── JSON [{id: 1, ...}] ────|

  Data flows:
    Client → Request → Server → DB → Server → Response → Client
```

**4. Event-Driven / Pub-Sub**
```
  Service A publishes event: "OrderPlaced"
    ↓
  Message Broker (Kafka, RabbitMQ)
    ↓              ↓              ↓
  Email Service  Inventory     Analytics
  (sends email)  (decrements)  (records event)
```
- **Decoupled**: Services don't know about each other
- **Async**: Events processed independently

**5. Streaming (Real-Time)**
```
  Server pushes data continuously:
    WebSocket: Bidirectional stream
    SSE: Server → Client stream
    Kafka Streams: Service → Service stream
```

### Stateless vs Stateful

| Aspect | Stateless | Stateful |
|--------|-----------|----------|
| **Server remembers** | Nothing between requests | Client context (session) |
| **Scaling** | Easy (any server handles any request) | Hard (sticky sessions needed) |
| **Failover** | Trivial (no state to lose) | Complex (state must be replicated) |
| **Example** | REST API with JWT | WebSocket connection, database connection |

**Modern Best Practice:**
- Keep application servers **stateless**
- Store state **externally** (Redis, database, object store)
- Any server can handle any request → easy horizontal scaling

### State Management Challenges

- **Stale state**: Cached data becomes outdated
- **Race conditions**: Two updates happen simultaneously, one overwrites the other
- **State synchronization**: Keeping multiple clients/servers in sync
- **State explosion**: Too many state variables make the system hard to reason about

**Solutions:**
- Use a single source of truth (centralized state store)
- Use optimistic updates with conflict resolution
- Use event sourcing to track all state changes
- Keep state minimal — derive what you can, don't store it
