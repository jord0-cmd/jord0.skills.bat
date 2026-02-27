# API Quick Reference

## Basic Generation

```python
from google import genai
from google.genai import types

client = genai.Client()

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

# Access generated image
for part in response.candidates[0].content.parts:
    if hasattr(part, 'inline_data'):
        image_data = part.inline_data.data
```

## Multi-Turn with Character Consistency

```python
chat = client.chats.create(
    model="gemini-3-pro-image-preview",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
    )
)

# Initial character
response = chat.send_message(
    "Generate a portrait of a woman with silver hair and green eyes wearing a leather jacket."
)

# Same character, new scene
response = chat.send_message(
    "Show the same character from the previous image seated at a bar. Keep all features identical."
)

# Refinement
response = chat.send_message(
    "Make the lighting warmer and add more visible bar details in background."
)
```

## Image Editing

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

## Sequential Grounding (Multi-Pass Pipeline)

The most powerful technique for complex scenes. Generate a base, then edit it in passes.

```python
from google import genai
from google.genai import types
from PIL import Image
from pathlib import Path

client = genai.Client(api_key="YOUR_KEY")

def generate_phase(prompt, output_path, aspect="16:9", source_path=None):
    """Generate or edit an image. Pass source_path for edit mode."""
    contents = [prompt]
    if source_path:
        contents = [prompt, Image.open(source_path)]

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(aspect_ratio=aspect)
        )
    )

    for part in response.candidates[0].content.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            Path(output_path).write_bytes(part.inline_data.data)
            return output_path
    return None

# Phase 1: Generate pure analog base (NO tech elements)
base = generate_phase(
    "A hyper-realistic engine room photograph on 35mm Kodak Portra 800...",
    "phase1_base.png"
)

# Phase 2: Feed base back, retrofit tech INTO the existing scene
retrofit = generate_phase(
    "Edit this image to install a server rack bolted to the floor...",
    "phase2_retrofit.png",
    source_path=base
)

# Phase 3 (optional): Color grade the result
graded = generate_phase(
    "Apply cinematic teal-orange color grade. Crush blacks. Villeneuve feel...",
    "phase3_graded.png",
    source_path=retrofit
)
```

### Using generate.py CLI for Sequential Grounding

```bash
# Source env first
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
