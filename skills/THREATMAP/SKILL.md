---
name: THREATMAP
description: |
  INVOKE THIS SKILL when: analyzing system security, building threat models,
  visualizing attack surfaces, STRIDE analysis, or when users describe their
  system architecture and want to understand security risks. Generates interactive
  force-directed threat model diagrams with attack path simulation.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# THREATMAP — Visual Threat Model Generator

> "See your attack surface. Then burn it down."

**Author:** jord0 | **Version:** 1.0

---

## Prerequisites

- Python 3 (for `http.server`)
- Modern browser (Chrome, Firefox, Safari, Edge)

---

## Usage

Describe your system architecture or provide documentation. THREATMAP identifies assets, maps trust boundaries, applies STRIDE analysis, and renders an interactive force-directed threat model diagram.

```
Threat model our web app: React frontend, API gateway, three microservices, PostgreSQL, Redis cache
```

```
Here's our architecture diagram — what are the security risks?
```

```
What happens if an attacker compromises the CDN?
```

### What You See

A force-directed graph with colour-coded nodes grouped into trust zones. Hexagonal cyan nodes for processes, amber rounded rectangles for data stores, jagged rose shapes for external entities, emerald shields for infrastructure. STRIDE-categorised threat barnacles orbit each asset. Animated bezier data flows pulse with sensitivity indicators. Click nodes to inspect, drag to rearrange, simulate attacks to see blast radius.

---

## When to Invoke

- User asks to threat model a system or architecture
- User describes their infrastructure and wants to understand security risks
- User says "threat model", "STRIDE", "attack surface", "security diagram"
- User wants to visualize trust boundaries and data flows
- User needs to identify and prioritize threats across components
- User wants to simulate attack paths through their architecture

---

## Capability Lookup

| Task | THREATMAP Does |
|------|---------------|
| Threat model from architecture | Generate force-directed diagram with STRIDE threats |
| Visualize trust boundaries | Color-coded zones (External, DMZ, Internal, Secure) |
| Map data flows | Animated bezier paths with sensitivity indicators |
| STRIDE analysis | Categorized threat barnacles orbiting each asset |
| Simulate attacks | Animated attack path propagation with blast radius |
| Assess controls | Deploy/retract security controls overlay |

---

## How It Works

### The Flow

```
1. User describes their system architecture (or provides a diagram/docs)
2. You identify assets, trust boundaries, data flows, threats, and controls
3. Copy template → /tmp/threatmap/index.html
4. Write threat model → /tmp/threatmap/data.json
5. Start local server on port 8788
6. User opens browser, explores the force-directed threat graph
7. User asks for changes → you update data.json → graph morphs live
```

### Step-by-Step

#### 1. Set Up the Server (First Time)

```bash
mkdir -p /tmp/threatmap
cp ~/.claude/skills/THREATMAP/references/template.html /tmp/threatmap/index.html
```

#### 2. Analyse the Architecture

When the user describes their system:

1. **Identify assets** — Every component: services, databases, queues, CDNs, firewalls
2. **Map trust boundaries** — Which zone does each asset live in? (External, DMZ, Internal, Secure)
3. **Trace data flows** — What talks to what? Protocols, encryption, sensitivity levels
4. **Apply STRIDE** — For each asset, consider Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege
5. **Score severity** — 0-10 scale based on impact and exploitability
6. **Identify controls** — Existing security measures and what they protect
7. **Map attack paths** — How would an attacker move laterally through the system?

#### 3. Write the Data File

Write `/tmp/threatmap/data.json` following the contract below.

#### 4. Start the Server

```bash
cd /tmp/threatmap && python3 -m http.server 8788 &
```

Run in background. Tell user to open `http://localhost:8788`.

**IMPORTANT — Tell the user this is interactive.** THREATMAP is a live visual page, not a
static report. After starting the server, always remind the user:

