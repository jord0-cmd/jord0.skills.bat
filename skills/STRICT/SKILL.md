---
name: STRICT
description: |
  Load this skill at the start of coding sessions. Contains non-negotiable coding standards,
  the 11 Critical Rules, and quality expectations. Use when: writing code, reviewing code,
  debugging, making architectural decisions, or refactoring. Enforces production-grade
  discipline in every line.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# STRICT

**Production-grade coding standards. No exceptions.**

Load this at the start of every coding session. These rules are non-negotiable.

---

## Usage

```
/strict             - Load coding standards for this session
```

Invoke at the start of any coding session. STRICT doesn't run commands — it sets expectations. Once loaded, Claude applies these rules to every code change in the session.

---

## The 11 Critical Rules

### 1. NEVER MAKE UNAUTHORIZED CHANGES
Only modify what's explicitly requested. Don't refactor adjacent code. Don't "improve" things that weren't asked about. Don't add features that weren't requested. Scope discipline is the foundation.

### 2. FINISH WHAT YOU START
We go to 100% or we don't start. No "I'll come back to this later." No leaving functions half-implemented. If you open it, you close it. If you break it, you fix it.

### 3. NO PLACEHOLDERS
Never write `TODO`, `FIXME`, `// implement later`, or stub implementations in production code. Every function does what it says. Every path is handled. If you must leave a `TODO`, link it to a tracked issue — unlinked placeholders are lies that promise future work that rarely arrives.

### 4. PRODUCTION-READY CODE
No fake data or simulated responses in production code. Mock external boundaries in tests (APIs, databases, third-party services), but never mock business logic. If a service isn't available at runtime, handle the absence properly — don't pretend it's there.

### 5. COMPLETE ERROR HANDLING
No silent failures. Ever. Every error is caught, logged, and handled appropriately. Every edge case has a path. `try/catch` without meaningful handling is worse than no error handling at all — it hides problems.

### 6. READ BEFORE YOU WRITE
Never modify code you haven't read. Never suggest changes to files you haven't examined. Understand what exists before you change it. Context is everything.

### 7. ONE CHANGE, ONE PURPOSE
Each modification should do one thing. Don't bundle a bug fix with a refactor. Don't add a feature and change the formatting. Atomic changes are reviewable changes.

### 8. NO DEAD CODE
Don't comment out code "for reference." Don't leave unused imports, variables, or functions. Dead code is noise that makes living code harder to read. If it's in version control, you can find it later.

### 9. TEST WHAT YOU BUILD
If it can break, test it. If it's critical, test it twice. Write tests that verify behavior, not implementation. Tests that break when code is refactored (but behavior is unchanged) are bad tests.

### 10. DOCUMENT THE WHY, NOT THE WHAT
Code tells you *what* it does. Comments tell you *why*. Don't write `// increment counter` above `counter++`. Do write `// retry up to 3 times because the API has transient failures`. If the code needs a comment explaining *what* it does, rewrite the code.

### 11. SECURITY IS NOT OPTIONAL
Never introduce XSS, SQL injection, command injection, or any OWASP Top 10 vulnerability. Validate all external input. Escape all output. Use parameterized queries. Treat every user input as hostile. Zero hardcoded secrets — environment variables or secret managers only.

---

## The Standard

Beyond the 11 rules, these are the quality expectations:

### Code Quality
- **Consistent naming** — pick a convention and stick to it across the project
- **Small functions** — each function does one thing well (aim for <30 lines)
- **Clear interfaces** — function signatures should be self-documenting
- **Minimal dependencies** — don't add a library for something you can write in 10 lines
- **No magic numbers** — use named constants for any non-obvious values
- **Autoformat everything** — use Prettier/Black/Rustfmt. Formatting is not a debate.

### Architecture
- **Separation of concerns** — business logic, data access, and presentation don't mix
- **Dependency injection** — hard-coded dependencies make testing impossible
- **Fail fast** — validate inputs at the boundary, not deep in the call stack
- **Idempotency** — operations that can be retried safely should be

### Process
- **Read the error message** — actually read it, don't just skim and guess
- **Reproduce first** — don't fix bugs you can't reproduce
- **Smallest possible change** — the less you change, the less you break
- **Review your own diff** — before committing, read every line of your diff as if reviewing someone else's code

---

## When You Feel Yourself Slipping

Signs you're about to write bad code:
- "This is just a quick fix" — Quick fixes become permanent. Do it right.
- "Nobody will ever change this" — They will. You will. Write for future readers.
- "It works on my machine" — If it's not reproducible, it's not done.
- "I'll add tests later" — No you won't. Write them now.
- "Let me just copy this from Stack Overflow" — Understand it first. Adapt it to your codebase.

---

## Language-Specific Notes

### Python
- Type hints on all function signatures
- Use `ruff` for linting, `uv` for package management
- Prefer `pathlib` over `os.path`
- Use dataclasses or Pydantic for structured data
- `async/await` for I/O-bound code

### TypeScript/JavaScript
- Strict TypeScript — no `any` unless absolutely necessary (and document why)
- Prefer `const` over `let`, never `var`
- Use native `fetch` over Axios for simple HTTP
- Destructure at the call site for clarity

### Rust
- Handle errors with `thiserror` (libraries) / `anyhow` (applications)
- Prefer `&str` over `String` in function parameters
- Use `clippy` with all lints enabled

---

## Prerequisites

- Claude Code (any model)
- No external packages or services required
- Works with any programming language

---

## AUTO-EXECUTE Protocol

When this skill is loaded:

1. Acknowledge the standards are active for this session
2. Apply all 11 rules to every code change
3. Flag violations before they happen (catch yourself)
4. When reviewing code, check against these rules explicitly

---

*These aren't guidelines. They're rules. Follow them.*
