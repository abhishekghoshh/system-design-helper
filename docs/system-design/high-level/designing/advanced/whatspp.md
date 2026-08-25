# Designing WhatsApp

Building a global, WhatsApp-scale messaging app is a seriously complex engineering challenge.
The hardest part: **stateful connections (WebSockets) in a stateless backend world**.

---

## Blogs and websites

## Medium

## Youtube

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          GLOBAL WHATSAPP ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────────────────────────┘

  ┌──────────┐                                              ┌──────────┐
  │ User A   │                                              │ User B   │
  │ (US)     │                                              │ (India)  │
  └────┬─────┘                                              └────┬─────┘
       │ WebSocket                                    WebSocket  │
       ▼                                                         ▼
┌─────────────┐                                        ┌─────────────┐
│     LB      │  ── US Region ──                       │     LB      │  ── India Region ──
│ (US Region) │                                        │(India Region│
└──────┬──────┘                                        └──────┬──────┘
       │                                                      │
       ▼                                                      ▼
┌──────────────┐  ┌──────────────┐          ┌──────────────┐  ┌──────────────┐
│ US-WS-       │  │ US-WS-       │          │ India-WS-    │  │ India-WS-    │
│ Server-1     │  │ Server-2     │          │ Server-3     │  │ Server-4     │
└──────┬───────┘  └──────────────┘          └───────┬──────┘  └──────────────┘
       │                                            │
       │         ┌────────────────────┐             │
       │         │  SESSION REGISTRY  │             │
       ├────────►│  (Redis Cluster /  │◄────────────┤
       │  lookup │   Cassandra)       │  register   │
       │         │                    │             │
       │         │ User-B ──► India-  │             │
       │         │            WS-     │             │
       │         │            Server-3│             │
       │         └────────────────────┘             │
       │                                            │
       │         ┌────────────────────┐             │
       └────────►│  MESSAGE BROKER    │◄────────────┘
          publish│  (Redis Pub/Sub /  │  subscribe
                 │   Kafka / gRPC)    │
                 └────────┬───────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
   ┌───────────────────┐   ┌──────────────────┐
   │  OFFLINE STORAGE  │   │ PUSH NOTIFICATION│
   │  (Cassandra /     │   │ SERVICE          │
   │   Distributed Q)  │   │ (APNs / FCM)     │
   └───────────────────┘   └──────────────────┘
```

---

## 1. Redis Pub/Sub for WebSocket Scaling

When a user connects to a WebSocket server, that connection is **sticky**. If User A (on Server 1) wants to talk to User B (on Server 2), Server 1 cannot magically send data down Server 2's socket. You need a **Message Broker** connecting the servers.

### Why Redis Pub/Sub Works

- **Lightning fast** — in-memory, sub-millisecond latency
- **Easy to set up** — Server 1 publishes a message, Server 2 receives it and pushes to User B
- **Great for MVP / medium-scale** apps

### The Catch at WhatsApp Scale

Redis Pub/Sub is a **"dumb" broadcast** mechanism. If you aren't careful:

> A message sent to a Redis channel gets broadcasted to **every** WebSocket server subscribed to it.
> With 1,000 servers globally, **999 servers** receive the message, realize User B isn't on them, and throw it away — wasting massive network bandwidth.

### The Solution

Instead of broadcasting to a global channel:

1. Each server subscribes to **its own unique channel** (e.g., `server-india-node-45`)
2. Messages are published **specifically** to that server's channel
3. At massive scale, consider **Kafka**, **RabbitMQ**, or **direct internal gRPC calls** for more reliable, targeted routing

---

## 2. Session Registry (Presence Service)

> "How does the US Server know the Indian user is on a specific server?"

This is solved by a central **Session Registry** (also called a Presence Service) — a highly available, extremely fast **key-value store** (often a global Redis cluster or Cassandra).

Because WebSocket connections are stateful, you must track **exactly where every online user is connected** at any given millisecond.

Example registry entry:

```json
{
  "userId": "User-B",
  "connected_to": "India-WS-Server-3"
}
```

---

## 3. Online Message Delivery Flow

```
 User A (US)                US-WS-Server-1        Session Registry       Message Broker       India-WS-Server-3        User B (India)
     │                            │                      │                     │                      │                      │
     │  1. Send msg to User B     │                      │                     │                      │                      │
     │ ──────────────────────────► │                      │                     │                      │                      │
     │        (WebSocket)         │                      │                     │                      │                      │
     │                            │  2. Where is User B? │                     │                      │                      │
     │                            │ ─────────────────────►                     │                      │                      │
     │                            │                      │                     │                      │                      │
     │                            │  3. "India-WS-       │                     │                      │                      │
     │                            │      Server-3"       │                     │                      │                      │
     │                            │ ◄─────────────────────                     │                      │                      │
     │                            │                      │                     │                      │                      │
     │                            │  4. Publish msg to India-WS-Server-3      │                      │                      │
     │                            │ ──────────────────────────────────────────►│                      │                      │
     │                            │                      │                     │                      │                      │
     │                            │                      │                     │  5. Forward msg       │                      │
     │                            │                      │                     │ ────────────────────► │                      │
     │                            │                      │                     │    (internal hop)     │                      │
     │                            │                      │                     │                      │  6. Push msg          │
     │                            │                      │                     │                      │ ────────────────────► │
     │                            │                      │                     │                      │     (WebSocket)       │
     │                            │                      │                     │                      │                      │
```

**Step-by-step:**

1. **Connection Time** — User B (India) opens the app → Load balancer assigns them to `India-WS-Server-3` → Server writes `User-B → India-WS-Server-3` to the Session Registry
2. **Send** — User A (US) sends a message → goes through their open WebSocket to `US-WS-Server-1`
3. **Lookup** — `US-WS-Server-1` queries the Session Registry: *"Where is User B?"* → Registry replies: `India-WS-Server-3`
4. **Internal Hop** — `US-WS-Server-1` publishes the message to the broker, targeting `India-WS-Server-3`'s channel
5. **Delivery** — `India-WS-Server-3` receives the message, finds User B's active WebSocket in local memory, and pushes it down the socket

> **Reconnection:** If User B disconnects and reconnects, they might land on `India-WS-Server-9`. The registry updates immediately, and the next message routes to the new server.

---

## 4. Offline Message Handling (Store-and-Forward)

When a user is **offline**, the real-time WebSocket pipeline breaks because there is no active server to receive the message. The architecture shifts from real-time routing to a **Store-and-Forward** mechanism combined with **push notifications**.

```
 User A (US)         US-WS-Server-1      Session Registry     Offline Storage     Push Service        User B (India)
     │                     │                    │                    │                  │                     │
     │  1. Send msg        │                    │                    │                  │                     │
     │ ───────────────────►│                    │                    │                  │                     │
     │                     │  2. Where is       │                    │                  │                     │
     │                     │     User B?        │                    │                  │                     │
     │                     │───────────────────►│                    │                  │                     │
     │                     │  3. "OFFLINE"      │                    │                  │                     │
     │                     │◄───────────────────│                    │                  │                     │
     │                     │                    │                    │                  │                     │
     │                     │  4. Store encrypted msg                 │                  │                     │
     │                     │───────────────────────────────────────► │                  │                     │
     │                     │                    │                    │                  │                     │
     │                     │  5. Trigger push notification           │                  │                     │
     │                     │──────────────────────────────────────────────────────────► │                     │
     │                     │                    │                    │                  │  6. "You have a     │
     │                     │                    │                    │                  │     new message"    │
     │                     │                    │                    │                  │────────────────────►│
     │                     │                    │                    │                  │   (APNs / FCM)      │
     │                     │                    │                    │                  │                     │
     │                     │                    │                    │                  │                     │
     │           ════════════════════ User B comes online ════════════════════          │                     │
     │                     │                    │                    │                  │                     │
     │              India-WS-Server-9           │                    │                  │                     │
     │                     │  7. Register       │                    │                  │           User B    │
     │                     │     online         │                    │                  │             │       │
     │                     │◄───────────────────────────────────────────────────────────────────────── │      │
     │                     │───────────────────►│                    │                  │             │       │
     │                     │                    │                    │                  │             │       │
     │                     │  8. Fetch pending messages              │                  │             │       │
     │                     │───────────────────────────────────────► │                  │             │       │
     │                     │◄─────────────────────────────────────── │                  │             │       │
     │                     │                    │                    │                  │             │       │
     │                     │  9. Push msgs via WebSocket             │                  │    ◄────────┘       │
     │                     │─────────────────────────────────────────────────────────────────────────►│       │
     │                     │                    │                    │                  │             │       │
     │                     │  10. ACK received  │  Delete stored msg │                  │             │       │
     │                     │───────────────────────────────────────► │                  │             │       │
     │                     │                    │                    │                  │                     │
```

### 4.1 The Failed Lookup

User A's server queries the Session Registry — this time the registry responds: **"User B is offline"** (no active server ID).

### 4.2 Offline Message Storage

The message cannot be delivered instantly, so the backend **saves it**. The storage strategy depends on the privacy model:

| Model | Storage | Details |
|-------|---------|---------|
| **WhatsApp (E2EE)** | Temporary DB (Cassandra / distributed queue) | Message is encrypted on User A's device; server stores ciphertext it cannot read. Sits waiting for delivery. |
| **Telegram (Cloud Sync)** | Primary DB (permanent) | Message saved permanently for multi-device sync. |

### 4.3 Push Notifications (The Wake-Up Call)

Mobile OSes severely limit background WebSocket connections to save battery. To wake the app:

1. Backend triggers a payload to **APNs** (Apple Push Notification Service) for iOS or **FCM** (Firebase Cloud Messaging) for Android
2. Apple/Google servers deliver the notification banner to User B's phone

> **Key detail for E2EE:** The push notification payload does **not** contain the actual message text (the server can't read it). It sends a **silent data trigger**: *"Wake up, you have pending encrypted data."*

### 4.4 Reconnection & Synchronization

When User B opens the app:

1. Phone establishes a **new WebSocket** connection to the nearest server (e.g., `India-WS-Server-9`)
2. Server registers User B in the Session Registry as **"Online"**
3. App sends a request: *"Give me my pending messages"*
4. Backend pulls encrypted messages from offline storage → pushes them down the WebSocket
5. User B's phone **decrypts** the messages, displays them, and sends back an **ACK**
6. Upon receiving the ACK, the backend **permanently deletes** the message from temporary storage
