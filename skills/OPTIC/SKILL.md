---
name: optic
description: |
  INVOKE THIS SKILL when: generating AI images, editing existing images, writing prompts for
  Gemini image models, performing surgical inpainting, running multi-pass Sequential Grounding,
  colour matching composites, or any AI image generation pipeline work. Contains the generator
  tool, prompt engineering framework, and advanced compositing techniques.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# OPTIC — AI Image Generation Pipeline

*From prompt to pixel. Text-to-image, image-to-image, and surgical compositing.*

Developed for the [jord0.skills](https://github.com/jord0-cmd/jord0.skills) ecosystem. OPTIC encodes the complete AI image generation pipeline: prompt engineering, model invocation, multi-pass refinement, and pixel-level compositing. These techniques were developed through extensive experimentation and produce dramatically better results than naive single-pass generation.

**Requirements**: Python 3.10+, `google-genai` package, `GEMINI_API_KEY` environment variable. Optional: `Pillow` + `numpy` for inpainting pipeline.

---

## When to Invoke This Skill

- Generating images from text descriptions (text-to-image)
- Editing or transforming existing images (image-to-image)
- Writing effective prompts for Gemini image models
- Multi-pass scene generation (Sequential Grounding)
- Surgical inpainting (crop, edit, colour match, composite)
- Hand-drawn guide line techniques for geometry control
- Any workflow where AI-generated imagery is a component

---

## What OPTIC Builds — Capability Lookup

| Need | Technique | Section |
|------|-----------|---------|
| "Generate an image from description" | Text-to-image via Generator | The Generator |
| "Edit this existing image" | Image-to-image via `--reference` | The Generator |
| "Complex scene with multiple elements" | Sequential Grounding | Sequential Grounding |
| "Fix perspective / geometry" | Hand-Drawn Guide Lines | Hand-Drawn Guide Lines |
| "Edit a specific region without affecting rest" | Surgical Inpainting | Surgical Inpainting |
| "Match colours between edited and original" | Per-channel colour transfer | Colour Match Code |
| "Blend edited region back seamlessly" | Feathered composite | Feathered Composite Code |
| "What camera angle / lighting / style?" | Reference keywords | Reference Keywords |
| "Prompt isn't working well" | 6-variable framework + checklist | Prompt Engineering |

---

## The Generator

OPTIC includes a drop-in Python CLI tool for calling Google Gemini image models. It handles API setup, model selection, aspect ratios, and both text-to-image and image-to-image modes.

### Setup

```bash
# Install dependencies
pip install google-genai Pillow

# Set API key
export GEMINI_API_KEY="your-api-key-here"

# Or add to .env file in the project root
echo 'GEMINI_API_KEY=your-key-here' >> .env
```

### CLI Usage

```bash
# Basic text-to-image (fast model)
python3 generate.py "a cozy coffee shop at night" -o coffee_shop.png

# High-quality model
python3 generate.py "detailed portrait with warm studio lighting" --quality -o portrait.png

# With aspect ratio
python3 generate.py "cinematic landscape" -q -a 16:9 -o landscape.png

# Image-to-image editing (Sequential Grounding Phase 2)
python3 generate.py "edit prompt describing changes" -q --reference base.png -o edited.png

# Source .env if running from shell
set -a && source .env && set +a
```

### CLI Arguments

| Flag | Short | Description |
|------|-------|-------------|
| `prompt` | — | Image generation prompt (positional) |
| `--quality` | `-q` | Use high-quality model (Gemini 3 Pro Image) |
| `--output` | `-o` | Output filename |
| `--reference` | `--ref` | Reference image for editing / transformation |
| `--aspect` | `-a` | Aspect ratio (default: `3:4`) |

### Models

| Nickname | API Model ID | Cost | Use For |
|----------|-------------|------|---------|
| Fast | `gemini-2.5-flash-image` | ~$0.04/image | Drafts, iteration, quick sketches |
| Quality | `gemini-3-pro-image-preview` | ~$0.13-0.24/image | Final output, detailed work, publication |

### Supported Aspect Ratios

```
1:1    (Square)
2:3    (Portrait - book covers)
3:2    (Landscape - photos)
3:4    (Portrait)
4:3    (Landscape - TV)
4:5    (Portrait - Instagram)
5:4    (Landscape)
9:16   (Vertical - stories/reels)
16:9   (Widescreen - cinematic)
21:9   (Ultra-wide - panoramic)
```

**Quality model additional**: 1.85:1, 2.39:1, 2.75:1, 4:1, 1:4

### Resolution Options

```
1K  (default)
2K
4K  (Quality model only)
```

**Important**: Must use uppercase 'K' in API calls.

### Generator Code (Drop-In)

Save as `generate.py` in your project. Requires a `config.json` alongside it.

```python
#!/usr/bin/env python3
"""
OPTIC Image Generator
Uses Google Gemini models for image generation and transformation.

Usage:
    python generate.py "prompt" [--quality] [--output filename]
    python generate.py "prompt" --reference image.png   # Transform existing image

Examples:
    python generate.py "a cozy coffee shop at night"
    python generate.py "technical diagram of neural network" --quality
    python generate.py "same scene but at sunset" --reference daytime.png
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai package not installed.")
    print("Run: pip install google-genai")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    Image = None


def load_config():
    """Load imaging configuration."""
    config_path = Path(__file__).parent / "config.json"
    with open(config_path) as f:
        return json.load(f)


def get_api_key(config):
    """Get API key from environment or .env file."""
    env_var = config.get("api_key_env", "GEMINI_API_KEY")
    api_key = os.environ.get(env_var)

    # Try .env file if not in environment
    if not api_key:
        env_file = Path(__file__).parent.parent / ".env"
        if not env_file.exists():
            env_file = Path.cwd() / ".env"
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith(f"{env_var}="):
                        api_key = line.strip().split("=", 1)[1].strip('"\'')
                        break

    if not api_key:
        print(f"Error: {env_var} not set.")
        print(f"Set in environment or add to .env file")
        sys.exit(1)
    return api_key


def generate_image(prompt: str, model_id: str, api_key: str, output_path: Path,
                   aspect_ratio: str = "3:4", reference_image: Path = None):
    """Generate or transform an image using Gemini."""
    client = genai.Client(api_key=api_key)

    print(f"Model: {model_id}")
    print(f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")

    if reference_image:
        print(f"Reference: {reference_image}")

        if Image is None:
            print("Error: PIL not installed. Run: pip install Pillow")
            sys.exit(1)

        source = Image.open(reference_image)
        contents = [prompt, source]
    else:
        contents = [prompt]

    response = client.models.generate_content(
        model=model_id,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
            )
        )
    )

    # Extract image from response
    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                image_data = part.inline_data.data
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                print(f"Saved: {output_path}")
                return output_path

    print("Error: No image generated")
    if response.candidates:
        print(f"Response: {response.candidates[0]}")
    return None


def main():
    parser = argparse.ArgumentParser(description="OPTIC Image Generator")
    parser.add_argument("prompt", nargs="?", help="Image generation prompt")
    parser.add_argument("--quality", "-q", action="store_true",
                        help="Use high-quality model (Gemini 3 Pro Image)")
    parser.add_argument("--output", "-o", help="Output filename")
    parser.add_argument("--reference", "--ref", metavar="IMAGE",
                        help="Reference image for transformation (image-to-image)")
    parser.add_argument("--aspect", "-a", default="3:4",
                        help="Aspect ratio (default: 3:4)")

    args = parser.parse_args()
    config = load_config()

    # Resolve reference image if provided
    reference_path = None
    if args.reference:
        path = Path(os.path.expanduser(args.reference))
        if not path.exists():
            print(f"Error: Reference image not found: {args.reference}")
            sys.exit(1)
        reference_path = path

    # Build prompt
    if args.prompt:
        prompt = args.prompt
    else:
        parser.print_help()
        return

    # Get settings
    api_key = get_api_key(config)
    model_key = "quality" if args.quality else "fast"
    model_id = config["models"][model_key]["model_id"]

    # Output path
    output_dir = Path(config["defaults"].get("output_dir", "./output"))
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = args.output or f"generated_{timestamp}.png"
    if not filename.endswith(".png"):
        filename += ".png"
    output_path = output_dir / filename

    # Generate
    generate_image(prompt, model_id, api_key, output_path, args.aspect, reference_path)


if __name__ == "__main__":
    main()
```

### Generator Config (Drop-In)

Save as `config.json` alongside `generate.py`:

```json
{
  "api_key_env": "GEMINI_API_KEY",
  "models": {
    "fast": {
      "name": "Gemini Flash Image",
      "model_id": "gemini-2.5-flash-image",
      "description": "Good, fast - ~$0.04/image",
      "use_for": "Quick sketches, explanations, day-to-day visuals"
    },
    "quality": {
      "name": "Gemini Pro Image",
      "model_id": "gemini-3-pro-image-preview",
      "description": "Excellent, 2K-4K - ~$0.13-0.24/image",
      "use_for": "Detailed work, portraits, publication quality"
    }
  },
  "defaults": {
    "model": "fast",
    "output_dir": "./output",
    "format": "png"
  }
}
```

---

## Prompt Engineering

### Core Principle

**DESCRIBE THE SCENE, DON'T LIST KEYWORDS.**

Gemini understands natural language. Write prompts like you're describing a scene to a film director, not tagging an image for search.

### WRONG (Keyword Soup)

```
fantasy warrior, cliff, volcanic, dramatic, epic, 4K, detailed, trending on artstation, masterpiece, best quality
```

### RIGHT (Narrative Description)

```
A lone warrior clad in dragon scale armor stands on a windswept cliff overlooking a vast, volcanic landscape. The sky is filled with ash and smoke. Harsh backlighting silhouettes the figure against molten orange glow rising from the caldera below. Dark fantasy atmosphere, cinematic wide shot.
```

---

### The 6-Variable Framework

Every strong prompt addresses these six elements:

1. **Subject** — Who/what (be specific: "a stoic robot barista with glowing blue optics")
2. **Action** — What's happening ("leaping across a rooftop gap")
3. **Environment** — Where ("neon-lit Tokyo back alley")
4. **Composition** — Camera angle/framing ("macro lens," "low angle shot," "wide shot")
5. **Lighting** — Light source and mood ("golden hour," "three-point softbox," "harsh noon sun")
6. **Style** — Artistic medium ("vintage 1980s polaroid," "oil painting," "anime cel shading")

### Prompt Structure Formula

```
[Subject + Adjectives] doing [Action] in [Location/Context].
[Composition/Camera Angle].
[Lighting/Atmosphere].
[Style/Media].
```

---

### Semantic Negative Prompting

Gemini does NOT support traditional negative prompts. Instead, describe what you WANT:

| Instead of | Write |
|------------|-------|
| "no cars" | "an empty, deserted street with no signs of traffic" |
| "no blur" | "crisp, sharp focus with detailed textures" |
| "no people" | "a solitary landscape with no human presence" |
| "no watermark" | "clean, unmarked image" |
| "no text" | "image without any visible text or typography" |

### Baseline Negative Elements (Semantic Framing)

```
"Clean composition without visual artifacts"
"Sharp focus throughout the frame"
"Natural proportions and anatomy"
"Professional quality without grain or noise"
```

---

### Common Mistakes to Avoid

#### 1. Keyword Spam
```
WRONG: beautiful, stunning, amazing, masterpiece, best quality, highly detailed, 4K, 8K, trending on artstation, unreal engine
RIGHT: A detailed portrait with natural skin texture and sharp focus, rendered in warm studio lighting.
```

#### 2. Vague Descriptions
```
WRONG: Make it pretty, add some effect
RIGHT: Add warm rim lighting on the left side, increase shadow depth, shift color palette toward amber tones
```

#### 3. Contradictory Instructions
```
WRONG: Bright daylight scene with deep noir shadows and moody darkness
RIGHT: Choose one coherent lighting scheme
```

#### 4. Over-prompting Quality Tags
```
WRONG: 4k, trending on artstation, masterpiece spam
RIGHT: Natural language description — the model understands quality
```

#### 5. Forgetting Identity Anchors (Character Work)
```
ALWAYS include: "Keep all character features identical to the previous image"
```

#### 6. Unlabeled Reference Images
```
WRONG: Just uploading multiple images
RIGHT: "Use Image A for character pose, Image B for art style, Image C for background"
```

#### 7. Re-rolling Instead of Editing
```
If 80% correct, don't regenerate from scratch. Say:
"Keep everything the same, but change the lighting to warmer tones"
```

---

### Text Rendering Guidelines (Quality Model)

#### Success Rates
- 1-3 words: ~75% accuracy
- 4-8 words: ~40% accuracy
- 9+ words: ~15% accuracy

#### Best Practices
```
Keep text under 3 words
Specify: "large bold sans-serif typography, centered, maximum legibility"
Use quotation marks for exact text: Write "HELLO WORLD" on the sign
Describe font style: "distressed vintage font" or "clean modern sans-serif"
```

For anything requiring perfect typography, generate the visual without text, then add text in a compositing tool.

---

### Multi-Image Composition

#### Label Your References
```
"Use Image 1 for the character's face and body proportions.
Use Image 2 for the art style and color palette.
Use Image 3 for the background environment.
Combine into a single cohesive scene."
```

#### Character + Scene Merge
```
"Place the exact character from Image 1 into the environment shown in Image 2. Match the lighting and color grading of the environment while preserving all character details."
```

#### Style Transfer with Reference
```
"Apply the artistic style from Image 1 to the photograph in Image 2. Preserve composition and subject but transform the rendering style completely."
```

---

### Iterative Refinement Phrases

These work well for multi-turn conversations:

```
"That's great, but make the lighting warmer"
"Keep everything the same, but change the expression to more serious"
"Same image, but shift the color palette toward cooler blues"
"Add more atmospheric fog in the background"
"Increase the contrast slightly"
"Move the subject slightly to the left for better composition"
"Make the background more blurred"
```

---

### Prompt Templates

#### Book Cover (2:3)

```
A [aspect] book cover composition. [Main subject description with specific
visual details]. [Background/environment description]. [Lighting description
with color and direction]. [Atmospheric elements]. The composition leaves
space at the top for title text and bottom for author name. [Style description]
with [texture/technique details]. [Mood summary].
```

#### Chapter Header (16:9)

```
A wide cinematic establishing shot of [location/scene]. [Detailed description
of the environment from a specific viewpoint]. [Specific objects and their
spatial relationships]. [Lighting conditions with color temperature and
direction]. [Atmospheric effects like dust, fog, light rays]. [What is
happening or has happened - evidence of story]. The atmosphere is [mood
description]. No figures present unless specifically needed. Rendered in
[style] with [technique details].
```

#### Character Portrait (3:4)

```
A [framing] portrait of [character description with specific features].
[Clothing and accessories with materials and condition]. [Expression and
body language]. [Lighting setup with direction and quality]. [Background
description, usually soft/blurred]. The mood is [emotional quality].
Rendered in [style] with attention to [specific details to emphasize].
```

---

### Checklist Before Generating

- [ ] Is this a narrative paragraph, not a keyword list?
- [ ] Did I specify the camera angle/viewpoint?
- [ ] Did I include spatial relationships (foreground, center, distance)?
- [ ] Did I describe the lighting with color and direction?
- [ ] Did I include atmospheric details (dust, fog, time of day)?
- [ ] Did I specify the art style and technique?
- [ ] Is the prompt at least 300+ characters? (500-1500 ideal for complex scenes)
- [ ] Did I avoid contradictory instructions?
- [ ] For character work: Did I include identity anchors?
- [ ] For edits: Did I specify what to keep vs change?

---

## Sequential Grounding (Multi-Pass Generation)

**The single most impactful technique for complex scene generation.** Instead of generating a complex scene in one shot (which produces flat, generic renders), generate in phases:

1. **Phase 1 — The Canvas**: Generate a hyper-real base scene with NO complex additions. Just the physical space with all its texture, grime, lighting, and atmosphere.
2. **Phase 2 — The Retrofit**: Feed Phase 1 back via `--reference` and ask Gemini to *install* new elements INTO the existing scene.
3. **Phase 3 — Color Grade** (optional): Feed Phase 2 back and apply cinematic color grading.

### Why It Works

When Gemini receives a source image, it must calculate how new elements interact with EXISTING lighting, reflections, and surfaces. This forces physically accurate integration rather than the flat compositing you get from single-pass prompts.

### When to Use

Any scene combining two distinct visual worlds (old/new, analog/digital, nature/tech, industrial/clean). Basically anything that needs "friction" between elements.

### Phase 1 Pattern: The Canvas

```
A hyper-realistic, low-light photograph shot on 35mm film (Kodak Portra 800)
inside [LOCATION]. [LENS] wide-angle lens. The perspective is [VIEWPOINT].

Atmosphere: [ENVIRONMENTAL EFFECTS — steam, haze, dust motes, humidity].
Lighting: [PRACTICAL LIGHT SOURCES ONLY — no fancy studio, just what would
actually be in this room]. [COLOR TEMPERATURE]. [SHADOW DESCRIPTION].

Textures: [SPECIFIC MATERIAL DETAILS — grime, wear, patina, damage].
[SPECIFIC OBJECTS that ground the space in reality].
No [ELEMENTS YOU'LL ADD LATER]. Pure [BASELINE GENRE].
High ISO film grain and [MOTION ELEMENT] to sell liveliness.
```

### Phase 2 Pattern: The Retrofit

```
Edit this image to [SPECIFIC INSTALLATION ACTION — "convert," "place,"
"install," "bolt," "wire in"].

The addition: [DESCRIBE NEW ELEMENTS with physical mounting details —
"bolted crudely to the steel floor," "taped down with gaffer tape,"
"wired directly into the mains"].

The details: [SPECIFIC OBJECTS with condition — scratched, dusty,
fingerprint-smudged, pristine-but-out-of-place].

Lighting clash: [NEW LIGHT SOURCE] emits [COLOR] that clashes with
[EXISTING LIGHT COLOR]. The [new light] reflects off [specific existing
surface — pools of oil, wet concrete, polished metal].

Maintain all original [film grain/texture/atmosphere]. The new elements
are [jerry-rigged/improvised/bolted/taped] in, not designed.
```

**Critical keywords for Phase 2:**
- "bolted," "taped," "wired," "jury-rigged," "improvised" — prevents floating/hovering elements
- "clashes with" — creates visual friction between light sources
- "reflects off [existing surface]" — forces lighting integration
- "Maintain all original" — prevents the model from cleaning up your beautiful grime

### Phase 3 Pattern: Cinematic Color Grade

```
Apply a cinematic color grade to this image. Push the shadows and dark
areas slightly toward teal/green. Keep the highlights and warm light
sources orange/amber. Crush the blacks slightly for depth. The overall
feel should be like a still from a Denis Villeneuve film — moody,
cinematic, unified color palette. Do NOT add any new objects or change
the composition. Only adjust the color grading and atmosphere. Maintain
all existing film grain and texture.
```

**Variations:**
- **Teal & Orange** (blockbuster): Shadows → teal, highlights → warm amber
- **Desaturated Cool** (noir): Pull saturation down 30%, push shadows blue
- **Warm Analog** (vintage): Lift blacks slightly, push everything amber, add grain
- **High Contrast** (editorial): Crush blacks hard, blow highlights slightly, minimal midtones

**Rule**: Always fork the file first. Save the ungraded version. Run the grade on a copy.

### Multi-Pass Variant Generation

Once you have a strong base, generate multiple variants:

```
Base Image (Phase 1)
  ├── V1 Edit: "Clean installation" (server rack, single monitor, professional)
  ├── V2 Edit: "The obsession" (3 monitors, graph viz, headphones, coffee mugs)
  ├── V3 Edit: "The nest" (lived-in, post-its, foil wrappers, turned chair)
  └── V4 Edit: "The aftermath" (screens showing error, scattered papers, 4am energy)
```

Consistent physical space with different narrative moods. Base lighting and texture stay coherent.

### CLI Pipeline for Sequential Grounding

```bash
# Source env
set -a && source .env && set +a

# Phase 1: Base scene
python3 generate.py "base scene prompt..." -q -a 16:9 -o phase1_base.png

# Phase 2: Edit with reference
python3 generate.py "edit prompt..." -q --reference output/phase1_base.png -a 16:9 -o phase2_edit.png

# Phase 3: Color grade
python3 generate.py "color grade prompt..." -q --reference output/phase2_edit.png -a 16:9 -o phase3_graded.png

# Variant: Same base, different edit
python3 generate.py "different edit..." -q --reference output/phase1_base.png -a 16:9 -o variant_b.png
```

---

## Hand-Drawn Guide Lines — Visual Geometry Control

**The poor man's ControlNet — and it works brilliantly.**

When Gemini can't get perspective or geometry right from text alone, **draw it**. Open any image editor, draw bold structural lines onto the image, and feed it back with instructions to transform those lines into real objects.

### The Technique

1. **Start with your best attempt** — Run the image through Gemini for initial correction
2. **Reinforce preservation** — If Gemini drifts, iterate with stronger anchoring: "preserve the monitor look and background", "freeze the screen content"
3. **Draw guide geometry** — Bold, unmistakable lines (black works best) showing where structural elements should be. Crude is fine — they're instructions, not art.
4. **Feed back with transformation prompt** — Tell Gemini to convert drawn lines into the real thing

### What You Can Draw

- **Horizontal/vertical lines** → Bezel edges, shelf positions, horizon lines
- **Rectangles/boxes** → Window frames, screen boundaries, panel outlines
- **Circles/ovals** → Dial positions, button locations, port holes
- **Arrows/direction indicators** → Light direction, motion direction
- **Outlines around objects** → "This area is the subject, preserve it"
- **X marks** → "Remove this object from here"

### Prompt Pattern for Guide Lines

```
Transform the [bold/drawn/black] [lines/shapes/marks] into [real objects].
[Describe what the objects should look like — material, finish, condition].
[Describe alignment and spatial relationships].
Maintain the exact same [background/lighting/environment/content].
Blend the new elements seamlessly into the environment.
[Camera/perspective instructions].
[What NOT to add — "no headphones", "no extra cables", etc.]
```

### Key Phrases That Work

- "Transform the rigid black guide lines into..." → Tells Gemini the lines are instructions, not content
- "Maintain the exact same..." → Anchors everything else in place
- "Blend seamlessly into the environment" → Forces photorealistic integration
- "Completely flat, straight-on, orthographic" → Geometric precision language
- "Absolutely no [unwanted element]" → Explicit removal of things Gemini likes to hallucinate

### Why This Works

- **Geometric intent is unambiguous** — A drawn line IS the target position
- **Gemini treats drawn lines as structural constraints** — It understands "this line should become a real object edge"
- **Low effort, high precision** — A 5-second scribble communicates what paragraphs of text can't
- **Composable with other techniques** — Draw guides THEN apply Sequential Grounding

---

## Surgical Inpainting — Crop, Edit, Composite

**When you need to edit a specific region of an image without affecting the rest, don't send the whole image.** Gemini will drift. Instead: isolate, edit, reintegrate.

### The Pipeline

```
Source Image
  │
  ├── 1. CROP: Extract square region around edit target (PIL)
  │         - Make it SQUARE — Gemini changes aspect ratio otherwise
  │         - Add padding (2-3% of image) for blending room
  │
  ├── 2. EDIT: Send crop to Gemini with --reference and -a 1:1
  │         - CRITICAL: Always force -a 1:1 (or matching aspect ratio)
  │         - Gemini WILL change aspect ratio if you don't specify
  │         - Describe removal/change in natural language
  │         - Anchor everything else: "keep all objects exactly as they are"
  │
  ├── 3. COLOUR MATCH: Histogram transfer per channel (PIL + NumPy)
  │         - Match mean/std of each RGB channel to original crop
  │         - Gemini shifts colour grading — this corrects it
  │         - Formula: pixel = (pixel - edit_mean) * (orig_std / edit_std) + orig_mean
  │
  ├── 4. FEATHER COMPOSITE: Gradient-masked paste-back (PIL)
  │         - Create alpha mask: white center, fading to black at edges
  │         - Gaussian blur the mask for smooth transitions
  │         - PIL.Image.composite(edited, original_crop, mask) → blended
  │         - Paste blended result at original crop coordinates
  │
  └── 5. VERIFY: Check alignment visually before saving
```

### Critical Rules

1. **GOLDEN RULE: Always square, always 1:1** — Non-negotiable. ALWAYS make your crop a perfect square and ALWAYS use `-a 1:1`. Even if the edit area is rectangular (e.g. 248x276), pad it to a square (276x276). Gemini returns whatever ratio it feels like without `-a 1:1`. Square eliminates all distortion. No exceptions.

2. **Colour matching is mandatory** — Gemini shifts colour grading even with explicit anchoring language. The per-channel mean/std transfer takes 5 lines of NumPy and fixes it completely.

3. **Feather width matters** — Too much feather (25px+) bleeds the original back in, defeating the edit. Too little shows a hard seam. 10-15px with a 3px Gaussian blur is the sweet spot for ~250px crops.

4. **Anchor aggressively** — For every ONE thing you ask Gemini to change, list FIVE things it must NOT change.

### The Anchoring Principle

Gemini will try to "improve" your image. It will shift colours, reshape objects, add detail. **You must be explicitly, aggressively specific about what NOT to change.**

Anchoring phrases that work (use several per prompt):
- "Keep [object] EXACTLY as it is — same shape, same position, same colour"
- "Do NOT alter [thing] in any way"
- "Maintain the EXACT same [lighting/grain/colour grading] throughout"
- "Only change [the specific thing] — leave everything else untouched"
- "Preserve all textures, surfaces, and material properties"

**Common Gemini drift to anchor against:**
- Colour grading shifts (anchor: "maintain exact colour temperature")
- Object reshaping (anchor: "same shape, same proportions")
- Added detail/cleanup (anchor: "preserve existing grain and imperfections")
- Style transfer (anchor: "this is NOT a style change — same medium, same look")

### Inpainting-Specific Phrases

These trigger specific behaviours in the vision encoder:

1. **Use "Inpaint" not "Edit" or "Change"** — "Inpaint" triggers the localised editing pathway. "Edit" and "Change" trigger global scene reinterpretation.
2. **"Keep surrounding pixels locked"** — Increases tensor adherence to the reference image's non-target regions.
3. **"Restrict changes strictly to the inner canvas area"** — Explicitly bounds the edit zone.
4. **Never describe the container** — If editing a painting inside a frame, describe ONLY what the painting should become. Don't mention the frame.
5. **"Maintain the exact noise pattern and compression artifacts"** — Prevents cleaning up grain/noise in surrounding areas, which creates visible seams.
6. **"Do not update the frame style"** — Explicit prohibition on container changes.

### Inpainting Prompt Example

```
Inpaint a dark oil painting of a storm cloud with rain into the canvas
area only. Restrict changes strictly to the inner canvas area. Keep
surrounding pixels locked. Do not alter the frame, wall, or any pixels
outside the painting surface. Maintain the exact noise pattern and
compression artifacts of the original background.
```

### Prompt Patterns

**Removal** — Remove something, reveal what's behind it:
```
Edit this image to remove [SPECIFIC ELEMENT]. The area where [element]
currently exists should show [WHAT WOULD BE BEHIND IT]. Keep [LIST
EVERY OBJECT] exactly as they are — same shape, same position, same
colour. Do NOT alter anything except [the element being removed].
Maintain the EXACT same lighting, film grain, and colour grading.
[Positive end state — "clean air" not "no smoke"].
```

**Addition** — Place something new into the scene:
```
Edit this image to add [NEW OBJECT] at [POSITION]. The [object] should
be [material, size, condition]. It sits [spatial relationship to existing
objects]. The lighting on [new object] matches the existing scene —
[describe light direction and colour temperature from the scene].
Do NOT change any existing objects, surfaces, or the background.
Maintain the EXACT same colour grading, grain, and atmosphere.
Only add [the new object] — nothing else changes.
```

**State change** — Transform something already there:
```
Edit this image to change [OBJECT] from [CURRENT STATE] to [NEW STATE].
The [object] remains in the exact same position and the same size. Only
its [specific property] changes. Everything else in the image — every
other object, the background, the lighting, the colour grading — must
remain IDENTICAL to the source. Do NOT reshape, reposition, or recolour
anything except [the specific change described].
```

### Colour Match Code (Copy-Paste Ready)

```python
import numpy as np
from PIL import Image

original_crop = np.array(Image.open("original_crop.png"), dtype=np.float64)
clean_crop = np.array(Image.open("clean_crop.png").resize(original_size, Image.LANCZOS), dtype=np.float64)

for c in range(3):
    om, os = original_crop[:,:,c].mean(), original_crop[:,:,c].std()
    cm, cs = clean_crop[:,:,c].mean(), clean_crop[:,:,c].std()
    if cs > 0:
        clean_crop[:,:,c] = (clean_crop[:,:,c] - cm) * (os / cs) + om

result = Image.fromarray(np.clip(clean_crop, 0, 255).astype(np.uint8))
```

### Feathered Composite Code (Copy-Paste Ready)

```python
from PIL import Image, ImageFilter
import numpy as np

feather = 15  # pixels — sweet spot for ~250px crops
w, h = crop_width, crop_height
mask = np.full((h, w), 255, dtype=np.float64)

for i in range(feather):
    a = i / feather * 255
    mask[i, :] = np.minimum(mask[i, :], a)          # top
    mask[h-1-i, :] = np.minimum(mask[h-1-i, :], a)  # bottom
    mask[:, i] = np.minimum(mask[:, i], a)           # left
    mask[:, w-1-i] = np.minimum(mask[:, w-1-i], a)  # right

mask_img = Image.fromarray(mask.astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))
room_crop = room.crop((x1, y1, x2, y2))
blended = Image.composite(colour_matched, room_crop, mask_img)
room.paste(blended, (x1, y1))
```

---

## The "Slice of Life" / Liminal Technique

For scenes that need to feel PHOTOGRAPHED rather than RENDERED:

### Camera Specification
```
Shot on 35mm film (Kodak Portra 800)
24mm wide-angle lens
High ISO film grain
Slight motion blur on [moving element]
```

### Imperfection Anchors
```
Fingerprints on glass/screens
Coffee stains on desk surfaces
Crumpled foil wrappers
Worn path in grime showing daily use
Cracked glass on gauges/instruments
Peeling paint
Condensation dripping
```

### Human Absence That Implies Presence
```
Chair turned as if someone just stood up
Half-empty coffee mug
Open laptop with screen still on
Headphones draped over monitor
Scattered sticky notes with sharpie diagrams
Warm indent in a chair cushion
```

**The key insight**: Gemini thinks in **narrative and atmosphere**, not tags. Write prompts like you're describing a photograph to someone who needs to FEEL the room.

---

## Gemini Prompt Philosophy

1. **Gemini thinks in narrative, not tags.** Describe the scene like you're telling someone what it feels like to stand there.
2. **Texture > Detail.** "Oily sheen on diamond-plate metal" beats "detailed metal floor."
3. **Light sources must be physically justified.** Don't say "dramatic lighting." Say "a single caged incandescent bulb casting amber shadows through the steam."
4. **Friction makes images feel real.** The clash between warm amber and cool blue LED. The ergonomic chair on a greasy industrial floor.
5. **When in doubt, add grime.** Fingerprints, dust, oil, condensation, wear. Perfect surfaces look fake.
6. **Specify the camera, not the quality.** "Shot on Kodak Portra 800, 24mm wide-angle" tells Gemini more than "high quality, 4K, detailed."

---

## Python API Quick Reference

### Basic Generation

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_KEY")

response = client.models.generate_content(
    model="gemini-2.5-flash-image",  # or "gemini-3-pro-image-preview"
    contents=["Your prompt here"],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            image_size="2K"  # Must be uppercase: "1K", "2K", "4K"
        )
    )
)

