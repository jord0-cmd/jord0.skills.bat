---
name: refrax
description: |
  INVOKE THIS SKILL when: reviewing AI-generated code, understanding unfamiliar codebases,
  visualizing code logic as flow diagrams, explaining code to non-technical stakeholders,
  identifying security risks in code, reviewing diffs visually, or when users need to
  understand code they didn't write. Generates interactive visual code comprehension pages.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
user-invocable: true
---

# REFRAX — Visual Code Comprehension

> "Stop reading code. Start seeing it."

**Author:** jord0 | **Version:** 1.0
**Requirements:** Python 3 (for http.server), modern browser

---

## When to Invoke

- User asks to understand or review code they didn't write
- User wants a visual explanation of a function, endpoint, or flow
- User says "explain this code", "review this", "what does this do"
- User wants to identify risks or security issues visually
- User asks to review a diff or pull request
- User needs to explain code to non-technical stakeholders

---

## Capability Lookup

| Task | REFRAX Does |
|------|-------------|
| Explain code visually | Generate logic spine with plain-English steps |
| Review AI-generated code | Identify risks, show fix prompts |
| Understand unfamiliar code | Break into numbered steps with context |
| Review a diff | Show changes linked to logic spine |
| Explain to non-technical users | Novice mode with jargon-free language |
| Identify security risks | Risk cards with severity, fix steps, fix prompts |

---

## How It Works

### The Flow

```
1. User points at code (file, function, diff, or paste)
2. You analyse the code and generate structured JSON
3. Copy template → /tmp/refrax/index.html
4. Write analysis → /tmp/refrax/data.json
5. Start local server on port 8789
6. User opens browser, clicks through the logic spine
7. User asks for changes → you update data.json → UI morphs live
```

### Step-by-Step

#### 1. Set Up the Server (First Time)

```bash
mkdir -p /tmp/refrax
cp ~/.claude/skills/refrax/references/template.html /tmp/refrax/index.html
```

#### 2. Analyse the Code

Read the target code. Think through it step by step:

1. **Identify the flow** — What triggers this code? What are the steps?
2. **Map decisions** — Where does it branch? What are the conditions?
3. **Find side effects** — Database writes, network calls, file operations
4. **Assess risks** — Security holes, performance issues, logic errors
5. **Extract tech stack** — What libraries/frameworks are in play?
6. **Build glossary** — What terms would a novice not understand?

#### 3. Write the Data File

Write `/tmp/refrax/data.json` following the contract below.

#### 4. Start the Server

```bash
cd /tmp/refrax && python3 -m http.server 8789 &
```

Run in background. Tell user to open `http://localhost:8789`.

**IMPORTANT — Tell the user this is interactive.** REFRAX is a live visual page, not a
static report. After starting the server, always remind the user:

> "Open **http://localhost:8789** in your browser. This is an interactive page — click
> nodes in the spine to inspect them, switch between Plain/Dev/Code views, browse risks
> with copy-paste fix prompts, and use the Files tab to filter by file. Toggle NOV/PRO
> mode for technical vs plain-English language. The page updates live whenever I refine
> the analysis — no need to refresh. If you want to explore a different part of the
> codebase, just ask and I'll update the view."

Users who haven't seen REFRAX before won't know the output is visual and clickable.
Always point this out explicitly on first use.

#### 5. Update the Analysis (Live)

When the user asks for changes (deeper analysis, fix applied, new risks), rewrite
`/tmp/refrax/data.json`. The browser polls every 500ms and morphs automatically.

**Do NOT restart the server.** The poller handles everything.

---

## The data.json Contract

### Top-Level Structure

```json
{
  "meta": { ... },
  "techStack": [ ... ],
  "files": [ ... ],
  "spine": { ... },
  "risks": [ ... ],
  "diff": { ... },
  "glossary": [ ... ]
}
```

### meta (required)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `projectName` | string | yes | Name of the project or component |
| `generatedAt` | string | no | ISO timestamp |
| `summary` | string | yes | Summary of what this code does (2-3 sentences for overview) |
| `confidence` | number | no | 0-1 confidence in analysis accuracy |
| `environment` | object | no | `{ venv: bool, venvPath: string, pythonVersion: string }` |
| `dependencies` | array | no | `[{ name, version }]` — key project dependencies |

### techStack (optional)

Array of `{ name, role, version, evidence }` objects. Each tech detected in the code.
The `version` field is shown inline on chips and in tooltips.

### files (required)

Array of file objects:

| Field | Type | Description |
|-------|------|-------------|
| `fileId` | string | Unique ID (e.g., "f1") |
| `path` | string | File path |
| `language` | string | "python", "javascript", "typescript" |
| `content` | string | Full file content (for code highlighting) |

### spine (required)

The logic spine — the heart of the visualisation:

```json
{
  "title": "User Login Flow",
  "trigger": "User submits email + password",
  "nodes": [ ... ]
}
```

#### Node types

| Type | Shape | Colour | Use For |
|------|-------|--------|---------|
| `step` | Rounded rect | Cyan | Actions, operations, transformations |
| `decision` | Diamond | Violet | If/else, switch, validation checks |
| `side_effect` | Rounded rect | Amber | DB queries, API calls, file I/O |
| `outcome` | Pill | Emerald/Rose | Final results (success or failure) |

