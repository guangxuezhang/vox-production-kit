# VOX Production Kit

This repository packages the reusable VOX workflow: Skill instructions, Remotion project scaffold, asset and motion schemas, audio cue rendering, QA helpers, and setup guidance.

## Quick start

```powershell
pwsh ./setup.ps1
Copy-Item .env.example .env
# Fill DOUBAO_API_KEY, EXTERNAL_IMAGE_API_KEY, and optionally IMA_API_KEY locally.
pnpm --dir remotion install
pnpm --dir remotion dev
```

The package does not contain credentials or a fixed topic. Each episode supplies its own script, reference images, generated assets, storyboard, and manifest.

## Production order

Script and shot mapping → reference style approval → external transparent collections + clean locked backgrounds → alpha split and QA → Create Storyboard motion table → Remotion implementation → Doubao narration → 1.3x pitch-preserving retime → captions and soundscape → render and QA.

The default voice and timing contract is recorded in `templates/vox-audio-defaults.json`. The deterministic sound engine is in `audio/render_soundscape.mjs`.

## Included skills

The local Codex installation should have `create-storyboard`, `remotion-best-practices`, and `vox-director`. This kit also includes the executable sound renderer so another device can reproduce the sound layer without relying on a machine-local path.
