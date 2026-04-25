# Design Google Docs

## Blogs and websites

## Medium

## Youtube

## Theory

### Problem Statement
Design a real-time collaborative document editing system like Google Docs where multiple users can simultaneously edit the same document with changes appearing instantly for all participants.

### Functional Requirements
- Create, edit, delete documents (rich text)
- Real-time collaborative editing (multiple cursors)
- See other users' cursors and selections
- Commenting and suggesting mode
- Version history and rollback
- Share with permissions (view, comment, edit)
- Offline editing with sync on reconnect

### Non-Functional Requirements
- **Latency**: Keystroke-to-screen < 50ms for local, < 200ms for remote users
- **Consistency**: All users converge to same document state
- **Scale**: 100M+ documents, 10M+ concurrent editing sessions
- **Availability**: 99.99%
- **Durability**: Zero document loss

### The Core Challenge: Conflict Resolution

```
User A types "Hello" at position 5
User B deletes character at position 3 (simultaneously)

After B's delete, position 5 in A's view ≠ position 5 in B's view
→ Without conflict resolution, document diverges

Two approaches:
  1. OT (Operational Transformation) — Google Docs' original approach
  2. CRDT (Conflict-free Replicated Data Types) — Modern approach
```

### Operational Transformation (OT)

```
Core idea: Transform operations against each other

A: insert("X", pos=5)
B: delete(pos=3)

If B arrives first at server:
  Transform A against B: insert("X", pos=4)  ← shifted left by 1
  
Server maintains single ordering of operations
Clients transform their pending ops against incoming ops

Server architecture:
  Central server receives all ops
  Assigns global ordering
  Broadcasts transformed ops to all clients

Pro: Well-proven (Google Docs uses this)
Con: Central server required, complex transformation functions
```

### CRDT Approach

```
Core idea: Data structure that guarantees convergence without coordination

Each character has a unique, ordered ID:
  "Hello" → (H,id1) (e,id2) (l,id3) (l,id4) (o,id5)

IDs are designed so insertion between any two chars always works:
  Insert "X" between id2 and id3 → assign id2.5 (fractional indexing)

Operations commute: order of application doesn't matter
  → No central server needed
  → Works offline naturally

Pro: Peer-to-peer capable, simpler consistency
Con: Metadata overhead per character, garbage collection needed
```

### High-Level Architecture

```
┌──────────┐       WebSocket        ┌────────────────────────┐
│  Client  │◀═══════════════════════▶│  Collaboration Service  │
│  Editor  │   (ops + cursor pos)    │  (OT/CRDT engine)      │
└──────────┘                         └───────────┬────────────┘
                                                 │
                                    ┌────────────┼────────────┐
                                    ▼            ▼            ▼
                              ┌──────────┐ ┌──────────┐ ┌──────────┐
                              │ Document │ │ Op Log   │ │ Presence │
                              │ Store    │ │ (events) │ │ Service  │
                              └──────────┘ └──────────┘ └──────────┘
```

### Collaboration Session Flow

```
1. User opens document
   → Load latest snapshot from Document Store
   → Establish WebSocket to Collaboration Service
   → Subscribe to document channel

2. User types a character
   → Apply locally (optimistic)
   → Send operation to server via WebSocket
   → Server validates, transforms, assigns sequence number
   → Broadcast to all other connected clients
   → Other clients transform and apply

3. Cursor/selection sync
   → Each client sends cursor position periodically
   → Presence Service broadcasts to all participants
   → Display colored cursors with user names
```

### Version History

```
Approach: Periodic snapshots + operation log

  t=0:   Snapshot_0 (base document)
  t=1-50: Operations 1-50
  t=50:  Snapshot_1 (compacted)
  t=51-100: Operations 51-100
  ...

View history: Show snapshots as "versions"
Rollback: Load snapshot + replay ops up to desired point
Storage: Keep recent ops in hot storage, archive old snapshots
```

### Key Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Conflict resolution | OT (server-mediated) | Proven at scale, lower metadata |
| Transport | WebSocket | Low-latency bidirectional |
| Persistence | Snapshot + op log | Fast load + full history |
| Presence | Ephemeral pub/sub (Redis) | Real-time cursor tracking |
| Offline | Queue local ops, sync on reconnect | OT handles merge |
| Permissions | Document-level ACL | Share with view/comment/edit |

### Scaling Considerations
- **Session stickiness**: All edits for a document route to same server (partition by doc_id)
- **Hot documents**: Single doc with 100+ editors → single server bottleneck → CRDT helps here
- **Storage**: Compact old operations into snapshots periodically
- **Global**: Multi-region with conflict resolution across regions
