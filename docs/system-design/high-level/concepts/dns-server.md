# Domain Name System (DNS)

## The Internet's Phone Book

DNS translates human-readable domain names (www.example.com) to machine-readable IP addresses (93.184.216.34). Without DNS, you'd need to memorize IP addresses for every website.

## How DNS Resolution Works: The Complete Journey

**The 8-Step Resolution Process:**

```
User types: www.example.com in browser

1. Browser Cache Check
   ┌──────────────────┐
   │ Browser Cache    │ → "Do I know this?"
   └──────────────────┘    ↓ Cache miss

2. Operating System Cache
   ┌──────────────────┐
   │ OS DNS Cache     │ → "Do I know this?"
   └──────────────────┘    ↓ Cache miss

3. Router Cache
   ┌──────────────────┐
   │ Router Cache     │ → "Do I know this?"
   └──────────────────┘    ↓ Cache miss

4. ISP DNS Resolver (Recursive Resolver)
   ┌──────────────────┐
   │ ISP Resolver     │ → "Let me find out!"
   │ 8.8.8.8          │
   └──────────────────┘
         ↓
         ↓ Query: www.example.com?
         ↓

5. Root DNS Server
   ┌──────────────────┐
   │ Root Server      │ → "Ask .com server at 192.5.6.30"
   │ a.root-servers   │
   └──────────────────┘
         ↓
         ↓ Query: www.example.com?
         ↓

6. TLD (Top-Level Domain) Server
   ┌──────────────────┐
   │ .com TLD Server  │ → "Ask example.com's NS at 1.2.3.4"
   │ 192.5.6.30       │
   └──────────────────┘
         ↓
         ↓ Query: www.example.com?
         ↓

7. Authoritative Name Server
   ┌──────────────────┐
   │ example.com NS   │ → "www.example.com = 93.184.216.34"
   │ 1.2.3.4          │
   └──────────────────┘
         ↓
         ↓ Returns IP
         ↓

8. Back to User
   ┌──────────────────┐
   │ Browser          │ ← "93.184.216.34"
   └──────────────────┘
         ↓
   Connects to 93.184.216.34:443 (HTTPS)
```

**Timing Example:**
```
First Visit (no cache):
  Browser cache:     0ms (miss)
  OS cache:          0ms (miss)
  ISP resolver:      2ms (miss)
  Root server:       20ms
  TLD server:        30ms
  Authoritative:     25ms
  Total:            ~77ms

Second Visit (cached):
  Browser cache:     0ms (hit!)
  Total:             0ms (instant)
```

## DNS Record Types: The Complete Reference

### A Record (Address Record)
**Purpose**: Map domain to IPv4 address

```
DNS Query:
  example.com. IN A

DNS Response:
  example.com.  3600  IN  A  93.184.216.34
               ↑ TTL      ↑ IP Address

Meaning: "example.com is at 93.184.216.34 for 3600 seconds"
```

**Use Cases:**
```
# Main website
www.example.com → 93.184.216.34

# Subdomain for API
api.example.com → 93.184.216.35

# Multiple IPs for load balancing
www.example.com → 93.184.216.34
www.example.com → 93.184.216.35
www.example.com → 93.184.216.36
```

### AAAA Record (IPv6 Address)
**Purpose**: Map domain to IPv6 address

```
example.com.  3600  IN  AAAA  2001:db8:85a3::8a2e:370:7334
```

**Modern Setup:**
```
# Dual-stack (both IPv4 and IPv6)
example.com.  IN  A     93.184.216.34
example.com.  IN  AAAA  2001:db8:85a3::8a2e:370:7334

Browser behavior:
1. Checks for AAAA (IPv6) first
2. Falls back to A (IPv4) if unavailable
```

### CNAME Record (Canonical Name)
**Purpose**: Alias one domain to another

```
www.example.com.  IN  CNAME  example.com.

Resolution:
www.example.com → (CNAME) → example.com → (A) → 93.184.216.34
```

**Real-World Examples:**
```
# CDN Setup
static.example.com.  IN  CNAME  d111111abcdef8.cloudfront.net.

# Subdomain aliasing
blog.example.com.    IN  CNAME  myblog.wordpress.com.

# Environment-specific
staging.example.com. IN  CNAME  staging-server.aws.example.com.

# Load balancer
www.example.com.     IN  CNAME  lb-12345.us-east-1.elb.amazonaws.com.
```

**CNAME Limitations:**
```
✗ Can't use at root domain (example.com)
  (RFC violation, but some providers allow it)

✗ Can't coexist with other records
  example.com. CNAME  other.com.  ← Invalid
  example.com. MX     mail.com.   ← Conflict!

✓ Perfect for subdomains
  www.example.com. CNAME other.com.  ← Valid
```

### MX Record (Mail Exchange)
**Purpose**: Specify mail servers for domain

```
example.com.  IN  MX  10  mail1.example.com.
example.com.  IN  MX  20  mail2.example.com.
                   ↑ Priority (lower = preferred)

Email to: user@example.com
  ↓
DNS lookup: example.com MX records
  ↓
Try mail1 (priority 10) first
If fails, try mail2 (priority 20)
```

