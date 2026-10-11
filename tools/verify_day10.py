"""Exercise Day 10 routes on the compiled ARM engine."""
from pathlib import Path
import ctypes as C
import json
import random

base=Path(__file__).with_name('verify_day1.py')
exec(base.read_text(encoding='utf8').split('checks=[]')[0])

assert C.sizeof(View)==1344 and View.walletCents.offset==1256
seen,orders,actors=set(),set(),set()
completed=breaks=music=0
rng=random.Random(1010)

def recipe(id,size='normal',alcohol=None):
    return next(r for r in recipes if r['id']==id and r['size']==size
                and (alcohol is None or r['alcohol']==alcohol))

def pour(r):
    v=get();v.mixer=Mixer();v.mixer.amount[:]=r['amount']
    v.mixer.ice=r['ice'];v.mixer.aged=r['aged'];v.mixer.blended=r['blended']
    v.mixer.ready=True;put(v);call('engine_serve',address)

def drinks(key,run):
    if key==(1,3):return [recipe('gpunch' if run%7==1 else 'sstar')]
    if key==(1,5):return [recipe('gpunch' if run%7==2 else 'btouch')]
    if key==(1,7):return [recipe('gpunch' if run%7==3 else 'beer')]
    if key==(1,9):return [recipe('gpunch') if run%5==1 else
                           recipe('scloud',alcohol='no') if run%5==2 else recipe('btouch')]
    if key==(2,2):return [recipe('gpunch') if run%6==1 else
                           recipe('btini') if run%6==2 else recipe('btini','big')]
    if key==(2,4):return [recipe('blight'),recipe('gpunch' if run%6==1 else 'blight')] if run%6!=2 else [recipe('gpunch'),recipe('gpunch')]
    if key==(2,8):return [recipe('beer'),recipe('gpunch' if run%6==3 else 'beer')] if run%6!=4 else [recipe('gpunch'),recipe('gpunch')]
    if key==(3,2):return [recipe('gpunch' if run%7==4 else 'scloud')]
    if key==(3,6):return [recipe('gpunch','normal') if run%5==1 else
                           recipe('gpunch','big') if run%5==2 else recipe('beer','big')]
    if key==(3,8):return [recipe('gpunch')]
    raise AssertionError(key)

for run in range(200):
    put(View());call('engine_start',address,1)
    v=get();v.mode=2;v.state.cur_day=9;v.block=1047;v.paidDay=9
    v.walletCents=2000000;v.purchases=(1<<3) if run%2==0 else 0
    v.state.kimdrunk1=run%2
    put(v);call('engine_next_day',address)
    v=get();assert (v.state.cur_day,v.block,v.mode)==(10,1101,5)
    assert call('engine_focused',address)==int(run%2==0)
    v.mode=0;put(v)
    for step in range(2200):
        v=get();seen.add(v.block)
        assert call('engine_valid',address)==1,(run,step,v.mode,v.block,v.state.cur_client,v.state.cur_stage)
        actors.update(i for i in (0,1,2,5,6,10,16) if v.visible[i])
        if v.mode in (2,6):
            assert v.mode==2,(run,v.block,v.state.cur_client,v.state.cur_stage)
            completed+=1;assert v.paidDay==10 and v.walletCents>=2000000
            before=bytes(v);call('engine_settle',address);assert bytes(get())==before
            break
        if v.mode==7:music+=1;call('engine_finish_jukebox',address);continue
        if v.mode==3:breaks+=1;call('engine_advance_checkpoint',address);continue
        if v.mode==0:call('engine_advance_checkpoint',address);continue
        assert v.mode==1,(run,step,v.mode,v.block)
        orders.add(v.state.orders)
        key=(v.state.cur_client,v.state.cur_stage)
        for r in drinks(key,run):pour(r)
    else:raise AssertionError(('Day 10 did not finish',run,get().block,get().state.cur_client,get().state.cur_stage))

assert completed==200 and breaks==200 and music>=400,(completed,breaks,music)
assert set(range(1101,1148))<=seen,sorted(set(range(1101,1148))-seen)
assert {85,86,87,88,89,90,92,93,94,95}<=orders,sorted(orders)

# Version 14 saves retain Day 9 choices, portraits, wallet and purchases.
put(View());call('engine_start',address,1)
v=get();v.state.cur_day=9;v.block=1047;v.mode=2;v.walletCents=876500
v.purchases=1<<13;v.paidDay=9;v.visible[22]=1;v.state.mario2=7
raw=bytes(v)
old=raw[:584]+b''.join(raw[getattr(View,n).offset:getattr(View,n).offset+92] for n in ('visible','position','face'))
old+=raw[View.saveError.offset:View.saveError.offset+12]
old+=raw[View.annaUntil.offset:View.annaUntil.offset+72]
assert len(old)==944
machine.mem_write(0x5120000,old)
assert call('engine_migrate',address,0x5120000,944)==1
v=get();assert (v.state.cur_day,v.walletCents,v.purchases,v.paidDay,v.state.mario2)==(9,876500,1<<13,9,7)
assert v.visible[22]==1 and all(getattr(v.state,n)==0 for n in ('virgilio4','virgilio5','virgilio6','sei7','stel6','stel7','stel8','kim4','kim5'))

# A third cheap wrong paid drink triggers Game Over and disables saving.
put(View());call('engine_start',address,1)
v=get();v.state.cur_day=10;v.state.cur_client=1;v.state.cur_stage=3
v.mode=1;v.cheapErrors=2;put(v);pour(recipe('fwater'))
v=get();assert (v.failed,v.block,v.mode)==(1,301,0),(v.failed,v.block,v.mode,v.cheapErrors)
assert call('engine_can_save',address)==0

report={'passed':True,'runs':completed,'blocks':sorted(seen),'orders':sorted(orders),
        'actors':sorted(actors),'breaks':breaks,'jukeboxes':music,'save_bytes':C.sizeof(View),
        'checks':['Day 9 to Day 10 transition','Poster focus and distracted order hints',
                  'Single and double drink branches','All dialogue blocks','Break and two music prompts',
                  'Once-only payroll','Version 14 save migration','Game Over'],
        'hardware_tested':False}
(P/'day10-test-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
