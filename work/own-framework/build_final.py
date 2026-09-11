from pathlib import Path
import json,re,shutil,math,subprocess,argparse
root=Path(__file__).resolve().parents[2];work=root/'work/own-framework';pub=root/'remotion/public';src=root/'remotion/src'
parser=argparse.ArgumentParser();parser.add_argument('--audio-stem',default='narration-final-raw');args=parser.parse_args()
assert re.fullmatch(r'[a-zA-Z0-9_-]+',args.audio_stem)
raw=json.loads((root/f'outputs/own-framework/motion/media/audio/{args.audio_stem}.subtitle.json').read_text('utf8'))
audioDefaults=json.loads((root/'work/vox-audio-defaults.json').read_text('utf8'))
speed=float(audioDefaults['playbackRate'])
assert .5<=speed<=2,'Unsupported playbackRate'
audioSource=root/f'outputs/own-framework/motion/media/audio/{args.audio_stem}.mp3'
rawDuration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(audioSource)]))
for sentence in raw['sentences']:
 for word in sentence['words']:
  word['start_time']/=speed
  word['end_time']/=speed
paras=(work/'narration-final.txt').read_text('utf8').strip().split('\n\n')
norm=lambda s:''.join(re.findall(r'[\u4e00-\u9fffA-Za-z0-9]',s))
words=[w for s in raw['sentences'] for w in s['words']]
chars=[]
for w in words:
 for c in norm(w['text']):chars.append(dict(text=c,start=w['start_time'],end=w['end_time']))
spoken=''.join(c['text'] for c in chars);approved=norm(''.join(paras))
assert spoken==approved,'Narration differs from approved script'
offsets=[];pos=0
for p in paras:offsets.append(pos);pos+=len(norm(p))
starts=[0]+[round(chars[i]['start']/1000*30) for i in offsets[1:]]
total=math.ceil((rawDuration/speed+.7)*30)
sizes={m['file']:m['size'] for m in json.loads((pub/'cutouts/manifest.json').read_text('utf8'))}
scenes=[]
def scene(n,title,meaning):
 d={'n':n,'title':title,'meaning':meaning,'start':starts[n-1],'duration':(starts[n] if n<8 else total)-starts[n-1],'layers':[]};scenes.append(d);return d
def cue(text):
 if not text:return 0
 d=scenes[-1];p=norm(paras[d['n']-1]);j=p.find(norm(text));assert j>=0,(d['n'],text)
 return max(0,round(chars[offsets[d['n']-1]+j]['start']/1000*30)-d['start'])
def add(g,i,x,y,w,when='',direction='left',label='',fs=48,labelpos=(.5,.5),z=3,r=0,move=None,exit=None):
 d=scenes[-1];f=f"shot{d['n']:02d}-assets-{g}-obj{i}.png";iw,ih=sizes[f]
 dx,dy={'left':(-1150,0),'right':(1150,0),'up':(0,-1800),'down':(0,1800),'still':(0,0)}[direction]
 l=dict(file=f,x=x,y=y,w=w,h=w*ih/iw,start=cue(when),cue=when or '开镜',dx=dx,dy=dy,angle=r,z=z,label=label,fontSize=fs,labelX=labelpos[0],labelY=labelpos[1],entry=22)
 if move:
  l['move']={'frame':cue(move[0]),'x':move[1],'y':move[2],'w':move[3]}
 if exit:l['exit']={'frame':cue(exit),'dx':1150,'dy':-80}
 d['layers'].append(l)

scene(1,'一个“嗯”\n能想多久？','手机先入；消息被逐条放大；放大镜引导注意力；人物最后承接自我批判。')
add('a',3,70,1210,430,direction='still',z=1)
add('a',1,65,405,430,'领导回了','left',z=3)
add('b',1,575,415,390,'嗯','right','嗯',78,z=4)
add('b',0,565,670,410,'聊天记录','right',z=3)
add('b',4,585,825,390,'十遍','right',z=3)
add('a',2,265,850,370,'事情还没变','right',z=6)
add('b',2,600,1000,390,'在脑子里','right','是我错了？',47,z=5)
add('a',0,545,1210,470,'替自己','down',z=30)
add('b',3,105,1590,290,'批斗会','left',z=2)

