# TCP Protocol (Transmission Control Protocol)

## Blogs and websites


## Medium


## Youtube


## Theory

> **Network Protocols** are rules and standards for network communication.
> **Layer Models:** OSI Model (7 layers) | TCP/IP Model (4 layers: Network Access, Internet, Transport, Application)

### The Reliable Foundation of the Internet

TCP is one of the **crown jewels of computer science**—a protocol so elegant and robust that it has powered the internet for over 40 years. It represents the solution to one of computing's hardest problems: **how to guarantee reliable, ordered delivery over an unreliable network**.

### The Deep Theory: Solving the Impossible

**The Problem TCP Solves:**
The internet is fundamentally **unreliable**:
- Packets get lost (router failures, congestion)
- Packets get corrupted (bit flips, interference)
- Packets arrive out of order (different routes)
- Network speed varies wildly (congestion, routing changes)

Yet applications need **reliability**:
- Every byte must arrive
- Bytes must be in the correct order
- No duplicates, no corruption

TCP creates **reliability from unreliability**—an almost magical transformation.

### The Three-Way Handshake: Establishing Truth

```
Client                                Server
  |                                      |
  |-------SYN (seq=100)----------------->|
  |  "I want to talk, my sequence is 100"
  |                                      |
  |<------SYN-ACK (seq=300, ack=101)-----|
  |  "OK, my sequence is 300, I got your 100"
  |                                      |
  |-------ACK (ack=301)----------------->|
  |  "Got it, let's begin"
  |                                      |
  |  <Connection established>            |
```

**Why Three Steps?**
- **Two steps aren't enough**: Server needs to know client received its SYN-ACK
- **Prevents ghost connections**: Old duplicate packets can't create false connections
- **Synchronizes sequence numbers**: Both sides agree on starting point
- **Allocates resources**: Both sides commit to the connection

**The Philosophy:**
The handshake embodies **mutual agreement**. Both parties must explicitly agree to communicate before resources are committed. This prevents:
- SYN flood attacks (partially mitigated)
- Resource exhaustion
- Ambiguous connection state

### Guaranteed Delivery: The Acknowledgment Dance

**How It Works:**
```
Sender                               Receiver
  |                                     |
  |----Packet 1 (seq=100, data="Hello")-|
  |                                     |
  |<---ACK 105 ("Got bytes 100-104")---|
  |                                     |
  |----Packet 2 (seq=105, data="World")-|
  |                                     |
  |  (packet lost!)                     |
  |                                     |
  |  <timeout expires>                  |
  |                                     |
  |----Packet 2 (seq=105, RETRANSMIT)---|
  |                                     |
  |<---ACK 110 ("Got bytes 105-109")---|
```

**The Mechanisms:**

1. **Sequence Numbers**: Every byte has a number
   - Allows detection of gaps (missing data)
   - Enables reordering (out-of-order arrival)
   - Prevents duplicates (ignore old sequences)

2. **Acknowledgments (ACKs)**: Receiver confirms receipt
   - **Cumulative**: ACK 1000 means "got everything up to 999"
   - **Selective** (SACK): Can acknowledge non-contiguous ranges

3. **Retransmission**: If no ACK, resend
   - **Timeout-based**: Wait for ACK, resend if timeout
   - **Adaptive timeout**: Learn network RTT, adjust timeout
   - **Fast retransmit**: Three duplicate ACKs trigger immediate resend

### Flow Control: Respecting the Receiver

**The Problem:**
Sender can produce data faster than receiver can consume it.

**The Solution: Sliding Window**
```
Receiver: "I have 10KB buffer available" (window size = 10KB)
Sender: "Got it, I'll send max 10KB unacknowledged data"
  ↓
Sender: Sends 8KB
Receiver: Processes 3KB, ACKs and says "window = 5KB now"
Sender: "OK, I can send 5KB more"
```

**Window Size = 0:**
- Receiver buffer is full
- Sender must stop sending
- Waits for window update
- **Prevents**: Buffer overflow, data loss

