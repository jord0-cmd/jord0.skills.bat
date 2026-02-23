# STRICT

<span class="tag tag-quality">quality</span>

**11 non-negotiable coding rules. Load at session start. Every session.**

STRICT doesn't write code for you. It makes Claude incapable of writing bad code.

---

## Usage

```
/strict
```

That's it. Load it once at the start of your session. Claude acknowledges the standards and applies them to everything that follows.

---

## The 11 Critical Rules

### 1. Never make unauthorized changes
Only modify what's explicitly requested. No drive-by refactors. No "while I'm here" improvements. Touch what you were asked to touch and nothing else.

### 2. Finish what you start
100% or don't start. No "I'll come back to this." No partial implementations. If you open it, you close it.

### 3. No placeholders
No `TODO`, no `FIXME`, no `// implement later`. Every line of code is production code or it doesn't exist.

### 4. Production-ready code
No fake data, no mock services, no stub implementations. If it's in the codebase, it works.

### 5. Complete error handling
No silent failures. Every error is caught, logged, and handled appropriately. Users never see raw stack traces.

### 6. Read before you write
Understand existing code before modifying it. Read the file. Understand the patterns. Then change it.

### 7. One change, one purpose
Each change does one thing. Don't bundle a bugfix with a refactor with a feature. Atomic changes, clear purpose.

### 8. No dead code
No commented-out blocks. No unused imports. No functions nothing calls. If it's not being used, it's not in the codebase.

### 9. Test what you build
If you write it, test it. Not "I'll add tests later." Now.

### 10. Document the why, not the what
Comments explain reasoning, not mechanics. The code shows what happens. Comments show why.

### 11. Security is not optional
No hardcoded secrets. No SQL injection. No XSS. No OWASP top 10 violations. Security is baked in, not bolted on.

---

## Language-Specific Standards

STRICT includes guidelines for common languages:

=== "Python"

    - Type hints on all function signatures
    - `ruff` for linting and formatting
    - `uv` for package management
    - `pathlib` over `os.path`
    - Dataclasses or Pydantic for data structures
    - `async/await` for I/O-bound operations

=== "TypeScript"

    - Strict mode enabled
    - `const` over `let`, never `var`
    - Native `fetch` over axios
    - Destructuring for clean interfaces
    - Proper error typing

=== "Rust"

    - `thiserror` for library errors, `anyhow` for applications
    - `&str` over `String` where possible
    - `clippy` with all lints enabled
    - Proper lifetime annotations

---

## Why This Exists

Claude is capable of writing excellent code. It's also capable of writing sloppy code if you don't set expectations. STRICT sets the bar on the first message so every interaction that follows meets a consistent standard.

The difference between a Claude session with STRICT and without is the difference between a disciplined engineer and someone who "just makes it work."

---

*No excuses. No exceptions. Ship it right or don't ship it.*
