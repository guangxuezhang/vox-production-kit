import React from 'react';
import {AbsoluteFill,Audio,Sequence,staticFile,useCurrentFrame} from 'remotion';
import data from './final-data.json';
import {Scene01} from './final-scenes/Scene01';
import {Scene02} from './final-scenes/Scene02';
import {Scene03} from './final-scenes/Scene03';
import {Scene04} from './final-scenes/Scene04';
import {Scene05} from './final-scenes/Scene05';
import {Scene06} from './final-scenes/Scene06';
import {Scene07} from './final-scenes/Scene07';
import {Scene08} from './final-scenes/Scene08';
const scenes=[Scene01,Scene02,Scene03,Scene04,Scene05,Scene06,Scene07,Scene08];
export const Finished=()=>{
 const frame=useCurrentFrame();const ms=frame/30*1000;const cap=data.captions.find(c=>ms>=c.startMs&&ms<c.endMs);
 return <AbsoluteFill style={{background:'#ede3cf',fontFamily:'Microsoft YaHei, sans-serif'}}>
  <Audio src={staticFile('narration-final.mp3')}/>
  {data.scenes.map((s,i)=>{const C=scenes[i];return <Sequence key={i} from={s.start} durationInFrames={s.duration} name={`镜${i+1} ${s.title.replace('\n',' ')}`}><C/></Sequence>})}
  {data.scenes.flatMap(s=>s.layers.filter(l=>l.z===30||l.z===5).map((l,i)=><Sequence key={`${s.n}-${i}`} from={s.start+l.start} durationInFrames={Math.min(12,data.durationInFrames-s.start-l.start)}><Audio src={staticFile('paper-swish.wav')} volume={.12}/></Sequence>))}
  {cap&&<div style={{position:'absolute',zIndex:100,left:75,right:75,bottom:108,textAlign:'center',fontSize:52,fontWeight:700,lineHeight:1.4,color:'#fff9ee'}}><span style={{background:'#242620ee',padding:'12px 20px',boxDecorationBreak:'clone',WebkitBoxDecorationBreak:'clone'}}>{cap.text}</span></div>}
 </AbsoluteFill>;
};
