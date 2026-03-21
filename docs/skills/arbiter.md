# ARBITER

<span class="tag tag-analysis">analysis</span>

**Turn any contract into a living manuscript. Paste a legal document and get interactive clause-by-clause risk analysis with breach cascade simulation.**

Every contract has buried risks. ARBITER renders them visible — colour-coded margin bars for danger levels, dotted underlines for defined terms, and animated cascades showing what happens when things go wrong. Toggle between plain English and legal text with one click.

---

## The Problem ARBITER Solves

You received a 40-page MSA. Your lawyer costs $500/hour. You need to know: what can hurt me, and how badly?

Traditional contract review means reading every clause, mentally cross-referencing definitions, and guessing at breach consequences. ARBITER makes the structure visible and the risks quantifiable.

---

## Usage

Paste a contract into the terminal or describe a contract scenario. ARBITER analyses every clause and renders it as an interactive manuscript on localhost.

```
Review this NDA for a SaaS partnership -- I'm the customer
```

```
Analyze this MSA -- highlight anything that could blow up in my face
```

```
Here's our employment contract template -- what would happen if the employee breaches the non-compete?
```

### What You See

A dark manuscript (Midnight Vellum) with contract text as the interface:

- **Red margin bars** -- high/critical risk clauses
- **Amber margin bars** -- medium risk, needs attention
- **Dotted cyan underlines** -- defined terms (hover to see definitions)
- **Purple borders** -- condition gates (if/then logic)
- **Wavy red underlines** -- dangerous keywords

Click any clause to expand its analysis. Click scenario tabs on the left to watch breach cascades in real time. Toggle NOV/PRO to switch between plain English and legal text.

---

## Key Features

| Feature | What It Does |
|---------|-------------|
| **Clause-by-clause analysis** | Every clause typed, risk-rated, and cross-referenced |
| **Plain English mode (NOV)** | Every clause explained without jargon |
| **Risk visualization** | Margin bars, minimap wells, severity badges |
| **Breach cascade simulation** | Watch consequences chain through clauses in real time |
| **Cross-reference threads** | SVG lines connecting dependent clauses |
| **Defined term tooltips** | Hover any defined term to see its full definition |
| **Redline suggestions** | Alternative language for risky clauses |
| **Market comparison** | Is this clause standard, aggressive, or favorable? |

---

## Breach Cascade Simulation

The signature feature. Click a scenario tab on the left:

1. The triggering clause lights up red
2. Consequences cascade through connected clauses
3. Each affected clause pulses as it activates
4. The terminal outcome stamps at the end: CAPPED or UNCAPPED
5. Financial exposure is displayed

You can build your own "what if" scenarios by asking Claude in the terminal.

---

## How It Works Under the Hood

```
1. You paste a contract or describe a scenario
2. Claude analyses every clause: type, risk, obligations, dependencies
3. Template HTML is copied to /tmp/arbiter/
4. Python http.server serves on port 8791
5. Browser loads the page and renders the manuscript
6. You ask questions -> Claude updates data.json -> manuscript morphs live
```

Everything is self-contained. One HTML file, one JSON contract. No CDN, no frameworks, no build tools.

---

## Clause Types

| Type | Visual | Colour |
|------|--------|--------|
| Standard obligation | Body text | Bone white |
| Condition/gate | Purple left border, gate label | Violet |
| Carve-out | Indented 15%, dashed amber border | Amber |
| Override | Frosted blackout tape | Frost |
| Limitation of liability | Cap bar at bottom | Cyan |
| Terminated | Oxidized/strikethrough text | Ghost sepia |

---

## Live Updates

ARBITER polls for changes automatically. When Claude refines the analysis (adds a scenario, expands a clause, changes perspective), the manuscript morphs in the browser. No refresh needed.

---

## Pairs With

- **WITNESS** -- Analyse contracts alongside forensic timelines
- **THREATMAP** -- Complement legal risk with technical threat modeling
- **LEDGER** -- See the financial impact of contract terms

---

## Prerequisites

- Python 3 (for `http.server` -- included in all Python installs)
- A modern browser
- No other dependencies

---

*The document is the territory.*
