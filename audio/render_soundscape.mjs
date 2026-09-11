#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const argv = process.argv.slice(2);
const arg = n => argv[argv.indexOf(n) + 1];
const configPath = arg('--config');
const outputPath = arg('--output');
if (!configPath || !outputPath) throw new Error('Usage: node render_soundscape.mjs --config sound-cues.json --output soundscape.wav');
const c = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const sr = c.sample_rate || 44100, seconds = c.duration, n = Math.ceil(sr * seconds);
const l = new Float64Array(n), r = new Float64Array(n);
let seed = c.seed || 20260904;
const rnd = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296) * 2 - 1;
const add = (t, d, fn, gain=1, pan=0) => {
  const a=Math.max(0,Math.floor(t*sr)), b=Math.min(n,a+Math.floor(d*sr));
  for(let i=a;i<b;i++){const x=(i-a)/sr, env=Math.sin(Math.PI*x/d); const v=fn(x,d)*env*gain; l[i]+=v*(1-pan)*.5; r[i]+=v*(1+pan)*.5;}
};
const tone=(f,x)=>Math.sin(2*Math.PI*f*x);
// Original, restrained editorial underscore. No external samples or licensed music.
const bpm=c.bpm||88, beat=60/bpm, chords=[[110,138.59,164.81],[98,123.47,146.83],[82.41,110,138.59],[92.5,116.54,146.83]];
const bedGain=c.bed_gain ?? 1;
for(let t=0,k=0;t<seconds && bedGain>0;t+=beat,k++){
  const ch=chords[Math.floor(k/4)%chords.length];
  add(t,Math.min(beat*.92,seconds-t),(x,d)=>ch.reduce((s,f)=>s+tone(f,x)*.22,0),.065*bedGain,0);
  if(k%2===0) add(t,.14,(x)=>Math.sin(2*Math.PI*(72-34*x/.14)*x),.16*bedGain,0);
  if(k%4===2) add(t,.08,()=>rnd(),.035*bedGain,.15);
}
const fx={
  whoosh:(t,g,p)=>add(t,.46,(x,d)=>rnd()*(x/d),g*.32,p),
  impact:(t,g,p)=>add(t,.32,x=>tone(62,x)*Math.exp(-11*x)+rnd()*.12*Math.exp(-18*x),g*.62,p),
  notification:(t,g,p)=>{add(t,.16,x=>tone(740,x),g*.25,p);add(t+.13,.2,x=>tone(988,x),g*.22,p);},
  scatter:(t,g,p)=>[0,.09,.18,.31].forEach((o,i)=>add(t+o,.13,x=>rnd()*.55+tone(180+i*55,x)*.2,g*.22,p+(i-1.5)*.18)),
  page:(t,g,p)=>add(t,.62,(x,d)=>rnd()*(.3+.7*x/d),g*.20,p),
  piano:(t,g,p)=>[220,277.18,329.63].forEach((f,i)=>add(t+i*.08,.9,x=>tone(f,x)*Math.exp(-2.8*x),g*.12,p)),
  creak:(t,g,p)=>add(t,.7,x=>tone(92+18*Math.sin(x*12),x)*.45+rnd()*.16,g*.20,p),
  cards:(t,g,p)=>[0,.08,.16,.24].forEach((o,i)=>add(t+o,.11,()=>rnd(),g*.16,p+(i-1.5)*.12)),
  crumple:(t,g,p)=>add(t,.58,(x)=>rnd()*(.35+.65*Math.sin(x*46)**2),g*.24,p),
  focus:(t,g,p)=>add(t,.7,(x,d)=>tone(210+520*x/d,x),g*.18,p),
  target:(t,g,p)=>{add(t,.42,(x,d)=>tone(150+700*x/d,x),g*.22,p);fx.impact(t+.36,g*.85,p);},
  pencil:(t,g,p)=>add(t,.48,()=>rnd(),g*.10,p),
  ui:(t,g,p)=>add(t,.18,x=>tone(520,x)+tone(780,x)*.5,g*.13,p),
  resolve:(t,g,p)=>[220,277.18,329.63,440].forEach((f,i)=>add(t+i*.11,1.25,x=>tone(f,x)*Math.exp(-1.8*x),g*.11,p))
};
for(const q of c.cues||[]){if(!fx[q.type]) throw new Error(`Unknown cue: ${q.type}`);fx[q.type](q.time,q.gain??1,q.pan??0);}
let peak=.0001; for(let i=0;i<n;i++) peak=Math.max(peak,Math.abs(l[i]),Math.abs(r[i]));
const scale=Math.min(1,(c.peak||.82)/peak), data=Buffer.alloc(n*4);
for(let i=0;i<n;i++){data.writeInt16LE(Math.round(Math.max(-1,Math.min(1,l[i]*scale))*32767),i*4);data.writeInt16LE(Math.round(Math.max(-1,Math.min(1,r[i]*scale))*32767),i*4+2);}
const h=Buffer.alloc(44);h.write('RIFF');h.writeUInt32LE(36+data.length,4);h.write('WAVE',8);h.write('fmt ',12);h.writeUInt32LE(16,16);h.writeUInt16LE(1,20);h.writeUInt16LE(2,22);h.writeUInt32LE(sr,24);h.writeUInt32LE(sr*4,28);h.writeUInt16LE(4,32);h.writeUInt16LE(16,34);h.write('data',36);h.writeUInt32LE(data.length,40);
fs.mkdirSync(path.dirname(outputPath),{recursive:true});fs.writeFileSync(outputPath,Buffer.concat([h,data]));
console.log(JSON.stringify({output:path.resolve(outputPath),duration:seconds,sample_rate:sr,cues:(c.cues||[]).length,peak_target:c.peak||.82}));
