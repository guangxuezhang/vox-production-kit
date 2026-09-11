import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const [keyFile, projectDir, requestedSpeaker, requestedStem, requestedSpeechRate, requestedTextFile] = process.argv.slice(2);
if (!keyFile || !projectDir) throw new Error('Usage: node doubao_tts_test.mjs <key-file> <project-dir>');

let apiKey = fs.readFileSync(keyFile, 'utf8').trim();
const assignment = apiKey.match(/(?:DOUBAO_SPEECH_API_KEY|X-Api-Key)\s*=\s*["']?([^\s"']+)/i);
if (assignment) apiKey = assignment[1];
if (!apiKey || /\s/.test(apiKey) || apiKey.length < 12) throw new Error('API key file format is invalid');

const privateDir = path.join(projectDir, '.private');
const audioDir = path.join(projectDir, 'motion', 'media', 'audio');
fs.mkdirSync(privateDir, { recursive: true });
fs.mkdirSync(audioDir, { recursive: true });
// Credentials stay in memory; do not copy them into generated project files.

const requestId = crypto.randomUUID();
const speaker = requestedSpeaker || 'zh_male_yuanboxiaoshu_uranus_bigtts';
const outputStem = requestedStem || 'doubao_voice_test';
const speechRate = requestedSpeechRate == null ? 0 : Number(requestedSpeechRate);
if (!Number.isFinite(speechRate)) throw new Error('speech-rate must be a number');
const textPrompt = requestedTextFile
  ? fs.readFileSync(requestedTextFile, 'utf8').trim()
  : '真正拖垮你的，往往不是事情太多，而是注意力被无法改变的人和事占满。';
if (!textPrompt) throw new Error('text prompt is empty');
const response = await fetch('https://openspeech.bytedance.com/api/v3/tts/create', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Api-Key': apiKey,
    'X-Api-Request-Id': requestId,
  },
  body: JSON.stringify({
    model: 'seed-audio-1.0',
    text_prompt: `请使用@音频1的声音，以自然、沉稳的男声完整朗读以下旁白。只朗读旁白正文，不加其他话，不要配乐或音效：\n${textPrompt}`,
    references: [{speaker}],
    audio_config: {
      format: 'mp3',
      sample_rate: 44100,
      speech_rate: speechRate,
      loudness_rate: 0,
      pitch_rate: 0,
      enable_subtitle: true,
    },
  }),
});

const raw = await response.text();
let data;
try { data = JSON.parse(raw); } catch { throw new Error(`Non-JSON response (HTTP ${response.status})`); }
if (!response.ok || (data.code != null && data.code !== 0)) {
  throw new Error(`Doubao API failed: HTTP ${response.status}; code=${data.code}; message=${data.message || 'unknown'}`);
}

const output = path.join(audioDir, `${outputStem}.mp3`);
if (data.audio) fs.writeFileSync(output, Buffer.from(data.audio, 'base64'));
else if (data.url) {
  const audioResponse = await fetch(data.url);
  if (!audioResponse.ok) throw new Error(`Audio download failed: HTTP ${audioResponse.status}`);
  fs.writeFileSync(output, Buffer.from(await audioResponse.arrayBuffer()));
} else throw new Error('Response contains neither audio nor URL');

fs.writeFileSync(path.join(audioDir, `${outputStem}.subtitle.json`), JSON.stringify(data.subtitle || {}, null, 2));
console.log(JSON.stringify({ ok: true, output, speaker, speechRate, bytes: fs.statSync(output).size, duration: data.duration, originalDuration: data.original_duration, hasSubtitle: Boolean(data.subtitle), requestId }));
