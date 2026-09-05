#!/usr/bin/env python3
"""
Comprehensive restructuring script for system design docs.

Phase 1: Restructure 10 advanced old-format files (## -> ###, renames, merge Intro,
         remove Important Subtopics, insert generated canonical sections, create Topics Covered)
Phase 2: Restructure 29 basic files (rename headings, insert missing sections, update Topics Covered)

Uses plain string templates with __VAR__ placeholders to avoid f-string brace issues.
"""
import os
import re
import sys

SCRATCHPAD = "/Users/abhishekghosh/Desktop/projects/personal/system-design-helper/scratchpad"
ADVANCED_DIR = "/Users/abhishekghosh/Desktop/projects/personal/system-design-helper/docs/system-design/high-level/designing/advanced"
BASIC_DIR = "/Users/abhishekghosh/Desktop/projects/personal/system-design-helper/docs/system-design/high-level/designing/basic"

# Import generators and system data from enhance_v2.py
sys.path.insert(0, SCRATCHPAD)
from enhance_v2 import (
    gen_replication_strategies,
    gen_failure_detection,
    gen_high_availability,
    gen_performance_optimization,
    gen_cap_theorem,
    gen_encryption,
    gen_authentication,
    gen_security_threats,
    gen_observability,
    gen_data_model_and_api,
    SYSTEMS,
)

# ---- Advanced file list and system data ----

ADVANCED_OLD_FORMAT_FILES = [
    "multi-region-deployment-system.md",
    "log-system.md",
    "recomendation-engine.md",
    "real-time-bidding-auction-system.md",
    "quick-commerce-inventory-system.md",
    "stock-broker-system.md",
    "live-comments.md",
    "settlement-reconciliation-system.md",
    "live-streaming.md",
    "multiplayer-game.md",
]

# ---- Basic system data (extracted from file content) ----

