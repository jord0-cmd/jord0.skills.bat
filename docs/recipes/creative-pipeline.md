# Creative Pipeline

**Skills used:** OPTIC + LOCUS

Generate stunning AI images, then make them interactive. The full pipeline from prompt to clickable experience.

---

## The Problem

You can generate beautiful AI images. You can build interactive websites. But the gap between "generated image" and "interactive experience" is where most projects stall. How do you:

- Map live content onto a perspective-distorted screen in an AI scene?
- Add hover effects that match the original lighting and grain?
- Define clickable zones on irregular shapes?
- Keep everything responsive at any viewport size?

OPTIC + LOCUS bridges that gap.

---

## The Pipeline

### Step 1: OPTIC — Generate the Scene

Use Sequential Grounding for complex scenes:

```bash
# Phase 1: The base environment
python3 generate.py "A retro-futuristic control room, 35mm film, warm
practical lighting..." -q -a 16:9 -o phase1_room.png

# Phase 2: Add technology elements
python3 generate.py "Install three CRT monitors on the desk, wire in
analog gauges..." -q --ref output/phase1_room.png -o phase2_tech.png

# Phase 3: Cinematic colour grade
python3 generate.py "Teal shadows, amber highlights, crush the blacks..."
-q --ref output/phase2_tech.png -o final_scene.png
```

Three passes. Each one builds on the last. The result has physically accurate lighting integration.

### Step 2: LOCUS IQM — Map the Coordinates

Tell Claude what you want interactive:

```
I want terminal text on all three monitors, the desk lamp should glow
on hover, and the gauge cluster should be clickable.
```

Claude builds a tuner page. You open it in your browser.

**For the monitors**: Drag four corners to match each screen's edges. The monitors are perspective-distorted — IQM handles that. Click COPY POSITIONS.

**For the lamp and gauges**: Same tuner, different quads. Drag rectangles around the lamp zone and gauge cluster.

### Step 3: LOCUS HQW — Warp Content onto Screens

Paste the monitor coordinates back to Claude. HQW computes the `matrix3d()` transform that maps flat HTML onto each tilted screen.

Now your terminal text, status displays, or live data sit perfectly within the perspective of the AI-generated monitors.

### Step 4: OPTIC + LOCUS CSI — Generate Hover States

For the desk lamp:

```
# Crop the lamp region (square!)
# Feed to OPTIC as reference with state change:
"Same lamp, same angle. The lamp is now switched on, casting warm amber
light across the desk surface. Warm glow emanates from the shade."
```

OPTIC generates the "lamp on" state. LOCUS CSI overlays it at the exact position, fading in on hover.

### Step 5: LOCUS ADT — Irregular Hotspots

The gauge cluster isn't rectangular. Open the ADT drawing tool, click around the gauge boundary to define a polygon. Export the vertices.

Now the irregular gauge region responds to clicks with proper point-in-polygon hit testing.

---

## The Result

A single AI-generated image becomes a fully interactive experience:

- Monitors display live terminal text, warped to match the scene's perspective
- The desk lamp glows on hover, with AI-generated lighting that matches the original
- Gauges respond to clicks within their actual shape boundaries
- A CompareSlider lets visitors see the original vs. the interactive version
- Everything is responsive — works on desktop and mobile

---

## Real Example

This exact pipeline was used to build the [jord0.net](https://jord0.net) under-construction page:

1. **OPTIC** generated a retro control room scene via Sequential Grounding (3 phases)
2. **IQM** mapped three monitor screens and five interactive zones
3. **HQW** warped terminal content onto perspective-distorted CRT monitors
4. **CSI** generated hover states for a desk lamp and indicator lights
5. **ADT** defined irregular boundaries for smoke particles and a gauge cluster

Single HTML page. No frameworks. All techniques working together.

---

## Tips

!!! tip "Generate first, map second"
    Don't try to map coordinates while the image is still changing. Finalise your OPTIC output before starting LOCUS work.

!!! tip "Square crops for inpainting"
    When using CSI with OPTIC-generated states, always use square crops with 1:1 aspect ratio. This is OPTIC's golden rule and it applies here too.

!!! tip "One tuner session for everything"
    The DebugTuner supports multiple named quads. Map all your monitors, CSI zones, and rectangular regions in a single session instead of opening the tuner multiple times.

!!! tip "ADT for organic shapes, IQM for rectangles"
    If the shape has four corners, use IQM. If it's irregular, use ADT. Don't over-complicate rectangular zones with polygon drawing.

---

*Generate. Map. Ship.*
