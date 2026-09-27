# Prompt templates

Use only fields that improve the requested result. Preserve a specific brief; do not add unsupported objects, story or branding.

## Reference-based cinematic still

~~~text
Create a [ratio] [photo/illustration/graphic] for [placement]. Use [identity reference]
to preserve [visible facts]. Show [subject/action] in [environment/time]. Compose as
[shot size/angle], with [depth/negative space]. Camera look: [focal-length character/
depth of field]. Light: [source/direction/softness/shadows]. Treatment: [color/material].
Preserve [geometry/count/marks]. Change only [requested edit]. Avoid [likely failure].
Output [size/format].
~~~

## Precise photo edit

~~~text
Edit the supplied image only by [one change]. Keep [identity, perspective, crop, geometry,
existing light and unmentioned elements] unchanged. Match [perspective/material/light/
reflection/contact shadow] of the new element. Do not add text, logos, people or other
changes. [Ratio/size].
~~~

## Cinematic image-to-video

~~~text
One continuous [duration] shot from this exact starting frame. The camera at [position]
makes a [single measured move]. [Subject] [simple physically plausible action] at [pace].
Preserve [identity/geometry/count/markings/background]. Only [permitted environment]
changes. [Light/tone]. No cut, morphing, new object, extra part, unstable text/logo,
exaggerated gesture, or [specific known failure].
~~~

## Text-to-video

~~~text
[One subject] [one observable action] in [specific setting/time]. [Shot size, camera
height, composition], with [one primary movement]. [Motivated light/palette], [texture/
style]. [Duration/ratio if supported]. Maintain [continuity locks]. Avoid [likely
artifacts]. Do not generate readable text unless specifically required and verified.
~~~

## Shot-panel manifest

~~~text
Shot: [number/title]
Timeline: [source timecode/duration] | lyric/beat/dialogue: [cue]
Reference: [path/role] | class: ARCHIVE / AI CONCEPT / GRAPHIC
Subject/action: [one action]
Framing: [wide/medium/close/detail], [camera height/angle], [lens look]
Move: [one movement/direction or locked]
Light/color: [source/direction/contrast/tone]
Continuity locks: [identity/geometry/count/text/location]
Prompt: [model-facing prompt]
Reject if: [observable critical defect]
Cut to next: [reason/beat/transition]
~~~

## Targeted revision

~~~text
Keep the approved result identical in [accepted properties]. Change only [one observed
issue] by [concrete adjustment]. Do not alter [continuity locks]. Preserve [shot/camera/
light/subject]. [Output requirement].
~~~

## Before sending

- Does it describe one coherent image or continuous action?
- Are user facts separated from creative choices?
- Do references have clear roles?
- Are hard identity/geometry constraints observable?
- Are camera, light, motion and ratio compatible?
- Is the avoid list limited to likely defects?
- Should exact text/logo be added in post?
- Are private, unsupported or unlicensed assets being exposed/reproduced?