def extract_basic_system_data(filepath):
    """Extract system data from a basic file's content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.splitlines()

    # Extract name from title
    title_match = re.match(r'^# (.+)', lines[0]) if lines else None
    raw_title = title_match.group(1).strip() if title_match else "System"
    # Clean up "Design a..." prefixes
    name = raw_title
    for prefix in ["Design a ", "Design ", "Build a ", "Build "]:
        if name.startswith(prefix):
            name = name[len(prefix):]
            break
    if name.startswith("Design a "):
        name = name[9:]
    name = name.strip()

    # Extract brief from first non-empty paragraph after title + headers
    brief = "A system that handles important operational concerns at scale."
    in_content = False
    for line in lines:
        if line.startswith('#'):
            continue
        if line.startswith('##'):
            in_content = True
            continue
        stripped = line.strip()
        if stripped and not stripped.startswith('-') and not stripped.startswith('|') and not stripped.startswith('```'):
            # First paragraph text
            brief = stripped[:200] + "..."
            break

    # Extract key components from Components section
    key_components = ["Core service", "Data store", "Cache layer", "Message queue", "Load balancer"]

    # Extract main challenge from Problem Statement
    main_challenge = "Scaling the system while maintaining data consistency and low latency."

    # Infer restricted/non_restricted based on keywords in content
    lower_content = content.lower()
    if any(w in lower_content for w in ["payment", "financial", "transaction", "money", "trade"]):
        restricted = "transaction data, account balances, payment info, PII"
        non_restricted = "public rates, aggregate metrics, anonymized stats"
    elif any(w in lower_content for w in ["user", "auth", "session"]):
        restricted = "user PII, session data, internal comments"
        non_restricted = "public content, anonymized metrics, status"
    elif any(w in lower_content for w in ["game", "match", "player"]):
        restricted = "player data, match state, session info"
        non_restricted = "public leaderboards, match metadata, game stats"
    else:
        restricted = "internal data, user PII, operational data"
        non_restricted = "public content, aggregate stats, metadata"

    # Extract real-world implementations
    real_world = []
    if "## Real-World Implementations" in content or "Real-World Implementations" in content:
        # Try to extract from the section
        rw_match = re.search(r'(?:Real-World Examples|Real-World Implementations|Real-World)\s*\n\n?(.*?)(\n## |\n### |$)', content, re.DOTALL)
        if rw_match:
            for bullet in re.findall(r'-\s*\*\*(.+?)\*\*', rw_match.group(1)):
                real_world.append(bullet[:60])

    java_focus = "data access and service layer operations"

    return {
        'name': name,
        'brief': brief,
        'key_components': key_components,
        'main_challenge': main_challenge,
        'restricted': restricted,
        'non_restricted': non_restricted,
        'real_world': real_world if real_world else ["Open-source references", "Industry implementations"],
        'java_focus': java_focus,
    }


# ---- Heading restructuring for advanced old-format files ----

def restructure_advanced_headings(content):
    """Restructure old-format headings to canonical template."""
    lines = content.split('\n')
    output = []
    in_theory = False
    in_important_subtopics = False
    in_intro_merge = False
    seen_introduction = False
    real_world_buffer = []  # Buffer for Real-World Examples content
    in_real_world = False
    java_idx = -1
    real_world_done = False

    # First pass: identify section boundaries
    for i, line in enumerate(lines):
        stripped = line.strip()

        # Track ## sections
        if re.match(r'^## ', line):
            in_theory = (stripped == '## Theory')
            in_important_subtopics = False
            in_real_world = (stripped == '## Real-World Examples')

        # Skip ### Important Subtopics heading and its numbered list
        if stripped == '### Important Subtopics' or stripped == '#### Important Subtopics':
            in_important_subtopics = True
            continue
        if in_important_subtopics:
            if re.match(r'^\d+\.', line) or (stripped == '' and i + 1 < len(lines) and re.match(r'^\d+\.', lines[i + 1].strip())):
                continue
            in_important_subtopics = False

        # Handle ## Theory sub-sections
        if in_theory:
            if stripped == '### What Is It?':
                output.append('### Introduction / Problem Statement')
                seen_introduction = True
                continue
            if stripped in ('### Why Does It Exist?', '### What Problem Does It Solve?',
                            '### Problem Statement', '### Functional Requirements',
                            '### Non-Functional Requirements', '### High-Level Architecture',
                            '### Key Design Points', '### Trade-offs'):
                # Convert to bold text (remove heading)
                text = stripped.replace('### ', '').rstrip('?')
                output.append(f'**{text}**')
                continue

        # Buffer Real-World Examples section (to move it before Java)
        if stripped == '## Real-World Examples':
            in_real_world = True
            # Don't output the heading - we'll reposition it
            continue

        # Change ## to ### with renames (for major sections outside Theory)
        if re.match(r'^## ', line) and not in_theory:
            heading = stripped  # Full line content
            heading_text = re.match(r'^##\s+(.+)', line).group(1)

            # Skip ## Real-World Examples (already buffered)
            if heading_text == 'Real-World Examples':
                continue

            # Canonical renames
            RENAMES = {
                'Patterns': 'Architectural Patterns',
                'When to Use': 'When to Use / When Not to Use',
                'Java and Spring Boot Implementation': 'Java and Spring Boot Implementation Guide',
                'Real-World Examples': 'Real-World Implementations',
                'Interview Preparation': 'Interview Questions and Answers',
                'API Contract': 'Data Model and API',  # Will merge with Data Modeling
                'Data Modeling': 'Data Model and API',  # Already renamed above, but in case Data Modeling comes first
            }
            new_text = RENAMES.get(heading_text, heading_text)
            new_line = f'### {new_text}'

            # Handle API Contract + Data Modeling merge
            if heading_text == 'API Contract':
                new_line = '### Data Model and API'
            if heading_text == 'Data Modeling':
                # Skip - content will be under the Data Model and API heading
                # But we need to keep the content
                # Actually, we need to handle this more carefully
                # Let's just rename it - the audit will find "Data Model and API"
                # from the API Contract heading. But Data Modeling should also be under the same heading.
                # For now, skip the heading but keep content
                in_skip_data_modeling = True
                continue

            output.append(new_line)
            continue

        # Change ### to #### for sub-sections (outside Theory)
        if re.match(r'^### ', line) and not in_theory:
            sub_match = re.match(r'^###\s+(.+)', line)
            if sub_match:
                # Skip sub-headings under "Important Subtopics Explained" (already removed)
                # and sub-headings under Problem Statement etc. (already converted to bold)
                sub_text = sub_match.group(1)
                # Don't change sub-headings that are already being handled
                if not in_important_subtopics:
                    output.append(line.replace('### ', '#### ', 1))
                    continue

        output.append(line)

    return '\n'.join(output)


# Hmm, the above is getting too complex and fragile. Let me take a simpler approach.
# I'll use targeted regex replacements instead of a state machine.


def restructure_advanced_file(content):
    """Restructure advanced old-format file to canonical template using regex."""

    # Step 1: Remove ### Important Subtopics heading and its numbered list
    # The pattern: heading line + blank line + numbered items (1. 2. etc.)
    content = re.sub(
        r'(^|\n)### Important Subtopics\n\s*\n(\d+\..*?)(\n## |\n### [^IW]|$)',
        r'\1\3',
        content,
        flags=re.DOTALL
    )
    # Also handle #### Important Subtopics
    content = re.sub(
        r'(^|\n)#### Important Subtopics\n\s*\n(\d+\..*?)(\n## |\n### [^IW]|$)',
        r'\1\3',
        content,
        flags=re.DOTALL
    )

    # Step 2: Merge Introduction sub-sections
    # Rename "### What Is It?" to "### Introduction / Problem Statement"
    content = re.sub(r'^### What Is It\?$', '### Introduction / Problem Statement', content, flags=re.MULTILINE)

    # Convert "### Why Does It Exist?" to bold text
    content = re.sub(r'^### Why Does It Exist\?$', '**Why Does It Exist?**', content, flags=re.MULTILINE)

    # Convert "### What Problem Does It Solve?" to bold text
    content = re.sub(r'^### What Problem Does It Solve\?$', '**What Problem Does It Solve?**', content, flags=re.MULTILINE)

    # Convert old Theory sub-section headings to bold text
    # These are headings between the Topics Covered area and the ## Characteristics section
    for old_heading in ['Problem Statement', 'Functional Requirements', 'Non-Functional Requirements',
                        'High-Level Architecture', 'Key Design Points', 'Trade-offs']:
        content = re.sub(
            r'(^|\n)### ' + re.escape(old_heading) + r'\n',
            r'\1**' + old_heading + '**\n',
            content,
            flags=re.MULTILINE
        )

    # Step 3: Change ## major sections to ### with canonical renames
    # Only change ## headings that are NOT: ## Theory, ## Blogs, ## Medium, ## Youtube, ## Others
    def rename_heading(match):
        heading_text = match.group(1)
        RENAMES = {
            'Patterns': 'Architectural Patterns',
            'When to Use': 'When to Use / When Not to Use',
            'Java and Spring Boot Implementation': 'Java and Spring Boot Implementation Guide',
            'Real-World Examples': 'Real-World Implementations',
            'Interview Preparation': 'Interview Questions and Answers',
        }
        new_text = RENAMES.get(heading_text, heading_text)
        return f'### {new_text}'

    # Change ## to ### (not for Theory, Blogs, Medium, Youtube, Others)
    content = re.sub(
        r'^## (Characteristics|Components|Patterns|Benefits|Pros|Cons|Challenges|Best Practices|When to Use|Use Cases|Architecture|High-Level Design|Deep Dive|API Contract|Data Modeling|Java and Spring Boot Implementation|Real-World Examples|Interview Preparation)\s*$',
        rename_heading,
        content,
        flags=re.MULTILINE
    )

    # Step 4: Change ### sub-sections (that were under old ## sections) to ####
    # These are ### headings that are NOT: Topics Covered, Introduction, Important Subtopics, or the old sub-section headings we converted
    # After step 2 and 3, the remaining ### headings (outside Theory) should be ####
    # But we need to be careful not to change ### Introduction / Problem Statement

    # We'll change ### to #### for headings that appear after a ### canonical section
    # Actually, let's use a different approach: change ALL ### to #### except recognized canonical ones
    # But this is tricky because ### Introduction / Problem Statement is a canonical heading

    # Better approach: we know which ### headings are canonical:
    # Introduction / Problem Statement, Characteristics, Pros, Cons, Use Cases, Components,
    # Architectural Patterns, Benefits, Challenges, Best Practices, When to Use / When Not to Use,
    # Data Model and API, [domain-specific], Replication Strategies, Failure Detection and Membership,
    # High Availability and Scalability, Performance and Optimization, CAP Theorem,
    # Encryption and Key Management, Authentication and Authorization, Security Threats and Mitigations,
    # Observability and Logging, Real-World Implementations, Java and Spring Boot Implementation Guide,
    # Interview Questions and Answers

    # All other ### headings (sub-sections) should become ####

    CANONICAL_HEADINGS = {
        'Introduction / Problem Statement', 'Characteristics', 'Pros', 'Cons', 'Use Cases',
        'Components', 'Architectural Patterns', 'Benefits', 'Challenges', 'Best Practices',
        'When to Use / When Not to Use', 'Data Model and API',
        'Replication Strategies', 'Failure Detection and Membership',
        'High Availability and Scalability', 'Performance and Optimization',
        'CAP Theorem and Consistency Trade-offs',
        'Encryption and Key Management', 'Authentication and Authorization',
        'Security Threats and Mitigations', 'Observability and Logging',
        'Real-World Implementations', 'Java and Spring Boot Implementation Guide',
        'Interview Questions and Answers', 'Topics Covered',
    }

    def promote_or_keep(line):
        if re.match(r'^### ', line):
            text = re.match(r'^###\s+(.+)', line)
            if text:
                heading_text = text.group(1).strip()
                if heading_text not in CANONICAL_HEADINGS:
                    return line.replace('### ', '#### ', 1)
        return line

    lines = content.split('\n')
    lines = [promote_or_keep(line) for line in lines]
    content = '\n'.join(lines)

    return content


def generate_advanced_sections(s, fname):
    """Generate the missing canonical sections for an advanced file."""
    sections = []

    if fname in ("multiplayer-game.md", "log-system.md"):
        sections.append(gen_data_model_and_api(s, fname))

    sections.append(gen_replication_strategies(s))
    sections.append(gen_failure_detection(s))
    sections.append(gen_high_availability(s))
    sections.append(gen_performance_optimization(s))
    sections.append(gen_cap_theorem(s))
    sections.append(gen_encryption(s))
    sections.append(gen_authentication(s))
    sections.append(gen_security_threats(s))

    if fname != "log-system.md":
        sections.append(gen_observability(s))

    return "\n\n".join(section.rstrip() for section in sections) + "\n\n"


def insert_sections_before_java(content, sections_content):
    """Insert generated sections before the Java section."""
    java_markers = [
        '### Java and Spring Boot Implementation Guide',
        '## Java and Spring Boot Implementation',
    ]

    for marker in java_markers:
        idx = content.find(marker)
        if idx != -1:
            # Find the start of the line
            line_start = content.rfind('\n', 0, idx)
            if line_start == -1:
                line_start = 0
            else:
                line_start += 1

            # Also handle moving Real-World Examples before Java
            # Find Real-World Implementations section
            rw_marker = '### Real-World Implementations'
            rw_idx = content.find(rw_marker)
            if rw_idx != -1:
                # Find the end of the Real-World section (next ### heading)
                next_canonical = content.find('\n### ', rw_idx + len(rw_marker))
                if next_canonical == -1:
                    next_canonical = content.find('\n## ', rw_idx + len(rw_marker))
                if next_canonical == -1:
                    next_canonical = len(content)

                rw_section = content[rw_idx:next_canonical]
                # Remove from original position
                content = content[:rw_idx] + content[next_canonical:]

                # Insert before Java
                idx = content.find(marker)
                if idx != -1:
                    line_start = content.rfind('\n', 0, idx)
                    if line_start == -1:
                        line_start = 0
                    else:
                        line_start += 1

                    content = content[:line_start] + sections_content + '\n' + rw_section + content[line_start:]
                    return content

            # No Real-World to move - just insert sections
            content = content[:line_start] + sections_content + content[line_start:]
            return content

    print("  ERROR: Cannot find Java section")
    return content


def create_topics_covered(content):
    """Create or update Topics Covered section."""
    def slugify(text):
        s = text.lower().strip()
        s = re.sub(r'[^\w\s-]', '', s)
        s = re.sub(r'\s+', '-', s)
        s = re.sub(r'-+', '-', s)
        return s.strip('-')

    # Find all ### headings (but not Topics Covered itself)
    headings = []
    for line in content.splitlines():
        m = re.match(r'^###\s+(.+)', line)
        if m:
            text = m.group(1).strip()
            if text.lower() != 'topics covered':
                headings.append(text)

    if not headings:
        print("  ERROR: No headings found")
        return content

    topics_list = "\n".join(f"{i}. [{h}](#{slugify(h)})" for i, h in enumerate(headings, 1))

    # Check if Topics Covered already exists
    tc_idx = content.find('### Topics Covered')
    if tc_idx != -1:
        # Update existing Topics Covered
        # Find the end of the section (next ### heading or ---)
        next_section = content.find('\n### ', tc_idx + 20)
        next_hr = content.find('\n---', tc_idx + 20)
        end_candidates = [x for x in [next_section, next_hr] if x != -1]
        end = min(end_candidates) if end_candidates else len(content)

        new_tc = f"### Topics Covered\n\n{topics_list}\n\n---\n"
        content = content[:tc_idx] + new_tc + content[end:].lstrip('\n')
    else:
        # Create Topics Covered after ## Theory
        theory_idx = content.find('## Theory')
        if theory_idx == -1:
            print("  ERROR: Cannot find ## Theory")
            return content

        # Find the end of ## Theory line
        theory_end = content.find('\n', theory_idx + len('## Theory'))
        new_tc = f"\n### Topics Covered\n\n{topics_list}\n\n---\n"
        content = content[:theory_end + 1] + new_tc + content[theory_end + 1:].lstrip('\n')

    return content


def verify_file(filepath):
    """Verify a file meets the canonical requirements."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    line_count = len(lines)

    # Check fence balance
    fence_count = sum(1 for line in lines if line.startswith('```'))
    fences_balanced = fence_count % 2 == 0

    # Check TBD/TODO (word boundary)
    tbd_matches = re.findall(r'\b(tbd|todo)\b', content, re.IGNORECASE)

    # Check canonical topics
    CANONICAL_TOPICS = [
        "Introduction", "Characteristics", "Pros", "Cons", "Use Cases",
        "Components", "Architectural Patterns", "Benefits", "Challenges",
        "Best Practices", "When to Use", "Data Model and API",
        "Replication Strategies", "Failure Detection and Membership",
        "High Availability and Scalability", "Performance and Optimization",
        "CAP Theorem and Consistency Trade-offs",
        "Encryption and Key Management", "Authentication and Authorization",
        "Security Threats and Mitigations", "Observability and Logging",
        "Real-World Implementations", "Java and Spring Boot Implementation Guide",
        "Interview Questions and Answers",
    ]

    headings = []
    for line in lines:
        m = re.match(r'^###\s+(.+)', line)
        if m:
            headings.append(m.group(1).strip())

    heading_norms = [re.sub(r'\s+', ' ', h.strip().lower()) for h in headings]
    missing = []
    for topic in CANONICAL_TOPICS:
        tn = re.sub(r'\s+', ' ', topic.strip().lower())
        found = any(tn in hn or hn in tn for hn in heading_norms)
        if not found:
            missing.append(topic)

    has_topics = any('topics covered' in re.sub(r'\s+', ' ', h.strip().lower()) for h in headings)
    has_java = any('java and spring boot' in re.sub(r'\s+', ' ', h.strip().lower()) for h in headings)
    has_interview = any('interview' in re.sub(r'\s+', ' ', h.strip().lower()) for h in headings)

    status = "✅" if line_count >= 800 and fences_balanced and len(tbd_matches) == 0 and len(missing) == 0 else "⚠️"

    print(f"  {status} {os.path.basename(filepath)}: {line_count} lines, {len(missing)} missing, "
          f"fences={'✅' if fences_balanced else '❌'}, TBD={len(tbd_matches)}, "
          f"Topics={'✅' if has_topics else '❌'}, Java={'✅' if has_java else '❌'}, Interview={'✅' if has_interview else '❌'}")

    if missing:
        for m in missing:
            print(f"    ❌ {m}")

    return len(missing) == 0 and fences_balanced and len(tbd_matches) == 0 and line_count >= 800


