# Session Preservation

**Skills used:** PORTAL + ECHO

The workflow that eliminates "where was I?" from your vocabulary.

---

## The Problem

You had a productive session. You made decisions, built features, hit your stride. Then you closed the terminal. Next session, you spend 15 minutes re-explaining context that Claude already knew an hour ago.

Multiply that by every session, every day, every project.

That's hours of your life, gone.

---

## The Solution

### End of Session

Before closing, two commands:

```
/echo create session-decisions
/portal create eod
```

**ECHO** captures the decisions you made and why. **PORTAL** captures everything else — what you were working on, which files you touched, what's next.

Takes 30 seconds. Saves 15 minutes tomorrow.

### Start of Session

```
/portal open eod
```

Claude reads the portal, integrates the context, and gives you a summary:

> *Restored context from yesterday. You were working on the auth middleware,
> decided to use refresh token rotation with httpOnly cookies. Next up:
> token revocation endpoint and integration tests. Files touched:
> src/auth/tokens.ts, src/middleware/auth.ts.*

You're back in flow. No re-explaining. No warmup. Just work.

### Need a Decision Refresher?

```
/echo query "Why did we choose token rotation?"
```

> *Decision: ECHO-4K2M — Refresh tokens rotate on every use (one-time).
> Reasoning: Prevents token theft replay attacks. Alternatives considered:
> long-lived refresh tokens (rejected — security risk), session-based auth
> (rejected — doesn't work for mobile). Confidence: 85%.*

---

## The Ritual

Make this a habit:

| When | What | Why |
|------|------|-----|
| **Session start** | `/portal open [last-portal]` | Restore context |
| **After big decisions** | `/echo create [name]` | Capture reasoning |
| **Before closing** | `/portal create eod` | Save everything |

That's it. Three touchpoints per session. The compound effect over weeks is enormous — you build a history of decisions, a chain of context, a record of your engineering journey.

---

## Advanced: Named Portals for Branches

Instead of generic `eod` portals, name them after what you're working on:

```
/portal create auth-middleware
/portal create api-redesign
/portal create perf-optimization
```

Now you can jump between workstreams:

```
/portal open auth-middleware     # Resume auth work
# ... do some work ...
/portal create auth-middleware   # Update the portal
/portal open api-redesign       # Switch to API work
```

Each workstream has its own preserved context. Switch freely without losing anything.

---

## Tips

!!! tip "Portal before branching"
    About to `git checkout` a different branch? Portal first. Different branches often mean different mental contexts.

!!! tip "Echo the non-obvious"
    Don't echo decisions that are obvious from the code. Echo the ones where future-you will wonder "why not the other way?"

!!! tip "Weekly cleanup"
    Old portals pile up. Once a week: `/portal list`, close the ones you'll never open again.
