---
name: RECON
description: |
  Deep technical research that persists. Use when: exploring new technologies, investigating
  frameworks, comparative analysis of tools, understanding complex systems, or any research
  task that should be saved for future reference. Invokes Claude's built-in research agent
  and auto-saves results to a knowledge base for retrieval across sessions.
user-invocable: true
allowed-tools: Read, Write, Bash, Grep, Glob, WebSearch, WebFetch
---

# RECON

**Deep research. Persistent results. Never research the same thing twice.**

---

## Usage

```
/recon [topic]                     - Research a topic in depth
/recon --quick [topic]             - Quick overview (5-10 minutes)
/recon --deep [topic]              - Comprehensive investigation (30+ minutes)
/recon --compare [A] vs [B]       - Comparative analysis
```

---

## What This Is

RECON is a research skill that produces thorough technical reports and automatically saves them to a local knowledge base. Next time you (or Claude) need the same information, it's already there — no redundant web searches, no lost research.

---

## The Research Process

### 1. Check Existing Knowledge
Before researching, RECON checks the knowledge base for existing reports on the topic. If a relevant report exists, it surfaces that first and asks if an update is needed.

### 2. Conduct Research
Uses Claude's built-in `technical-research-agent` to:
- Decompose the topic into subtopics
- Search multiple sources (web, documentation, repos)
- Synthesize findings into a structured report
- Identify code examples and implementation patterns

### 3. Save Results
Reports are saved as markdown files to the knowledge base directory:
```
knowledge/
  research/
    2024-01-15_react-server-components.md
    2024-01-20_rust-vs-go-backends.md
    2024-02-01_vector-databases-comparison.md
  index.json    # Master index for search
```

### 4. Index for Future Retrieval
The report is indexed with:
- Title, topic, date
- Key technologies mentioned
- Summary for quick scanning
- Tags for semantic search

---

## AUTO-EXECUTE Protocol

When this skill is invoked:

1. **Parse the topic** from the user's message
2. **Check knowledge base** — search `knowledge/index.json` for existing research
3. **If found:** Display the existing report summary, ask if an update is needed
4. **If not found:** Launch the `technical-research-agent` (Task tool, subagent_type: `technical-research-agent`)
5. **Save the report** to `knowledge/research/YYYY-MM-DD_<topic-slug>.md`
6. **Update the index** with metadata
7. **Summarize findings** to the user

---

## Report Structure

Every RECON report follows this format:

```markdown
# [Topic]

## Summary
One-paragraph executive summary.

## Key Findings
- Finding 1
- Finding 2
- Finding 3

## Deep Dive
Detailed analysis with code examples where relevant.

## Comparison (if applicable)
| Feature | Option A | Option B |
|---------|----------|----------|
| ...     | ...      | ...      |

## Recommendations
What to use and why, given the context.

## Sources
Links to documentation, articles, repos referenced.
```

---

## Knowledge Base Setup

Create the following directory structure:
```
knowledge/
  research/      # Research reports (markdown)
  references/    # Quick reference docs
  index.json     # Master index
```

The `index.json` schema:
```json
{
  "entries": [
    {
      "id": "k-001",
      "title": "React Server Components Deep Dive",
      "file": "research/2024-01-15_react-server-components.md",
      "date": "2024-01-15",
      "tags": ["react", "rsc", "frontend", "server-components"],
      "summary": "One-line summary for quick scanning"
    }
  ]
}
```

---

## When to Use

- Evaluating a new framework or library
- Comparing architectural approaches
- Understanding a technology before prototyping
- Any research you don't want to repeat next week

---

## Prerequisites

- **Claude Code** with Task tool access (the `technical-research-agent` is a built-in Claude Code subagent — no external setup needed)
- **File system access** for knowledge base storage
- **Web search access** for current information (WebSearch tool must be available)

**Note:** The `technical-research-agent` is part of Claude Code itself, not an external service. If you have Claude Code, you have the agent.

---

*Research once. Remember forever.*
