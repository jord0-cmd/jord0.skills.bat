# Skills Overview

10 skills. Zero dependencies (except NOTIFY). Copy a folder, get a superpower.

---

## Context & Memory

Tools that make Claude remember.

| Skill | What It Does | Invoke |
|-------|-------------|--------|
| [**PORTAL**](portal.md) | Save/restore session context across sessions and machines | `/portal` |
| [**ECHO**](echo.md) | Persistent decision records — queryable ADR system | `/echo` |

## Research & Knowledge

Tools that make Claude learn.

| Skill | What It Does | Invoke |
|-------|-------------|--------|
| [**RECON**](recon.md) | Deep research that auto-saves to a knowledge base | `/recon` |
| [**RECALL**](recall.md) | Search your knowledge base before searching the web | `/recall` |

## Cognitive Tools

Tools that make Claude think differently.

| Skill | What It Does | Invoke |
|-------|-------------|--------|
| [**CONCLAVE**](conclave.md) | 9-voice structured debate for complex decisions | `/conclave` |
| [**MIRROR**](mirror.md) | Force counterarguments against recommendations | `/mirror` |
| [**SPARK**](spark.md) | Divergent thinking — explore the non-obvious | `/spark` |

## Quality & Standards

Tools that make Claude disciplined.

| Skill | What It Does | Invoke |
|-------|-------------|--------|
| [**STRICT**](strict.md) | 11 critical coding rules — load at session start | `/strict` |
| [**FORGE**](forge.md) | Deep project onboarding — generates CLAUDE.md | `/forge` |

## System

Tools that let Claude reach through the screen.

| Skill | What It Does | Invoke |
|-------|-------------|--------|
| [**NOTIFY**](notify.md) | Cross-platform desktop notifications | `/notify` |

---

!!! tip "Recommended combo"
    Start every session with `/strict`, then `/forge` on new projects. Use `/portal` to save context before closing. Use `/recon` + `/recall` to build persistent knowledge. That's the foundation — everything else builds on it.
