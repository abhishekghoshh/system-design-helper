#!/usr/bin/env python3
"""
Fix f-string brace escaping in enhance_v2.py for Java code blocks.
Same approach as fix_braces.py but targets enhance_v2.py.
Only processes lines between ```java and ``` markers.
"""
filepath = "/Users/abhishekghosh/Desktop/projects/personal/system-design-helper/scratchpad/enhance_v2.py"
with open(filepath, 'r') as f:
    lines = f.readlines()

in_java = False
in_fstring = False
output = []
changes = 0

for line in lines:
    stripped = line.strip()
    # Track if we're inside a Java code block
    if stripped.startswith('```java') or stripped == '```java':
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
        output.append(s)
    else:
        output.append(line)

with open(filepath, 'w') as f:
    f.writelines(output)

print(f"Done. {changes} lines with brace changes.")
