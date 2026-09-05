#!/usr/bin/env python3
"""
For each file in the advanced directory that is missing a Topics Covered section,
generate the Topics Covered list and insert it after ## Theory.
Also print the missing canonical sections per file.
"""
import os, re

ADVANCED_DIR = "/Users/abhishekghosh/Desktop/projects/personal/system-design-helper/docs/system-design/high-level/designing/advanced"

def slugify(text):
    """Generate GitHub/MkDocs-style anchor slug from heading text."""
    # Lowercase
    s = text.lower().strip()
    # Remove anything that's not a letter, number, space, or hyphen
    s = re.sub(r'[^\w\s-]', '', s)
    # Replace spaces with hyphens
    s = re.sub(r'[\s]+', '-', s)
    # Collapse multiple hyphens
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

def get_h3_headings(content):
    """Extract all ### level headings (text only)."""
    headings = []
    for line in content.splitlines():
        m = re.match(r'^###\s+(.+)', line)
        if m:
            headings.append(m.group(1).strip())
    return headings

def generate_topics_covered(headings):
    """Generate Topics Covered markdown list with anchor links."""
    lines = []
    for i, h in enumerate(headings, 1):
        slug = slugify(h)
        lines.append(f"{i}. [{h}](#{slug})")
    return "\n".join(lines)

# Process all .md files (skip todo.md)
for fname in sorted(os.listdir(ADVANCED_DIR)):
    if not fname.endswith('.md') or fname == 'todo.md':
        continue
    filepath = os.path.join(ADVANCED_DIR, fname)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if Topics Covered already exists
    if '### Topics Covered' in content:
        print(f"SKIP (has Topics Covered): {fname}")
        continue

    headings = get_h3_headings(content)
    if not headings:
        print(f"SKIP (no headings): {fname}")
        continue

    topics_covered = generate_topics_covered(headings)
    
    # Find insertion point: after "## Theory"
    pattern = '## Theory\n\n'
    replacement = f'## Theory\n\n### Topics Covered\n\n{topics_covered}\n\n'
    
    if pattern in content:
        new_content = content.replace(pattern, replacement, 1)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"INSERTED Topics Covered ({len(headings)} items): {fname}")
    else:
        # Try alternative patterns
        pattern2 = '## Theory\n'
        if pattern2 in content:
            new_content = content.replace(pattern2, replacement, 1)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"INSERTED Topics Covered (alt pattern, {len(headings)} items): {fname}")
        else:
            print(f"ERROR: Could not find ## Theory in: {fname}")
            print(f"  First 5 headings: {headings[:5]}")
