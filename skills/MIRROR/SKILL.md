---
name: MIRROR
description: |
  Force counterarguments to your own recommendations. Use when: you've just made a
  recommendation and want to stress-test it, before committing to an approach, when
  you suspect confirmation bias, or any time "what am I missing?" needs answering.
  A cognitive debiasing tool that challenges your own thinking.
user-invocable: true
allowed-tools: Read, Write
---

# MIRROR

**Challenge your own recommendations. Find the blind spots.**

---

## Usage

```
/mirror                        - Challenge the last recommendation made
/mirror [topic]                - Challenge thinking on a specific topic
/mirror reflect "statement"    - Examine a specific statement for weaknesses
```

---

## What This Is

MIRROR is a self-check tool. After making a recommendation, invoke MIRROR to force genuine counterarguments against your own position. It selects from 8 challenge frameworks and applies the most relevant ones to your current context.

This isn't devil's advocacy for fun — it's a structured way to catch blind spots before they become mistakes.

---

## The 8 Challenge Frameworks

| Framework | Question It Asks |
|-----------|-----------------|
| **Devil's Advocate** | What are the strongest arguments AGAINST this approach? |
| **Alternative Paths** | What completely different approaches were not considered? |
| **Hidden Costs** | What are the non-obvious downsides or maintenance burdens? |
| **Failure Modes** | How could this fail? What's the worst-case scenario? |
| **Premature Optimization** | Is this solving a problem that doesn't exist yet? |
| **Reversibility** | How hard is it to undo this decision? What are we locking in? |
| **Second Order Effects** | What will this cause downstream? Unintended consequences? |
| **Expertise Blind Spots** | What would someone with a different background see? |

---

## How It Works

### Basic Mirror
When you invoke `/mirror`:
1. Select 3 challenge frameworks (contextually relevant or random)
2. Apply each framework to the most recent recommendation
3. Present the challenges clearly
4. **Reflect honestly** — if the challenges reveal genuine concerns, voice them

### Targeted Reflect
When you invoke `/mirror reflect "statement"`:
1. Analyze keywords in the statement
2. Select the most relevant frameworks:
   - "best/optimal/should" → Alternative Paths
   - "simple/quick/easy" → Hidden Costs
   - "future/scalable" → Premature Optimization
   - "never/always/definitely" → Devil's Advocate
3. Apply selected frameworks
4. Present counterarguments

---

## AUTO-EXECUTE Protocol

When this skill is invoked:

1. **Identify the target** — what recommendation or statement is being challenged
2. **Select 3 frameworks** — contextually relevant or semi-random
3. **Apply each framework genuinely** — don't softball the challenges
4. **Present the challenges** with clear formatting
5. **Conclude honestly:**
   - If the recommendation holds up → proceed with confidence
   - If concerns were found → flag them before continuing

---

## Output Format

```
══════════════════════════════════════════════════════
  MIRROR — Counterargument Mode
══════════════════════════════════════════════════════

  Challenging: [recommendation or statement]

  [1] HIDDEN COSTS
      What are the non-obvious downsides or maintenance burdens?

  [2] ALTERNATIVE PATHS
      What completely different approaches were not considered?

  [3] REVERSIBILITY
      How hard is it to undo this decision? What are we locking in?

──────────────────────────────────────────────────────

  Reflect on these angles before proceeding.
  If concerns are genuine, raise them.
  If the recommendation holds, proceed with confidence.

══════════════════════════════════════════════════════
```

---

## Prerequisites

- Claude Code (any model)
- No external packages or services required

---

## When to Use

- After making any significant technical recommendation
- Before committing to an architecture or framework choice
- When you catch yourself being too certain
- After a CONCLAVE debate, to stress-test the conclusion
- Any time "what am I missing?" is a useful question

---

*The mirror doesn't lie. Use it before you ship.*
