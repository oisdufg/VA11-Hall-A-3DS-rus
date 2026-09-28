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
 for i in ([1,2,3,4,5,6,55,56] if name=='news' else range(1,4)):
  im=gd.sprite(source,i)
  bounds=im.convert('RGB').getbbox()
  if bounds:im=im.crop((0,0,im.width,min(im.height,max(188,bounds[3]+8))))
  assets.append((f'home_{name}{i}',im))
head=['#pragma once','#include "assets.h"'];body=['#include "home_assets.h"']
for name,im in assets:
 im.save(gen/(name+'.png'));head.append(f'extern const Sprite {name};')
 body.append('static const uint8_t px_'+name+'[]={'+','.join(map(str,im.tobytes()))+'};')
 body.append(f'const Sprite {name}={{{im.width},{im.height},px_{name}}};')
head.append('extern const Sprite *const phonePages[3][3];\nextern const Sprite *const day2News[2][3];')
body.append('const Sprite *const day2News[2][3]={{&home_news4,&home_news5,&home_news6},{&home_news4,&home_news55,&home_news56}};')
body.append('const Sprite *const phonePages[3][3]={{&home_news1,&home_news2,&home_news3},{&home_forum1,&home_forum2,&home_forum3},{&home_miki1,&home_miki2,&home_miki3}};')
(gen/'home_assets.h').write_text('\n'.join(head));(gen/'home_assets.c').write_text('\n'.join(body))
print('Extracted room, title, and nine original Russian phone pages')
