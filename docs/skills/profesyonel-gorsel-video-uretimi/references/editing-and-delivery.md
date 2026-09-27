# Editing, sound and delivery

## Build the timeline

Create a shot manifest: file, source/AI class, in/out, duration, ratio, frame rate, lyric/beat cue, transition, audio and review state. Preserve originals; work from selected copies.

1. Assemble a rough cut/animatic with intended audio and order.
2. Confirm story and timing against the whole master, including intro, lyric onset, rests, jingle and ending tail.
3. Replace approved shots, lightly match color, add transitions, and place logos/text as vector/text overlays.
4. Render a review copy and watch/listen from start to finish.
5. Fix observed issues; render and verify the delivery.

Cut on a lyric, beat, gesture or change of idea. Use dissolves when temporal continuity helps; keep them short. Avoid repeated generic transitions. A slow crop move can animate a still; maintain safe framing and vary shot size/movement for rhythm.

## Match music and dialogue

Use the supplied master when the user expects the existing song. Do not replace it with generated audio or let a video model alter lyrics. Place changes on actual lyric onsets, not merely subtitle cue boundaries; listen to the audio. Keep the song audible under dialogue, reduce only where needed, and ramp naturally around speech.

For voiceover, settle a script first; use requested voice/language/pronunciation; render separately from music and effects; check names, diacritics, pacing and intelligibility; add accurate captions as a separate text layer/track when requested.

Add only scene-appropriate ambience/foley; do not make sound fabricate evidence of an event. After muxing, check clipping, jumps, silence, sync drift and the ending tail.

## Graphics and typography

Add titles, captions, logos, URLs and exact marks in deterministic layers. Use approved vector/transparent artwork, not model-rendered logos. Check safe zones, contrast, spelling, Turkish glyph support and phone-size legibility.

Avoid persistent karaoke lyric overlays unless requested. If the song carries the message, use brief editorial titles or a clean end card.

## Encoding and verification

Choose dimensions, ratio, frame rate, codec and audio for the named platform and source quality. Preview renders may be smaller; do not upscale and call it native resolution. A broadly compatible MP4 often uses H.264 video and AAC audio.

Verify the output: play/listen all the way through; inspect frame sheet and transitions; compare sensitive subjects to references; use ffprobe for duration, dimensions, FPS, streams and codecs; check crop/ratio, black frames, freezes, dropped audio, sync and ending; confirm a standard player opens it.

For batch generation, keep a reject manifest and exclude unreviewed shots. Deliver video, storyboard, selected keyframes, prompts/manifests and assembly source when requested.