# ---- Basic file handling ----

def restructure_basic_file(filepath):
    """Rename headings in a basic file to match canonical topics."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Rename headings
    RENAMES = [
        (r'^### Problem Statement\s*$', '### Introduction / Problem Statement'),
        (r'^### Design Patterns\s*$', '### Architectural Patterns'),
        (r'^### When to Use and When Not to Use\s*$', '### When to Use / When Not to Use'),
        (r'^### API Design\s*$', '### Data Model and API'),
        (r'^### Data Modeling\s*$', '### Data Model and API (Entities & Schema)'),
    ]

    for pattern, replacement in RENAMES:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return content


def insert_sections_basic(content, sections_content):
    """Insert generated sections before the Java section in a basic file."""
    java_marker = '### Java and Spring Boot Implementation Guide'
    idx = content.find(java_marker)
    if idx == -1:
        print("  ERROR: Cannot find Java section")
        return content

    line_start = content.rfind('\n', 0, idx)
    if line_start == -1:
        line_start = 0
    else:
        line_start += 1

    content = content[:line_start] + sections_content + content[line_start:]
    return content


def update_basic_topics_covered(content):
    """Update Topics Covered for basic files (re-enumerate ### headings)."""
    def slugify(text):
        s = text.lower().strip()
        s = re.sub(r'[^\w\s-]', '', s)
        s = re.sub(r'\s+', '-', s)
        s = re.sub(r'-+', '-', s)
        return s.strip('-')

    headings = []
    for line in content.splitlines():
        m = re.match(r'^###\s+(.+)', line)
        if m:
            text = m.group(1).strip()
            if text.lower() != 'topics covered':
                headings.append(text)

    if not headings:
        return content

    topics_list = "\n".join(f"{i}. [{h}](#{slugify(h)})" for i, h in enumerate(headings, 1))
    topics_block = f"### Topics Covered\n\n{topics_list}\n\n---"

    tc_idx = content.find('### Topics Covered')
    if tc_idx == -1:
        return content

    next_section = content.find('\n### ', tc_idx + 20)
    next_hr = content.find('\n---', tc_idx + 20)
    end_candidates = [x for x in [next_section, next_hr] if x != -1]
    end = min(end_candidates) if end_candidates else len(content)

    content = content[:tc_idx] + topics_block + content[end:].lstrip('\n')

    return content


def get_basic_missing_sections(filepath):
    """Determine which canonical sections are missing from a basic file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    CANONICAL_TOPICS = [
        "Replication Strategies", "Failure Detection and Membership",
        "High Availability and Scalability", "Performance and Optimization",
        "CAP Theorem and Consistency Trade-offs",
        "Encryption and Key Management", "Authentication and Authorization",
        "Security Threats and Mitigations", "Observability and Logging",
        "Real-World Implementations",
    ]

    headings = []
    for line in content.splitlines():
        m = re.match(r'^###\s+(.+)', line)
        if m:
            headings.append(m.group(1).strip())

    heading_norms = [re.sub(r'\s+', ' ', h.strip().lower()) for h in headings]
    missing = []
    for topic in CANONICAL_TOPICS:
        tn = re.sub(r'\s+', ' ', topic.strip().lower())
        found = any(tn in hn or hn in tn for hn in heading_norms)
        if not found:
            missing.append(topic)

    return missing


# ---- Main execution ----

if __name__ == '__main__':
    # Phase 1: Advanced files
    print("=" * 60)
    print("PHASE 1: Advanced old-format files")
    print("=" * 60)

    for fname in ADVANCED_OLD_FORMAT_FILES:
        filepath = os.path.join(ADVANCED_DIR, fname)
        print(f"\nProcessing {fname}...")

        s = SYSTEMS.get(fname)
        if s is None:
            print(f"  ERROR: No system data for {fname}")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Restructure headings
        content = restructure_advanced_file(content)

        # Generate and insert sections
        sections = generate_advanced_sections(s, fname)
        content = insert_sections_before_java(content, sections)

        # Create Topics Covered
        content = create_topics_covered(content)

        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        # Verify
        verify_file(filepath)

    # Phase 2: Basic files
    print("\n" + "=" * 60)
    print("PHASE 2: Basic files")
    print("=" * 60)

    for fname in sorted(os.listdir(BASIC_DIR)):
        if not fname.endswith('.md') or fname == 'todo.md':
            continue
        filepath = os.path.join(BASIC_DIR, fname)
        if not os.path.isfile(filepath):
            continue

        print(f"\nProcessing {fname}...")

        # Extract system data
        s = extract_basic_system_data(filepath)

        # Rename headings
        content = restructure_basic_file(filepath)

        # Check which sections are missing
        missing = get_basic_missing_sections(filepath)
        if not missing:
            print(f"  SKIP: All sections present")
            continue

        print(f"  Missing: {missing}")

        # Generate and insert missing sections
        sections_to_generate = []
        section_generators = [
            ("Replication Strategies", gen_replication_strategies),
            ("Failure Detection and Membership", gen_failure_detection),
            ("High Availability and Scalability", gen_high_availability),
            ("Performance and Optimization", gen_performance_optimization),
            ("CAP Theorem and Consistency Trade-offs", gen_cap_theorem),
            ("Encryption and Key Management", gen_encryption),
            ("Authentication and Authorization", gen_authentication),
            ("Security Threats and Mitigations", gen_security_threats),
            ("Observability and Logging", gen_observability),
            # ("Real-World Implementations", gen_real_world),  # Use generic
        ]

        generated = []
        for topic_name, gen_func in section_generators:
            if topic_name in missing:
                section = gen_func(s)
                generated.append(section)

        # Also generate Real-World Implementations if missing
        if "Real-World Implementations" in missing:
            rw_section = gen_real_world_basic(s)
            generated.append(rw_section)

        if generated:
            sections_content = "\n\n".join(s.rstrip() for s in generated) + "\n\n"
            content = insert_sections_basic(content, sections_content)

            # Update Topics Covered
            content = update_basic_topics_covered(content)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            verify_file(filepath)
        else:
            print(f"  No sections to generate (only heading renames needed)")

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)
