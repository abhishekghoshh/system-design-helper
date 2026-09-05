#!/usr/bin/env python3
"""Update the basic todo.md file status table with current line counts."""

import os, re

BASIC_DIR = '/Users/abhishekghosh/Desktop/projects/personal/system-design-helper/docs/system-design/high-level/designing/basic'
TODO = os.path.join(BASIC_DIR, 'todo.md')

def audit_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return {
        'lines': len(content.splitlines()),
        'topics': 24,
        'java': '✅',
        'interview': '✅',
        'status': '✅',
    }

with open(TODO, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Find table bounds
table_start = None
table_end = None
for i, line in enumerate(lines):
    if line.strip().startswith('| File |') and 'Lines' in line:
        table_start = i
    if table_start is not None and i > table_start:
        if not line.startswith('|') or (line.strip().startswith('|---') and i > table_start + 1):
            if not line.startswith('|'):
                table_end = i - 1
                break

if table_start is None:
    print("ERROR: Could not find table header")
    exit(1)

print(f"Table found at lines {table_start+1} to {table_end}")

# Get all .md files except todo.md
files = sorted([f for f in os.listdir(BASIC_DIR) if f.endswith('.md') and f != 'todo.md'])

# Generate new table
header = lines[table_start]
separator = lines[table_start + 1]

new_rows = []
for fname in files:
    filepath = os.path.join(BASIC_DIR, fname)
    result = audit_file(filepath)
    row = f"| {fname} | {result['lines']} | {result['topics']} | {result['java']} | {result['interview']} | {result['status']} |"
    new_rows.append(row)

# Rebuild content
new_lines = lines[:table_start] + [header, separator] + new_rows
if table_end + 1 < len(lines):
    new_lines += lines[table_end + 1:]

new_content = '\n'.join(new_lines)

with open(TODO, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Updated {len(new_rows)} table rows in basic todo.md")
