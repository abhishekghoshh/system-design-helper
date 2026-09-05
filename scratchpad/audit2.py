#!/usr/bin/env python3
"""
Improved audit: check canonical topics with fuzzy name matching.
Also check for leftover 'Important Subtopics' headings and heading-level issues.
"""
import os, re, sys

ADVANCED_DIR = "/Users/abhishekghosh/Desktop/projects/personal/system-design-helper/docs/system-design/high-level/designing/advanced"
BASIC_DIR = "/Users/abhishekghosh/Desktop/projects/personal/system-design-helper/docs/system-design/high-level/designing/basic"

# Canonical topics with their keyword patterns (lowercased, must be substring of heading)
CANONICAL_TOPICS = {
    "Introduction": "introduction",
    "Characteristics": "characteristics",
    "Pros": "pros",
    "Cons": "cons",
    "Use Cases": "use cases",
    "Components": "component",
    "Architectural Patterns": "architectural pattern",
    "Benefits": "benefit",
    "Challenges": "challenge",
    "Best Practices": "best practice",
    "When to Use": "when to use",
    "Data Model and API": ["data model", "api design", "data modeling"],
    "Domain-Specific": None,  # placeholder
    "Replication Strategies": "replication",
    "Failure Detection and Membership": "failure detection",
    "High Availability and Scalability": "high availability",
    "Performance and Optimization": "performance and optimization",
    "CAP Theorem": "cap theorem",
    "Encryption and Key Management": "encryption",
    "Authentication and Authorization": "authentication",
    "Security Threats and Mitigations": "security threat",
    "Observability and Logging": "observability",
    "Real-World Implementations": "real-world",
    "Java and Spring Boot Implementation Guide": "java and spring boot",
    "Interview Questions and Answers": "interview",
}

# Remove placeholder
del CANONICAL_TOPICS["Domain-Specific"]

def normalize(s):
    return re.sub(r'\s+', ' ', s.strip().lower())

def check_topic_present(topic, keyword, headings_lower):
    """Check if a canonical topic is present in any heading."""
    if isinstance(keyword, list):
        return any(kw in h for h in headings_lower for kw in keyword)
    return any(keyword in h for h in headings_lower)

def audit_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    line_count = len(lines)

    # Find all headings (## and above for section detection, ### for canonical)
    all_headings = []  # (level, text)
    h3_headings = []
    for line in lines:
        m = re.match(r'^(#{1,6})\s+(.+)', line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            all_headings.append((level, text))
            if level == 3:
                h3_headings.append(text)

    headings_lower = [normalize(h) for h in h3_headings]

    # Check fence balance
    fence_count = 0
    for line in lines:
        if line.startswith('```'):
            fence_count += 1

    # Check TBD/TODO (word-boundary)
    tbd_matches = re.findall(r'\b(tbd|todo)\b', content, re.IGNORECASE)

    # Check Topics Covered
    has_topics = any("topics covered" in h.lower() for _, h in all_headings)

    # Check missing canonical topics
    missing = []
    present_topics = set()
    for topic, keyword in CANONICAL_TOPICS.items():
        if check_topic_present(topic, keyword, headings_lower):
            present_topics.add(topic)
        else:
            missing.append(topic)

    # Check for leftover 'Important Subtopics' as a heading (any level)
    important_subtopics_headings = []
    for level, text in all_headings:
        if "important subtopics" in normalize(text):
            important_subtopics_headings.append((level, text))

    # Check for heading-level issues (## instead of ### for Java/Interview)
    java_h2 = any(level == 2 and "java and spring boot" in normalize(text) for level, text in all_headings)
    interview_h2 = any(level == 2 and "interview" in normalize(text) for level, text in all_headings)

    # Check for 'Important Subtopics' at h3 level specifically
    important_subtopics_h3 = [text for level, text in all_headings if level == 3 and "important subtopics" in normalize(text)]

    return {
        'file': os.path.basename(filepath),
        'lines': line_count,
        'has_topics': has_topics,
        'fence_count': fence_count,
        'fences_balanced': fence_count % 2 == 0,
        'tbd_count': len(tbd_matches),
        'missing': missing,
        'missing_count': len(missing),
        'important_subtopics': important_subtopics_headings,
        'java_h2': java_h2,
        'interview_h2': interview_h2,
    }

def audit_directory(dirpath, label):
    print(f"\n{'='*100}")
    print(f"  {label}: {dirpath}")
    print(f"{'='*100}")
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
    print(f"\n{'File':<55} {'Lines':>6} {'Miss':>4} {'Top':>4} {'FBal':>4} {'TBD':>3} {'ImpSub':>6} {'J2':>2} {'I2':>2}")
    print("-" * 95)
    for r in results:
        imp_sub = f"{len(r['important_subtopics'])}" if r['important_subtopics'] else ""
        print(f"{r['file'][:54]:<55} {r['lines']:>6} {r['missing_count']:>4} "
              f"{'✅' if r['has_topics'] else '❌':>4} "
              f"{'✅' if r['fences_balanced'] else '❌':>4} "
              f"{r['tbd_count']:>3} "
              f"{imp_sub:>6} "
              f"{'⚠' if r['java_h2'] else '':>2} "
              f"{'⚠' if r['interview_h2'] else '':>2}")

    # Print issues detail
    has_issues = [r for r in results if r['important_subtopics'] or r['java_h2'] or r['interview_h2'] or r['tbd_count'] > 0 or not r['fences_balanced']]
    if has_issues:
        print(f"\n--- ISSUES DETAIL ({len(has_issues)} files) ---")
        for r in has_issues:
            issues = []
            if r['important_subtopics']:
                issues.append(f"Important Subtopics headings: {r['important_subtopics']}")
            if r['java_h2']:
                issues.append("Java section uses ## instead of ###")
            if r['interview_h2']:
                issues.append("Interview section uses ## instead of ###")
            if r['tbd_count'] > 0:
                issues.append(f"TBD/TODO placeholders: {r['tbd_count']}")
            if not r['fences_balanced']:
                issues.append(f"Unbalanced fences: {r['fence_count']}")
            print(f"\n{r['file']}:")
            for i in issues:
                print(f"  ⚠️ {i}")

    # Print missing topics detail for incomplete files
    incomplete = [r for r in results if r['missing_count'] > 0]
    if incomplete:
        print(f"\n--- MISSING TOPICS DETAIL ({len(incomplete)} incomplete files) ---")
        for r in incomplete:
            print(f"\n{r['file']} ({r['lines']} lines, {r['missing_count']} missing)")
            for t in r['missing']:
                print(f"  ❌ {t}")

    return results

audit_directory(ADVANCED_DIR, "ADVANCED")
audit_directory(BASIC_DIR, "BASIC")