#### Node fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique ID (e.g., "n1") |
| `type` | string | yes | "step", "decision", "side_effect", "outcome" |
| `label` | string | yes | Short label (verb-first, max ~30 chars) |
| `plain` | string | yes | Plain English explanation (no jargon) |
| `dev` | string | yes | Technical explanation |
| `fileId` | string | no | Links to a file in files[] |
| `lines` | [int,int] | no | Start and end line numbers |
| `riskIds` | string[] | no | IDs of linked risks |
| `diffStatus` | string | no | "added", "modified", "deleted", or null |
| `branches` | array | no | Decision branches (decision nodes only) |

#### Branch fields (for decision nodes)

| Field | Type | Description |
|-------|------|-------------|
| `condition` | string | "Yes", "No", "Valid", "Invalid", etc. |
| `targetId` | string | ID of the target node |

### risks (optional)

Array of risk objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique ID (e.g., "r1") |
| `title` | string | Short title |
| `severity` | string | "high", "medium", "low" |
| `category` | string | "security", "performance", "logic", "reliability" |
| `plain` | string | Plain explanation of the risk |
| `whyItMatters` | string | Why this is dangerous |
| `where` | object | `{ fileId, lines: [start, end] }` |
| `nodeIds` | string[] | Affected spine nodes |
| `fix.title` | string | Fix description |
| `fix.steps` | string[] | Step-by-step fix instructions |
| `fix.effort` | string | "low", "medium", "high" |
| `fixPrompt` | string | Ready-made prompt to give Claude to fix this |

### diff (optional)

```json
{
  "baseLabel": "main@abc123",
  "headLabel": "feature/auth@def456",
  "summary": "Added password hashing with bcrypt.",
  "hunks": [ ... ]
}
```

#### Hunk fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique ID |
| `fileId` | string | Links to a file |
| `lines` | array | `{ type: "add"|"del"|"context", num, text }` |
| `nodeIds` | string[] | Linked spine nodes |
| `explanation` | string | What this change does |

### glossary (optional)

Array of `{ term, plain, dev }` objects. Terms are auto-linked in the UI.
The optional `dev` field provides a technical definition shown in PRO mode.

---

## Outcome Node Colours

Outcome nodes are coloured by their label text:
- Labels containing **"fail"**, **"error"**, or **"reject"** → render as **rose** (failure)
- All other outcomes → render as **emerald** (success)

Write outcome labels accordingly. Example: "Login failed" (rose), "Token created" (emerald).

---

## Labelling Rules

Labels should be readable by someone who has never programmed:

**DO use:**
- Verbs first: "Checks the password", "Saves to database", "Sends email"
- Plain nouns: "the user's email", "the login form", "the saved record"
- Questions for decisions: "Is the email valid?", "Does the user exist?"

**DON'T use:**
- `void`, `return`, `class`, `instantiate`, `callback`, `middleware`
- Function signatures in labels
- Variable names without explanation

**Novice alternatives:**
- "function" → "helper"
- "endpoint" → "URL"
- "exception" → "error"
- "parameter" → "input"
- "boolean" → "yes/no value"

---

## Spine Size Guidance

Aim for **8–20 nodes** per spine. If the code has more steps, group related operations
into single nodes. For large codebases, create separate analyses per function or module
rather than one massive spine. A focused spine is more useful than an exhaustive one.

---

## AI Partnership Patterns

### Analysing Code

When the user points at code:

1. **Read the full file** — understand context, imports, dependencies
2. **Identify the entry point** — what triggers this code?
3. **Trace the flow** — step by step, decision by decision
4. **Mark side effects** — anything that touches external systems
5. **Assess risks** — security, performance, logic, reliability
6. **Generate data.json** — following the contract exactly
7. **Serve and explain** — start server, give user the overview

### Reviewing Diffs

When the user has a diff to review:

1. **Read both versions** — understand what changed and why
2. **Build the spine** — for the NEW version's logic
3. **Mark diff status** — which nodes are added/modified/deleted
4. **Generate hunks** — with explanations of each change
5. **Assess new risks** — what did this change introduce?

### Iterative Refinement

The power move: user sees the spine, asks questions, you refine.

1. User: "What does step 3 actually do?"
2. You: Expand the `plain` and `dev` text for that node
3. You: Update data.json → UI morphs
4. User: "That risk looks bad, can you fix it?"
5. You: Fix the code, update the spine, risks update accordingly

---

## Serving Instructions

### Start Server

```bash
mkdir -p /tmp/refrax
cp ~/.claude/skills/refrax/references/template.html /tmp/refrax/index.html
cd /tmp/refrax && python3 -m http.server 8789 &
```

### Check If Already Running

```bash
lsof -i :8789
```

If already running, skip the server start. Just update data.json.

### Stop Server

```bash
kill $(lsof -t -i :8789) 2>/dev/null
```

---

## Companion Skills

- **REGTRAX** — Regex railroad visualizer (same architecture)
- **CANVAS** — Immersive 3D web experiences
- **LOCUS** — Interactive image hotspots
- **OPTIC** — AI image generation

---

## Security Checklist

- [ ] No external CDN or script tags — everything is inline
- [ ] No eval() or Function() constructor
- [ ] No localStorage of sensitive data (only sessionStorage for mode toggle)
- [ ] Server binds to localhost only
- [ ] data.json contains analysis data only, no executable code
- [ ] Template is read-only — never modified at runtime
- [ ] File content in data.json is display-only, never executed

---

## Quality Checklist

- [ ] Every spine node has both `plain` and `dev` text
- [ ] Labels use verbs, not jargon
- [ ] At least one risk identified (or explicitly noted if code is clean)
- [ ] File content is included for code highlighting
- [ ] Line numbers in nodes match actual file content
- [ ] Glossary covers terms a novice wouldn't know
- [ ] data.json is valid JSON
- [ ] Server is running before telling user to open browser
