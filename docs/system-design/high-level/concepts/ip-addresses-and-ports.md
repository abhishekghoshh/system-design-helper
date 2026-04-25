# IP Addresses & Ports

## Blogs and websites


## Medium


## Youtube


## Theory

### IP Addresses: The Internet's Postal System

**IP Address**: Unique identifier for devices on a network - like a street address for computers.

#### IPv4 Architecture

**Format**: 32-bit address (4 bytes), written as dotted decimal
```
192.168.1.100
 ↓   ↓   ↓  ↓
 1   2   3  4  (octets)

Binary representation:
11000000.10101000.00000001.01100100
```

**Address Classes:**
```
Class A: 0.0.0.0      to 127.255.255.255   (16M hosts/network)
         [Network].[Host].[Host].[Host]
         Example: 10.1.2.3

Class B: 128.0.0.0    to 191.255.255.255   (65K hosts/network)
         [Network].[Network].[Host].[Host]
         Example: 172.16.1.100

Class C: 192.0.0.0    to 223.255.255.255   (254 hosts/network)
         [Network].[Network].[Network].[Host]
         Example: 192.168.1.50
```

**Private vs Public IP Addresses:**

```
Private IP Ranges (RFC 1918):
┌─────────────────────────────────────────────────┐
│ 10.0.0.0      - 10.255.255.255   (Class A)     │
│ 172.16.0.0    - 172.31.255.255   (Class B)     │
│ 192.168.0.0   - 192.168.255.255  (Class C)     │
└─────────────────────────────────────────────────┘
     ↓ Not routable on public Internet
     ↓ Used inside organizations
     ↓ NAT translates to public IP

Public IP:
     ↓ Globally unique
     ↓ Routable on Internet
     ↓ Assigned by ISP/cloud provider
```

**Real-World Example:**
```
Your Home Network:
┌──────────────────────────────────────────┐
│ Public IP: 203.0.113.45 (ISP-assigned)  │
│                                          │
│  Router (NAT)                           │
│    └─ Private Network: 192.168.1.0/24   │
│         ├─ Laptop:  192.168.1.10       │
│         ├─ Phone:   192.168.1.11       │
│         └─ Tablet:  192.168.1.12       │
└──────────────────────────────────────────┘

Outbound connection:
Laptop (192.168.1.10:5000) 
  → NAT translates to →
Public (203.0.113.45:5000)
  → Internet
```

#### IPv6: The Future (and Present)

**Format**: 128-bit address (16 bytes), written in hexadecimal
```
2001:0db8:85a3:0000:0000:8a2e:0370:7334
  ↓ Simplified (remove leading zeros):
2001:db8:85a3:0:0:8a2e:370:7334
  ↓ Further simplified (:: for consecutive zeros):
2001:db8:85a3::8a2e:370:7334
```

**Why IPv6?**
```
IPv4 addresses: 4.3 billion (2^32)
  ↓ Exhausted in 2011
  ↓ NAT is a workaround, not a solution

IPv6 addresses: 340 undecillion (2^128)
  ↓ 340,282,366,920,938,463,463,374,607,431,768,211,456
  ↓ Enough for every grain of sand on Earth
```

**IPv6 Example:**
```
Global Unicast Address:
2001:db8:85a3:1234:5678:8a2e:370:7334
│    │   │    │    │    │    │   └── Interface ID
│    │   │    └────┴────┴────┴────── Subnet/Host
└────┴───┴────────────────────────── Network Prefix
```

### Ports: Doorways to Applications

**Concept**: IP gets you to the building (server), port gets you to the right apartment (application).

```
Server: 192.168.1.100
┌──────────────────────────┐
│ Port 80:  Web Server     │ ← http://192.168.1.100:80
│ Port 443: HTTPS          │ ← https://192.168.1.100:443
│ Port 22:  SSH            │ ← ssh user@192.168.1.100
│ Port 3306: MySQL         │ ← mysql://192.168.1.100:3306
│ Port 5432: PostgreSQL    │ ← postgres://192.168.1.100:5432
│ Port 6379: Redis         │ ← redis://192.168.1.100:6379
└──────────────────────────┘
```

