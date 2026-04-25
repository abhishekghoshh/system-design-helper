# WebRTC

## Blogs and websites


## Medium


## Youtube

- [WebRTC | Video Calling](https://www.youtube.com/playlist?list=PLinedj3B30sDxXVu4VXdFx678W2pJmORa)
- [System Design Behind Multi-Conference Video Calls - WebRTC vs SFU vs MCU](https://www.youtube.com/watch?v=Zaz6hYVm-WE)

## Theory

### What is WebRTC?

**WebRTC (Web Real-Time Communication)** is an open-source technology that enables peer-to-peer audio, video, and data sharing between browsers and mobile applications without requiring plugins or intermediate servers.

**Key Features:**
- 🎥 **Real-time Audio/Video**: Live streaming between peers
- 📡 **Peer-to-Peer**: Direct communication without server relay
- 🔒 **Secure**: Encrypted by default (DTLS/SRTP)
- 🌐 **Browser Native**: Built into modern browsers
- 📱 **Cross-Platform**: Works on web, iOS, Android

**Common Use Cases:**
- Video conferencing (Zoom, Google Meet, Microsoft Teams)
- Live streaming
- Screen sharing
- File sharing
- Online gaming
- Telemedicine

### Video Conferencing Architectures

When building multi-user video conferencing applications, there are three main architectural approaches:

1. **WebRTC (Peer-to-Peer Mesh)**
2. **SFU (Selective Forwarding Unit)**
3. **MCU (Multipoint Control Unit)**

Each has different trade-offs in terms of scalability, bandwidth, CPU usage, and quality.

---

### 1. WebRTC (Peer-to-Peer Mesh)

#### Description

In a **peer-to-peer (P2P) mesh** architecture, each participant establishes direct connections with every other participant in the call. Every user sends their media streams to all other users and receives streams from all other users.

```
┌─────────────────────────────────────────────────────────────┐
│           WebRTC Peer-to-Peer Mesh Architecture             │
└─────────────────────────────────────────────────────────────┘

2 PARTICIPANTS (Simple - Works Well):
─────────────────────────────────────

     ┌────────────┐
     │   Alice    │
     │  (Browser) │
     └─────┬──────┘
           │
           │ Direct P2P Connection
           │ • Video stream
           │ • Audio stream
           │
     ┌─────▼──────┐
     │    Bob     │
     │  (Browser) │
     └────────────┘

Connections: 1
Bandwidth per user: 1 upload + 1 download


4 PARTICIPANTS (Still Manageable):
───────────────────────────────────

            ┌────────────┐
            │   Alice    │
            └──┬───┬───┬─┘
               │   │   │
       ┌───────┘   │   └────────┐
       │           │            │
   ┌───▼────┐  ┌──▼─────┐  ┌───▼────┐
   │  Bob   │  │ Charlie│  │  David │
   └───┬────┘  └──┬─────┘  └───┬────┘
       │          │            │
       └──────────┼────────────┘
                  │
          All connected to all

Total Connections: 6 (n × (n-1) / 2)
Each user maintains: 3 connections

Alice uploads to: Bob, Charlie, David (3 streams)
Alice downloads from: Bob, Charlie, David (3 streams)


10 PARTICIPANTS (Problem - Doesn't Scale!):
────────────────────────────────────────────

         ┌──────┐
         │  U1  │
         └─┬─┬─┬┘
       ┌───┘ │ └────┐
    ┌──▼──┐┌─▼──┐┌──▼──┐
    │ U2  ││ U3 ││ U4  │
    └──┬──┘└─┬──┘└──┬──┘
    ┌──▼──┐┌─▼──┐┌──▼──┐
    │ U5  ││ U6 ││ U7  │
    └──┬──┘└─┬──┘└──┬──┘
    ┌──▼──┐┌─▼──┐┌──▼──┐
    │ U8  ││ U9 ││ U10 │
    └─────┘└────┘└─────┘

Total Connections: 45 (10 × 9 / 2)
Each user maintains: 9 connections
Each user uploads: 9 streams
Each user downloads: 9 streams

❌ Network Overload!
❌ CPU Overload (encoding 9 times)!
❌ Bandwidth Explosion!

BANDWIDTH CALCULATION (10 users):
─────────────────────────────────
Assume each video stream: 2 Mbps

Per User Upload: 9 streams × 2 Mbps = 18 Mbps
Per User Download: 9 streams × 2 Mbps = 18 Mbps
Total per user: 36 Mbps

Most home internet:
• Upload: 5-10 Mbps ❌ NOT ENOUGH!
• Download: 50-100 Mbps ✓ OK

Result: Call fails due to insufficient upload bandwidth
```

#### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│              WebRTC P2P Connection Flow                      │
└─────────────────────────────────────────────────────────────┘

PEER A                                              PEER B
──────                                              ──────

1. Signaling (Exchange connection info)
───────────────────────────────────────
│                                                     │
│  Create Offer (SDP)                                 │
│  - Media capabilities                               │
│  - ICE candidates (network paths)                   │
│                                                     │
│         ──────▶ Signaling Server ──────▶            │
│                                                     │
│                                         Create Answer (SDP)
│                                         - Media capabilities
│                                         - ICE candidates
│                                                     │
│         ◀────── Signaling Server ◀──────            │
│                                                     │

2. ICE (Interactive Connectivity Establishment)
───────────────────────────────────────────────
│  Find best network path:                            │
│  1. Direct connection (if possible)                 │
│  2. STUN server (NAT traversal)                     │
│  3. TURN server (relay if needed)                   │
│                                                     │
│ ◀────────── Try Connection Paths ──────────────▶    │
│                                                     │

3. Direct P2P Connection Established
────────────────────────────────────
│                                                     │
│ ◀══════════ Audio/Video Stream ═══════════════▶     │
│                 (Encrypted)                         │
│                                                     │

Media Encoding/Decoding:
──────────────────────
│  Camera → Encode → Send                             │
│           (VP8/H.264)                               │
│                                         Receive → Decode → Display
│                                         (VP8/H.264)
```

#### Advantages

```
✅ BENEFITS:
───────────

1. NO SERVER COSTS
   • Direct peer-to-peer
   • No media server infrastructure
   • Minimal hosting expenses

2. LOW LATENCY
   • Direct connection
   • No intermediate hops
   • Best for 1-on-1 calls
   • Typical latency: 20-50ms

3. PRIVACY
   • Data doesn't pass through servers
   • End-to-end encryption
   • Private conversations

4. SIMPLE ARCHITECTURE
   • Easy to implement for small scale
   • No complex server infrastructure
   • Built-in browser support

5. HIGH QUALITY
   • Direct stream, no transcoding
   • Original quality maintained
   • No quality degradation from server processing
```

#### Disadvantages

```
❌ LIMITATIONS:
──────────────

1. DOESN'T SCALE
   • Exponential connection growth: O(n²)
   • 2 users: 1 connection ✓
   • 4 users: 6 connections ⚠️
   • 10 users: 45 connections ❌
   • 50 users: 1,225 connections ❌❌❌

2. BANDWIDTH EXPLOSION
   • Each user uploads N-1 streams
   • 10-person call: Upload 18 Mbps
   • Exceeds typical home upload (5-10 Mbps)
   • Mobile devices: Even worse

3. CPU OVERLOAD
   • Must encode video N-1 times
   • Browser struggles with >4 encoders
   • Drains battery on mobile
   • Fan noise on laptops

4. INCONSISTENT QUALITY
   • Limited by weakest peer's connection
   • One poor connection affects everyone
   • Can't adapt streams per recipient

5. NAT/FIREWALL ISSUES
   • Requires STUN/TURN servers
   • Corporate firewalls may block
   • 10-20% of connections need TURN relay
   • TURN relay = not truly P2P anymore

MAXIMUM PRACTICAL PARTICIPANTS:
───────────────────────────────
Desktop: 4-6 participants
Mobile: 2-3 participants
Recommended: 1-on-1 calls only
```

#### Use Cases

```
✅ IDEAL FOR:
────────────
• 1-on-1 video calls
• Voice calls (1-on-1)
• File sharing between two users
• Gaming (2 players)
• Simple video chat apps

❌ NOT SUITABLE FOR:
───────────────────
• Group video conferences (>4 people)
• Webinars
• Live streaming to many viewers
• Enterprise video meetings
```

---

### 2. SFU (Selective Forwarding Unit)

#### Description

An **SFU** is a media server that receives video/audio streams from each participant and selectively forwards them to other participants. Unlike P2P, each client only sends one stream to the SFU, which then distributes it to others.

**Key Concept:** The SFU forwards media streams without decoding or re-encoding them.

```
┌─────────────────────────────────────────────────────────────┐
│           SFU (Selective Forwarding Unit) Architecture       │
└─────────────────────────────────────────────────────────────┘

4 PARTICIPANTS WITH SFU:
────────────────────────

     ┌────────────┐
     │   Alice    │
     └─────┬──────┘
           │ Upload: 1 stream (2 Mbps)
           │ Download: 3 streams (6 Mbps)
           ▼
     ╔═════════════════╗
     ║      SFU        ║
     ║  Media Router   ║
     ║                 ║
     ║  Forwards:      ║
     ║  • Alice → B,C,D║
     ║  • Bob → A,C,D  ║
     ║  • Charlie→A,B,D║
     ║  • David → A,B,C║
     ╚═══╦═══╦═══╦═════╝
         ║   ║   ║
    ┌────╨┐ ┌╨───┐ ┌╨────┐
    │ Bob │ │Char││David│
    └─────┘ └────┘ └─────┘

Each User:
• Uploads: 1 stream
• Downloads: N-1 streams
• Total connections: 1 (to SFU)


10 PARTICIPANTS WITH SFU (Scales Well!):
─────────────────────────────────────────

U1  U2  U3  U4  U5  U6  U7  U8  U9  U10
 │   │   │   │   │   │   │   │   │   │
 └───┴───┴───┴───┼───┴───┴───┴───┴───┘
                 │
                 ▼
         ╔═══════════════╗
         ║      SFU      ║
         ║               ║
         ║   Forwards    ║
         ║   streams     ║
         ║   to all      ║
         ╚═══════════════╝
                 │
     ┌───────────┼───────────┐
     │           │           │
     ▼           ▼           ▼
   Each user receives 9 streams

Per User Bandwidth:
• Upload: 1 stream = 2 Mbps ✓
• Download: 9 streams = 18 Mbps ✓

Server Bandwidth:
• Receives: 10 streams = 20 Mbps
• Sends: 90 streams = 180 Mbps
(Each of 10 streams sent to 9 participants)


100 PARTICIPANTS WITH SFU (With Optimizations):
────────────────────────────────────────────────

                ╔═══════════════╗
                ║      SFU      ║
                ║               ║
                ║  Simulcast:   ║
                ║  • HD: 2 Mbps ║
                ║  • SD: 500Kbps║
                ║  • Low:200Kbps║
                ║               ║
                ║  Smart Logic: ║
                ║  • Active speaker: HD
                ║  • Others: Low quality
                ╚═══════════════╝

Per User Bandwidth (optimized):
• Upload: 1 stream (multi-quality)
• Download: Active + thumbnails
  = 2 Mbps (active) + 10×200Kbps (thumbnails)
  = 4 Mbps total ✓

✅ Scales to 100+ participants!
```

#### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                SFU Processing Flow                           │
└─────────────────────────────────────────────────────────────┘

PARTICIPANT                 SFU                    PARTICIPANTS
───────────                ─────                   ────────────

Alice sends stream:
┌────────────┐
│  Camera    │
│    ↓       │
│  Encode    │ 1080p
│  (H.264)   │ 2 Mbps
└─────┬──────┘
      │
      │ Upload 1 stream
      ▼
    ╔═══════════════════════════════╗
    ║           SFU                 ║
    ║                               ║
    ║  1. RECEIVE stream from Alice ║
    ║     (encrypted)               ║
    ║         ↓                     ║
    ║  2. FORWARD without changes   ║
    ║     (no decoding/encoding)    ║
    ║         ↓                     ║
    ║  3. ROUTE to recipients       ║
    ║     • Bob                     ║
    ║     • Charlie                 ║
    ║     • David                   ║
    ║                               ║
    ║  ⚡ Low CPU (no transcoding)  ║
    ║  ⚡ Low latency (<50ms)       ║
    ╚═══════════════════════════════╝
            │       │       │
            │       │       │
    ┌───────▼┐  ┌──▼────┐  ┌▼──────┐
    │  Bob   │  │Charlie│  │ David │
    │        │  │       │  │       │
    │ Decode │  │Decode │  │Decode │
    │Display │  │Display│  │Display│
    └────────┘  └───────┘  └───────┘

SIMULCAST (Multi-quality streaming):
────────────────────────────────────

Alice's browser encodes SAME video at 3 qualities:

Camera Feed
    ↓
┌──────────────────────┐
│  Encoder 1: 1080p    │ 2 Mbps (high)
│  Encoder 2: 720p     │ 1 Mbps (medium)
│  Encoder 3: 360p     │ 300 Kbps (low)
└──────────┬───────────┘
           │ All 3 sent to SFU
           ▼
    ╔═══════════════════════════════╗
    ║           SFU                 ║
    ║                               ║
    ║  Smart Routing:               ║
    ║                               ║
    ║  Bob (good connection):       ║
    ║    → Send 1080p               ║
    ║                               ║
    ║  Charlie (medium):            ║
    ║    → Send 720p                ║
    ║                               ║
    ║  David (poor/mobile):         ║
    ║    → Send 360p                ║
    ╚═══════════════════════════════╝

BANDWIDTH ADAPTATION:
─────────────────────

SFU monitors each recipient's connection:

┌────────────────────────────────────┐
│ Bob's Connection                   │
│ ├─ Bandwidth: 10 Mbps ✓           │
│ ├─ Packet loss: 0.1% ✓            │
│ └─ Latency: 30ms ✓                │
│                                    │
│ Decision: Send HD quality          │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│ David's Connection                 │
│ ├─ Bandwidth: 1 Mbps ⚠️            │
│ ├─ Packet loss: 5% ⚠️              │
│ └─ Latency: 150ms ⚠️               │
│                                    │
│ Decision: Send Low quality         │
│ (Better to have choppy low-res     │
│  than frozen high-res)             │
└────────────────────────────────────┘
```

#### Advantages

```
✅ BENEFITS:
───────────

1. EXCELLENT SCALABILITY
   • Handles 100+ participants
   • Linear bandwidth growth for clients
   • Each user: 1 upload, N downloads
   • No exponential connection growth

2. EFFICIENT BANDWIDTH
   • Clients upload only 1 stream
   • 10-person call: 2 Mbps upload (vs 18 Mbps in P2P)
   • Works on typical home internet
   • Mobile-friendly

3. LOW CLIENT CPU
   • Encode once, SFU distributes
   • No need to encode multiple times
   • Better battery life
   • Works on low-end devices

4. ADAPTIVE QUALITY (Simulcast)
   • Send different quality to each user
   • High quality for good connections
   • Low quality for poor connections
   • Each user gets best possible experience

5. FAST & LOW LATENCY
   • No transcoding (forwarding only)
   • Typical latency: 50-150ms
   • Near real-time communication
   • Much faster than MCU

6. EASY TO SCALE HORIZONTALLY
   • Add more SFU servers
   • Load balance across servers
   • Geographic distribution (CDN-like)

7. COST EFFECTIVE
   • Lower server costs than MCU
   • No heavy CPU for transcoding
   • Can use cheaper servers
```

#### Disadvantages

```
❌ LIMITATIONS:
──────────────

1. SERVER INFRASTRUCTURE REQUIRED
   • Need to host SFU servers
   • Operational costs
   • Maintenance overhead
   • Not free like P2P

2. HIGH CLIENT DOWNLOAD BANDWIDTH
   • Still receives N-1 streams
   • 100-person call: Download 100+ streams
   • Can overwhelm client connection
   • Mitigated with simulcast + active speaker

3. HIGH SERVER BANDWIDTH
   • Must receive all streams
   • Must send all streams to all participants
   • 100 users = receive 100, send 9,900 streams
   • Expensive bandwidth costs at scale

4. CLIENT MUST DECODE MULTIPLE STREAMS
   • CPU to decode 9-100 video streams
   • Memory usage
   • Can struggle on low-end devices
   • Mitigated with active speaker layouts

5. NO BUILT-IN RECORDING
   • SFU doesn't decode streams
   • Recording requires separate component
   • Must record all individual streams
   • Post-processing needed for single output

6. NETWORK QUALITY VARIES PER USER
   • Each user sees different quality
   • Depends on their connection
   • Inconsistent experience
   • Some see HD, others see potato quality

7. REQUIRES SIMULCAST SUPPORT
   • Not all browsers support it well
   • Adds complexity to client
   • Triples encoding bandwidth (3 qualities)
```

#### Use Cases

```
✅ IDEAL FOR:
────────────
• Group video calls (4-100 people)
• Virtual meetings (Zoom, Google Meet, Microsoft Teams)
• Online education (moderate class sizes)
• Telemedicine
• Remote interviews
• Gaming streams with viewers
• Social video apps

✅ BEST FOR:
───────────
• Interactive video conferences
• When low latency is critical (<200ms)
• When participants need to see each other
• When quality can vary per user
```

---

### 3. MCU (Multipoint Control Unit)

#### Description

An **MCU** is a media server that receives all participant streams, **decodes them**, **mixes/composes them** into a single unified stream, and **re-encodes** it before sending to each participant. Each participant receives one combined video layout.

**Key Concept:** The MCU does heavy processing - decode, mix, encode.

```
┌─────────────────────────────────────────────────────────────┐
│         MCU (Multipoint Control Unit) Architecture           │
└─────────────────────────────────────────────────────────────┘

4 PARTICIPANTS WITH MCU:
────────────────────────

┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
│Alice │  │ Bob  │  │Charli│  │David │
└───┬──┘  └──┬───┘  └──┬───┘  └──┬───┘
    │        │         │         │
    │ 1080p  │ 1080p   │ 1080p   │ 1080p
    │ 2 Mbps │ 2 Mbps  │ 2 Mbps  │ 2 Mbps
    │        │         │         │
    └────────┴────┬────┴─────────┘
                  ▼
         ╔════════════════════╗
         ║        MCU         ║
         ║                    ║
         ║  1. RECEIVE all    ║
         ║  2. DECODE all     ║
         ║  3. COMPOSE layout ║
         ║     ┌─────┬─────┐  ║
         ║     │ A   │ B   │  ║
         ║     ├─────┼─────┤  ║
         ║     │ C   │ D   │  ║
         ║     └─────┴─────┘  ║
         ║  4. ENCODE once    ║
         ║  5. SEND to all    ║
         ╚══════════╦═════════╝
                    │
                    │ Same stream to everyone
         ┌──────────┼──────────┐
         │          │          │
    ┌────▼──┐  ┌────▼──┐  ┌───▼───┐  ┌────▼──┐
    │Alice  │  │ Bob   │  │Charlie│  │ David │
    │       │  │       │  │       │  │       │
    │ Grid  │  │ Grid  │  │ Grid  │  │ Grid  │
    │Layout │  │Layout │  │Layout │  │Layout │
    └───────┘  └───────┘  └───────┘  └───────┘

Each User:
• Upload: 1 stream (2 Mbps)
• Download: 1 stream (2 Mbps) ✓✓✓ Very efficient!
• Total: 4 Mbps (vs 8 Mbps in SFU, 36 Mbps in P2P)


10 PARTICIPANTS WITH MCU:
─────────────────────────

10 users send individual streams
           ↓
    ╔═══════════════════════════╗
    ║           MCU             ║
    ║                           ║
    ║  DECODE: 10 streams       ║
    ║      ↓                    ║
    ║  COMPOSE: Grid layout     ║
    ║  ┌──┬──┬──┬──┬──┐         ║
    ║  │U1│U2│U3│U4│U5│         ║
    ║  ├──┼──┼──┼──┼──┤         ║
    ║  │U6│U7│U8│U9│10│         ║
    ║  └──┴──┴──┴──┴──┘         ║
    ║      ↓                    ║
    ║  ENCODE: 1 composed video ║
    ║                           ║
    ╚═══════════════════════════╝
                │
      Same composite to all 10 users

Per User Bandwidth:
• Upload: 2 Mbps
• Download: 2 Mbps
• Total: 4 Mbps ✓

MCU Server:
• CPU: VERY HIGH (decode 10, encode 1)
• Bandwidth: Moderate (receive 10, send 10)


100 PARTICIPANTS WITH MCU:
──────────────────────────

MCU creates different layouts for different roles:

    ╔═══════════════════════════╗
    ║           MCU             ║
    ║                           ║
    ║  Presenter View:          ║
    ║  ┌─────────────────────┐  ║
    ║  │   Active Speaker    │  ║
    ║  │      (Large)        │  ║
    ║  └─────────────────────┘  ║
    ║                           ║
    ║  Attendee View:           ║
    ║  ┌────────┐               ║
    ║  │Speaker │               ║
    ║  └────────┘               ║
    ║  (Small, presenter only)  ║
    ║                           ║
    ╚═══════════════════════════╝

Per User Bandwidth:
• Upload: 2 Mbps (or muted for attendees)
• Download: 2 Mbps (single composite)
• Total: 2-4 Mbps ✓✓✓

✅ Extremely efficient for client!
❌ Extremely expensive for server!
```

#### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│              MCU Processing Pipeline                         │
└─────────────────────────────────────────────────────────────┘

STEP 1: RECEIVE
───────────────

Alice    Bob    Charlie   David
  │       │        │        │
  │ H.264 │ H.264  │ H.264  │ VP8
  │ 1080p │ 720p   │ 1080p  │ 720p
  │       │        │        │
  └───────┴────────┴────────┘
            ↓
    ╔═══════════════════╗
    ║  MCU - Receive    ║
    ║  4 different      ║
    ║  streams          ║
    ╚═══════════════════╝

STEP 2: DECODE
──────────────

    ╔═══════════════════╗
    ║  MCU - Decode     ║
    ║                   ║
    ║  Decoder 1: H.264 → Raw video frames
    ║  Decoder 2: H.264 → Raw video frames
    ║  Decoder 3: H.264 → Raw video frames
    ║  Decoder 4: VP8   → Raw video frames
    ║                   ║
    ║  Output: Raw RGB/YUV frames
    ║                   ║
    ║  🔥 CPU INTENSIVE!
    ╚═══════════════════╝

STEP 3: COMPOSE/MIX
───────────────────

    ╔═══════════════════════════════════╗
    ║  MCU - Video Compositor           ║
    ║                                   ║
    ║  Create layout:                   ║
    ║                                   ║
    ║  ┌─────────────────────────────┐  ║
    ║  │  Canvas: 1920 × 1080        │  ║
    ║  │                             │  ║
    ║  │  ┌──────┬──────┐            │  ║
    ║  │  │Alice │ Bob  │            │  ║
    ║  │  │960×540│960×540           │  ║
    ║  │  ├──────┼──────┤            │  ║
    ║  │  │Charl.│David │            │  ║
    ║  │  │960×540│960×540           │  ║
    ║  │  └──────┴──────┘            │  ║
    ║  │                             │  ║
    ║  │  + Overlay graphics         │  ║
    ║  │  + Names, logos             │  ║
    ║  │  + Highlight active speaker │  ║
    ║  └─────────────────────────────┘  ║
    ║                                   ║
    ║  🔥 CPU & MEMORY INTENSIVE!       ║
    ╚═══════════════════════════════════╝

    Audio Mixing:
    ┌─────────────────────────────────┐
    │  Mix all audio streams:         │
    │  Alice audio + Bob audio +      │
    │  Charlie audio + David audio    │
    │  = Single mixed audio track     │
    │                                 │
    │  • Remove echo                  │
    │  • Normalize volume             │
    │  • Suppress background noise    │
    └─────────────────────────────────┘

STEP 4: ENCODE
──────────────

    ╔═══════════════════════════════════╗
    ║  MCU - Encoder                    ║
    ║                                   ║
    ║  Composite video + Mixed audio    ║
    ║         ↓                         ║
    ║  Encode to H.264/VP8              ║
    ║  1080p @ 2 Mbps                   ║
    ║         ↓                         ║
    ║  Single output stream             ║
    ║                                   ║
    ║  🔥 CPU INTENSIVE!                ║
    ╚═══════════════════════════════════╝

STEP 5: DISTRIBUTE
──────────────────

    ╔═══════════════════════════════════╗
    ║  MCU - Send                       ║
    ║                                   ║
    ║  Same stream to all participants  ║
    ║         ↓         ↓         ↓     ║
    ╚═════════╦═════════╦═════════╦═════╝
              │         │         │
         ┌────▼──┐ ┌────▼──┐ ┌───▼────┐
         │Alice  │ │ Bob   │ │ Charlie│
         │       │ │       │ │        │
         │Decode │ │Decode │ │ Decode │
         │   +   │ │   +   │ │   +    │
         │Display│ │Display│ │Display │
         └───────┘ └───────┘ └────────┘

CPU USAGE COMPARISON:
─────────────────────

P2P (4 users):
├─ Each user encodes: 3 times
├─ Each user decodes: 3 times
└─ Total: 12 encode + 12 decode operations

SFU (4 users):
├─ Each user encodes: 1 time
├─ Each user decodes: 3 times
├─ SFU: 0 encode, 0 decode (just forwards)
└─ Total: 4 encode + 12 decode operations

MCU (4 users):
├─ Each user encodes: 1 time
├─ Each user decodes: 1 time
├─ MCU: 4 decode + 1 encode
└─ Total: 5 encode + 8 decode operations
    But MCU handles heavy lifting on server!
```

#### Advantages

```
✅ BENEFITS:
───────────

1. ULTRA-EFFICIENT CLIENT BANDWIDTH
   • Upload: 1 stream (2 Mbps)
   • Download: 1 stream (2 Mbps)
   • Total: 4 Mbps (same for 10 or 100 people!)
   • Perfect for poor connections
   • Great for mobile devices

2. MINIMAL CLIENT CPU
   • Encode once
   • Decode once
   • No matter how many participants
   • Excellent battery life
   • Works on very low-end devices

3. CONSISTENT QUALITY
   • Everyone sees same quality
   • No variation between users
   • Predictable experience
   • Professional appearance

4. ADVANCED FEATURES
   • Custom layouts (grid, spotlight, picture-in-picture)
   • Active speaker detection
   • Screen share layouts
   • Branding/overlays
   • Real-time effects
   • Background replacement (server-side)

5. BUILT-IN RECORDING
   • Easy to record
   • One stream to capture
   • No post-processing needed
   • Single video file output

6. WORKS ON TERRIBLE NETWORKS
   • Low bandwidth requirements
   • 2-4 Mbps sufficient
   • 2G/3G compatible
   • Dial-in phone integration possible

7. CONTROL & MODERATION
   • Server controls who sees what
   • Easy to mute/remove participants
   • Layout control
   • Recording/compliance
```

#### Disadvantages

```
❌ LIMITATIONS:
──────────────

1. EXTREMELY CPU INTENSIVE
   • Must decode ALL incoming streams
   • Must encode output stream
   • 100 participants = decode 100 + encode 1
   • Requires powerful servers
   • High cooling/power costs

2. HIGH INFRASTRUCTURE COSTS
   • Expensive hardware (GPUs often needed)
   • High operational costs
   • Complex to maintain
   • Doesn't scale horizontally easily

3. HIGHER LATENCY
   • Decode → Compose → Encode pipeline
   • Typical latency: 200-500ms
   • Not suitable for real-time interaction
   • Noticeable delay in conversations

4. SINGLE POINT OF FAILURE
   • If MCU fails, entire call fails
   • Difficult to load balance
   • Complex failover

5. FIXED LAYOUT
   • Everyone sees same view
   • Can't personalize
   • Can't see all participants in large calls
   • Limited flexibility

6. QUALITY BOTTLENECK
   • Limited by MCU's encoding quality
   • Can't deliver higher than MCU output
   • 1080p limit common
   • Original quality lost (transcoding)

7. SCALING IS EXPENSIVE
   • Linear cost per participant
   • Can't easily add servers
   • Each MCU handles full processing
   • Very expensive for large calls

CPU COST EXAMPLE (10 participants):
───────────────────────────────────
Decode 10 streams:  10 CPU cores
Compose:            2 CPU cores
Encode 1 stream:    2 CPU cores
Total:              14 CPU cores

vs SFU:             0 CPU cores (forwarding only)
vs P2P:             0 server cost
```

#### Use Cases

```
✅ IDEAL FOR:
────────────
• Webinars (presenter + many viewers)
• Online classes (teacher + students)
• Broadcasting to large audiences
• Corporate town halls
• Dial-in phone participants
• Very poor network environments (2G/3G)
• Regulated industries (recording/compliance)
• Professional broadcasts

✅ WHEN TO USE:
──────────────
• Need consistent quality for all
• Recording is essential
• Many participants with poor connections
• Custom branded layouts required
• Budget for server infrastructure
• Latency <500ms is acceptable
```

---

### Comparison: WebRTC vs SFU vs MCU

#### Architecture Comparison

```
┌─────────────────────────────────────────────────────────────┐
│               Architecture Comparison                        │
└─────────────────────────────────────────────────────────────┘

PEER-TO-PEER (WebRTC Mesh):
───────────────────────────
U1 ◀──▶ U2
 ◀───X───▶
 │       │
U3 ◀──▶ U4

Characteristics:
• Direct connections
• No server
• Fully distributed


SFU (Selective Forwarding Unit):
─────────────────────────────────
U1 ──▶ ┌───────┐ ──▶ U2, U3, U4
U2 ──▶ │  SFU  │ ──▶ U1, U3, U4
U3 ──▶ │Forward│ ──▶ U1, U2, U4
U4 ──▶ └───────┘ ──▶ U1, U2, U3

Characteristics:
• Centralized routing
• No transcoding
• Fast forwarding


MCU (Multipoint Control Unit):
───────────────────────────────
U1 ──▶ ┌───────────┐
U2 ──▶ │    MCU    │
U3 ──▶ │  Decode   │
U4 ──▶ │  Compose  │ ──▶ Composite ──▶ All users
       │  Encode   │
       └───────────┘

Characteristics:
• Centralized processing
• Full transcoding
• Single output
```

#### Feature Comparison Table

| Feature | P2P (Mesh) | SFU | MCU |
|---------|-----------|-----|-----|
| **Max Participants** | 2-4 | 50-100+ | 100-1000+ |
| **Client Upload BW** | High (N-1 streams) | Low (1 stream) | Low (1 stream) |
| **Client Download BW** | High (N-1 streams) | High (N-1 streams) | Very Low (1 stream) |
| **Client CPU** | Very High | Medium | Very Low |
| **Server CPU** | None | Very Low | Very High |
| **Server Cost** | $0 | $$ | $$$$ |
| **Latency** | 20-50ms | 50-150ms | 200-500ms |
| **Quality** | Best | Good | Medium |
| **Scalability** | ❌ Poor | ✅ Good | ⚠️ Expensive |
| **Bandwidth Efficiency** | ❌ Poor | ⚠️ Medium | ✅ Excellent |
| **Recording** | Hard | Medium | Easy |
| **Custom Layouts** | No | No | Yes |
| **Works on Mobile** | 2-3 users | Yes | Yes (best) |
| **Works on Poor Network** | No | Medium | ✅ Best |

#### Bandwidth Comparison (10 Participants, 2 Mbps per stream)

```
┌─────────────────────────────────────────────────────────────┐
│          Bandwidth Usage Comparison (10 Users)               │
└─────────────────────────────────────────────────────────────┘

PER USER:
─────────

P2P Mesh:
├─ Upload: 9 streams × 2 Mbps = 18 Mbps ❌ Too high!
├─ Download: 9 streams × 2 Mbps = 18 Mbps
└─ Total: 36 Mbps per user

SFU:
├─ Upload: 1 stream × 2 Mbps = 2 Mbps ✓
├─ Download: 9 streams × 2 Mbps = 18 Mbps ⚠️
└─ Total: 20 Mbps per user

MCU:
├─ Upload: 1 stream × 2 Mbps = 2 Mbps ✓
├─ Download: 1 composite × 2 Mbps = 2 Mbps ✓✓
└─ Total: 4 Mbps per user ✅ Best!


SERVER:
───────

P2P Mesh:
└─ Server bandwidth: 0 (no server)

SFU:
├─ Receive: 10 streams × 2 Mbps = 20 Mbps
├─ Send: 10 streams × 9 recipients = 180 Mbps
└─ Total: 200 Mbps

MCU:
├─ Receive: 10 streams × 2 Mbps = 20 Mbps
├─ Send: 1 composite × 10 recipients = 20 Mbps
└─ Total: 40 Mbps ✅ Efficient


TOTAL NETWORK TRAFFIC:
──────────────────────

P2P: 10 users × 36 Mbps = 360 Mbps total
SFU: 200 Mbps server + (10 × 2 uploads) = 220 Mbps
MCU: 40 Mbps server + (10 × 2 uploads) = 60 Mbps ✅ Lowest
```

#### Cost Comparison (100 Participants)

```
┌─────────────────────────────────────────────────────────────┐
│              Monthly Cost Estimation (100 users)             │
└─────────────────────────────────────────────────────────────┘

P2P (Peer-to-Peer):
───────────────────
Server Costs: $0
STUN/TURN: $50-100/month
Total: ~$100/month

❌ But doesn't work! (Can't handle 100 users)


SFU (Selective Forwarding Unit):
─────────────────────────────────
Server Instances: 5 × $200 = $1,000
Bandwidth: 50 TB × $10/TB = $500
Total: ~$1,500/month

✅ Scales well, reasonable cost


MCU (Multipoint Control Unit):
───────────────────────────────
GPU Servers: 10 × $500 = $5,000
Bandwidth: 10 TB × $10/TB = $100
Total: ~$5,100/month

⚠️ Expensive but best quality
```

#### When to Use Each Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Decision Matrix                             │
└─────────────────────────────────────────────────────────────┘

USE P2P (WebRTC Mesh) WHEN:
──────────────────────────
✓ Only 1-on-1 or max 4 people
✓ Want zero server costs
✓ Need lowest possible latency
✓ Privacy is critical (no server)
✓ Simple use case

Examples: FaceTime, WhatsApp video (1-on-1), peer file sharing


USE SFU WHEN:
────────────
✓ Group calls (4-100 people) ← Most common!
✓ Need low latency (<200ms)
✓ Interactive communication
✓ Users need to see each other
✓ Quality can vary per user
✓ Reasonable budget

Examples: Zoom, Google Meet, Microsoft Teams, Discord


USE MCU WHEN:
────────────
✓ Large webinars (100+ viewers)
✓ Broadcasting/streaming
✓ Very poor client connections
✓ Need professional layouts
✓ Recording is essential
✓ Compliance requirements
✓ Budget for infrastructure
✓ Latency <500ms acceptable

Examples: Cisco Webex, professional broadcasts, online classes


HYBRID APPROACHES:
─────────────────

Many modern platforms use combinations:

1. SFU + Active Speaker Layout:
   └─ SFU forwards streams
   └─ Client shows only active speaker + thumbnails
   └─ Reduces decode load

2. SFU + MCU fallback:
   └─ SFU for most users
   └─ MCU for dial-in phone participants
   └─ Best of both worlds

3. Cascading SFUs:
   └─ Multiple SFUs in different regions
   └─ Reduce latency globally
   └─ Better scalability
```

#### Real-World Examples

```
┌─────────────────────────────────────────────────────────────┐
│            Real-World Platform Architectures                 │
└─────────────────────────────────────────────────────────────┘

ZOOM:
─────
Primary: SFU
Features:
• Up to 1,000 participants (SFU)
• Gallery view: SFU sends all streams
• Active speaker view: Optimized SFU
• Recording: MCU component
• Phone dial-in: MCU gateway

Architecture: Hybrid SFU + MCU


GOOGLE MEET:
───────────
Primary: SFU
Features:
• Up to 250 participants
• Simulcast for quality adaptation
• AI-powered active speaker detection
• Low latency mode

Architecture: Pure SFU with smart routing


MICROSOFT TEAMS:
───────────────
Primary: SFU with MCU fallback
Features:
• SFU for modern clients
• MCU for legacy/phone participants
• Together mode (MCU-composed view)
• Recording uses MCU

Architecture: Hybrid


DISCORD:
────────
Primary: SFU
Features:
• Voice channels: P2P (small groups)
• Video: SFU (larger groups)
• Go Live streaming: SFU
• Very low latency focus

Architecture: P2P → SFU based on size


WHATSAPP:
─────────
Primary: P2P
Features:
• 1-on-1: Direct P2P
• Group calls (2-8): P2P Mesh
• Max 8 participants
• End-to-end encrypted

Architecture: Pure P2P (limited scale)


FACETIME:
─────────
Primary: P2P → SFU
Features:
• 1-on-1: P2P
• Group (3+): Apple's SFU servers
• Up to 32 participants
• Low latency

Architecture: Hybrid P2P/SFU
```

#### Summary & Best Practices

```
KEY TAKEAWAYS:
─────────────

1. P2P (WebRTC Mesh):
   ✅ Best for: 1-on-1 calls
   ❌ Don't use for: >4 participants

2. SFU (Selective Forwarding Unit):
   ✅ Best for: Group video calls (4-100)
   ✅ Sweet spot: Interactive communication
   ❌ High client download bandwidth

3. MCU (Multipoint Control Unit):
   ✅ Best for: Webinars, broadcasts, poor networks
   ✅ Ultra-efficient for clients
   ❌ Expensive servers, higher latency


MODERN BEST PRACTICE:
────────────────────

Start with SFU, add optimizations:

1. Simulcast: Multiple quality layers
2. Active Speaker: Highlight main speaker
3. Thumbnail view: Low quality for non-speakers
4. Adaptive bitrate: Adjust to network
5. Screen share priority: Boost presentation quality
6. Spatial audio: Better audio experience

This gives 95% of users great experience
at reasonable cost!


SCALING STRATEGY:
────────────────

Small (2-4):     P2P
Medium (5-50):   SFU
Large (50-100):  SFU + optimizations
Huge (100+):     SFU + MCU hybrid
Broadcast:       MCU or CDN streaming
```
