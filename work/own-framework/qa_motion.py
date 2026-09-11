from pathlib import Path
import subprocess,json
import numpy as np
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[2];out=root/'outputs/own-framework';data=json.loads((root/'remotion/src/final-data.json').read_text('utf8'))
video=out/'own-framework-finished-v2.mp4';dst=out/'own-framework-finished-v2-qa';dst.mkdir(exist_ok=True)
def frame(k,name):
 path=dst/f'{name}.png';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(k/30),'-i',str(video),'-frames:v','1',str(path)],check=True);return Image.open(path).convert('RGB')
rows=[];stats=[]
for i,s in enumerate(data['scenes']):
 person=next(l for l in s['layers'] if l['z']==30)
 start=s['start']+person['start'];ks=[max(s['start'],start-1),start+8,start+24]
 ims=[frame(k,f'motion-{i+1}-{j}') for j,k in enumerate(ks)]
 delta=np.abs(np.array(ims[0],dtype='int16')-np.array(ims[2],dtype='int16')).mean(axis=2)
 changed=float((delta>12).mean())
 patch1=np.array(ims[0].crop((1020,20,1060,60)),dtype='float32');patch2=np.array(ims[2].crop((1020,20,1060,60)),dtype='float32')
 stats.append({'scene':i+1,'frames':ks,'changedPixelFraction':round(changed,4),'staticBackgroundCornerMeanDifference':round(float(abs(patch1-patch2).mean()),3)})
 row=Image.new('RGB',(810,500),'#ddd5c9');d=ImageDraw.Draw(row)
 for j,im in enumerate(ims):im.thumbnail((270,480));row.paste(im,(j*270,20));d.text((j*270+5,3),f'Scene {i+1} / frame {ks[j]}',fill='black')
 rows.append(row)
board=Image.new('RGB',(1620,2000))
for i,row in enumerate(rows):board.paste(row,(i%2*810,i//2*500))
board.save(dst/'motion-contact.jpg');(dst/'motion-qa.json').write_text(json.dumps(stats,indent=2),encoding='utf8');print(json.dumps(stats))
