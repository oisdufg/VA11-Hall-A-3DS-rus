"""Exercise the separate test launcher on ARM, including apartment/shop entry."""
from pathlib import Path
import ctypes as C,json
path=Path(__file__).with_name('verify_day1.py')
exec(path.read_text(encoding='utf8').split('checks=[]')[0].replace('build/va11-3ds.elf','build-test/va11-3ds.elf'))

class Menu(C.LittleEndianStructure):
    _fields_=[(n,C.c_int32) for n in ['screen','selection','app','article','scroll','hasSave','notice']]
ui=0x5110000
def menu():return Menu.from_buffer_copy(machine.mem_read(ui,C.sizeof(Menu)))
def action(keys,x=0,y=0):return call('menu_input',ui,address,keys,x,y)
def shot(name):
    call('draw_menu',0x5000000,0x5050000,address,ui)
    canvas=Image.new('RGB',(416,512),(8,7,12))
    for base,w,y in [(0x5000000,400,8),(0x5050000,320,264)]:
        im=Image.frombytes('RGB',(240,w),bytes(machine.mem_read(base,w*240*3)),'raw','BGR').transpose(Image.Transpose.ROTATE_90)
        canvas.paste(im,((416-w)//2,y))
    (P/'previews').mkdir(exist_ok=True);canvas.save(P/'previews'/f'test-{name}.png')

put(View());call('engine_start',address,1)
for day in range(1,6):
    call('menu_init',ui,0);action(2);assert menu().selection==2
    shot('title');action(16);assert menu().screen==12
    shot('days')
    # Touch selection uses the same four rows as the visible menu.
    assert action(256,80,50+(day-1)*30)==0
    v=get();assert menu().screen==2 and v.mode==5 and v.state.cur_day==day
    assert v.walletCents==2000000 and v.purchases==0 and v.paidDay==day-1
    assert call('engine_can_save',address)==1
    shot(f'day{day}-home');action(16);assert menu().screen==3
    # Every phone app can open an article and return to the apartment.
    for app in range(3):
        u=menu();u.selection=app;machine.mem_write(ui,bytes(u));action(16);action(16)
        assert menu().screen==5;shot(f'day{day}-phone{app}')
        action(2);action(32);action(32);assert menu().screen==3
    action(32);action(1);action(16);assert menu().screen==11
    action(16);assert menu().notice==1 and get().purchases==0
    action(16);assert menu().notice==2 and get().purchases==1 and get().walletCents==1950000
    shot(f'day{day}-shop');action(32);assert menu().screen==2
    action(1);assert menu().selection==2 and action(16)==1
    # Opening day selector then cancelling must preserve the current test progress.
    saved=bytes(get());action(32);action(2);action(2);action(16);action(32)
    assert menu().screen==1 and bytes(get())==saved
    action(16);action(2);action(16)
    assert menu().screen==0 and get().mode==0 and get().state.cur_day==day
    assert get().purchases==1 and get().walletCents==1950000
    assert call('engine_valid',address)==1
    # Starting dialogue reaches a mixer/jukebox without an invalid transition.
    for step in range(500):
        v=get()
        if v.mode in (1,7):break
        call('engine_advance_checkpoint',address);assert get().mode!=4
    else:raise AssertionError(('no playable opening',day))

binary=(P/'build-test/va11-3ds.elf').read_bytes()
for suffix in ('sav','bak','tmp'):
    assert f'sdmc:/3ds/va11-3ds/test-day1.{suffix}\0'.encode() in binary
    assert f'sdmc:/3ds/va11-3ds/day1.{suffix}\0'.encode() not in binary
report={'passed':True,'days':[1,2,3,4,5],'starting_dollars':20000,'checks':['Touch day selection and cancelled selection','Phone apps on every day','Shop purchase and manual save action','Starting shifts retains purchases and balance','Playable opening of each day','All compiled save paths isolated from ordinary saves'],'hardware_tested':False}
(P/'test-launcher-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
