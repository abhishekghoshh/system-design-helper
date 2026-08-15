# Networking

## Blogs and websites


## Medium


## Youtube

- [1. Network Protocols (Hindi), High Level Design | Client Server vs P2P Model | webSocket vs WebRTC](https://www.youtube.com/watch?v=JwTiZ9ENquI)
- [Network Protocols (English Dubbed) | Better with 1.25x playback speed](https://www.youtube.com/watch?v=S6KQkIxNm_k)
- [WebSockets vs Polling vs Server Sent Events](https://www.youtube.com/watch?v=WS352jTTkPU)
- [Webhooks for Beginners - From Polling to Real‑Time Events](https://www.youtube.com/watch?v=bXY7899m6M8)

## Theory

### WebSockets vs Polling vs Server-Sent Events

These are three different approaches for real-time client-server communication, each with different characteristics and use cases.

---

### 1. Polling (Short Polling)

#### Description
The client repeatedly sends HTTP requests to the server at regular intervals to check for new data, regardless of whether data is available.

#### How It Works

```
┌─────────┐                                           ┌─────────┐
│ Client  │                                           │ Server  │
└────┬────┘                                           └────┬────┘
     │                                                      │
     │  Request: "Any updates?"                            │
     ├─────────────────────────────────────────────────────>│
     │                                                      │
     │  Response: "No data" (Empty)                        │
     │<─────────────────────────────────────────────────────┤
     │                                                      │
     │  ⏱️ Wait (e.g., 5 seconds)                          │
     │                                                      │
     │  Request: "Any updates?"                            │
     ├─────────────────────────────────────────────────────>│
     │                                                      │
     │  Response: "No data" (Empty)                        │
     │<─────────────────────────────────────────────────────┤
     │                                                      │
     │  ⏱️ Wait (e.g., 5 seconds)                          │
     │                                                      │
     │  Request: "Any updates?"                            │
     ├─────────────────────────────────────────────────────>│
     │                                                      │
     │  Response: "Here's data!" ✅                        │
     │<─────────────────────────────────────────────────────┤
     │                                                      │
     │  ⏱️ Wait (e.g., 5 seconds)                          │
     │                                                      │
     └──────────────────────────────────────────────────────┘
     
     Process repeats indefinitely...
```

#### Python Implementation

**Server (Flask):**
```python
from flask import Flask, jsonify
from datetime import datetime
import random

app = Flask(__name__)

# Simulated data store
messages = []

@app.route('/poll', methods=['GET'])
def poll():
    """Short polling endpoint"""
    # Return any new messages
    if messages:
        data = messages.copy()
        messages.clear()
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'messages': data
        }), 200
    else:
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'messages': []
        }), 200

@app.route('/send', methods=['POST'])
def send_message():
    """Endpoint to add messages"""
    from flask import request
    message = request.json.get('message')
    messages.append(message)
    return jsonify({'status': 'received'}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

**Client:**
```python
import requests
import time

SERVER_URL = "http://localhost:5000"
POLL_INTERVAL = 5  # seconds

def poll_server():
    """Client polling implementation"""
    print("Starting polling client...")
    request_count = 0
    
    while True:
        try:
            request_count += 1
            print(f"\n[Request #{request_count}] Polling server...")
            
            response = requests.get(f"{SERVER_URL}/poll", timeout=10)
            data = response.json()
            
            if data['messages']:
                print(f"✅ Received data: {data['messages']}")
            else:
                print("❌ No new data")
            
            # Wait before next poll
            time.sleep(POLL_INTERVAL)
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            time.sleep(POLL_INTERVAL)

if __name__ == '__main__':
    poll_server()
```

#### Advantages
1. ✅ **Simple to implement** - Uses standard HTTP requests
2. ✅ **Stateless** - No connection state to maintain
3. ✅ **Works everywhere** - Compatible with all browsers and proxies
4. ✅ **Firewall friendly** - Standard HTTP traffic
5. ✅ **Easy to debug** - Can test with curl or browser

#### Disadvantages
1. ❌ **High latency** - Updates delayed by polling interval
2. ❌ **Resource wasteful** - Many empty requests when no data
3. ❌ **Server load** - Continuous requests even without updates
4. ❌ **Network overhead** - Full HTTP headers on every request
5. ❌ **Battery drain** - Constant requests on mobile devices
6. ❌ **Not real-time** - Gap between data availability and delivery

---

### 2. Long Polling

#### Description
The client sends a request to the server, and the server holds the request open until new data is available or a timeout occurs. Once data is sent or timeout happens, the client immediately makes another request.

#### How It Works

```
┌─────────┐                                           ┌─────────┐
│ Client  │                                           │ Server  │
└────┬────┘                                           └────┬────┘
     │                                                      │
     │  Request: "Any updates?" (Connection held open)     │
     ├─────────────────────────────────────────────────────>│
     │                                                      │
     │                    ⏱️ Server waits...               │
     │                    (holding connection)              │
     │                    No data yet...                    │
     │                    Still waiting...                  │
     │                                                      │
     │                    📬 New data arrives!              │
     │  Response: "Here's data!" ✅                        │
     │<─────────────────────────────────────────────────────┤
     │                                                      │
     │  Immediately reconnect                               │
     │  Request: "Any updates?" (Connection held open)     │
     ├─────────────────────────────────────────────────────>│
     │                                                      │
     │                    ⏱️ Server waits...               │
     │                    (holding connection)              │
     │                    No data yet...                    │
     │                                                      │
     │                    ⏰ Timeout (e.g., 30s)            │
     │  Response: "No data" (Timeout)                      │
     │<─────────────────────────────────────────────────────┤
     │                                                      │
     │  Immediately reconnect                               │
     │  Request: "Any updates?"                            │
     ├─────────────────────────────────────────────────────>│
     │                                                      │
     └──────────────────────────────────────────────────────┘
```

#### Python Implementation

**Server (Flask with Threading):**
```python
from flask import Flask, jsonify, request
from datetime import datetime
import time
import threading
from queue import Queue, Empty

app = Flask(__name__)

# Queue for each client
client_queues = {}
queue_lock = threading.Lock()

@app.route('/long-poll', methods=['GET'])
def long_poll():
    """Long polling endpoint"""
    client_id = request.args.get('client_id', 'default')
    timeout = 30  # seconds
    
    # Create queue for this client if doesn't exist
    with queue_lock:
        if client_id not in client_queues:
            client_queues[client_id] = Queue()
    
    queue = client_queues[client_id]
    
    try:
        # Wait for data with timeout
        data = queue.get(timeout=timeout)
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'message': data,
            'status': 'data'
        }), 200
    except Empty:
        # Timeout - no data available
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'message': None,
            'status': 'timeout'
        }), 200

