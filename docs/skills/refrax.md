# REFRAX

<span class="tag tag-development">development</span>

**Stop reading code. Start seeing it. Turn any code into an interactive visual diagram with logic spines, risk dashboards, and diff views.**

AI writes code faster than humans can read it. REFRAX turns that code into a visual story — a numbered logic spine where every step, decision, side effect, and outcome is clickable, inspectable, and explained in plain English.

---

## The Problem REFRAX Solves

You asked an AI to build a billing service. It wrote 500 lines across 6 files. Now you need to:

- Understand what it actually does
- Find the security holes it left behind
- Explain it to your team lead who doesn't code
- Review a diff without reading every line

Reading raw code is slow. REFRAX makes it visual.

---

## Usage

Point Claude at any code. Say "analyse this" or "review this endpoint." REFRAX generates a structured JSON analysis and serves it as an interactive HTML page on localhost.

```
Analyse the auth endpoint in auth.py
```

```
Review the changes in this PR
```

```
Explain this billing service to a non-technical stakeholder
```

### What You See

A two-panel interface: the **Logic Spine** on the left (a vertical flow diagram of every step in the code), and the **Inspector** on the right (details, code, risks, diffs, glossary).

Click any node in the spine to inspect it. Toggle between Plain English and Developer views. Browse risk cards with one-click fix prompts.

---

## The Logic Spine

The spine breaks code into a numbered sequence of typed nodes:

| Type | Shape | Colour | Use |
|------|-------|--------|-----|
| **Step** | Rounded rect | Cyan | Actions, operations, transformations |
| **Decision** | Diamond | Violet | If/else, switch, validation checks |
| **Side Effect** | Rounded rect | Amber | Database queries, API calls, file I/O |
| **Outcome** | Pill | Emerald/Rose | Final results (success or failure) |

Each node has:

- A **plain English** explanation (no jargon)
- A **developer** explanation (with technical detail)
- Links to source **code** with line highlights
- Links to any **risks** affecting that step

---

## Risk Dashboard

REFRAX doesn't just visualise logic — it flags problems.

Every risk card includes:

- **Severity** — high, medium, or low
- **Category** — security, performance, logic, or reliability
- **Why it matters** — plain language explanation
- **Fix steps** — numbered instructions
- **Fix prompt** — a ready-made prompt to paste into Claude to fix the issue

Click a risk to jump to the affected node in the spine.

---

## Diff View

When reviewing changes, REFRAX shows hunks linked to spine nodes. See what changed, which steps were added or modified, and what risks the changes introduced.

---

## Modes

Toggle **NOV** / **PRO** in the header:

- **NOV** (Novice) — Plain English everywhere. "Checks the password" instead of "bcrypt.compare() with timing-safe comparison"
- **PRO** (Professional) — Full technical detail. Function names, library calls, implementation specifics

Both modes show the same spine — only the language changes.

---

## Live Updates

REFRAX polls for changes automatically. When Claude refines the analysis (adds a risk, expands an explanation, updates the diff), the diagram morphs in the browser. No refresh needed.

---

## How It Works Under the Hood

```
1. You point Claude at code
2. Claude analyses the code and generates structured JSON (data.json)
3. Template HTML is copied to /tmp/refrax/
4. Python http.server serves on port 8789
5. Browser loads the page and renders the spine
6. You ask questions → Claude updates data.json → UI morphs live
```

Everything is self-contained. The HTML template is a single file with zero external dependencies — no CDN, no frameworks, no build tools.

---

## Features

- **Tech Stack Bar** — Detected technologies shown as chips with hover tooltips
- **Confidence Score** — Analysis confidence badge in the header
- **File Filtering** — Filter the spine by file
- **Glossary Auto-Linking** — Technical terms are underlined; hover for definitions
- **Code View** — Full source with highlighted lines for the selected node
- **Overview Button** — Return to the summary view after inspecting nodes

---

## Pairs With

- **STRICT** — Load coding standards first, then REFRAX to review against them
- **FORGE** — Onboard a new project, then REFRAX to visualise its key flows

---

## Prerequisites

- Python 3 (for `http.server` — included in all Python installs)
- A modern browser
- No other dependencies

---

*Stop reading code. Start seeing it.*
