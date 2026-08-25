# Design Online Code Editor

## Blogs and websites

## Medium

## Youtube

## Theory

### Problem Statement
Design an online collaborative code editor like Replit, CodeSandbox, or VS Code for the Web that supports writing, running, and debugging code in multiple languages with real-time collaboration.

### Functional Requirements
- Create projects with file/folder structure
- Edit code with syntax highlighting, autocompletion, linting
- Run code in multiple languages (Python, JS, Go, Java, etc.)
- Real-time collaborative editing (multiple cursors)
- Terminal access
- File management (create, rename, delete, upload)
- Share projects with a URL
- Version history / snapshots

### Non-Functional Requirements
- **Latency**: Keystrokes < 50ms, code execution start < 2s
- **Scale**: 1M+ concurrent coding sessions
- **Security**: Code execution must be fully sandboxed
- **Availability**: 99.9%
- **Isolation**: One user's code cannot affect another's environment

### High-Level Architecture

```
┌──────────┐      WebSocket       ┌─────────────────────────────┐
│  Browser  │◀══════════════════▶│      Service Layer           │
│  (Monaco  │                     │                              │
│  Editor)  │                     │  ┌────────────────────────┐  │
└───────────┘                     │  │ Collaboration Service   │  │
                                  │  │ Project Service         │  │
                                  │  │ Execution Service       │  │
                                  │  │ Language Server (LSP)   │  │
                                  │  └───────────┬────────────┘  │
                                  └──────────────┼───────────────┘
                                                 │
                              ┌──────────────────┼──────────────────┐
                              ▼                  ▼                  ▼
                       ┌────────────┐     ┌────────────┐    ┌────────────┐
                       │  Project   │     │ Container  │    │  File      │
                       │  Store DB  │     │ Orchestrator│   │  Storage   │
                       └────────────┘     └────────────┘    └────────────┘
```

### Code Execution Sandbox

```
Each user session gets an isolated container:

┌─────────────────────────────────────┐
│  Container (per session)            │
│  ┌───────────────────────────────┐  │
│  │  Language runtime (Python 3)  │  │
│  │  User's code files            │  │
│  │  Terminal (PTY)               │  │
│  └───────────────────────────────┘  │
│                                     │
│  Resource limits:                   │
│    CPU: 0.5 cores                   │
│    Memory: 512MB                    │
│    Disk: 1GB                        │
│    Network: restricted (no egress   │
│    to internal services)            │
│    Time: 30s max execution          │
│                                     │
│  Technology: gVisor / Firecracker   │
│  → Kernel-level isolation           │
│  → Syscall filtering                │
└─────────────────────────────────────┘

Container lifecycle:
  User opens project → warm container from pool
  User idle > 10min → snapshot + hibernate
  User returns → restore from snapshot (fast resume)
```

### Real-Time Collaboration

```
Uses same approach as Google Docs:
  OT (Operational Transformation) or CRDT

Client edits → send ops via WebSocket → server transforms
  → broadcast to all collaborators

Presence:
  - Cursor positions with user colors
  - Selection highlights
  - Active file indicator per user

Session management:
  - Document partitioned by project_id
  - All collaborators connect to same server (sticky sessions)
  - Operation log for undo/redo across users
```

### Language Server Protocol (LSP)

```
Each container runs a language server:
  Python → Pylance/Pyright
  JS/TS → tsserver
  Go → gopls

Browser editor ↔ WebSocket ↔ LSP Proxy ↔ Container LSP

Features powered by LSP:
  - Autocomplete
  - Go to definition
  - Find references
  - Inline errors/warnings
  - Hover documentation
```

### Key Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Editor | Monaco (VS Code's editor) | Industry standard, extensible |
| Sandbox | Firecracker microVMs | Strong isolation, fast boot (~125ms) |
| Collaboration | CRDT (Yjs) | Offline-capable, no central bottleneck |
| File storage | Object store (S3) + local container FS | Persist + fast access |
| Container pool | Pre-warmed containers per language | Instant project open |
| LSP | Per-container language server | Full IDE intelligence |

### Scaling Considerations
- **Container scheduling**: Kubernetes + custom scheduler for bin-packing
- **Warm pool**: Maintain ready containers per language (scale with demand)
- **File sync**: Background sync from container FS → S3 (every few seconds)
- **Global**: Multi-region deployment, route user to nearest region
- **Cost**: Hibernate idle containers, resume on demand
