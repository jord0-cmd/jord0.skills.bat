---
name: locus
description: |
  INVOKE THIS SKILL when: making AI-generated images interactive, mapping clickable zones
  onto generated artwork, warping HTML content onto perspective surfaces in images,
  defining freeform polygon hotspots, creating hover/click states for elements in AI art,
  or performing surgical edits on specific regions of generated images. Contains four
  original techniques: CSI, IQM, HQW, and ADT.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# LOCUS — Interactive Image Toolkit

*Four original techniques for making static AI-generated images interactive.*

Developed by [jord0-cmd](https://github.com/jord0-cmd). These techniques were invented to solve real problems that existing tools don't address: how do you add hover states to AI art? How do you map HTML onto a perspective-distorted screen in a generated image? How do you define clickable zones on irregular shapes? LOCUS answers all of these.

**Requirements**: React 18+ environment. Components use hooks, refs, and modern React patterns. Works with any React framework (Next.js, Vite, Remix, etc.) or standalone React.

---

## Usage

Describe what you want to make interactive — hover states, perspective-warped content, polygon hotspots, or before/after comparisons. LOCUS provides the four techniques (CSI, IQM, HQW, ADT) and the collaborative human-in-the-loop workflow to map coordinates visually.

---

## How This Works — The Human-in-the-Loop

**CRITICAL**: LOCUS is a collaborative toolkit. You (Claude) build the pages and components. The **user** does the visual work in their browser. Do NOT guess coordinates — they will be wrong.

### The Core Loop

```
1. USER describes what they want ("overlay text on that monitor screen")
2. YOU build a tuner/tool page with the right LOCUS component
3. YOU start a dev server and give the user the URL
4. USER opens browser, visually positions/draws/drags things
5. USER copies the output (JSON coordinates) and pastes it back to you
6. YOU wire those exact coordinates into the production components
7. REPEAT until everything looks right
8. YOU ask how they want the final page saved and deliver it
```

**The user's eyes are the instrument.** Pixel-level alignment on AI-generated images cannot be done programmatically — perspective distortion, barrel lens effects, and artistic irregularity make every surface unique. The IQM DebugTuner and ADT drawing tools exist specifically so the human can do what code cannot: look at it and drag it until it's right.

### Dev Server — Required Dependency

Every LOCUS project needs a running dev server so the user can interact with the tools in their browser. When starting a LOCUS workflow:

```bash
# If the project doesn't exist yet, scaffold it:
npx create-next-app@latest locus-project --typescript --tailwind --app --src-dir --use-npm
cd locus-project
npm install dompurify @types/dompurify

# Start the dev server:
npm run dev
# → http://localhost:3000
```

**Always tell the user the URL.** Say: *"I've set up the tuner at http://localhost:3000/tuner — open that in your browser, drag the corners to match the screen edges, then click COPY POSITIONS and paste the JSON back to me."*

If the user doesn't have a project yet, scaffold one. If they do, add the tuner page to their existing project. The dev server is not optional — it is the interface.

### What You Build vs What They Do

| Step | Who | What |
|------|-----|------|
| Scaffold project & install deps | **You** | Create Next.js project, install packages |
| Build tuner/tool pages | **You** | Write DebugTuner, ADT tool, or CSI preview pages |
| Start dev server | **You** | `npm run dev`, give user the URL |
| Drag corners / draw polygons / tune positions | **User** | Visual work in the browser |
| Copy coordinates | **User** | Click COPY, paste JSON back to chat |
| Wire coordinates into production code | **You** | Build HQW warps, CSI overlays, ADT hit zones |
| Visual review | **User** | Check it looks right, request adjustments |
| Final delivery | **You** | Ask format preference, save and clean up |

---

## Security — Read This First

These techniques involve DOM injection, coordinate transforms, and image processing. Before shipping:

- **Sanitize all DOM content** injected via CSI overlays (use DOMPurify)
- **Validate all coordinate inputs** — must be numeric, 0-100 range for percentages
- **Never `eval()` coordinate data** from external sources — use `JSON.parse()` only
- **Validate `matrix3d` inputs** — never pass unsanitized user input to CSS transforms
- **Prevent path traversal** in image file references — no `../` in dynamic paths

Full security checklist at the end of this skill. These are non-negotiable.

---

## When to Invoke This Skill

- Adding hover/click/scroll states to elements within AI-generated images
- Mapping interactive content onto perspective-distorted surfaces (screens, monitors, signs)
- Defining clickable zones on irregular shapes in generated artwork
- Performing surgical edits on specific regions of AI images without affecting the rest
- Fitting HTML/text content into frames, screens, or panels within AI art
- Building interactive portfolios, landing pages, or experiences from AI-generated scene images
- Any time you need to make a static generated image feel alive

---

## The Four Techniques — Quick Reference

| Technique | Full Name | Purpose | Output |
|-----------|-----------|---------|--------|
| **CSI** | Contextual State Injection | AI-generated hover/click/scroll states | State overlay images |
| **IQM** | Interactive Quad Mapping | Visual coordinate tuner — drag corners to map zones | Quad coordinates (%) |
| **HQW** | Homography Quad Warp | Map rectangular content onto perspective surfaces | CSS `matrix3d()` transform |
| **ADT** | Area Drawing Tool | Freeform polygon hotspot definition | Polygon vertices (%) |

**Typical workflow**: IQM maps the TV screen quad -> HQW warps terminal text onto it -> CSI generates the hover glow state -> ADT defines the irregular smoke boundary for particle effects. IQM also positions CSI rectangular zones — same DebugTuner, multiple named quads.

---

## CSI — Contextual State Injection

*Originated in the jord0-cmd workshop, 2026. The technique that makes AI art interactive.*

CSI creates perfectly-integrated hover/click/scroll states for elements within AI-generated images. Instead of manual compositing, you feed the element back to an AI image generator as a reference image with instructions for the target state. The AI handles lighting, color grading, grain, and physical consistency automatically — because the new state is *derived from* the original.

### The CSI Pipeline

**Step 1 — Target**: Identify a static element in the image (switch, monitor, dial, light, gauge, text, sign).

**Step 2 — Extract**: Crop with 10% buffer. Record percentage coordinates relative to canvas:

```json
{
  "id": "panel_indicator_light",
  "source": "scene_base.png",
  "crop": { "top": "34.2%", "left": "18.7%", "width": "8.5%", "height": "12.1%" },
  "states": ["dim", "glow", "flicker"]
}
```

**Step 3 — Generate**: Feed the crop to your AI image generator as a reference image. Prompt for the target state change only — the reference forces consistent lighting, grain, and color:

```
Prompt: "Same element, same angle, same lighting. [STATE: The indicator light is now glowing bright amber]"
Reference: cropped_element.png
Aspect ratio: match the crop
```

This works for ANY visual change — lights, screens, mechanical parts, weather, damage states, time-of-day shifts. The reference image is the key innovation: it constrains the generator to produce only the state change, not a new interpretation.

**Step 4 — Integrate**: Position the overlay at the original coordinates. See the CSIOverlay component below.

**Step 5 — Blend**: Match black levels and color temperature to the base plate. Apply post-generation color grading if the generated state drifts slightly from the original palette.

### The CSIOverlay Component

```tsx
'use client'

import { useState, useCallback } from 'react'
import Image from 'next/image'
import DOMPurify from 'dompurify'

interface CSIOverlayProps {
  /** Path to the default/inactive state image */
  base: string
  /** Path to the active state image */
  active: string
  /** Position as percentage coordinates relative to the parent container */
  position: { top: string; left: string; width: string; height: string }
  /** Interaction trigger type */
  trigger: 'hover' | 'click' | 'scroll' | 'proximity'
  /** CSS mix-blend-mode for compositing */
  blendMode?: string
  /** Fade duration in seconds */
  transition?: number
  /** Optional accessible label for the interactive zone */
  ariaLabel?: string
  /** Optional HTML content to overlay (will be sanitized) */
  overlayContent?: string
}

/**
 * Sanitize any HTML content before injecting into the DOM.
 * Uses DOMPurify to strip scripts, event handlers, and dangerous attributes.
 */
function sanitizeContent(html: string): string {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['span', 'div', 'p', 'strong', 'em', 'br'],
    ALLOWED_ATTR: ['class', 'style'],
  })
}

export function CSIOverlay({
  base,
  active,
  position,
  trigger,
  blendMode = 'normal',
  transition = 0.3,
  ariaLabel,
  overlayContent,
}: CSIOverlayProps) {
  const [isActive, setIsActive] = useState(false)

  const handlers =
    trigger === 'hover'
      ? {
          onMouseEnter: () => setIsActive(true),
          onMouseLeave: () => setIsActive(false),
        }
      : trigger === 'click'
        ? { onClick: () => setIsActive((prev) => !prev) }
        : {}

  return (
    <div
      className="absolute cursor-pointer"
      style={{ ...position }}
      role="button"
      tabIndex={0}
      aria-label={ariaLabel}
      aria-pressed={trigger === 'click' ? isActive : undefined}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault()
          setIsActive((prev) => !prev)
        }
      }}
      {...handlers}
    >
      <Image src={base} alt="" fill className="object-cover" />
      <Image
        src={active}
        alt=""
        fill
        className="object-cover"
        style={{
          opacity: isActive ? 1 : 0,
          transition: `opacity ${transition}s ease`,
          mixBlendMode: blendMode as React.CSSProperties['mixBlendMode'],
        }}
      />
      {overlayContent && (
        <div
          className="absolute inset-0 flex items-center justify-center"
          dangerouslySetInnerHTML={{
            __html: sanitizeContent(overlayContent),
          }}
        />
      )}
    </div>
  )
}
```

### CSI Coordinate Mapping

**Critical — The Aspect-Ratio Container Pattern**: Do NOT use `object-fit: contain` on the base image for CSI overlays. The `object-contain` approach creates a gap between the container bounds and the rendered image area — CSS absolute positioning is relative to the *container*, not the letterboxed image, so all CSI zone positions will be offset.

**The correct pattern**: Wrap the image in a container that matches the image's aspect ratio. The image fills the container with `w-full h-full` (no object-fit needed). CSI zones then position correctly because the container IS the image bounds.

```tsx
{/* CORRECT — container matches image, zones align */}
<div className="relative max-w-full max-h-full" style={{ aspectRatio: '1376/768' }}>
  <img src="/scene.png" alt="Scene" className="w-full h-full" draggable={false} />

  {/* CSI zones — positioned relative to the container = image bounds */}
  <div className="absolute" style={{ top: '25%', left: '30%', width: '8%', height: '10%' }}>
    {/* zone content */}
  </div>
</div>

{/* WRONG — object-contain creates gap, zones drift */}
<div className="relative w-full h-full">
  <img src="/scene.png" className="w-full h-full object-contain" />
  <div className="absolute" style={{ top: '25%', left: '30%' }}>
    {/* THIS WILL BE OFFSET — positioned relative to container, not image */}
  </div>
</div>
```

**Note**: The DebugTuner uses `object-contain` internally because its SVG viewBox and percentage calculations account for it. But when building production CSI pages with CSS absolute positioning, always use the aspect-ratio container pattern instead.

### Using DebugTuner for CSI Zone Positioning

The DebugTuner is the universal positioning tool for CSI zones — not just HQW quads. A rectangular CSI zone is just a quad where all four corners form an axis-aligned rectangle. Load multiple named quads with distinct colors:

```tsx
// app/tuner/page.tsx — CSI Zone Tuner
'use client'
import { DebugTuner } from '@/components/locus/DebugTuner'

const INITIAL_QUADS = {
  lamp: {
    tl: [20, 22] as [number, number],  // Rough rectangles —
    tr: [32, 22] as [number, number],  // user drags to position
    bl: [20, 42] as [number, number],
    br: [32, 42] as [number, number],
  },
  gauges: {
    tl: [40, 5] as [number, number],
    tr: [74, 5] as [number, number],
    bl: [40, 23] as [number, number],
    br: [74, 23] as [number, number],
  },
  phone: {
    tl: [68, 62] as [number, number],
    tr: [78, 62] as [number, number],
    bl: [68, 78] as [number, number],
    br: [78, 78] as [number, number],
  },
}

export default function CSITunerPage() {
  return (
    <DebugTuner
      imageSrc="/scene.png"
      aspectRatio="1376/768"
      initialQuads={INITIAL_QUADS}
      colors={{ lamp: '#ffaa00', gauges: '#00ffff', phone: '#ff00ff' }}
    />
  )
}
```

The user drags each zone into position, clicks COPY POSITIONS, and pastes the JSON back. Then convert the quad corners to CSS rect positioning:

```typescript
// Convert quad tl/br corners to CSS positioning
// quad.tl = top-left corner, quad.br = bottom-right corner
function quadToCSS(quad: { tl: [number, number]; br: [number, number] }) {
  return {
    top: `${quad.tl[1]}%`,
    left: `${quad.tl[0]}%`,
    width: `${quad.br[0] - quad.tl[0]}%`,
    height: `${quad.br[1] - quad.tl[1]}%`,
  }
}

// Example: user pastes { lamp: { tl: [30.2, 25.2], tr: [38.1, 25.2], bl: [30.2, 34.9], br: [38.1, 34.9] } }
// → quadToCSS gives: { top: '25.2%', left: '30.2%', width: '7.9%', height: '9.7%' }
```

Wire these into CSI overlay `<div>` elements positioned absolutely within the aspect-ratio container.

### What CSI Can Generate

| Category | Example States |
|----------|---------------|
| **Lights** | off, dim, glow, flicker, alarm, color-shift |
| **Screens** | blank, boot sequence, running code, error, screensaver |
| **Mechanical** | lever up/down, dial positions, valve open/closed |
| **Text/Signage** | blank panel, stenciled warning, illuminated text |
| **Damage/Wear** | clean, dirty, damaged, repaired |
| **Weather** | clear, fog, rain on glass, frost |
| **Time-of-Day** | dawn, noon, dusk, night on the same scene |

### Security: DOM Sanitization

Any text content injected via CSI overlays must be sanitized before DOM insertion. The `sanitizeContent` utility above uses DOMPurify to strip scripts, event handlers, and dangerous attributes. Never use `dangerouslySetInnerHTML` with unsanitized input.

```typescript
// Sanitization utility — use for ANY dynamic content in overlays
import DOMPurify from 'dompurify'

export function sanitizeOverlayContent(html: string): string {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['span', 'div', 'p', 'strong', 'em', 'br', 'code'],
    ALLOWED_ATTR: ['class', 'style'],
    FORBID_ATTR: ['onclick', 'onerror', 'onload', 'onmouseover'],
  })
}
```

### Analogue Fork — CSI Without AI Generation

Not every user has access to an AI image generator. The Analogue Fork provides CSS-only state changes for CSI overlays:

```css
/* CSS filter approach — no AI generation needed */
.csi-zone {
  transition: filter 0.3s ease, opacity 0.3s ease;
}

.csi-zone:hover {
  filter: brightness(1.4) contrast(1.1) saturate(1.3);
}

.csi-zone[data-state="glow"] {
  filter: brightness(1.6) saturate(1.5) drop-shadow(0 0 8px var(--color-primary, #39ff14));
}

.csi-zone[data-state="dim"] {
  filter: brightness(0.4) saturate(0.3);
}

.csi-zone[data-state="alarm"] {
  filter: brightness(1.2) hue-rotate(340deg) saturate(2);
}
```

When a user says "I don't have OPTIC / Midjourney / DALL-E (or any AI image generator)" — use CSS filters on the cropped region instead. Less photorealistic than AI-generated states, but functional and immediate. Works with any static image.

---

## IQM — Interactive Quad Mapping

*Originated in the jord0-cmd workshop, February 2026. The technique that makes coordinate mapping drag-and-drop.*

### The Problem IQM Solves

AI-generated images have elements (monitors, screens, panels, signs, windows) that are almost never perfectly rectangular. They have subtle perspective distortion, barrel distortion, or artistic skew. Rectangular `{top, left, width, height}` overlays never fit. You need **quads** — four independent corners that can form any quadrilateral.

Before IQM, mapping coordinates meant: guess percentages, screenshot, compare, nudge, repeat — sometimes 4-5 rounds of trial and error. IQM eliminates this by rendering draggable corner handles directly on the image.

### When to Use IQM

- Mapping screen overlays onto AI-generated monitors
- **Positioning CSI click/hover zones** — the DebugTuner is the universal positioning tool for CSI rectangular zones too (see "Using DebugTuner for CSI Zone Positioning" below)
- Placing interactive content over any AI-generated image
- Mapping clickable zones onto concept art
- Fitting content into perspective-distorted frames
- Defining crop regions for surgical inpainting

### The DebugTuner Component (Drop-In)

Self-contained React component. The **universal positioning tool** for both HQW quad mapping AND CSI rectangular zone placement. Two interaction modes: **drag corners** to reshape individual quad vertices, and **drag inside a quad** to move it as a whole (all four corners shift together). Supports multiple named quads with distinct colors — use one quad per HQW surface or CSI zone. Set `DEBUG_CROP = true` to activate the tuner during development. Set `false` for production.

```tsx
'use client'

import { useCallback, useRef, useState } from 'react'

/** Quad type: each corner is [x%, y%] relative to the image container */
type Quad = {
  tl: [number, number] // top-left
  tr: [number, number] // top-right
  bl: [number, number] // bottom-left
  br: [number, number] // bottom-right
}

interface DebugTunerProps {
  /** Path to the image being mapped */
  imageSrc: string
  /** Aspect ratio of the image (e.g. '1792/592') */
  aspectRatio: string
  /** Initial quad positions — start with rough estimates */
  initialQuads: Record<string, Quad>
  /** Optional color per zone for visual distinction */
  colors?: Record<string, string>
}

export function DebugTuner({
  imageSrc,
  aspectRatio,
  initialQuads,
  colors = {},
}: DebugTunerProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [quads, setQuads] = useState<Record<string, Quad>>(initialQuads)
  const [dragging, setDragging] = useState<{
    screen: string
    corner: keyof Quad
  } | null>(null)
  const [moving, setMoving] = useState<{
    screen: string
    lastPct: [number, number]
  } | null>(null)
  const [copied, setCopied] = useState(false)

  /** Convert mouse event coordinates to percentage position */
  const getPct = useCallback(
    (clientX: number, clientY: number): [number, number] | null => {
      if (!containerRef.current) return null
      const rect = containerRef.current.getBoundingClientRect()
      return [
        Math.round(((clientX - rect.left) / rect.width) * 1000) / 10,
        Math.round(((clientY - rect.top) / rect.height) * 1000) / 10,
      ]
    },
    [],
  )

  const handleMouseDown =
    (screen: string, corner: keyof Quad) => (e: React.MouseEvent) => {
      e.preventDefault()
      e.stopPropagation()
      setDragging({ screen, corner })
    }

  /** Start whole-quad move when clicking inside a polygon */
  const handleQuadMouseDown = useCallback(
    (screen: string, clientX: number, clientY: number) => {
      const pct = getPct(clientX, clientY)
      if (pct) {
        setMoving({ screen, lastPct: pct })
      }
    },
    [getPct],
  )

  const handleMouseMove = useCallback(
    (e: React.MouseEvent) => {
      const pct = getPct(e.clientX, e.clientY)
      if (!pct) return

      if (dragging) {
        // Corner drag — reshape one vertex
        setQuads((prev) => ({
          ...prev,
          [dragging.screen]: {
            ...prev[dragging.screen],
            [dragging.corner]: [
              Math.max(0, Math.min(100, pct[0])),
              Math.max(0, Math.min(100, pct[1])),
            ],
          },
        }))
      } else if (moving) {
        // Whole-quad move — shift all four corners by the same delta
        const dx = pct[0] - moving.lastPct[0]
        const dy = pct[1] - moving.lastPct[1]
        setQuads((prev) => {
          const q = prev[moving.screen]
          return {
            ...prev,
            [moving.screen]: {
              tl: [q.tl[0] + dx, q.tl[1] + dy] as [number, number],
              tr: [q.tr[0] + dx, q.tr[1] + dy] as [number, number],
              bl: [q.bl[0] + dx, q.bl[1] + dy] as [number, number],
              br: [q.br[0] + dx, q.br[1] + dy] as [number, number],
            },
          }
        })
        setMoving((prev) =>
          prev ? { ...prev, lastPct: pct } : null,
        )
      }
    },
    [dragging, moving, getPct],
  )

  const handleMouseUp = useCallback(() => {
    setDragging(null)
    setMoving(null)
  }, [])

  const copyPositions = () => {
    const text = JSON.stringify(quads, null, 2)
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
    console.log('QUAD_POSITIONS =', text)
  }

  const defaultColor = '#84cc16'

  return (
    <div
      className="relative w-full h-full bg-black flex flex-col items-center justify-center select-none"
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
    >
      <div
        ref={containerRef}
        className="relative w-full max-w-[95vw] max-h-[80vh]"
        style={{ aspectRatio }}
      >
        {/* Base image */}
        <img
          src={imageSrc}
          alt="IQM Tuner"
          className="absolute inset-0 w-full h-full object-contain"
          draggable={false}
        />

        {/* SVG polygon outlines — interactive for whole-quad move */}
        <svg
          className="absolute inset-0 w-full h-full"
          viewBox="0 0 100 100"
          preserveAspectRatio="none"
          style={{ pointerEvents: 'none' }}
        >
          {Object.entries(quads).map(([key, q]) => {
            const c = colors[key] ?? defaultColor
            return (
              <polygon
                key={key}
                points={`${q.tl[0]},${q.tl[1]} ${q.tr[0]},${q.tr[1]} ${q.br[0]},${q.br[1]} ${q.bl[0]},${q.bl[1]}`}
                fill={`${c}15`}
                stroke={c}
                strokeWidth="0.3"
                style={{ pointerEvents: 'all', cursor: 'move' }}
                onMouseDown={(e) => {
                  e.preventDefault()
                  handleQuadMouseDown(key, e.clientX, e.clientY)
                }}
              />
            )
          })}
        </svg>

        {/* Draggable corner handles */}
        {Object.entries(quads).map(([screenKey, q]) => {
          const c = colors[screenKey] ?? defaultColor
          return Object.entries(q).map(([cornerKey, [x, y]]) => (
            <div
              key={`${screenKey}-${cornerKey}`}
              className="absolute z-50 cursor-crosshair"
              style={{
                left: `${x}%`,
                top: `${y}%`,
                transform: 'translate(-50%, -50%)',
              }}
              onMouseDown={handleMouseDown(
                screenKey,
                cornerKey as keyof Quad,
              )}
            >
              <div
                className="w-4 h-4 rounded-full border-2 border-black"
                style={{ background: c }}
              />
              <span
                className="absolute left-5 top-[-4px] text-[9px] font-mono whitespace-nowrap px-1 pointer-events-none"
                style={{ color: c, background: 'rgba(0,0,0,0.8)' }}
              >
                {screenKey[0].toUpperCase()}.{cornerKey} [{x.toFixed(1)},{' '}
                {y.toFixed(1)}]
              </span>
            </div>
          ))
        })}

        {/* Zone labels at center of each quad */}
        {Object.entries(quads).map(([key, q]) => {
          const cx = (q.tl[0] + q.tr[0]) / 2
          const cy = (q.tl[1] + q.bl[1]) / 2
          const c = colors[key] ?? defaultColor
          return (
            <div
              key={`label-${key}`}
              className="absolute font-mono text-xs font-bold pointer-events-none"
              style={{
                left: `${cx}%`,
                top: `${cy}%`,
                transform: 'translate(-50%, -50%)',
                color: c,
                textShadow: '0 0 8px rgba(0,0,0,0.9)',
              }}
            >
              {key.toUpperCase()}
            </div>
          )
        })}
      </div>

      <div className="mt-4 flex gap-4 font-mono text-xs">
        <button
          onClick={copyPositions}
          className="px-4 py-2 bg-lime-500 text-black font-bold tracking-wider cursor-pointer hover:bg-lime-400 transition-colors"
        >
          {copied ? 'COPIED!' : 'COPY POSITIONS'}
        </button>
        <span className="text-gray-500 self-center">
          Drag corners to reshape. Drag inside a quad to move it. Click COPY when done.
        </span>
      </div>
    </div>
  )
}
```

### Using the Tuner Output

The tuner exports JSON with percentage coordinates:

```json
{
  "left": {
    "tl": [4.3, 12.1],
    "tr": [32.6, 15.0],
    "bl": [5.0, 83.7],
    "br": [32.7, 78.1]
  }
}
```

Convert to a positioned element with `clip-path: polygon()`:

```tsx
export interface ScreenQuad {
  tl: [number, number]
  tr: [number, number]
  bl: [number, number]
  br: [number, number]
}

/** Calculate the axis-aligned bounding box of a quad (in %) */
function quadBounds(q: ScreenQuad) {
  const xs = [q.tl[0], q.tr[0], q.bl[0], q.br[0]]
  const ys = [q.tl[1], q.tr[1], q.bl[1], q.br[1]]
  const left = Math.min(...xs)
  const top = Math.min(...ys)
  const right = Math.max(...xs)
  const bottom = Math.max(...ys)
  return { left, top, width: right - left, height: bottom - top }
}

/** Convert quad corners to a CSS clip-path polygon relative to the bounding box */
function quadClipPath(
  q: ScreenQuad,
  bounds: ReturnType<typeof quadBounds>,
) {
  const toLocal = ([x, y]: [number, number]) => {
    const lx = ((x - bounds.left) / bounds.width) * 100
    const ly = ((y - bounds.top) / bounds.height) * 100
    return `${lx.toFixed(2)}% ${ly.toFixed(2)}%`
  }
  return `polygon(${toLocal(q.tl)}, ${toLocal(q.tr)}, ${toLocal(q.br)}, ${toLocal(q.bl)})`
}

// Usage: position with bounding box, clip to exact quad shape
const bounds = quadBounds(quad)
const clipPath = quadClipPath(quad, bounds)

<div
  style={{
    position: 'absolute',
    top: `${bounds.top}%`,
    left: `${bounds.left}%`,
    width: `${bounds.width}%`,
    height: `${bounds.height}%`,
    clipPath,
  }}
>
  {/* Your overlay content — images, video, interactive elements */}
</div>
```

### Expanding Quads Programmatically

If overlays are slightly too small (showing slivers of the underlying image at the edges), push all corners outward from the centroid:

```tsx
function expandQuad(q: ScreenQuad, amount: number): ScreenQuad {
  const cx = (q.tl[0] + q.tr[0] + q.bl[0] + q.br[0]) / 4
  const cy = (q.tl[1] + q.tr[1] + q.bl[1] + q.br[1]) / 4
  const push = ([x, y]: [number, number]): [number, number] => {
    const dx = x - cx
    const dy = y - cy
    const len = Math.sqrt(dx * dx + dy * dy)
    if (len === 0) return [x, y]
    return [x + (dx / len) * amount, y + (dy / len) * amount]
  }
  return {
    tl: push(q.tl),
    tr: push(q.tr),
    bl: push(q.bl),
    br: push(q.br),
  }
}
```

### The Full IQM Pipeline — Collaborative Workflow

IQM is a **human-interactive** tool. You build the tuner page; the user does the visual positioning. Do NOT hardcode quad coordinates by guessing — they will not align.

**Step 1: BUILD THE TUNER PAGE**

You create a dedicated route with the DebugTuner component, the user's image, and rough initial quad estimates:

```tsx
// app/tuner/page.tsx — You build this
'use client'
import { DebugTuner } from '@/components/locus/DebugTuner'

const INITIAL_QUADS = {
  screen_left: {
    tl: [15, 10] as [number, number],   // Rough guesses — the user
    tr: [35, 10] as [number, number],   // will drag these to the
    bl: [15, 45] as [number, number],   // correct positions
    br: [35, 45] as [number, number],
  },
}

export default function TunerPage() {
  return (
    <DebugTuner
      imageSrc="/scene.png"
      aspectRatio="1376/768"
      initialQuads={INITIAL_QUADS}
      colors={{ screen_left: '#39ff14' }}
    />
  )
}
```

**Step 2: START THE SERVER & DIRECT THE USER**

```bash
npm run dev
```

Tell the user exactly what to do:

> *"I've built the quad tuner at **http://localhost:3000/tuner** — open that in your browser. You'll see green dots on the image. Drag each corner so the quad outline sits exactly on the edges of the monitor screen. When it looks right, click **COPY POSITIONS** and paste the JSON back to me."*

Be specific. Name the URL. Explain what they'll see. Explain what to do.

**Step 3: USER TUNES IN THE BROWSER**

The user opens the URL, sees the image with draggable neon corner handles, and visually aligns the quad to the target surface. This is the step that makes LOCUS precise — no amount of coordinate guessing replaces the human eye.

**Step 4: USER PASTES COORDINATES BACK**

The user clicks COPY POSITIONS and pastes JSON like this into the chat:

```json
{
  "screen_left": {
    "tl": [17.2, 8.4],
    "tr": [34.8, 7.9],
    "bl": [17.5, 43.2],
    "br": [34.6, 42.8]
  }
}
```

**Step 5: YOU WIRE THE COORDINATES INTO PRODUCTION CODE**

Take the user's exact coordinates and build HQW warps, CSI overlays, clip-path elements — whatever the project needs.

**Step 6: REVIEW & ITERATE**

The user views the result on the dev server. If something's off, update the tuner with new quads and repeat. Each round gets closer. Usually 1-2 rounds is enough.

**Why this works**: The image IS the interface. The human eye does what pixel analysis and verbal descriptions cannot. Trying to skip the human step produces overlays that are always slightly wrong — and "slightly wrong" on a perspective surface looks terrible.

The `DebugTuner` component is reused for both steps: mapping source crops AND aligning final overlays. Same tool, different images, different purposes.

---

## HQW — Homography Quad Warp

*Originated in the jord0-cmd workshop, February 2026. The technique that makes text look painted on the glass.*

IQM maps coordinates and clips to shape. HQW goes further — it **warps the actual content** (text, HTML, anything) to match an arbitrary quadrilateral using CSS `matrix3d()`. Same math as OpenCV's `getPerspectiveTransform()`, but running in the browser with zero dependencies.

### When to Use HQW vs IQM

| Technique | Use When | Content Behavior |
|-----------|----------|------------------|
| **IQM + clip-path** | Overlaying images/video onto a quad | Content stays rectangular, clipped to quad shape |
| **HQW + matrix3d** | Overlaying text/HTML onto a surface with perspective | Content distorts to match the surface — text narrows, slopes, follows the plane |

If the TV screen narrows to the right and slopes downward, `clip-path` just crops — the text stays rectangular inside the crop. HQW makes the text perspective-match the surface, as if projected onto the glass.

### The Core Function (Zero Dependencies)

```javascript
/**
 * Compute CSS matrix3d() that warps a rectangle to an arbitrary quad.
 * Uses homography via Direct Linear Transform (DLT).
 *
 * @param {number} w - Source rectangle width (pixels)
 * @param {number} h - Source rectangle height (pixels)
 * @param {Array<{x:number, y:number}>} dst - Four destination corners: [TL, TR, BR, BL]
 * @returns {string} CSS transform value: "matrix3d(...)"
 *
 * CRITICAL: Set transform-origin: 0 0 on the element.
 * SECURITY: Validate all coordinate inputs are finite numbers before calling.
 */
function computeQuadWarp(w, h, dst) {
  // Validate inputs
  if (
    typeof w !== 'number' || typeof h !== 'number' ||
    !Number.isFinite(w) || !Number.isFinite(h) ||
    w <= 0 || h <= 0
  ) {
    console.error('computeQuadWarp: invalid source dimensions')
    return ''
  }
  for (const pt of dst) {
    if (!Number.isFinite(pt.x) || !Number.isFinite(pt.y)) {
      console.error('computeQuadWarp: non-finite coordinate detected')
      return ''
    }
  }

  const src = [
    { x: 0, y: 0 },
    { x: w, y: 0 },
    { x: w, y: h },
    { x: 0, y: h },
  ]

  function solve3x3(A, b) {
    const det =
      A[0] * (A[4] * A[8] - A[5] * A[7]) -
      A[1] * (A[3] * A[8] - A[5] * A[6]) +
      A[2] * (A[3] * A[7] - A[4] * A[6])
    if (det === 0) return null
    const invDet = 1 / det
    const adj = [
      (A[4] * A[8] - A[5] * A[7]) * invDet,
      (A[2] * A[7] - A[1] * A[8]) * invDet,
      (A[1] * A[5] - A[2] * A[4]) * invDet,
      (A[5] * A[6] - A[3] * A[8]) * invDet,
      (A[0] * A[8] - A[2] * A[6]) * invDet,
      (A[2] * A[3] - A[0] * A[5]) * invDet,
      (A[3] * A[7] - A[4] * A[6]) * invDet,
      (A[1] * A[6] - A[0] * A[7]) * invDet,
      (A[0] * A[4] - A[1] * A[3]) * invDet,
    ]
    return [
      adj[0] * b[0] + adj[1] * b[1] + adj[2] * b[2],
      adj[3] * b[0] + adj[4] * b[1] + adj[5] * b[2],
      adj[6] * b[0] + adj[7] * b[1] + adj[8] * b[2],
    ]
  }

  function adj3x3(m) {
    return [
      m[4] * m[8] - m[5] * m[7],
      m[2] * m[7] - m[1] * m[8],
      m[1] * m[5] - m[2] * m[4],
      m[5] * m[6] - m[3] * m[8],
      m[0] * m[8] - m[2] * m[6],
      m[2] * m[3] - m[0] * m[5],
      m[3] * m[7] - m[4] * m[6],
      m[1] * m[6] - m[0] * m[7],
      m[0] * m[4] - m[1] * m[3],
    ]
  }

  function mult3x3(a, b) {
    const c = []
    for (let i = 0; i < 3; i++)
      for (let j = 0; j < 3; j++) {
        let val = 0
        for (let k = 0; k < 3; k++) val += a[3 * i + k] * b[3 * k + j]
        c[3 * i + j] = val
      }
    return c
  }

  function basisToPoints(p1, p2, p3, p4) {
    const m = [p1.x, p2.x, p3.x, p1.y, p2.y, p3.y, 1, 1, 1]
    const s = solve3x3(m, [p4.x, p4.y, 1])
    if (!s) return null
    return [
      m[0] * s[0], m[1] * s[1], m[2] * s[2],
      m[3] * s[0], m[4] * s[1], m[5] * s[2],
      m[6] * s[0], m[7] * s[1], m[8] * s[2],
    ]
  }

  const srcBasis = basisToPoints(src[0], src[1], src[2], src[3])
  const dstBasis = basisToPoints(dst[0], dst[1], dst[2], dst[3])
  if (!srcBasis || !dstBasis) return ''

  const H = mult3x3(dstBasis, adj3x3(srcBasis))
  for (let i = 0; i < 9; i++) H[i] /= H[8]

  // Column-major for CSS matrix3d()
  return `matrix3d(${[
    H[0], H[3], 0, H[6],
    H[1], H[4], 0, H[7],
    0, 0, 1, 0,
    H[2], H[5], 0, H[8],
  ].join(',')})`
}
```

### The Oversized Source Trick

The destination quad on screen might only be ~150x170 pixels. If you set the source div to that size, text overflows and `overflow: hidden` clips it before the transform applies.

**Solution**: Render the source element LARGE (e.g. 500x600px), then let `matrix3d()` scale it down to fit the quad. The text renders comfortably in the large box, and the GPU downsamples it into the destination shape.

```css
.warped-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 500px;          /* Large source — NOT the destination size */
  height: 600px;
  transform-origin: 0 0; /* MANDATORY for homography math */
  background: transparent;
  overflow: hidden;
  /* GPU quality hints */
  backface-visibility: hidden;
  will-change: transform;
  -webkit-font-smoothing: antialiased;
  /* Use comfortable font sizes — matrix3d handles the scaling */
  font-size: 28px;
  padding: 40px 50px;
}
```

### Applying the Warp (with object-fit:contain handling)

When the background image uses `object-fit: contain`, you must calculate where the image actually renders within the container:

```javascript
/**
 * Apply the quad warp to a target element, accounting for object-fit: contain.
 *
 * @param {string} imageSelector - CSS selector for the background image element
 * @param {string} targetSelector - CSS selector for the element to warp
 * @param {ScreenQuad} quad - The quad coordinates (% of image)
 * @param {number} sourceW - Width of the oversized source element
 * @param {number} sourceH - Height of the oversized source element
 */
function applyQuadWarp(imageSelector, targetSelector, quad, sourceW, sourceH) {
  const imgEl = document.querySelector(imageSelector)
  const target = document.querySelector(targetSelector)
  const frame = imgEl.parentElement
  const fw = frame.offsetWidth
  const fh = frame.offsetHeight

  // Get actual image dimensions
  const natW = imgEl.naturalWidth || 1
  const natH = imgEl.naturalHeight || 1
  const imgAspect = natW / natH
  const frameAspect = fw / fh

  // object-fit:contain — calculate actual rendered image position
  let imgW, imgH, imgLeft, imgTop
  if (frameAspect > imgAspect) {
    imgH = fh
    imgW = fh * imgAspect
    imgLeft = (fw - imgW) / 2
    imgTop = 0
  } else {
    imgW = fw
    imgH = fw / imgAspect
    imgLeft = 0
    imgTop = (fh - imgH) / 2
  }

  // Convert quad % to pixel coords relative to container
  const q = quad
  const dst = [
    { x: imgLeft + (q.tl[0] / 100) * imgW, y: imgTop + (q.tl[1] / 100) * imgH },
    { x: imgLeft + (q.tr[0] / 100) * imgW, y: imgTop + (q.tr[1] / 100) * imgH },
    { x: imgLeft + (q.br[0] / 100) * imgW, y: imgTop + (q.br[1] / 100) * imgH },
    { x: imgLeft + (q.bl[0] / 100) * imgW, y: imgTop + (q.bl[1] / 100) * imgH },
  ]

  target.style.transform = computeQuadWarp(sourceW, sourceH, dst)
}

// Recompute on load and resize
const imgEl = document.querySelector('img')
imgEl.addEventListener('load', () => applyQuadWarp(/* ... */))
window.addEventListener('resize', () => applyQuadWarp(/* ... */))
if (imgEl.complete) applyQuadWarp(/* ... */)
```

### The HQW Pipeline

```
Step 1: Generate scene image (AI image generator)
Step 2: Color grade for atmosphere (optional)
Step 3: Build IQM tuner page, start dev server, give user the URL
Step 4: USER drags corners to map the target surface in their browser
Step 5: USER clicks COPY, pastes quad JSON back to chat
Step 6: Apply computeQuadWarp() with oversized source div using those coordinates
Step 7: User reviews result on dev server — iterate if needed
```

**Steps 3-5 are the human-in-the-loop.** See the IQM Collaborative Workflow section above. Do not skip this — guessed coordinates will not align correctly on perspective surfaces.

### Key Gotchas

1. **`transform-origin: 0 0` is MANDATORY** — The default `50% 50%` breaks all the math. Every element using `matrix3d()` from `computeQuadWarp` must have `transform-origin: 0 0`.
2. **`overflow: hidden` clips BEFORE transform** — That is why the oversized source trick exists. Render large, let matrix3d scale down.
3. **CSS rotateX/rotateY CANNOT do this** — They rotate in 3D space; they cannot map to an arbitrary quad. Only `matrix3d()` with homography gives independent corner control.
4. **Convex quads only** — Concave quads produce visual artifacts. All four corners must form a convex polygon.
5. **Pointer events respect the warp** — Links inside warped content are clickable at the warped position.
6. **Recompute on resize** — Pixel coordinates change with the viewport. Always `window.addEventListener('resize', recompute)`.
7. **Use naturalWidth/naturalHeight** — Never assume the image aspect ratio. Read it from the element after load.
8. **Validate coordinate inputs** — Never pass unsanitized user input into `matrix3d()` values. All coordinates must be validated as finite numbers (see the validation in `computeQuadWarp` above).

---

## ADT — Area Drawing Tool

*Originated in the jord0-cmd workshop. Freeform polygon hotspot definition for irregular shapes.*

### The Problem

Images with irregular interactive areas — freeform smoke regions above an ashtray, the pool of light from a lamp, a character's facial feature in a painting. Standard rectangular `<div>` hotspots cannot define these boundaries. You need freeform polygon regions, defined in percentage coordinates so they scale with the image.

### Three Drawing Modes

| Mode | Input | Output | Best For |
|------|-------|--------|----------|
| **Freeform** | Click and drag smooth paths | Simplified polygon vertices (%) | Organic shapes: smoke, light, water |
| **Polygon** | Click to place vertices, double-click to close | Exact polygon vertices (%) | Geometric shapes: signs, panels, windows |
| **Square** | Click and drag for perfect square | Pixel crop coordinates + % | Surgical inpainting regions |

All modes output coordinates as **percentage of image dimensions** — resolution-independent, works at any viewport size. Square mode additionally outputs pixel coordinates and crop commands.

### ADT Collaborative Workflow

Like IQM, ADT is a **human-interactive** tool. The user draws the polygon in their browser. You do NOT guess polygon coordinates.

1. **You** build a drawing tool page with the user's image and the appropriate drawing mode
2. **You** start the dev server and tell the user the URL
3. **The user** opens the URL, draws the polygon by clicking/dragging on the image
4. **The user** clicks SAVE/COPY and pastes the output coordinates back to the chat
5. **You** wire those coordinates into production code (clip-path, hit-testing, particle bounds)

Tell the user exactly what to do:

> *"I've set up the area drawing tool at **http://localhost:3000/draw** — open that in your browser. Click around the edge of the smoke area to place polygon points, then double-click to close the shape. Click COPY when you're happy with it and paste the coordinates back to me."*

### Douglas-Peucker Path Simplification

Freeform drawing captures hundreds of raw mouse points. Douglas-Peucker reduces these to the minimum vertices needed to represent the shape within a tolerance:

```javascript
/**
 * Perpendicular distance from point to line segment.
 * @param {{x:number,y:number}} point - The point to measure from
 * @param {{x:number,y:number}} lineStart - Start of line segment
 * @param {{x:number,y:number}} lineEnd - End of line segment
 * @returns {number} Distance from point to line
 */
function perpDist(point, lineStart, lineEnd) {
  const dx = lineEnd.x - lineStart.x
  const dy = lineEnd.y - lineStart.y
  const lenSq = dx * dx + dy * dy
  if (lenSq === 0) {
    const ex = point.x - lineStart.x
    const ey = point.y - lineStart.y
    return Math.sqrt(ex * ex + ey * ey)
  }
  const t = Math.max(0, Math.min(1, ((point.x - lineStart.x) * dx + (point.y - lineStart.y) * dy) / lenSq))
  const projX = lineStart.x + t * dx
  const projY = lineStart.y + t * dy
  const ex = point.x - projX
  const ey = point.y - projY
  return Math.sqrt(ex * ex + ey * ey)
}

/**
 * Douglas-Peucker path simplification.
 * Reduces a list of points to the minimum needed to represent the shape.
 *
 * @param {Array<{x:number,y:number}>} points - Raw input points
 * @param {number} tolerance - Maximum allowed perpendicular deviation
 * @returns {Array<{x:number,y:number}>} Simplified points
 */
function simplifyPath(points, tolerance) {
  if (points.length <= 2) return points
  let maxDist = 0
  let maxIdx = 0
  const start = points[0]
  const end = points[points.length - 1]

  for (let i = 1; i < points.length - 1; i++) {
    const d = perpDist(points[i], start, end)
    if (d > maxDist) {
      maxDist = d
      maxIdx = i
    }
  }

  if (maxDist > tolerance) {
    const left = simplifyPath(points.slice(0, maxIdx + 1), tolerance)
    const right = simplifyPath(points.slice(maxIdx), tolerance)
    return left.slice(0, -1).concat(right)
  }
  return [start, end]
}
```

**Tolerance**: `1.5` (in % units) is the recommended sweet spot — enough simplification for clean code, preserves shape fidelity.

### Output Formats

The tool exports three formats for each saved area:

**1. JS array** — for runtime hit-testing and particle boundaries:
```javascript
const AREAS = {
  smoke: [
    [25.03, 55.99],
    [29.39, 75.65],
    [31.42, 55.73],
    [26.92, 54.17],
    [24.45, 55.86],
  ],
}
```

**2. CSS clip-path** — for clipping elements to the polygon shape:
```css
clip-path: polygon(25.03% 55.99%, 29.39% 75.65%, 31.42% 55.73%);
```

**3. Bounding box** — derived from min/max of points, for spawn regions:
```javascript
const bbox = {
  left: 24.45,
  top: 54.17,
  right: 31.42,
  bottom: 75.65,
  width: 6.97,
  height: 21.48,
}
```

### Point-in-Polygon Hit Testing

For particle effects bounded to freeform areas, or click detection on irregular shapes, use ray casting:

```javascript
/**
 * Ray casting algorithm for point-in-polygon testing.
 * Works with any simple (non-self-intersecting) polygon.
 *
 * @param {number} x - Test point X coordinate
 * @param {number} y - Test point Y coordinate
 * @param {Array<[number,number]>} polygon - Array of [x, y] vertex pairs
 * @returns {boolean} True if point is inside the polygon
 */
function pointInPolygon(x, y, polygon) {
  let inside = false
  for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
    const [xi, yi] = polygon[i]
    const [xj, yj] = polygon[j]
    if (
      yi > y !== yj > y &&
      x < ((xj - xi) * (y - yi)) / (yj - yi) + xi
    ) {
      inside = !inside
    }
  }
  return inside
}
```

Use this for:
- Spawning particles only within a polygon boundary
- Soft boundary bouncing (reverse velocity when particle exits)
- Click detection on freeform regions (not just rectangular hotspots)
- Proximity triggers based on cursor position relative to irregular shapes

### Converting % to Canvas Pixels

ADT stores coordinates as image-relative percentages. To render on a canvas overlay, convert using the same `object-fit: contain` calculation from HQW:

```javascript
/**
 * Get the actual rendered position of an image using object-fit: contain.
 * @param {HTMLImageElement} imgEl - The image element
 * @returns {{ imgW: number, imgH: number, imgLeft: number, imgTop: number }}
 */
function getImageBounds(imgEl) {
  const frame = imgEl.parentElement
  const fw = frame.offsetWidth
  const fh = frame.offsetHeight
  const natW = imgEl.naturalWidth || 1
  const natH = imgEl.naturalHeight || 1
  const imgAspect = natW / natH
  const frameAspect = fw / fh

  if (frameAspect > imgAspect) {
    const imgH = fh
    const imgW = fh * imgAspect
    return { imgW, imgH, imgLeft: (fw - imgW) / 2, imgTop: 0 }
  } else {
    const imgW = fw
    const imgH = fw / imgAspect
    return { imgW, imgH, imgLeft: 0, imgTop: (fh - imgH) / 2 }
  }
}

/**
 * Convert percentage coordinates to canvas pixel coordinates.
 * @param {number} px - X percentage (0-100)
 * @param {number} py - Y percentage (0-100)
 * @param {{ imgW: number, imgH: number, imgLeft: number, imgTop: number }} bounds
 * @returns {[number, number]} Pixel coordinates [x, y]
 */
function pctToCanvas(px, py, bounds) {
  return [
    bounds.imgLeft + (px / 100) * bounds.imgW,
    bounds.imgTop + (py / 100) * bounds.imgH,
  ]
}
```

### Integration: The LOCUS Trilogy

ADT completes the interactive-image toolkit:

| Technique | Purpose | Output |
|-----------|---------|--------|
| **IQM** | Tune 4-corner positions for perspective mapping | Quad coordinates (%) |
| **HQW** | Map rectangular content onto perspective quad | `matrix3d()` transform |
| **ADT** | Define freeform interactive/particle regions | Polygon vertices (%) |

**Typical flow**: IQM places the TV screen quad -> HQW warps terminal text onto it -> ADT defines the smoke area above the ashtray and the light pool under the lamp.

---

## Surgical Inpainting — Edit Regions Without Touching the Rest

*Developed by jord0-cmd, 2026. Bridges ADT/CSI with AI image editing for pixel-perfect localized image edits.*

When you need to remove, replace, or alter a specific region of an AI-generated image without affecting the rest, do not send the whole image. Most AI image editors will drift on surrounding details. Instead: **isolate, edit, reintegrate.**

### When to Use

| Task | Technique |
|------|-----------|
| Remove baked-in smoke, particles, text, watermarks | Surgical Inpainting (removal) |
| Change a painting, screen, sign within a scene | Surgical Inpainting (state change) |
| Add an object into a specific location | Surgical Inpainting (addition) |
| Generate hover/click states for interactive elements | CSI (uses the same crop-edit-overlay pattern) |
| Full scene mood change (lighting, time of day) | Whole-image editing (not surgical) |

### The Pipeline

```
1. DEFINE — Use ADT Square mode to draw the edit region
     |
2. CROP  — Extract a pixel-perfect SQUARE from the source image
     |
3. EDIT  — Send to AI image editor with reference and 1:1 aspect ratio
     |
4. MATCH — Per-channel colour match (mean/std transfer per RGB)
     |
5. BLEND — Feathered composite back at original coordinates
```

### The Golden Rule

**ALWAYS use square crops with 1:1 aspect ratio.** This is non-negotiable. Most AI image editors change aspect ratio if you do not force it — even if the edit area is rectangular, pad it to a square. Non-square crops cause geometry drift that becomes visible in the composite.

### Prompting for Edits

Use **"Inpaint"** not "Edit" or "Change" — this triggers the localized editing pathway in most AI image generators. Key phrases:

- **"Keep surrounding pixels locked"** — enforces adherence to non-target regions
- **"Restrict changes strictly to the inner canvas area"** — bounds the edit zone
- **Never describe the container** — if editing a painting in a frame, only describe the painting content
- **"Maintain the exact noise pattern and compression artifacts"** — prevents seam-creating cleanup

**The Anchoring Principle**: For every ONE thing you change, anchor FIVE things you do not. AI image generators seek global coherence and will "improve" surrounding pixels unless explicitly told not to.

### Colour Matching Formula

After the AI edits the crop, colors will shift slightly. Match them back to the original:

```python
import numpy as np
from PIL import Image

def colour_match(edit_path, original_crop_path, output_path):
    """
    Per-channel mean/std colour transfer.
    Matches the edit's colour distribution to the original crop.

    Formula per channel: pixel = (pixel - edit_mean) * (orig_std / edit_std) + orig_mean
    """
    edit = np.array(Image.open(edit_path)).astype(np.float64)
    orig = np.array(Image.open(original_crop_path)).astype(np.float64)

    for ch in range(3):  # R, G, B
        e_mean = edit[:, :, ch].mean()
        e_std = edit[:, :, ch].std() or 1.0  # avoid division by zero
        o_mean = orig[:, :, ch].mean()
        o_std = orig[:, :, ch].std() or 1.0

        edit[:, :, ch] = (edit[:, :, ch] - e_mean) * (o_std / e_std) + o_mean

    edit = np.clip(edit, 0, 255).astype(np.uint8)
    Image.fromarray(edit).save(output_path)
    print(f"Colour matched: {output_path}")
```

### Feathered Compositing

Paste the colour-matched edit back with soft edges to prevent visible seams:

```python
from PIL import Image, ImageFilter

def feathered_composite(base_path, edit_path, crop_coords, output_path, feather_px=12, blur_px=3):
    """
    Composite the edited crop back onto the base image with feathered edges.

    Args:
        base_path: Path to the full base image
        edit_path: Path to the colour-matched edited crop
        crop_coords: (left, top, right, bottom) in pixels
        output_path: Where to save the result
        feather_px: Width of the alpha fade at edges (10-15px for ~250px crops)
        blur_px: Gaussian blur radius for the feather mask (3px recommended)
    """
    base = Image.open(base_path).convert('RGBA')
    edit = Image.open(edit_path).convert('RGBA')
    left, top, right, bottom = crop_coords

    # Resize edit to match crop dimensions if needed
    crop_w = right - left
    crop_h = bottom - top
    if edit.size != (crop_w, crop_h):
        edit = edit.resize((crop_w, crop_h), Image.LANCZOS)

    # Create feathered alpha mask
    mask = Image.new('L', (crop_w, crop_h), 255)
    pixels = mask.load()
    for y in range(crop_h):
        for x in range(crop_w):
            dist = min(x, y, crop_w - 1 - x, crop_h - 1 - y)
            if dist < feather_px:
                pixels[x, y] = int(255 * (dist / feather_px))

    # Blur the mask for smooth transitions
    mask = mask.filter(ImageFilter.GaussianBlur(radius=blur_px))

    # Composite
    edit.putalpha(mask)
    base.paste(edit, (left, top), edit)
    base.save(output_path)
    print(f"Composited: {output_path}")
```

**Feathering sweet spot**: 10-15px feather for ~250px crops, 3px Gaussian blur radius.

### Security: Image Processing

- **Validate image file types** before processing. Check MIME types, not just extensions.
- **Validate crop coordinates** are within image bounds. Do not allow negative values or values exceeding dimensions.
- **Sanitize file paths** — do not allow path traversal (`../`) in crop coordinate inputs or file references.

```python
import os
from pathlib import Path

def validate_image_path(path, allowed_dir):
    """Prevent path traversal attacks in image file references."""
    resolved = Path(path).resolve()
    allowed = Path(allowed_dir).resolve()
    if not str(resolved).startswith(str(allowed)):
        raise ValueError(f"Path traversal detected: {path}")
    return resolved

def validate_crop_coords(left, top, right, bottom, img_width, img_height):
    """Validate crop coordinates are within image bounds."""
    for val in [left, top, right, bottom]:
        if not isinstance(val, (int, float)) or val < 0:
            raise ValueError(f"Invalid coordinate: {val}")
    if right > img_width or bottom > img_height:
        raise ValueError(f"Crop exceeds image bounds: ({right}, {bottom}) > ({img_width}, {img_height})")
    if left >= right or top >= bottom:
        raise ValueError(f"Invalid crop region: ({left},{top}) to ({right},{bottom})")
    return True
```

---

## Debug Wireframe Plane

A toggle to visualize quad warp meshes and ADT polygons as bright neon wireframes during development. Essential for trusting the math before final compositing.

### DebugOverlay Component

```tsx
'use client'

import { useEffect, useRef } from 'react'

interface DebugOverlayProps {
  /** Whether the debug overlay is visible */
  enabled: boolean
  /** Quads to render as wireframes (IQM/HQW coordinates) */
  quads?: Record<string, {
    tl: [number, number]
    tr: [number, number]
    bl: [number, number]
    br: [number, number]
  }>
  /** Polygons to render as wireframes (ADT coordinates) */
  polygons?: Record<string, [number, number][]>
  /** Color scheme for different zones */
  colors?: Record<string, string>
  /** Reference to the image element for object-fit:contain calculation */
  imageRef: React.RefObject<HTMLImageElement>
}

export function DebugOverlay({
  enabled,
  quads = {},
  polygons = {},
  colors = {},
  imageRef,
}: DebugOverlayProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    if (!enabled || !canvasRef.current || !imageRef.current) return

    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    function draw() {
      const img = imageRef.current
      if (!img || !img.parentElement) return

      const frame = img.parentElement
      canvas.width = frame.offsetWidth
      canvas.height = frame.offsetHeight
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      // Calculate image bounds (object-fit: contain)
      const natW = img.naturalWidth || 1
      const natH = img.naturalHeight || 1
      const imgAspect = natW / natH
      const frameAspect = canvas.width / canvas.height

      let imgW: number, imgH: number, imgLeft: number, imgTop: number
      if (frameAspect > imgAspect) {
        imgH = canvas.height
        imgW = canvas.height * imgAspect
        imgLeft = (canvas.width - imgW) / 2
        imgTop = 0
      } else {
        imgW = canvas.width
        imgH = canvas.width / imgAspect
        imgLeft = 0
        imgTop = (canvas.height - imgH) / 2
      }

      const toPixel = (px: number, py: number): [number, number] => [
        imgLeft + (px / 100) * imgW,
        imgTop + (py / 100) * imgH,
      ]

      // Draw quads
      Object.entries(quads).forEach(([key, q]) => {
        const color = colors[key] || '#00ff41'
        const corners = [q.tl, q.tr, q.br, q.bl].map(([x, y]) => toPixel(x, y))

        ctx.strokeStyle = color
        ctx.lineWidth = 2
        ctx.setLineDash([6, 4])
        ctx.beginPath()
        ctx.moveTo(corners[0][0], corners[0][1])
        corners.forEach(([x, y]) => ctx.lineTo(x, y))
        ctx.closePath()
        ctx.stroke()

        // Corner dots
        ctx.setLineDash([])
        corners.forEach(([x, y]) => {
          ctx.fillStyle = color
          ctx.beginPath()
          ctx.arc(x, y, 4, 0, Math.PI * 2)
          ctx.fill()
        })

        // Label
        const cx = corners.reduce((s, [x]) => s + x, 0) / 4
        const cy = corners.reduce((s, [, y]) => s + y, 0) / 4
        ctx.fillStyle = color
        ctx.font = 'bold 11px monospace'
        ctx.textAlign = 'center'
        ctx.fillText(key.toUpperCase(), cx, cy)
      })

      // Draw polygons
      Object.entries(polygons).forEach(([key, pts]) => {
        const color = colors[key] || '#ff00ff'
        const pixels = pts.map(([x, y]) => toPixel(x, y))

        ctx.strokeStyle = color
        ctx.lineWidth = 2
        ctx.setLineDash([3, 3])
        ctx.beginPath()
        if (pixels.length > 0) {
          ctx.moveTo(pixels[0][0], pixels[0][1])
          pixels.forEach(([x, y]) => ctx.lineTo(x, y))
          ctx.closePath()
        }
        ctx.stroke()

        // Vertex dots
        ctx.setLineDash([])
        pixels.forEach(([x, y]) => {
          ctx.fillStyle = color
          ctx.beginPath()
          ctx.arc(x, y, 3, 0, Math.PI * 2)
          ctx.fill()
        })

        // Label
        if (pixels.length > 0) {
          const cx = pixels.reduce((s, [x]) => s + x, 0) / pixels.length
          const cy = pixels.reduce((s, [, y]) => s + y, 0) / pixels.length
          ctx.fillStyle = color
          ctx.font = 'bold 11px monospace'
          ctx.textAlign = 'center'
          ctx.fillText(key.toUpperCase(), cx, cy)
        }
      })
    }

    draw()
    window.addEventListener('resize', draw)
    return () => window.removeEventListener('resize', draw)
  }, [enabled, quads, polygons, colors, imageRef])

  if (!enabled) return null

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 pointer-events-none z-50"
      style={{ mixBlendMode: 'screen' }}
    />
  )
}
```

Usage:

```tsx
const imgRef = useRef<HTMLImageElement>(null)
const [debugMode, setDebugMode] = useState(false)

// Toggle with keyboard shortcut during development
useEffect(() => {
  const handler = (e: KeyboardEvent) => {
    if (e.key === 'd' && e.ctrlKey && e.shiftKey) {
      setDebugMode(prev => !prev)
    }
  }
  window.addEventListener('keydown', handler)
  return () => window.removeEventListener('keydown', handler)
}, [])

return (
  <div className="relative">
    <img ref={imgRef} src="/scene.webp" className="w-full object-contain" />
    <DebugOverlay
      enabled={debugMode}
      imageRef={imgRef}
      quads={{ screen: SCREEN_QUAD }}
      polygons={{ smoke: SMOKE_POLYGON }}
      colors={{ screen: '#00ff41', smoke: '#ff6b35' }}
    />
  </div>
)
```

---

## Ghost Mode — Before/After Comparison Slider

A slider for comparing surgical inpainting results against the original. Essential for fine-tuning feathering and colour matching. Drag the slider left/right to reveal the before or after state.

### CompareSlider Component

```tsx
'use client'

import { useCallback, useRef, useState } from 'react'

interface CompareSliderProps {
  /** Path to the original (before) image */
  before: string
  /** Path to the edited (after) image */
  after: string
  /** Initial slider position (0-100, default 50) */
  initialPosition?: number
  /** Aspect ratio of the images (e.g. '16/9') */
  aspectRatio?: string
  /** Label for the before state */
  beforeLabel?: string
  /** Label for the after state */
  afterLabel?: string
}

export function CompareSlider({
  before,
  after,
  initialPosition = 50,
  aspectRatio = '16/9',
  beforeLabel = 'BEFORE',
  afterLabel = 'AFTER',
}: CompareSliderProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [position, setPosition] = useState(initialPosition)
  const [isDragging, setIsDragging] = useState(false)

  const updatePosition = useCallback(
    (clientX: number) => {
      if (!containerRef.current) return
      const rect = containerRef.current.getBoundingClientRect()
      const x = Math.max(0, Math.min(clientX - rect.left, rect.width))
      setPosition((x / rect.width) * 100)
    },
    [],
  )

  const handleMouseDown = useCallback(
    (e: React.MouseEvent) => {
      e.preventDefault()
      setIsDragging(true)
      updatePosition(e.clientX)
    },
    [updatePosition],
  )

  const handleMouseMove = useCallback(
    (e: React.MouseEvent) => {
      if (!isDragging) return
      updatePosition(e.clientX)
    },
    [isDragging, updatePosition],
  )

  const handleMouseUp = useCallback(() => setIsDragging(false), [])

  const handleTouchMove = useCallback(
    (e: React.TouchEvent) => {
      if (e.touches.length > 0) {
        updatePosition(e.touches[0].clientX)
      }
    },
    [updatePosition],
  )

  return (
    <div
      ref={containerRef}
      className="relative select-none cursor-col-resize overflow-hidden"
      style={{ aspectRatio }}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
      onTouchStart={(e) => {
        setIsDragging(true)
        handleTouchMove(e)
      }}
      onTouchMove={handleTouchMove}
      onTouchEnd={() => setIsDragging(false)}
      role="slider"
      aria-label="Before/after comparison"
      aria-valuenow={Math.round(position)}
      aria-valuemin={0}
      aria-valuemax={100}
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'ArrowLeft') setPosition((p) => Math.max(0, p - 1))
        if (e.key === 'ArrowRight') setPosition((p) => Math.min(100, p + 1))
      }}
    >
      {/* After image (full) */}
      <img
        src={after}
        alt={afterLabel}
        className="absolute inset-0 w-full h-full object-contain"
        draggable={false}
      />

      {/* Before image (clipped) */}
      <div
        className="absolute inset-0 overflow-hidden"
        style={{ clipPath: `inset(0 ${100 - position}% 0 0)` }}
      >
        <img
          src={before}
          alt={beforeLabel}
          className="absolute inset-0 w-full h-full object-contain"
          draggable={false}
        />
      </div>

      {/* Slider line */}
      <div
        className="absolute top-0 bottom-0 w-0.5 bg-white z-10"
        style={{ left: `${position}%`, transform: 'translateX(-50%)' }}
      >
        {/* Handle */}
        <div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-white/90 border-2 border-white shadow-lg flex items-center justify-center"
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M5 3L2 8L5 13" stroke="#333" strokeWidth="2" strokeLinecap="round" />
            <path d="M11 3L14 8L11 13" stroke="#333" strokeWidth="2" strokeLinecap="round" />
          </svg>
        </div>
      </div>

      {/* Labels */}
      <div className="absolute top-3 left-3 font-mono text-xs bg-black/70 text-white px-2 py-1 rounded pointer-events-none">
        {beforeLabel}
      </div>
      <div className="absolute top-3 right-3 font-mono text-xs bg-black/70 text-white px-2 py-1 rounded pointer-events-none">
        {afterLabel}
      </div>
    </div>
  )
}
```

Usage:

```tsx
<CompareSlider
  before="/images/scene_original.webp"
  after="/images/scene_edited.webp"
  aspectRatio="16/9"
  beforeLabel="ORIGINAL"
  afterLabel="INPAINTED"
/>
```

---

## Aspect Ratio Validator

A utility that checks container ratio vs image ratio and warns when mismatch is detected. This is critical because all LOCUS coordinate systems assume percentage-based positioning relative to the image — if the container and image ratios do not match (and `object-fit: contain` is not used), coordinates will drift.

### useAspectRatioGuard Hook

```tsx
import { useEffect, useRef, useState } from 'react'

interface AspectRatioStatus {
  /** Whether the container and image ratios match (within tolerance) */
  isValid: boolean
  /** The container's current aspect ratio */
  containerRatio: number
  /** The image's natural aspect ratio */
  imageRatio: number
  /** Percentage drift between the two ratios */
  drift: number
}

/**
 * Hook that monitors the aspect ratio relationship between a container
 * and an image. Warns when mismatch detected (coordinates will drift).
 *
 * @param imageRef - Ref to the <img> element
 * @param containerRef - Ref to the container element
 * @param tolerance - Maximum allowed ratio drift (default 0.02 = 2%)
 * @returns AspectRatioStatus
 */
export function useAspectRatioGuard(
  imageRef: React.RefObject<HTMLImageElement>,
  containerRef: React.RefObject<HTMLElement>,
  tolerance: number = 0.02,
): AspectRatioStatus {
  const [status, setStatus] = useState<AspectRatioStatus>({
    isValid: true,
    containerRatio: 0,
    imageRatio: 0,
    drift: 0,
  })

  useEffect(() => {
    function check() {
      const img = imageRef.current
      const container = containerRef.current
      if (!img || !container) return

      const imageRatio = (img.naturalWidth || 1) / (img.naturalHeight || 1)
      const containerRatio = container.offsetWidth / (container.offsetHeight || 1)
      const drift = Math.abs(containerRatio - imageRatio) / imageRatio

      const isValid = drift <= tolerance

      if (!isValid) {
        console.warn(
          `[LOCUS] Aspect ratio mismatch detected.\n` +
          `  Image ratio:     ${imageRatio.toFixed(4)}\n` +
          `  Container ratio:  ${containerRatio.toFixed(4)}\n` +
          `  Drift:           ${(drift * 100).toFixed(2)}%\n` +
          `  Threshold:       ${(tolerance * 100).toFixed(2)}%\n` +
          `  LOCUS coordinates will drift unless object-fit: contain is used.`,
        )
      }

      setStatus({ isValid, containerRatio, imageRatio, drift })
    }

    check()

    const img = imageRef.current
    if (img) {
      img.addEventListener('load', check)
    }
    window.addEventListener('resize', check)

    return () => {
      if (img) img.removeEventListener('load', check)
      window.removeEventListener('resize', check)
    }
  }, [imageRef, containerRef, tolerance])

  return status
}
```

Usage:

```tsx
const imgRef = useRef<HTMLImageElement>(null)
const containerRef = useRef<HTMLDivElement>(null)
const ratioStatus = useAspectRatioGuard(imgRef, containerRef)

// In development, show a warning banner
{!ratioStatus.isValid && process.env.NODE_ENV === 'development' && (
  <div className="absolute top-0 left-0 right-0 bg-red-600 text-white text-xs font-mono p-1 z-50">
    LOCUS: Aspect ratio drift {(ratioStatus.drift * 100).toFixed(1)}% — coordinates will be inaccurate
  </div>
)}
```

---

## File Structure Rule

All LOCUS-generated components go in `src/components/locus/`:

```
src/components/locus/
├── CSIOverlay.tsx      # State injection overlays
├── DebugTuner.tsx      # IQM drag-and-drop coordinate mapper (also positions CSI zones)
├── DebugOverlay.tsx    # Ctrl+Shift+D wireframe overlay
├── HQWTerminal.tsx     # Homography quad warp content
├── CompareSlider.tsx   # Ghost Mode before/after slider
└── utils/
    └── locus-math.ts   # Pure math functions (quadBounds, computeQuadWarp, etc.)
```

To uninstall LOCUS from a project: delete `src/components/locus/`, remove dompurify dependency. Clean separation.

---

## Screenshot Handshake

Same pattern as CANVAS. After starting a dev server with LOCUS tools, ask:

> *"Dev server running at http://localhost:3000/tuner — can you paste a screenshot? I want to confirm the image and tuner handles are rendering correctly before you start dragging."*

This is especially critical for LOCUS because coordinate accuracy depends on correct rendering. If the image isn't displaying at the right aspect ratio, every coordinate will drift.

---

## Security Checklist

Before shipping any interactive image built with LOCUS, verify each item:

- [ ] **Sanitize DOM content** — All HTML injected via CSI overlays uses DOMPurify or equivalent. No raw `dangerouslySetInnerHTML` with user-supplied content.
- [ ] **Validate coordinates** — All percentage inputs are numeric and in the range 0-100. All pixel coordinates are non-negative and within image bounds.
- [ ] **Prevent path traversal** — Image file references are validated against an allowed directory. No `../` sequences permitted in dynamic paths.
- [ ] **Content Security Policy** — If loading images dynamically, ensure CSP headers allow the image sources. Use `img-src` directives appropriately.
- [ ] **No eval() on coordinate data** — Never use `eval()`, `new Function()`, or similar on coordinate data from external sources. Parse JSON with `JSON.parse()` only.
- [ ] **Validate image MIME types** — Before processing images for surgical inpainting, check the actual MIME type (not just the file extension).
- [ ] **Validate matrix3d inputs** — The `computeQuadWarp` function includes input validation. Never pass unsanitized user input directly to CSS `transform` properties.
- [ ] **Rate-limit interactive triggers** — Debounce or throttle CSI state transitions to prevent performance degradation from rapid hover/click spam.

---

## Quality Checklist

Before shipping any interactive image:

- [ ] All CSI overlays fade smoothly (no pop-in, no flicker)
- [ ] IQM quad coordinates match the visual element precisely (screenshot verify)
- [ ] HQW warped text is readable and follows the surface perspective
- [ ] ADT polygon boundaries contain particles/effects correctly
- [ ] Aspect-ratio container pattern used for CSI overlays (NOT `object-fit: contain` with absolute positioning)
- [ ] Aspect ratio guard shows no drift warnings
- [ ] All interactive zones are keyboard accessible (Tab + Enter/Space)
- [ ] `prefers-reduced-motion` disables CSI transitions (opacity snaps instead of fading)
- [ ] Images are optimized (WebP/AVIF, appropriate dimensions)
- [ ] Surgical inpainting results pass the Ghost Mode comparison slider test
- [ ] Debug wireframe overlay confirms all zones align
- [ ] Performance: 60fps during interactions (no layout thrash from overlays)
- [ ] Mobile: touch events work on all interactive zones
- [ ] Security checklist above is fully satisfied

---

## Final Delivery — Ask Before Saving

When the interactive page is complete and the user is happy with how it looks, **ask them how they want the final output saved**. Do not assume a format. Present clear options:

> *"The interactive page is looking great. How would you like me to save the final version?"*

| Option | What You Deliver | Best For |
|--------|-----------------|----------|
| **Standalone HTML** | Single `.html` file with all JS/CSS inlined, images as base64 or relative paths | Quick demos, sharing via email, no build step |
| **Next.js project** | Clean project directory, `npm run build` ready, production config | Deploying to Netlify/Vercel, ongoing development |
| **React components** | Just the components + utility files, no framework wrapper | Dropping into an existing project |
| **Static export** | Pre-built `out/` directory from `next export` | Direct upload to any static host |

Also ask about:
- **Where to save**: specific directory path, or let you choose
- **Image optimization**: convert PNGs to WebP/AVIF for production
- **Cleanup**: remove tuner/debug pages from the final build, or keep them for future iteration
- **Git**: initialize a repo and make an initial commit

The user drove the visual work — respect that by giving them control over the final output too.

---

## Companion Skills

**CANVAS** (Immersive Web Pipeline) provides the React Three Fiber, GSAP ScrollTrigger, and Next.js foundation that LOCUS overlays operate within. LOCUS is fully self-contained and works standalone with any web stack, but pairs naturally with CANVAS for building complete immersive experiences where 3D scenes, scroll-driven animations, and interactive AI-generated imagery work together.

**OPTIC** (AI Image Generation Pipeline) provides the image generation and compositing pipeline that creates the visual assets LOCUS makes interactive. OPTIC generates scenes via Gemini models, handles multi-pass refinement (Sequential Grounding), and performs surgical inpainting with colour matching and feathered compositing. Any AI image generator works with LOCUS, but OPTIC is the recommended companion for the full creative pipeline.

---

## Prerequisites

- React 18+ environment (Next.js, Vite, Remix, or standalone)
- `dompurify` package for DOM sanitization (`npm install dompurify @types/dompurify`)
- A running dev server (the tuner tools run in the browser)
- No other external dependencies

---

*LOCUS encodes four original techniques for making AI-generated images interactive.*
*Developed in the jord0-cmd workshop. No existing tools do what these do.*
*CSI for states. IQM for mapping. HQW for warping. ADT for polygons.*
*The human eye positions. The code transforms. Together they ship.*