for part in response.candidates[0].content.parts:
    if hasattr(part, 'inline_data'):
        image_data = part.inline_data.data
```

### Multi-Turn with Character Consistency

```python
chat = client.chats.create(
    model="gemini-3-pro-image-preview",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
    )
)

# Initial character
response = chat.send_message(
    "Generate a portrait of a woman with silver hair and green eyes."
)

# Same character, new scene
response = chat.send_message(
    "Show the same character seated at a bar. Keep all features identical."
)

# Refinement
response = chat.send_message(
    "Make the lighting warmer and add more visible bar details."
)
```

### Image Editing

```python
from PIL import Image

source_image = Image.open('/path/to/image.png')

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        "Change the time of day to sunset with warm orange lighting. Keep all other elements unchanged.",
        source_image
    ],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"]
    )
)
```

---

## Reference Keywords

For detailed keyword libraries, see the companion files:

- **`example-prompts.md`** — Complete working prompts across all categories (portraits, fantasy, product, sequential grounding)
- **`api-reference.md`** — Python API code patterns (basic, multi-turn, editing, sequential grounding pipeline)
- **`composition-keywords.md`** — Camera angles, shot framing, lens specs, composition rules
- **`lighting-keywords.md`** — Natural light, studio light, atmospheric effects
- **`style-keywords.md`** — Art styles, photography styles, aesthetic movements, era-specific

---

## Companion Skills: CANVAS + LOCUS

OPTIC is the **imaging pillar** of the jord0.skills creative pipeline:

- **CANVAS** (Immersive Web Pipeline) — Builds the React + Three.js + GSAP foundation. OPTIC generates the visual assets that CANVAS brings to life with 3D, animation, and scroll-driven effects.
- **LOCUS** (Interactive Image Toolkit) — Makes OPTIC-generated images interactive. CSI for hover states, IQM for coordinate mapping, HQW for perspective warping, ADT for polygon hotspots.

**The full pipeline**: OPTIC generates → LOCUS maps → CANVAS renders.

Each skill is fully self-contained and works standalone. Together they form a complete creative-to-interactive pipeline.

---

## Security Checklist

- [ ] API key loaded from environment variable, never hardcoded
- [ ] `.env` file in `.gitignore`
- [ ] No user data or PII in prompts
- [ ] Output directory permissions appropriate
- [ ] Reference images don't contain sensitive content

## Quality Checklist

- [ ] Prompt is narrative, not keyword soup
- [ ] All 6 variables addressed (Subject, Action, Environment, Composition, Lighting, Style)
- [ ] 300+ characters for complex scenes
- [ ] No contradictory instructions
- [ ] For edits: anchoring phrases included (5:1 anchor-to-change ratio)
- [ ] For inpainting: square crop, 1:1 aspect ratio forced
- [ ] Colour matching applied to composited edits
- [ ] Feather width appropriate for crop size (10-15px for ~250px crops)

---

*OPTIC encodes the complete AI image generation pipeline for the jord0.skills ecosystem.*
*Text-to-image. Image-to-image. Multi-pass refinement. Surgical compositing.*
*Prompt engineering that works. Techniques that produce.*
*The generator generates. The pipeline composes. The result ships.*
