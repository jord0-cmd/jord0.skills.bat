---
name: ARBITER
description: |
  INVOKE THIS SKILL when: analyzing contracts, reviewing legal agreements, visualizing
  contract clauses, explaining contract risks, simulating breach scenarios, or when
  users paste legal documents for review. Generates interactive contract manuscripts
  with risk visualization, breach cascade simulation, and cross-reference mapping.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# ARBITER — Contract Clause Flow Analyzer

> "The document is the territory."

**Author:** jord0 | **Version:** 1.0

---

## Prerequisites

- Python 3 (for `http.server`)
- Modern browser (Chrome, Firefox, Safari, Edge)

---

## Usage

Paste a contract, upload a document, or describe a contract scenario. ARBITER generates an interactive manuscript with risk analysis, breach cascades, and cross-reference mapping.

```
Review this NDA for a SaaS partnership — I'm the customer
```

```
Analyze this MSA — highlight anything that could blow up in my face
```

```
Here's our employment contract template — what would happen if the employee breaches the non-compete?
```

### What You See

A dark manuscript (Midnight Vellum) with contract text as the interface. Red margin bars flag dangerous clauses. Dotted underlines reveal defined terms. Click scenario tabs to watch breach consequences cascade through the contract in real time. Toggle between plain English (NOV) and legal text (PRO).

---

## When to Invoke

- User pastes or uploads a contract, agreement, policy, or terms of service
- User asks to "review", "analyze", or "check" a legal document
- User says "contract", "agreement", "NDA", "MSA", "SaaS agreement", "employment contract"
- User asks about contract risks, liability, indemnification, or breach scenarios
- User wants to understand what a contract actually means in plain English
- User asks "what happens if..." about a contractual scenario

---

## Capability Lookup

| Task | ARBITER Does |
|------|-------------|
| Contract review | Full clause-by-clause risk analysis |
| Risk identification | Severity rating with market comparison |
| Plain English translation | NOV mode: every clause in readable language |
| Breach simulation | Cascade animation showing consequence chains |
| Cross-reference mapping | Visual threads between dependent clauses |
| Defined term analysis | Hover definitions with scope-creep warnings |
| Redline suggestions | Alternative language for risky clauses |

---

## How It Works

### The Flow

```
1. User pastes a contract or describes a scenario
2. You analyze every clause: type, risk, obligations, dependencies
3. Copy template → /tmp/arbiter/index.html
4. Write analysis → /tmp/arbiter/data.json
5. Start local server on port 8791
6. User opens browser, explores the interactive manuscript
7. User asks "what if?" → you update data.json → manuscript morphs live
```

### Step-by-Step

#### 1. Set Up the Server (First Time)

```bash
mkdir -p /tmp/arbiter
cp ~/.claude/skills/ARBITER/references/template.html /tmp/arbiter/index.html
```

#### 2. Analyze the Contract

Read the full contract. For each clause, determine:

- **Type**: obligation, right, condition, definition, representation, warranty, covenant, boilerplate, termination, indemnification, limitation
- **Risk level**: low, medium, high, critical
- **Dependencies**: what other clauses does it reference, trigger, override, or carve out?
- **Plain English**: what does this actually mean for the user's party?
- **Market comparison**: is this standard, aggressive, or favorable?

Group clauses into semantic clusters: scope, financial, risk_allocation, term, boilerplate, etc.

#### 3. Write the Data File

Write `/tmp/arbiter/data.json` with the full analysis:

