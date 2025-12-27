# Load Balancers



## Youtube

- [Proxy vs Reverse Proxy vs Load Balancer | Simply Explained](https://www.youtube.com/watch?v=xo5V9g9joFs)

- [17. Proxy vs Reverse Proxy (Example) | How Proxy differs from VPN, LoadBalancer | SystemDesign](https://www.youtube.com/watch?v=yeaPUFaXgdA)
- [18. Load Balancer & Different Algorithms - System Design | Static & Dynamic Load Balancing Algorithm](https://www.youtube.com/watch?v=vJYycNWAYZU)



## Theory

### Proxy Server

A proxy server is an intermediary server that sits between clients and other servers, forwarding client requests and server responses. It acts as a gateway or middleman in network communications.

**Key Characteristics:**
- Acts as an intermediary for requests
- Can cache responses to improve performance
- Can filter and modify requests/responses
- Provides anonymity and access control

#### Forward Proxy Server

A forward proxy sits between client devices and the internet, forwarding client requests to external servers.

**How it works:**
1. Client sends request to the forward proxy
2. Forward proxy forwards the request to the destination server (on behalf of the client)
3. Destination server responds to the proxy
4. Proxy returns the response to the client

**Use Cases:**
- **Corporate networks**: Control and monitor employee internet access
- **Content filtering**: Block access to specific websites
- **Anonymity**: Hide client IP addresses from destination servers
- **Caching**: Store frequently accessed content to reduce bandwidth
- **Access control**: Bypass geo-restrictions

**Example Tools:**
- Squid
- Apache HTTP Server (mod_proxy)
- HAProxy (can function as forward proxy)

**Connection to Other Concepts:**
- **Different from Reverse Proxy**: Forward proxy protects clients, reverse proxy protects servers
- **Similar to VPN**: Both provide anonymity, but VPN encrypts all traffic while forward proxy works at application layer
- **Can work with Firewall**: Often deployed together for network security

#### Reverse Proxy Server

A reverse proxy sits in front of backend servers, receiving client requests and forwarding them to appropriate backend servers.

**How it works:**
1. Client sends request to what appears to be the final server (actually the reverse proxy)
2. Reverse proxy forwards request to one of the backend servers
3. Backend server processes and responds to the proxy
4. Proxy returns the response to the client

**Use Cases:**
- **Load distribution**: Distribute traffic across multiple servers
- **SSL termination**: Handle SSL/TLS encryption/decryption
- **Caching**: Cache static content to reduce backend load
- **Security**: Hide backend server details, protect from DDoS
- **Compression**: Compress responses before sending to clients
- **Web acceleration**: Optimize content delivery

**Example Tools:**
- Nginx
- Apache HTTP Server (mod_proxy)
- HAProxy
- Traefik
- Envoy

**Connection to Other Concepts:**
- **Different from Forward Proxy**: Protects servers instead of clients; clients don't need configuration
- **Often functions as Load Balancer**: Many reverse proxies include load balancing features
- **Can be part of CDN**: CDN edge servers act as reverse proxies
- **Works with Firewall**: Provides additional security layer

### Load Balancer

A load balancer distributes incoming network traffic across multiple backend servers to ensure no single server bears too much load, improving application availability and responsiveness.

**How it works:**
1. Client sends request to the load balancer's IP address
2. Load balancer selects a backend server using a specific algorithm
3. Request is forwarded to the selected server
4. Server processes and responds through the load balancer
5. Load balancer returns response to the client

**Types of Load Balancers:**

Load balancers can be categorized based on the OSI layer they operate on and their deployment model.

#### 1. Network Load Balancer (NLB) - Layer 4

**Description:**
- Operates at the Transport Layer (Layer 4) of the OSI model
- Routes traffic based on IP protocol data (IP address and TCP/UDP ports)
- Does NOT inspect application content (HTTP headers, URLs, cookies)
- Extremely fast and can handle millions of requests per second

**How it works:**
1. Receives TCP/UDP packets
2. Examines source/destination IP and port
3. Uses hash or connection tracking to select backend server
4. Forwards packets to selected server (NAT or DSR mode)
5. Maintains minimal state, often just connection table

**Characteristics:**
- **Performance**: Ultra-low latency (microseconds), high throughput
- **Protocol Support**: Any TCP/UDP protocol (HTTP, HTTPS, SMTP, FTP, custom protocols)
- **Static IP**: Provides static IP address (important for DNS)
- **Connection-based**: Preserves client IP address
- **TLS Termination**: Can do TLS passthrough or termination (limited)

**Use Cases:**
- High-performance applications requiring millions of requests/second
- Non-HTTP protocols (databases, gaming servers, IoT)
- Volatile workloads with sudden traffic spikes
- When you need static IP addresses
- WebSocket connections and long-lived TCP connections

**Examples:**
- AWS Network Load Balancer (NLB)
- Azure Load Balancer
- Google Cloud Network Load Balancer
- HAProxy in TCP mode

**Advantages:**
- ✅ Extremely fast and high throughput
- ✅ Lower cost (less processing)
- ✅ Protocol-agnostic (works with any TCP/UDP)
- ✅ Preserves source IP address
- ✅ Lower latency

**Disadvantages:**
- ❌ No content-based routing
- ❌ No URL-based routing or host-based routing
- ❌ Limited SSL/TLS capabilities
- ❌ No HTTP header manipulation
- ❌ Cannot make intelligent decisions based on application data

#### 2. Application Load Balancer (ALB) - Layer 7

**Description:**
- Operates at the Application Layer (Layer 7) of the OSI model
- Understands HTTP/HTTPS protocols and can inspect request content
- Makes routing decisions based on URL paths, hostnames, headers, methods, query strings
- Terminates and re-creates connections (proxy mode)

**How it works:**
1. Receives HTTP/HTTPS request
2. Terminates client connection (SSL offloading if HTTPS)
3. Inspects URL path, headers, cookies, query parameters
4. Routes to appropriate target group based on routing rules
5. Creates new connection to backend server
6. Returns response to client

**Characteristics:**
- **Content-aware**: Routes based on URL, headers, methods
- **SSL Termination**: Handles SSL/TLS encryption/decryption
- **HTTP/2 & WebSocket**: Full support for modern protocols
- **Sticky Sessions**: Cookie-based session affinity
- **Health Checks**: Application-level health checks (HTTP status codes)

**Routing Capabilities:**
- **Path-based**: Route `/api/*` to API servers, `/images/*` to image servers
- **Host-based**: Route `api.example.com` and `www.example.com` to different targets
- **Header-based**: Route based on User-Agent (mobile vs desktop)
- **Query-based**: Route based on query parameters
- **Method-based**: Different routing for GET, POST, PUT, DELETE

**Use Cases:**
- Microservices architectures (route to different services based on path)
- Multi-tenant applications (route by hostname)
- A/B testing (route based on headers/cookies)
- Mobile vs web traffic routing
- API gateways
- Modern web applications with complex routing needs

**Examples:**
- AWS Application Load Balancer (ALB)
- Azure Application Gateway
- Google Cloud HTTP(S) Load Balancer
- HAProxy in HTTP mode
- Nginx

**Advantages:**
- ✅ Advanced routing based on application content
- ✅ SSL/TLS termination (reduces backend load)
- ✅ Better for microservices and containerized apps
- ✅ Cookie-based sticky sessions
- ✅ HTTP/2 and WebSocket support
- ✅ Application-level health checks
- ✅ WAF integration for security

**Disadvantages:**
- ❌ Higher latency than NLB (content inspection overhead)
- ❌ Lower throughput compared to NLB
- ❌ More expensive (more processing required)
- ❌ HTTP/HTTPS only (not for other protocols)
- ❌ Doesn't preserve client IP (uses X-Forwarded-For header)

#### 3. Classic Load Balancer (CLB) - Layer 4 & 7

**Description:**
- Legacy load balancer type (AWS specific, but concept exists elsewhere)
- Can operate at both Layer 4 and Layer 7
- Basic load balancing across EC2 instances
- Being replaced by NLB and ALB in modern architectures

**Characteristics:**
- Simple round-robin or least-connections routing
- Basic health checks
- SSL termination support
- Less features than ALB/NLB

**Use Cases:**
- Legacy applications
- Simple load balancing needs
- When migrating from older infrastructure

**Status:**
- AWS recommends migrating to ALB or NLB
- Not recommended for new deployments

#### 4. Gateway Load Balancer (GWLB)

**Description:**
- Operates at Layer 3 (Network Layer)
- Designed for deploying, scaling, and managing third-party virtual appliances
- Combines transparent network gateway + load balancer

**How it works:**
1. Traffic enters GWLB
2. Distributes traffic to fleet of virtual appliances (firewalls, IDS/IPS)
3. Appliances inspect/process traffic
4. GWLB returns traffic to original flow

**Use Cases:**
- Deploy firewalls, IDS/IPS, DPI tools at scale
- Network security appliances
- Traffic inspection and monitoring

**Examples:**
- AWS Gateway Load Balancer
- Used with Palo Alto, Fortinet, Check Point appliances

#### 5. Global Load Balancer (GSLB)

**Description:**
- DNS-based load balancing across geographic regions
- Routes users to nearest or best-performing data center
- Disaster recovery and multi-region failover

**How it works:**
1. User queries DNS for `www.example.com`
2. GSLB returns IP of nearest/healthiest data center
3. User connects to that data center
4. Local load balancer distributes within data center

**Use Cases:**
- Multi-region deployments
- Global applications
- Disaster recovery
- Geographic traffic steering

**Examples:**
- AWS Route 53 with health checks
- Azure Traffic Manager
- Google Cloud Global Load Balancer
- Cloudflare Load Balancing
- F5 BIG-IP DNS

**Advantages:**
- ✅ Geographic distribution
- ✅ Disaster recovery
- ✅ Reduced latency (route to nearest region)
- ✅ Cross-region failover

**Disadvantages:**
- ❌ DNS caching can delay failover
- ❌ Less granular than application-level LB
- ❌ Depends on DNS TTL

### Comparison: NLB vs ALB

| Feature | Network LB (L4) | Application LB (L7) |
|---------|----------------|---------------------|
| **Layer** | Transport (Layer 4) | Application (Layer 7) |
| **Protocols** | TCP, UDP, TLS | HTTP, HTTPS, HTTP/2, WebSocket |
| **Routing** | IP + Port | URL, headers, cookies, query params |
| **Performance** | Ultra-high (millions RPS) | High (thousands RPS) |
| **Latency** | Microseconds | Milliseconds |
| **SSL Termination** | TLS passthrough | Full SSL offloading |
| **Sticky Sessions** | IP-based | Cookie-based |
| **Health Checks** | TCP/UDP ping | HTTP status codes, response content |
| **Client IP** | Preserved | Via X-Forwarded-For header |
| **Use Cases** | Gaming, IoT, databases | Web apps, microservices, APIs |
| **Cost** | Lower | Higher |

**When to use NLB:**
- Need extreme performance (millions of connections)
- Non-HTTP protocols
- Require static IP
- Minimal latency critical
- Preserve source IP address

**When to use ALB:**
- HTTP/HTTPS applications
- Microservices architecture
- Content-based routing needed
- SSL termination required
- Modern web applications

**Load Balancing Algorithms:**

Load balancing algorithms determine how traffic is distributed across backend servers. They fall into two categories: **Static** (predetermined logic) and **Dynamic** (runtime decisions based on server state).

### Static Load Balancing Algorithms

Static algorithms use predetermined logic without considering current server state or load.

#### 1. Round Robin

**How it works:**
- Distributes requests sequentially across all servers in circular order
- Server 1 → Server 2 → Server 3 → Server 1 → Server 2...
- Maintains a pointer to track the next server

**Example:**
```
Request 1 → Server A
Request 2 → Server B
Request 3 → Server C
Request 4 → Server A
Request 5 → Server B
```

**Best for:**
- Servers with identical specifications
- Requests with similar processing time
- Simple, predictable distribution

**Advantages:**
- ✅ Simple to implement
- ✅ Equal distribution across servers
- ✅ No complex calculations needed
- ✅ Predictable behavior
- ✅ Works well with identical servers

**Disadvantages:**
- ❌ Doesn't consider server capacity differences
- ❌ Ignores current server load
- ❌ Can overload slower servers
- ❌ No consideration for request complexity
- ❌ Poor for heterogeneous server environments
- ❌ Doesn't handle server failures well initially

**Use Case:**
- Homogeneous server cluster with similar request patterns
- Stateless applications
- When simplicity is priority

#### 2. Weighted Round Robin

**How it works:**
- Assigns weight to each server based on capacity
- Higher weight = receives more requests
- Server with weight 3 receives 3x more traffic than server with weight 1

**Example:**
```
Server A: weight = 3
Server B: weight = 2
Server C: weight = 1

Distribution:
Request 1 → Server A
Request 2 → Server A
Request 3 → Server A
Request 4 → Server B
Request 5 → Server B
Request 6 → Server C
(Then repeats)
```

**Best for:**
- Servers with different capacities (CPU, RAM, network)
- Heterogeneous infrastructure
- Gradual server rollouts (new server gets low weight initially)

**Advantages:**
- ✅ Handles servers with different capacities
- ✅ Better utilization of powerful servers
- ✅ Can phase in new servers gradually
- ✅ Simple to configure and understand
- ✅ Predictable distribution based on weights

**Disadvantages:**
- ❌ Requires manual weight configuration
- ❌ Doesn't adapt to runtime conditions
- ❌ Weights may become outdated as server performance changes
- ❌ Doesn't consider current server load
- ❌ Still distributes requests even if server is overloaded

**Use Case:**
- Mixed server environment (e.g., some servers with 16GB RAM, others with 32GB)
- Blue-green deployments (old version weight=1, new version weight=9)
- Canary releases

#### 3. IP Hash (Source IP Hash)

**How it works:**
- Hashes client's IP address to determine which server handles request
- Same client always routed to same server (session persistence)
- Hash function: `hash(client_IP) % number_of_servers`

**Example:**
```
Client IP: 192.168.1.100 → hash() → Server A
Client IP: 192.168.1.101 → hash() → Server C
Client IP: 192.168.1.102 → hash() → Server B

All future requests from 192.168.1.100 go to Server A
```

**Best for:**
- Session persistence without cookies
- Stateful applications
- Applications with server-side caching per user

**Advantages:**
- ✅ Session persistence (no need for sticky sessions configuration)
- ✅ Simple implementation
- ✅ No session store required
- ✅ Good for applications with user-specific server state
- ✅ Deterministic routing

**Disadvantages:**
- ❌ Uneven distribution if client IPs are not uniformly distributed
- ❌ Adding/removing servers changes hash distribution (session loss)
- ❌ Doesn't consider server load
- ❌ Multiple users behind same NAT go to same server
- ❌ No failover for user's designated server
- ❌ Can create hotspots if many users share IP range

**Use Case:**
- Shopping carts stored in server memory
- WebSocket connections requiring persistent connections
- Applications with server-side user sessions

#### 4. URL Hash

**How it works:**
- Hashes the requested URL to determine server
- Same URL always goes to same server
- Enables effective caching per server

**Example:**
```
URL: /images/logo.png → hash() → Server A
URL: /api/users → hash() → Server B
URL: /static/style.css → hash() → Server C

All requests for logo.png go to Server A (cached there)
```

**Best for:**
- Cache optimization
- Content-based distribution
- CDN origin selection

**Advantages:**
- ✅ Maximizes cache hit ratio
- ✅ Same content always on same server
- ✅ Reduces redundant caching across servers
- ✅ Good for content servers

**Disadvantages:**
- ❌ Can create uneven load distribution
- ❌ Popular URLs create hotspots
- ❌ Adding/removing servers disrupts caching
- ❌ Not suitable for dynamic content

**Use Case:**
- Proxy caching servers
- Static content distribution
- CDN origin server selection

### Dynamic Load Balancing Algorithms

Dynamic algorithms make real-time decisions based on current server state and performance metrics.

#### 1. Least Connections

**How it works:**
- Tracks active connections to each server
- Routes new request to server with fewest active connections
- Updates connection count as connections are established/closed

**Example:**
```
Server A: 5 active connections
Server B: 3 active connections  ← New request goes here
Server C: 7 active connections

Next request goes to server with least connections at that moment
```

**Best for:**
- Requests with varying processing times
- Long-lived connections (WebSockets, SSE)
- Heterogeneous request complexity

**Advantages:**
- ✅ Better distribution than round-robin for variable request times
- ✅ Prevents overloading servers with long requests
- ✅ Adapts to server performance automatically
- ✅ Good for applications with mixed quick/slow requests
- ✅ Real-time load awareness

**Disadvantages:**
- ❌ More complex than static algorithms
- ❌ Requires connection tracking overhead
- ❌ Doesn't consider request complexity (1 heavy request = 1 light request)
- ❌ Connection count doesn't always reflect actual load
- ❌ May not work well if all requests are very short

**Use Case:**
- Chat applications (long-lived WebSocket connections)
- Streaming services
- Database connection pooling
- Applications with mixed request durations

#### 2. Weighted Least Connections

**How it works:**
- Combines server weights with connection counts
- Routes to server with lowest ratio of `(current_connections / weight)`
- Accounts for both capacity and current load

**Example:**
```
Server A: 10 connections, weight = 3 → ratio = 10/3 = 3.33
Server B: 5 connections, weight = 2  → ratio = 5/2 = 2.50  ← New request
Server C: 8 connections, weight = 1  → ratio = 8/1 = 8.00
```

**Advantages:**
- ✅ Combines benefits of weighted round-robin and least connections
- ✅ Handles heterogeneous servers with varying loads
- ✅ Better than least connections for different server capacities
- ✅ Adaptive to both static capacity and runtime load

**Disadvantages:**
- ❌ Requires weight configuration
- ❌ More complex tracking
- ❌ Still doesn't measure actual CPU/memory usage

**Use Case:**
- Mixed server environments with variable request durations

#### 3. Least Response Time (Least Latency)

**How it works:**
- Monitors response time from each server
- Routes to server with fastest average response time
- May combine response time with active connections

**Example:**
```
Server A: avg response = 50ms, 5 connections
Server B: avg response = 30ms, 8 connections  ← New request (fastest)
Server C: avg response = 80ms, 3 connections
```

**Best for:**
- Geographically distributed servers
- Servers with varying performance
- Applications where latency is critical

**Advantages:**
- ✅ Routes to fastest/healthiest server
- ✅ Automatically detects server performance issues
- ✅ Excellent user experience (lowest latency)
- ✅ Geographic optimization
- ✅ Adapts to network conditions

**Disadvantages:**
- ❌ Requires continuous response time monitoring
- ❌ Higher overhead (tracking and calculations)
- ❌ Can create positive feedback loop (fast server gets more traffic, becomes slow)
- ❌ Sensitive to temporary spikes
- ❌ May need smoothing algorithms to prevent oscillation

**Use Case:**
- Multi-region deployments
- CDN origin selection
- Real-time applications requiring low latency

#### 4. Resource-Based (Adaptive / Load-Based)

**How it works:**
- Monitors actual server resources: CPU, memory, disk I/O, network
- Routes to server with most available resources
- Requires agent or monitoring system on each server

**Example:**
```
Server A: CPU 80%, Memory 60%, Score = Low
Server B: CPU 40%, Memory 30%, Score = High  ← New request
Server C: CPU 70%, Memory 85%, Score = Low
```

**Best for:**
- Compute-intensive applications
- Servers with varying workload types
- Cloud environments with auto-scaling

**Advantages:**
- ✅ Most accurate representation of server load
- ✅ Prevents resource exhaustion
- ✅ Works well for diverse workload types
- ✅ Can consider multiple metrics (CPU, memory, custom)
- ✅ Best for complex applications

**Disadvantages:**
- ❌ Most complex to implement
- ❌ Requires monitoring agents on servers
- ❌ Higher overhead
- ❌ Latency in metric collection
- ❌ Requires careful tuning of metrics and thresholds

**Use Case:**
- Video encoding servers (CPU-intensive)
- Data processing pipelines
- Machine learning inference servers
- Batch processing systems

#### 5. Least Bandwidth

**How it works:**
- Tracks bandwidth usage per server
- Routes to server consuming least bandwidth (Mbps)
- Good for content delivery

**Advantages:**
- ✅ Optimizes network utilization
- ✅ Good for bandwidth-constrained environments
- ✅ Prevents network saturation

**Disadvantages:**
- ❌ Requires bandwidth monitoring
- ❌ Doesn't reflect server CPU/memory load
- ❌ Less common in modern deployments

**Use Case:**
- Video/media streaming
- Large file downloads
- Bandwidth-limited servers

#### 6. Random

**How it works:**
- Selects server randomly
- Simple probabilistic distribution

**Advantages:**
- ✅ Extremely simple
- ✅ No state tracking
- ✅ Works well with large server pools

**Disadvantages:**
- ❌ No load awareness
- ❌ Uneven distribution possible
- ❌ Not optimal for most use cases

**Use Case:**
- Large, homogeneous server pools
- Stateless microservices with auto-scaling

### Algorithm Selection Guide

| Scenario | Recommended Algorithm | Reason |
|----------|---------------------|--------|
| Identical servers, simple requests | Round Robin | Simple, equal distribution |
| Different server capacities | Weighted Round Robin | Accounts for capacity differences |
| Session persistence needed | IP Hash | Maintains user-server affinity |
| Long-lived connections | Least Connections | Prevents connection buildup |
| Variable request complexity | Least Connections | Adapts to request duration |
| Different servers + variable load | Weighted Least Connections | Best of both worlds |
| Latency-critical applications | Least Response Time | Routes to fastest server |
| CPU/memory-intensive work | Resource-Based | Monitors actual resource usage |
| Multi-region deployment | Least Response Time / GSLB | Geographic optimization |
| Content caching | URL Hash | Maximizes cache hits |

**Layers of Load Balancing:**
- **Layer 4 (Transport)**: Operates at TCP/UDP level, routes based on IP and port
- **Layer 7 (Application)**: Operates at HTTP level, routes based on content, headers, cookies

**Use Cases:**
- Distribute traffic across multiple servers
- Ensure high availability through redundancy
- Enable horizontal scaling
- Perform health checks and remove failed servers
- Implement session persistence (sticky sessions)

**Example Tools:**
- HAProxy
- Nginx
- AWS ELB/ALB/NLB
- Google Cloud Load Balancing
- F5 BIG-IP
- Envoy
- Traefik

**Connection to Other Concepts:**
- **Type of Reverse Proxy**: Load balancer is a specialized reverse proxy focused on distribution
- **Different from Reverse Proxy**: Load balancer specifically focuses on distributing load; reverse proxy has broader capabilities
- **Can be used instead of**: Simple reverse proxy when you need traffic distribution
- **Works with**: CDN (load balancing can happen at CDN edge), Firewall (for security)

### CDN (Content Delivery Network)

A CDN is a geographically distributed network of proxy servers and data centers that deliver content to users based on their geographic location, ensuring faster content delivery and reduced latency.

**How it works:**
1. Origin server stores the original content
2. CDN caches content at multiple edge locations worldwide
3. Client request is routed to nearest edge server
4. Edge server serves cached content (if available) or fetches from origin
5. Content is cached at edge for future requests

**Components:**
- **Origin Server**: The source of truth for content
- **Edge Servers**: Distributed servers that cache content
- **PoP (Point of Presence)**: Physical locations of edge servers

**Use Cases:**
- Deliver static content (images, CSS, JavaScript)
- Stream video/audio content
- Reduce origin server load
- Improve website performance globally
- DDoS protection through distributed architecture
- Handle traffic spikes

**Example Tools/Services:**
- Cloudflare
- AWS CloudFront
- Akamai
- Fastly
- Azure CDN
- Google Cloud CDN

**Connection to Other Concepts:**
- **Uses Reverse Proxy**: Each edge server is a reverse proxy
- **Different from Load Balancer**: CDN focuses on geographic distribution and caching; load balancer focuses on traffic distribution across servers in same location
- **Can replace**: Load balancer for static content delivery
- **Works with**: Load balancer (CDN for static, LB for dynamic content)
- **Includes**: Caching, which reverse proxies can also do

### VPN (Virtual Private Network)

A VPN creates a secure, encrypted tunnel between client and server (or network), ensuring privacy and security of data transmission over public networks.

**How it works:**
1. Client initiates VPN connection to VPN server
2. Encrypted tunnel is established
3. All client traffic is routed through this tunnel
4. VPN server forwards traffic to destination
5. Responses return through the encrypted tunnel

**Types:**
- **Remote Access VPN**: Individual users connect to corporate network
- **Site-to-Site VPN**: Connect entire networks (e.g., office branches)
- **SSL/TLS VPN**: Browser-based VPN access
- **IPSec VPN**: Protocol-level encryption for network traffic

**Use Cases:**
- Secure remote access to corporate resources
- Encrypt internet traffic on public WiFi
- Bypass geo-restrictions and censorship
- Hide IP address and location
- Connect multiple office locations securely

**Example Tools:**
- OpenVPN
- WireGuard
- Cisco AnyConnect
- IPSec
- PPTP/L2TP

**Connection to Other Concepts:**
- **Different from Forward Proxy**: VPN encrypts ALL traffic at network layer; forward proxy works at application layer without encryption
- **Different from Reverse Proxy**: VPN focuses on secure tunneling; reverse proxy on request forwarding
- **Can be used instead of**: Forward proxy when encryption and privacy are critical
- **Similar to**: SSH tunneling (both create encrypted tunnels)
- **Works with**: Firewall (VPN often integrated with firewall policies)

### Firewall

A firewall is a network security system that monitors and controls incoming and outgoing network traffic based on predetermined security rules, acting as a barrier between trusted and untrusted networks.

**How it works:**
1. Traffic attempts to enter or leave the network
2. Firewall examines packets against configured rules
3. Allowed traffic passes through; blocked traffic is denied
4. Logs security events for monitoring

**Types:**
- **Packet Filtering Firewall**: Examines packets in isolation based on IP, port, protocol
- **Stateful Inspection Firewall**: Tracks connection state, examines packet context
- **Application Layer Firewall (WAF)**: Inspects application-level data (HTTP, FTP)
- **Next-Generation Firewall (NGFW)**: Deep packet inspection, IPS, application awareness
- **Proxy Firewall**: Acts as intermediary, no direct connection between networks

**Levels:**
- **Network Firewall**: Protects entire network perimeter
- **Host-based Firewall**: Protects individual devices
- **Cloud Firewall**: Protects cloud infrastructure

**Use Cases:**
- Block unauthorized access
- Filter malicious traffic
- Implement security policies
- Segment network zones
- Prevent data exfiltration
- Comply with security regulations

**Example Tools:**
- iptables/nftables (Linux)
- pfSense
- Cisco ASA
- Palo Alto Networks
- Fortinet FortiGate
- AWS Security Groups
- Azure Firewall

**Connection to Other Concepts:**
- **Can include Proxy**: Proxy firewalls combine both technologies
- **Different from Proxy**: Firewall focuses on security rules; proxy on request forwarding
- **Works with**: Load balancers, reverse proxies (deployed in layers)
- **Can be used with**: VPN (firewall rules control VPN access)
- **Different from WAF**: Traditional firewall works at network layer; WAF at application layer

## Comparison Summary

### Key Differences

| Concept | Primary Purpose | Layer | Direction | Client Awareness |
|---------|----------------|-------|-----------|------------------|
| Forward Proxy | Protect clients, control access | Application (L7) | Client → Internet | Client configured |
| Reverse Proxy | Protect servers, optimize delivery | Application (L7) | Internet → Servers | Transparent to client |
| Load Balancer | Distribute traffic | L4 or L7 | Internet → Servers | Transparent to client |
| CDN | Geographic content delivery | Application (L7) | Internet → Edge Servers | Transparent to client |
| VPN | Secure encrypted tunnel | Network (L3) | Bidirectional | Client configured |
| Firewall | Security filtering | L3-L7 | Bidirectional | Transparent |

### When to Use What

**Use Forward Proxy when:**
- You need to control outbound traffic
- You want to cache external content
- You need to provide anonymity for clients
- You want to filter employee internet access

**Use Reverse Proxy when:**
- You need to hide backend infrastructure
- You want to handle SSL termination
- You need request routing based on content
- You want to cache responses from backend

**Use Load Balancer when:**
- You have multiple servers handling same service
- You need high availability and fault tolerance
- You want to scale horizontally
- You need session persistence

**Use CDN when:**
- You serve content to global audience
- You have large amounts of static content
- You need to reduce origin server load
- You want to improve page load times

**Use VPN when:**
- You need secure remote access
- You want to encrypt all traffic
- You need to connect remote offices
- Privacy and security are top priorities

**Use Firewall when:**
- You need to enforce security policies
- You want to block unauthorized access
- You need to segment your network
- Compliance requires traffic filtering

### Can Be Used As Alternatives

1. **Load Balancer ↔ Reverse Proxy**: For simple traffic distribution, reverse proxy can replace load balancer
2. **Forward Proxy ↔ VPN**: For basic anonymity, but VPN provides encryption
3. **CDN ↔ Reverse Proxy with Caching**: For local deployments, reverse proxy can cache like CDN
4. **Firewall ↔ Proxy**: Application-layer proxy can provide some firewall functionality

### Complementary Use (Used Together)

- **Firewall + Load Balancer**: Firewall filters traffic before load balancer distributes it
- **CDN + Load Balancer**: CDN handles static content, load balancer handles dynamic
- **Reverse Proxy + Firewall**: Layered security and optimization
- **VPN + Firewall**: Secure remote access with access control
- **Load Balancer + Reverse Proxy**: Load balancer distributes, reverse proxy handles SSL/caching

## OSI Layer Analysis

### Application Layer (Layer 7)

Components that operate at the application layer understand and can manipulate the content of requests/responses:

**Forward Proxy:**
- **Layer**: Application Layer (L7)
- **How**: Interprets HTTP/HTTPS requests, understands URLs, headers, cookies
- **Capabilities**: Can modify request headers, block specific URLs, authenticate users, cache based on content
- **Example**: Squid proxy parsing HTTP requests, filtering based on URL patterns

**Reverse Proxy:**
- **Layer**: Application Layer (L7)
- **How**: Inspects HTTP requests, routes based on URL paths, headers, methods
- **Capabilities**: SSL termination, URL rewriting, header manipulation, content-based routing
- **Example**: Nginx routing `/api/*` to API servers and `/static/*` to static file servers

**Layer 7 Load Balancer:**
- **Layer**: Application Layer (L7)
- **How**: Deep packet inspection, understands HTTP/HTTPS, can read request content
- **Capabilities**: Route based on URL, cookies, headers; sticky sessions based on cookies; advanced health checks
- **Example**: AWS ALB routing based on URL path `/users/*` to user service, `/orders/*` to order service

**CDN:**
- **Layer**: Application Layer (L7)
- **How**: Understands HTTP/HTTPS, caches based on content type, headers (Cache-Control, ETag)
- **Capabilities**: Smart caching, content compression, image optimization, HTTP/2 and HTTP/3 support
- **Example**: CloudFlare caching static assets, respecting HTTP cache headers

**Web Application Firewall (WAF):**
- **Layer**: Application Layer (L7)
- **How**: Deep packet inspection, parses HTTP requests/responses, understands SQL, XSS patterns
- **Capabilities**: SQL injection detection, XSS prevention, OWASP Top 10 protection
- **Example**: AWS WAF inspecting POST body for malicious SQL patterns

### Network/Transport Layer (Layer 3/4)

Components that operate at network or transport layer work with IP addresses, ports, and protocols:

**Layer 4 Load Balancer:**
- **Layer**: Transport Layer (L4)
- **How**: Operates on TCP/UDP packets, routes based on IP address and port
- **Capabilities**: Faster than L7 (no content inspection), lower latency, protocol-agnostic
- **Example**: AWS NLB routing TCP connections on port 443 without inspecting HTTPS content

**VPN:**
- **Layer**: Network Layer (L3) - primarily, can also use L4
- **How**: Encapsulates IP packets, creates encrypted tunnels at IP level
- **Types by Layer**:
  - IPSec VPN: Layer 3 (Network)
  - OpenVPN: Can use Layer 3 (tun) or Layer 2 (tap)
  - WireGuard: Layer 3
- **Capabilities**: Encrypts all traffic regardless of protocol, routes entire network segments
- **Example**: IPSec encrypting IP packets, creating site-to-site tunnels

**Traditional Firewall (Packet Filter):**
- **Layer**: Network (L3) and Transport (L4)
- **How**: Inspects IP headers (source/dest IP) and TCP/UDP headers (ports)
- **Capabilities**: Fast filtering based on IP, port, protocol; maintains connection state
- **Example**: iptables blocking incoming traffic on port 22 from specific IP ranges

**Stateful Firewall:**
- **Layer**: Network (L3) and Transport (L4)
- **How**: Tracks TCP connection states (SYN, ACK, FIN), maintains session tables
- **Capabilities**: Understands connection lifecycle, prevents half-open attacks, allows return traffic
- **Example**: pfSense tracking established connections, auto-allowing response packets

### Both Application and Network Layer

**Next-Generation Firewall (NGFW):**
- **Layers**: L3, L4, and L7
- **How**: Multi-layer inspection - packet headers, connection state, AND application content
- **Capabilities**: IPS/IDS, application awareness, user identity, malware detection
- **Example**: Palo Alto firewall identifying and blocking BitTorrent traffic regardless of port

**Advanced Load Balancers:**
- **Layers**: Can operate at both L4 and L7
- **How**: HAProxy, F5 can do simple L4 routing or deep L7 inspection based on configuration
- **Capabilities**: Flexibility to choose performance (L4) vs features (L7)
- **Example**: HAProxy using L4 mode for high-throughput video streaming, L7 for API routing

## Packet-Level Operations

### Components Working at Packet Level

**Packet Filtering Firewall:**
- **Operation**: Examines each packet individually
- **What it sees**: IP header (source IP, dest IP, protocol), TCP/UDP header (ports, flags)
- **Decisions**: Allow/deny based on rules matching packet attributes
- **Limitation**: No context about connection state or application data
- **Example**: Blocking all packets from IP 192.168.1.100 to port 3389 (RDP)

**Stateful Firewall:**
- **Operation**: Examines packets AND tracks connection state
- **What it maintains**: Connection table (5-tuple: src IP, src port, dst IP, dst port, protocol)
- **State Tracking**: NEW, ESTABLISHED, RELATED, INVALID states
- **Advantage**: Allows return traffic automatically, detects anomalies
- **Example**: Allowing outbound HTTPS (NEW), auto-allowing return packets (ESTABLISHED)

**Layer 4 Load Balancer:**
- **Operation**: Examines IP and TCP/UDP headers of packets
- **Packet Modification**: Changes destination IP (from LB IP to backend server IP), maintains source IP or uses NAT
- **Session Tracking**: Ensures all packets from same connection go to same backend server
- **Performance**: Minimal packet inspection = high throughput
- **Example**: AWS NLB forwarding TCP packets based on 5-tuple hash

**VPN (IPSec):**
- **Operation**: Encapsulates and encrypts IP packets
- **Packet Structure**:
  - Original: `[IP Header][TCP Header][Data]`
  - After IPSec: `[New IP Header][IPSec Header][Encrypted: IP Header + TCP Header + Data]`
- **Modes**:
  - **Transport Mode**: Encrypts only payload
  - **Tunnel Mode**: Encrypts entire original packet
- **Example**: Site-to-site VPN encrypting all packets between office networks

**Deep Packet Inspection (DPI):**
- **Who uses it**: NGFW, WAF, IDS/IPS, some ISPs
- **Operation**: Examines packet payload (actual data content), not just headers
- **What it finds**: Malware signatures, protocol violations, encrypted traffic patterns, application types
- **Use cases**: Detecting malware, identifying applications (Skype, BitTorrent), enforcing policies
- **Example**: NGFW detecting SSH tunnel inside HTTPS traffic based on packet patterns

### Components NOT Working at Packet Level

**Application Layer Proxies (L7):**
- **Operation**: Terminates connections, works with complete HTTP requests/responses
- **What it sees**: Full HTTP request with headers, body, cookies - NOT individual packets
- **Difference**: Reassembles TCP stream into HTTP message before processing
- **Example**: Nginx receives complete HTTP request, makes decisions, creates new request to backend

**Layer 7 Load Balancer:**
- **Operation**: Processes complete HTTP requests, not packets
- **Buffer**: Receives and buffers entire request before routing
- **Latency Trade-off**: Slightly higher latency than L4, but enables content-based routing
- **Example**: ALB waits for complete HTTP request to read URL path before routing

## Caching Capabilities

### Where Caching is Achieved

#### 1. Forward Proxy (✅ Caching)

**What is cached:**
- External website content (HTML, CSS, JS, images)
- API responses from external services
- Software packages, updates, downloads

**How it works:**
- Client requests `example.com/image.jpg`
- Proxy checks local cache for this URL
- If cached and fresh: Returns cached copy (cache HIT)
- If not cached or stale: Fetches from origin, stores in cache, returns to client (cache MISS)

**Cache Validation:**
- **TTL (Time To Live)**: Cache for N seconds/minutes
- **HTTP Headers**: Respects `Cache-Control`, `Expires`, `ETag`, `Last-Modified`
- **Revalidation**: Asks origin "Is this still valid?" using `If-None-Match`, `If-Modified-Since`

**Benefits:**
- Reduced bandwidth usage (don't re-download same files)
- Faster response for frequently accessed content
- Reduced load on external servers

**Example:**
```
Squid caching configuration:
- Cache all images for 7 days
- Cache CSS/JS for 24 hours
- Never cache dynamic content (URLs with query params)
```

**Use Case:** Corporate proxy caching Windows updates - download once, serve to 1000 employees

#### 2. Reverse Proxy (✅ Caching)

**What is cached:**
- Static files (images, CSS, JS, fonts)
- API responses (especially GET requests)
- Rendered HTML pages
- Database query results (application-level caching)

**How it works:**
- Client requests `/api/products`
- Reverse proxy checks cache for this endpoint
- If cached: Returns immediately (backend not touched)
- If not cached: Forwards to backend, caches response, returns to client

**Cache Strategies:**
- **Cache Key**: URL, query params, headers (User-Agent, Accept-Language)
- **Cache Invalidation**: Time-based (TTL), event-based (purge on update), LRU (Least Recently Used)
- **Selective Caching**: Only cache GET requests, specific paths, or response codes (200, 301, 404)

**Benefits:**
- Dramatically reduced backend load
- Sub-millisecond response times for cached content
- Better handling of traffic spikes

**Example:**
```nginx
# Nginx caching configuration
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g;
proxy_cache my_cache;
proxy_cache_valid 200 1h;  # Cache successful responses for 1 hour
proxy_cache_valid 404 5m;  # Cache 404s for 5 minutes
```

**Use Case:** E-commerce site caching product images and static product details, reducing database queries by 90%

#### 3. CDN (✅ Caching - Primary Purpose)

**What is cached:**
- Static assets (images, videos, CSS, JavaScript)
- Downloadable files (PDFs, software installers)
- Streaming media chunks
- API responses (at edge locations)

**How it works:**
- User in Tokyo requests `cdn.example.com/logo.png`
- Request goes to nearest CDN edge server (Tokyo PoP)
- Edge server checks local cache
- If cached: Serves immediately (< 10ms latency)
- If not cached: Fetches from origin (or parent cache), stores locally, serves to user
- Subsequent requests from Tokyo users served from edge cache

**Cache Hierarchy:**
- **Edge Servers**: Closest to users, cache most popular content
- **Regional Caches**: Mid-tier, cache less popular content
- **Origin Shield**: Optional layer before origin, reduces origin load

**Advanced Caching:**
- **Geo-specific caching**: Different content for different regions
- **Device-specific caching**: Mobile vs desktop versions
- **Dynamic content caching**: Cache personalized content with cache keys based on cookies/headers

**Benefits:**
- Global performance - low latency worldwide
- Massive bandwidth offload from origin (95%+ cache hit rates possible)
- Handles traffic spikes (viral content)

**Example:**
```
CloudFlare Page Rules:
- Cache Everything for *.jpg, *.png, *.css (1 month TTL)
- Cache API responses for /api/public/* (5 minutes TTL)
- Bypass cache for /api/user/* (personalized data)
```

**Use Case:** Netflix using CDN to cache movie chunks - origin serves each chunk once, CDN serves millions of times

#### 4. Load Balancer (⚠️ Limited Caching)

**Layer 4 Load Balancer:**
- **Caching**: ❌ NO - only forwards packets, doesn't cache
- **Reason**: Works at transport layer, doesn't see application content

**Layer 7 Load Balancer:**
- **Caching**: ⚠️ POSSIBLE but not primary purpose
- **What can be cached**: Similar to reverse proxy (static responses, API responses)
- **Reality**: Most L7 LBs don't cache by default; use dedicated reverse proxy/CDN instead

**Connection Caching (Different):**
- **Persistent Connections**: LB maintains connection pools to backend servers
- **Benefit**: Reduces TCP handshake overhead for backend connections
- **Not content caching**: Caches connections, not data

**Example:**
- HAProxy: Primarily routes, but can be configured with caching using cache plugin
- AWS ALB: No native caching (use CloudFront in front of ALB)
- F5 BIG-IP: Advanced models have content caching feature

**Recommendation:** Use dedicated caching layer (reverse proxy or CDN) instead of relying on LB caching

#### 5. VPN (❌ NO Caching)

**Why no caching:**
- Operates at network layer (L3), doesn't understand application content
- All traffic is encrypted - cannot inspect or cache
- Purpose is secure tunnel, not performance optimization
- Tunnels packets as-is without modification

**Exception:**
- VPN concentrator might cache DNS responses
- But not HTTP content or application data

#### 6. Firewall (❌ NO Caching - Traditional)

**Traditional Firewall:**
- **Caching**: ❌ NO
- **Reason**: Filters packets based on rules, doesn't store content
- **Purpose**: Security, not performance

**Exception - Application Firewall/WAF:**
- **Connection state caching**: Maintains state tables (not content)
- **DNS caching**: Some firewalls cache DNS responses
- **Not content caching**: Doesn't cache HTTP responses or files

**Next-Gen Firewall (NGFW):**
- **Threat signature caching**: Caches malware signatures, URL categories
- **Still not content caching**: For security purposes only

### Caching Comparison Table

| Component | Caches Content? | What is Cached | Cache Location | Primary Purpose |
|-----------|----------------|----------------|----------------|-----------------|
| Forward Proxy | ✅ YES | External content, downloads | Proxy server | Reduce outbound bandwidth |
| Reverse Proxy | ✅ YES | Static files, API responses | Reverse proxy server | Reduce backend load |
| CDN | ✅ YES (Primary) | Static assets, media | Edge servers globally | Global performance |
| L4 Load Balancer | ❌ NO | N/A | N/A | Traffic distribution |
| L7 Load Balancer | ⚠️ Limited | Possible but uncommon | LB server | Traffic distribution |
| VPN | ❌ NO | N/A | N/A | Secure tunnel |
| Firewall | ❌ NO | N/A | N/A | Security filtering |
| WAF | ❌ NO* | *Only threat signatures | WAF server | Security |

### Caching Strategy Recommendations

**For Static Content Globally:**
- **Use CDN** - Purpose-built for this, best performance

**For API Responses (Same Region):**
- **Use Reverse Proxy** - Nginx, Varnish, built-in app cache

**For Corporate Outbound Traffic:**
- **Use Forward Proxy** - Squid, cache downloads and updates

**For Dynamic Content:**
- **Application-level caching** - Redis, Memcached
- **Reverse proxy** for rendered output

**Don't Use for Caching:**
- Load balancers (use CDN/reverse proxy instead)
- VPN (wrong purpose, encrypted traffic)
- Firewalls (security focus, not performance)