@app.route('/broadcast', methods=['POST'])
def broadcast():
    """Broadcast message to all connected clients"""
    message = request.json.get('message')
    
    with queue_lock:
        for queue in client_queues.values():
            queue.put(message)
    
    return jsonify({
        'status': 'broadcasted',
        'clients': len(client_queues)
    }), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True, threaded=True)
```

**Client:**
```python
import requests
import time
import uuid

SERVER_URL = "http://localhost:5001"
CLIENT_ID = str(uuid.uuid4())

def long_poll_client():
    """Client long polling implementation"""
    print(f"Starting long polling client (ID: {CLIENT_ID})...")
    request_count = 0
    
    while True:
        try:
            request_count += 1
            print(f"\n[Request #{request_count}] Long polling server...")
            
            # Long polling request (will wait on server)
            response = requests.get(
                f"{SERVER_URL}/long-poll",
                params={'client_id': CLIENT_ID},
                timeout=35  # Slightly longer than server timeout
            )
            
            data = response.json()
            
            if data['status'] == 'data':
                print(f"✅ Received data: {data['message']}")
            elif data['status'] == 'timeout':
                print("⏰ Request timed out, reconnecting...")
            
            # Immediately reconnect (no delay)
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            time.sleep(5)  # Wait before retry on error

if __name__ == '__main__':
    long_poll_client()