#### Port Ranges and Their Purposes

**Well-Known Ports (0-1023):** System/privileged services
```
20/21   FTP (File Transfer)
22      SSH (Secure Shell)
23      Telnet (insecure, avoid)
25      SMTP (Email sending)
53      DNS (Domain Name System)
80      HTTP (Web)
110     POP3 (Email retrieval)
143     IMAP (Email access)
443     HTTPS (Secure web)
3306    MySQL
5432    PostgreSQL
6379    Redis
27017   MongoDB
```

**Registered Ports (1024-49151):** User applications
```
3000    Node.js development
5000    Flask default
8000    Django development
8080    Alternative HTTP
8443    Alternative HTTPS
9200    Elasticsearch
```

**Dynamic/Private Ports (49152-65535):** Temporary client connections
```
Client connects:
192.168.1.10:54231 → 93.184.216.34:443
     ↑                        ↑
  Random port            HTTPS port
  (ephemeral)            (well-known)
```

#### Real-World Use Cases

**Use Case 1: Web Server**
```
Setup:
┌─────────────────────────────────┐
│ Server: example.com (1.2.3.4)  │
│   Port 80:  HTTP (redirect)    │
│   Port 443: HTTPS (main site)  │
└─────────────────────────────────┘

User types: http://example.com
  ↓ Browser resolves DNS
Connects to: 1.2.3.4:80
  ↓ Server responds
301 Redirect to https://example.com
  ↓ Browser reconnects
Connects to: 1.2.3.4:443
  ↓ Secure connection established
Serves website
```

**Use Case 2: Microservices Architecture**
```
Server: 10.0.1.50
┌──────────────────────────────────┐
│ 3000: Auth Service               │ ← JWT validation
│ 3001: User Service               │ ← User CRUD
│ 3002: Product Service            │ ← Catalog
│ 3003: Order Service              │ ← Orders
│ 6379: Redis (shared cache)       │ ← Session store
│ 5432: PostgreSQL (shared DB)     │ ← Data persistence
└──────────────────────────────────┘

API Gateway: 10.0.1.10:80
  Routes:
    /auth/*     → 10.0.1.50:3000
    /users/*    → 10.0.1.50:3001
    /products/* → 10.0.1.50:3002
    /orders/*   → 10.0.1.50:3003
```

**Use Case 3: Database Cluster**
```
PostgreSQL Cluster:
┌─────────────────────────────────────┐
│ Primary:   10.0.2.10:5432 (writes) │
│ Replica 1: 10.0.2.11:5432 (reads)  │
│ Replica 2: 10.0.2.12:5432 (reads)  │
└─────────────────────────────────────┘

Application config:
write_db = "postgresql://10.0.2.10:5432/mydb"
read_db = [
    "postgresql://10.0.2.11:5432/mydb",
    "postgresql://10.0.2.12:5432/mydb"
]
```

#### Code Example: Socket Programming

**Python Server (Listens on IP:Port):**
```python
import socket

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to IP and Port
host = '0.0.0.0'  # Listen on all network interfaces
port = 8080
server_socket.bind((host, port))

# Listen for connections
server_socket.listen(5)
print(f"Server listening on {host}:{port}")

while True:
    # Accept client connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address[0]}:{client_address[1]}")
    
    # Send response
    client_socket.send(b"HTTP/1.1 200 OK\r\n\r\nHello, World!")
    client_socket.close()
```

**Python Client (Connects to IP:Port):**
```python
import socket

# Create TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
server_ip = '192.168.1.100'
server_port = 8080
client_socket.connect((server_ip, server_port))

# Send request
client_socket.send(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")

# Receive response
response = client_socket.recv(4096)
print(response.decode())

client_socket.close()
```

