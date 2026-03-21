# THREATMAP

<span class="tag tag-analysis">analysis</span>

**See your attack surface. Describe your system architecture and get an interactive force-directed threat model with STRIDE analysis and attack path simulation.**

Security architecture diagrams are usually static boxes and arrows in a slide deck. THREATMAP turns them into a living force-directed graph where threats orbit their targets, data flows pulse with sensitivity indicators, and you can simulate attacks propagating through your system in real time.

---

## The Problem THREATMAP Solves

You need to threat model your system. The whiteboard session produces a static diagram that's outdated by the next sprint. Nobody revisits it. When someone asks "what happens if the CDN is compromised?", nobody can trace the blast radius.

THREATMAP makes threat models interactive, updatable, and explorable. Describe your architecture, and Claude builds a living graph you can prod.

---

## Usage

Describe your system architecture or provide documentation. THREATMAP identifies assets, maps trust boundaries, applies STRIDE analysis, and renders an interactive force-directed graph.

```
Threat model our web app: React frontend, API gateway, three microservices, PostgreSQL, Redis cache
```

```
Here's our architecture diagram -- what are the security risks?
```

```
What happens if an attacker compromises the CDN?
```

### What You See

A force-directed graph with:

- **Hexagons** (cyan) -- processes and services
- **Rounded rectangles** (amber) -- data stores
- **Jagged shapes** (rose) -- external entities (untrusted)
- **Shields** (emerald) -- infrastructure (firewalls, WAFs)
- **Orbiting barnacles** -- STRIDE threats, colour-coded by category
- **Animated data flows** -- bezier curves with sensitivity indicators

Nodes are grouped into trust zones (External, DMZ, Internal, Secure) with distinct backgrounds.

---

## Key Features

| Feature | What It Does |
|---------|-------------|
| **Force-directed layout** | Drag nodes to rearrange, physics simulation keeps it readable |
| **STRIDE categorization** | Six threat categories with distinct colours and glyphs |
| **Severity visualization** | Critical threats vibrate, high threats tremble, low threats stay calm |
| **Attack path simulation** | Watch tendrils probe, exploits fire, and lateral movement spread |
| **Trust zone mapping** | External, DMZ, Internal, Secure zones with visual boundaries |
| **Data flow sensitivity** | Line width indicates data sensitivity (PII, auth tokens, public) |
| **Security controls overlay** | Toggle controls on/off to see their coverage |
| **Side panel inspector** | Click any node or threat for detailed analysis |

---

## Attack Simulation

Click a threat barnacle, then "Simulate Attack" in the panel:

1. **Tendrils** probe from the threat to the target
2. **Exploit arcs** fire when the target is compromised
3. **Lateral movement** spreads through connected data flows
4. Compromised nodes glow red with persistent **scars**
5. The blast radius becomes viscerally clear

---

## STRIDE Categories

| Category | Colour | Examples |
|----------|--------|----------|
| **Spoofing** | Violet | Credential theft, session hijacking |
| **Tampering** | Amber | SQL injection, parameter manipulation |
| **Repudiation** | Slate | Missing audit logs, unsigned transactions |
| **Information Disclosure** | Cyan | Data leaks, verbose errors |
| **Denial of Service** | Rose | DDoS, resource exhaustion |
| **Elevation of Privilege** | Crimson | IDOR, SSRF, container escape |

---

## How It Works Under the Hood

```
1. You describe your system architecture
2. Claude identifies assets, flows, threats, controls, and attack paths
3. Template HTML is copied to /tmp/threatmap/
4. Python http.server serves on port 8788
5. Browser loads the page and renders the force-directed graph
6. You ask questions -> Claude updates data.json -> graph morphs live
```

---

## Live Updates

THREATMAP polls for changes automatically. Add a new service, revise threats, deploy controls -- the graph morphs in place. No refresh needed.

---

## Pairs With

- **ARBITER** -- Complement technical threats with contractual risk analysis
- **WITNESS** -- Reconstruct what happened after a breach
- **STRICT** -- Apply coding standards to reduce the attack surface

---

## Prerequisites

- Python 3 (for `http.server` -- included in all Python installs)
- A modern browser
- No other dependencies

---

*See your attack surface. Then burn it down.*