```

#### Advantages
1. ✅ **Near real-time** - Minimal delay when data arrives
2. ✅ **Reduced requests** - Only reconnects when data received or timeout
3. ✅ **Lower server load** - Fewer requests than short polling
4. ✅ **Works with proxies** - Standard HTTP
5. ✅ **Better than short polling** - More efficient resource usage

#### Disadvantages
1. ❌ **Server resources** - Holds connections open (threads/memory)
2. ❌ **Scalability issues** - Limited concurrent connections per server
3. ❌ **Complex implementation** - Requires threading/async on server
4. ❌ **Timeout management** - Need to handle connection timeouts
5. ❌ **Still HTTP overhead** - Full headers on each request/response
6. ❌ **Not bidirectional** - Only server-to-client push

---

### 3. Server-Sent Events (SSE)

#### Description
A unidirectional channel from server to client over a single HTTP connection. The server can push data to the client whenever new data is available. Client only listens.

#### How It Works

```
┌─────────┐                                           ┌─────────┐
│ Client  │                                           │ Server  │
└────┬────┘                                           └────┬────┘
     │                                                      │
     │  Initial Request: "Open SSE connection"             │
     ├─────────────────────────────────────────────────────>│
     │                                                      │
     │  Response: HTTP 200 OK                              │
     │  Content-Type: text/event-stream                    │
     │  Connection: keep-alive                             │
     │<─────────────────────────────────────────────────────┤
     │                                                      │
     │════════════════════════════════════════════════════│
     │         🔌 Connection Stays Open                    │
     │════════════════════════════════════════════════════│
     │                                                      │
     │                    📬 Event 1 arrives                │
     │  ⬅️ data: {"message": "Hello"}                     │
     │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┤
     │                                                      │
     │  Client processes event                              │
     │                                                      │
     │                    📬 Event 2 arrives                │
     │  ⬅️ data: {"message": "World"}                     │
     │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┤
     │                                                      │
     │  Client processes event                              │
     │                                                      │
     │                    📬 Event 3 arrives                │
     │  ⬅️ data: {"message": "Goodbye"}                   │
     │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┤
     │                                                      │
     │════════════════════════════════════════════════════│
     │     Connection remains open for more events         │
     │════════════════════════════════════════════════════│
     │                                                      │
     └──────────────────────────────────────────────────────┘
```

#### SSE Event Format

```
event: message
id: 1
retry: 10000
data: {"user": "John", "text": "Hello!"}

event: notification
id: 2
data: {"type": "alert", "message": "New update"}

event: heartbeat
data: ping

```

#### Python Implementation

**Server (Flask with streaming):**
```python
from flask import Flask, Response, request
import json
import time
import threading
from datetime import datetime

app = Flask(__name__)

# Store active connections
active_connections = []
connection_lock = threading.Lock()

def event_stream():
    """Generator function for SSE"""
    # Create a queue for this client
    from queue import Queue
    message_queue = Queue()
    
    # Register this connection
    with connection_lock:
        active_connections.append(message_queue)
    
    try:
        # Send initial connection event
        yield f"event: connected\ndata: {json.dumps({'timestamp': datetime.now().isoformat()})}\n\n"
        
        # Send heartbeat and messages
        while True:
            try:
                # Non-blocking get with timeout
                message = message_queue.get(timeout=15)
                
                # Format SSE event
                event_data = f"event: message\n"
                event_data += f"id: {int(time.time())}\n"
                event_data += f"data: {json.dumps(message)}\n\n"
                
                yield event_data
                
            except:
                # Send heartbeat on timeout
                yield f"event: heartbeat\ndata: {json.dumps({'time': datetime.now().isoformat()})}\n\n"
    
    finally:
        # Cleanup on disconnect
        with connection_lock:
            if message_queue in active_connections:
                active_connections.remove(message_queue)

