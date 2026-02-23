---
name: PORTAL
description: |
  Context transfer between sessions, projects, and machines. Use when: saving work context
  before switching tasks, resuming from a previous session, carrying context across machines,
  or any time "where was I?" needs answering. Creates portable context snapshots with unique
  portal ID codes for instant recall.
user-invocable: true
allowed-tools: Bash, Read, Write
---

# PORTAL

**Save and restore session context across sessions, projects, and machines.**

---

## Usage

```
/portal create <name>   - Save current context with a portal name
/portal open <id>       - Open a portal by ID (JORD0-PT-XXXX) or name
/portal list            - Show all available portals
/portal close <id>      - Delete a portal permanently
/portal update <id>     - Update an existing portal with new context
```

---

## How It Works

### Creating a Portal

When this skill is invoked with `create <name>`:

1. **Gather context — ALWAYS include these 5 standardized fields:**
   - **Active branch & last commit** — run `git branch --show-current` and `git log -1 --oneline` to capture exactly where the codebase sits
   - **Current task & status** — what you're working on and how far along (e.g., "Auth refactor — 60% complete, middleware done, token refresh WIP")
   - **Key decisions made** — important choices from this session (architecture picks, library selections, design tradeoffs)
   - **Blocked on / next steps** — what's pending, what's blocking progress, and what comes next
   - **Files modified** — key files touched this session (run `git diff --name-only` if unsure)

   Additionally capture if relevant:
   - What's the session state / energy?
   - Any important context that doesn't fit above?

2. **Generate a unique portal ID** — format: `JORD0-PT-XXXX` (4 random alphanumeric chars)

3. **Save the portal** as a JSON file containing all captured context

4. **Show the portal ID** — this is the code to resume later

### Opening a Portal

When invoked with `open <portal-id>` or `open <name>`:

1. **Read the portal file** by portal ID code or name lookup

2. **Internalize the context** — become aware of:
   - Where the work was happening
   - What was being done
   - The mood and energy
   - Important context
   - Next steps

3. **Continue naturally** — pick up where you left off

### Knowledge Transfer Checklist

When opening a portal, ensure ACTUAL transfer of all 5 standardized fields:

- [ ] Acknowledged the **branch & last commit**
- [ ] Stated the **current task & status** in your own words
- [ ] Acknowledged **key decisions made**
- [ ] Identified **blockers / next steps**
- [ ] Noted **files modified** and their relevance
- [ ] Adopted the mood/energy (not just displayed it)
- [ ] Noted any knowledge entries to load
- [ ] Ready to continue as if the previous session never ended

**The portal is not just data display — it's context RESTORATION.**

---

## AUTO-EXECUTE Protocol

When this skill is invoked:

**For `/portal create <name>`**:
1. Run `git branch --show-current` and `git log -1 --oneline` to capture branch state
2. Run `git diff --name-only` to identify modified files (if not already known)
3. Analyze the current conversation and extract the 5 standardized fields:
   - **Active branch & last commit** → `--state` (prepend branch/commit info)
   - **Current task & status** → `--context`
   - **Key decisions made** → `--decisions`
   - **Blocked on / next steps** → `--next`
   - **Files modified** → `--files`
4. Generate a unique `JORD0-PT-XXXX` code
5. Save portal JSON to `portals/` directory
6. Show the portal ID code prominently
7. Optionally commit to git for cross-machine sync

**For `/portal open <id>`**:
1. Load the portal by portal ID or name
2. Read and internalize the context
3. **SUMMARIZE BACK the 5 standardized fields to the user:**
   - "Branch: [branch] @ [last commit]"
   - "Working on: [current task & status]"
   - "Key decisions made: [decisions]"
   - "Blocked on / next steps: [blockers and next steps]"
   - "Files modified: [files]"
   - Plus session state/energy and any important context if present
4. **Adopt the mood/energy** from the portal
5. Ask if ready to continue or if anything needs clarification

**For `/portal list`**:
1. Scan portals directory
2. Display available portals with names, codes, and dates

---

## Portal Data Format

```json
{
  "portal ID": "JORD0-PT-XXXX",
  "name": "project-name",
  "spell_type": "portal",
  "created": "ISO timestamp",
  "origin": {
    "project": "current directory name",
    "machine": "hostname",
    "working_dir": "/path/to/project",
    "timestamp": "human-readable timestamp"
  },
  "context": {
    "summary": "What we're doing",
    "active_work": ["item1", "item2"],
    "decisions": ["decision1", "decision2"],
    "blockers": [],
    "files_touched": ["file1.py", "file2.ts"],
    "current_state": "Branch/commit state"
  },
  "session_state": {
    "mood": "focused|creative|debugging|exploring|flow",
    "energy": "high|normal|low",
    "notes": "Additional session notes"
  },
  "continuation": {
    "next_steps": ["step1", "step2"],
    "questions_pending": [],
    "important_context": "Critical info to carry forward"
  }
}
```

---

## Incantation Format

```
JORD0-PT-7X3F
  │    │   │
  │    │   └── Unique 4-char code
  │    └────── PT = Portal type
  └─────────── Prefix (customize to your brand)
```

---

## Setup

PORTAL is self-contained. To install:

1. Copy this folder to `~/.claude/skills/PORTAL/`
2. Create a `portals/` directory wherever you want to store portals (default: project root or `~/.claude/portals/`)
3. **For cross-machine sync**: store your `portals/` directory inside a git repository

**Cross-machine sync requires git.** Portal files are plain JSON. The skill will offer to `git add && git commit && git push` after creating a portal if it detects a git repository. On the receiving machine, `git pull` brings all portals up to date. Alternatively, use any synced directory (Dropbox, iCloud, etc.).

**Conflict safety:** Opening a portal does NOT modify your working tree. It only restores *cognitive* context — what you were doing, decisions made, next steps. Your git state remains untouched.

The skill works by instructing Claude to gather context, generate codes, and save/load JSON files. No external dependencies required.

---

## Examples

```
/portal create auth-refactor
/portal open JORD0-PT-7X3F
/portal open auth-refactor
/portal list
/portal close JORD0-PT-7X3F
```

---

## Prerequisites

- Claude Code with Bash, Read, and Write tool access
- **Git** — required for cross-machine sync (portals are committed and pushed to a shared repo). Without git, portals are local-only.
- A `portals/` directory for storage (skill will create it if missing)
- No external packages required

---

## When to Use

- Switching between projects mid-session
- Ending a session and wanting to resume later
- Moving work between machines
- Handing off context to a colleague
- Any time "where was I?" is a question you'll need to answer

---

*Context is everything. Don't lose it.*
