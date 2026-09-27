# Image production and editing

## Decide the image's job

Choose whether the deliverable is a photograph, cinematic still, concept frame, character/vehicle sheet, poster, interface screenshot or infographic. Use image generation/editing for visual assets; use deterministic layout tools for exact copy, tables, logos and interface text.

For each source, record what must remain recognizable (identity, silhouette, dimensions, colors, part count, markings, location or clothing), what may change (crop, exposure, lighting, background, camera angle), and what must not be invented (unverified details, extra components, claims, copy or marks).

Keep identity references separate from style references. Use real subject photos to lock geometry; use style images only for requested light, texture, framing or palette. Resolve conflicting product versions before generation.

## Still-image prompt structure

Use the fields that matter:

1. Subject and intended use.
2. Environment, moment, time and weather.
3. Composition: frame size, camera height, placement, layers, negative space and reading direction.
4. Camera look and depth of field.
5. Light source/direction/softness, contrast, white balance, shadows and restrained grade.
6. Materials and details visible in the references.
7. Continuity constraints.
8. Likely failure modes to avoid.
9. Aspect ratio, resolution, crop and output format.

Preserve detailed user prompts without adding characters, objects, story beats, slogans or brand colors. For broad briefs, fill only missing choices that materially improve the result.

## Composition and camera

Use a composition that serves the story: thirds for balanced placement; leading lines to guide the eye; framing for depth; symmetry for stable architecture; negative space for a quiet subject or later typography; foreground/midground/background layers for depth; balance for stability. Do not force every technique into one image.

Focal-length language is a visual cue, not a guarantee:

- 18–24 mm look: broad environment and strong foreground perspective; avoid edge distortion on faces/products.
- 28–35 mm look: documentary environment with subject and setting.
- 50 mm look: natural perspective for product/workbench stills.
- 85 mm look: compressed portrait or isolated detail.
- 90–105 mm macro look: close material detail; verify that detail exists in the reference.

Eye level feels observational; low angle gives scale; high angle explains layout; overhead clarifies a workbench; POV communicates a participant view. Keep lens and shot-size cues compatible.

## Lighting and color

Name a motivated source, direction and quality: window side light, overcast sky, practical work light, soft fill, or golden-hour edge light. Request plausible contact shadows and reflections. Keep highlights recoverable and dark detail legible.

For cinematic documentary work, start with natural color, restrained contrast, coherent white balance and subtle grain only when appropriate. Avoid stacking neon, flare, glow, heavy grain and unrelated color grades.

## Reference-based edit loop

1. Create a clean baseline from the best source.
2. Change one main variable at a time: composition, light, background or angle.
3. Reuse only an approved output that preserves the subject.
4. Compare against source at the same crop and inspect technical details.
5. Preserve originals and record accepted prompt/model/version.

Do not ask a model for exact small copy, serial numbers or logos unless there is no alternative. Add approved vector marks/text in post and inspect spelling, glyphs, contrast and safe margins.

## Multi-view and storyboard assets

Create turnarounds only when source views establish unseen sides. Keep all views on one model and mark unverified angles as concepts. Never call a generated turnaround a measured drawing.

Generate storyboard scene images separately, then assemble a labeled sheet: shot number, timecode, action, camera/lens, movement, sound cue and source class (ARCHIVE / AI CONCEPT / GRAPHIC). Do not ask the image model to typeset the sheet. Add a turnaround/reference strip only when real consistent views support it.

## Review

Inspect fit-to-screen and detail scale. Check identity/version; component count, connections and proportions; contact with surfaces; faces/hands; reflections/shadows/perspective; text/logos; crop, noise and compression; intended ratio and safe zones. Reject critical false details even when the style looks polished.
