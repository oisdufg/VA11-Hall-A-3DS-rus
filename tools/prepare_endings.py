"""Extract the owner's ending stills and credits for local 3DS builds."""
from pathlib import Path
import argparse
from PIL import Image
from prepare import GameData

parser=argparse.ArgumentParser()
parser.add_argument('game',type=Path)
args=parser.parse_args()
project=Path(__file__).resolve().parents[1]
generated=project/'generated'
game=GameData(args.game/'data.win')
names=('curry_spr','concert_spr','anna_doro_spr','hair_spr','vacation_spr','alma_and_jill_spr')
header=['#pragma once','#include "assets.h"','extern const Sprite endingScenes[6];','extern const Sprite endingCredits;']
source=['#include "ending_assets.h"']
scenes=[]
for index,name in enumerate(names):
    image=game.sprite(name).resize((400,225),Image.Resampling.NEAREST)
    image.save(generated/f'ending_{index+1}.png')
    source.append(f'static const uint8_t ending_pixels_{index}[]={{'+','.join(map(str,image.tobytes()))+'};')
    scenes.append(f'{{400,225,ending_pixels_{index}}}')
source.append('const Sprite endingScenes[6]={'+','.join(scenes)+'};')
credits=game.sprite('credits_spr')
credits=credits.resize((400,round(credits.height*400/credits.width)),Image.Resampling.NEAREST)
credits.save(generated/'ending_credits.png')
source.append('static const uint8_t ending_credit_pixels[]={'+','.join(map(str,credits.tobytes()))+'};')
source.append(f'const Sprite endingCredits={{400,{credits.height},ending_credit_pixels}};')
(generated/'ending_assets.h').write_text('\n'.join(header),encoding='utf8')
(generated/'ending_assets.c').write_text('\n'.join(source),encoding='utf8')
print(f'Extracted six endings and {credits.width}x{credits.height} credits')
