---
name: ECHO
description: |
  Capture decision reasoning for future reference. Use when: making architectural decisions,
  choosing between options, recording why something was done a certain way, or any time
  "why did we do it this way?" might come up later. Creates a queryable decision log with
  full reasoning context.
user-invocable: true
allowed-tools: Bash, Read, Write
---

# ECHO

**Capture decision reasoning. Query it later. Never forget the "why."**

---

## Usage

```
/echo create <name> --decision "what" --reasoning "why"
/echo query <id> [question]
/echo list
```

---

## What This Is

ECHO captures decision points with their full reasoning context — what was decided, why, what alternatives were rejected, and what unknowns existed at the time. When future-you asks "why did we do it this way?", ECHO has the answer.

This is architectural decision records (ADRs) made practical and queryable.

---

## Creating an Echo

```
/echo create auth-strategy \
  --decision "JWT with refresh tokens over session-based auth" \
  --reasoning "Stateless scales better for our microservices architecture" \
  --alternatives "Session cookies, OAuth2 only, API keys" \
  --confidence 0.8 \
  --unknowns "Token revocation performance at scale"
```

### Fields

| Field | Flag | Description |
|-------|------|-------------|
| **Name** | (positional) | Human-readable identifier |
| **Decision** | `--decision` | What was decided |
| **Reasoning** | `--reasoning` | Why this choice was made |
| **Alternatives** | `--alternatives` | Comma-separated rejected options |
| **Confidence** | `--confidence` | 0.0 - 1.0, how sure you were |
| **Unknowns** | `--unknowns` | Comma-separated things you didn't know |
| **Project** | `--project` | Project name (defaults to current directory) |
| **Context** | `--context` | Additional session context |
| **Files** | `--files` | Comma-separated related files |

### Output
```
══════════════════════════════════════════════════════
  ECHO CAPTURED
══════════════════════════════════════════════════════
  Name:        auth-strategy
  ID:          BATCH-EC-L6C4
  Decision:    JWT with refresh tokens over session-ba...
  Confidence:  0.8

  Query later with:
    /echo query BATCH-EC-L6C4 'why did we choose JWT?'
══════════════════════════════════════════════════════
```

---

## Querying an Echo

```
/echo query auth-strategy "why not session cookies?"
/echo query BATCH-EC-L6C4 "what were the unknowns?"
```

Returns the full decision context including:
- The original decision
- Complete reasoning
- Rejected alternatives
- Unknowns at decision time
- Confidence level
- Date and project context

---

## AUTO-EXECUTE Protocol

When this skill is invoked:

**For `/echo create <name>`:**
1. Parse all provided flags
2. Generate a unique ID: `BATCH-EC-XXXX`
3. Save echo JSON to `echoes/` directory
4. Update the echo index
5. Display the echo ID for future reference

**For `/echo query <id>`:**
1. Look up the echo by ID or name
2. Load the full decision context
3. Display the reasoning in context of the question asked
4. Log the query (useful for tracking which decisions get revisited)

**For `/echo list`:**
1. Scan the echoes directory
2. Display all captured decisions with IDs, names, and dates

---

## Echo Data Format

```json
{
  "id": "BATCH-EC-L6C4",
  "name": "auth-strategy",
  "created": "2024-01-15T14:30:00",
  "decision": {
    "what": "JWT with refresh tokens",
    "reasoning": "Stateless for microservices",
    "alternatives_rejected": ["Sessions", "API keys"],
    "confidence": 0.8,
    "unknowns": ["Revocation at scale"]
  },
  "context": {
    "project": "my-api",
    "related_files": ["src/auth/middleware.ts"]
  },
  "queries": []
}
```

---

## When to Use

- Choosing between architectures, libraries, or approaches
- Making tradeoff decisions you'll need to justify later
- Before and after any "should we..." discussion
- Any time the answer to "why?" matters for future work

---

## Prerequisites

- Claude Code with Bash, Read, and Write tool access
- An `echoes/` directory for storage (skill will create it if missing)
- No external dependencies — uses Python standard library only

## Setup

1. Copy this folder to `~/.claude/skills/ECHO/`
2. The `echoes/` directory will be created automatically on first use

---

*Decisions without reasoning are accidents. Capture the why.*