```json
{
  "meta": {
    "title": "SaaS Master Service Agreement",
    "contractType": "saas",
    "generatedAt": "2026-03-20T14:30:00Z",
    "summary": "Master service agreement between Acme Corp (Provider) and Beta Inc (Customer) for cloud software services.",
    "overallRisk": "medium",
    "overallRiskRationale": "Generally market-standard with three areas of concern.",
    "governingLaw": "Delaware",
    "perspective": "customer",
    "clauseCount": 12,
    "crossReferenceCount": 18
  },
  "parties": [
    { "id": "p1", "name": "Acme Corp", "shortName": "Provider", "role": "vendor", "jurisdiction": "Delaware, USA" },
    { "id": "p2", "name": "Beta Inc", "shortName": "Customer", "role": "customer", "jurisdiction": "Ontario, Canada" }
  ],
  "definedTerms": [
    {
      "id": "dt1",
      "term": "Services",
      "definition": "The cloud-based software services described in Schedule A.",
      "section": "1.1",
      "risk": "medium",
      "riskRationale": "Broad definition includes 'ancillary support services' not further defined.",
      "usedIn": ["c1", "c3"],
      "dependsOn": []
    }
  ],
  "clauses": [
    {
      "id": "c1",
      "section": "2.1",
      "title": "Grant of License",
      "type": "obligation",
      "subType": "grant",
      "obligor": "p1",
      "obligee": "p2",
      "plain": "Acme grants Beta a limited right to use the software during the contract term.",
      "dev": "Provider grants Customer a non-exclusive, non-transferable license to access the Services during the Term.",
      "fullText": "Provider hereby grants to Customer a non-exclusive, non-transferable, non-sublicensable right...",
      "risk": "low",
      "riskRationale": "Standard SaaS license grant. Market-standard terms.",
      "effortLevel": null,
      "temporal": { "activates": "effectiveDate", "expires": "termination", "survives": false },
      "cluster": "scope",
      "nodeType": "step"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "source": "c3",
      "target": "c7",
      "type": "triggers",
      "label": "Breach triggers default",
      "strength": "strong"
    }
  ],
  "risks": [
    {
      "id": "r1",
      "title": "Uncapped Data Breach Indemnification",
      "severity": "critical",
      "category": "liability",
      "clauseIds": ["c8", "c9"],
      "plain": "No limit on how much you could owe for a data breach.",
      "dev": "Section 10.2(c) carves data breach indemnification out of the liability cap.",
      "marketComparison": "Market standard is a 2-5x super cap.",
      "suggestedRedline": "Customer's obligations under Section 10.2(c) shall be subject to a cap of two (2) times annual fees.",
      "negotiability": "high",
      "negotiabilityRationale": "Most vendors accept a super cap here."
    }
  ],
  "scenarios": [
    {
      "id": "s1",
      "title": "Data Breach",
      "description": "Provider suffers a security incident exposing Customer data",
      "triggerClauseId": "c5",
      "cascadePath": ["c5", "c6", "c8", "c9"],
      "outcome": "Customer's indemnification activates. WARNING: Uncapped.",
      "financialImpact": "EXPOSURE: UNCAPPED"
    }
  ]
}
```

#### 4. Start the Server

```bash
cd /tmp/arbiter && python3 -m http.server 8791
```

Run this in the background. Tell the user to open `http://localhost:8791`.

#### 5. Update the Analysis (Live)

When the user asks for changes (new scenario, deeper analysis, different perspective), just rewrite `/tmp/arbiter/data.json`. The browser polls every 500ms and morphs automatically.

**Do NOT restart the server.** The HTML poller handles everything.

---

## The data.json Contract

### Top-Level Structure

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `meta` | object | yes | Contract metadata and risk summary |
| `parties` | array | yes | Parties to the contract |
| `definedTerms` | array | yes | Defined terms (can be empty `[]`) |
| `clauses` | array | yes | All analyzed clauses |
| `edges` | array | yes | Cross-references and dependencies |
| `risks` | array | yes | Identified risk items |
| `scenarios` | array | no | Pre-built breach scenarios |

