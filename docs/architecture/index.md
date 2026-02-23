# Architecture

How the skill system works under the hood. For the curious and the builders.

---

## The Mental Model

Skills are **behavioral instructions**, not executable code.

Traditional plugins run code when triggered. Skills teach Claude new behaviors by providing detailed context and protocols. When you invoke `/portal`, Claude doesn't execute a portal binary — it reads the PORTAL skill's instructions and follows them using its existing tools (Read, Write, Bash, etc.).

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   User says  │────▶│ Claude loads  │────▶│ Claude follows│
│   /portal    │     │  SKILL.md    │     │  the protocol │
└──────────────┘     └──────────────┘     └──────────────┘
```

This is why skills are just markdown files. No runtime. No dependencies. No build step.

---

## File System Layout

```
~/.claude/skills/
├── PORTAL/
│   └── SKILL.md           # Skill definition
├── STRICT/
│   └── SKILL.md
├── FORGE/
│   └── SKILL.md
├── CONCLAVE/
│   └── SKILL.md
├── ECHO/
│   └── SKILL.md
├── MIRROR/
│   └── SKILL.md
├── SPARK/
│   └── SKILL.md
├── RECON/
│   └── SKILL.md
├── RECALL/
│   └── SKILL.md
└── NOTIFY/
    ├── SKILL.md
    └── scripts/
        ├── notify.sh      # Bash wrapper
        └── toast.py        # Python notification engine
```

NOTIFY is the only skill with supporting scripts — it needs to interface with platform-specific notification APIs.

---

## SKILL.md Anatomy

```yaml
---
name: SKILLNAME              # ALL CAPS identifier
description: |               # Trigger conditions
  When to invoke this skill.
  Multiple lines of context.
user-invocable: true         # Can users call it directly?
allowed-tools: Read, Write   # Tool permissions
---

# Instructions follow here...
```

### Frontmatter Fields

| Field | Required | Purpose |
|-------|:---:|--------|
| `name` | Yes | Skill identifier, must match folder name |
| `description` | Yes | Trigger conditions — Claude uses this to decide when to activate |
| `user-invocable` | Yes | Whether `/skillname` works as a direct invocation |
| `allowed-tools` | No | Restricts which Claude Code tools the skill can use |

### Instruction Body

The markdown below the frontmatter is the skill's brain. Common sections:

- **Purpose** — what this skill does
- **Usage** — commands and syntax
- **AUTO-EXECUTE protocol** — step-by-step instructions for Claude
- **Output format** — what the result should look like
- **Edge cases** — how to handle unusual situations

---

## Data Flow

### Portal data flow

```
/portal create ──▶ Claude gathers context ──▶ JSON file in portals/
                                                    │
/portal open  ◀── Claude reads + integrates ◀──────┘
```

### Research data flow

```
/recon [topic] ──▶ Research agent ──▶ Markdown report
                                          │
                                    ▼─────┘
                              knowledge/research/
                                          │
                              knowledge/index.json
                                          │
/recall [query] ◀── Search + retrieve ◀──┘
```

### Decision data flow

```
/conclave ──▶ 9-voice debate ──▶ Recommendation
                                       │
/mirror ──▶ 3 challenge frameworks ────┘
                                       │
/echo create ◀── Capture reasoning ◀───┘
                         │
                   echoes/JORD0-EC-XXXX.json
```

---

## Design Principles

### 1. Zero infrastructure

No servers, no databases, no APIs, no Docker containers. Skills run on Claude's existing tool access. Data is files on disk.

### 2. Portability

Everything is a file. JSON for structured data, markdown for reports. Move them, git them, grep them, backup them. No proprietary formats.

### 3. Composability

Skills are independent but designed to chain. RECON feeds RECALL. CONCLAVE feeds MIRROR feeds ECHO. PORTAL wraps everything. Each skill does one thing well.

### 4. Progressive disclosure

Start with one skill. Add more as habits form. The system works with 1 skill or all 10.

### 5. No magic

Every skill's behavior is readable in its SKILL.md. No hidden logic, no compiled code, no obfuscation. If you want to know what a skill does, read it.

---

## Building Your Own

The skill format is open. Create `~/.claude/skills/MYSKILL/SKILL.md` with valid frontmatter and instructions, and it works.

See [CONTRIBUTING.md](https://github.com/jord0-cmd/jord0.skills/blob/main/CONTRIBUTING.md) for the full specification and quality requirements.
