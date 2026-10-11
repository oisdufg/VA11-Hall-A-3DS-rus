"""Exercise playlist state, menu editing and old-save migration in ARM code."""
from pathlib import Path
import ctypes as C
import json

base=Path(__file__).with_name('verify_day1.py')
exec(base.read_text(encoding='utf8').split('checks=[]')[0])
assert C.sizeof(View)==1344 and View.playlist.offset==1292

class Menu(C.LittleEndianStructure):
    _fields_=[(name,C.c_int32) for name in ('screen','selection','app','article','scroll','hasSave','notice')]

menu_address=0x5110000
def getmenu():return Menu.from_buffer_copy(machine.mem_read(menu_address,C.sizeof(Menu)))
def nav(keys):return call('menu_input',menu_address,address,keys,0,0)

v=View();v.musicTrack=12;put(v);call('engine_start',address,1)
v=get();assert v.musicTrack==12 and v.playlistPos==0 and list(v.playlist)==[12]*12
call('playlist_assign',address,0,1);call('playlist_assign',address,1,2)
assert call('playlist_advance',address)==2 and get().playlistPos==1
for _ in range(11):call('playlist_advance',address)
assert get().playlistPos==0 and get().musicTrack==1

v=get();v.playlist[3]=59;put(v);assert call('engine_valid',address)==0
v.playlist[3]=0;v.playlistPos=12;put(v);assert call('engine_valid',address)==0
v.playlistPos=0;v.musicTrack=0;put(v);assert call('engine_valid',address)==1

u=Menu();u.screen=0;machine.mem_write(menu_address,bytes(u))
call('menu_music',menu_address,address)
assert getmenu().screen==10
nav(128);assert getmenu().scroll==1
call('draw_menu',0x5000000,0x5050000,address,menu_address)
canvas=Image.new('RGB',(416,512),(8,7,12))
for framebuffer,width,y in ((0x5000000,400,8),(0x5050000,320,264)):
    raw=bytes(machine.mem_read(framebuffer,width*240*3))
    panel=Image.frombytes('RGB',(240,width),raw,'raw','BGR').transpose(Image.Transpose.ROTATE_90)
    canvas.paste(panel,((416-width)//2,y))
(P/'previews').mkdir(exist_ok=True)
canvas.save(P/'previews/playlist-editor.png')
nav(2);nav(16);assert getmenu().article==0  # The unbought bonus track is locked.
nav(2);nav(16);assert get().playlist[0]==2 and getmenu().article==1
nav(2);nav(16);assert get().playlist[1]==3 and getmenu().article==2
nav(64);assert getmenu().screen==0 and get().musicTrack==2 and get().playlistPos==0

call('menu_music',menu_address,address)
u=getmenu();u.selection=4;machine.mem_write(menu_address,bytes(u));nav(16)
assert list(get().playlist)==[4]*12 and get().musicTrack==4

old=bytes(get())[:1296]
machine.mem_write(0x5120000,old)
assert call('engine_migrate',address,0x5120000,len(old))==1
assert list(get().playlist)==[4]*12 and get().playlistPos==0

put(View());call('engine_start',address,1)
for _ in range(300):
    if get().mode==7:break
    call('engine_advance_checkpoint',address)
else:raise AssertionError('Scripted Day 1 jukebox was not reached')
u=Menu();u.screen=0;machine.mem_write(menu_address,bytes(u))
call('menu_music',menu_address,address)
nav(128);nav(2);nav(2);nav(16);nav(64)
assert get().mode==0 and get().block==102 and get().musicTrack==2

report={'passed':True,'save_bytes':C.sizeof(View),
        'checks':['12 saved slots and automatic wrap','Invalid tracks and positions rejected',
                  'Menu assigns two slots and starts first track','Single-track choice fills all slots',
                  '0.24.0 save migration preserves the selected track',
                  'Scripted Day 1 jukebox resumes dialogue after playlist selection'],
        'hardware_tested':False,'hardware_pending':'SD audio handoff at end of a track'}
(P/'playlist-test-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
