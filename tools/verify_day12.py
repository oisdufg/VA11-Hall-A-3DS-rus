"""Exercise Day 12 routes and save migration in the compiled ARM engine."""
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
    if key==(1,3):return [recipe('cvelvet','big') if run%9==0 else recipe('btini' if run%4 else 'fwater')]
    if key==(1,5):return [recipe('cvelvet','big') if run%9==0 else recipe('fdream' if run%4 else 'fwater')]
    if key==(2,2):return [recipe('pwman','big') if run%4==0 else recipe('srush',alcohol='yes' if run%4==1 else 'no') if run%4 in (1,2) else recipe('beer')]
    if key==(2,4):return [recipe(['bfairy','beer','fwater'][run%3])]
    if key==(2,7):return [recipe('pwman','big') if (run//4)%4==0 else recipe(['srush','fdream','gpunch'][(run//4)%4-1])]
    if key==(4,2):return [recipe(['scloud','cvelvet','moblast','srush'][run%4])]
    if key==(4,4):return [recipe('fwater' if run%2 else 'beer')]
    if key==(5,2):return [recipe('gpunch' if run%2 else 'beer')]
    if key==(5,4):return [recipe('cvelvet' if run%2 else 'beer')]
    raise AssertionError(key)

seen,orders,actors=set(),set(),set()
completed=breaks=music=0
for run in range(120):
    put(View());call('engine_start',address,1)
    v=get();v.mode=2;v.state.cur_day=11;v.block=1251;v.paidDay=11
    v.walletCents=2000000 if run%2==0 else 500000
    if run%3==0:v.state.dorodrink1=json.loads((P/'generated/v8-metadata.json').read_text())['tokens']['pwman']
    put(v);call('engine_next_day',address)
    v=get();assert (v.state.cur_day,v.block,v.mode)==(12,1301,5)
    assert (v.state.lightdl,v.walletCents)==((1,1200000) if run%2==0 else (2,500000))
    assert call('engine_focused',address)==int(run%2==0)
    v.mode=0;put(v)
    for step in range(2400):
        v=get();seen.add(v.block)
        assert call('engine_valid',address)==1,(run,step,v.mode,v.block,v.state.cur_client,v.state.cur_stage)
        actors.update(i for i in range(27) if v.visible[i])
        if v.mode in (2,6):
            assert v.mode==2,(run,v.block,v.state.cur_client,v.state.cur_stage)
            completed+=1;assert v.paidDay==12
            before=bytes(v);call('engine_settle',address);assert bytes(get())==before
            break
        if v.mode==7:music+=1;call('engine_finish_jukebox',address);continue
        if v.mode==3:breaks+=1;call('engine_advance_checkpoint',address);continue
        if v.mode==0:call('engine_advance_checkpoint',address);continue
        assert v.mode==1,(run,step,v.mode,v.block)
        orders.add(v.state.orders)
        for r in drinks((v.state.cur_client,v.state.cur_stage),run):pour(r)
    else:raise AssertionError(('Day 12 did not finish',run,get().block,get().state.cur_client,get().state.cur_stage))

print('Day 12 route summary',completed,breaks,music,'missing',sorted(set(range(1301,1350))-seen),'seen2',sorted(x for x in seen if 1323<=x<=1335),flush=True)
assert completed==120 and breaks==120 and music>=120,(completed,breaks,music)
assert set(range(1301,1350))<=seen,sorted(set(range(1301,1350))-seen)

# Version 16 saves retain Day 11 choices and portraits.
put(View());call('engine_start',address,1)
v=get();v.state.cur_day=11;v.block=1251;v.mode=2;v.walletCents=876500
v.purchases=1<<8;v.paidDay=11;v.visible[24]=1;v.state.nacho3=7
raw=bytes(v)
old=raw[:648]+b''.join(raw[getattr(View,n).offset:getattr(View,n).offset+100] for n in ('visible','position','face'))
old+=raw[View.saveError.offset:View.saveError.offset+12]+raw[View.annaUntil.offset:View.annaUntil.offset+72]
assert len(old)==1032
machine.mem_write(0x5120000,old)
assert call('engine_migrate',address,0x5120000,1032)==1
v=get();assert (v.state.cur_day,v.walletCents,v.purchases,v.paidDay,v.state.nacho3)==(11,876500,1<<8,11,7)
assert v.visible[24]==1 and all(getattr(v.state,n)==0 for n in ('dorodrink7','dorodrink9','sei8','sei9','lightdl'))

report={'passed':True,'runs':completed,'blocks':sorted(seen),'orders':sorted(orders),
        'actors':sorted(actors),'breaks':breaks,'jukeboxes':music,'save_bytes':C.sizeof(View),
        'checks':['Day 11 to Day 12 transition and light bill','Drink branches and break dialogue',
                  'All nonempty dialogue blocks','Once-only payroll','Version 16 save migration'],
        'hardware_tested':False}
(P/'day12-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
