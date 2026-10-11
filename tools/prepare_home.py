from pathlib import Path
import argparse
from prepare import GameData
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('game',type=Path);a=p.parse_args()
root=Path(__file__).resolve().parents[1];gen=root/'generated';gd=GameData(a.game/'data.win')
room=gd.sprite('jillroom_default_spr')
for name,x,y in [('jillblink_spr',142,127),('room_walls_spr',0,21),('shadows_spr',0,0),('room_kotatsu_spr',0,21),('catbreath_spr',97,137),('room_clothes_spr',0,21)]:room.alpha_composite(gd.sprite(name),(x,y))
assets=[('home_room',room),('home_title',gd.sprite('jilltitle_spr').resize((400,225),Image.Resampling.NEAREST)),('home_logo',gd.sprite('intrologo2'))]
for name,source in [('news','augmented_eye_long_base_spr'),('forum','dange_thread1'),('miki','miki_entry')]:
 for i in ([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,60] if name=='news' else range(1,25) if name=='forum' else range(1,7)):
  im=gd.sprite(source,i)
  bounds=im.convert('RGB').getbbox()
  if bounds:im=im.crop((0,0,im.width,min(im.height,max(188,bounds[3]+8))))
  assets.append((f'home_{name}{i}',im))
head=['#pragma once','#include "assets.h"'];body=['#include "home_assets.h"']
for name,im in assets:
 im.save(gen/(name+'.png'));head.append(f'extern const Sprite {name};')
 if name.startswith(('home_news','home_forum','home_miki')):
  # Phone pages are read only by the article viewer. Pack alpha and RGB into
  # two bytes per pixel to keep the executable within the original 3DS memory budget.
  packed=bytearray()
  raw=im.tobytes()
  for offset in range(0,len(raw),4):
   r,g,b,alpha=raw[offset:offset+4]
   value=((alpha>127)<<15)|((r>>3)<<10)|((g>>3)<<5)|(b>>3)
   packed.extend((value&255,value>>8))
  pixels=packed
 else:pixels=im.tobytes()
 body.append('static const uint8_t px_'+name+'[]={'+','.join(map(str,pixels))+'};')
 body.append(f'const Sprite {name}={{{im.width},{im.height},px_{name}}};')
head.append('/* Article pages use packed ARGB1555 pixels; other sprites use RGBA8888. */\nextern const Sprite *const phonePages[3][3];\nextern const Sprite *const day2News[2][3];\nextern const Sprite *const day3News[2][3];\nextern const Sprite *const day4News[2][3];\nextern const Sprite *const newsPages[61];\nextern const Sprite *const forumPages[25];\nextern const Sprite *const mikiPages[7];')
body.append('const Sprite *const day4News[2][3]={{&home_news10,&home_news11,&home_news12},{&home_news58,&home_news11,&home_news12}};')
body.append('const Sprite *const day3News[2][3]={{&home_news7,&home_news8,&home_news9},{&home_news7,&home_news57,&home_news60}};')
body.append('const Sprite *const day2News[2][3]={{&home_news4,&home_news5,&home_news6},{&home_news4,&home_news55,&home_news56}};')
body.append('const Sprite *const phonePages[3][3]={{&home_news1,&home_news2,&home_news3},{&home_forum1,&home_forum2,&home_forum3},{&home_miki1,&home_miki2,&home_miki3}};')
news_ids=[*range(1,59),60]
body.append('const Sprite *const newsPages[61]={'+','.join(f'[{i}]=&home_news{i}' for i in news_ids)+'};')
body.append('const Sprite *const forumPages[25]={0,'+','.join(f'&home_forum{i}' for i in range(1,25))+'};')
body.append('const Sprite *const mikiPages[7]={0,'+','.join(f'&home_miki{i}' for i in range(1,7))+'};')
(gen/'home_assets.h').write_text('\n'.join(head));(gen/'home_assets.c').write_text('\n'.join(body))
print('Extracted room, title, 24 forum threads and six Kira Miki posts')