@app.route('/stream')
def stream():
    """SSE endpoint"""
    return Response(
        event_stream(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',  # Disable nginx buffering
            'Connection': 'keep-alive'
        }
    )

@app.route('/broadcast', methods=['POST'])
def broadcast():
    """Broadcast message to all connected clients"""
    message = request.json
    
    with connection_lock:
        for queue in active_connections:
            queue.put(message)
    
    return json.dumps({
        'status': 'sent',
        'clients': len(active_connections)
    }), 200

if __name__ == '__main__':
    app.run(port=5002, debug=True, threaded=True)
```

**Client (Python):**
```python
import requests
import json

SERVER_URL = "http://localhost:5002"

def sse_client():
    """SSE client implementation"""
    print("Connecting to SSE stream...")
    
    response = requests.get(
        f"{SERVER_URL}/stream",
        stream=True,
        headers={'Accept': 'text/event-stream'}
    )
    
    if response.status_code == 200:
        print("✅ Connected to SSE stream")
        
        # Read stream line by line
        event_type = None
        event_id = None
        data_buffer = []
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                
                if line.startswith('event:'):
                    event_type = line.split(':', 1)[1].strip()
                elif line.startswith('id:'):
                    event_id = line.split(':', 1)[1].strip()
                elif line.startswith('data:'):
                    data = line.split(':', 1)[1].strip()
                    data_buffer.append(data)
                elif line.startswith('retry:'):
                    retry = line.split(':', 1)[1].strip()
            else:
                # Empty line signals end of event
                if data_buffer:
                    full_data = '\n'.join(data_buffer)
                    
                    try:
                        parsed_data = json.loads(full_data)
                        print(f"\n📬 Event: {event_type or 'message'}")
                        print(f"   Data: {parsed_data}")
                    except:
                        print(f"\n📬 Event: {event_type or 'message'}")
                        print(f"   Data: {full_data}")
                    
                    # Reset
                    event_type = None
                    event_id = None
                    data_buffer = []
    else:
        print(f"❌ Failed to connect: {response.status_code}")

if __name__ == '__main__':
    sse_client()
```

**Client (JavaScript - Browser):**
```javascript
// Browser implementation using EventSource API
const eventSource = new EventSource('http://localhost:5002/stream');

// Listen for specific event types
eventSource.addEventListener('connected', (event) => {
    console.log('✅ Connected:', JSON.parse(event.data));
});

eventSource.addEventListener('message', (event) => {
    console.log('📬 Message:', JSON.parse(event.data));
});

eventSource.addEventListener('heartbeat', (event) => {
    console.log('💓 Heartbeat:', JSON.parse(event.data));
});

// Handle errors
eventSource.onerror = (error) => {
    console.error('❌ SSE Error:', error);
    if (eventSource.readyState === EventSource.CLOSED) {
        console.log('Connection closed');
    }
};

