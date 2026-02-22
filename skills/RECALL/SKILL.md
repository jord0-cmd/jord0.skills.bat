---
name: RECALL
description: |
  Search and retrieve from a persistent knowledge base. Use BEFORE web searches or external
  research — check what you already know first. Use when: looking up previously researched
  topics, finding API references, checking what past sessions discovered, or any time
  you need information that might already be in the knowledge base.
user-invocable: true
allowed-tools: Read, Grep, Glob
---

# RECALL

**Search your knowledge base before searching the web.**

---

## Usage

```
/recall [query]            - Search the knowledge base
/recall --list             - Show all knowledge entries
/recall --tags [tag]       - Filter by tag
/recall --recent           - Show recent additions
/recall --id [id]          - Load a specific entry by ID
```

---

## What This Is

RECALL searches a local knowledge base of previously saved research, references, and documentation. It's the retrieval half of RECON — where RECON saves knowledge, RECALL finds it.

**Always check RECALL before launching a web search.** If past research exists on the topic, you save time and get more reliable, curated results.

---

## How It Works

### 1. Search the Index
RECALL reads `knowledge/index.json` and searches across:
- Entry titles
- Tags
- Summaries
- Full-text content (if needed)

### 2. Rank Results
Results are ranked by relevance:
- Exact title match → highest
- Tag match → high
- Summary keyword match → medium
- Full-text match → lower

### 3. Display Results
Shows matching entries with:
- ID, title, date
- Tags and summary
- Option to load the full report

---

## AUTO-EXECUTE Protocol

When this skill is invoked:

1. **Read** `knowledge/index.json`
2. **Parse** the user's query into search terms
3. **Search** entries by title, tags, and summary
4. **Rank** and display top results
5. **Offer to load** the full report for any match

**Proactive use:** Before any web search, check if the knowledge base already has relevant information. Mention what you found (or didn't find) before going external.

---

## Knowledge Base Structure

```
knowledge/
  research/      # Deep research reports (from RECON)
  references/    # Quick reference docs
  index.json     # Master index (searchable)
```

Each index entry:
```json
{
  "id": "k-001",
  "title": "Entry Title",
  "file": "research/filename.md",
  "date": "2024-01-15",
  "tags": ["tag1", "tag2"],
  "summary": "Brief description for quick scanning"
}
```

---

## Prerequisites

- A `knowledge/` directory with an `index.json` file
- Works standalone, but best paired with **RECON** for populating the knowledge base
- If installed without RECON, you can manually add entries to `index.json`
- No external packages required

---

## When to Use

- Before any web search — check existing knowledge first
- When a topic feels familiar — you probably researched it before
- When you need a quick reference — API docs, architecture notes
- To review what's in the knowledge base — `/recall --list`

---

## Pair With RECON

RECALL and RECON work as a pair:
- **RECON** researches and saves
- **RECALL** finds and loads

The workflow: `/recall [topic]` → not found → `/recon [topic]` → saved → next time `/recall [topic]` → instant results.

---

*Check the library before going to the bookstore.*