#### Network Address Translation (NAT)

**The Problem:**
Private IPs can't communicate with public internet directly.

**The Solution: NAT**
```
Internal Network                    NAT Router                 Internet
┌─────────────────┐              ┌────────────┐           ┌──────────┐
│ PC1: 192.168.1.10│──┐          │            │           │          │
│ PC2: 192.168.1.11│──┼─────────▶│  Translates │──────────▶│ Internet │
│ PC3: 192.168.1.12│──┘          │   to/from  │◀──────────│  Servers │
└─────────────────┘              │203.0.113.45│           └──────────┘
                                  └────────────┘
                                  Public IP: 203.0.113.45

NAT Translation Table:
┌──────────────────────────────────────────────────────┐
│ Internal IP:Port    │  NAT IP:Port     │ Destination │
├────────────────────────────────────────────────────────┤
│ 192.168.1.10:5000  │  203.0.113.45:5000│  8.8.8.8:53 │
│ 192.168.1.11:5001  │  203.0.113.45:5001│  1.1.1.1:443│
│ 192.168.1.12:5002  │  203.0.113.45:5002│  93.1.1.1:80│
└──────────────────────────────────────────────────────┘
```

**Outbound Request Flow:**
```
1. PC1 (192.168.1.10:5000) sends to Google (8.8.8.8:443)
   ↓
2. Router receives, creates NAT entry
   ↓
3. Router rewrites source to (203.0.113.45:5000)
   ↓
4. Google receives from (203.0.113.45:5000)
   ↓
5. Google responds to (203.0.113.45:5000)
   ↓
6. Router checks NAT table, finds PC1
   ↓
7. Router forwards to (192.168.1.10:5000)
   ↓
8. PC1 receives response
```

#### Common Networking Commands

**Find your IP address:**
```bash
# Linux/Mac
ifconfig          # Show all interfaces
ip addr show      # Modern alternative
hostname -I       # Just the IPs

# Windows
ipconfig          # Show all adapters

# Output example:
eth0: inet 192.168.1.100  netmask 255.255.255.0
      ↑ Your local IP
```

**Check which process is using a port:**
```bash
# Linux/Mac
sudo lsof -i :8080
sudo netstat -tuln | grep 8080

# Windows
netstat -ano | findstr :8080

# Output:
PID   PORT   PROCESS
1234  8080   node
```

**Test connection to IP:Port:**
```bash
# Check if port is open
telnet 192.168.1.100 8080
nc -zv 192.168.1.100 8080     # netcat

# Test HTTP endpoint
curl http://192.168.1.100:8080/health

# Scan ports on a host
nmap 192.168.1.100 -p 80,443,8080
```

#### Security Considerations

**Firewall Rules:**
```bash
# Allow specific port (iptables)
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Block all other incoming
sudo iptables -A INPUT -j DROP

# AWS Security Group example:
Inbound Rules:
┌──────────┬──────────┬─────────────┬─────────────┐
│ Type     │ Protocol │ Port        │ Source      │
├──────────┼──────────┼─────────────┼─────────────┤
│ HTTP     │ TCP      │ 80          │ 0.0.0.0/0   │
│ HTTPS    │ TCP      │ 443         │ 0.0.0.0/0   │
│ SSH      │ TCP      │ 22          │ MyIP/32     │
│ Custom   │ TCP      │ 3000        │ VPC only    │
└──────────┴──────────┴─────────────┴─────────────┘
```

**Best Practices:**
```
✓ Expose only necessary ports
✓ Use non-standard ports for SSH (e.g., 2222 instead of 22)
✓ Restrict admin ports to specific IPs
✓ Use VPN for internal service access
✓ Enable firewall on all servers
✗ Don't expose databases directly to internet
✗ Don't use default ports for sensitive services
```