// Close connection when done
// eventSource.close();
```

#### Advantages
1. ✅ **Real-time** - Instant server-to-client push
2. ✅ **Efficient** - Single long-lived connection
3. ✅ **Auto-reconnection** - Browser handles reconnection automatically
4. ✅ **Event IDs** - Can resume from last received event
5. ✅ **Simple protocol** - Text-based, easy to debug
6. ✅ **Native browser support** - EventSource API built-in
7. ✅ **Less overhead** - No repeated HTTP headers

#### Disadvantages
1. ❌ **Unidirectional** - Only server → client (client uses HTTP for server)
2. ❌ **HTTP/1.1 limitation** - Max 6 connections per domain in browsers
3. ❌ **Text only** - Binary data needs encoding (Base64)
4. ❌ **No IE support** - Internet Explorer doesn't support EventSource
5. ❌ **Proxy issues** - Some proxies may buffer events

---

### 4. WebSockets

#### Description
Full-duplex bidirectional communication channel over a single TCP connection. Both client and server can send messages to each other at any time after the initial handshake.

#### How It Works

```
┌─────────┐                                           ┌─────────┐
│ Client  │                                           │ Server  │
└────┬────┘                                           └────┬────┘
     │                                                      │
     │  HTTP Request (Upgrade: websocket)                  │
     ├─────────────────────────────────────────────────────>│
     │  GET /ws HTTP/1.1                                   │
     │  Connection: Upgrade                                 │
     │  Upgrade: websocket                                  │
     │  Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==        │
     │                                                      │
     │  HTTP Response (101 Switching Protocols)            │
     │<─────────────────────────────────────────────────────┤
     │  HTTP/1.1 101 Switching Protocols                   │
     │  Upgrade: websocket                                  │
     │  Connection: Upgrade                                 │
     │  Sec-WebSocket-Accept: HSmrc0sMlYUkAGmm5OPpG2HaGWk= │
     │                                                      │
     │════════════════════════════════════════════════════│
     │         🔌 WebSocket Connection Established         │
     │              (Full-Duplex Channel)                   │
     │════════════════════════════════════════════════════│
     │                                                      │
     │  ➡️  Message: "Hello Server"                       │
     ├─────────────────────────────────────────────────────>│
     │                                                      │
     │  ⬅️  Message: "Hello Client"                       │
     │<─────────────────────────────────────────────────────┤
     │                                                      │
     │  ⬅️  Message: "Notification"                       │
     │<─────────────────────────────────────────────────────┤
     │                                                      │
     │  ➡️  Message: "Acknowledgment"                     │
     ├─────────────────────────────────────────────────────>│
     │                                                      │
     │  ➡️  Message: "User typing..."                     │
     ├─────────────────────────────────────────────────────>│
     │                                                      │
     │  ⬅️  Message: "Broadcast: User X typing"          │
     │<─────────────────────────────────────────────────────┤
     │                                                      │
     │════════════════════════════════════════════════════│
     │     Both can send/receive simultaneously            │
     │════════════════════════════════════════════════════│
     │                                                      │
     │  Close Frame                                         │
     ├─────────────────────────────────────────────────────>│
     │                                                      │
     │  Close Frame                                         │
     │<─────────────────────────────────────────────────────┤
     │                                                      │
     └──────────────────────────────────────────────────────┘
```

#### WebSocket Frame Structure

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
|N|V|V|V|       |S|             |   (if payload len==126/127)   |
| |1|2|3|       |K|             |                               |
+-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
|     Extended payload length continued, if payload len == 127  |
+ - - - - - - - - - - - - - - - +-------------------------------+
|                               |Masking-key, if MASK set to 1  |
+-------------------------------+-------------------------------+
| Masking-key (continued)       |          Payload Data         |
+-------------------------------- - - - - - - - - - - - - - - - +
:                     Payload Data continued ...                :
+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
|                     Payload Data continued ...                |
+---------------------------------------------------------------+

FIN: 1 bit - Is this the final fragment?
RSV1-3: 3 bits - Reserved for extensions
Opcode: 4 bits - 0x0=continuation, 0x1=text, 0x2=binary, 0x8=close, 0x9=ping, 0xA=pong
MASK: 1 bit - Is payload masked? (client→server must be masked)
Payload length: 7 bits, 7+16 bits, or 7+64 bits
```

#### Python Implementation

**Server (using `websockets` library):**
```python
import asyncio
import websockets
import json
from datetime import datetime

# Store connected clients
connected_clients = set()

async def handler(websocket, path):
    """Handle WebSocket connections"""
    print(f"✅ Client connected: {websocket.remote_address}")
    connected_clients.add(websocket)
    
    try:
        # Send welcome message
        await websocket.send(json.dumps({
            'type': 'welcome',
            'message': 'Connected to WebSocket server',
            'timestamp': datetime.now().isoformat()
        }))
        
        # Listen for messages
        async for message in websocket:
            print(f"📬 Received: {message}")
            
            try:
                data = json.loads(message)
                
                # Echo back to sender
                response = {
                    'type': 'echo',
                    'original': data,
                    'timestamp': datetime.now().isoformat()
                }
                await websocket.send(json.dumps(response))
                
                # Broadcast to all other clients
                if data.get('broadcast'):
                    broadcast_msg = {
                        'type': 'broadcast',
                        'message': data.get('message'),
                        'from': str(websocket.remote_address),
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    # Send to all except sender
                    for client in connected_clients:
                        if client != websocket:
                            await client.send(json.dumps(broadcast_msg))
            
            except json.JSONDecodeError:
                # Handle non-JSON messages
                await websocket.send(f"Received text: {message}")
    
    except websockets.exceptions.ConnectionClosed:
        print(f"❌ Client disconnected: {websocket.remote_address}")
    
    finally:
        connected_clients.remove(websocket)

async def main():
    """Start WebSocket server"""
    async with websockets.serve(handler, "localhost", 8765):
        print("🚀 WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
```

