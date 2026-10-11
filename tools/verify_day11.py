"""Exercise Day 11 dialogue, drinks, payroll and save migration on ARM."""
from pathlib import Path
import ctypes as C
import json

base=Path(__file__).with_name('verify_day1.py')
exec(base.read_text(encoding='utf8').split('checks=[]')[0])
assert C.sizeof(View)==1344 and View.walletCents.offset==1256

def recipe(id,size='normal',alcohol=None):
    return next(r for r in recipes if r['id']==id and r['size']==size
                and (alcohol is None or r['alcohol']==alcohol))

def pour(r):
    v=get();v.mixer=Mixer();v.mixer.amount[:]=r['amount']
    v.mixer.ice=r['ice'];v.mixer.aged=r['aged'];v.mixer.blended=r['blended']
    v.mixer.ready=True;put(v);call('engine_serve',address)

def drinks(key,run):
    if key==(1,3):return [recipe(['gpunch','gtemple','fwater'][run%3])]
    if key==(2,2):return [recipe(['beer','beer','fwater'][run%3], 'big' if run%3==1 else 'normal')]
    if key==(2,7):
        options=[('blight','fweaver'),('fweaver','blight'),('blight','gpunch'),
                 ('gpunch','blight'),('fweaver','gpunch'),('gpunch','fweaver'),
                 ('blight','blight'),('gpunch','gpunch')]
        return [recipe(x) for x in options[run%len(options)]]
    if key==(3,2):return [recipe(['btini','srush','beer','fwater'][run%4])]
    if key==(3,5):return [recipe(['btini','beer','scloud','fwater'][run%4])]
    if key==(3,7):return [recipe(['srush','scloud','fdream','bjane','beer'][run%5])]
    if key==(3,9):return [recipe('srush' if run%3==0 else 'bjane' if run%3==2 else 'gpunch')]
    if key==(3,11):return [recipe(['beer','beer','gpunch'][run%3], 'big' if run%3==1 else 'normal')]
    raise AssertionError(key)

seen,orders,actors=set(),set(),set()
completed=breaks=music=0
for run in range(120):
    put(View());call('engine_start',address,1)
    v=get();v.mode=2;v.state.cur_day=10;v.block=1147;v.paidDay=10
    v.walletCents=2000000;v.purchases=(1<<8) if run%2==0 else 0
    v.state.bettydrunk1=run%2
    put(v);call('engine_next_day',address)
    v=get();assert (v.state.cur_day,v.block,v.mode)==(11,1201,5)
    assert call('engine_focused',address)==int(run%2==0)
    v.mode=0;put(v)
    for step in range(2000):
        v=get();seen.add(v.block)
        assert call('engine_valid',address)==1,(run,step,v.mode,v.block,v.state.cur_client,v.state.cur_stage)
        actors.update(i for i in range(25) if v.visible[i])
        if v.mode in (2,6):
            assert v.mode==2,(run,v.block,v.state.cur_client,v.state.cur_stage)
            completed+=1;assert v.paidDay==11 and v.walletCents>=2000000
            before=bytes(v);call('engine_settle',address);assert bytes(get())==before
            break
        if v.mode==7:music+=1;call('engine_finish_jukebox',address);continue
        if v.mode==3:breaks+=1;call('engine_advance_checkpoint',address);continue
        if v.mode==0:call('engine_advance_checkpoint',address);continue
        assert v.mode==1,(run,step,v.mode,v.block)
        orders.add(v.state.orders)
        for r in drinks((v.state.cur_client,v.state.cur_stage),run):pour(r)
    else:raise AssertionError(('Day 11 did not finish',run,get().block,get().state.cur_client,get().state.cur_stage))

assert completed==120 and breaks==120 and music>=240,(completed,breaks,music)
assert set(range(1201,1252))<=seen,sorted(set(range(1201,1252))-seen)
assert {23,24}<=actors,actors

# Version 15 saves retain Day 10 choices, portraits, wallet and purchases.
put(View());call('engine_start',address,1)
v=get();v.state.cur_day=10;v.block=1147;v.mode=2;v.walletCents=876500
v.purchases=1<<8;v.paidDay=10;v.visible[22]=1;v.state.virgilio6=7
raw=bytes(v)
old=raw[:620]+b''.join(raw[getattr(View,n).offset:getattr(View,n).offset+92] for n in ('visible','position','face'))
old+=raw[View.saveError.offset:View.saveError.offset+12]+b'\0'*4
old+=raw[View.annaUntil.offset:View.annaUntil.offset+72]
assert len(old)==984
machine.mem_write(0x5120000,old)
assert call('engine_migrate',address,0x5120000,984)==1
v=get();assert (v.state.cur_day,v.walletCents,v.purchases,v.paidDay,v.state.virgilio6)==(10,876500,1<<8,10,7)
assert v.visible[22]==1 and all(getattr(v.state,n)==0 for n in ('alma7','alma8','db4','db5','jill1','jill2','nacho3'))

report={'passed':True,'runs':completed,'blocks':sorted(seen),'orders':sorted(orders),
        'actors':sorted(actors),'breaks':breaks,'jukeboxes':music,'save_bytes':C.sizeof(View),
        'checks':['Day 10 to Day 11 transition','Holiday focus and music prompts',
                  'Single and double drink branches','All dialogue blocks','Break and payroll',
                  'Version 15 save migration'],'hardware_tested':False}
(P/'day11-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
