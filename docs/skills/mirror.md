# MIRROR

<span class="tag tag-cognitive">cognitive</span>

**Force counterarguments against your own recommendations. 8 challenge frameworks. Find the blind spots.**

You just recommended an approach. MIRROR makes Claude argue against it — genuinely, not performatively.

---

## Usage

```
/mirror
```

Challenges the last recommendation Claude made in the current session.

```
/mirror Should we migrate to TypeScript?
```

Challenges a specific proposition.

```
/mirror reflect "Microservices are the right architecture for this"
```

Challenges a stated belief.

---

## The 8 Challenge Frameworks

| Framework | Question |
|-----------|----------|
| **Devil's Advocate** | What's the strongest case against this? |
| **Alternative Paths** | What approaches haven't we considered? |
| **Hidden Costs** | What will this cost us that we're not seeing? |
| **Failure Modes** | How could this fail? What's the blast radius? |
| **Premature Optimization** | Are we solving a problem that doesn't exist yet? |
| **Reversibility** | If this is wrong, how hard is it to undo? |
| **Second Order Effects** | What happens because of what happens? |
| **Expertise Blind Spots** | What are we assuming because of our background? |

MIRROR selects 3 contextually relevant frameworks per invocation and applies them genuinely.

---

## When to Use It

- After any significant recommendation
- Before committing to an architecture
- When you have a gut feeling but want it tested
- When the team agrees too quickly (that's suspicious)
- Before writing an ECHO — stress-test first, record after

!!! tip "The MIRROR → ECHO flow"
    `/mirror` your recommendation. If it survives, `/echo create` it. Decisions that survive MIRROR are decisions you can trust.

---

## Prerequisites

- Claude Code (any model)
- No external packages

---

*The recommendation that survives its mirror is the one worth shipping.*