**Google Workspace Example:**
```
example.com.  IN  MX  1   aspmx.l.google.com.
example.com.  IN  MX  5   alt1.aspmx.l.google.com.
example.com.  IN  MX  5   alt2.aspmx.l.google.com.
example.com.  IN  MX  10  alt3.aspmx.l.google.com.
example.com.  IN  MX  10  alt4.aspmx.l.google.com.
```

### TXT Record (Text Information)
**Purpose**: Store arbitrary text, verification, security policies

**SPF (Sender Policy Framework) - Prevent Email Spoofing:**
```
example.com.  IN  TXT  "v=spf1 include:_spf.google.com ~all"

Meaning:
  v=spf1          → Version 1
  include:...     → Allow Google's mail servers
  ~all            → Soft fail others (probably spam)
```

**DKIM (DomainKeys Identified Mail) - Email Signature:**
```
default._domainkey.example.com.  IN  TXT  "v=DKIM1; k=rsa; p=MIGfMA0GCS..."
                                             ↑ Public key for verification
```

**DMARC (Domain-based Message Authentication):**
```
_dmarc.example.com.  IN  TXT  "v=DMARC1; p=reject; rua=mailto:dmarc@example.com"

Meaning:
  p=reject        → Reject emails that fail SPF/DKIM
  rua=mailto:...  → Send reports to this email
```

**Domain Verification:**
```
# Google Search Console
example.com.  IN  TXT  "google-site-verification=abc123..."

# SSL Certificate Validation
_acme-challenge.example.com.  IN  TXT  "validation-token-here"
```

### NS Record (Name Server)
**Purpose**: Delegate domain to specific DNS servers

```
example.com.  IN  NS  ns1.nameserver.com.
example.com.  IN  NS  ns2.nameserver.com.

Meaning: "Ask these servers for example.com records"
```

**Subdomain Delegation:**
```
# Main domain managed by Cloudflare
example.com.      IN  NS  ns1.cloudflare.com.

# Blog subdomain managed by WordPress
blog.example.com. IN  NS  ns1.wordpress.com.
                           ns2.wordpress.com.
```

### Other Important Records

**SRV Record (Service Location):**
```
_service._proto.name.  TTL  IN  SRV  priority weight port target

Example (Minecraft server):
_minecraft._tcp.example.com.  IN  SRV  0 5 25565  mc.example.com.
                                       ↑ ↑   ↑      ↑
                                     Pri Wt Port  Host
```

**CAA Record (Certificate Authority Authorization):**
```
example.com.  IN  CAA  0 issue "letsencrypt.org"

Meaning: "Only Let's Encrypt can issue SSL certs for this domain"
```

## DNS Caching: The Speed Secret

**TTL (Time To Live):**
```
example.com.  3600  IN  A  93.184.216.34
              ↑ Cache for 3600 seconds (1 hour)

TTL Strategy:
Static content:    86400  (24 hours)
Dynamic content:   300    (5 minutes)
Before migration:  60     (1 minute) ← Quick updates
After migration:   3600   (1 hour)   ← Stable
```

**Cache Hierarchy:**
```
┌─────────────────┐  TTL: Varies
│ Browser Cache   │  (respects TTL)
└────────┬────────┘
         ↓
┌─────────────────┐  TTL: Varies
│ OS Cache        │  (respects TTL)
└────────┬────────┘
         ↓
┌─────────────────┐  TTL: Varies
│ ISP Resolver    │  (might ignore TTL)
└────────┬────────┘
         ↓
┌─────────────────┐  Authoritative
│ DNS Server      │  (source of truth)
└─────────────────┘
```

## Real-World Use Cases

**Use Case 1: Multi-Region Setup**
```
GeoDNS Routing:

User in US → DNS returns: 52.1.1.1  (US East server)
User in EU → DNS returns: 18.1.1.1  (EU West server)
User in Asia → DNS returns: 13.1.1.1 (Asia Pacific server)

Configuration (Route 53 example):
www.example.com
  ├─ US-EAST-1:  52.1.1.1   (for North America)
  ├─ EU-WEST-1:  18.1.1.1   (for Europe)
  └─ AP-SOUTHEAST-1: 13.1.1.1 (for Asia)
```

**Use Case 2: Blue-Green Deployment**
```
Before deployment:
www.example.com → 10.0.1.50 (blue environment - v1.0)

During deployment:
1. Deploy v2.0 to green: 10.0.1.51
2. Test green environment
3. Update DNS:
   www.example.com → 10.0.1.51 (green environment - v2.0)
4. Wait for TTL to expire
5. All traffic now on v2.0
6. Keep blue as rollback option

Rollback (if needed):
www.example.com → 10.0.1.50 (back to blue - v1.0)
```

