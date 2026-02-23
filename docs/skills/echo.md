# ECHO

<span class="tag tag-context">context</span>

**Decision records that persist. When future-you asks "why did we do it this way?" — ECHO has the answer.**

ECHO is an architectural decision record (ADR) system made practical and queryable. Every significant decision gets captured with its reasoning, alternatives considered, and confidence level.

---

## Usage

### Create an echo

```
/echo create auth-approach
```

Claude captures:

| Field | Purpose |
|-------|---------|
| **Decision** | What was decided |
| **Reasoning** | Why this approach over others |
| **Alternatives** | What else was considered |
| **Confidence** | How sure are we (0-100) |
| **Unknowns** | What we don't know yet |
| **Context** | What project/situation this applies to |
| **Files** | Which files are affected |

Each echo gets a unique ID: `ECHO-XXXX`

### Query an echo

```
/echo query ECHO-4K2M
```

### List all echoes

```
/echo list
```

### Search by question

```
/echo query "Why did we choose JWT over sessions?"
```

Claude searches your echoes and finds the relevant decision.

---

## Why This Matters

Three months from now, you'll look at a piece of code and wonder why it's done that way. Without ECHO, you'll guess. Rewrite it. Break something. Learn the hard way why the original decision was right.

With ECHO, you ask and get the full context: the decision, the reasoning, the alternatives you already rejected, and what you were uncertain about.

---

## Pairs Well With

- **PORTAL** — capture decisions before portalling out of a session
- **MIRROR** — stress-test a decision before committing to an echo
- **CONCLAVE** — debate the options, then echo the winner

See the [Decision Audit Trail](../recipes/decision-trail.md) recipe for the full workflow.

---

## Prerequisites

- Claude Code with Bash, Read, Write tools
- `echoes/` directory auto-created on first use

---

*Decisions fade. Echoes persist.*
