"""Prepare static Day 6 apartment scenes from the owner's original game data."""
from pathlib import Path
import argparse
from PIL import Image
from prepare import GameData


def prepare(game,project):
    gd=GameData(game/'data.win')
    sprites=gd.pointers('SPRT')
    output=project/'generated'
    header=['#pragma once','#include "assets.h"']
    source=['#include "day6_assets.h"']
    for key,jill in [('day6_scene',603),('day6_scene_drunk',611)]:
        scene=Image.new('RGBA',(320,183))
        for index in (602,jill,604):
            pointer=sprites[index]
            scene.alpha_composite(gd.sprite(gd.string(gd.u(pointer))))
        scene.save(output/(key+'.png'))
        header.append(f'extern const Sprite {key};')
        source.append('static const uint8_t px_'+key+'[]={'+','.join(map(str,scene.tobytes()))+'};')
        source.append(f'const Sprite {key}={{320,183,px_{key}}};')
    (output/'day6_assets.h').write_text('\n'.join(header)+'\n')
    (output/'day6_assets.c').write_text('\n'.join(source)+'\n')
    print('Prepared two static Day 6 apartment scenes.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('game',type=Path)
    args=parser.parse_args()
    prepare(args.game,Path(__file__).resolve().parents[1])
