#!/usr/bin/env python3
"""Update the advanced todo.md file status table with current line counts."""

import os, re

ADVANCED_DIR = '/Users/abhishekghosh/Desktop/projects/personal/system-design-helper/docs/system-design/high-level/designing/advanced'
TODO = os.path.join(ADVANCED_DIR, 'todo.md')

def normalize(s):
    return re.sub(r'\s+', ' ', s.strip().lower())

CANONICAL_TOPICS = [
    "Introduction", "Characteristics", "Pros", "Cons", "Use Cases",
    "Components", "Architectural Patterns", "Benefits", "Challenges",
    "Best Practices", "When to Use / When Not to Use", "Data Model and API",
    "Replication Strategies", "Failure Detection and Membership",
    "High Availability and Scalability", "Performance and Optimization",
    "CAP Theorem and Consistency Trade-offs", "Encryption and Key Management",
    "Authentication and Authorization", "Security Threats and Mitigations",
    "Observability and Logging", "Real-World Implementations",
    "Java and Spring Boot Implementation Guide", "Interview Questions and Answers",
]

def audit_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    line_count = len(lines)

    # Headings
    headings = []
    for line in lines:
        m = re.match(r'^###\s+(.+)', line)
        if m:
            headings.append(m.group(1).strip())
    heading_norms = [normalize(h) for h in headings]

    # Canonical topics
    missing = []
    for topic in CANONICAL_TOPICS:
        tn = normalize(topic)
        if not any(tn in hn or hn in tn for hn in heading_norms):
            missing.append(topic)
    missing_count = len(missing)

    # Topics Covered
    has_topics = any("topics covered" in hn for hn in heading_norms)

    # Java
    has_java = any("java and spring boot" in hn for hn in heading_norms) or \
               any(re.match(r'^##+\s+.*Java and Spring Boot', line) for line in lines)

    # Interview
    has_interview = any("interview" in hn for hn in heading_norms) or \
                    any(re.match(r'^##+\s+.*Interview', line) for line in lines)

    # Fences
    fence_count = sum(1 for line in lines if line.startswith('```'))
    fences_balanced = (fence_count % 2 == 0)

    # TBD
    tbd = len(re.findall(r'\b(tbd|todo)\b', content, re.IGNORECASE))

    return {
        'lines': line_count,
        'missing': missing_count,
        'topics': '✅' if has_topics else '❌',
        'java': '✅' if has_java else '❌',
        'interview': '✅' if has_interview else '❌',
        'fences': '✅' if fences_balanced else '⚠️',
        'tbd': str(tbd) if tbd else '✅',
        'status': '✅' if missing_count == 0 and has_topics and has_java and has_interview and fences_balanced and tbd == 0 else '⚠️',
    }

# Read current todo.md
with open(TODO, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the table header and rows
lines = content.split('\n')
table_start = None
table_end = None
for i, line in enumerate(lines):
    if 'File | Lines' in line and 'Lines' in line:
        table_start = i
    if table_start is not None and i > table_start:
        if line.strip() == '' or line.startswith('---') or not line.startswith('|'):
            if table_end is None and line.strip() == '':
                table_end = i
                break

if table_start is None:
    print("ERROR: Could not find table header")
    exit(1)

if table_end is None:
    table_end = len(lines)

print(f"Table found at lines {table_start+1} to {table_end}")

# Get all .md files except todo.md
files = sorted([f for f in os.listdir(ADVANCED_DIR) if f.endswith('.md') and f != 'todo.md'])

# Generate new table rows
header = lines[table_start]
separator = lines[table_start + 1]

new_rows = []
for fname in files:
    filepath = os.path.join(ADVANCED_DIR, fname)
    result = audit_file(filepath)
    
    tbd_display = result['tbd'] if result['tbd'] != '✅' else '✅'
    
    row = f"| {fname} | {result['lines']} | {result['missing']} | {result['topics']} | {result['java']} | {result['interview']} | {result['fences']} | {tbd_display} | {result['missing']}/24 | {result['status']} |"
    new_rows.append(row)

# Rebuild the content
new_lines = lines[:table_start] + [header, separator] + new_rows
if table_end < len(lines):
    new_lines += [''] + lines[table_end+1:]

new_content = '\n'.join(new_lines)

with open(TODO, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Updated {len(new_rows)} table rows in todo.md")
