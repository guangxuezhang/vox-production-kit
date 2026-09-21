---
name: vox-production
description: Produce reusable Vox-style paper-collage explainer videos with external image assets, transparent element collections, fixed backgrounds, storyboard-driven motion, Remotion rendering, Doubao male narration, captions, and deterministic sound design.
metadata:
  short-description: End-to-end VOX collage video production kit
---

# VOX Production

Portable service setup: after cloning, read SERVICES.md and run configure.py. It prompts for Doubao Key, FriModel Key, and optional IMA Client ID plus Key. Use vox.py check/image/tts/ima. This supersedes the older .env-only setup below. Do not claim local configuration checks prove successful API authentication; do not invoke paid generation during installation.

Use this skill when the user asks for a VOX-style collage video, paper-collage explainer, or a reusable end-to-end production workflow.

## Required workflow

1. Read the episode brief and, when present, `work/friends-enemies/VOX_WORKFLOW.md`. Do not assume the topic or source is always IMA; follow the user's current source instruction.
2. Prepare the script and shot list. A shot is defined by narration meaning and action, not by a fixed number of shots. Confirm the script/shot mapping when the user requests staged approval. Generate the approved male narration, apply pitch-preserving `atempo=1.3`, and measure the processed audio before fixing scene, caption, or motion times. Retarget word timestamps and cue times to the processed audio; verify the voice by listening.
3. For each reference image, generate a clean locked background plus transparent collection images containing 3–5 semantic elements. Split collections into independent PNGs only after visual QA. Do not use a 2x2 contact sheet as the production layout and do not silently fall back to crude rectangular crops.
4. **Director gate:** after asset QA, read the installed Create Storyboard skill and produce a per-shot action plan tied to final-audio word cues. For each independent asset, record purpose, exact cue, entry/settle/exit frames, trajectory, position, scale, rotation, layer, and handoff to the next beat. Record each shot's visual focus and the receiving cue for the next shot. A generic sequence of identical left/right/bottom entrances is not a completed storyboard. Confirm the action plan with the user when staged review is requested. Do not equate reading a skill with applying it.
5. Read the installed Remotion best-practices router and its relevant references, then implement the action plan in Remotion. Render from the same plan data, or validate every planned asset and cue against the renderer before rendering. For a new episode, use `node scripts/render_episode.cjs <episode-plan.json> <composition-id> <output.mp4>` so director-plan validation runs before Remotion; if it fails, stop before preview or final render. The repo's plain `pnpm --dir remotion render` remains only for the bundled historical reference episode. Keep the render deterministic: frame-based interpolation, explicit z-index/layer order, fixed backgrounds, and no default sinusoidal floating for every object. People remain above other visual elements; captions are an independent top layer. All on-canvas annotations, labels, and emphasis words are separate text layers with an explicit z value at or above 90; visual assets stay below 90, people stay above other visual assets, and captions stay at or above 100. Preflight must reject missing or too-low annotation z values.
6. Render captions from the retimed narration and add sound cues through the bundled `audio/render_soundscape.mjs` engine. Cue types may include whoosh, impact, notification, scatter, page, piano, creak, cards, crumple, focus, target, pencil, ui, and resolve.
7. Run media and motion QA: dimensions, duration, audio presence, script match, alpha integrity, locked background, no unintended overlap, captions within safe area, and at least three meaningful independent visual elements per ordinary-mode shot. Inspect each shot's start, key action, settle, and handoff frames. A rendered video without a validated director plan is a diagnostic draft, not an accepted preview.
8. Deliver the MP4 plus the episode manifest, storyboard, cue file, QA reports, and source asset manifest. Never commit API keys, `.env`, raw credentials, or giant generated media unless the user explicitly asks for an archive.

## Setup on another device

Clone this repository, run `setup.ps1`, install the three user-provided credentials into a local `.env` (`DOUBAO_API_KEY`, `EXTERNAL_IMAGE_API_KEY`, `IMA_API_KEY`), and run the Remotion project. The IMA key is optional when the user supplies another source. External image generation is used for transparent collections and backgrounds; no built-in image generator is assumed.

Read the focused references only when needed:
- [references/portable-workflow.md](references/portable-workflow.md) for setup, API boundaries, and delivery.
- [references/motion-schema.md](references/motion-schema.md) for shot and layer data.
- [references/director-plan.md](references/director-plan.md) for the required cue-driven plan format and preflight gate.
- After cloning, use `work/own-framework/sound-cues.json` as the working sound schema.

## Repository bootstrap

Repository: https://github.com/guangxuezhang/vox-production-kit.git
When the Skill is installed without the project, clone that repository into a user workspace and run its setup.ps1. Never replace a dirty checkout or pull over user edits. Read README.md for executable commands and remaining provider requirements. The included own-framework episode is a reference implementation, not a mandatory script or shot count. Confirm each production stage with the user before advancing unless they explicitly authorize a full run.
