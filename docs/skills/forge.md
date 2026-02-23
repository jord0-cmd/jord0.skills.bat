# FORGE

<span class="tag tag-system">system</span>

**Deep project onboarding. Point it at a codebase, get a CLAUDE.md that gives Claude complete context.**

Opening a new project? FORGE reads the entire thing and writes the manual Claude needs to be useful immediately.

---

## Usage

```
/forge
```

Analyzes the current directory. Or point it at a specific path:

```
/forge ~/projects/my-app
```

### Other commands

```
/forge update    # Refresh an existing CLAUDE.md
/forge check     # Verify CLAUDE.md completeness
```

---

## What FORGE Does

1. **Detects project type** — language, framework, build tools
2. **Scans directory structure** — maps the architecture
3. **Reads config files** — `package.json`, `pyproject.toml`, `Cargo.toml`, `tsconfig.json`, etc.
4. **Analyzes entry points** — where does the code start?
5. **Maps dependencies** — what does the project depend on?
6. **Identifies patterns** — naming conventions, architecture style, error handling approach
7. **Generates CLAUDE.md** — a structured document with everything Claude needs

---

## The Generated CLAUDE.md

FORGE produces a CLAUDE.md with these sections:

| Section | Contents |
|---------|----------|
| **Overview** | What the project does, tech stack, architecture style |
| **Architecture** | Directory structure, module relationships, data flow |
| **Key Files** | Entry points, config files, important modules |
| **Development** | How to build, test, run, deploy |
| **Conventions** | Naming patterns, code style, error handling approach |
| **Important Context** | Gotchas, known issues, things Claude should know |

---

## Why This Matters

A `CLAUDE.md` file in your project root is the single most impactful thing you can do for Claude Code productivity. It's the difference between Claude asking "what framework is this?" and Claude knowing exactly how your project works.

FORGE automates the creation of this file by actually reading your codebase — not guessing.

!!! tip "First session ritual"
    When opening a new project for the first time: `/strict` then `/forge`. Standards loaded, project understood. You're ready to work.

---

## Prerequisites

- Claude Code with Read, Write, Edit, Bash, Grep, Glob tools
- No external packages
- Works with any language or framework

---

*Know the codebase. Then change it.*
