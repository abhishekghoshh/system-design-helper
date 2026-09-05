#!/usr/bin/env python3
"""
Audit all .md files in a directory for canonical topic completeness.
Output: file stats + missing canonical topics per file.
"""
import os, re, sys

ADVANCED_DIR = "/Users/abhishekghosh/Desktop/projects/personal/system-design-helper/docs/system-design/high-level/designing/advanced"
BASIC_DIR = "/Users/abhishekghosh/Desktop/projects/personal/system-design-helper/docs/system-design/high-level/designing/basic"

CANONICAL_TOPICS = [
    "Introduction",
    "Characteristics",
    "Pros",
    "Cons",
    "Use Cases",
    "Components",
    "Architectural Patterns",
    "Benefits",
    "Challenges",
    "Best Practices",
    "When to Use",
    "Data Model and API",
    "Replication Strategies",
    "Failure Detection and Membership",
    "High Availability and Scalability",
    "Performance and Optimization",
    "CAP Theorem and Consistency Trade-offs",
    "Encryption and Key Management",
    "Authentication and Authorization",
    "Security Threats and Mitigations",
    "Observability and Logging",
    "Real-World Implementations",
    "Java and Spring Boot Implementation Guide",
    "Interview Questions and Answers",
]

def normalize(s):
    return re.sub(r'\s+', ' ', s.strip().lower())

def audit_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    line_count = len(lines)

    # Find all ### headings
    headings = []
    for line in lines:
        m = re.match(r'^###\s+(.+)', line)
        if m:
            headings.append(m.group(1).strip())

    # Check fence balance
    fence_count = 0
    for line in lines:
        if line.startswith('```'):
            fence_count += 1

    # Check TBD/TODO (word-boundary regex per taste)
    tbd_matches = re.findall(r'\b(tbd|todo)\b', content, re.IGNORECASE)

    # Check Topics Covered
    has_topics_covered = False
    for h in headings:
        if "topics covered" in h.lower():
            has_topics_covered = True
            break

    # Check missing canonical topics (heading-level match)
    missing = []
    heading_norms = [normalize(h) for h in headings]
    for topic in CANONICAL_TOPICS:
        tn = normalize(topic)
        found = any(tn in hn or hn in tn for hn in heading_norms)
        if not found:
            missing.append(topic)

    # Check Java (any heading level)
    has_java = any("java and spring boot" in normalize(h) for h in headings) or \
               any(re.match(r'##+\s+.*Java and Spring Boot', line) for line in lines)

    # Check Interview (any heading level)
    has_interview = any("interview" in normalize(h) for h in headings) or \
                    any(re.match(r'##+\s+.*Interview', line) for line in lines)

    return {
        'file': os.path.basename(filepath),
        'lines': line_count,
        'headings': headings,
        'has_topics': has_topics_covered,
        'has_java': has_java,
        'has_interview': has_interview,
        'fence_count': fence_count,
        'fences_balanced': fence_count % 2 == 0,
        'tbd_count': len(tbd_matches),
        'missing': missing,
        'missing_count': len(missing),
    }

def audit_directory(dirpath, label):
    print(f"\n{'='*80}")
    print(f"  {label}: {dirpath}")
    print(f"{'='*80}")
    results = []
    for fname in sorted(os.listdir(dirpath)):
        if not fname.endswith('.md') or fname == 'todo.md':
            continue
        filepath = os.path.join(dirpath, fname)
        if os.path.isfile(filepath):
            results.append(audit_file(filepath))

    # Sort by missing count (descending), then by line count
    results.sort(key=lambda r: (-r['missing_count'], -r['lines']))

    # Print summary table
    print(f"\n{'File':<55} {'Lines':>6} {'Miss':>4} {'Top':>4} {'Java':>4} {'Int':>4} {'FBal':>4} {'TBD':>3}")
    print("-" * 90)
    for r in results:
        print(f"{r['file'][:54]:<55} {r['lines']:>6} {r['missing_count']:>4} "
              f"{'✅' if r['has_topics'] else '❌':>4} "
              f"{'✅' if r['has_java'] else '❌':>4} "
              f"{'✅' if r['has_interview'] else '❌':>4} "
              f"{'✅' if r['fences_balanced'] else '❌':>4} "
              f"{r['tbd_count']:>3}")

    # Print missing topics detail for in-progress files
    incomplete = [r for r in results if r['missing_count'] > 0]
    if incomplete:
        print(f"\n--- MISSING TOPICS DETAIL ({len(incomplete)} incomplete files) ---")
        for r in incomplete:
            print(f"\n{r['file']} ({r['lines']} lines, {r['missing_count']} missing)")
            for t in r['missing']:
                print(f"  ❌ {t}")

    return results

# Run audits
audit_directory(ADVANCED_DIR, "ADVANCED")
audit_directory(BASIC_DIR, "BASIC")
