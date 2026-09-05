#!/usr/bin/env python3
"""
Escape { and } in Java code blocks within f-strings.
Uses placeholder approach to avoid double-escaping already-escaped {{ }}.
Only processes lines between ```java and ``` markers.
"""
filepath = "/Users/abhishekghosh/Desktop/projects/personal/system-design-helper/scratchpad/enhance_files.py"
with open(filepath, 'r') as f:
    lines = f.readlines()

in_java = False
output = []
changes = 0

for line in lines:
    stripped = line.strip()
    if stripped == '```java' or stripped.startswith('```java'):
        in_java = True
        output.append(line)
        continue
    if stripped == '```' and in_java:
        in_java = False
        output.append(line)
        continue

    if in_java:
        s = line
        # Save already-escaped braces, escape lone ones, restore
        s = s.replace('{{', '\x00').replace('}}', '\x01')
        s = s.replace('{', '{{').replace('}', '}}')
        s = s.replace('\x00', '{{').replace('\x01', '}}')
        if s != line:
            changes += 1
            if changes <= 3:
                print(f"  Changed: {line.rstrip()} -> {s.rstrip()}")
        output.append(s)
    else:
        output.append(line)

with open(filepath, 'w') as f:
    f.writelines(output)

print(f"Done. {changes} lines with brace changes.")
