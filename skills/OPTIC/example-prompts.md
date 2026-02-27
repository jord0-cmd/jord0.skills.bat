# Complete Working Prompts

## Photorealistic Portraits

### Simple Portrait
```
A photorealistic close-up portrait of an elderly Japanese ceramicist with deep, sun-etched wrinkles and a warm smile. He is inspecting a freshly glazed tea bowl in his rustic, sun-drenched workshop. Soft, golden hour light streaming through a window, highlighting the fine texture of the clay.
```

### Emotional Portrait
```
A weathered fisherman's face fills the frame, captured in intimate close-up. Deep lines carved by salt and sun speak of decades at sea. His pale blue eyes hold both weariness and contentment. Shot on 85mm lens, shallow depth of field, natural window light creating soft shadows. Film grain, muted color palette.
```

### Professional Headshot
```
Corporate headshot of a confident woman in her 40s. Sharp navy blazer, subtle earrings. Genuine smile that reaches her eyes. Clean white background. Three-point studio lighting with soft fill. Shot on Canon 5D, 85mm f/1.4, sharp focus on eyes.
```

## Fantasy & Genre

### Dark Fantasy Scene
```
A dark fantasy throne room shrouded in shadow. Ancient stone pillars rise into darkness above, illuminated only by flickering torchlight that casts long, dancing shadows. A figure in ornate black armor sits upon a throne of twisted iron, face obscured by a crowned helm. Volumetric light streams through a single high window, catching dust motes suspended in the still air. Deep blues and burnt oranges dominate the palette. Cinematic composition, low angle emphasizing the throne's imposing presence.
```

### Cyberpunk Character
```
A neon-lit portrait of a street samurai in Neo-Tokyo. Cybernetic eye glows electric blue against rain-slicked skin. Black tactical jacket over mesh underlayer. Cherry blossom tattoo visible on neck. Background blurred into bokeh of pink and cyan neon signs. Shot from slight low angle, dramatic rim lighting. Cinematic color grading with teal shadows and orange highlights.
```

### Cosmic Horror
```
A lone lighthouse stands against an impossible sky filled with geometric patterns that suggest vast, incomprehensible entities. The ocean below churns with unnatural phosphorescence. Tiny silhouettes of fishing boats emphasize the terrifying scale. Deep indigo and sickly green dominate the palette. Atmospheric perspective creates depth. The lighthouse beam catches something colossal and wrong in the sky.
```

## Product Photography

### Luxury Product
```
A high-resolution, studio-lit product photograph of a gold necklace on sandy beach surface. Morning light creates warm highlights on the metal. Scattered seashells nearby for context. Shallow depth of field, crisp focus on the pendant. 45-degree elevated angle. Clean, minimal composition.
```

### Cosmetics
```
Skincare cream jar on polished marble countertop with natural window light. Soft shadows, high-key lighting. Water droplets suggest freshness. Green plant leaves in soft background blur. Product photography style, magazine quality. Square format.
```

### Tech Product
```
Smartwatch floating in futuristic CGI environment. Neon accent lighting in blue and purple. Geometric shapes suggest technology and precision. Sharp focus on watch face showing time. Reflection on glossy black surface below. Premium product photography aesthetic.
```

## Character Consistency Prompts

### Establishing Character
```
Generate a portrait of a woman with silver hair cut in an asymmetrical bob, sharp angular features, and striking green eyes. She has a small scar through her left eyebrow. She wears a weathered leather jacket. Expression is guarded but intelligent. Three-quarter view, medium close-up, soft studio lighting.
```

### Same Character, New Scene
```
Using the character from the previous image, show her seated at a dimly lit bar. Same silver asymmetrical hair, green eyes, scar through left eyebrow. She holds a whiskey glass, looking pensive. Keep all facial features identical. Warm amber lighting from bar fixtures, moody atmosphere.
```

### Identity Lock Phrase
```
"Maintain exact facial features, hair style, and distinguishing marks from the reference image. Same character, different [pose/outfit/scene]."
```

## Manga & Anime

### Anime Portrait
```
Manga-style portrait of a stoic female warrior with long silver hair and piercing amber eyes. Traditional Japanese aesthetic with modern edge. Clean linework, vibrant colors, cel-shading style. Cherry blossoms falling in background. Dramatic side lighting.
```

### Action Panel
```
High-impact manga panel showing two samurai mid-clash. Speed lines radiating from impact point. Dynamic diagonal composition. Black and white with selective red color on blood splatter. Extreme contrast, bold inking. Shonen action style.
```

## Infographics & Text (Quality Model)

### Infographic
```
Create a step-by-step infographic showing how to make Elaichi Chai. Use accurate ingredients: cardamom pods, loose tea leaves, ginger, and milk. Style: Clean vector art with pastel colors. Label each ingredient correctly. Numbered steps 1-5 on left side.
```

### Movie Poster
```
Create a minimalist movie poster for a thriller titled 'THE SILENT ECHO'. Large, distressed sans-serif font at the top. Visual: lone cabin in snowy forest viewed from above. High contrast black and white. Title must be perfectly legible and centered.
```