> "Open **http://localhost:8788** in your browser. This is an interactive threat model —
> click nodes to inspect assets and their threats, click threat barnacles to see severity
> and blast radius, drag nodes to rearrange the graph, hover to highlight data flows,
> and use the Controls button to deploy security measures. Click 'Simulate Attack' on
> threats with defined attack paths to watch exploitation propagate through the system.
> The page updates live whenever I refine the model — no need to refresh."

#### 5. Update the Model (Live)

When the user asks for changes (new assets, revised threats, updated controls), rewrite
`/tmp/threatmap/data.json`. The browser polls every 500ms and morphs automatically.

**Do NOT restart the server.** The poller handles everything.

---

## The data.json Contract

### Top-Level Structure

```json
{
  "title": "My Application Threat Model",
  "description": "Brief overview of the system",
  "assets": [ ... ],
  "dataFlows": [ ... ],
  "threats": [ ... ],
  "controls": [ ... ],
  "attackPaths": [ ... ]
}
```

### assets (required)

Array of asset objects representing system components:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier (e.g., "api-gateway") |
| `name` | string | yes | Display name (e.g., "API Gateway") |
| `type` | string | yes | "process", "datastore", "external", "infrastructure" |
| `subtype` | string | no | Specific technology (e.g., "PostgreSQL", "nginx") |
| `zone` | string | yes | Trust zone: "external", "dmz", "internal", "secure" |
| `criticality` | number | yes | 1-5 scale, affects node size |
| `description` | string | no | What this component does |

#### Node Types

| Type | Shape | Color | Use For |
|------|-------|-------|---------|
| `process` | Hexagon | Cyan `#22d3ee` | Services, APIs, applications |
| `datastore` | Rounded rect | Amber `#fbbf24` | Databases, caches, file storage |
| `external` | Jagged polygon | Rose `#fb7185` | Users, third-party APIs, browsers |
| `infrastructure` | Shield | Emerald `#34d399` | Firewalls, WAFs, load balancers |

#### Trust Zones

| Zone | Background | Use For |
|------|-----------|---------|
| `external` | Void `#05060a` | Untrusted: users, internet, third parties |
| `dmz` | Dark `#0f1318` | Semi-trusted: reverse proxies, CDN, WAF |
| `internal` | Blue-dark `#0c1229` | Trusted network: app servers, queues |
| `secure` | Teal-dark `#081a1a` | Highly trusted: databases, secrets, PKI |

### dataFlows (required)

Array of data flow objects:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier |
| `source` | string | yes | Source asset ID |
| `target` | string | yes | Target asset ID |
| `label` | string | no | Flow description (e.g., "Auth tokens") |
| `protocol` | string | no | Protocol used (e.g., "HTTPS", "gRPC") |
| `sensitivity` | number | no | 1-4 (1=public routing, 4=PII/auth) — affects line width |
| `encrypted` | boolean | no | Whether the flow is encrypted (default true) |

### threats (required)

Array of threat objects:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier |
| `title` | string | yes | Short threat name |
| `stride` | string | yes | STRIDE category (see below) |
| `severity` | number | yes | 0-10 score |
| `assetId` | string | yes | Primary affected asset ID |
| `assets` | string[] | no | All affected asset IDs |
| `description` | string | no | Detailed threat description |
| `mitigation` | string | no | Recommended countermeasure |
| `attackPathId` | string | no | Links to an attack path for simulation |

#### STRIDE Categories

| Category | Color | Threat Examples |
|----------|-------|-----------------|
| `Spoofing` | Violet `#a78bfa` | Credential theft, session hijacking, IP spoofing |
| `Tampering` | Amber `#fbbf24` | SQL injection, parameter manipulation, MitM |
| `Repudiation` | Slate `#94a3b8` | Missing audit logs, unsigned transactions |
| `Information Disclosure` | Cyan `#22d3ee` | Data leaks, verbose errors, side channels |
| `Denial of Service` | Rose `#fb7185` | DDoS, resource exhaustion, algorithmic complexity |
| `Elevation of Privilege` | Crimson `#ef4444` | IDOR, SSRF, privilege escalation, container escape |

#### Severity Scale

