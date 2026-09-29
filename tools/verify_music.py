"""ARM UI, scripted jukebox and save migration checks; PCM catalog integrity."""
from verify_menu import *
import struct
catalog=json.loads((P/'generated/music-manifest.json').read_text())
count=len(catalog);assert count==59
for track in catalog:
 path=P/'sd/3ds/va11-3ds/music'/f"{track['index']:03}.pcm"
 assert path.stat().st_size==track['bytes'] and track['bytes']>0 and track['bytes']%2==0
put(View());call('engine_start',address,1);call('menu_init',ui,1)
u=getmenu();u.screen=0;machine.mem_write(ui,bytes(u))
# Reach the actual Day 1 music prompt through dialogue, with no manual flag edits.
for _ in range(300):
 if get().mode==7:break
 assert get().mode==0;call('engine_advance_checkpoint',address)
else:raise AssertionError('Day 1 jukebox prompt missing')
before=get();assert before.state.juke==1 and before.block==101
call('menu_music',ui,address);assert getmenu().screen==10
shot('music-day1')
action(1);assert getmenu().selection==count-1
action(2);assert getmenu().selection==0
action(8);assert getmenu().selection==5
action(16);after=get()
assert after.musicTrack==5 and after.mode==0 and after.block==102 and not after.state.juke
assert getmenu().screen==0
# Pause selection preserves dialogue, mixer state and failure counter.
v=get();v.overlay=2;v.cheapErrors=2;put(v);saved=bytes(v)
call('menu_music',ui,address);action(2);action(32)
assert bytes(get())==saved and getmenu().screen==0
call('menu_music',ui,address);action(256,50,110)
v=get();assert v.musicTrack==7 and v.overlay==2 and v.block==after.block and v.cheapErrors==2
# A save made at the mandatory selection can resume the prompt.
v.mode=7;v.state.juke=1;put(v);assert call('engine_valid',address)==1
call('menu_music',ui,address);action(32);assert get().mode==0 and get().block==102
# Authentic 0.6.0 layout: 72 state ints and 11 actors, then error fields/timer.
v=get();v.state.cur_day=3;v.block=401;v.line=0;v.face[1]=3;v.state.almadrunk1=1
legacy=bytes(v)[:80]+bytes(v.state)[:288]+bytes(v.visible)[:44]+bytes(v.position)[:44]+bytes(v.face)[:44]+struct.pack('<iiiQ',v.saveError,v.cheapErrors,v.failed,v.annaUntil)
assert len(legacy)==520
machine.mem_write(0x5120000,legacy);assert call('engine_migrate',address,0x5120000,520)==1
m=get();assert m.block==401 and m.state.almadrunk1==1 and m.face[1]==3 and m.musicTrack==0
assert all(m.visible[i]==0 for i in range(11,15))
# Day 4 apartment news must reflect the relevant Donovan flags.
v=get();v.mode=2;v.state.cur_day=3;v.state.dondrunk1=v.state.dondrunk3=1;put(v);call('engine_next_day',address)
call('menu_init',ui,1);action(16);assert getmenu().screen==2 and get().state.cur_day==4
shot('day4-home');action(16);action(16);action(16);shot('day4-news')
assert call('menu_phone_page',address,ui)==symbols['home_news58']
v=get();v.state.dondrunk3=2;put(v);assert call('menu_phone_page',address,ui)==symbols['home_news10']
report={'passed':True,'tracks':count,'checks':['Day 1 scripted prompt','Track selection, wrap, page jump and touch','Cancel preserves game state','Selection advances the story without autosave','520-byte save migration and unchanged Dana mask index','Day 4 apartment and branching news','PCM file sizes and sample alignment'],'hardware_audio_tested':False}
(P/'music-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
