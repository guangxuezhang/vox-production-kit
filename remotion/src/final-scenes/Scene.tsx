import React from 'react';
import {AbsoluteFill,Img,staticFile,useCurrentFrame,interpolate,Easing} from 'remotion';
import data from '../final-data.json';
const ease={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const,easing:Easing.bezier(.16,1,.3,1)};
const Layer=({l,n}:{l:any;n:number})=>{
 const f=useCurrentFrame();
 const m=l.move;
 const exit=l.exit;
 const x=m?interpolate(f,[m.frame,m.frame+24],[l.x,m.x],ease):l.x;
 const y=m?interpolate(f,[m.frame,m.frame+24],[l.y,m.y],ease):l.y;
 const w=m?interpolate(f,[m.frame,m.frame+24],[l.w,m.w],ease):l.w;
 const ex=exit?interpolate(f,[exit.frame,exit.frame+20],[0,exit.dx],ease):0;
 const ey=exit?interpolate(f,[exit.frame,exit.frame+20],[0,exit.dy],ease):0;
 const orange=(n===1&&['shot01-assets-b-obj1.png','shot01-assets-b-obj2.png'].includes(l.file))||(n===5&&l.file==='shot05-assets-b-obj2.png')||(n===6&&l.file==='shot06-assets-b-obj2.png')||(n===4&&l.file==='shot04-assets-a-obj3.png')||(n===8&&l.file==='shot08-assets-a-obj3.png');
 return <div style={{position:'absolute',left:x,top:y,width:w,height:l.h*w/l.w,zIndex:l.z,opacity:f<l.start?0:1,translate:`${interpolate(f,[l.start,l.start+l.entry],[l.dx,0],ease)+ex}px ${interpolate(f,[l.start,l.start+l.entry],[l.dy,0],ease)+ey}px`,rotate:`${interpolate(f,[l.start,l.start+l.entry],[l.dx?Math.sign(l.dx)*9:-7,l.angle],ease)}deg`}}>
  <Img src={staticFile(`cutouts/${l.file}`)} style={{width:'100%',height:'100%',display:'block',filter:'drop-shadow(0px 5px 3px rgba(38,28,16,.16))'}}/>
  {l.label&&<div style={{position:'absolute',left:`${l.labelX*100}%`,top:`${l.labelY*100}%`,translate:'-50% -50%',width:l.labelX>.6?'43%':'88%',textAlign:'center',fontWeight:900,fontSize:l.fontSize,lineHeight:1.35,whiteSpace:'pre-line',color:orange?'#fff4dc':'#282926'}}>{l.label}</div>}
 </div>;
};
export const Scene=({n}:{n:number})=>{
 const s=data.scenes[n-1];const f=useCurrentFrame();
 return <AbsoluteFill style={{overflow:'hidden',background:'#eee5d3',fontFamily:'Microsoft YaHei, sans-serif',color:'#262824'}}>
  <Img src={staticFile(`shot${String(n).padStart(2,'0')}-background.png`)} style={{position:'absolute',width:1080,height:1920,objectFit:'cover'}}/>
  <div style={{position:'absolute',left:85,top:95,fontSize:27,letterSpacing:5,fontWeight:700,color:'#934523'}}>建立自己的判断框架 · {String(n).padStart(2,'0')}</div>
  <div style={{position:'absolute',left:80,right:80,top:158,fontSize:88,fontWeight:900,lineHeight:1.13,letterSpacing:-2,whiteSpace:'pre-line',translate:`0 ${interpolate(f,[0,16],[35,0],ease)}px`,opacity:interpolate(f,[0,8],[0,1],ease)}}>{s.title}</div>
  {s.layers.map((l,i)=><Layer key={i} l={l} n={n}/>)}
 </AbsoluteFill>;
};
