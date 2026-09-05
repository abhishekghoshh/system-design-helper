#!/usr/bin/env python3
"""Fix vpn.md: rename headings, add missing sections, update Topics Covered."""

import sys, re
sys.path.insert(0, 'scratchpad')

from enhance_v2 import (
    gen_replication_strategies, gen_failure_detection,
    regenerate_topics_covered,
)

VPN_SYSTEM = {
    'name': 'VPN',
    'brief': 'A Virtual Private Network (VPN) extends a private network across public networks by creating an encrypted tunnel.',
    'key_components': ['VPN gateway/server', 'Tunnel protocol (WireGuard, IPsec, OpenVPN)', 'Authentication server', 'Encryption engine'],
    'main_challenge': 'Balancing strong security with acceptable performance and user-friendly configuration',
    'restricted': 'user credentials, private network topology, session tokens',
    'non_restricted': 'public endpoint addresses, anonymized traffic statistics, system health status',
    'real_world': ['NordVPN', 'ExpressVPN', 'OpenVPN', 'WireGuard', 'AWS Client VPN'],
    'java_focus': 'VPN session management, tunnel establishment, and authentication flows using Spring Security',
}

filepath = 'docs/system-design/high-level/designing/basic/vpn.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Step 1: Rename headings
content = content.replace('### Encryption and Key Exchange', '### Encryption and Key Management')
content = content.replace('### Real-World VPN Implementations', '### Real-World Implementations')

# Step 2: Generate and insert missing sections before Java section
gen_data_model_and_api_vpn = """### Data Model and API

**VPN data model**

```mermaid
erDiagram
    USER ||--o{ VPN_SESSION : has
    USER {
        string userId PK
        string username
        string email
    }
    VPN_SESSION {
        string sessionId PK
        string userId FK
        string tunnelProtocol
        string serverEndpoint
        datetime createdAt
        datetime expiresAt
    }
    SERVER {
        string serverId PK
        string endpoint
        string region
        string publicKey
    }
    VPN_SESSION }o--|| SERVER : connects_to
    CERTIFICATE {
        string certId PK
        string userId FK
        string certData
        datetime issuedAt
        datetime expiresAt
    }
    USER ||--o{ CERTIFICATE : holds
```

**Entities**

- **User**: Stores credentials, authentication state, and assigned VPN profile.
- **VPN Session**: Tracks active tunnel connections, including protocol, server endpoint, and expiration time.
- **Server**: Represents a VPN gateway with endpoint address, region, and public key.
- **Certificate**: Manages client certificates issued for mutual TLS authentication.

**API contract**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/login` | Authenticate user and issue session token |
| `POST` | `/api/v1/vpn/connect` | Request a VPN tunnel to a specific server |
| `DELETE` | `/api/v1/vpn/disconnect` | Terminate an active VPN session |
| `GET` | `/api/v1/vpn/servers` | List available VPN servers (region-filtered) |
| `POST` | `/api/v1/cert/request` | Request a client certificate for mTLS |

**Typical response**

```json
{
  "sessionId": "sess_abc123",
  "server": {
    "endpoint": "10.0.1.5:51820",
    "region": "us-east-1",
    "protocol": "wireguard"
  },
  "config": "base64-encoded-wireguard-config",
  "expiresAt": "2026-09-05T00:00:00Z"
}
```"""

all_sections = '\n\n'.join([
    gen_data_model_and_api_vpn.rstrip(),
    gen_replication_strategies(VPN_SYSTEM).rstrip(),
    gen_failure_detection(VPN_SYSTEM).rstrip(),
])

java_marker = '### Java and Spring Boot Implementation Guide'
idx = content.find(java_marker)
if idx == -1:
    print("ERROR: Cannot find Java section")
    sys.exit(1)

insert_point = content.rfind('\n\n', 0, idx)
if insert_point == -1:
    insert_point = content.rfind('\n', 0, idx)

content = content[:insert_point + 2] + all_sections + '\n\n' + content[insert_point + 2:]

# Step 3: Write the file
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# Step 4: Regenerate Topics Covered
regenerate_topics_covered(filepath)

# Step 5: Verify
with open(filepath, 'r', encoding='utf-8') as f:
    final_content = f.read()

fences = final_content.count('```')
print(f"Lines: {len(final_content.splitlines())}")
print(f"Fences: {fences} ({'balanced' if fences % 2 == 0 else 'UNBALANCED'})")

CANONICAL_TOPICS = [
    "Introduction", "Characteristics", "Pros", "Cons", "Use Cases",
    "Components", "Architectural Patterns", "Benefits", "Challenges",
    "Best Practices", "When to Use", "Data Model and API",
    "Replication Strategies", "Failure Detection and Membership",
    "High Availability and Scalability", "Performance and Optimization",
    "CAP Theorem and Consistency Trade-offs", "Encryption and Key Management",
    "Authentication and Authorization", "Security Threats and Mitigations",
    "Observability and Logging", "Real-World Implementations",
    "Java and Spring Boot Implementation Guide", "Interview Questions and Answers",
]

def normalize(s):
    return re.sub(r'\s+', ' ', s.strip().lower())

headings = []
for line in final_content.splitlines():
    m = re.match(r'^###\s+(.+)', line)
    if m:
        headings.append(m.group(1).strip())
heading_norms = [normalize(h) for h in headings]

missing = []
for topic in CANONICAL_TOPICS:
    tn = normalize(topic)
    if not any(tn in hn or hn in tn for hn in heading_norms):
        missing.append(topic)

print(f"Missing: {len(missing)}")
if missing:
    for m in missing:
        print(f"  ❌ {m}")
else:
    print("  All canonical topics present!")
print("Done!")
