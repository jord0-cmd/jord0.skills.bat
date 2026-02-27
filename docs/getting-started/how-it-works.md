# How Skills Work

No magic. Just markdown that teaches Claude new behaviors.

---

## Anatomy of a Skill

Every skill is a folder containing a `SKILL.md` file:

```
SKILLNAME/
  SKILL.md              # Required — the skill definition
  scripts/              # Optional — supporting scripts
```

The `SKILL.md` has two parts: **frontmatter** and **instructions**.

### Frontmatter

```yaml
---
name: PORTAL
description: |
  Save and restore session context across sessions and machines.
  Use when: user says /portal, needs to preserve context, or
  wants to resume previous work.
user-invocable: true
allowed-tools: Read, Write, Bash
---
```

| Field | Purpose |
|-------|---------|
| `name` | Skill identifier (ALL CAPS) |
| `description` | Trigger conditions — when should Claude use this? |
| `user-invocable` | Can the user call it directly with `/skillname`? |
| `allowed-tools` | Which Claude Code tools this skill can use |

### Instructions

Everything below the frontmatter is the skill's brain. This is where you tell Claude:

- **What to do** when the skill is invoked
- **How to do it** — step-by-step protocols
- **What to output** — expected format and behavior
- **Edge cases** — how to handle unusual situations

Claude reads this markdown and follows it like a playbook.

---

## How Claude Loads Skills

1. Claude Code scans `~/.claude/skills/` on startup
2. Each `SKILL.md` frontmatter is parsed
3. The `description` field is used for matching — when the user's request matches the trigger conditions, Claude loads the full skill
4. When invoked (via `/skillname` or automatic detection), Claude reads the entire `SKILL.md` and follows its instructions

!!! info "Skills are context, not code"
    Skills don't execute like plugins in traditional software. They're instructions that Claude follows. Think of them as extremely detailed prompts that teach Claude new behaviors.

---

## The AUTO-EXECUTE Pattern

Most skills include an `AUTO-EXECUTE` section — a step-by-step protocol that Claude follows immediately when the skill is invoked:

```markdown
## AUTO-EXECUTE PROTOCOL

When this skill is invoked:

1. Parse the user's input for [parameters]
2. Check [preconditions]
3. Perform [action]
4. Output [result]
5. Confirm [completion]
```

This removes ambiguity. Claude doesn't have to guess what to do — the protocol tells it exactly.

---

## Skill Categories

The 12 skills fall into natural groups:

| Category | Skills | Purpose |
|----------|--------|---------|
| **Creative Tools** | OPTIC, LOCUS | AI image generation and interactive mapping |
| **Context & Memory** | PORTAL, ECHO | Persist information across sessions |
| **Research & Knowledge** | RECON, RECALL | Build and query a knowledge base |
| **Cognitive Tools** | CONCLAVE, MIRROR, SPARK | Structured thinking and debate |
| **Quality & Standards** | STRICT, FORGE | Coding discipline and project onboarding |
| **System** | NOTIFY | Desktop notifications |

---

## Building Your Own

Skills are just markdown. If you can write a README, you can write a skill.

The key ingredients:

1. **Clear trigger conditions** — when should this activate?
2. **Specific instructions** — what exactly should Claude do?
3. **An AUTO-EXECUTE protocol** — step-by-step, no ambiguity
4. **Examples** — show real invocations with expected output

See [CONTRIBUTING.md](https://github.com/jord0-cmd/jord0.skills/blob/main/CONTRIBUTING.md) for the full spec.
