const fs = require('fs');
const path = require('path');

function fail(message) {
  console.error(`Director plan invalid: ${message}`);
  process.exit(1);
}
const file = process.argv[2];
if (!file) fail('pass an episode-plan.json path');
const planPath = path.resolve(file);
if (!fs.existsSync(planPath)) fail(`plan not found: ${planPath}`);
const plan = JSON.parse(fs.readFileSync(planPath, 'utf8'));
const {fps, audioDurationSeconds, narrationText, scenes} = plan;
if (!Number.isFinite(fps) || fps <= 0 || !Number.isFinite(audioDurationSeconds) || audioDurationSeconds <= 0) fail('final audio duration and fps are required');
if (!narrationText || !Array.isArray(scenes) || scenes.length === 0) fail('narration and scenes are required');
const spoken = narrationText.replace(/[\s，。！？、；：,.!?;:]/g, '');
const base = path.dirname(planPath);
let previousEnd = 0;
for (const scene of scenes) {
  const label = `scene ${scene.id ?? '?'}`;
  if (!Number.isInteger(scene.startFrame) || !Number.isInteger(scene.endFrame) || scene.startFrame !== previousEnd || scene.endFrame <= scene.startFrame) fail(`${label}: invalid scene boundary`);
  previousEnd = scene.endFrame;
  if (!scene.focus || !scene.handoff || !scene.background) fail(`${label}: focus, handoff, and background are required`);
  if (!fs.existsSync(path.resolve(base, scene.background))) fail(`${label}: background file missing`);
  if (!Array.isArray(scene.layers) || scene.layers.length < 3) fail(`${label}: at least three independent visual layers are required`);
  for (const annotation of [...(scene.labels || []), ...(scene.annotations || [])]) {
    if (!annotation.text || !Number.isInteger(annotation.startFrame) || !Number.isInteger(annotation.endFrame)) fail(`${label}: annotation timing/text is required`);
    if (!Number.isInteger(annotation.z) || annotation.z < 90) fail(`${label}: annotation ${annotation.text} must use z>=90`);
    if (annotation.startFrame < scene.startFrame || annotation.endFrame <= annotation.startFrame || annotation.endFrame > scene.endFrame) fail(`${label}: annotation ${annotation.text} is outside scene`);
  }
  const assets = new Set();
  const starts = new Set();
  for (const layer of scene.layers) {
    const who = `${label}, layer ${layer.id ?? '?'}`;
    if (!layer.id || !layer.asset || assets.has(layer.asset)) fail(`${who}: missing or duplicate independent asset`);
    assets.add(layer.asset);
    if (!fs.existsSync(path.resolve(base, layer.asset))) fail(`${who}: asset file missing`);
    if (/collection(?:[-_.]|$)/i.test(path.basename(layer.asset)) && !/collection-\d+\.png$/i.test(path.basename(layer.asset))) fail(`${who}: full collection sheet cannot be a layer`);
    const cue = String(layer.cueText || '').replace(/[\s，。！？、；：,.!?;:]/g, '');
    if (!cue || !spoken.includes(cue)) fail(`${who}: cue is absent from narration`);
    if (!Number.isFinite(layer.cueTimeSeconds) || layer.cueTimeSeconds < scene.startFrame / fps - 0.2 || layer.cueTimeSeconds > scene.endFrame / fps + 0.2) fail(`${who}: cue time is outside scene`);
    if (!layer.purpose || !layer.action || !layer.enter?.from || !layer.enter?.to) fail(`${who}: purpose, action, and trajectory are required`);
    const enter = layer.enter;
    if (!Number.isInteger(enter.startFrame) || !Number.isInteger(enter.settleFrame) || enter.startFrame < scene.startFrame || enter.settleFrame <= enter.startFrame || enter.settleFrame > scene.endFrame) fail(`${who}: invalid entry and settle frames`);
    if (!Number.isInteger(layer.holdUntilFrame) || layer.holdUntilFrame < enter.settleFrame || layer.holdUntilFrame > scene.endFrame) fail(`${who}: invalid hold`);
    if (!Number.isInteger(layer.z)) fail(`${who}: z-index missing`);
    starts.add(enter.startFrame);
  }
  if (starts.size < 2) fail(`${label}: every asset starts together`);
}
if (Math.abs(previousEnd / fps - audioDurationSeconds) > 0.15) fail('scene timeline differs from final audio by more than 0.15 seconds');
console.log(`Director plan valid: ${scenes.length} scenes, ${previousEnd} frames`);