scene(2,'模糊的信号\n确定的判决','模糊聊天→问号→三条猜测依次占据中景；清单缩到角落，呈现被忽略的行动。')
add('a',3,100,1210,410,direction='still',z=1,move=('越忘了',65,1370,300))
add('a',1,70,430,650,'模糊的信号','left',z=2)
add('a',2,760,500,225,'你却急着','up',z=5)
add('b',0,70,760,440,'确定的判决','left','他不满意？',52,z=4)
add('b',1,565,805,440,'猜得越多','right','是不是我错了？',42,z=4)
add('b',2,95,1050,450,'越忘了','left','我不够好？',51,z=4)
add('a',0,575,1220,440,'手头真正','right',z=30)
add('b',3,435,1450,270,'要做什么','down',z=2)

scene(3,'事实 · 猜测\n行动','先出现人物与错误猜想；在“三分处理”逐项出现框架及对应道具。人物只整体位移，不虚构手部动作。')
add('a',0,535,730,505,direction='right',z=30)
add('a',4,155,560,345,'我感觉的就是真相','left',z=5,exit='是把事实')
add('a',1,65,420,510,'事实','left','事实\n已发生',57,(.75,.51),z=2)
add('b',0,100,490,240,'事实','down',z=3)
add('a',2,80,850,500,'猜测','left','猜测\n未证实',55,(.75,.5),z=2)
add('b',1,115,920,225,'猜测','down',z=3)
add('a',3,65,1270,520,'行动','left','行动\n下一步',57,(.75,.5),z=2)
add('b',2,105,1320,240,'行动','down',z=3)

scene(4,'回复很短\n不等于不满','两张证据纸并置，逐句标记事实与猜测；在“两张纸”扩大间距；档案与照片保留事实依据的语义。')
add('a',1,130,450,405,'已经发生','left','事实\n回复很短',52,(.52,.64),z=2,move=('两张纸',60,450,410))
add('a',2,515,490,405,'他对我不满','right','猜测\n他不满意',52,(.52,.64),z=2,move=('两张纸',605,490,400))
add('a',3,170,975,250,'他回复很短','left','嗯',64,z=5,move=('两张纸',100,975,250))
add('b',0,680,945,150,'这是猜测','up',z=5,move=('两张纸',755,945,150))
add('b',1,70,1250,320,'把两者写在','left',z=1)
add('b',2,390,1310,250,'你会发现','down',z=2)
add('b',3,320,1410,250,'让你焦虑','left',z=3)
add('a',0,635,1190,415,'往往是第二张','right',z=30)

scene(5,'别猜语气\n问清要求','灰色猜测先到；具体问题替换灰色气泡；橙色提问与方案对应，笔引出修改位置。')
add('a',1,70,430,420,direction='left',z=2)
add('b',0,570,450,420,'反复琢磨','right','他不满意？',50,z=3,exit='不如问清楚')
add('b',2,555,650,455,'不如问清楚','right','哪一处要改？',49,z=4)
add('a',2,95,1160,460,'这份方案','left','这份方案\n具体改哪里？',51,z=3)
add('a',3,320,1395,230,'最需要改','down',z=6)
add('a',0,560,1040,470,'哪一处','right',z=30)
add('b',4,85,1510,170,'具体的要求','left',z=1)

scene(6,'给行动\n定三个标准','交付、质量、协商按旁白形成不同落点；尺子整件横向入场，不假装能伸缩；人物在标准确立后进入。')
add('a',1,445,450,165,direction='still',z=1)
add('a',2,70,445,370,'今天交付什么','left',z=3)
add('b',0,480,580,500,'质量怎样判断','right',z=4)
add('b',1,635,800,330,'质量怎样判断','down','质量\n如何判断',48,(.53,.57),z=3)
add('a',3,90,1150,325,'重新协商','left',z=3)
add('b',2,90,1430,430,'标准越清楚','left','交付 · 质量 · 协商',39,z=5)
add('a',0,530,1200,460,'越不容易','right',z=30)

