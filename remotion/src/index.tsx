import React from 'react';
import {Finished} from './finished';
import finalData from './final-data.json';
import {AbsoluteFill,Composition,registerRoot,Img,staticFile,useCurrentFrame,interpolate,Easing} from 'remotion';
const opt={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const,easing:Easing.bezier(.16,1,.3,1)};
const Layer:React.FC<{file:string;x:number;y:number;w:number;start:number;dx?:number;dy?:number;angle?:number;z:number}>=({file,x,y,w,start,dx=0,dy=0,angle=0,z})=>{
 const f=useCurrentFrame();
 return <div style={{position:'absolute',left:x,top:y,width:w,zIndex:z,opacity:f<start?0:1,translate:`${interpolate(f,[start,start+24],[dx,0],opt)}px ${interpolate(f,[start,start+24],[dy,0],opt)}px`,rotate:`${interpolate(f,[start,start+24],[angle,0],opt)}deg`}}><Img src={staticFile(file)} style={{width:'100%',display:'block',clipPath:file==='document.png'?'inset(8% 0 0 0)':undefined}}/></div>;
};
const Shot01=()=>{const f=useCurrentFrame();const captions=[[0,70,'领导回了一个“嗯”'],[70,150,'你把聊天记录翻了十遍'],[150,222,'事情还没变'],[222,360,'你已经在脑子里','替自己开完了一场批斗会']];const cap=captions.find(c=>f>=Number(c[0])&&f<Number(c[1]));
 return <AbsoluteFill style={{background:'#eee5d3',overflow:'hidden',fontFamily:'Microsoft YaHei'}}>
 <Img src={staticFile('background.png')} style={{position:'absolute',width:'100%',height:'100%',objectFit:'cover'}}/>
 <Layer file="document.png" x={80} y={1160} w={490} start={0} z={1}/>
 <Layer file="phone.png" x={68} y={160} w={500} start={8} dx={-820} angle={-12} z={2}/>
 <div style={{position:'absolute',left:325,top:321,zIndex:3,fontSize:48,fontWeight:900,rotate:'-10deg',opacity:f>=38?1:0}}>嗯</div>
 {[72,100,128].map((s,i)=><div key={s} style={{position:'absolute',left:600,top:220+i*170,width:365,padding:'28px 22px',boxSizing:'border-box',background:i===2?'#c05724':'#e3d6bf',color:i===2?'#fff':'#242522',fontSize:42,fontWeight:700,zIndex:4,opacity:f<s?0:1,translate:`${interpolate(f,[s,s+20],[650,0],opt)}px 0px`,rotate:`${i%2?3:-3}deg`,boxShadow:'0 8px 0 #00000016'}}>{['他什么意思？','是不是不满意？','是我做错了？'][i]}</div>)}
 <Layer file="magnifier.png" x={380} y={660} w={470} start={158} dx={780} dy={-320} angle={26} z={5}/>
 <Layer file="person.png" x={440} y={1070} w={570} start={224} dy={1000} angle={-7} z={10}/>
 <div style={{position:'absolute',left:80,right:80,bottom:95,zIndex:20,textAlign:'center',fontSize:48,fontWeight:700,lineHeight:1.5,color:'#252522'}}>{cap?.slice(2).map((t,i)=><div key={i}><span style={{background:'#f7f1e4ed',padding:'6px 18px',boxDecorationBreak:'clone'}}>{t}</span></div>)}</div>
 </AbsoluteFill>};
const Root=()=> <><Composition id="Finished" component={Finished} width={1080} height={1920} fps={30} durationInFrames={finalData.durationInFrames}/><Composition id="Shot01" component={Shot01} width={1080} height={1920} fps={30} durationInFrames={360}/><Composition id="FullDraft" component={require('./full').Full} width={1080} height={1920} fps={30} durationInFrames={720}/></>;
registerRoot(Root);