### meta

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | yes | Full title of the contract |
| `contractType` | enum | yes | `nda`, `msa`, `sow`, `saas`, `employment`, `lease`, `spa`, `apa`, `loan`, `other` |
| `generatedAt` | string | yes | ISO 8601 timestamp |
| `summary` | string | yes | 2-4 sentence executive summary |
| `overallRisk` | enum | yes | `low`, `medium`, `high`, `critical` |
| `overallRiskRationale` | string | yes | Why the overall risk level was assigned |
| `governingLaw` | string | no | Governing law jurisdiction |
| `perspective` | string | no | Which party's perspective (e.g., "customer") |
| `clauseCount` | number | no | Total clauses identified |
| `crossReferenceCount` | number | no | Total cross-references |

### parties

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique party ID (e.g., "p1") |
| `name` | string | yes | Full legal name |
| `shortName` | string | yes | Short display name |
| `role` | string | yes | Role (e.g., "vendor", "customer") |
| `jurisdiction` | string | no | Party's jurisdiction |

### definedTerms

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique term ID (e.g., "dt1") |
| `term` | string | yes | The defined term |
| `definition` | string | yes | Full definition text |
| `section` | string | no | Section where defined |
| `risk` | enum | no | `low`, `medium`, `high`, `critical` |
| `riskRationale` | string | no | Why this term is risky |
| `usedIn` | string[] | no | Clause IDs where this term appears |
| `dependsOn` | string[] | no | Other defined term IDs this depends on |

### clauses

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique clause ID (e.g., "c1") |
| `section` | string | yes | Section number (e.g., "4.2") |
| `title` | string | yes | Short clause title |
| `type` | enum | yes | `obligation`, `right`, `condition`, `definition`, `representation`, `warranty`, `covenant`, `boilerplate`, `termination`, `indemnification`, `limitation` |
| `subType` | string | no | Specific type (e.g., `payment`, `carve_out`, `override`) |
| `obligor` | string | no | Party ID bearing the obligation |
| `obligee` | string | no | Party ID benefiting |
| `plain` | string | yes | Plain English explanation (NOV mode) |
| `dev` | string | yes | Legal/technical explanation (PRO mode) |
| `fullText` | string | no | Complete original clause text |
| `risk` | enum | yes | `low`, `medium`, `high`, `critical` |
| `riskRationale` | string | yes | Why this risk level was assigned |
| `effortLevel` | enum | no | `best`, `all_reasonable`, `reasonable`, `commercially_reasonable` |
| `temporal` | object | no | `{ activates, expires, survives }` |
| `cluster` | string | no | Semantic group (e.g., "financial", "scope") |
| `nodeType` | enum | yes | `step`, `decision`, `side_effect`, `outcome`, `filter` |
| `branches` | array | no | For decision nodes: `[{ condition, targetId, outcome }]` |

### edges

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique edge ID |
| `source` | string | yes | Source clause ID |
| `target` | string | yes | Target clause ID |
| `type` | enum | yes | `depends_on`, `triggers`, `overrides`, `carves_out`, `defines`, `references`, `qualifies`, `incorporates` |
| `label` | string | no | Human-readable description |
| `strength` | enum | no | `strong`, `moderate`, `weak` |

### risks

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique risk ID |
| `title` | string | yes | Short risk title |
| `severity` | enum | yes | `low`, `medium`, `high`, `critical` |
| `category` | enum | yes | `liability`, `financial`, `ip`, `data`, `termination`, `scope`, `compliance`, `operational` |
| `clauseIds` | string[] | yes | Involved clause IDs |
| `plain` | string | yes | Plain English explanation |
| `dev` | string | yes | Legal/technical analysis |
| `marketComparison` | string | no | How this compares to market standard |
| `suggestedRedline` | string | no | Proposed alternative language |
| `negotiability` | enum | no | `high`, `medium`, `low`, `none` |
| `negotiabilityRationale` | string | no | Explanation |

### scenarios

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique scenario ID |
| `title` | string | yes | Short scenario title |
| `description` | string | no | Longer description |
| `triggerClauseId` | string | yes | Clause that starts the cascade |
| `cascadePath` | string[] | yes | Ordered list of clause IDs in the cascade |
| `outcome` | string | yes | What happens at the end |
| `financialImpact` | string | no | Financial consequence |

