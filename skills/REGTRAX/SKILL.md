---
name: REGTRAX
description: |
  INVOKE THIS SKILL when: visualizing regex patterns, debugging regular expressions,
  explaining regex to users, building regex from natural language, testing regex patterns
  interactively, or when railroad diagrams would help understand complex patterns.
  Generates animated railroad diagrams in the browser with live testing.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# REGTRAX — Regex Railroad Visualizer

> "Don't just write Regex. Replay it."

**Author:** jord0 | **Version:** 1.0

---

## Prerequisites

- Python 3 (for `http.server`)
- Modern browser (Chrome, Firefox, Safari, Edge)

---

## Usage

Describe what you want to match, or paste a regex you want to understand. REGTRAX generates an animated railroad diagram and serves it in your browser.

```
Match email addresses that end in .gov or .mil
```

```
Debug this regex: ^(\d{4}-\d{2}-\d{2})\s(INFO|WARN|ERROR)\s(\w+):\s(.+)$
```

```
Explain this pattern — I inherited it and nobody knows what it does
```

### What You See

A dark-themed railroad diagram with colour-coded nodes: cyan for literals, amber for character classes, violet for quantifiers, emerald for groups, rose for anchors. Type a test string and watch a photon walk the track — green on match, red on failure with the exact derailment point highlighted.

---

## When to Invoke

- User asks for help writing a regex
- User wants to understand/debug an existing regex
- User says "regex", "pattern", "match", "railroad", "visualize"
- User provides a natural language description of what to match
- User has a regex that isn't working and wants to see why

---

## Capability Lookup

| Task | REGTRAX Does |
|------|-------------|
| Natural language → regex | Write the pattern + explanation |
| Explain existing regex | Parse it, describe each part |
| Debug failing regex | Visualize where the match fails |
| Test regex interactively | Animated dot traversal in browser |
| Compare regex versions | Update pattern, diagram morphs live |
| Teach regex concepts | Visual railroad + plain English |

---

## How It Works

### The Flow

```
1. User describes what they want to match (or provides a regex to debug)
2. You write the regex pattern with plain-English explanation
3. Copy template → /tmp/regtrax/index.html
4. Write regex data → /tmp/regtrax/data.json
5. Start local server on port 8787
6. User opens browser, tests strings, sees animated diagram
7. User asks for changes → you update data.json → diagram morphs live
```

### Step-by-Step

#### 1. Set Up the Server (First Time)

```bash
mkdir -p /tmp/regtrax
cp ~/.claude/skills/REGTRAX/references/template.html /tmp/regtrax/index.html
```

#### 2. Write the Data File

Write `/tmp/regtrax/data.json` with the regex pattern, flags, explanation, and test cases:

```json
{
  "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
  "flags": "",
  "explanation": "Matches email addresses:\n- ^ anchors to start of string\n- [a-zA-Z0-9._%+-]+ matches the local part (letters, digits, dots, underscores, percent, plus, hyphen)\n- @ matches the literal @ symbol\n- [a-zA-Z0-9.-]+ matches the domain name\n- \\.[a-zA-Z]{2,} matches a dot followed by the TLD (2+ letters)\n- $ anchors to end of string",
  "testCases": [
    { "input": "hello@world.com", "shouldMatch": true },
    { "input": "user+tag@domain.co.uk", "shouldMatch": true },
    { "input": "not-an-email", "shouldMatch": false },
    { "input": "@missing-local.com", "shouldMatch": false }
  ]
}
```

#### 3. Start the Server

```bash
cd /tmp/regtrax && python3 -m http.server 8787
```

Run this in the background. Tell the user to open `http://localhost:8787`.

#### 4. Update the Pattern (Live)

When the user asks for changes, just rewrite `/tmp/regtrax/data.json`. The browser
polls every 500ms and will detect the change automatically. The diagram morphs in place.

**Do NOT restart the server.** The HTML poller handles everything.

---

