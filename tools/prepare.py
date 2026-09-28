"""Convert the owner's GameMaker resources into assets for the tutorial prototype."""
from pathlib import Path
import argparse, struct, io, json, re, textwrap, hashlib, sys
from PIL import Image, ImageDraw, ImageFont

class GameData:
    def __init__(self,path):
        self.data=Path(path).read_bytes(); self.chunks={};p=8
        if self.data[:4]!=b'FORM':raise ValueError('Expected GameMaker FORM container')
        while p<len(self.data):
            size=self.u(p+4);self.chunks[self.data[p:p+4].decode()]=(p+8,size);p+=8+size
        self.textures={}
    def u(self,p):return struct.unpack_from('<I',self.data,p)[0]
    def string(self,p):return self.data[p:self.data.index(b'\0',p)].decode('utf8')
    def pointers(self,name):
        p=self.chunks[name][0];return [self.u(p+4+i*4) for i in range(self.u(p))]
    def sprite(self,name,frame=0):
        p=next(p for p in self.pointers('SPRT') if self.string(self.u(p))==name)
        w,h=self.u(p+4),self.u(p+8); count=self.u(p+56)
        if not 0<=frame<count:raise ValueError((name,frame,count))
        t=self.u(p+60+frame*4)
        sx,sy,sw,sh,tx,ty,tw,th,bw,bh,idx=struct.unpack_from('<10Hh',self.data,t)
        if idx not in self.textures:
            start=self.u(self.pointers('TXTR')[idx]+4);end=self.data.index(b'IEND',start)+8
            self.textures[idx]=Image.open(io.BytesIO(self.data[start:end])).convert('RGBA')
        crop=self.textures[idx].crop((sx,sy,sx+sw,sy+sh))
        if crop.size!=(tw,th):crop=crop.resize((tw,th),Image.Resampling.NEAREST)
        result=Image.new('RGBA',(w,h));result.paste(crop,(tx,ty));return result
    def audio(self,name):
        p=next(p for p in self.pointers('SOND') if self.string(self.u(p))==name)
        if self.u(p+28)!=0:raise ValueError('External audio group')
        a=self.pointers('AUDO')[self.u(p+32)];return self.data[a+4:a+4+self.u(a)]

def parse_tutorial(path):
    blocks={}; block=0; face=0; faces={'':0,'cods':1,'surprise':2,'fucked':3}
    for raw in Path(path).read_text(encoding='utf-8-sig').splitlines():
        for value in re.findall(r'\[XS:gilface,([^\]]*)\]',raw):face=faces[value]
        text=re.sub(r'\[[^\]]*\]','',raw).replace('#',' ')
        text=' '.join(text.split())
        if text:
            name,sep,body=text.partition(':')
            if not sep:name,body='',text
            wrapped=textwrap.wrap(body.strip(),width=46,break_long_words=True,break_on_hyphens=False)
            for i in range(0,len(wrapped),4):
                blocks.setdefault(block,[]).append(dict(name=name,text='\n'.join(wrapped[i:i+4]),face=face))
        for event in re.findall(r'\[E:(\d+)\]',raw):block=int(event)
    if set(blocks)!=set(range(1,11)):raise ValueError('Unexpected tutorial blocks')
    return blocks

