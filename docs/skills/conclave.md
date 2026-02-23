# CONCLAVE

<span class="tag tag-cognitive">cognitive</span>

**9-voice structured debate. Minimalist vs chaos agent vs philosopher. Let them fight before you decide.**

When you're facing a complex decision, CONCLAVE spins up 8 distinct reasoning perspectives plus a chairperson. They argue. They challenge. They find what you'd miss alone.

---

## Usage

```
/conclave Should we use GraphQL or REST for this API?
```

### Options

```
/conclave --brief [topic]        # Shorter output
/conclave --rounds=N [topic]     # Custom number of rounds (default: 2)
```

---

## The Council

| Voice | Role | Thinking Style |
|-------|------|---------------|
| **RAZE** | Minimalist | Strip it down. What's the simplest version? |
| **RIOT** | Chaos Agent | Break assumptions. What if everything you think is wrong? |
| **RHEA** | Systems Thinker | How does this connect to everything else? |
| **RUNE** | Philosopher | What's the deeper principle at work? |
| **ROOK** | Builder | Can we actually build this? How? |
| **REED** | Empath | How does this affect the humans involved? |
| **RAZOR** | Skeptic | Prove it. Where's the evidence? |
| **RADIANCE** | Visionary | What's the boldest possible version? |
| **CHAIR** | Chairperson | Synthesize. What's the actual recommendation? |

---

## How It Works

**Round 1: Opening Positions**
Each voice states their position on the topic independently.

**Challenge Rounds**
Voices respond to each other. Agreements, disagreements, and new angles emerge.

**Synthesis**
The CHAIR weighs all perspectives and delivers a structured recommendation with confidence levels.

---

## When to Use It

- **Architectural decisions** — monolith vs microservices, database selection, API design
- **Design tradeoffs** — performance vs readability, flexibility vs simplicity
- **Strategic choices** — build vs buy, technology adoption, migration timing
- **Creative blocks** — stuck on an approach, need fresh angles
- **Feature prioritization** — limited bandwidth, many options

!!! warning "Not for simple questions"
    Don't use CONCLAVE to decide variable names. Use it when the decision has real consequences and multiple valid approaches.

---

## Prerequisites

- Claude Code (any model)
- No external packages

---

*Nine minds. One recommendation. Better decisions.*
