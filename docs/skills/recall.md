# RECALL

<span class="tag tag-research">research</span>

**Search your knowledge base before searching the web. The retrieval half of RECON.**

You've used RECON to research topics. RECALL finds those results instantly — no web search, no re-research, no waiting.

---

## Usage

```
/recall WebSocket auth
```

```
/recall --list                    # Show everything in the knowledge base
/recall --tags rust               # Filter by tag
/recall --recent                  # Most recently added
/recall --id research-2026-02-15  # Load specific entry
```

---

## How It Works

1. Reads `knowledge/index.json`
2. Searches across titles, tags, summaries, and full-text content
3. Ranks results by relevance
4. Displays matching entries with option to load the full report

---

## Knowledge Base Structure

```
knowledge/
  research/      # Deep research reports from RECON
  references/    # Quick reference docs
  index.json     # Master index (searchable)
```

---

## The RECON + RECALL Flow

```
/recon [topic]    →  Research and save
/recall [query]   →  Find and retrieve
```

!!! tip "Always RECALL before RECON"
    Before launching a new research session, check if the topic is already in your knowledge base. Saves time and API calls.

---

## Prerequisites

- `knowledge/` directory with `index.json`
- Best paired with RECON
- No external packages

---

*Don't search twice. Remember once.*