**The Elegance:**
Flow control is **receiver-driven**. The receiver controls the pace, ensuring it's never overwhelmed.

### Congestion Control: Respecting the Network

**The Problem:**
Sending too fast causes network congestion:
- Routers drop packets
- Retransmissions increase load
- Network collapse (congestion collapse)

**The Solution: Adaptive Rate Control**

TCP dynamically adjusts sending rate based on network conditions.

**Algorithms:**

1. **Slow Start** (Exponential Growth):
   ```
   Start: Send 1 packet
   Got ACK: Send 2 packets
   Got ACKs: Send 4 packets
   ... (doubles each RTT until threshold)
   ```
   - **Fast growth** from slow start
   - **Goal**: Quickly find network capacity

2. **Congestion Avoidance** (Linear Growth):
   ```
   After threshold: Increase by 1 packet per RTT
   Got ACKs: Window += 1/window
   ```
   - **Careful growth** near capacity
   - **Goal**: Avoid triggering congestion

3. **Fast Recovery** (After Packet Loss):
   ```
   Packet loss detected
   → Reduce window by half (multiplicative decrease)
   → Continue sending (don't stop)
   → Slowly increase again (additive increase)
   ```
   - **AIMD**: Additive Increase, Multiplicative Decrease
   - **Fairness**: Converges to fair share among flows

**Modern Algorithms:**
- **TCP Reno**: Classic AIMD
- **TCP Cubic**: Optimized for high-bandwidth, high-latency networks
- **TCP BBR** (Bottleneck Bandwidth and RTT): Google's modern algorithm, models network

**The Philosophy:**
Congestion control is **network-respectful**. TCP backs off when it senses congestion, preventing collapse and ensuring fairness.

### Ordered Delivery: Sequence Numbers Save the Day

**The Challenge:**
Packets take different routes, arrive out of order.

**The Solution:**
```
Received: Packet 3, Packet 1, Packet 5, Packet 2, Packet 4
TCP: Reorders to 1, 2, 3, 4, 5
Application: Sees data in correct order
```

Sequence numbers allow TCP to:
- **Reorder**: Hold out-of-order packets until gaps fill
- **Detect gaps**: Know when packets are missing
- **Remove duplicates**: Ignore packets we've already seen

### Connection Termination: Graceful Goodbye

**Four-Way Handshake:**
```
Client                              Server
  |                                    |
  |-------FIN ("I'm done sending")---->|
  |                                    |
  |<------ACK ("OK, got it")----------|
  |                                    |
  |<------FIN ("I'm done too")---------|
  |                                    |
  |-------ACK ("Acknowledged")-------->|
  |                                    |
  <Both sides closed>                  
```

**Why Four Steps?**
- Connection is **bidirectional**
- Each side must close independently
- Allows half-close (one side done, other still sending)

**TIME_WAIT State:**
- Client waits 2×MSL (Maximum Segment Lifetime) before full close
- **Why**: Ensure final ACK arrives; handle delayed packets
- **Trade-off**: Sockets remain in use temporarily

### TCP Header: Every Bit Matters

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Data |       |C|E|U|A|P|R|S|F|                               |
| Offset| Rsrvd |W|C|R|C|S|S|Y|I|            Window             |
|       |       |R|E|G|K|H|T|N|N|                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Checksum            |         Urgent Pointer        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Key Fields:**
- **Sequence Number**: Byte stream position
- **ACK Number**: Next expected byte
- **Window**: Available buffer space
- **Flags**: SYN, ACK, FIN, RST, PSH
- **Checksum**: Data integrity

### Performance Characteristics

**Latency Components:**
- **Connection Setup**: 1 RTT (Round Trip Time) for handshake
- **Data Transfer**: 1 RTT per window (with pipelining)
- **Connection Close**: 1 RTT for termination

