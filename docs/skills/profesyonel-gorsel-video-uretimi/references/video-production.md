# Cinematic video production

## Choose the production path

- Real footage is first choice for identifiable people, precise operation, important places, authentic events and factual claims.
- AI image-to-video suits controlled camera motion, short B-roll and atmosphere based on an approved still.
- AI text-to-video suits fictional/non-factual scenes where exact continuity matters less.
- Post-production pan/zoom or parallax is safer than regeneration when the still is right but generation changes the subject.
- Remotion or another deterministic editor suits graphics, captions, screen recordings and repeatable layouts. Keep exact logos/text in separate layers.

Choose according to user preference, available tools, fidelity, duration, format and budget. Do not treat a static model comparison as current; verify official documentation before generation.

## Plan the story and shots

Write a one-line premise and a simple progression (opening → action/work → proof/result → ending). Give each shot an editorial purpose. Record:

- timeline/timecode and lyric, dialogue, beat or sound cue;
- subject and one visible action;
- source and class: real archive, licensed material, AI concept or graphic;
- shot size, camera height, lens look, composition and one primary movement;
- lighting, environment, color continuity and sound;
- must-preserve details and observable rejection criteria;
- cut reason/transition into the next shot.

An animatic/storyboard is a plan, not finished video. Number panels chronologically. Add clear production labels after image generation. Keep generated image text out of the sheet; crop a clean panel as a video model reference.

## Camera and movement

Pan/tilt rotates in place. Dolly/push/pull moves the camera toward/away. Tracking follows a moving subject. Orbit travels around a subject. Zoom changes focal length. Static/locked means no camera movement. Handheld is intentional small shake.

Do not ask for unrelated movements in one short generation. Avoid large/fast moves around detailed machinery, faces or text. If the subject must remain fixed, state it and move only the camera.

## Image-to-video prompt pattern

The input frame establishes appearance, layout and style. Describe change over time rather than restating the image:

~~~text
One continuous [duration] shot. The camera [single restrained movement, distance, height].
[Subject action and pace]. Keep [identity, geometry, count, markings, people and background]
fixed. Only [permitted environmental motion] changes. [Light and atmosphere].
No cuts, morphing, added objects, invented text/logos, exaggerated gestures, or [known failure].
~~~

Use natural micro-actions for people; avoid exaggerated expressions and gestures. For machinery, lock part counts and geometry; state whether it is grounded, operating or moving.

## Text-to-video prompt pattern

Describe subject → action → setting → framing/camera → light/atmosphere → style/texture → duration/ratio when supported. Use one shot and one primary action. Add exact language, lyrics, marks and end cards in post.

## Use storyboard references as actual inputs

Verify the model supports the reference type/count. Match one clean panel to its intended shot; do not send the whole sheet if the model will interpret it as a collage. Crop labels out unless they are intentional scene content.

Assign references deliberately: identity/object; style; first frame; supported end frame; prior video/interaction only when its state and continuation are verified.

## Model routing

For Gemini API implementation, load global gemini-api-dev or gemini-omni-flash-api and read relevant live docs. The Gemini API CLI is installed as gemini-api; check gemini-api video --help/--usage, inspect --schema for body commands, and run --dry-run before paid/network generation. Do not assume model IDs or limits from a static sheet.

## Iterate on evidence

Generate one representative shot. Make a contact sheet including first, middle and final frames; inspect full playback and compare source details. Classify defects:

- critical identity/physics error: reject;
- small color/exposure mismatch: correct in post;
- camera move too strong: reduce that move only, or animate the still;
- wrong framing: repair the still first;
- bad transition: edit the timeline;
- bad logo/text: replace with true vector/text.

Retry only when a targeted change can plausibly help. If a critical defect repeats, switch methods.