**Client (Python):**
```python
import asyncio
import websockets
import json

async def client():
    """WebSocket client"""
    uri = "ws://localhost:8765"
    
    async with websockets.connect(uri) as websocket:
        print(f"✅ Connected to {uri}")
        
        # Receive welcome message
        welcome = await websocket.recv()
        print(f"📬 Server: {welcome}")
        
        # Send messages
        messages = [
            {'message': 'Hello Server', 'broadcast': False},
            {'message': 'This is a test', 'broadcast': True},
            {'message': 'Broadcasting to all', 'broadcast': True}
        ]
        
        for msg in messages:
            print(f"\n➡️  Sending: {msg}")
            await websocket.send(json.dumps(msg))
            
            # Wait for response
            response = await websocket.recv()
            print(f"⬅️  Response: {response}")
            
            await asyncio.sleep(1)
        
        print("\n👋 Closing connection")

if __name__ == "__main__":
    asyncio.run(client())
```

**Client (JavaScript - Browser):**
```javascript
// Browser WebSocket implementation
const ws = new WebSocket('ws://localhost:8765');

// Connection opened
ws.addEventListener('open', (event) => {
    console.log('✅ Connected to WebSocket server');
    
    // Send a message
    ws.send(JSON.stringify({
        message: 'Hello from browser!',
        broadcast: true
    }));
});

// Listen for messages
ws.addEventListener('message', (event) => {
    console.log('📬 Message from server:', event.data);
    
    try {
        const data = JSON.parse(event.data);
        console.log('Parsed:', data);
    } catch (e) {
        console.log('Text message:', event.data);
    }
});

// Connection closed
ws.addEventListener('close', (event) => {
    console.log('❌ Disconnected from server');
    console.log('Code:', event.code, 'Reason:', event.reason);
});

// Error occurred
ws.addEventListener('error', (error) => {
    console.error('WebSocket error:', error);
});

// Send message function
function sendMessage(message) {
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(message));
    } else {
        console.error('WebSocket is not open');
    }
}

// Close connection
function closeConnection() {
    ws.close(1000, 'Client closing connection');
}
```

#### Advantages
1. ✅ **Full-duplex** - Bidirectional communication
2. ✅ **Real-time** - Extremely low latency
3. ✅ **Efficient** - Minimal overhead after handshake
4. ✅ **Binary support** - Can send binary data directly
5. ✅ **Single connection** - Reduces server load
6. ✅ **Native browser support** - WebSocket API built-in
7. ✅ **Push from both sides** - Both client and server can initiate

#### Disadvantages
1. ❌ **Stateful** - Connection state must be maintained
2. ❌ **Complex scaling** - Sticky sessions or message broker needed
3. ❌ **Proxy issues** - Some corporate proxies block WebSockets
4. ❌ **Load balancing complexity** - Need WebSocket-aware load balancers
5. ❌ **No automatic reconnection** - Must implement manually
6. ❌ **Firewall issues** - May be blocked in restrictive networks

---

### Comparison Table