---

## AI Partnership Patterns

### Contract Review (Primary Use Case)

1. **Read the full contract** — every page, every clause
2. **Identify all defined terms** — check for scope creep, circular definitions
3. **Classify each clause** — type, risk level, obligations, temporal scope
4. **Map all cross-references** — triggers, overrides, carve-outs, qualifications
5. **Assess risks** — compare to market standard, suggest redlines
6. **Build scenarios** — "what if" cascades for the 2-3 most likely events
7. **Write data.json** — comprehensive analysis in structured format
8. **Explain key findings** — in the terminal, in plain English

### Iterative Deep Dive

After the initial analysis, users will ask:

- "What happens if we breach Section 8?" → Add a new scenario, update data.json
- "Can you elaborate on the indemnification?" → Add more detail to those clauses
- "Analyze from the vendor's perspective" → Change `meta.perspective`, rewrite risk assessments
- "Compare this to the amendment" → Use `documentHierarchy` for multi-document analysis

### Perspective Matters

Always ask: **"Which party are you?"** The same clause can be low-risk for the vendor and critical-risk for the customer. The `meta.perspective` field drives the risk assessment.

---

## Visual Reference

### Risk Indicators

| Risk Level | Margin Bar | Minimap Weight |
|------------|-----------|----------------|
| Low | No bar | Thin line |
| Medium | Amber 4px bar | Medium well |
| High | Red 4px bar with glow | Deep well |
| Critical | Bright red 4px bar, strong glow | Deepest well |

### Clause Types

| Type | Visual | Colour |
|------|--------|--------|
| Standard obligation | Body text | Bone white |
| Condition/gate | Purple left border, gate label | Violet |
| Carve-out | Indented 15%, dashed amber border | Amber |
| Override | Frosted blackout tape on overridden ref | Frost |
| Limitation of liability | Cap bar at bottom | Cyan |
| Terminated | Oxidized/strikethrough text | Ghost sepia |

### Edge Types

| Type | Colour | Style |
|------|--------|-------|
| Triggers | Red | Solid with glow |
| Overrides | Red | Dashed with glow |
| Carves out | Amber | Dotted |
| Defines | Cyan | Thin solid |
| References | Grey | Thin solid |
| Qualifies | Amber | Dashed |

---

## Serving Instructions

### Start Server

```bash
mkdir -p /tmp/arbiter
cp ~/.claude/skills/ARBITER/references/template.html /tmp/arbiter/index.html
cd /tmp/arbiter && python3 -m http.server 8791 &
```

### Check If Already Running

```bash
lsof -i :8791
```

If already running, skip the server start. Just update data.json.

### Stop Server

```bash
kill $(lsof -t -i :8791) 2>/dev/null
```

---

## Companion Skills

- **REFRAX** — Visual code comprehension (different visual domain)
- **REGTRAX** — Regex railroad diagrams
- **WITNESS** — Forensic timeline reconstructor 
- **THREATMAP** — Visual threat model generator 

---

## Security Checklist

- [ ] No external CDN or script tags — everything is inline
- [ ] No eval() or Function() constructor
- [ ] No localStorage/sessionStorage of sensitive data
- [ ] Server binds to localhost only (python http.server default)
- [ ] data.json contains only analysis data, no executable code
- [ ] Template is read-only — Claude never modifies it at runtime
- [ ] Contract text stays local — never transmitted to external services

---

## Quality Checklist

- [ ] All clauses have risk level, plain text, and dev text
- [ ] All cross-references are mapped as edges
- [ ] At least 2 scenarios provided for non-trivial contracts
- [ ] Defined terms are complete with definitions
- [ ] Perspective is set correctly for risk assessment
- [ ] data.json is valid JSON (no trailing commas, proper quotes)
- [ ] Server is running before telling user to open browser
