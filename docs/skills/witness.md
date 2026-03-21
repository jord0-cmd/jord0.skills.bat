# WITNESS

<span class="tag tag-analysis">analysis</span>

**Reconstruct what happened from multiple sources. Paste logs, transcripts, and reports -- WITNESS builds an interactive forensic timeline with source reliability encoding and contradiction detection.**

Investigations deal in fragments. Server logs say one thing, witness statements say another, and the badge access records tell a third story. WITNESS lays them all on the same timeline, highlights where they agree, and flags where they contradict.

---

## The Problem WITNESS Solves

You have an incident. Multiple sources of evidence. Different formats, different timestamps, different levels of reliability. You need to know: what actually happened, and where do the stories conflict?

Traditional investigation means manually building a spreadsheet timeline, eyeballing timestamp overlaps, and hoping you catch the contradictions. WITNESS automates the assembly and makes conflicts impossible to miss.

---

## Usage

Paste evidence into the terminal -- logs, transcripts, reports, financial records. WITNESS extracts events, maps entities, grades source reliability, and renders an interactive timeline.

```
Reconstruct what happened from these server logs and the IT admin's statement
```

```
Build a timeline from this incident report -- cross-reference with the badge access data
```

```
I have three witness statements about the same event -- show me where they contradict
```

### What You See

A dark timeline (the Excavation Trench) with swimlane tracks per entity:

- **Cyan blocks** -- machine/system logs (high precision)
- **Amber blocks** -- human testimony (variable precision)
- **Violet blocks** -- documents and records
- **Green blocks** -- visual evidence (CCTV, photos)
- **Sharp blocks** = high confidence, **Blurry blocks** = low confidence
- **Magenta fracture zones** -- contradictions between sources
- **Gold dashed lines** -- causal inferences (Surveyor's Tape)

Click any event to open the Spectrometer panel with full source chain details.

---

## Key Features

| Feature | What It Does |
|---------|-------------|
| **Multi-source correlation** | Logs, testimony, documents, financial records on one timeline |
| **Confidence-based blur** | Low-confidence events appear blurry, snap into focus on hover |
| **Contradiction detection** | Magenta fracture zones where sources disagree |
| **Admiralty grading** | Source reliability x information confidence (A1-F6 scale) |
| **Causal chain mapping** | Gold dashed lines trace inferred cause-effect relationships |
| **Evidence gaps** | Pulsing markers where expected evidence is missing |
| **Entity swimlanes** | Each person/device/location gets their own track |
| **Core sample minimap** | Event density histogram at the bottom for navigation |

---

## Reading the Timeline

The **Flashlight effect**: hover over any blurry event to snap it into focus. This mirrors real investigation -- uncertain evidence becomes clearer when you look directly at it.

The **Spectrometer**: click any event to see its full evidence chain. Where did this information come from? How reliable is the source? Does it conflict with anything?

The **Fracture Ledger**: the left panel lists all detected contradictions. Click one to jump directly to the conflict zone.

---

## How It Works Under the Hood

```
1. You paste evidence (logs, transcripts, reports)
2. Claude extracts events with timestamps, entities, sources, confidence
3. Template HTML is copied to /tmp/witness/
4. Python http.server serves on port 8792
5. Browser loads the page and renders the timeline
6. You add more evidence -> Claude updates data.json -> timeline morphs live
```

---

## Live Updates

WITNESS polls for changes automatically. Add more evidence, and the timeline extends. Refine confidence levels, and blocks sharpen or blur. All in real time, no refresh.

---

## Pairs With

- **ARBITER** -- Combine contract analysis with incident reconstruction
- **THREATMAP** -- Map the security vulnerabilities that led to the incident
- **ECHO** -- Record your investigative decisions and reasoning

---

## Prerequisites

- Python 3 (for `http.server` -- included in all Python installs)
- A modern browser
- No other dependencies

---

*Every event has a witness. Not all stories agree.*