scene(7,'听取反馈\n也守住边界','有效反馈留在画面内；灰色贬低从右侧进入后退出；橙色边界及人物保持，避免将贬低写成人物定论。')
add('a',2,80,455,390,'事实依据','left','有事实\n就调整',48,(.53,.53),z=3)
add('b',0,75,920,330,'就调整','left',z=2)
add('b',1,400,535,265,'就调整','down',z=2)
add('b',2,750,440,240,'只有情绪','right','情绪',44,z=3,exit='明确边界')
add('b',3,750,750,245,'贬低','right','贬低',44,z=3,exit='你可以听取')
add('b',4,715,1060,245,'就明确','right','指责',44,z=3,exit='但不必')
add('a',1,475,1050,460,'明确边界','down',z=5)
add('a',0,540,960,450,'你可以听取','right',z=30)

scene(8,'把注意力\n拿回行动','手机在“停一下”退出；三问便签逐项出现；成果、待办和笔收束，结束画面停留。')
add('b',1,700,460,230,'翻聊天记录','right',z=2,exit='先停一下')
add('a',1,70,435,510,'事实是什么','left','事实是什么？',52,z=3)
add('a',2,80,855,500,'需要问清','left','还要问清什么？',46,z=3)
add('a',3,70,1270,510,'推进哪一步','left','现在推进哪一步？',43,z=3)
add('a',0,575,1060,425,'把注意力','right',z=30)
add('b',0,690,410,300,'他怎么看我','down',z=2)
add('b',4,695,760,270,'拿回到','right',z=3)
add('b',3,600,1510,155,'我要怎么做','left',z=2)
add('b',2,795,1530,230,'我要怎么做','right',z=4)

# Keep generated paper text exact and editable; word timestamps come from Doubao.
captions=[];batch=[]
def flush():
 if not batch:return
 text=''.join(w['text'] for w in batch).strip().replace('‘','“').replace('’','”')
 if norm(text):captions.append({'text':text,'startMs':batch[0]['start_time'],'endMs':max(w['end_time'] for w in batch)+60,'timestampMs':None,'confidence':None})
 batch.clear()
for w in words:
 batch.append(w)
 if w['text'] in '，。；：？！' or len(norm(''.join(x['text'] for x in batch)))>=17:flush()
flush()
data={'fps':30,'durationInFrames':total,'audioDuration':rawDuration/speed,'playbackRate':speed,'scenes':scenes,'captions':captions,'scriptVerified':True}
(src/'final-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
subprocess.run(['ffmpeg','-v','error','-y','-i',str(audioSource),'-af',f'atempo={speed}','-codec:a','libmp3lame','-q:a','2',str(pub/'narration-final.mp3')],check=True)
for i in range(1,9):shutil.copy2(root/f'outputs/own-framework/shot{i:02d}-background.png',pub/f'shot{i:02d}-background.png')
lines=['# 成片逐字对齐动作表','', f'配音按默认 {speed} 倍保调变速；字幕和动作 cue 同步重算。原始音频 {rawDuration:.2f} 秒；画布 1080×1920 / 30 fps，总时长 {total/30:.2f} 秒。文本比对通过不等于音色听感验收。','背景锁定；人物层 30；字幕层 100。所有物件按生成 Alpha 连通轮廓分离，不使用 2×2 裁块。','']
for s in scenes:
 lines += [f"## 镜 {s['n']} · {s['start']/30:.2f}–{(s['start']+s['duration'])/30:.2f} 秒",s['meaning'],'','| 素材 | 旁白 cue | 本镜入场帧 | 落点 x/y | 宽 | 图层 |','|---|---|---:|---|---:|---:|']
 for l in s['layers']:lines.append(f"|{l['file']}|{l['cue']}|{l['start']}–{l['start']+22}|{l['x']}/{l['y']}|{l['w']}|{l['z']}|")
 lines+=['','接镜：保留奶油纸底与锈橙视觉联系，旁白段首硬切；不移动背景，不让人物在相邻画面之间瞬移表演。','']
(work/'final-action-table.md').write_text('\n'.join(lines),encoding='utf8')
print(json.dumps({'seconds':total/30,'sceneSeconds':[round(s['duration']/30,2) for s in scenes],'layers':sum(len(s['layers']) for s in scenes),'captions':len(captions),'scriptMatch':True},ensure_ascii=False))