| Feature | Polling | Long Polling | Server-Sent Events | WebSockets |
|---------|---------|--------------|-------------------|------------|
| **Direction** | Client → Server | Client → Server | Server → Client | Bidirectional |
| **Connection** | New per request | New per request | Single long-lived | Single long-lived |
| **Latency** | High (interval) | Low | Very Low | Very Low |
| **Server Load** | Very High | Medium | Low | Very Low |
| **Complexity** | Very Simple | Medium | Medium | High |
| **Real-time** | ❌ No | ✅ Near | ✅ Yes | ✅ Yes |
| **Binary Data** | ✅ Yes (encoded) | ✅ Yes (encoded) | ❌ No (Base64) | ✅ Yes (native) |
| **Browser Support** | ✅ Universal | ✅ Universal | ⚠️ No IE | ✅ Modern browsers |
| **Scalability** | Poor | Medium | Good | Excellent |
| **Firewall Friendly** | ✅ Yes | ✅ Yes | ✅ Yes | ⚠️ Sometimes blocked |
| **Auto Reconnect** | N/A | N/A | ✅ Yes | ❌ No (manual) |
| **HTTP Compatible** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ Upgrades to WS |
| **Message Ordering** | Not guaranteed | Not guaranteed | ✅ Guaranteed | ✅ Guaranteed |

---

### Bandwidth & Overhead Comparison

#### Example: Sending 100 bytes of data

**Short Polling (every 5 seconds):**
```
Request Headers:  ~800 bytes
Response Headers: ~500 bytes
Data:             100 bytes
Total per poll:   ~1,400 bytes

Polls per minute: 12
Total per minute: ~16,800 bytes (16.4 KB)
Efficiency:       ~0.7% (100/1400)
```

**Long Polling:**
```
Request Headers:  ~800 bytes
Response Headers: ~500 bytes
Data:             100 bytes
Total per message: ~1,400 bytes

Messages per minute: Variable (only when data available)
If 5 messages/min:   ~7,000 bytes (6.8 KB)
Efficiency:          ~0.7% (100/1400)
```

**Server-Sent Events:**
```
Initial Request:  ~800 bytes
Initial Response: ~500 bytes
Per Event:        ~50 bytes (event overhead) + 100 bytes = 150 bytes

Initial:          ~1,300 bytes
5 events:         ~750 bytes
Total:            ~2,050 bytes (2 KB)
Efficiency:       ~24% (500/2050)
```

**WebSockets:**
```
Initial Handshake: ~1,300 bytes (one-time)
Per Message:       ~6 bytes (frame overhead) + 100 bytes = 106 bytes

Handshake:        ~1,300 bytes
5 messages:       ~530 bytes
Total:            ~1,830 bytes (1.8 KB)
Efficiency:       ~27% (500/1830)
```

---

### Use Cases

#### Short Polling
- **Dashboard updates** (not critical, every 30-60 seconds)
- **Email checking** (every few minutes)
- **Weather updates** (periodic data)
- **Simple status checks**
- **Legacy system compatibility**

**Example:** Email client checking for new mail every 5 minutes

#### Long Polling
- **Chat applications** (before WebSockets)
- **Notifications** (when SSE not supported)
- **Order status updates**
- **Job progress monitoring**
- **Fallback for SSE/WebSockets**

**Example:** Facebook notifications (used long polling before switching to other methods)

#### Server-Sent Events
- **Live news feeds**
- **Stock price tickers**
- **Social media feeds**
- **Real-time notifications**
- **Server-side event broadcasts**
- **Live sports scores**
- **Monitoring dashboards**

**Example:** Twitter live feed, stock market tickers

#### WebSockets
- **Chat applications** (Slack, Discord)
- **Real-time gaming** (multiplayer games)
- **Collaborative editing** (Google Docs)
- **Live streaming** (Twitch chat)
- **Trading platforms**
- **IoT device communication**
- **Video conferencing** (signaling)

**Example:** WhatsApp Web, Discord chat, online multiplayer games

---

### Decision Matrix