| Range | Level | Visual | Description |
|-------|-------|--------|-------------|
| 9-10 | Critical | Deep Red, vibrating | Actively exploitable, catastrophic impact |
| 7-8.9 | High | Red-Orange, trembling | Likely exploitable, significant impact |
| 4-6.9 | Medium | Amber, steady | Exploitable with effort, moderate impact |
| 0.1-3.9 | Low | Teal, calm | Difficult to exploit or minimal impact |
| 0 | Info | Dim blue | Informational finding |

### controls (optional)

Array of security control objects:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier |
| `name` | string | yes | Control name (e.g., "WAF Rules") |
| `type` | string | no | "preventive", "detective", "corrective" |
| `description` | string | no | What this control does |
| `assets` | string[] | yes | Asset IDs this control protects |
| `mitigates` | string[] | no | Threat IDs this control addresses |

### attackPaths (optional)

Array of attack path objects for simulation:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier |
| `name` | string | no | Attack path name |
| `description` | string | no | How the attack progresses |
| `steps` | string[] | yes | Ordered array of asset IDs (attack path) |
| `threats` | string[] | no | Related threat IDs |

---

## AI Partnership Patterns

### Building a Threat Model from Scratch

When the user describes their architecture:

1. **Ask clarifying questions** — "Is the API publicly exposed? What auth mechanism? What data sensitivity?"
2. **Identify all components** — Don't miss infrastructure like load balancers, DNS, CDNs
3. **Map trust boundaries** — Group components by trust level
4. **Apply STRIDE systematically** — Consider each category for each component
5. **Score realistically** — Use CVSS-like reasoning for severity
6. **Define attack paths** — Trace how an attacker would pivot through the system
7. **Generate data.json** — Following the contract exactly
8. **Serve and explain** — Start server, walk user through the highest-risk findings

### Reviewing Existing Architecture

When the user has documentation or diagrams:

1. **Parse the architecture** — Identify all components and connections
2. **Map to THREATMAP format** — Assign types, zones, criticality
3. **Identify gaps** — Missing authentication, unencrypted flows, over-privileged services
4. **Generate threats** — Focus on the most impactful, not just the obvious
5. **Suggest controls** — Practical mitigations with effort estimates

### Iterative Refinement

The power move: user sees the graph, asks questions, you refine.

1. User: "What about if the CDN is compromised?"
2. You: Add new threats targeting the CDN, add attack path from CDN to internal services
3. You: Update data.json, graph morphs
4. User: "Can we add rate limiting?"
5. You: Add control, link it to DoS threats, redeploy

---

## Serving Instructions

### Start Server

```bash
mkdir -p /tmp/threatmap
cp ~/.claude/skills/THREATMAP/references/template.html /tmp/threatmap/index.html
cd /tmp/threatmap && python3 -m http.server 8788 &
```

### Check If Already Running

```bash
lsof -i :8788
```

If already running, skip the server start. Just update data.json.

### Stop Server

```bash
kill $(lsof -t -i :8788) 2>/dev/null
```

---

## Companion Skills

- **REGTRAX** — Regex railroad visualizer (same architecture)
- **REFRAX** — Visual code comprehension (same architecture)
- **CANVAS** — Immersive 3D web experiences
- **OPTIC** — AI image generation

---

## Security Checklist

- [ ] No external CDN or script tags — everything is inline
- [ ] No eval() or Function() constructor
- [ ] No localStorage/sessionStorage of sensitive data
- [ ] Server binds to localhost only (python http.server default)
- [ ] data.json contains only model data, no executable code
- [ ] Template is read-only — Claude never modifies it at runtime
- [ ] Severity scores are realistic, not inflated for drama

---

## Quality Checklist

- [ ] Every asset has a type, zone, and criticality
- [ ] STRIDE categories are correctly applied (not just guessing)
- [ ] Severity scores reflect actual risk, not just category
- [ ] Data flows include protocol and encryption status
- [ ] At least one attack path is defined for the highest-severity threat
- [ ] Controls reference the threats they mitigate
- [ ] data.json is valid JSON (no trailing commas, proper quotes)
- [ ] Server is running before telling user to open browser
