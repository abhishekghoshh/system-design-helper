#!/usr/bin/env python3
"""Restructure multi-region-deployment-system.md from old ## format to canonical ### format."""
import re, os

ADVANCED_DIR = "/Users/abhishekghosh/Desktop/projects/personal/system-design-helper/docs/system-design/high-level/designing/advanced"
filepath = os.path.join(ADVANCED_DIR, "multi-region-deployment-system.md")

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Rename ## content headings to ### and fix canonical names
renames = {
    '## Characteristics': '### Characteristics',
    '## Components': '### Components',
    '## Patterns': '### Architectural Patterns',
    '## Benefits': '### Benefits',
    '## Pros': '### Pros',
    '## Cons': '### Cons',
    '## Challenges': '### Challenges',
    '## Best Practices': '### Best Practices',
    '## When to Use': '### When to Use / When Not to Use',
    '## Use Cases': '### Use Cases',
    '## Architecture': '### Architecture',
    '## High-Level Design': '### High-Level Design',
    '## Deep Dive': '### Deep Dive',
    '## API Contract': '### API Contract',
    '## Data Modeling': '### Data Model and API',
    '## Java and Spring Boot Implementation': '### Java and Spring Boot Implementation Guide',
    '## Real-World Examples': '### Real-World Implementations',
    '## Interview Preparation': '### Interview Questions and Answers',
}
for old, new in renames.items():
    content = content.replace(old, new)

# 2. Demote Introduction sub-sections to ####
for h in ['What Is It?', 'Why Does It Exist?', 'What Problem Does It Solve?',
          'Problem Statement', 'Functional Requirements', 'Non-Functional Requirements']:
    content = content.replace(f'### {h}', f'#### {h}')

# 3. Demote Challenges sub-sections to ####
for h in ['Technical Challenges', 'Scalability Challenges', 'Performance Challenges',
          'Reliability Challenges', 'Maintainability Challenges', 'Security Concerns']:
    content = content.replace(f'### {h}', f'#### {h}')

# 4. Demote pattern sub-sections to ####
content = content.replace('### GeoDNS + Home Region Routing', '#### GeoDNS + Home Region Routing')
content = content.replace('### Regional Data Isolation', '#### Regional Data Isolation')

# 5. Remove ### Important Subtopics section (heading + numbered list + mermaid)
# Remove from ### Important Subtopics to the next #### or ### heading
content = re.sub(
    r'\n### Important Subtopics\n.*?(?=\n#### |\n### |\n---|\n## |\Z)',
    '\n---\n',
    content,
    count=1,
    flags=re.DOTALL
)

# 6. Add ### Introduction / Problem Statement before #### What Is It?
content = content.replace(
    '#### What Is It?',
    '### Introduction / Problem Statement\n\n#### What Is It?',
    1
)

# 7. Add --- separator between Topics Covered and Introduction if not present
# (gen_topics.py may not have added it)
if '### Topics Covered' in content and '### Introduction / Problem Statement' in content:
    # Check if there's a --- separator between them
    tc_idx = content.find('### Topics Covered')
    intro_idx = content.find('### Introduction / Problem Statement')
    between = content[tc_idx + len('### Topics Covered'):intro_idx]
    if '---' not in between:
        content = content[:intro_idx] + '---\n\n' + content[intro_idx:]

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. File restructured.")
print(f"Total lines: {len(content.splitlines())}")

# Show all ### headings
h3 = [m.group(1) for line in content.split('\n') if (m := re.match(r'^###\s+(.+)', line))]
print(f"Level 3 headings: {len(h3)}")
for h in h3:
    print(f"  ### {h}")
