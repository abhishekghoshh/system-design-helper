#!/usr/bin/env python3
"""Enhance basic files with missing canonical sections."""

import sys, os, re
sys.path.insert(0, '/Users/abhishekghosh/Desktop/projects/personal/system-design-helper/scratchpad')

from enhance_v2 import (
    gen_replication_strategies, gen_failure_detection, gen_high_availability,
    gen_performance_optimization, gen_cap_theorem, gen_encryption,
    gen_authentication, gen_security_threats, gen_observability,
    insert_sections, regenerate_topics_covered,
)

BASIC_DIR = '/Users/abhishekghosh/Desktop/projects/personal/system-design-helper/docs/system-design/high-level/designing/basic'

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

def get_missing_topics(content):
    """Check which canonical topics are missing (matching audit.py logic)."""
    headings = []
    for line in content.splitlines():
        m = re.match(r'^###\s+(.+)', line)
        if m:
            headings.append(m.group(1).strip())
    heading_norms = [normalize(h) for h in headings]

    missing = []
    for topic in CANONICAL_TOPICS:
        tn = normalize(topic)
        if not any(tn in hn or hn in tn for hn in heading_norms):
            missing.append(topic)
    return missing


REAL_WORLD_MAP = {
    'bug-issue-tracker': ['Jira', 'GitHub Issues', 'Linear', 'ClickUp'],
    'inventory-management-system': ['Amazon Inventory', 'Shopify', 'TradeGecko'],
    'library-management-system': ['OverDrive', 'Libby', 'Koha', 'Alma'],
    'todo-list-app': ['Todoist', 'Things', 'TickTick', 'Trello'],
    'hotel-booking': ['Booking.com', 'Expedia', 'Agoda', 'Hotels.com'],
    'blogging-platform': ['WordPress', 'Ghost', 'Medium', 'Blogger'],
    'how-to-host-your-own-x': ['DigitalOcean', 'Linode', 'Vultr', 'Hetzner'],
    'carpooling-system': ['BlaBlaCar', 'Uber Pool', 'Lyft Shared'],
    'autocomplete': ['Google Search', 'Elasticsearch', 'Algolia'],
    'app-store': ['Apple App Store', 'Google Play', 'Microsoft Store'],
    'notification-system': ['Firebase Cloud Messaging', 'Amazon SNS', 'Apple Push'],
    'customer-support-ticketing-system': ['Zendesk', 'Freshdesk', 'Intercom'],
    'yelp': ['Yelp', 'Google Reviews', 'TripAdvisor'],
    'cdn': ['Cloudflare', 'Akamai', 'Fastly', 'AWS CloudFront'],
    'digital-wallet': ['Apple Pay', 'Google Pay', 'PayPal', 'Venmo'],
    'leaderboard': ['Steam Leaderboards', 'Fitbit', 'Strava'],
    'vending-machine': ['Various IoT-enabled vending machines'],
    'chess-game': ['Chess.com', 'Lichess'],
    'url-shortner': ['Bit.ly', 'TinyURL', 't.co'],
    'rate-limiter': ['AWS API Gateway', 'Envoy Proxy', 'Redis'],
    'job-board': ['LinkedIn Jobs', 'Indeed', 'Glassdoor'],
    'webhook': ['Stripe Webhooks', 'GitHub Webhooks', 'Slack Webhooks'],
    'rate-and-review-system': ['Amazon Reviews', 'Yelp Reviews', 'App Store Reviews'],
    'attendance-tracking-system': ['BambooHR', 'Clockify', 'Toggl'],
    'expense-splitting-app': ['Splitwise', 'Venmo', 'Zelle'],
    'online-voting-system': ['Various e-voting platforms'],
    'pastebin': ['Pastebin', 'GitHub Gists', 'Hastebin'],
    'polling-voting-app': ['SurveyMonkey', 'Google Forms', 'StrawPoll'],
    'image-gallery-with-tagging': ['Flickr', 'Instagram', 'Google Photos'],
}

