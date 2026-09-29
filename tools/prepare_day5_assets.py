"""Stage Day 5 static portraits, sound cues and special-drink metadata locally."""
from pathlib import Path
import argparse,io,json,re,struct
import numpy as np
import soundfile as sf
from PIL import Image
from prepare import GameData

def prepare(game,scripts,project):
    folder=project/'generated/day5';folder.mkdir(exist_ok=True)
    gd=GameData(game/'data.win');pointers=gd.pointers('SPRT')
    # Original Draw events: body first, mouth frame zero, open-eye frame zero.
    layers={'taylor-normal':[399], 'virgilio-normal':[389,391,390],
            'virgilio-smug':[392,393], 'virgilio-serious':[394,395,396],
            'virgilio-dissapoint':[397,398], 'doro-wah':[249,250,251]}
    preview=Image.new('RGBA',(6*180,280),(27,17,38,255));manifest={}
    for column,(key,ids) in enumerate(layers.items()):
        def read(index):
            p=pointers[index];return gd.sprite(gd.string(gd.u(p))),struct.unpack_from('<ii',gd.data,p+48)
        im,(ox,oy)=read(ids[0])
        for index in ids[1:]:
            overlay,(x,y)=read(index);im.alpha_composite(overlay,(ox-x,oy-y))
        im=im.resize((round(im.width/2),round(im.height/2)),Image.Resampling.NEAREST)
        assert im.getbbox() and im.height<=270
        im.save(folder/(key+'.png'))
        manifest[key]={'layers':ids,'width':im.width,'height':im.height,'origin':[ox/2,oy/2]}
        preview.alpha_composite(im,(column*180+(180-im.width)//2,270-im.height))
    preview.convert('RGB').save(folder/'actors-preview.png')
    sounds={}
    for filename,name in [('bang','plomamentazon'),('crash','carcrash')]:
        a,rate=sf.read(io.BytesIO(gd.audio(name)),dtype='float32',always_2d=True);mono=a.mean(axis=1)
        if rate==44100:mono=mono[:len(mono)//2*2].reshape(-1,2).mean(axis=1)
        elif rate!=22050:raise ValueError((name,rate))
        data=np.clip(mono*26000,-32768,32767).astype('<i2').tobytes()
        assert len(data)>0 and len(data)%2==0
        (folder/(filename+'.pcm')).write_bytes(data);sounds[filename]={'source':name,'bytes':len(data),'rate':22050}
    src=(scripts/'gml_Script_drink_a.gml').read_text();drinks=[]
    for name in ('rum','abs','fed'):
        body=re.search(r'if \(global.exdrink_a == "'+name+r'"\)\s*\{(.*?)exit;',src,re.S)[1]
        fields=dict(re.findall(r'global\.(\w+)_a = "([^"\n]*)";',body))
        fields['price']=int(re.search(r'global.drinkscore_a = (\d+);',body)[1])
        fields['availability']='always' if name=='fed' else 'day >= 5 and '+('both Stella orders right' if name=='rum' else 'not both Stella orders right')
        drinks.append(fields)
    (folder/'assets-manifest.json').write_text(json.dumps({'portraits':manifest,'sounds':sounds,'special_drinks':drinks},indent=2),encoding='utf8')
    print('Staged six portraits, two PCM effects, and three original special drinks.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('game',type=Path);p.add_argument('scripts',type=Path);a=p.parse_args()
    prepare(a.game,a.scripts,Path(__file__).resolve().parents[1])
