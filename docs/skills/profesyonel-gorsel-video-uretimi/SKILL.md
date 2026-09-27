---
name: profesyonel-gorsel-video-uretimi
description: Plan, generate, edit, storyboard, assemble, and quality-check polished images and videos from briefs and visual references using Gemini, image-generation tools, and deterministic editing.
---

# Professional image and video production

Use this skill for image creation/editing, cinematic scenes, storyboards, AI video, music videos, explainers, and reference-based visual assets.

Turn the brief into a concrete visual result. Preserve real-world facts, select the right generation/editing path, inspect the actual output, and deliver media when requested. Do not stop at prompts or a storyboard when the final version of the media is requested.

## Operating sequence

1. **Read the brief.** Identify purpose, audience, platform, duration, ratio, tone, supplied assets, brand rules, audio and deliverables. Infer from context where clear; ask only for a decision that changes the result.
2. **Inspect references.** Open every supplied image/video/document. Record visible facts separately from guesses. Give each reference a role: identity/product geometry, style/light, composition/camera, or content evidence. Do not let a style reference redefine the real subject.
3. **Plan the sequence.** For multi-shot work, create a shot list and visual storyboard before expensive video generation. Specify lyric/dialogue/beat timing, duration, action, framing, camera move, light, reference and acceptance criteria per panel.
4. **Make strong stills first.** If camera angle, light, or source quality needs work, produce and inspect a cinematic keyframe before animating it. Preserve identity, geometry, object count, markings and important text. Add exact copy and logos later in deterministic design layers.
5. **Choose tools per shot.** First, determine the user's model preference. Then, if stills are needed, use available image tools. If video is required, check if Gemini Omni is suitable for the requested motion. Use FFmpeg or Remotion for timing, graphics, transitions and audio. Read the relevant installed official/model skill before writing API code.
6. **Generate and inspect.** Start with one representative shot; inspect it before batching. Review first, middle and final frames, transitions and full playback. Compare identity-sensitive scenes with their source.
7. **Assemble and deliver.** Match shots to the soundtrack, build a preview, make targeted fixes, render and verify. Provide the actual media plus reusable project/source files when requested. Label real source images, generated reconstructions and graphics accurately.

## Quality bar

- Give each shot one primary action and one dominant camera move.
- Prefer believable materials, restrained motion, purposeful framing and coherent light over spectacle.
- Keep gestures, faces and camera energy proportional. Avoid exaggerated surprise, constant slow motion, random flares, decorative UI, gratuitous particles and generic stock inserts.
- Do not fabricate technical parts, branding, results, locations or documentary evidence. Mark generated new angles as concepts or AI scenes.
- Reject generations that alter critical geometry, identity, object count, text, logos, hands or continuity. Retry with one targeted correction; if the defect repeats, use real footage, post-production motion on a still, or redesign the shot.
- Keep credentials in environment variables or supported secret storage. Never print, commit, or include keys in prompts, metadata, logs or generated files.
- Storyboard sheets need readable labels laid out after image generation, not tiny model-rendered text.

## References

- Read references/image-production.md for photo editing, camera, light, composition and reference control.
- Read references/video-production.md for shot design, storyboards, image-to-video prompts and continuity.
- Read references/editing-and-delivery.md for audio, timelines, graphics, encoding and review.
- Read references/prompt-templates.md for adaptable still, edit, video and revision prompt structures.
- Read references/gemini-cli.md when using Google's Gemini API CLI.
- Use references/gorsel-video-prompt-uretim-el-kitabi.md as a detailed camera/style/source guide; check current model capabilities separately.
- For Gemini API implementation, load gemini-api-dev or gemini-omni-flash-api. For realtime audio/video applications, load gemini-live-api-dev.
- Check current official model/API documentation at execution time. Names, limits, pricing and schemas change.
