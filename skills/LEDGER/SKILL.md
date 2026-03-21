---
name: LEDGER
description: |
  INVOKE THIS SKILL when: analyzing business finances, projecting cash flow,
  understanding burn rate and runway, comparing financial scenarios, or when
  users describe their revenue, expenses, and financial situation. Generates
  interactive kinetic financial visualizations with scenario modeling.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# LEDGER — Kinetic Financial Visualizer

> "Watch your money breathe."

**Author:** jord0 | **Version:** 1.0

---

## Prerequisites

- Python 3 (for `http.server`)
- Modern browser (Chrome, Firefox, Safari, Edge)

---

## Usage

Describe your business financials — revenue streams, expenses, cash on hand, growth rates. LEDGER generates an interactive kinetic visualization with cash flow projections, runway analysis, and scenario comparison.

```
We have $500K in the bank, $30K/mo revenue growing 8% monthly, $45K/mo burn rate. How long do we have?
```

```
Model our SaaS financials with three scenarios: base, optimistic, pessimistic
```

```
We're planning to hire 3 engineers in Q3 — show me the impact on runway
```

### What You See

A Cartesian financial landscape. Revenue ghosts float above the equator as hatched cyan blocks. The cash reservoir fills and drains below. OPEX furnaces glow crimson. CAPEX diamonds mark one-time investments. A runway meter shows months remaining. Hover the playhead across the chart to see exact figures at any month.

---

## When to Invoke

- User asks about cash flow projections or runway
- User describes business revenue, expenses, burn rate
- User wants to compare financial scenarios (optimistic vs pessimistic)
- User says "financials", "runway", "burn rate", "cash flow", "budget"
- User provides revenue streams, expenses, or asks "how long will my money last?"
- User wants to visualize where money flows in a business

---

## Capability Lookup

| Task | LEDGER Does |
|------|-------------|
| Cash flow projection | Compute monthly cash balances with growth, churn, payment delays |
| Runway analysis | Show exactly when cash hits zero |
| Scenario modeling | Compare base, optimistic, pessimistic outcomes |
| Expense breakdown | Visualize OPEX, COGS, taxes, CAPEX as distinct flows |
| Revenue visualization | Show revenue ghosts with payment term delays |
| Burn rate calculation | Average monthly cash consumption rate |

---

## How It Works

### The Flow

```
1. User describes their financial situation (revenue, expenses, cash)
2. You extract the numbers and structure them into data.json
3. Copy template → /tmp/ledger/index.html
4. Write financial data → /tmp/ledger/data.json
5. Start local server on port 8790
6. User opens browser, sees kinetic financial landscape
7. User asks for changes → you update data.json → visualization morphs live
```

### Step-by-Step

#### 1. Set Up the Server (First Time)

```bash
mkdir -p /tmp/ledger
cp ~/.claude/skills/LEDGER/references/template.html /tmp/ledger/index.html
```

#### 2. Write the Data File

Extract the user's financial information and structure it as `/tmp/ledger/data.json`:

```json
{
  "meta": {
    "companyName": "Acme Corp",
    "summary": "Short description of the business situation",
    "modelType": "startup",
    "baseCurrency": "USD"
  },
  "config": {
    "defaultView": "monthly",
    "defaultScenario": "base",
    "showRunwayMeter": true,
    "showBalanceCheck": true,
    "detailLevel": "standard"
  },
  "financials": {
    "starting_cash": 500000,
    "currency": "USD",
    "revenue_streams": [...],
    "cost_of_goods": [...],
    "operating_expenses": [...],
    "taxes": {...},
    "capital_expenditure": [...]
  },
  "scenarios": [...],
  "timeline": {
    "startDate": "2026-01-01",
    "months": 24,
    "granularity": "monthly"
  }
}
```

#### 3. Start the Server

```bash
cd /tmp/ledger && python3 -m http.server 8790 &
```

Run this in the background. Tell the user to open `http://localhost:8790`.

#### 4. Update the Model (Live)

When the user asks for changes, just rewrite `/tmp/ledger/data.json`. The browser
polls every 500ms and will detect the change automatically. The visualization morphs in place.

