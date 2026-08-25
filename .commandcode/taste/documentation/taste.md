# Documentation

- For system-design concept docs, wants every topic covered with the same recipe: detailed explanation, real-life use case, interview questions with answers, diagrams (mermaid), and Java/Spring Boot code examples. Confidence: 0.95
- Wants concept docs organized with a "Topics Covered" list under a `## Theory` section (fundamentals → advanced), plus a closing reference section covering Characteristics, Pros, Cons, Use Cases, Components, Patterns, Benefits, Challenges, Best Practices, and When to Use — with a detailed explanation for each individual point, not just one-liners. Confidence: 0.9
- When editing existing docs, never remove existing content — review, correct, and elaborate it instead. Confidence: 0.95
- Interview-prep sections should target senior Java backend / system-design interviews: grade questions from beginner to senior/system-design level, answer each in depth, and add likely follow-ups, expected discussion points, common mistakes, and trade-offs. Confidence: 0.9
- Relevance gate: only add sections that fit the specific topic (API contracts for API topics, data modeling for storage topics, distributed considerations for distributed topics); never force template sections or Spring Boot examples into topics where they don't belong. Confidence: 0.95
- Avoid duplicating shared concepts between related topic files — give a concise explanation and cross-reference the relevant topic instead. Confidence: 0.9
- Keep headings, terminology, formatting, diagram style, code style, and explanation depth consistent across all topic files. Confidence: 0.9
- Diagrams: prefer Mermaid, pick the right diagram type per concept (flowchart, sequence, class, ER, state, architecture, data-flow), keep them syntactically valid, and accompany every diagram with a clear explanation of what it shows and how to interpret it. Confidence: 0.85
- Finished docs must contain no placeholders (`TODO`, `TBD`, incomplete sections); close out with a review pass verifying consistency, diagram syntax, and code correctness. Confidence: 0.85