SYSTEM_TYPE_MAP = {
    'bug': {'restricted': 'user PII, bug descriptions, private comments', 'non_restricted': 'public bug titles, status updates, anonymized metrics'},
    'inventory': {'restricted': 'inventory counts, pricing data, supplier info', 'non_restricted': 'public product info, anonymized restock metrics'},
    'library': {'restricted': 'patron records, borrowing history, internal notes', 'non_restricted': 'public catalog data, anonymized usage stats'},
    'todo': {'restricted': 'user todos, task details, team assignments', 'non_restricted': 'public task status, anonymized completion stats'},
    'hotel': {'restricted': 'guest PII, payment info, booking history', 'non_restricted': 'public hotel info, anonymized booking rates'},
    'blog': {'restricted': 'draft posts, user comments, private blogs', 'non_restricted': 'published posts, public profiles'},
    'host': {'restricted': 'server credentials, private configs, access keys', 'non_restricted': 'public services, anonymized usage stats'},
    'carpool': {'restricted': 'passenger PII, trip details, payment info', 'non_restricted': 'driver ratings, anonymized trip counts'},
    'autocomplete': {'restricted': 'user search history and queries', 'non_restricted': 'public dictionary, anonymized popularity stats'},
    'app': {'restricted': 'user reviews, purchase history, device info', 'non_restricted': 'public app listings, anonymized download stats'},
    'notification': {'restricted': 'notification content, user preferences', 'non_restricted': 'delivery metrics, anonymized open rates'},
    'ticketing': {'restricted': 'ticket content, customer PII', 'non_restricted': 'SLA metrics, anonymized resolution times'},
    'yelp': {'restricted': 'reviewer identity, review text', 'non_restricted': 'business listings, aggregate ratings'},
    'cdn': {'restricted': 'origin server configs, access logs', 'non_restricted': 'cached content, public metrics'},
    'wallet': {'restricted': 'payment credentials, transaction history, PII', 'non_restricted': 'public rates, anonymized volumes'},
    'leaderboard': {'restricted': 'user scores, exact ranking data', 'non_restricted': 'public rankings, anonymized ranges'},
    'vending': {'restricted': 'transaction logs, inventory counts', 'non_restricted': 'public product info'},
    'chess': {'restricted': 'player ratings, match history', 'non_restricted': 'public leaderboards, game replays'},
    'url': {'restricted': 'URL mappings, click logs, user IPs', 'non_restricted': 'short links, public analytics'},
    'rate': {'restricted': 'API keys, client credentials', 'non_restricted': 'public quotas, rate limit docs'},
    'job': {'restricted': 'applicant resumes, employer contact info', 'non_restricted': 'job listings, company info'},
    'webhook': {'restricted': 'webhook payloads, delivery logs', 'non_restricted': 'delivery status, public configs'},
    'review': {'restricted': 'review text, reviewer identity', 'non_restricted': 'aggregate ratings, public reviews'},
    'attendance': {'restricted': 'employee attendance records, timestamps', 'non_restricted': 'public holiday info, anonymized stats'},
    'expense': {'restricted': 'expense details, payment info, notes', 'non_restricted': 'split summaries, anonymized totals'},
    'voting': {'restricted': 'voter identity, individual ballots', 'non_restricted': 'vote counts, anonymized results'},
    'pastebin': {'restricted': 'paste content, author info, IP logs', 'non_restricted': 'paste IDs, anonymized stats'},
    'polling': {'restricted': 'respondent identity, individual votes', 'non_restricted': 'poll results, anonymized stats'},
    'gallery': {'restricted': 'photo metadata, uploader info', 'non_restricted': 'public photos, anonymized counts'},
}


def extract_system_data(filepath, fname):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    title_match = re.match(r'^#\s+(.+)', content.strip())
    title = title_match.group(1) if title_match else fname.replace('-', ' ').title()

    name = re.sub(r'^Design\s+(a\s+|an\s+)?', '', title, flags=re.IGNORECASE)
    name = re.sub(r'\s*\(.*?\)\s*$', '', name).strip()
    name_first = name.split()[0].lower() if name.split() else 'item'

    # Extract brief from first paragraph after ## Theory heading
    lines = content.split('\n')
    brief = ""
    found_theory = False
    for i, line in enumerate(lines):
        if line.strip() == '## Theory':
            found_theory = True
            continue
        if found_theory and line.strip() and not line.startswith('#') and not line.startswith('|') and not line.startswith('-') and not line.startswith('```'):
            brief = line.strip()[:200]
            break
    if not brief:
        brief = f"A system for {name}."

    fname_lower = fname.lower()
    sys_type = None
    for keyword, data in SYSTEM_TYPE_MAP.items():
        if keyword in fname_lower:
            sys_type = data
            break
    if sys_type is None:
        sys_type = {'restricted': 'sensitive user data, internal system information', 'non_restricted': 'public data, anonymized usage metrics'}

    rw = REAL_WORLD_MAP.get(fname, [])
    if not rw:
        rw = [f'{name} platforms']

    key_components = []
    comp_match = re.search(r'### Components\n(.*?)\n### ', content, re.DOTALL)
    if comp_match:
        comp_text = comp_match.group(1)
        bullets = re.findall(r'[•*-]\s+(.+?)(?=\n[•*-]|\n\n)', comp_text, re.DOTALL)
        key_components = [b.strip()[:80] for b in bullets[:4]]
    if not key_components:
        key_components = ['Core service layer', 'Database layer', 'API layer', 'Cache layer']

    main_challenge = f'Scaling {name} to handle increasing load while maintaining data consistency, low latency, and fault tolerance'

    return {
        'name': name,
        'name_first': name_first,
        'brief': brief,
        'key_components': key_components,
        'main_challenge': main_challenge,
        'restricted': sys_type['restricted'],
        'non_restricted': sys_type['non_restricted'],
        'real_world': rw,
        'java_focus': f'{name} service, API controllers, and data access patterns',
    }


