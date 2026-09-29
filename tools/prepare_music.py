"""Extract the owner's jukebox catalog as streaming 22.05 kHz mono PCM."""
from pathlib import Path
import argparse,io,json,re
import numpy as np
import soundfile as sf
from prepare import GameData,cstr

def prepare(game,decompiled,project):
    gd=GameData(game/'data.win');dest=project/'sd/3ds/va11-3ds/music';dest.mkdir(parents=True,exist_ok=True)
    source=(decompiled/'gml_Object_jukebox_list_Create_0.gml').read_text()
    ids=[int(n) for args in re.findall(r'ds_list_add\(global.fullplaylist, ([^;]+)\);',source) for n in re.findall(r'\b\d+\b',args)]
    titles=[name for args in re.findall(r'ds_list_add\(global.fullplayliststrings, ([^;]+)\);',source) for name in re.findall(r'"([^"]*)"',args)][1:]
    titles=[t for t in titles if t]
    assert len(ids)==len(titles),(len(ids),len(titles))
    names=[gd.string(gd.u(p)) for p in gd.pointers('SOND')]
    catalog=list(zip(ids,titles));welcome=next(x for x in catalog if names[x[0]]=='welcome_to_valhalla')
    catalog.remove(welcome);catalog.insert(0,welcome)
    def pcm(name):
        data=gd.audio(name)
        # Some owned tracks multiplex Theora video with Vorbis. Keep complete
        # Vorbis pages (including their original checksums), dropping video.
        if data.startswith(b'OggS'):
            pages=[];offset=0;audio_serial=None
            while offset<len(data):
                assert data[offset:offset+4]==b'OggS',name
                count=data[offset+26];header=27+count
                size=header+sum(data[offset+27:offset+header])
                page=data[offset:offset+size];serial=page[14:18]
                if page[header:header+7]==b'\x01vorbis':audio_serial=serial
                pages.append((serial,page));offset+=size
            if audio_serial is not None:data=b''.join(page for serial,page in pages if serial==audio_serial)
        a,rate=sf.read(io.BytesIO(data),dtype='float32',always_2d=True);mono=a.mean(axis=1)
        if rate==44100:mono=mono[:len(mono)//2*2].reshape(-1,2).mean(axis=1)
        elif rate!=22050:raise ValueError((name,rate))
        return np.clip(mono*26000,-32768,32767).astype('<i2').tobytes()
    rows=[]
    for index,(sound,title) in enumerate(catalog):
        data=pcm(names[sound]);(dest/f'{index:03}.pcm').write_bytes(data)
        rows.append({'index':index,'title':title,'source':names[sound],'bytes':len(data)})
    (dest/'boom.pcm').write_bytes(pcm('shot'))
    (dest/'bang.pcm').write_bytes(pcm('plomamentazon'))
    (dest/'crash.pcm').write_bytes(pcm('carcrash'))
    (project/'generated/music.h').write_text('#pragma once\n#define MUSIC_COUNT '+str(len(rows))+'\nstatic const char *const musicTitles[]={'+','.join(cstr(r['title']) for r in rows)+'};\n')
    (project/'generated/music-manifest.json').write_text(json.dumps(rows,indent=2))
    print('Prepared',len(rows),'tracks;',sum(r['bytes'] for r in rows),'PCM bytes')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('game',type=Path);p.add_argument('decompiled',type=Path);a=p.parse_args()
    prepare(a.game,a.decompiled,Path(__file__).resolve().parents[1])
