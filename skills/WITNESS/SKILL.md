---
name: WITNESS
description: |
  INVOKE THIS SKILL when: reconstructing timelines from evidence, analyzing incident
  chronologies, investigating events from multiple sources, correlating logs with
  testimony, visualizing forensic timelines, or when users paste interview transcripts,
  log files, news articles, or reports for chronological analysis. Generates interactive
  multi-track timelines with source reliability encoding and contradiction detection.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# WITNESS — Forensic Timeline Reconstructor

> "Every event has a witness. Every witness tells a story. Not all stories agree."

**Author:** jord0 | **Version:** 1.0

---

## Prerequisites

- Python 3 (for `http.server`)
- Modern browser (Chrome, Firefox, Safari, Edge)

---

## Usage

Paste evidence into the terminal — logs, transcripts, reports, financial records. WITNESS extracts events, maps entities, grades source reliability, and renders an interactive multi-track timeline.

```
Reconstruct what happened from these server logs and the IT admin's statement
```

```
Build a timeline from this incident report — cross-reference with the badge access data
```

```
I have three witness statements about the same event — show me where they contradict
```

### What You See

A dark timeline (the Excavation Trench) with swimlane tracks per entity. Sharp cyan blocks for machine logs, blurry amber smears for uncertain testimony. Magenta fracture zones where sources contradict. Gold dashed lines (Surveyor's Tape) tracing causal chains above the evidence. Click any event to see the full source chain in the Spectrometer panel.

---

## When to Invoke

- User pastes logs, transcripts, reports, or evidence for timeline analysis
- User asks to "reconstruct", "timeline", "chronology", or "what happened"
- User mentions incident investigation, forensics, or event correlation
- User has multiple sources describing the same events
- User asks about contradictions between accounts
- User says "when did", "sequence of events", "timeline of"

---

## How It Works

### The Flow

```
1. User pastes evidence (logs, transcripts, reports)
2. You extract events with timestamps, entities, sources, confidence
3. Copy template → /tmp/witness/index.html
4. Write analysis → /tmp/witness/data.json
5. Start local server on port 8792
6. User opens browser, explores the interactive timeline
7. User adds more evidence → you update data.json → timeline morphs
```

### Step-by-Step

#### 1. Set Up the Server (First Time)

```bash
mkdir -p /tmp/witness
cp ~/.claude/skills/WITNESS/references/template.html /tmp/witness/index.html
```

#### 2. Extract Events

For each piece of evidence, extract:
- **Timestamp**: Exact ISO 8601 or fuzzy `{ earliest, latest, precision }`
- **Description**: What happened
- **Type**: `fact` (machine-recorded), `assertion` (human claim), `inference` (analyst deduction)
- **Entities**: Who/what was involved
- **Source**: Where this information came from
- **Confidence**: 0.0 to 1.0 (how certain)
- **Admiralty Grade**: A1-F6 (source reliability × information confidence)

#### 3. Write data.json and Start Server

```bash
cd /tmp/witness && python3 -m http.server 8792 &
```

#### 4. Update Live

Add more evidence → rewrite data.json → browser morphs automatically.

---

## The data.json Contract

### Top-Level Structure

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `meta` | object | yes | Case metadata |
| `entities` | array | yes | People, devices, locations involved |
| `sources` | array | yes | Evidence sources with reliability |
| `events` | array | yes | All extracted events |
| `causal_links` | array | no | Inferred cause-effect relationships |
| `corroborations` | array | no | Events confirmed by multiple sources |
| `conflicts` | array | no | Contradictions between sources |
| `gaps` | array | no | Expected evidence that is missing |

### Key Schema Details

See the full schema in the blueprint. Key points:
- Timestamps can be exact ISO strings or fuzzy objects: `{ earliest, latest, display, precision }`
- Entity types: `person`, `organisation`, `device`, `location`, `vehicle`, `account`, `phone`
- Source types: `system_log`, `testimony`, `document`, `email`, `chat`, `news`, `surveillance`, `financial`, `forensic`, `inference`
- Event types: `fact`, `assertion`, `inference`
- Confidence: 0.0-1.0 maps to visual blur (0=invisible fog, 1=razor sharp)

---

## Serving Instructions

### Start Server

```bash
mkdir -p /tmp/witness
cp ~/.claude/skills/WITNESS/references/template.html /tmp/witness/index.html
cd /tmp/witness && python3 -m http.server 8792 &
```

### Check / Stop

```bash
lsof -i :8792
kill $(lsof -t -i :8792) 2>/dev/null
```

---

## Security Checklist

- [ ] No external CDN or script tags
- [ ] No eval() or Function() constructor
- [ ] No localStorage/sessionStorage of sensitive data
- [ ] Server binds to localhost only
- [ ] Template is read-only at runtime

---

## Quality Checklist

- [ ] All events have timestamps, descriptions, and confidence levels
- [ ] Sources are graded for reliability
- [ ] Contradictions are explicitly identified, not hidden
- [ ] Inferences clearly marked as type "inference"
- [ ] Entities properly linked to events
- [ ] data.json is valid JSON