## The data.json Contract

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pattern` | string | yes | The regex pattern (no delimiters) |
| `flags` | string | no | Regex flags: `i`, `g`, `m`, `s`, etc. |
| `explanation` | string | yes | Plain-English explanation with bullet points |
| `testCases` | array | no | Array of `{ input, shouldMatch }` objects |

### Escaping Rules

JSON requires double-escaping backslashes. `\d` becomes `\\d`, `\.` becomes `\\.`, etc.

```
Regex:  ^\d{3}-\d{4}$
JSON:   "^\\d{3}-\\d{4}$"
```

---

## AI Partnership Patterns

### Building Regex from Natural Language

When the user describes what to match:

1. **Clarify edge cases** — "Should it match Unicode? Multi-line? Partial strings?"
2. **Write the pattern** — Start simple, add complexity as needed
3. **Explain every part** — Use the explanation field with bullet points
4. **Provide test cases** — At least 2 matching + 2 failing strings
5. **Show the visualization** — Start the server if not running

### Debugging Existing Regex

When the user has a regex that isn't working:

1. **Understand the intent** — "What should this match?"
2. **Identify the bug** — Run mental simulation, find the failure point
3. **Explain the issue** — "The pattern fails at character N because..."
4. **Fix and visualize** — Update data.json, let the animation show the fix
5. **Compare before/after** — Explain what changed and why

### Iterative Refinement

The power move: user tests in browser, sees failure, asks you to fix.

1. User: "It's not matching X"
2. You: Explain WHY it fails (the animation shows the derailment point)
3. You: Fix the pattern, update data.json
4. Browser: Diagram morphs, user retests
5. Repeat until perfect

---

## Regex Parser Coverage

The template's built-in parser handles:

| Feature | Syntax | Supported |
|---------|--------|-----------|
| Literals | `a`, `1`, `@` | Yes |
| Escaped chars | `\d`, `\w`, `\s`, `\.` | Yes |
| Hex escapes | `\x00`-`\xFF` | Yes |
| Unicode escapes | `\u0000`-`\uFFFF` | Yes |
| Character classes | `[a-z]`, `[^0-9]`, `[\w\s]` | Yes |
| Dot (any char) | `.` | Yes |
| Alternation | `a\|b\|c` | Yes |
| Quantifiers | `?`, `*`, `+` | Yes |
| Bounded quantifiers | `{n}`, `{n,}`, `{n,m}` | Yes |
| Lazy quantifiers | `??`, `*?`, `+?` | Yes |
| Capturing groups | `(abc)` | Yes |
| Named groups | `(?<name>abc)` | Yes |
| Non-capturing groups | `(?:abc)` | Yes |
| Backreferences | `\1`-`\9` | Yes |
| Anchors | `^`, `$` | Yes |
| Word boundaries | `\b`, `\B` | Yes |
| Positive lookahead | `(?=abc)` | Yes |
| Negative lookahead | `(?!abc)` | Yes |
| Lookbehind | `(?<=)`, `(?<!)` | No |
| Unicode properties | `\p{L}` | No |

---

## Visual Reference

### Color Coding

| Node Type | Color | Var |
|-----------|-------|-----|
| Literals | Cyan/teal | `--cyan: #06b6d4` |
| Character classes | Amber | `--amber: #f59e0b` |
| Quantifiers | Violet | `--violet: #8b5cf6` |
| Groups | Emerald | `--emerald: #10b981` |
| Anchors | Rose | `--rose: #f43f5e` |

### Animation States

- **Idle**: Faint breathing glow on tracks
- **Advancing**: Cyan photon with fading trail
- **Match**: Green pulse, all tracks light up
- **Fail**: Red photon derails with gravity fall
- **Scrubbing**: Manual step-through, no animation

---

## Serving Instructions

### Start Server

```bash
mkdir -p /tmp/regtrax
cp ~/.claude/skills/REGTRAX/references/template.html /tmp/regtrax/index.html
cd /tmp/regtrax && python3 -m http.server 8787 &
```

### Check If Already Running

```bash
lsof -i :8787
```

If already running, skip the server start. Just update data.json.

### Stop Server

```bash
kill $(lsof -t -i :8787) 2>/dev/null
```

---

## Companion Skills

- **REFRAX** — Visual code comprehension (different visual domain)
- **LOCUS** — Interactive image hotspots
- **OPTIC** — AI image generation

---

## Security Checklist

- [ ] No external CDN or script tags — everything is inline
- [ ] No eval() or Function() constructor
- [ ] No localStorage/sessionStorage of sensitive data
- [ ] Server binds to localhost only (python http.server default)
- [ ] data.json contains only pattern data, no executable code
- [ ] Template is read-only — Claude never modifies it at runtime

---

## Quality Checklist

- [ ] Pattern is syntactically valid (test with `new RegExp()` mentally)
- [ ] Explanation covers every part of the pattern
- [ ] At least 2 matching + 2 failing test cases provided
- [ ] Escaping is correct in JSON (double backslashes)
- [ ] Server is running before telling user to open browser
- [ ] data.json is valid JSON (no trailing commas, proper quotes)
