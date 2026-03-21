# LEDGER

<span class="tag tag-analysis">analysis</span>

**Watch your money breathe. Describe your business financials and get a kinetic SVG visualization with cash flow projections, runway analysis, and scenario modeling.**

Spreadsheets are where financial intuition goes to die. LEDGER renders your cash flow as a living landscape -- revenue streams float above the equator as ghostly cyan blocks, expenses drain downward through crimson furnaces, and the cash reservoir rises and falls like terrain. Switch between scenarios and watch the landscape morph.

---

## The Problem LEDGER Solves

You need to know: how long will our money last? What if growth slows? What if we hire two more engineers?

Traditional financial modeling means building a spreadsheet, staring at rows of numbers, and hoping your formulas are right. LEDGER makes the answer visual and interactive -- you see the cliff coming, not just the row where the number goes negative.

---

## Usage

Describe your business situation -- revenue, expenses, cash on hand, growth assumptions. LEDGER structures the data, computes projections, and renders the visualization.

```
We have $500K in the bank, $30K/mo revenue growing 8% monthly, $45K/mo burn rate. How long do we have?
```

```
Model our SaaS financials with three scenarios: base, optimistic, pessimistic
```

```
We're planning to hire 3 engineers in Q3 -- show me the impact on runway
```

### What You See

A Cartesian landscape:

- **Above the equator** (y=0): Revenue ghosts -- hatched cyan blocks with payment delay offsets
- **The equator**: The settlement line where money changes hands
- **Below the equator**: The cash reservoir -- dark dense terrain that rises and falls
- **Below the reservoir**: OPEX furnace (crimson), COGS parasites (amber), taxes (slate), CAPEX diamonds (violet)
- **The cliff**: Where cash hits zero -- red line with black void beyond

---

## Key Features

| Feature | What It Does |
|---------|-------------|
| **Cash flow projection** | Monthly cash balances with growth, churn, and payment delays |
| **Runway meter** | HUD showing months remaining, burn rate, and break-even point |
| **Scenario comparison** | Animated transitions between base, optimistic, pessimistic |
| **Probability corridor** | Translucent area between best and worst case |
| **OPEX breakdown** | Click any expense pipe to expand into sub-categories |
| **Revenue ghosts** | Payment terms create ghost blocks offset from recognition |
| **Playhead** | Hover across the chart to see exact figures at any month |
| **Hazard warning** | Acid yellow pulse when runway drops below 3 months |

---

## The Visual Language

| Element | Colour | Meaning |
|---------|--------|---------|
| Revenue ghosts | Cyan + diagonal hatching | Recognized revenue (not yet received) |
| Cash reservoir | Dark slate to deep cobalt gradient | Actual cash on hand |
| OPEX furnace | Crimson thermal gradient | Operating expenses burning cash |
| COGS parasites | Amber | Cost of goods (percentage of revenue) |
| Taxes | Slate (cold, mechanical) | Tax obligations |
| CAPEX diamonds | Violet | One-time capital expenditures |
| Cliff/failure | Red line + black void | Cash hits zero |
| Hazard zone | Acid yellow pulse | Less than 3 months runway |

---

## How It Works Under the Hood

```
1. You describe your financial situation
2. Claude structures revenue, expenses, scenarios into data.json
3. Template HTML is copied to /tmp/ledger/
4. Python http.server serves on port 8790
5. Browser loads the page and renders the financial landscape
6. You ask questions -> Claude updates data.json -> visualization morphs live
```

The financial engine handles compound/linear growth, monthly churn, payment term delays (net-30, net-60, net-90), quarterly/annual tax calculations, and scenario adjustments -- all computed client-side from the data.

---

## Live Updates

LEDGER polls for changes automatically. Add a new hire, adjust growth assumptions, create a new scenario -- the landscape morphs in place. The runway meter recalculates instantly.

---

## Pairs With

- **ARBITER** -- See the financial impact of contract terms
- **THREATMAP** -- Quantify the financial risk of security threats
- **ECHO** -- Record the reasoning behind financial decisions

---

## Prerequisites

- Python 3 (for `http.server` -- included in all Python installs)
- A modern browser
- No other dependencies

---

*Watch your money breathe.*