**Use Case 3: CDN Configuration**
```
Setup:
┌──────────────────────────────────────┐
│ Origin Server: origin.example.com    │
│ IP: 93.184.216.34                    │
└──────────────────────────────────────┘
         ↑
         │ Pulls content
         │
┌──────────────────────────────────────┐
│ CDN: d123.cloudfront.net             │
│ Edge Locations: 200+ globally        │
└──────────────────────────────────────┘
         ↑
         │ CNAME
         │
┌──────────────────────────────────────┐
│ Public DNS:                          │
│ www.example.com → d123.cloudfront.net│
│ static.example.com → d123.cloudfront │
└──────────────────────────────────────┘
```

**Use Case 4: Failover Configuration**
```
Health Check Based Failover:

Primary:
www.example.com → 10.0.1.100 (primary server)
  ↓ Health check fails!
  ↓
Automatic Failover:
www.example.com → 10.0.2.100 (backup server)

Route 53 Config:
www.example.com
  Primary:  10.0.1.100 (healthy check every 30s)
  Secondary: 10.0.2.100 (used if primary fails)
```

## DNS Commands & Tools

**Query DNS Records:**
```bash
# Using dig (most detailed)
dig example.com
dig example.com A
dig example.com MX
dig @8.8.8.8 example.com  # Query specific DNS server

# Using nslookup
nslookup example.com
nslookup -type=MX example.com

# Using host
host example.com
host -t MX example.com
```

**Example dig output:**
```bash
$ dig example.com

; <<>> DiG 9.10.6 <<>> example.com
;; ANSWER SECTION:
example.com.    3600    IN    A    93.184.216.34
                ↑ TTL        ↑ Type  ↑ IP

;; Query time: 23 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Sat Jan 25 10:30:00 PST 2026
```

**Flush DNS Cache:**
```bash
# macOS
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

# Windows
ipconfig /flushdns

# Linux
sudo systemd-resolve --flush-caches
sudo /etc/init.d/nscd restart

# Chrome browser
chrome://net-internals/#dns → Clear host cache
```

**Check DNS Propagation:**
```bash
# Query multiple DNS servers worldwide
dig @8.8.8.8 example.com      # Google (US)
dig @1.1.1.1 example.com      # Cloudflare (Global)
dig @208.67.222.222 example.com  # OpenDNS (US)

# Online tools:
# https://www.whatsmydns.net
# https://dnschecker.org
```

## DNS Security

**DNSSEC (DNS Security Extensions):**
```
Problem: DNS responses can be spoofed

Solution: Cryptographic signatures

1. DNS server signs responses with private key
2. Client verifies with public key (DS/DNSKEY records)
3. Chain of trust from root to your domain

Example:
example.com.  IN  DNSKEY  257 3 8 AwEAAa...
                              ↑ Public key

example.com.  IN  RRSIG   A 8 2 3600 20260201000000 ...
                              ↑ Signature
```

**DNS over HTTPS (DoH) / DNS over TLS (DoT):**
```
Traditional DNS: Plain text (can be intercepted)
  User → ISP DNS (port 53, unencrypted)

DoH/DoT: Encrypted
  User → Cloudflare 1.1.1.1 (HTTPS/TLS, encrypted)

Benefits:
  ✓ Privacy (ISP can't see queries)
  ✓ Integrity (can't be modified)
  ✓ Bypasses censorship
```

## Common DNS Issues

**Issue 1: Propagation Delay**
```
Problem:
  Changed DNS record, but old IP still appears

Cause:
  TTL not expired, caches still have old value

Solution:
  1. Lower TTL before changes (24 hours in advance)
  2. Make changes
  3. Wait for old TTL to expire
  4. Raise TTL back to normal
```

**Issue 2: CNAME at Root**
```
Problem:
  example.com. CNAME other.com.  ← Not allowed!

Reason:
  RFC violation (conflicts with NS, MX records)

Solution:
  Use A/AAAA record at root
  Or use ALIAS/ANAME record (provider-specific)
```

**Issue 3: Multiple CNAMEs**
```
Problem:
  www → cdn → lb → server (too many hops)

Impact:
  Multiple DNS lookups = slower

Solution:
  Minimize CNAME chain depth
  Use A records when possible
```

## Best Practices

```
✓ Use low TTL (300s) before making changes
✓ Use high TTL (3600s+) for stable records
✓ Implement DNSSEC for security
✓ Use multiple NS records (redundancy)
✓ Monitor DNS health (uptime, latency)
✓ Use GeoDNS for global applications
✓ Enable health-check based failover

✗ Don't use single DNS provider (SPOF)
✗ Don't set TTL too low permanently (load on DNS)
✗ Don't forget to update NS records when changing providers
✗ Don't use CNAME at root domain
```

---

# Design DNS server

## Youtube

- [How DNS works? | System Design of Domain Name System](https://www.youtube.com/watch?v=QVdX34quUgU)

- [Build Your Own DNS Server - Beginner Friendly](https://www.youtube.com/watch?v=Ui66W7zeAbI)
- [Build Your Own DNS Server](https://www.youtube.com/watch?v=52wnTsBI_HE)
- [I created an AI Based DNS Server - Toying with DNS](https://www.youtube.com/watch?v=Sgk0yy8rJ8M)




## Websites

- [DNS Record Types: Defined and Explained](https://www.site24x7.com/learn/dns-record-types.html)