```
                    Short Polling  Long Polling    SSE      WebSockets
                    ═══════════════════════════════════════════════════
Unidirectional         ✅            ✅            ✅          ✅
Bidirectional          ❌            ❌            ❌          ✅
Simple implementation  ✅            ⚠️            ✅          ❌
Low latency           ❌            ⚠️            ✅          ✅
Low server load       ❌            ⚠️            ✅          ✅
Mobile friendly       ❌            ⚠️            ✅          ✅
Firewall friendly     ✅            ✅            ✅          ⚠️
Binary data           ⚠️            ⚠️            ❌          ✅
Scales well           ❌            ⚠️            ✅          ✅
```

---

### When to Use What?

#### Use Short Polling When:
- Updates are infrequent (> 30 seconds)
- Real-time not critical
- Simplest implementation needed
- Working with very old systems

#### Use Long Polling When:
- Need better than short polling
- SSE/WebSockets not available
- Moderate real-time requirements
- Need to support all browsers/proxies

#### Use Server-Sent Events When:
- Only server → client push needed
- Client doesn't need to send much data
- Need automatic reconnection
- Broadcasting events to many clients
- Modern browser environment

#### Use WebSockets When:
- Need bidirectional communication
- Real-time is critical (< 100ms latency)
- High message frequency
- Binary data transfer needed
- Building chat, gaming, or collaborative apps

---

### Evolution Timeline

```
2000s: Short Polling
  └─> Simple HTTP requests
  └─> High overhead, poor for real-time

2006: Comet / Long Polling
  └─> Improved latency
  └─> Still HTTP overhead

2009: Server-Sent Events (HTML5)
  └─> EventSource API
  └─> One-way server push

2011: WebSockets (RFC 6455)
  └─> Full-duplex communication
  └─> Minimal overhead
  └─> Industry standard for real-time

Future: HTTP/3 + QUIC
  └─> Improved performance
  └─> Better mobile support
  └─> Reduced latency
```

---

### Performance Comparison (Real-World Scenario)

**Scenario:** 1000 users, 1 message per second per user

| Method | Connections | Requests/sec | Bandwidth/sec | Server CPU | Server RAM |
|--------|-------------|--------------|---------------|------------|------------|
| Short Polling (5s) | 0 | 200 (1000÷5) | ~280 KB | High | Low |
| Long Polling | 1000 | 1000 | ~1.4 MB | Very High | High |
| SSE | 1000 | 1000 initial | ~146 KB | Medium | Medium |
| WebSockets | 1000 | 1000 initial | ~103 KB | Low | Medium |

**Winner:** WebSockets for efficiency, SSE for simplicity with one-way communication

---

### Best Practices

#### For Polling:
```python
# Use exponential backoff on errors
def poll_with_backoff():
    delay = 1
    max_delay = 60
    
    while True:
        try:
            response = requests.get(url)
            delay = 1  # Reset on success
            process(response)
        except:
            time.sleep(delay)
            delay = min(delay * 2, max_delay)  # Exponential backoff
```

#### For SSE:
```python
# Include heartbeats to detect dead connections
def sse_with_heartbeat():
    while True:
        if has_data():
            yield f"data: {get_data()}\n\n"
        else:
            yield ":heartbeat\n\n"  # Comment (ignored by client)
        time.sleep(15)
```

#### For WebSockets:
```javascript
// Implement reconnection logic
class WebSocketClient {
    connect() {
        this.ws = new WebSocket(this.url);
        
        this.ws.onclose = () => {
            console.log('Disconnected, reconnecting in 3s...');
            setTimeout(() => this.connect(), 3000);
        };
    }
}
```

---

### Summary

1. **Short Polling**: Simplest but wasteful - use only for very infrequent updates
2. **Long Polling**: Better than short polling - good fallback when SSE/WS unavailable
3. **Server-Sent Events**: Efficient one-way push - perfect for feeds, notifications, dashboards
4. **WebSockets**: Most powerful - ideal for chat, gaming, collaborative apps with bidirectional needs

**Modern Recommendation:**
- **Primary:** WebSockets for bidirectional, SSE for unidirectional
- **Fallback:** Long polling for old browser/proxy support
- **Avoid:** Short polling unless absolutely necessary
