# Decision Audit Trail

**Skills used:** CONCLAVE + MIRROR + ECHO

Debate it. Stress-test it. Record it. The bulletproof decision pipeline.

---

## The Problem

Big architectural decisions deserve more than a gut feeling. But most teams either:

1. **Decide too fast** — first idea wins, nobody challenges it
2. **Decide too slow** — endless meetings, analysis paralysis, decision by committee

You need a process that's thorough but fast. Rigorous but practical.

---

## The Pipeline

### Step 1: CONCLAVE — Let Them Fight

```
/conclave Should we use a monorepo or polyrepo for the microservices?
```

9 voices. 2 rounds. The minimalist argues for simplicity. The systems thinker maps the dependencies. The chaos agent breaks your assumptions. The builder asks if you can actually maintain it.

You get a synthesized recommendation with dissenting opinions preserved.

**Time: 2 minutes.**

### Step 2: MIRROR — Stress-Test the Winner

Take CONCLAVE's recommendation and throw it in the mirror:

```
/mirror The CONCLAVE recommends monorepo with Turborepo
```

MIRROR picks 3 challenge frameworks and genuinely argues against the recommendation:

- **Hidden Costs:** Monorepo tooling overhead, CI complexity, blame diffusion
- **Failure Modes:** One broken build blocks everyone, merge conflicts at scale
- **Reversibility:** Splitting a monorepo later is painful — how painful?

If the recommendation survives MIRROR, it's solid. If it doesn't, you just saved yourself months of regret.

**Time: 1 minute.**

### Step 3: ECHO — Carve It in Stone

The decision survived. Record it:

```
/echo create repo-architecture
```

Claude captures:

- **Decision:** Monorepo with Turborepo
- **Reasoning:** CONCLAVE synthesis + MIRROR survival
- **Alternatives:** Polyrepo (rejected — coordination overhead), monolith (rejected — scaling concerns)
- **Confidence:** 78%
- **Unknowns:** CI performance at 20+ packages, developer onboarding friction

**Time: 30 seconds.**

---

## Total Time: Under 4 Minutes

Compare that to a 45-minute architecture meeting where half the team is checked out and the decision is made by whoever talks loudest.

---

## When to Use This

- Technology selection (framework, database, hosting)
- Architecture patterns (monolith vs micro, REST vs GraphQL)
- Migration decisions (rewrite vs refactor vs abandon)
- Any decision you'll need to justify in 6 months

---

## Revisiting Decisions

Six months later, someone asks "why monorepo?"

```
/echo query "repo architecture"
```

Full context. Full reasoning. Full list of alternatives you already considered. No archaeology required.

---

## Tips

!!! tip "Skip CONCLAVE for small decisions"
    Not everything needs 9 voices. For smaller calls, go straight to MIRROR → ECHO. Save CONCLAVE for the decisions that keep you up at night.

!!! tip "Record the unknowns"
    ECHO captures unknowns for a reason. Revisit them periodically. When an unknown becomes known, update the echo.

!!! tip "Confidence thresholds"
    Below 60% confidence? The decision isn't ready. Research more (RECON), debate more (CONCLAVE), or accept you're making a bet and document it honestly.
