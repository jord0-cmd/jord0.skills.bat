# OPTIC

<span class="tag tag-creative">creative</span>

**AI image generation pipeline. From prompt to pixel — text-to-image, editing, multi-pass refinement, and surgical compositing.**

Stop getting mediocre AI images. OPTIC encodes the prompt engineering, multi-pass techniques, and compositing workflows that produce dramatically better results than naive single-pass generation.

---

## The Problem OPTIC Solves

Most people use AI image generators like this:

```
"a cool scene with a robot in a city"
```

And get generic, flat results. OPTIC teaches Claude the techniques that professionals use — narrative prompts, sequential multi-pass generation, surgical inpainting, and colour-matched compositing. The difference isn't subtle.

---

## Usage

OPTIC works through conversation. Describe what you want, and Claude applies the right technique:

```
Generate a retro-futuristic control room with CRT monitors and analog gauges
```

```
Edit this image to add warm desk lamp lighting on the left side
```

```
Inpaint the portrait area — replace it with a storm cloud painting
```

### The Generator Tool

OPTIC includes a drop-in Python CLI for calling Gemini image models:

```bash
# Basic text-to-image
python3 generate.py "a cozy coffee shop at night" -o coffee_shop.png

# High-quality model
python3 generate.py "detailed portrait" --quality -o portrait.png

# Edit an existing image
python3 generate.py "make it sunset" --reference daytime.png -o sunset.png

# With aspect ratio
python3 generate.py "cinematic landscape" -q -a 16:9 -o landscape.png
```

| Flag | Description |
|------|-------------|
| `--quality` / `-q` | Use high-quality model (slower, better) |
| `--output` / `-o` | Output filename |
| `--reference` / `--ref` | Source image for editing |
| `--aspect` / `-a` | Aspect ratio (default: 3:4) |

---

## Key Techniques

### Prompt Engineering — The 6-Variable Framework

Every strong prompt addresses six elements:

| Variable | Example |
|----------|---------|
| **Subject** | "a stoic robot barista with glowing blue optics" |
| **Action** | "leaping across a rooftop gap" |
| **Environment** | "neon-lit Tokyo back alley" |
| **Composition** | "low angle shot, 24mm wide lens" |
| **Lighting** | "golden hour, harsh rim light from behind" |
| **Style** | "vintage 1980s Polaroid, slight grain" |

!!! warning "Describe scenes, don't list keywords"
    Wrong: `fantasy warrior, cliff, volcanic, dramatic, epic, 4K, trending on artstation`

    Right: `A lone warrior in dragon scale armor stands on a windswept cliff overlooking a volcanic landscape. Harsh backlighting silhouettes the figure against molten orange glow. Dark fantasy atmosphere, cinematic wide shot.`

### Sequential Grounding — Multi-Pass Generation

The single most impactful technique for complex scenes. Instead of generating everything in one shot, build in phases:

**Phase 1 — The Canvas**: Generate a hyper-real base scene with NO complex additions. Just the physical space.

**Phase 2 — The Retrofit**: Feed Phase 1 back as a reference and ask the model to *install* new elements INTO the existing scene.

**Phase 3 — Colour Grade** (optional): Feed Phase 2 back and apply cinematic colour grading.

```bash
# Phase 1: Base scene
python3 generate.py "empty industrial room, 35mm film..." -q -a 16:9 -o phase1.png

# Phase 2: Add elements using Phase 1 as reference
python3 generate.py "install three CRT monitors on the desk..." -q --ref output/phase1.png -o phase2.png

# Phase 3: Colour grade
python3 generate.py "cinematic teal and orange grade..." -q --ref output/phase2.png -o phase3.png
```

Why? When the model receives a source image, it calculates how new elements interact with EXISTING lighting, reflections, and surfaces. This forces physically accurate integration.

### Surgical Inpainting

Edit a specific region of an image without affecting the rest:

```
Source Image
  ├── 1. CROP: Extract square region (must be square!)
  ├── 2. EDIT: Send crop as reference with -a 1:1
  ├── 3. COLOUR MATCH: Per-channel histogram transfer
  ├── 4. FEATHER COMPOSITE: Gradient-masked paste-back
  └── 5. VERIFY: Check alignment
```

!!! danger "The Golden Rule"
    Always use square crops with `-a 1:1`. Non-square crops cause geometry drift even with matching aspect ratio flags. No exceptions.

OPTIC includes copy-paste-ready Python code for colour matching and feathered compositing.

### Hand-Drawn Guide Lines

When the model can't get perspective right from text alone — draw it. Bold structural lines on the image, then feed it back with instructions to transform those lines into real objects. The poor man's ControlNet, and it works brilliantly.

---

## What's Included

| File | Purpose |
|------|---------|
| `SKILL.md` | Complete skill with all techniques, code, and patterns |
| `example-prompts.md` | Working prompts across categories (portraits, fantasy, product, scenes) |
| `api-reference.md` | Python API patterns (basic, multi-turn, editing, pipelines) |
| `composition-keywords.md` | Camera angles, shot framing, lens specs |
| `lighting-keywords.md` | Natural light, studio light, atmospheric effects |
| `style-keywords.md` | Art styles, photography styles, aesthetic movements |

---

## Pairs With LOCUS

OPTIC generates images. LOCUS makes them interactive.

```
OPTIC: Generate a retro control room scene
LOCUS: Map clickable hover states onto the monitors, warp terminal text
       onto the screens, define polygon hotspots around the gauges
```

See the [Creative Pipeline](../recipes/creative-pipeline.md) recipe for the full workflow.

---

## Prerequisites

- Python 3.10+
- `google-genai` package (`pip install google-genai`)
- `GEMINI_API_KEY` environment variable
- Optional: `Pillow` + `numpy` for inpainting pipeline

---

*From prompt to pixel. The pipeline that produces.*
