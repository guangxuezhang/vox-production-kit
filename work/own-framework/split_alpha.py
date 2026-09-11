from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np,json
root=Path(__file__).resolve().parents[2]
src=root/'outputs/own-framework';dst=root/'remotion/public/cutouts';dst.mkdir(exist_ok=True)
manifest=[]
for file in sorted(src.glob('shot??-assets-?.png')):
 im=Image.open(file).convert('RGBA');a=np.array(im.getchannel('A'));binary=a>40
 parents=[];runs=[];prev=[]
 def find(i):
  while parents[i]!=i:
   parents[i]=parents[parents[i]];i=parents[i]
  return i
 for y,row in enumerate(binary):
  edges=np.flatnonzero(np.diff(np.r_[False,row,False].astype(np.int8)))
  cur=[];j=0
  for x0,x1 in zip(edges[::2],edges[1::2]):
   k=len(parents);parents.append(k);runs.append((y,int(x0),int(x1)));cur.append((int(x0),int(x1),k))
   while j<len(prev) and prev[j][1]<x0:j+=1
   t=j
   while t<len(prev) and prev[t][0]<=x1:
    p=find(prev[t][2]);q=find(k)
    if p!=q:parents[q]=p
    t+=1
  prev=cur
 groups={}
 for k,r in enumerate(runs):groups.setdefault(find(k),[]).append(r)
 parts=[]
 for rr in groups.values():
  area=sum(x1-x0 for y,x0,x1 in rr)
  if area<60:continue
  bb=(min(r[1] for r in rr),min(r[0] for r in rr),max(r[2] for r in rr),max(r[0] for r in rr)+1)
  parts.append({'area':area,'box':bb,'runs':rr})
 main=[p for p in parts if p['area']>im.width*im.height*.006]
 small=[p for p in parts if p not in main]
 # Keep nearby detached paper fibers, marker rays and punctuation with their object.
 for p in small:
  x0,y0,x1,y1=p['box'];scores=[]
  for m in main:
   u0,v0,u1,v1=m['box'];dist=max(u0-x1,x0-u1,0)**2+max(v0-y1,y0-v1,0)**2;scores.append(dist)
  if scores and min(scores)<(im.width*.035)**2:main[scores.index(min(scores))]['runs']+=p['runs']
 main.sort(key=lambda p:(round((p['box'][1]+p['box'][3])/2/im.height*3),p['box'][0]))
 for i,p in enumerate(main):
  mask=Image.new('L',im.size);d=ImageDraw.Draw(mask)
  for y,x0,x1 in p['runs']:d.line((x0,y,x1-1,y),fill=255)
  # Expand only the component selection, then restore original alpha for soft edges.
  mask=mask.filter(ImageFilter.MaxFilter(5));clean=im.copy();clean.putalpha(Image.fromarray(np.minimum(a,np.array(mask))))
  bb=clean.getbbox();clean=clean.crop(bb);name=file.stem+f'-obj{i}.png';clean.save(dst/name)
  manifest.append({'file':name,'source':file.name,'box':bb,'size':clean.size,'mainArea':p['area']})
 print(file.name,len(main),flush=True)
(dst/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
board=Image.new('RGB',(1600,((len(manifest)+7)//8)*240),'#b7b1a6');d=ImageDraw.Draw(board)
for i,r in enumerate(manifest):
 tile=Image.open(dst/r['file']);tile.thumbnail((188,205));x=i%8*200;y=i//8*240
 board.paste(tile,(x+(200-tile.width)//2,y+30),tile);d.text((x+5,y+5),r['file'].replace('shot','').replace('-assets',''),fill='black')
board.save(src/'alpha-cutouts-review.jpg');print('TOTAL',len(manifest))
