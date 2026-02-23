# RECON

<span class="tag tag-research">research</span>

**Deep technical research that auto-saves to a knowledge base. Never research the same thing twice.**

RECON conducts comprehensive research using Claude's built-in research agent, then saves the results persistently. Next time the topic comes up — in this session or any future session — the knowledge is already there.

---

## Usage

```
/recon WebSocket authentication best practices
```

```
/recon --quick difference between JWT and session tokens
```

```
/recon --deep Rust async runtime comparison: tokio vs async-std vs smol
```

```
/recon --compare GraphQL vs REST for mobile APIs
```

---

## What Happens

1. **Check existing knowledge** — is this already researched?
2. **Conduct research** — launches Claude's `technical-research-agent`
3. **Generate report** — structured markdown with findings
4. **Save to knowledge base** — `knowledge/research/YYYY-MM-DD_topic-slug.md`
5. **Update index** — `knowledge/index.json` for future searchability

---

## Report Structure

Every RECON report includes:

| Section | Contents |
|---------|----------|
| **Summary** | TL;DR of findings |
| **Key Findings** | Bullet points of the most important discoveries |
| **Deep Dive** | Detailed analysis with code examples |
| **Comparison** | Side-by-side evaluation (if applicable) |
| **Recommendations** | What to actually do |
| **Sources** | Where the information came from |

---

## Pairs With RECALL

RECON saves knowledge. RECALL retrieves it.

```
/recon WebSocket authentication       # Research and save
# ... months later ...
/recall WebSocket auth                 # Find it instantly
```

See the [Deep Research Pipeline](../recipes/research-pipeline.md) recipe for the full workflow.

---

## Prerequisites

- Claude Code with Task tool (built-in `technical-research-agent`)
- Web search access
- `knowledge/` directory auto-created on first use

---

*Research once. Know forever.*