### Text in Image
```
The word "IMAGINE" rendered in 3D block letters with metallic gold texture. Soft shadow cast on white background. Clean, modern typography.
```

## UI/Web Design

### Tech Blog Homepage
```
Tech blog homepage design. Minimalist layout with hero section featuring gradient blue-purple background. Clean navigation bar with logo. Article card grid below with thumbnail images. Modern sans-serif typography. CTA button in accent orange. Footer with social links. Desktop viewport, light theme.
```

### Product Landing Page
```
Product release webpage for premium headphones. Bold headline "PURE SOUND", hero banner with product floating on gradient. 3-4 product feature cards below with icons. Clean white space, professional tech aesthetic. Desktop view.
```

## Editing Prompts

### Background Replacement
```
Replace the background with a realistic urban sunset skyline. Maintain proper shadows and ambient light interaction with the subject. Keep the foreground figure exactly as is.
```

### Style Transfer
```
Transform this photograph into the artistic style of Van Gogh's Starry Night. Preserve the original composition but render with swirling brushstrokes and impasto technique. Emphasize deep blues and bright yellows.
```

### Object Removal
```
Remove the person in the background and seamlessly blend the environment. Keep all other elements exactly the same including lighting and shadows.
```

### Color Grading
```
Apply moody, cinematic teal-and-orange color grade. Increase contrast, enhance sunlight highlights, deepen shadows to rich blacks. Film look.
```

### Specific Element Change
```
Change only the sky to dramatic sunset with orange and purple clouds. Keep everything else exactly the same - the buildings, the street, the lighting on ground level.
```

## Sequential Grounding (Advanced Multi-Pass)

*These prompts produce dramatically better results than single-pass generation for complex scenes.*

### Phase 1: Grimy Engine Room Base
```
A hyper-realistic, low-light photograph shot on 35mm film (Kodak Portra 800) inside the cramped engine room of an aging industrial freighter. 24mm wide-angle lens. The perspective is eye-level, looking down a narrow maintenance walkway flanked by massive, greasy diesel engine manifolds. The air is thick with steam and volumetric haze. Lighting is practical and dim — flickering, amber-colored caged incandescent bulbs casting harsh, long shadows. Oily sheen on the diamond-plate metal flooring, peeling Safety Yellow paint on the handrails, condensation dripping from rusted overhead pipes. Analog pressure gauges with cracked glass faces. No digital technology visible. Pure mechanical heavy industry. High ISO film grain and slight motion blur on a cooling fan to sell the liveliness.
```
*Use with: `--quality --aspect 16:9`*

### Phase 2a: Tech Installation (feed Phase 1 via --reference)
```
Edit this image to convert a section of the walkway into a makeshift, high-tech workspace. In the foreground or middle distance, clear a space for a chaotic but powerful AI development rig. A sleek, matte-black server rack is bolted crudely to the steel floor, contrasting sharply with the rusty surroundings. A curved ultra-wide monitor sits on a heavy industrial workbench, displaying cascading terminal code in green and white text. Thick bundles of fiber-optic cables snake across the oily floor, taped down with gaffer tape, connecting the pristine server to the dirty ship power supply. The monitors and server LEDs emit a cool, clinical electric blue light that clashes with the warm, dirty amber of the ship's incandescent bulbs. The blue light reflects off the pools of oil on the floor. It looks like a cyberpunk squat inside a working ship. Keep the grime, the rust, the film grain.
```
*Use with: `--quality --reference base_image.png --aspect 16:9`*

### Phase 2b: Lived-In Nest Variant (feed Phase 1 via --reference)
```
Edit the image to place a lived-in, improvised workspace deeper down the walkway, tucked into a recess between the machinery. A heavy-duty, scratched folding table cluttered with tech. A multi-monitor setup — one vertical, one horizontal — glowing brightly, cutting through the steam. A half-empty, stained white ceramic coffee mug on a vibration dampener. Crumpled foil wrappers. A chaotic array of yellow and pink Post-it notes stuck to the monitor bezels and nearby rusty pipework. Scribbled diagrams in sharpie. An ugly, ergonomic mesh office chair that looks completely out of place in this industrial hellscape, turned slightly as if the user just stood up. The monitors display a dense IDE with a dark background. The soft white/blue glow illuminates the Safety Yellow paint on the nearby railing and catches the steam rising from the pipes. Maintain all original film grain, steam, and atmosphere.
```
*Use with: `--quality --reference base_image.png --aspect 16:9`*

### Phase 3: Cinematic Color Grade (feed Phase 2 via --reference)
```
Apply a cinematic color grade to this image. Push the shadows and dark areas slightly toward teal/green. Keep the highlights and warm light sources orange/amber. Crush the blacks slightly for depth. The overall feel should be like a still from a Denis Villeneuve film — moody, cinematic, unified color palette. Do NOT add any new objects or change the composition. Only adjust the color grading and atmosphere. Maintain all existing film grain and texture.
```
*Use with: `--quality --reference phase2_image.png --aspect 16:9`*