**Do NOT restart the server.** The HTML poller handles everything.

---

## The data.json Contract

### meta

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `companyName` | string | yes | Display name |
| `summary` | string | no | One-line business description |
| `modelType` | string | no | "startup", "smb", "enterprise" |
| `baseCurrency` | string | no | "USD", "GBP", "EUR" |

### config

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `defaultView` | string | no | "monthly" (only option for now) |
| `defaultScenario` | string | no | ID of default scenario to display |
| `showRunwayMeter` | boolean | no | Show the runway HUD overlay |
| `showBalanceCheck` | boolean | no | Enable balance check features |
| `detailLevel` | string | no | "standard" or "detailed" |

### financials

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `starting_cash` | number | yes | Cash in hand at month 0 |
| `currency` | string | no | Currency code (default "USD") |
| `revenue_streams` | array | no | Revenue stream objects |
| `cost_of_goods` | array | no | COGS objects |
| `operating_expenses` | array | no | OPEX objects |
| `taxes` | object | no | Tax configuration |
| `capital_expenditure` | array | no | CAPEX objects |

### revenue_streams[]

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier (e.g., "rev-1") |
| `name` | string | yes | Display name |
| `amount` | number | yes | Base amount per period |
| `frequency` | string | yes | "monthly", "quarterly", "annual" |
| `growthRate` | number | no | Growth rate per month (0.08 = 8%) |
| `growthType` | string | no | "compound", "linear", "flat" |
| `paymentTerms` | string | no | "prepaid", "net-30", "net-60", "net-90" |
| `churnRate` | number | no | Monthly churn rate (0.03 = 3%) |
| `startMonth` | number | no | Month this stream begins (default 1) |
| `endMonth` | number | no | Month this stream ends |

### cost_of_goods[]

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier |
| `name` | string | yes | Display name |
| `type` | string | yes | "percentage" or "fixed" |
| `value` | number | yes | Percentage (0.15 = 15%) or fixed amount |
| `appliesTo` | string | no | "all_revenue" or specific stream ID |

### operating_expenses[]

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier |
| `name` | string | yes | Display name |
| `amount` | number | yes | Amount per period |
| `frequency` | string | yes | "monthly", "quarterly", "annual" |
| `growthRate` | number | no | Growth rate per month |
| `category` | string | no | "engineering", "marketing", "operations", etc. |
| `paymentMonth` | number | no | For annual: which month to pay |

### taxes

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `effectiveRate` | number | yes | Tax rate (0.21 = 21%) |
| `frequency` | string | yes | "monthly", "quarterly", "annual" |
| `method` | string | no | "percentage-of-profit" |

### capital_expenditure[]

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier |
| `name` | string | yes | Display name |
| `amount` | number | yes | One-time amount |
| `month` | number | yes | Which month the expense occurs |
| `notes` | string | no | Description |

### scenarios[]

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier ("base", "optimistic", etc.) |
| `name` | string | yes | Display name |
| `description` | string | no | What this scenario represents |
| `adjustments` | array | yes | Array of adjustment objects |

### scenarios[].adjustments[]

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `targetId` | string | yes | ID of the financial item to adjust |
| `field` | string | yes | Field to adjust ("amount", "growthRate", "churnRate", "endMonth") |
| `operation` | string | yes | "multiply", "add", "set" |
| `value` | number | yes | The adjustment value |
| `startMonth` | number | no | When adjustment takes effect |
| `endMonth` | number | no | When adjustment expires |
| `reason` | string | no | Why this adjustment exists |

### timeline

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `startDate` | string | yes | ISO date string (e.g., "2026-01-01") |
| `months` | number | yes | Number of months to project |
| `granularity` | string | no | "monthly" |

---

## Visual Language

### The Cartesian Landscape