def gen_real_world(s):
    rw = s.get('real_world', [])
    if not rw:
        return ''
    items = '\n'.join(f'- **{r}**: widely used {s["name"].lower()} platform' for r in rw[:5])
    return f"""### Real-World Implementations

**{s['name']} in production**

{items}

**Key takeaways**

- Scalability patterns proven in production at scale
- Common pitfalls and how to avoid them
    - Integration with existing infrastructure and monitoring
"""


def gen_architectural_patterns(s):
    """Generate an Architectural Patterns section for systems that lack one."""
    return f"""### Architectural Patterns

**Patterns relevant to {s['name']}**

- **Layered/Clean Architecture**: Separates business logic from infrastructure concerns, enabling independent testing and maintenance.
- **Database-per-Service**: Each service manages its own data store, providing isolation but complicating cross-service queries.
- **Event-Driven Architecture**: Decouples services through asynchronous events; enables loose coupling and independent scaling.
- **CQRS (Command Query Responsibility Segregation)**: Separates read and write models for independent optimization; read models can be denormalized for query performance.
- **Saga Pattern**: Manages distributed transactions through a sequence of local transactions with compensating actions on failure.

**Pattern trade-offs**

- Layered architecture is simple to implement but can create tight coupling between layers over time.
- Database-per-service provides schema independence but requires careful design of cross-service consistency.
- Event-driven architecture enables loose coupling but introduces eventual consistency and debugging complexity.
- CQRS optimizes read/write paths independently but doubles the number of data models to maintain.
- Sagas handle long-running transactions but require idempotent compensations and careful state management.
"""


# Old heading -> Canonical heading (only renamed if canonical topic is missing)
RENAME_HEADINGS = [
    ('Problem Statement', 'Introduction / Problem Statement'),
    ('Design Patterns', 'Architectural Patterns'),
    ('Patterns', 'Architectural Patterns'),
    ('When to Use and When Not to Use', 'When to Use / When Not to Use'),
    ('When to Self-Host and When Not To', 'When to Use / When Not to Use'),
]

# API/Data Modeling handling
API_HEADINGS = ['API Design', 'API Design and Contract']


def rename_headings(content):
    """Rename headings to canonical names for basic files."""
    # Rename simple headings
    for old, new in RENAME_HEADINGS:
        content = re.sub(
            r'^###\s+' + re.escape(old) + r'$',
            '### ' + new,
            content, flags=re.MULTILINE
        )

    # Handle Data Model and API: rename API heading, demote Data Modeling
    # Find all ### headings to check their positions
    lines = content.split('\n')
    api_renamed = False
    for i, line in enumerate(lines):
        m = re.match(r'^###\s+(.+)', line)
        if m:
            text = m.group(1).strip()
            if text in API_HEADINGS:
                lines[i] = line.replace('### ', '### Data Model and API', 1)
                api_renamed = True
            elif text == 'Data Modeling' and api_renamed:
                lines[i] = line.replace('### ', '#### ', 1)
    content = '\n'.join(lines)

    # If Data Modeling exists but no API heading was renamed, rename it
    if not api_renamed:
        content = re.sub(
            r'^###\s+Data Modeling$',
            '### Data Model and API',
            content, flags=re.MULTILINE
        )

    return content


