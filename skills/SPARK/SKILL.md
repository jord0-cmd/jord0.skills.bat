---
name: SPARK
description: |
  Break out of conventional thinking. Use when: brainstorming feels predictable, standard
  approaches have failed, creative challenges need unconventional solutions, or when
  exploring radical alternatives. Invokes Claude's built-in tail-sampler agent to explore
  low-probability solution spaces that standard reasoning avoids.
user-invocable: true
allowed-tools: Read, Write, Bash, Grep, Glob, WebSearch, WebFetch
---

# SPARK

**Break the pattern. Find the unexpected solution.**

---

## Usage

```
/spark [problem or question]
/spark --wild [topic]              - Maximum divergence, no safety nets
/spark --count=N [topic]           - Generate N distinct approaches (default: 5)
```

---

## What This Is

SPARK generates unconventional, non-obvious approaches to problems. While standard reasoning optimizes for the most likely correct answer, SPARK deliberately explores the long tail — the weird, surprising, and counterintuitive ideas that conventional thinking filters out.

This isn't random brainstorming. It's structured divergent thinking using Claude's `tail-sampler` agent, which is specifically designed to break out of predictable solution spaces.

---

## How It Works

### 1. Problem Framing
SPARK reframes your problem from multiple unusual angles:
- Inversion: What if we did the exact opposite?
- Constraint removal: What if [assumed constraint] didn't exist?
- Domain transfer: How is this problem solved in [unrelated field]?
- Scale shift: What if this was 100x bigger? 100x smaller?
- Time shift: How would this be solved in 10 years? 100 years ago?

### 2. Divergent Generation
Using Claude's `tail-sampler` agent, SPARK generates ideas that deliberately avoid the top of the probability distribution — the conventional answers. It samples from the tails where surprising connections live.

### 3. Evaluation
Each generated idea is evaluated for:
- **Novelty** — is this actually different from standard approaches?
- **Feasibility** — could this work with effort, or is it pure fantasy?
- **Insight** — even if impractical, does this reveal something useful?

---

## AUTO-EXECUTE Protocol

When this skill is invoked:

1. **Parse the problem** from the user's message
2. **Launch the tail-sampler agent** (Task tool, subagent_type: `tail-sampler`)
3. **Frame the problem** with the divergent thinking prompts
4. **Generate 5+ unconventional approaches** (or count specified)
5. **Evaluate each** for novelty, feasibility, and insight
6. **Present results** ranked by potential impact

---

## Output Format

```
══════════════════════════════════════════════════════
  SPARK — Divergent Solutions
══════════════════════════════════════════════════════

  Problem: [restated problem]

  [1] THE INVERSION
      What if instead of X, we did Y?
      Novelty: High | Feasibility: Medium
      Insight: [what this reveals]

  [2] THE DOMAIN TRANSFER
      In [field], they solve this by...
      Novelty: High | Feasibility: High
      Insight: [what this reveals]

  [3] THE CONSTRAINT BREAKER
      Remove [assumption] and suddenly...
      Novelty: Medium | Feasibility: Low
      Insight: [what this reveals]

  ...

══════════════════════════════════════════════════════

  Wildcard: [one truly out-there idea]

══════════════════════════════════════════════════════
```

---

## When to Use

- Brainstorming sessions where initial ideas feel too predictable
- Design challenges requiring fresh perspectives
- Problem-solving when standard approaches have failed
- Innovation workshops seeking radical alternatives
- Creative projects needing unexpected angles
- When you're stuck and need to think differently

---

## When NOT to Use

- When you need the most reliable, proven solution
- Time-critical debugging (use STRICT, not SPARK)
- When the answer is well-known and just needs implementing
- Compliance or safety-critical decisions (divergence is the enemy)

---

## Prerequisites

- **Claude Code** with Task tool access (the `tail-sampler` is a built-in Claude Code subagent — no external setup needed)
- No external packages required

**Important:** SPARK generates unconventional *ideas*, not production code. Always validate SPARK output before implementing. The value is in the insights and angles, not in copy-paste solutions.

---

*The obvious answer is the first one everyone thinks of. The best answer is often the fifth.*