```
Y-axis (Dollars)
    ^
    |   ═══════════           [STRATOSPHERE: Revenue ghosts]
    |   ║ Rev A ║──→──┐       (hatched, translucent cyan)
    |   ═══════════    │
    |   ──────────────┼───── [EQUATOR: Settlement line, y=0]
    |                  ↓
    |   ████████████████████  [LITHOSPHERE: Cash reservoir]
    |   ██████████████████    (dark, solid, dense blue-slate)
    |        ↓    ↓    ↓
    |      [OPEX drains]      [FURNACE: crimson gradient]
    +────────────────────────→ X-axis (Time / Months)
```

### Colour Coding

| Element | Colour | Hex |
|---------|--------|-----|
| Revenue ghosts | Cyan + diagonal hatching | `#00E5FF` |
| Cash reservoir | Dark slate → Deep cobalt gradient | `#0F172A` → `#1E3A8A` |
| OPEX furnace | Crimson thermal gradient | `#E11D48` |
| COGS parasites | Amber | `#F59E0B` |
| Taxes | Slate (cold, mechanical) | `#64748B` |
| CAPEX investments | Violet diamonds | `#8B5CF6` |
| Cliff / failure | Red line + black void | `#DC2626` |
| Hazard (< 3mo) | Acid yellow pulse | `#FAFF00` |

### Interactive Elements

- **Hover** on any element → tooltip with name, amount, % of total
- **Click** OPEX pipe → expands into sub-category breakdown
- **Scenario buttons** → animated transition between projections
- **Probability corridor** → translucent area between optimistic ceiling and pessimistic floor
- **Playhead** → hover across chart to see balance at any month

---

## AI Partnership Patterns

### Building a Financial Model from Conversation

When the user describes their business:

1. **Extract numbers** — Revenue, expenses, cash on hand, growth rates
2. **Clarify gaps** — "What's your monthly burn? Any payment delays? Growth assumptions?"
3. **Build scenarios** — At minimum: base, optimistic, pessimistic
4. **Write data.json** — Structure everything per the contract above
5. **Show the visualization** — Start the server if not running

### Common Questions to Ask

- "What's your current cash position?"
- "What are your main revenue streams and their growth rates?"
- "Any revenue with delayed payment terms (net-30, net-60)?"
- "What are your fixed monthly expenses?"
- "Any one-time capital expenditures planned?"
- "What does your optimistic scenario look like? Pessimistic?"

### Iterative Refinement

The power move: user sees the visualization, realizes something's missing.

1. User: "Actually, we're hiring two more engineers in Q3"
2. You: Update operating_expenses or add a scenario adjustment
3. Rewrite data.json
4. Browser: Visualization morphs, runway recalculates
5. Repeat until the model reflects reality

---

## Serving Instructions

### Start Server

```bash
mkdir -p /tmp/ledger
cp ~/.claude/skills/LEDGER/references/template.html /tmp/ledger/index.html
cd /tmp/ledger && python3 -m http.server 8790 &
```

### Check If Already Running

```bash
lsof -i :8790
```

If already running, skip the server start. Just update data.json.

### Stop Server

```bash
kill $(lsof -t -i :8790) 2>/dev/null
```

---

## Companion Skills

- **REGTRAX** — Regex railroad visualizer (same architecture pattern)
- **REFRAX** — Code refactoring visualizer
- **THREATMAP** — Threat modeling visualizer
- **WITNESS** — Evidence timeline visualizer

---

## Security Checklist

- [ ] No external CDN or script tags — everything is inline
- [ ] No eval() or Function() constructor
- [ ] No localStorage/sessionStorage of sensitive data
- [ ] Server binds to localhost only (python http.server default)
- [ ] data.json contains only financial data, no executable code
- [ ] Template is read-only — Claude never modifies it at runtime
- [ ] No sensitive credentials or account numbers in data.json

---

## Quality Checklist

- [ ] All revenue streams have unique IDs
- [ ] starting_cash is a realistic number
- [ ] At least 2-3 scenarios provided (base + variations)
- [ ] Growth rates are monthly, not annual (convert if needed)
- [ ] Payment terms match real-world delays
- [ ] Timeline covers enough months to see the trend
- [ ] Server is running before telling user to open browser
- [ ] data.json is valid JSON (no trailing commas, proper quotes)
