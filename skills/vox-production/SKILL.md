---
name: vox-production
description: Produce reusable Vox-style paper-collage explainer videos with external image assets, transparent element collections, fixed backgrounds, storyboard-driven motion, Remotion rendering, Doubao male narration, captions, and deterministic sound design.
metadata:
  short-description: End-to-end VOX collage video production kit
---

# VOX Production

Use this skill when the user asks for a VOX-style collage video, paper-collage explainer, or a reusable end-to-end production workflow.

## Required workflow

1. Read the episode brief and, when present, `work/friends-enemies/VOX_WORKFLOW.md`. Do not assume the topic or source is always IMA; follow the user's current source instruction.
2. Prepare the script and shot list before rendering. A shot is defined by narration meaning and action, not by a fixed number of shots. Confirm the script/shot mapping when the user requests staged approval.
3. For each reference image, generate a clean locked background plus transparent collection images containing 3–5 semantic elements. Split collections into independent PNGs only after visual QA. Do not use a 2x2 contact sheet as the production layout and do not silently fall back to crude rectangular crops.
4. Build a storyboard motion table with the Create Storyboard rules: shot purpose, narration cue, layer order, entry/exit, position, scale, rotation, camera move, and hold. Backgrounds stay fixed. Elements enter in staggered beats and settle; avoid unnecessary overlap. People remain above other visual elements; captions are an independent top layer.
5. Implement the motion table in Remotion using the bundled project. Keep the render deterministic: frame-based interpolation, explicit z-index/layer order, and no default sinusoidal floating for every object.
6. Generate narration with Doubao using the configured, user-approved male voice. Generate at the original rate, then apply FFmpeg `atempo=1.3` while preserving pitch. Divide subtitle and motion cue times by 1.3. Verify the actual voice by listening; do not accept an ID solely because it contains `male`.
7. Render captions from the retimed narration and add sound cues through the bundled `audio/render_soundscape.mjs` engine. Cue types may include whoosh, impact, notification, scatter, page, piano, creak, cards, crumple, focus, target, pencil, ui, and resolve.
8. Run media and motion QA: dimensions, duration, audio presence, script match, alpha integrity, locked background, no unintended overlap, captions within safe area, and at least two meaningful independently moving elements per shot where the shot allows it.
9. Deliver the MP4 plus the episode manifest, storyboard, cue file, QA reports, and source asset manifest. Never commit API keys, `.env`, raw credentials, or giant generated media unless the user explicitly asks for an archive.

## Setup on another device

Clone this repository, run `setup.ps1`, install the three user-provided credentials into a local `.env` (`DOUBAO_API_KEY`, `EXTERNAL_IMAGE_API_KEY`, `IMA_API_KEY`), and run the Remotion project. The IMA key is optional when the user supplies another source. External image generation is used for transparent collections and backgrounds; no built-in image generator is assumed.

Read the focused references only when needed:
- [references/portable-workflow.md](../../references/portable-workflow.md) for setup, API boundaries, and delivery.
- [references/motion-schema.md](../../references/motion-schema.md) for shot and layer data.
- [templates/sound-cues.example.json](../../templates/sound-cues.example.json) for deterministic sound placement.
