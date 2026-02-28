# SMTP Server


## Youtube

- [Build Your Own MAIL Server | SMTP Server](https://www.youtube.com/watch?v=l3htAzOAx7c)



## Theory

### What is SMTP Protocol?

**SMTP (Simple Mail Transfer Protocol)** is an application-layer protocol used for sending and transferring email messages between mail servers and from email clients to mail servers.

- **Default Port**: 25 (unencrypted)
- **Protocol Type**: TCP-based, text-based protocol
- **Purpose**: Email transmission and relay between servers
- **Direction**: Push protocol (sender pushes email to recipient's server)

### SMTP Secured (SMTPS)

**Secure SMTP** uses encryption to protect email transmission:

1. **SMTPS (SMTP over SSL/TLS)**
   - **Port 465**: SMTP over implicit TLS/SSL (deprecated but still widely used)
   - Connection is encrypted from the start

2. **STARTTLS**
   - **Port 587**: Submission port with STARTTLS (recommended)
   - **Port 25**: Can also use STARTTLS for server-to-server communication
   - Connection starts unencrypted, then upgrades to TLS

### SMTP Server Components

An SMTP server consists of several key components:

```
┌─────────────────────────────────────────────────────────────┐
│                      SMTP Server                            │
│                                                             │
│  ┌─────────────────┐        ┌──────────────────┐          │
│  │   Mail User     │        │   Mail Transfer  │          │
│  │   Agent (MUA)   │───────▶│   Agent (MTA)    │          │
│  │  (Email Client) │        │  (SMTP Server)   │          │
│  └─────────────────┘        └──────────────────┘          │
│                                      │                      │
│                                      ▼                      │
│                             ┌──────────────────┐           │
│                             │   Mail Queue     │           │
│                             │   (Outgoing)     │           │
│                             └──────────────────┘           │
│                                      │                      │
│                                      ▼                      │
│                             ┌──────────────────┐           │
│                             │  Relay/Routing   │           │
│                             │     Engine       │           │
│                             └──────────────────┘           │
│                                      │                      │
│                                      ▼                      │
│                             ┌──────────────────┐           │
│                             │   Mail Delivery  │           │
│                             │   Agent (MDA)    │           │
│                             └──────────────────┘           │
│                                      │                      │
│                                      ▼                      │
│                             ┌──────────────────┐           │
│                             │   Mailbox        │           │
│                             │   Storage        │           │
│                             └──────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

**Components:**

1. **Mail User Agent (MUA)**: Email client (Outlook, Gmail, Thunderbird)
2. **Mail Transfer Agent (MTA)**: SMTP server that sends/receives emails
3. **Mail Queue**: Temporary storage for outgoing emails
4. **Relay/Routing Engine**: Routes emails to appropriate destination
5. **Mail Delivery Agent (MDA)**: Delivers email to recipient's mailbox
6. **Mailbox Storage**: Final storage location for emails

### SMTP Commands

Core SMTP commands used in email transmission:

| Command | Description | Example |
|---------|-------------|---------|
| `HELO` | Identify client to server (legacy) | `HELO client.example.com` |
| `EHLO` | Extended HELO (modern, supports extensions) | `EHLO client.example.com` |
| `MAIL FROM` | Specify sender's email address | `MAIL FROM:<sender@example.com>` |
| `RCPT TO` | Specify recipient's email address | `RCPT TO:<recipient@example.com>` |
| `DATA` | Begin email message content | `DATA` |
| `RSET` | Reset the current session | `RSET` |
| `VRFY` | Verify email address exists | `VRFY user@example.com` |
| `NOOP` | No operation (keep-alive) | `NOOP` |
| `QUIT` | End session | `QUIT` |
| `STARTTLS` | Upgrade to encrypted connection | `STARTTLS` |
| `AUTH` | Authenticate client | `AUTH LOGIN` |

**Terms:**

- **Envelope**: SMTP commands that define sender/recipient (MAIL FROM, RCPT TO)
- **Header**: Email metadata (From, To, Subject, Date)
- **Body**: Actual message content
- **MIME**: Multipurpose Internet Mail Extensions (attachments, HTML)

### SMTP Status Codes

Status codes indicate the result of SMTP commands:

| Code Range | Category | Meaning |
|------------|----------|---------|
| 2xx | Success | Command completed successfully |
| 3xx | Intermediate | Waiting for more information |
| 4xx | Transient Error | Temporary failure, retry later |
| 5xx | Permanent Error | Permanent failure, don't retry |

**Common Status Codes:**

| Code | Message | Description |
|------|---------|-------------|
| 220 | Service ready | Server ready to accept connection |
| 221 | Service closing | Server closing connection |
| 250 | Requested action okay | Command completed successfully |
| 251 | User not local; will forward | Recipient not on this server, forwarding |
| 354 | Start mail input | Ready to receive message data |
| 421 | Service not available | Server temporarily unavailable |
| 450 | Mailbox unavailable | Mailbox temporarily unavailable |
| 451 | Action aborted | Local error in processing |
| 452 | Insufficient storage | Not enough disk space |
| 500 | Syntax error | Command not recognized |
| 501 | Syntax error in parameters | Invalid command arguments |
| 502 | Command not implemented | Command not supported |
| 503 | Bad sequence of commands | Commands sent in wrong order |
| 550 | Mailbox unavailable | Mailbox does not exist |
| 551 | User not local | Recipient not on this server |
| 552 | Storage allocation exceeded | Message too large |
| 553 | Mailbox name invalid | Invalid email address |
| 554 | Transaction failed | General permanent failure |

### Complete Email Sending Flow

```
Client                                    SMTP Server
  │                                            │
  │────── TCP Connection (Port 25/587) ──────▶│
  │                                            │
  │◀────────── 220 Service Ready ─────────────│
  │                                            │
  │────────── EHLO client.com ───────────────▶│
  │                                            │
  │◀────── 250 Hello client.com ──────────────│
  │        250-SIZE 52428800                   │
  │        250-STARTTLS                        │
  │        250 AUTH LOGIN PLAIN                │
  │                                            │
  │────────── STARTTLS ──────────────────────▶│
  │                                            │
  │◀────── 220 Ready to start TLS ────────────│
  │                                            │
  │═══════ TLS Handshake & Encryption ════════│
  │                                            │
  │────── AUTH LOGIN ────────────────────────▶│
  │                                            │
  │◀────── 334 (base64 Username) ─────────────│
  │                                            │
  │────── dXNlcm5hbWU= ───────────────────────▶│
  │                                            │
  │◀────── 334 (base64 Password) ─────────────│
  │                                            │
  │────── cGFzc3dvcmQ= ───────────────────────▶│
  │                                            │
  │◀────── 235 Authentication successful ──────│
  │                                            │
  │─── MAIL FROM:<sender@example.com> ───────▶│
  │                                            │
  │◀────── 250 OK ─────────────────────────────│
  │                                            │
  │─── RCPT TO:<recipient@example.com> ──────▶│
  │                                            │
  │◀────── 250 OK ─────────────────────────────│
  │                                            │
  │────── DATA ───────────────────────────────▶│
  │                                            │
  │◀────── 354 Start mail input ──────────────│
  │                                            │
  │─── From: sender@example.com ──────────────▶│
  │─── To: recipient@example.com ─────────────▶│
  │─── Subject: Test Email ───────────────────▶│
  │─── Date: Mon, 20 Jan 2026 10:00:00 ───────▶│
  │───                              ───────────▶│
  │─── This is the email body ────────────────▶│
  │─── . (end of data) ───────────────────────▶│
  │                                            │
  │◀────── 250 Message accepted ───────────────│
  │                                            │
  │────── QUIT ───────────────────────────────▶│
  │                                            │
  │◀────── 221 Bye ────────────────────────────│
  │                                            │
  │────── Connection Closed ───────────────────│
```

**Step-by-step breakdown:**

1. **Handshake**: TCP connection established, server sends 220 greeting
2. **EHLO**: Client identifies itself, server lists supported extensions
3. **STARTTLS**: (Optional) Upgrade to encrypted connection
4. **AUTH**: (Optional) Client authenticates with credentials
5. **MAIL FROM**: Specify sender's email address
6. **RCPT TO**: Specify recipient's email address (can be repeated for multiple recipients)
7. **DATA**: Begin message transmission
8. **Message Content**: Headers and body, terminated by `\r\n.\r\n`
9. **QUIT**: Close the connection gracefully

### DNS Records for Email

#### MX Record (Mail Exchanger)

**Purpose**: Specifies the mail servers responsible for accepting email for a domain, with priority ordering for failover.

**Record Type**: MX (dedicated record type)

**Example:**
```
example.com.    MX    10    mail1.example.com.
example.com.    MX    20    mail2.example.com.
example.com.    MX    30    mail3.example.com.
```

**MX Record Components:**

| Component | Description | Example |
|-----------|-------------|---------|
| Domain | Domain receiving email | `example.com.` |
| Record Type | Always MX | `MX` |
| Priority | Preference (lower = higher priority) | `10`, `20`, `30` |
| Mail Server | Hostname of mail server | `mail1.example.com.` |

**Priority System:**

- **Lower number = Higher priority**: Server with priority 10 is tried first
- **Same priority**: Load balanced between servers with same priority
- **Failover**: If primary fails, try next priority level

**Example Configurations:**

1. **Single Mail Server:**
   ```
   example.com.    MX    10    mail.example.com.
   ```

2. **Primary with Backup:**
   ```
   example.com.    MX    10    mail1.example.com.
   example.com.    MX    20    mail2.example.com.
   ```

3. **Load Balanced Primary:**
   ```
   example.com.    MX    10    mail1.example.com.
   example.com.    MX    10    mail2.example.com.
   example.com.    MX    20    backup.example.com.
   ```

4. **Cloud Email Services:**
   ```
   example.com.    MX    1     aspmx.l.google.com.
   example.com.    MX    5     alt1.aspmx.l.google.com.
   example.com.    MX    5     alt2.aspmx.l.google.com.
   example.com.    MX    10    alt3.aspmx.l.google.com.
   example.com.    MX    10    alt4.aspmx.l.google.com.
   ```

**MX Lookup Process:**

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: DNS Query for MX Records                           │
│ Query: example.com MX                                       │
│ Response:                                                   │
│   10 mail1.example.com.                                     │
│   20 mail2.example.com.                                     │
│   30 mail3.example.com.                                     │
└─────────────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Sort by Priority (lowest first)                    │
│ 1. mail1.example.com (priority 10)  ← Try first           │
│ 2. mail2.example.com (priority 20)  ← Try if 1 fails      │
│ 3. mail3.example.com (priority 30)  ← Try if 2 fails      │
└─────────────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Resolve A/AAAA Record for mail1.example.com        │
│ Query: mail1.example.com A                                  │
│ Response: 192.0.2.10                                        │
└─────────────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Attempt SMTP Connection                            │
│ Connect to 192.0.2.10:25                                    │
│ If successful → Deliver email                               │
│ If failed → Try mail2.example.com (priority 20)            │
└─────────────────────────────────────────────────────────────┘
```

**Best Practices:**

- **Always use FQDN**: End with dot (.) for absolute domain
- **Multiple MX records**: Provide redundancy (minimum 2)
- **Valid hostnames**: MX records must point to A/AAAA records, not CNAME
- **No localhost**: Never point MX to localhost or 127.0.0.1
- **Priority spacing**: Use gaps (10, 20, 30) to allow future insertions

**Common Issues:**

- **MX pointing to CNAME**: Not allowed per RFC (must point to A record)
- **No A record**: MX hostname must resolve to IP
- **Loop detection**: Mail server won't accept mail for itself via MX
- **No MX record**: Falls back to A record of domain itself

#### A Record (Address Record)

**Purpose**: Maps a domain name to an IPv4 address.

**Record Type**: A (Address)

**Example:**
```
mail1.example.com.    A    192.0.2.10
mail2.example.com.    A    192.0.2.11
www.example.com.      A    192.0.2.1
example.com.          A    192.0.2.1
```

**Multiple A Records (Round-Robin Load Balancing):**
```
mail.example.com.     A    192.0.2.10
mail.example.com.     A    192.0.2.11
mail.example.com.     A    192.0.2.12
```

**AAAA Record (IPv6):**

Similar to A record but for IPv6 addresses:

```
mail1.example.com.    AAAA    2001:db8::1
mail2.example.com.    AAAA    2001:db8::2
```

**Email DNS Resolution Flow:**

```
1. MX Query: example.com → mail.example.com
2. A Query: mail.example.com → 192.0.2.10
3. SMTP Connection: 192.0.2.10:25
```

**Dual Stack (IPv4 + IPv6):**
```
mail.example.com.     A       192.0.2.10
mail.example.com.     AAAA    2001:db8::1
```

#### PTR Record (Pointer Record)

**Purpose**: Reverse DNS lookup - maps IP address to domain name. Critical for email servers to prevent spam.

**Record Type**: PTR (set in reverse DNS zone)

**Example:**
```
10.2.0.192.in-addr.arpa.    PTR    mail.example.com.
```

**Why PTR is Important for Email:**

1. **Spam Prevention**: Many mail servers reject emails from IPs without valid PTR
2. **Reputation**: Proper reverse DNS improves sender reputation
3. **Verification**: Confirms mail server is legitimate

**Forward vs Reverse DNS:**

```
Forward Lookup (A):
  mail.example.com → 192.0.2.10

Reverse Lookup (PTR):
  192.0.2.10 → mail.example.com
```

**PTR Validation Process:**

```
┌─────────────────────────────────────────────────────────┐
│ Email received from IP: 192.0.2.10                     │
│ EHLO: mail.example.com                                  │
└─────────────────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│ Reverse DNS Lookup (PTR)                               │
│ Query: 10.2.0.192.in-addr.arpa PTR                     │
│ Response: mail.example.com                              │
└─────────────────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│ Forward Confirmation (A)                               │
│ Query: mail.example.com A                               │
│ Response: 192.0.2.10                                    │
└─────────────────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│ Validation Result                                      │
│ ✓ FCrDNS Pass: PTR matches forward DNS                 │
│ ✗ FCrDNS Fail: Mismatch or missing PTR                 │
└─────────────────────────────────────────────────────────┘
```

**FCrDNS (Forward-Confirmed Reverse DNS):**

The PTR record must match at least one A record:

```
PTR: 192.0.2.10 → mail.example.com
A:   mail.example.com → 192.0.2.10 ✓ MATCH
```

**Important Notes:**

- **ISP Control**: PTR records typically managed by IP owner (ISP/hosting provider)
- **One PTR per IP**: Each IP can only have one PTR record
- **Match EHLO**: PTR should match hostname used in SMTP EHLO command

#### TXT Record (Text Record)

**Purpose**: Store arbitrary text data. Used extensively for email authentication (SPF, DKIM, DMARC).

**Record Type**: TXT

**Examples:**

```
example.com.                          TXT    "v=spf1 mx ~all"
default._domainkey.example.com.       TXT    "v=DKIM1; k=rsa; p=MIGfMA..."
_dmarc.example.com.                   TXT    "v=DMARC1; p=reject; rua=..."
example.com.                          TXT    "google-site-verification=abc123"
```

**Multiple TXT Records:**

A domain can have multiple TXT records for different purposes:

```
example.com.    TXT    "v=spf1 include:_spf.google.com ~all"
example.com.    TXT    "google-site-verification=abc123xyz"
example.com.    TXT    "MS=ms12345678"
example.com.    TXT    "stripe-verification=secret123"
```

**Character Limits:**

- **Single string**: 255 characters
- **Multiple strings**: Can concatenate for longer records
  ```
  TXT    "v=DKIM1; p=MIGfMA0GCSqGSIb3DQEBAQUAA4G..." "NADCBiQKBgQDXyz123..."
  ```

#### CNAME Record (Canonical Name)

**Purpose**: Creates an alias from one domain to another.

**Record Type**: CNAME

**Example:**
```
mail.example.com.     CNAME    mail.hosting-provider.com.
```

**Important Restrictions:**

- **Cannot coexist** with MX record at same level
- **Invalid for email**:
  ```
  example.com.    MX    10    mail.example.com.
  mail.example.com. CNAME  mailserver.provider.com.  ✗ WRONG
  ```
  
- **Correct usage**:
  ```
  example.com.    MX    10    mail.example.com.
  mail.example.com. A     192.0.2.10                ✓ CORRECT
  ```

**Valid CNAME Use Cases:**

1. **Subdomain delegation:**
   ```
   webmail.example.com.    CNAME    mail.google.com.
   ```

2. **Service aliases:**
   ```
   smtp.example.com.       CNAME    mail1.example.com.
   imap.example.com.       CNAME    mail1.example.com.
   ```

**RFC Restriction**: CNAME cannot coexist with any other record type at the same name.

#### SPF Record (Sender Policy Framework)

**Purpose**: Prevents email spoofing and phishing by specifying which mail servers are authorized to send emails on behalf of a domain.

**Record Type**: TXT record published in DNS

**Example:**
```
example.com.    TXT    "v=spf1 ip4:192.0.2.0/24 ip6:2001:db8::/32 include:_spf.google.com a mx ~all"
```

**SPF Mechanisms (Authorization Methods):**

| Mechanism | Description | Example |
|-----------|-------------|---------|
| `all` | Matches all IPs (usually used at end) | `~all`, `-all` |
| `ip4` | Authorize specific IPv4 address/range | `ip4:192.0.2.10` or `ip4:192.0.2.0/24` |
| `ip6` | Authorize specific IPv6 address/range | `ip6:2001:db8::1` or `ip6:2001:db8::/32` |
| `a` | Authorize IPs from domain's A record | `a:example.com` or just `a` |
| `mx` | Authorize IPs from domain's MX records | `mx:example.com` or just `mx` |
| `include` | Include another domain's SPF record | `include:_spf.google.com` |
| `exists` | DNS lookup check (advanced) | `exists:%{i}.spf.example.com` |
| `ptr` | Reverse DNS lookup (deprecated) | `ptr:example.com` |

**SPF Qualifiers (Results):**

| Qualifier | Symbol | Meaning | Action |
|-----------|--------|---------|--------|
| Pass | `+` (default) | Sender is authorized | Accept email |
| Fail | `-` | Sender not authorized | Reject email |
| SoftFail | `~` | Sender not authorized (lenient) | Accept but mark suspicious |
| Neutral | `?` | No policy assertion | Accept (treat as no SPF) |

**Complete Examples:**

1. **Simple SPF (only MX servers can send)**
   ```
   example.com.    TXT    "v=spf1 mx -all"
   ```

2. **SPF with multiple sources**
   ```
   example.com.    TXT    "v=spf1 ip4:192.0.2.0/24 include:_spf.google.com include:sendgrid.net mx ~all"
   ```

3. **SPF for subdomain**
   ```
   mail.example.com.    TXT    "v=spf1 ip4:192.0.2.10 -all"
   ```

**SPF Validation Process:**

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. Email received from IP 192.0.2.15                           │
│    MAIL FROM: <user@example.com>                               │
└─────────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. Query DNS: TXT record for example.com                       │
│    Response: "v=spf1 ip4:192.0.2.0/24 mx ~all"                 │
└─────────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. Check if sender IP (192.0.2.15) matches SPF mechanisms      │
│    ✓ ip4:192.0.2.0/24 matches (192.0.2.15 is in range)        │
└─────────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. Result: SPF PASS                                            │
│    Email accepted, no spoofing detected                         │
└─────────────────────────────────────────────────────────────────┘
```

**Common Issues:**

- **Too many DNS lookups**: SPF limit is 10 DNS lookups (includes, a, mx)
- **Multiple SPF records**: Only one SPF record per domain (use one TXT with all mechanisms)
- **Missing "all" mechanism**: Always end with `~all` or `-all`
- **Subdomain inheritance**: Subdomains don't inherit parent SPF

**SPF Headers Added:**

```
Received-SPF: pass (google.com: domain of sender@example.com designates 192.0.2.15 as permitted sender)
```

#### DKIM Record (DomainKeys Identified Mail)

**Purpose**: Email authentication using cryptographic signatures to verify email integrity and sender authenticity.

**Record Type**: TXT record at subdomain `<selector>._domainkey.<domain>`

**Example:**
```
default._domainkey.example.com.    TXT    "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC..."
```

**DKIM Record Components:**

| Tag | Required | Description | Example |
|-----|----------|-------------|---------|
| `v` | Yes | Version | `v=DKIM1` |
| `k` | No | Key type | `k=rsa` (default), `k=ed25519` |
| `p` | Yes | Public key (base64) | `p=MIGfMA0GCS...` |
| `t` | No | Flags | `t=s` (strict, domain must match exactly), `t=y` (testing mode) |
| `s` | No | Service types | `s=email` or `s=*` (all services) |
| `h` | No | Acceptable hash algorithms | `h=sha256` |
| `n` | No | Notes/comments | `n=This is a DKIM key` |

**DKIM Signature Header:**

When an email is sent, the DKIM signature is added to the email header:

```
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
  d=example.com; s=default;
  h=from:to:subject:date:message-id:mime-version;
  bh=frcCV1k9oG9oKj3dpUqdJg1PxRT2RSN/XKdLCPjaYaY=;
  b=GJ3VbW8qFZj8TKNl2f8PqN3K9BxYmZvQ7RtPq5VzX9K8FjNmL2kJ3h4G...
```

**Signature Components:**

| Tag | Description | Example |
|-----|-------------|---------|
| `v` | Version | `v=1` |
| `a` | Signing algorithm | `a=rsa-sha256` |
| `c` | Canonicalization algorithm | `c=relaxed/relaxed` or `c=simple/simple` |
| `d` | Signing domain | `d=example.com` |
| `s` | Selector (subdomain) | `s=default` |
| `h` | Signed headers | `h=from:to:subject:date` |
| `bh` | Body hash | `bh=frcCV1k9...` (base64) |
| `b` | Signature of headers | `b=GJ3VbW8...` (base64) |
| `i` | Identity (user) | `i=@example.com` |
| `t` | Timestamp | `t=1737369600` |
| `x` | Expiration time | `x=1737456000` |

**DKIM Signing & Verification Process:**

```
┌──────────────────── SENDER SIDE ────────────────────┐
│                                                      │
│  1. Compose Email                                    │
│     From: user@example.com                           │
│     To: recipient@gmail.com                          │
│     Subject: Hello                                   │
│     Body: This is a test email                       │
│                                                      │
│            ▼                                         │
│  2. Canonicalize email content                       │
│     (normalize whitespace, line endings)             │
│                                                      │
│            ▼                                         │
│  3. Hash the body                                    │
│     SHA-256(body) = frcCV1k9oG9oKj3...              │
│                                                      │
│            ▼                                         │
│  4. Create header hash                               │
│     SHA-256(from:to:subject:date:body-hash)          │
│                                                      │
│            ▼                                         │
│  5. Sign with PRIVATE KEY                            │
│     RSA(header-hash, private-key) = signature        │
│                                                      │
│            ▼                                         │
│  6. Add DKIM-Signature header to email               │
│     DKIM-Signature: v=1; a=rsa-sha256; d=example.com │
│                     s=default; bh=...; b=...         │
│                                                      │
└──────────────────────────────────────────────────────┘
                          │
                          │ Email transmitted
                          │
                          ▼
┌──────────────────── RECEIVER SIDE ───────────────────┐
│                                                      │
│  7. Receive email with DKIM-Signature header         │
│                                                      │
│            ▼                                         │
│  8. Extract signature parameters                     │
│     Domain: d=example.com                            │
│     Selector: s=default                              │
│                                                      │
│            ▼                                         │
│  9. DNS Query for public key                         │
│     Query: default._domainkey.example.com TXT        │
│     Response: v=DKIM1; k=rsa; p=MIGfMA0GCS...       │
│                                                      │
│            ▼                                         │
│  10. Verify body hash                                │
│      Compute: SHA-256(body)                          │
│      Compare with bh= value in signature             │
│                                                      │
│            ▼                                         │
│  11. Verify signature                                │
│      Decrypt signature with PUBLIC KEY               │
│      Compare with computed header hash               │
│                                                      │
│            ▼                                         │
│  12. DKIM Result                                     │
│      ✓ PASS: Signature valid, email not modified    │
│      ✗ FAIL: Signature invalid or email tampered    │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Multiple DKIM Selectors:**

Organizations often use multiple selectors for different purposes:

```
default._domainkey.example.com    TXT    "v=DKIM1; k=rsa; p=..."
marketing._domainkey.example.com  TXT    "v=DKIM1; k=rsa; p=..."
transactional._domainkey.example.com TXT "v=DKIM1; k=rsa; p=..."
```

**Benefits:**

- **Email Integrity**: Detect if email was modified in transit
- **Authentication**: Verify email actually came from claimed domain
- **Reputation**: Improve sender reputation and deliverability
- **Non-repudiation**: Sender cannot deny sending the email

**DKIM vs SPF:**

| Feature | DKIM | SPF |
|---------|------|-----|
| What it validates | Email content & domain | Sender IP address |
| Survives forwarding | Yes | No (IP changes) |
| Detects tampering | Yes | No |
| Cryptographic | Yes | No |
| DNS lookups | 1 per signature | Up to 10 |

**Common Issues:**

- **Key length**: Recommended 2048-bit RSA (1024-bit deprecated)
- **DNS record too long**: Split with quotes or use shorter key
- **Clock skew**: Signature timestamp must be valid
- **Selector mismatch**: Ensure selector in signature matches DNS record
- **Header modification**: Some headers change during transit (Received, etc.)

#### DMARC Record (Domain-based Message Authentication, Reporting & Conformance)

**Purpose**: Policy framework that builds on SPF and DKIM to tell receiving servers how to handle authentication failures and where to send reports.

**Record Type**: TXT record at subdomain `_dmarc.<domain>`

**Example:**
```
_dmarc.example.com.    TXT    "v=DMARC1; p=reject; rua=mailto:dmarc-reports@example.com; ruf=mailto:dmarc-forensic@example.com; pct=100; adkim=s; aspf=s; sp=reject; fo=1"
```

**DMARC Tags:**

| Tag | Required | Description | Values | Example |
|-----|----------|-------------|--------|---------|
| `v` | Yes | Protocol version | `DMARC1` | `v=DMARC1` |
| `p` | Yes | Policy for domain | `none`, `quarantine`, `reject` | `p=reject` |
| `sp` | No | Policy for subdomains | `none`, `quarantine`, `reject` | `sp=quarantine` |
| `rua` | No | Aggregate reports email | mailto: URI | `rua=mailto:reports@example.com` |
| `ruf` | No | Forensic reports email | mailto: URI | `ruf=mailto:forensic@example.com` |
| `pct` | No | % of emails to apply policy | 0-100 | `pct=100` |
| `adkim` | No | DKIM alignment mode | `r` (relaxed), `s` (strict) | `adkim=r` |
| `aspf` | No | SPF alignment mode | `r` (relaxed), `s` (strict) | `aspf=r` |
| `fo` | No | Forensic report options | `0`, `1`, `d`, `s` | `fo=1` |
| `rf` | No | Report format | `afrf`, `iodef` | `rf=afrf` |
| `ri` | No | Report interval (seconds) | Number | `ri=86400` (24h) |

**DMARC Policies:**

| Policy | Description | Action | Use Case |
|--------|-------------|--------|----------|
| `none` | Monitor only | Deliver email normally, send reports | Initial DMARC deployment, testing |
| `quarantine` | Suspicious | Mark as spam/junk | Transitioning to enforcement |
| `reject` | Strict | Reject email outright | Full DMARC enforcement |

**Alignment Modes:**

**Strict Alignment (`s`)**: Domains must match exactly
```
From: user@example.com
DKIM: d=example.com         ✓ PASS
DKIM: d=mail.example.com    ✗ FAIL
```

**Relaxed Alignment (`r`)**: Organizational domain must match
```
From: user@example.com
DKIM: d=example.com         ✓ PASS
DKIM: d=mail.example.com    ✓ PASS (subdomain okay)
DKIM: d=other.com           ✗ FAIL
```

**DMARC Authentication Flow:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Email Received                                                  │
│ From: user@example.com                                          │
│ MAIL FROM: <user@example.com>                                   │
└─────────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Check SPF                                               │
│ Query: example.com TXT (SPF record)                             │
│ Validate: Does sender IP match SPF?                             │
│ Result: ✓ SPF PASS or ✗ SPF FAIL                               │
└─────────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Check DKIM                                              │
│ Query: <selector>._domainkey.example.com TXT                    │
│ Validate: Does signature verify with public key?                │
│ Result: ✓ DKIM PASS or ✗ DKIM FAIL                             │
└─────────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Check Alignment                                         │
│                                                                 │
│ SPF Alignment:                                                  │
│   MAIL FROM domain vs From header domain                        │
│   user@example.com vs user@example.com → ✓ Aligned             │
│                                                                 │
│ DKIM Alignment:                                                 │
│   DKIM d= domain vs From header domain                          │
│   d=example.com vs example.com → ✓ Aligned                      │
└─────────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: DMARC Evaluation                                        │
│                                                                 │
│ DMARC PASS requires:                                            │
│   (SPF PASS + SPF Aligned) OR (DKIM PASS + DKIM Aligned)       │
│                                                                 │
│ ✓ DMARC PASS: At least one passes                              │
│ ✗ DMARC FAIL: Both fail                                        │
└─────────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Apply Policy                                            │
│ Query: _dmarc.example.com TXT                                   │
│ Response: v=DMARC1; p=reject; pct=100                           │
│                                                                 │
│ If DMARC PASS:                                                  │
│   → Deliver email normally                                      │
│                                                                 │
│ If DMARC FAIL:                                                  │
│   p=none      → Deliver, log failure                            │
│   p=quarantine → Send to spam/junk                              │
│   p=reject    → Reject email (550 error)                        │
└─────────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 6: Send Reports                                            │
│                                                                 │
│ Aggregate Report (rua):                                         │
│   - Daily/periodic XML summary                                  │
│   - Statistics of all authentication results                    │
│   - Sent to rua=mailto:reports@example.com                      │
│                                                                 │
│ Forensic Report (ruf):                                          │
│   - Real-time individual failure reports                        │
│   - Contains redacted email samples                             │
│   - Sent to ruf=mailto:forensic@example.com                     │
└─────────────────────────────────────────────────────────────────┘
```

**DMARC Pass/Fail Logic:**

| SPF | SPF Aligned | DKIM | DKIM Aligned | DMARC Result |
|-----|-------------|------|--------------|--------------|
| ✓ | ✓ | ✓ | ✓ | **PASS** |
| ✓ | ✓ | ✗ | ✗ | **PASS** (SPF sufficient) |
| ✗ | ✗ | ✓ | ✓ | **PASS** (DKIM sufficient) |
| ✓ | ✗ | ✓ | ✗ | **FAIL** (no alignment) |
| ✗ | ✗ | ✗ | ✗ | **FAIL** (both fail) |

**Forensic Options (`fo`):**

| Value | When to Generate Report |
|-------|------------------------|
| `0` | Generate if both SPF and DKIM fail (default) |
| `1` | Generate if either SPF or DKIM fails |
| `d` | Generate if DKIM fails |
| `s` | Generate if SPF fails |

**Example DMARC Aggregate Report (XML):**

```xml
<?xml version="1.0"?>
<feedback>
  <report_metadata>
    <org_name>gmail.com</org_name>
    <email>noreply-dmarc@google.com</email>
    <report_id>12345</report_id>
    <date_range>
      <begin>1737331200</begin>
      <end>1737417600</end>
    </date_range>
  </report_metadata>
  <policy_published>
    <domain>example.com</domain>
    <p>reject</p>
    <sp>reject</sp>
    <pct>100</pct>
  </policy_published>
  <record>
    <row>
      <source_ip>192.0.2.15</source_ip>
      <count>127</count>
      <policy_evaluated>
        <disposition>none</disposition>
        <dkim>pass</dkim>
        <spf>pass</spf>
      </policy_evaluated>
    </row>
    <identifiers>
      <header_from>example.com</header_from>
    </identifiers>
    <auth_results>
      <dkim>
        <domain>example.com</domain>
        <result>pass</result>
      </dkim>
      <spf>
        <domain>example.com</domain>
        <result>pass</result>
      </spf>
    </auth_results>
  </record>
</feedback>
```

**DMARC Deployment Strategy:**

```
Phase 1: Monitoring (p=none)
┌─────────────────────────────────────────┐
│ _dmarc.example.com TXT                  │
│ "v=DMARC1; p=none; rua=mailto:...;"     │
│                                         │
│ Duration: 2-4 weeks                     │
│ Goal: Collect data, identify sources    │
└─────────────────────────────────────────┘
              ▼
Phase 2: Gradual Enforcement (p=quarantine, pct=10)
┌─────────────────────────────────────────┐
│ _dmarc.example.com TXT                  │
│ "v=DMARC1; p=quarantine; pct=10; ..."   │
│                                         │
│ Duration: 2-4 weeks                     │
│ Goal: Test impact on 10% of emails      │
└─────────────────────────────────────────┘
              ▼
Phase 3: Full Quarantine (p=quarantine, pct=100)
┌─────────────────────────────────────────┐
│ _dmarc.example.com TXT                  │
│ "v=DMARC1; p=quarantine; pct=100; ..."  │
│                                         │
│ Duration: 4-8 weeks                     │
│ Goal: Monitor quarantined emails        │
└─────────────────────────────────────────┘
              ▼
Phase 4: Full Rejection (p=reject, pct=100)
┌─────────────────────────────────────────┐
│ _dmarc.example.com TXT                  │
│ "v=DMARC1; p=reject; pct=100; ..."      │
│                                         │
│ Goal: Maximum protection                │
└─────────────────────────────────────────┘
```

**Common DMARC Configurations:**

1. **Monitoring Only:**
   ```
   v=DMARC1; p=none; rua=mailto:dmarc@example.com
   ```

2. **Strict Security:**
   ```
   v=DMARC1; p=reject; rua=mailto:dmarc@example.com; ruf=mailto:forensic@example.com; pct=100; adkim=s; aspf=s
   ```

3. **Subdomain Different Policy:**
   ```
   v=DMARC1; p=reject; sp=quarantine; rua=mailto:dmarc@example.com
   ```

4. **Gradual Rollout:**
   ```
   v=DMARC1; p=quarantine; pct=25; rua=mailto:dmarc@example.com
   ```

**Benefits:**

- **Brand Protection**: Prevent domain spoofing and phishing
- **Visibility**: Reports show who's sending email from your domain
- **Deliverability**: Authenticated emails more likely to reach inbox
- **Compliance**: Required by many organizations (government, finance)

**Common Issues:**

- **Breaking legitimate email**: Forwarding, mailing lists may fail
- **Subdomain inheritance**: Subdomains without DMARC use parent policy
- **Report volume**: Large domains receive many reports
- **Third-party senders**: Must configure SPF/DKIM for all email services

### Cross-Server Email Flow (Gmail to Outlook)

Complete flow when sending email from `user@gmail.com` to `recipient@outlook.com`:

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. User composes email in Gmail                                 │
└──────────────────────────────────────────────────────────────────┘
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│ 2. Gmail MUA sends to Gmail SMTP server (smtp.gmail.com:587)    │
│    - STARTTLS encryption                                         │
│    - Authentication with user credentials                        │
│    - MAIL FROM, RCPT TO, DATA                                    │
└──────────────────────────────────────────────────────────────────┘
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│ 3. Gmail SMTP server processes email                            │
│    - Signs email with DKIM (private key)                         │
│    - Adds SPF information                                        │
│    - Queues email for delivery                                   │
└──────────────────────────────────────────────────────────────────┘
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│ 4. Gmail DNS lookup for recipient domain                        │
│    Query: MX record for outlook.com                              │
│    Response: outlook-com.olc.protection.outlook.com (priority 5) │
└──────────────────────────────────────────────────────────────────┘
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│ 5. Gmail DNS lookup for mail server IP                          │
│    Query: A record for outlook-com.olc.protection.outlook.com    │
│    Response: 104.47.xx.xx                                        │
└──────────────────────────────────────────────────────────────────┘
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│ 6. Gmail SMTP connects to Outlook SMTP (port 25)                │
│    - TLS/STARTTLS encryption                                     │
│    - EHLO gmail.com                                              │
│    - MAIL FROM:<user@gmail.com>                                  │
│    - RCPT TO:<recipient@outlook.com>                             │
│    - DATA (transfers email)                                      │
└──────────────────────────────────────────────────────────────────┘
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│ 7. Outlook SMTP server validates email                          │
│    - SPF check: Is Gmail's IP authorized for gmail.com?          │
│    - DKIM check: Verify signature with Gmail's public key        │
│    - DMARC check: Does email pass SPF/DKIM alignment?            │
│    - Spam filters and content scanning                           │
└──────────────────────────────────────────────────────────────────┘
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│ 8. Outlook accepts or rejects email                             │
│    Pass: 250 OK - Email queued for delivery                      │
│    Fail: 550 - Email rejected                                    │
└──────────────────────────────────────────────────────────────────┘
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│ 9. Outlook MDA delivers to recipient's mailbox                  │
│    - Stores in recipient@outlook.com mailbox                     │
│    - Updates inbox, applies filters/rules                        │
└──────────────────────────────────────────────────────────────────┘
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│ 10. Recipient retrieves email via IMAP/POP3                     │
│     - outlook.com retrieves from mailbox                         │
│     - Email appears in recipient's inbox                         │
└──────────────────────────────────────────────────────────────────┘
```

**Key Points:**

1. **Different protocols**: SMTP for sending, IMAP/POP3 for receiving
2. **DNS is critical**: MX and A records route email to correct server
3. **Authentication layers**: SPF, DKIM, DMARC prevent spoofing
4. **Encryption**: TLS/STARTTLS protects data in transit
5. **Server-to-server**: Port 25, Client-to-server: Port 587
6. **Queuing**: Emails queued at multiple stages for reliability
7. **Retry logic**: If delivery fails, retry with exponential backoff

