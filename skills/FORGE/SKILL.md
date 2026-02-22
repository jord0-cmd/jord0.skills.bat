---
name: FORGE
description: |
  Project onboarding and CLAUDE.md generation. Use when: starting work on a new codebase,
  setting up a project for the first time, creating or updating a project CLAUDE.md,
  generating module summaries, or when opening a project with no CLAUDE.md file. Forges
  a complete project knowledge base so Claude understands the codebase from day one.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# FORGE

**Onboard any project. Generate a CLAUDE.md. Make Claude understand your codebase.**

---

## Usage

```
/forge                  - Forge the current project (auto-detect)
/forge <path>           - Forge a specific project directory
/forge update           - Update an existing project's CLAUDE.md
/forge check            - Verify project knowledge completeness
```

---

## What FORGE Does

FORGE performs a deep scan of a codebase and generates a comprehensive `CLAUDE.md` file that gives Claude full context about the project. It's the difference between Claude guessing at your architecture and Claude *knowing* it.

### The Forging Process

1. **Detect project type** — language, framework, build tools, package manager
2. **Scan directory structure** — map the project layout, identify key directories
3. **Read configuration files** — `package.json`, `pyproject.toml`, `Cargo.toml`, `tsconfig.json`, etc.
4. **Analyze entry points** — find main files, API routes, CLI entry points
5. **Map dependencies** — external packages, internal module relationships
6. **Identify patterns** — architecture style (MVC, hexagonal, etc.), testing approach, CI/CD
7. **Generate CLAUDE.md** — structured project context file

### What Gets Generated

```markdown
# Project Name

## Overview
Brief description, purpose, key technologies.

## Architecture
Directory structure, key patterns, data flow.

## Key Files
Entry points, configuration, critical modules.

## Development
How to install, run, test, build, deploy.

## Conventions
Naming, file organization, coding patterns used.

## Important Context
Things Claude should know that aren't obvious from code.
```

---

## AUTO-EXECUTE Protocol

When this skill is invoked:

1. **Check for existing CLAUDE.md** — if present, read it first
2. **Scan the project root:**
   - `ls` the top-level directory
   - Read `package.json`, `pyproject.toml`, `Cargo.toml`, or equivalent
   - Read `README.md` if present
   - Check for `.env.example` or `.env.template`
3. **Scan source directories:**
   - Glob for source files (`**/*.py`, `**/*.ts`, `**/*.rs`, etc.)
   - Read key entry points (main files, index files, app files)
   - Identify test directories and patterns
4. **Scan configuration:**
   - Build tools (webpack, vite, esbuild, cargo)
   - Linting (eslint, ruff, clippy)
   - CI/CD (GitHub Actions, GitLab CI)
   - Docker/containerization
5. **Detect architecture patterns:**
   - Look for common patterns (routes/, controllers/, models/, services/)
   - Identify state management, API patterns, database layers
6. **Generate CLAUDE.md** — write to project root
7. **Report findings** — summarize what was discovered

---

## When to Use

- Opening a project for the first time
- Joining a new team or codebase
- A project has no CLAUDE.md and Claude keeps making wrong assumptions
- After major refactoring that changed project structure
- When Claude says "I'm not sure about the architecture"

---

## Safety

- FORGE will **never overwrite** an existing `CLAUDE.md` without asking first
- If a `CLAUDE.md` exists, FORGE reads it and offers to update (not replace)
- FORGE only reads files — it does not execute any code from the project

---

## Prerequisites

- Claude Code with file read/write access
- A project directory with source code to scan
- No external packages required

---

## Quality Checklist

A properly forged CLAUDE.md should:

- [ ] Accurately describe the project's purpose
- [ ] List all major dependencies and their roles
- [ ] Map the directory structure with explanations
- [ ] Document how to install, run, test, and build
- [ ] Identify naming conventions and coding patterns
- [ ] Note any non-obvious architecture decisions
- [ ] Be concise enough to fit in context without waste

---

## Tips

- Run `/forge check` periodically to verify the CLAUDE.md is still accurate
- After major changes, run `/forge update` instead of a full re-forge
- FORGE reads your code — it doesn't execute it. Safe to run on any project.
- The generated CLAUDE.md is a starting point. Edit it to add context only you know.

---

*Know the codebase. Then write the code.*
