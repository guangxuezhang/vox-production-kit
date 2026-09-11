from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess,sys
root=Path(__file__).resolve().parents[2];out=root/'outputs/own-framework'
video=out/(sys.argv[1] if len(sys.argv)>1 else 'own-framework-finished-v1.mp4');data=json.loads((root/'remotion/src/final-data.json').read_text('utf8'))
folder=out/(video.stem+'-qa');folder.mkdir(exist_ok=True)
for kind in ['mid','end']:
 board=Image.new('RGB',(1280,1196),'#ded7c9');draw=ImageDraw.Draw(board)
 for i,s in enumerate(data['scenes']):
  frame=s['start']+(s['duration']//2 if kind=='mid' else s['duration']-12)
  path=folder/f'{kind}-{i+1:02d}.png'
  subprocess.run(['ffmpeg','-v','error','-y','-ss',str(frame/30),'-i',str(video),'-frames:v','1',str(path)],check=True)
  im=Image.open(path);im.thumbnail((320,568));x=i%4*320;y=i//4*598;board.paste(im,(x,y+30));draw.text((x+8,y+8),f'Scene {i+1} / frame {frame}',fill='black')
 board.save(folder/f'{kind}-contact.jpg')
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_name,width,height,r_frame_rate,sample_rate,channels','-of','json',str(video)]))
(folder/'technical-qa.json').write_text(json.dumps(meta,indent=2),encoding='utf8');print(json.dumps(meta))
