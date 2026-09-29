from verify_day1 import *
class Menu(C.LittleEndianStructure):
 _fields_=[(n,C.c_int32) for n in ['screen','selection','app','article','scroll','hasSave','notice']]
ui=0x5110000
def getmenu():return Menu.from_buffer_copy(machine.mem_read(ui,C.sizeof(Menu)))
def action(keys,x=0,y=0):return call('menu_input',ui,address,keys,x,y)
def shot(name):
 call('draw_menu',0x5000000,0x5050000,address,ui)
 canvas=Image.new('RGB',(416,512),(8,7,12))
 for base,w,y in [(0x5000000,400,8),(0x5050000,320,264)]:
  im=Image.frombytes('RGB',(240,w),bytes(machine.mem_read(base,w*240*3)),'raw','BGR').transpose(Image.Transpose.ROTATE_90);canvas.paste(im,((416-w)//2,y))
 canvas.save(P/'previews'/f'menu-{name}.png')
put(View());call('engine_start',address,1);call('menu_init',ui,0)
assert getmenu().selection==1 and getmenu().screen==1
shot('title');action(16);assert getmenu().screen==6
action(2);assert action(16)==0 and get().mode==5
assert call('engine_valid',address)==1
shot('home');action(16);assert getmenu().screen==3
shot('phone');action(16);assert getmenu().screen==4
shot('news');action(16);assert getmenu().screen==5
shot('article')
for i in range(100):action(2)
limit=getmenu().scroll
assert 0<limit<=812
action(2);assert getmenu().scroll==limit
for i in range(100):action(1)
assert getmenu().scroll==0
action(32);action(32);action(32);assert getmenu().screen==2
action(2);assert action(16)==0 and getmenu().screen==0 and get().mode==0 and get().state.cur_client==1
saved=bytes(get());call('menu_init',ui,1);action(16)
assert getmenu().screen==0 and bytes(get())==saved
call('menu_init',ui,1);action(2);action(16);action(32)
assert bytes(get())==saved
# Touch opens the second title row, then tutorial and apartment.
assert action(256,50,90)==0 and getmenu().screen==6
action(16);assert get().round==1 and get().mode==5
action(2);action(16);assert get().state.cur_client==0

v=get();v.mode=2;v.state.cur_day=1;v.state.dondrunk1=1;put(v);call('engine_next_day',address)
call('menu_init',ui,1);action(16);assert getmenu().screen==2
shot('day2-home');action(16);action(16);action(16);shot('day2-news')
action(32);action(32);action(32);action(2)
assert action(16)==0 and get().state.cur_day==2 and get().mode==0
v=get();v.mode=2;v.state.dondrunk2=1;put(v);call('engine_next_day',address)
call('menu_init',ui,1);action(16);assert getmenu().screen==2 and get().state.cur_day==3
shot('day3-home');action(16);action(16);action(16);shot('day3-news')
assert call('menu_phone_page',address,ui)==symbols['home_news7']
action(32);action(2);action(16);assert call('menu_phone_page',address,ui)==symbols['home_news57']
action(32);action(2);action(16);assert call('menu_phone_page',address,ui)==symbols['home_news60']
v=get();v.state.dondrunk2=0;put(v);assert call('menu_phone_page',address,ui)==symbols['home_news9']
action(32);action(32);action(32);action(2)
assert action(16)==0 and get().state.cur_day==3 and get().mode==0 and get().block==401
report={'passed':True,'checks':['New game via apartment, with and without tutorial','Continue preserves current dialogue byte-for-byte','Cancel new game preserves progress','No automatic save at new game or start of work','Phone apps, article selection, scroll limits, back navigation','Touch title navigation','ARM-rendered title, apartment, phone, news and article previews'],'hardware_tested':False}
(P/'menu-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

# Startup-only credits preserve the existing save and title selection.
saved=bytes(get());call('menu_init',ui,1);u=getmenu();u.screen=8;machine.mem_write(ui,bytes(u));shot('credits')
assert action(1)==0 and getmenu().screen==8
assert action(16)==0 and getmenu().screen==9 and bytes(get())==saved
shot("translation");assert action(32)==0 and getmenu().screen==9
assert action(16)==0 and getmenu().screen==1 and getmenu().selection==0 and bytes(get())==saved
u=getmenu();u.screen=8;machine.mem_write(ui,bytes(u));assert action(256,160,210)==0 and getmenu().screen==9
assert action(256,160,210)==0 and getmenu().screen==1 and bytes(get())==saved
report['checks'].append('Startup credits and translation: A/touch opens both screens before title without changing save')
(P/'menu-test-report.json').write_text(json.dumps(report,indent=2))
