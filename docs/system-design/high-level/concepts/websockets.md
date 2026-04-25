# WebSockets

## Blogs and websites


## Medium


## Youtube

- [How to horizontally scale up websocket servers](https://www.youtube.com/watch?v=hl3_MANBiyc)
- [Scaling Websockets Horizontally | SocketIo | Redis Pub\Sub | HandsOn](https://www.youtube.com/watch?v=dcroxRr8uJc)
- [How to scale WebSockets to millions of connections](https://www.youtube.com/watch?v=vXJsJ52vwAA)
- [Scaling Websockets with Redis, HAProxy and Node JS - High-availability Group Chat Application](https://www.youtube.com/watch?v=gzIcGhJC8hA)
- [WebSockets Aren’t as Reliable as You Think.. Here's Why](https://www.youtube.com/watch?v=ImzYxO3Lsvc)
- [How I would SCALE WebSocket system in 2026 (Architecture deep dive) | Hindi](https://www.youtube.com/watch?v=ORupgrqr3R0)

## Theory

### The Real-Time Communication Channel

Full-duplex, persistent connection for real-time communication.

**Features:**
- Bidirectional communication
- Low latency
- Persistent connection
- Works over HTTP (upgrades connection)

**How WebSocket Works:**
```
1. Client initiates HTTP request
   GET /chat HTTP/1.1
   Host: example.com
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==

2. Server accepts upgrade
   HTTP/1.1 101 Switching Protocols
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=

3. Connection upgraded to WebSocket
   ┌────────────────────────────────┐
   │   Client ←───────────→ Server   │
   │                                │
   │   Bidirectional messages       │
   │   Both can send anytime        │
   └────────────────────────────────┘

4. Messages flow freely
   Client → Server: {type: "message", text: "Hello"}
   Server → Client: {type: "ack", id: 123}
   Server → Client: {type: "notification", data: ...}
```

**Use Cases:**
- Chat applications
- Real-time notifications
- Live sports updates
- Collaborative editing
- Online gaming
- Stock trading platforms

### Advantages of WebSockets

```
✓ Real-Time Bidirectional Communication
  - Both client and server can send anytime
  - No need to poll for updates
  - Instant message delivery

✓ Low Latency
  - No HTTP overhead per message
  - Just data frames
  - Typical latency: 10-50ms

✓ Lower Overhead
  - No headers per message (after handshake)
  - Smaller frame headers (2-14 bytes)
  - More efficient than HTTP polling

✓ Persistent Connection
  - Single connection for lifetime
  - No repeated handshakes
  - Less server resources

✓ Server Push
  - Server can initiate messages
  - No waiting for client poll
  - Event-driven architecture

✓ Better Mobile Performance
  - Persistent connection uses less battery
  - No repeated HTTP connections
  - Lower data usage
```

**Performance Comparison:**
```
HTTP Polling (every 1s):
  Request:  200 bytes
  Response: 100 bytes
  Per hour: 300 bytes × 3600 = 1.08 MB
  
  Latency: 0.5-2 seconds (poll interval + network)

WebSocket:
  Handshake: 500 bytes (once)
  Message:   50 bytes (just data)
  Per hour:  50 bytes × 3600 = 180 KB + 500 bytes
  
  Latency: 10-50ms (instant)
  
Data Savings: ~80-90%
Latency Improvement: ~100x faster
```

### Disadvantages of WebSockets

```
✗ Complex Implementation
  - Harder than HTTP request/response
  - Need to handle connection state
  - Reconnection logic required
  - Message queuing needed

✗ Connection Management
  - Keep-alive pings needed
  - Detect disconnections
  - Handle reconnections gracefully
  - State synchronization

✗ Scaling Challenges
  - Stateful connections
  - Sticky sessions required
  - Load balancer must support WebSocket
  - Connection limits per server

✗ Firewall/Proxy Issues
  - Some corporate firewalls block
  - Some proxies don't handle upgrades
  - May need fallback to polling

✗ Resource Intensive
  - One connection per client (always)
  - 10,000 clients = 10,000 connections
  - Memory per connection
  - File descriptor limits

✗ No HTTP Caching
  - Can't leverage HTTP cache
  - No CDN support
  - All traffic to origin

✗ Browser Compatibility
  - Old browsers don't support
  - Need fallback mechanism
  - Polyfills add complexity

✗ Security Considerations
  - CSRF protection needed
  - Authentication per message
  - Rate limiting complex
  - DDoS risk (connection exhaustion)
```

### Alternatives to WebSockets

**1. HTTP Long Polling**
```
How it works:
  Client: Request to server (waits...)
  Server: Holds request until data available
  Server: Responds with data
  Client: Immediately requests again

Advantages over WebSocket:
  + Works everywhere (no upgrade needed)
  + Simpler fallback
  + Better firewall compatibility

Disadvantages:
  - Higher latency
  - More server resources
  - Not true bidirectional
  - Connection churn

When to use:
  → Simple updates
  → Legacy browser support needed
  → Corporate firewall issues
```

**2. Server-Sent Events (SSE)**
```
How it works:
  Client: Opens connection
  Server: Pushes events continuously
  
Advantages over WebSocket:
  + Simpler (just HTTP)
  + Auto-reconnection built-in
  + Event IDs for replay
  + Better browser support

Disadvantages:
  - One-way only (server → client)
  - Text only (no binary)
  - HTTP/1.1 connection limit (6 per domain)

When to use:
  → Server needs to push to client
  → Client doesn't need to send much
  → Simpler alternative to WebSocket
  
Example:
  Stock prices, news feeds, notifications
```

**3. HTTP/2 Server Push**
```
How it works:
  Client: Requests index.html
  Server: Pushes style.css, script.js
  
Advantages:
  + No connection upgrade
  + Uses existing HTTP infrastructure
  + Multiplexed

Disadvantages:
  - Only for initial page load
  - Not for continuous updates
  - Limited browser support

When to use:
  → Optimize page load
  → Not for real-time updates
```

**4. WebRTC Data Channels**
```
How it works:
  Peer-to-peer connection
  No server in the middle (after setup)
  
Advantages over WebSocket:
  + Peer-to-peer (no server)
  + Lower latency
  + UDP-based (configurable reliability)
  + Built-in encryption

Disadvantages:
  - Complex setup (STUN/TURN)
  - Not for server communication
  - NAT traversal issues

When to use:
  → Peer-to-peer (gaming, file sharing)
  → Video/voice calls
  → Ultra-low latency needed
```

**5. Message Queues (for backend)**
```
For server-to-server:
  Kafka, RabbitMQ, Redis Pub/Sub
  
Advantages:
  + Guaranteed delivery
  + Persistence
  + Buffering
  + Scalability

When to use:
  → Backend services communication
  → Not for client connections
```

### When to Use WebSockets vs Alternatives

| Use Case | Best Choice | Reason |
|----------|-------------|--------|
| **Chat application** | WebSocket | Bidirectional, instant |
| **Notifications only** | SSE | Simpler, server → client |
| **Stock ticker** | SSE or WS | Server pushes updates |
| **Collaborative editing** | WebSocket | Real-time sync both ways |
| **Live dashboard** | SSE | Server pushes metrics |
| **Online gaming** | WebSocket/WebRTC | Low latency critical |
| **Video call** | WebRTC | P2P, media optimized |
| **Admin updates** | Long Polling | Simple, infrequent |
| **Live sports scores** | SSE | One-way updates |
| **IoT device control** | WebSocket/MQTT | Bidirectional control |

### WebSocket Implementation Examples

**Client (JavaScript):**
```javascript
// Create connection
const ws = new WebSocket('wss://example.com/chat');

// Connection opened
ws.onopen = (event) => {
  console.log('Connected');
  ws.send(JSON.stringify({type: 'auth', token: 'abc123'}));
};

// Receive messages
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

// Handle errors
ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

// Connection closed
ws.onclose = (event) => {
  console.log('Disconnected');
  // Reconnect logic
  setTimeout(() => {
    // Recreate connection
  }, 5000);
};

// Send message
function sendMessage(text) {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({type: 'message', text}));
  }
}
```

**Server (Node.js with ws library):**
```javascript
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

const clients = new Set();

wss.on('connection', (ws) => {
  console.log('Client connected');
  clients.add(ws);
  
  // Send welcome message
  ws.send(JSON.stringify({type: 'welcome', message: 'Connected!'}));
  
  // Receive messages
  ws.on('message', (data) => {
    const message = JSON.parse(data);
    
    // Broadcast to all clients
    clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify(message));
      }
    });
  });
  
  // Handle disconnect
  ws.on('close', () => {
    console.log('Client disconnected');
    clients.delete(ws);
  });
  
  // Keep-alive ping
  const interval = setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.ping();
    }
  }, 30000);
  
  ws.on('close', () => clearInterval(interval));
});
```

### WebSocket Best Practices

**Do's:**
```
✓ Use wss:// (secure WebSocket)
✓ Implement reconnection logic
✓ Send heartbeat/ping messages
✓ Authenticate connections
✓ Validate all incoming messages
✓ Implement rate limiting
✓ Handle connection limits gracefully
✓ Use message queuing for offline clients
✓ Implement proper error handling
✓ Monitor connection health
```

**Don'ts:**
```
✗ Don't assume connection is always alive
✗ Don't send huge messages (use chunking)
✗ Don't trust client-side validation
✗ Don't keep connections open indefinitely without heartbeat
✗ Don't forget to clean up resources
✗ Don't use for file uploads (use HTTP)
✗ Don't send sensitive data without encryption
✗ Don't ignore backpressure
```

### Scaling WebSocket Servers

**The Problem:**
```
10,000 concurrent connections
× 1 server
= 10,000 connections on one server (limit!)

With load balancer:
  Client A → LB → Server 1
  Client B → LB → Server 2
  
  Problem: Client A and B can't communicate!
  (Different servers)
```

**Solutions:**

**1. Sticky Sessions (Session Affinity)**
```
Load Balancer routes same user to same server

Pros: Simple
Cons: 
  - Uneven distribution
  - No failover
  - Server restart = all clients disconnect
```

**2. Message Broker (Redis Pub/Sub, Kafka)**
```
  Server 1 ──┐
             ├─→ Redis Pub/Sub ←─┐
  Server 2 ──┘                   └── Broadcast to all servers
  
How it works:
  1. Client A sends to Server 1
  2. Server 1 publishes to Redis
  3. All servers (1, 2, 3) subscribe
  4. All servers broadcast to their clients
  
Pros:
  + Scales horizontally
  + Failover support
  + Clients can be on any server
  
Cons:
  - Added latency (Redis hop)
  - More complex
  - Redis is SPOF (use cluster)
```

**3. Dedicated WebSocket Servers**
```
Architecture:
  
  API Servers (HTTP)     WebSocket Servers
  ┌────────────┐         ┌──────────────┐
  │  Server 1  │         │   WS Server  │
  │  Server 2  │  ←────→ │   + Redis    │
  │  Server 3  │         │   Pub/Sub    │
  └────────────┘         └──────────────┘
  
Pros:
  + Separate scaling
  + Optimize each tier
  + Easier to manage
```

### WebSocket vs HTTP: The Decision

**Use WebSocket when:**
```
✓ Real-time updates needed (<100ms)
✓ Bidirectional communication
✓ Frequent messages (>1/second)
✓ Push notifications from server
✓ Collaborative features
✓ Live data feeds
```

**Use HTTP when:**
```
✓ Request/response pattern
✓ Infrequent updates (>10 seconds)
✓ One-time data fetch
✓ Need HTTP caching
✓ Simple CRUD operations
✓ Simpler to implement/maintain
```

**Use SSE when:**
```
✓ Only server → client updates
✓ Simpler than WebSocket
✓ Auto-reconnect important
✓ Text-based data
```

---

### Websockets
