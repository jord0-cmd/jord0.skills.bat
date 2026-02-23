# Deep Research Pipeline

**Skills used:** RECON + RECALL + ECHO

Research once, remember forever, document why it mattered.

---

## The Problem

You research a topic. Claude gives you a thorough answer. You close the session. Three weeks later, the same topic comes up. You research it again. Same answer. Same time spent. Same ground covered twice.

Knowledge should accumulate, not evaporate.

---

## The Pipeline

### Step 1: RECALL — Check What You Know

Before researching anything:

```
/recall WebSocket authentication
```

If it's already in your knowledge base, you're done. No API calls, no web search, no waiting. Instant retrieval.

If nothing comes back, proceed to step 2.

### Step 2: RECON — Go Deep

```
/recon WebSocket authentication best practices
```

RECON launches Claude's research agent, which:

- Decomposes the topic
- Searches multiple sources
- Synthesizes findings
- Generates a structured report

The report auto-saves to `knowledge/research/2026-02-22_websocket-auth.md` and the index updates.

### Step 3: ECHO — Mark the Decision

If the research informs a decision:

```
/echo create websocket-auth-approach
```

Now you have the research AND the decision it led to, both persistently stored.

---

## The Compound Effect

Week 1: You research 5 topics. Knowledge base: 5 entries.

Week 4: You've researched 20 topics. But you've also *recalled* 8 of them without re-researching. That's 8 web searches you didn't do, 8 times you got instant answers.

Month 3: Your knowledge base has 50+ entries. New projects start faster because half the decisions have prior research backing them. RECALL hits before RECON even needs to fire.

**This is how you get faster over time instead of starting from zero every session.**

---

## Real Example

```
# Monday — new project, need to choose a database
/recall time-series databases
# Nothing found

/recon --compare TimescaleDB vs InfluxDB vs QuestDB for IoT data
# Deep research saved to knowledge base

/echo create database-selection
# Decision recorded: TimescaleDB, with reasoning

# Thursday — another project needs time-series storage
/recall time-series databases
# Instant hit. Full research report from Monday.
# Decision already made and documented.
```

Two minutes on Thursday instead of twenty. Multiply across every topic you'll ever research.

---

## Tips

!!! tip "Tag consistently"
    RECON auto-generates tags. Review them. Add more if they're missing. Good tags make RECALL faster.

!!! tip "Research before deciding"
    Don't ECHO a decision before you've RECONed the alternatives. Informed decisions > gut decisions.

!!! tip "Share the knowledge base"
    If your `knowledge/` directory is in a shared repo, your team benefits from everyone's research. One person's RECON is the whole team's RECALL.