**Throughput:**
```
Max Throughput = Window Size / RTT
```
- **Window Size**: Limited by receiver buffer and congestion window
- **RTT**: Round trip time
- **Implication**: High RTT = lower throughput (long distance problem)

**Bandwidth-Delay Product:**
```
BDP = Bandwidth × RTT
```
- **Optimal Window Size** = BDP
- **Example**: 100 Mbps, 100ms RTT → Need 1.25 MB window
- **Problem**: Default windows too small for high-speed, long-distance links
- **Solution**: TCP Window Scaling (negotiate larger windows)

### When TCP Shines

**Perfect For:**
- **Web browsing**: Every byte matters, order critical
- **File transfers**: Integrity non-negotiable
- **Email**: Reliability required
- **Database connections**: Transactions need guarantees
- **API calls**: Correctness over speed
- **SSH/Remote access**: Every keystroke must arrive

**The Pattern:**
When **correctness** is more important than **speed**, TCP is your friend.

### When TCP Struggles

**Problems:**

1. **Head-of-Line Blocking**:
   - One lost packet blocks entire stream
   - Application waits for retransmission
   - **Impact**: Poor for real-time (video, gaming)

2. **Overhead**:
   - Connection setup (1 RTT)
   - Headers (20-60 bytes per packet)
   - ACKs (additional packets)
   - **Impact**: Inefficient for small, one-off requests

3. **Latency Sensitivity**:
   - Retransmissions add delay
   - Congestion control slows down proactively
   - **Impact**: Poor for ultra-low latency needs

4. **Fairness Issues**:
   - Aggressive flows get more bandwidth
   - Short flows starved by long flows
   - **Impact**: Unfair resource allocation

### TCP Variants and Evolution

**Classic Versions:**
- **TCP Tahoe** (1988): First congestion control
- **TCP Reno** (1990): Fast retransmit and recovery
- **TCP New Reno**: Better loss handling

**Modern Versions:**
- **TCP Cubic** (Linux default): Better for high-bandwidth networks
- **TCP BBR** (Google, 2016): Model-based congestion control, higher throughput
- **TCP Fast Open**: 0-RTT connection establishment

**Optimizations:**
- **Nagle's Algorithm**: Batch small writes (reduces overhead)
- **Delayed ACK**: Wait before ACKing (reduce ACK traffic)
- **TCP Window Scaling**: Support windows > 64KB
- **Selective Acknowledgment (SACK)**: Acknowledge non-contiguous blocks

### The Trade-offs

| Aspect | TCP | UDP |
|--------|-----|-----|
| **Reliability** | Guaranteed | Best-effort |
| **Order** | Maintained | Not guaranteed |
| **Latency** | Higher (retransmissions) | Lower (no retries) |
| **Overhead** | 20-60 bytes + ACKs | 8 bytes |
| **Connection** | Required (3-way handshake) | Connectionless |
| **Use Case** | Correctness critical | Speed critical |

### The Wisdom

**Why TCP Won the Internet:**
1. **Reliability**: Just works, hides network complexity
2. **Fairness**: Plays nice with other flows
3. **Adaptability**: Adjusts to any network
4. **Simplicity**: Applications don't worry about loss

**The Golden Rule:**
*"Use TCP unless you have a specific reason not to. The reason is usually: real-time, multicast, or you're implementing your own reliability."*

**Modern Reality:**
- **HTTP/1.1, HTTP/2**: Over TCP (reliability matters)
- **HTTP/3**: Over QUIC/UDP (reinvents TCP at application layer)
- **Databases**: Over TCP (data integrity critical)
- **APIs**: Over TCP (correctness over speed)

**The Paradox:**
TCP's reliability mechanisms (retransmissions, ordering) can cause **more latency** than the loss they're compensating for. This is why real-time applications avoid it.

**The Legacy:**
TCP is a testament to brilliant protocol design. It's survived 40+ years because it solves fundamental problems elegantly, adapts to changing networks, and hides complexity from applications. It's not perfect, but it's **remarkably good** at what it does.
