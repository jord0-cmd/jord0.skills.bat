# SPARK

<span class="tag tag-cognitive">cognitive</span>

**Divergent thinking engine. When standard approaches feel stale, SPARK explores the weird, wild long tail.**

Normal reasoning optimizes for the most likely answer. SPARK deliberately explores the unlikely ones — because sometimes the best solution is the one nobody would think of first.

---

## Usage

```
/spark How should we handle user onboarding?
```

```
/spark --wild What if we redesigned error handling from scratch?
```

```
/spark --count=8 Novel approaches to caching
```

---

## Divergent Thinking Prompts

SPARK uses these frames to break out of conventional thinking:

| Frame | Question |
|-------|----------|
| **Inversion** | What if we did the exact opposite? |
| **Constraint Removal** | What if [assumed constraint] didn't exist? |
| **Domain Transfer** | How is this solved in a completely unrelated field? |
| **Scale Shift** | What if this was 100x bigger? 100x smaller? |
| **Time Shift** | How would this be solved in 10 years? 100 years ago? |

---

## What You Get

5+ unconventional approaches, each evaluated on:

- **Novelty** — is this actually different from standard approaches?
- **Feasibility** — could this work with reasonable effort?
- **Insight** — even if we don't use this, does it reveal something useful?

Results are ranked by potential impact.

---

## When to Use It

- Brainstorming feels predictable
- Standard approaches don't fit
- You want to see what you're not seeing
- Innovation is the goal, not optimization
- Creative projects need fresh angles

!!! warning "Ideas, not implementations"
    SPARK generates ideas, not production code. Always validate before implementing. The value is in the perspective shift, not the raw output.

---

## Prerequisites

- Claude Code with Task tool (uses `tail-sampler` subagent)
- No external packages

---

*The best ideas are the ones you wouldn't have had.*
