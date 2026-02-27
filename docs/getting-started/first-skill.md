# Your First Skill

Let's walk through using PORTAL — the skill that gives Claude persistent memory across sessions.

---

## The Problem

You're deep in a coding session. You've made architectural decisions, debugged tricky issues, established context. Then you close the terminal.

Next session? Claude has no idea what you were doing. You spend 15 minutes re-explaining everything.

PORTAL fixes this.

---

## Install

```bash
git clone https://github.com/jord0-cmd/jord0.skills.git
cp -r jord0.skills/skills/* ~/.claude/skills/
```

This installs all 12 skills. We'll be using PORTAL for this walkthrough.

---

## Create Your First Portal

You're working on a project. Things are flowing. Before you close the session:

```
/portal create my-feature
```

Claude captures everything:

- **Git state** — current branch, last commit
- **Current task** — what you were working on
- **Decisions made** — architectural choices from this session
- **Next steps** — what's left to do
- **Files modified** — what you touched

You get back an incantation code:

```
PORTAL-7X3F
```

That's your portal. A snapshot of this exact moment in time.

---

## Open It Later

Next session. Different day. Maybe even a different machine. Type:

```
/portal open PORTAL-7X3F
```

Or use the name:

```
/portal open my-feature
```

Claude reads the portal, internalizes the context, and picks up exactly where you left off. No re-explaining. No context loss. Just flow.

---

## List Your Portals

```
/portal list
```

Shows all saved portals with names, dates, and brief summaries.

---

## What Just Happened?

You taught Claude a new behavior with a single markdown file. No API configuration, no external services, no build step. The skill told Claude:

1. **When to activate** — when you type `/portal`
2. **What to capture** — the 5 standardized context fields
3. **How to store it** — as a JSON file with a unique ID
4. **How to restore it** — read the file, internalize, continue

That's the pattern for every skill in this collection. A markdown file that teaches Claude a new superpower.

---

## Next Steps

- [How Skills Work](how-it-works.md) — understand the mechanics
- [Portal Deep Dive](../skills/portal.md) — advanced portal tricks
- [Session Preservation](../recipes/session-preservation.md) — never lose context again