def cstr(s):return json.dumps(s,ensure_ascii=False)
def prepare(game,out,fontpath):
    out=Path(out);gen=out/'generated';gen.mkdir(parents=True,exist_ok=True)
    sd=out/'sd/3ds/va11-3ds';sd.mkdir(parents=True,exist_ok=True)
    gd=GameData(Path(game)/'data.win')
    assets=[]
    bg=gd.sprite('barground').crop((0,0,338,250)).resize((264,195),Image.Resampling.NEAREST)
    assets.append(('background',bg))
    for name,layers in [
        ('gil0',['gil_spr','gil_eyes','gil_lips']),
        ('gil1',['gil_cods','gil_cods_eyes','gil_cods_lips']),
        ('gil2',['gil_surprised','gil_surprised_eyes','gil_surprised_lips']),
        # This emotion is a face overlay, not a complete character sprite.
        ('gil3',['gil_spr','gil_fucked_up']),
        ('jill',['jill_spr','jill_eyes','jill_lips'])]:
        im=gd.sprite(layers[0])
        for layer in layers[1:]:im.alpha_composite(gd.sprite(layer))
        im=im.resize((round(im.width*.5),round(im.height*.5)),Image.Resampling.NEAREST)
        assets.append((name,im))
    declarations=['#pragma once','#include <stdint.h>','typedef struct { int w,h; const uint8_t *rgba; } Sprite;']
    definitions=['#include "assets.h"']
    for name,im in assets:
        im.save(gen/(name+'.png'));raw=im.tobytes()
        definitions.append('static const uint8_t pixels_'+name+'[]={'+','.join(map(str,raw))+'};')
        definitions.append(f'const Sprite {name}={{{im.width},{im.height},pixels_{name}}};')
        declarations.append(f'extern const Sprite {name};')
    (gen/'assets.h').write_text('\n'.join(declarations));(gen/'assets.c').write_text('\n'.join(definitions))
    blocks=parse_tutorial(Path(game)/'scripts/eng/tutorial.txt')
    story=['#pragma once','typedef struct {const char *name,*text; int face;} Line;']
    starts=[0]*11;counts=[0]*11;lines=[]
    for b,entries in blocks.items():
        starts[b]=len(lines);counts[b]=len(entries)
        for line in entries:lines.append('{'+cstr(line['name'])+','+cstr(line['text'])+','+str(line['face'])+'}')
    story+=['static const Line story[]={'+',\n'.join(lines)+'};','static const int blockStart[]={'+','.join(map(str,starts))+'};','static const int blockCount[]={'+','.join(map(str,counts))+'};']
    (gen/'story.h').write_text('\n'.join(story),encoding='utf8');(gen/'story.json').write_text(json.dumps(blocks,ensure_ascii=False,indent=2),encoding='utf8')
    codes=list(range(32,127))+list(range(0x400,0x460))+[0xab,0xbb,0x2013,0x2014,0x2018,0x2019,0x201c,0x201d,0x2026]
    font=ImageFont.truetype(str(fontpath),12);glyphs=[]
    for cp in codes:
        im=Image.new('L',(8,15));ImageDraw.Draw(im).text((0,-2),chr(cp),font=font,fill=255)
        glyphs.append([sum((1<<(7-x)) for x in range(8) if im.getpixel((x,y))>=95) for y in range(15)])
    (gen/'font.h').write_text('#pragma once\n#include <stdint.h>\nstatic const uint32_t fontCodes[]={'+','.join(map(str,codes))+'};\nstatic const uint8_t fontBits[][15]={'+','.join('{'+','.join(map(str,g))+'}' for g in glyphs)+'};\n')
    import soundfile as sf
    import numpy as np
    audio,rate=sf.read(io.BytesIO(gd.audio('welcome_to_valhalla')),dtype='float32',always_2d=True)
    mono=audio.mean(axis=1)
    # This source is 44.1 kHz: average adjacent samples for a small 22.05 kHz stream.
    if rate==44100:mono=mono[:len(mono)//2*2].reshape(-1,2).mean(axis=1)
    elif rate!=22050:raise ValueError(f'Unsupported sample rate {rate}')
    pcm=np.clip(mono*26000,-32768,32767).astype('<i2').tobytes();(sd/'music.pcm').write_bytes(pcm)
    manifest={'source_sha256':hashlib.sha256(gd.data).hexdigest(),'tutorial_sha256':hashlib.sha256((Path(game)/'scripts/eng/tutorial.txt').read_bytes()).hexdigest(),'story_pages':len(lines),'sprite_bytes':sum(len(im.tobytes()) for _,im in assets),'music_bytes':len(pcm),'music_rate':22050,'music_channels':1,'music_track':'welcome_to_valhalla','scope':'Tutorial prototype; manually reconstructed tutorial branching, not the full GameMaker runtime.'}
    (out/'asset-manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('game');p.add_argument('--out',default=str(Path(__file__).resolve().parents[1]));p.add_argument('--font',required=True);a=p.parse_args();prepare(a.game,a.out,a.font)