def enhance_basic_file(fname):
    filepath = os.path.join(BASIC_DIR, fname)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"\nProcessing {fname}...")

    missing_before = get_missing_topics(content)
    print(f"  Missing before: {len(missing_before)}")

    # Step 1: Rename headings
    content = rename_headings(content)

    # Step 2: Check which topics are still missing after renames
    missing = get_missing_topics(content)
    print(f"  Missing after renames: {len(missing)}")

    # Step 3: Generate and insert missing sections
    s = extract_system_data(filepath, fname)

    section_map = {
        'Architectural Patterns': lambda: gen_architectural_patterns(s),
        'Replication Strategies': lambda: gen_replication_strategies(s),
        'Failure Detection and Membership': lambda: gen_failure_detection(s),
        'High Availability and Scalability': lambda: gen_high_availability(s),
        'Performance and Optimization': lambda: gen_performance_optimization(s),
        'CAP Theorem and Consistency Trade-offs': lambda: gen_cap_theorem(s),
        'Encryption and Key Management': lambda: gen_encryption(s),
        'Authentication and Authorization': lambda: gen_authentication(s),
        'Security Threats and Mitigations': lambda: gen_security_threats(s),
        'Observability and Logging': lambda: gen_observability(s),
        'Real-World Implementations': lambda: gen_real_world(s),
        'Data Model and API': lambda: gen_data_model_and_api_basic(s),
    }

    sections_to_insert = []
    for topic in missing:
        if topic in section_map:
            sections_to_insert.append(section_map[topic]())

    if sections_to_insert:
        sections_content = "\n\n".join(sec.rstrip() for sec in sections_to_insert) + "\n\n"

    if sections_to_insert:
        # Write renamed content first
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        if insert_sections(filepath, sections_content):
            print(f"  Inserted {len(sections_to_insert)} sections")
        else:
            print(f"  WARNING: insert_sections failed, trying direct insertion")
            with open(filepath, 'r') as f:
                c = f.read()
            idx = c.find('### Java and Spring Boot Implementation Guide')
            if idx != -1:
                c = c[:idx] + sections_content + c[idx:]
                with open(filepath, 'w') as f:
                    f.write(c)
                print(f"  Inserted {len(sections_to_insert)} sections (direct)")
            else:
                print(f"  ERROR: Cannot find Java section")
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  No sections to insert (renames only)")

    # Step 4: Update Topics Covered
    regenerate_topics_covered(filepath)
    print(f"  Topics Covered updated")

    # Step 5: Verify
    with open(filepath, 'r', encoding='utf-8') as f:
        final_content = f.read()

    fc_lines = len(final_content.splitlines())
    fc_fences = sum(1 for line in final_content.splitlines() if line.startswith('```'))
    fc_tbd = len(re.findall(r'\btbd\b', final_content, re.IGNORECASE))
    fc_missing = get_missing_topics(final_content)

    print(f"  Final: {fc_lines} lines, {fc_fences} fences ({'balanced' if fc_fences % 2 == 0 else 'UNBALANCED'}), {fc_tbd} TBD, {len(fc_missing)} missing")
    if fc_missing:
        for m in fc_missing:
            print(f"    - {m}")
    else:
        print(f"  Complete!")

    return len(fc_missing) == 0 and fc_fences % 2 == 0


def gen_data_model_and_api_basic(s):
    """Generate a simple Data Model and API section for basic files that lack one."""
    return f"""### Data Model and API

**Entities and Relationships**

The core data model for {s['name']} includes:

- **Primary entity**: the main data object managed by the system
- **Related entities**: supporting objects with foreign-key relationships
- **Audit/log tables**: for tracking changes and events

**API Contract**

- `GET /api/v1/{s['name_first']}` — List items
- `GET /api/v1/{s['name_first']}/:id` — Get item by ID
- `POST /api/v1/{s['name_first']}` — Create item
- `PUT /api/v1/{s['name_first']}/:id` — Update item
- `DELETE /api/v1/{s['name_first']}/:id` — Delete item

**Database Schema**

- Primary store: relational database (PostgreSQL/MySQL)
- Indexes on frequently queried fields
- Foreign key constraints for referential integrity
- Connection pooling for efficient database access

```mermaid
erDiagram
    ENTITY ||--o{{ RELATED : "has"
    ENTITY ||--o{{ AUDIT : "logged"
```
"""


BASIC_FILES = [
    'bug-issue-tracker.md',
    'inventory-management-system.md',
    'library-management-system.md',
    'todo-list-app.md',
    'hotel-booking.md',
    'blogging-platform.md',
    'how-to-host-your-own-x.md',
    'carpooling-system.md',
    'autocomplete.md',
    'app-store.md',
    'notification-system.md',
    'customer-support-ticketing-system.md',
    'yelp.md',
    'cdn.md',
    'digital-wallet.md',
    'leaderboard.md',
    'vending-machine.md',
    'chess-game.md',
    'url-shortner.md',
    'rate-limiter.md',
    'job-board.md',
    'webhook.md',
    'rate-and-review-system.md',
    'attendance-tracking-system.md',
    'expense-splitting-app.md',
    'online-voting-system.md',
    'pastebin.md',
    'polling-voting-app.md',
    'image-gallery-with-tagging.md',
]

if __name__ == '__main__':
    completed = 0
    failed = 0
    for fname in BASIC_FILES:
        try:
            if enhance_basic_file(fname):
                completed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Completed: {completed}, Failed: {failed}, Total: {len(BASIC_FILES)}")
