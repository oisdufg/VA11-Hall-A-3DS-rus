"""Exercise Day 14 drink routes, optional Lexi scene and save migration."""
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

def drink(key,run):
    good=run%4!=1
    if key==(1,3):return recipe('bjane' if good else 'beer')
    if key==(1,5):return recipe('blight' if good else 'beer')
    if key==(1,8):return recipe('gpunch' if good else 'beer')
    if key==(2,2):return recipe('gpunch' if good else 'beer')
    if key==(2,4):return recipe('fweaver' if good else 'beer')
    if key==(3,2):return recipe('fweaver' if good else 'beer')
    if key==(3,4):return recipe('srush' if good else 'beer')
    if key==(4,3):return recipe('beer' if good else 'gpunch')
    if key==(4,5):return recipe('srush' if good else 'beer')
    if key==(4,7):return recipe('beer' if good else 'gpunch')
    raise AssertionError(key)

seen,orders,actors=set(),set(),set()
completed=breaks=music=0
for run in range(120):
    put(View());call('engine_start',address,1)
    v=get();v.mode=2;v.state.cur_day=13;v.block=1427;v.paidDay=12
    v.walletCents=2000000;v.purchases=(1<<6) if run%2==0 else 0
    v.state.ft_any=int(run%3==0)
    v.state.stel1=v.state.stel2=v.state.stel4=v.state.stel5=87 if run%2==0 else 0
    put(v);call('engine_next_day',address)
    v=get();assert (v.state.cur_day,v.block,v.mode)==(14,1501,5)
    assert call('engine_focused',address)==int(run%2==0)
    v.mode=0;put(v)
    for step in range(2100):
        v=get();seen.add(v.block)
        assert call('engine_valid',address)==1,(run,step,v.mode,v.block,v.state.cur_client,v.state.cur_stage)
        actors.update(i for i in range(29) if v.visible[i])
        if v.mode in (2,6):
            assert v.mode==2,(run,v.block,v.state.cur_client,v.state.cur_stage)
            completed+=1;assert v.paidDay==14 and v.walletCents>=2000000
            before=bytes(v);call('engine_settle',address);assert bytes(get())==before
            break
        if v.mode==7:music+=1;call('engine_finish_jukebox',address);continue
        if v.mode==3:breaks+=1;call('engine_advance_checkpoint',address);continue
        if v.mode==0:call('engine_advance_checkpoint',address);continue
        assert v.mode==1,(run,step,v.mode,v.block)
        orders.add(v.state.orders);pour(drink((v.state.cur_client,v.state.cur_stage),run))
    else:raise AssertionError(('Day 14 did not finish',run,get().block,get().state.cur_client,get().state.cur_stage))

assert completed==120 and breaks==120 and music>=120,(completed,breaks,music)
assert set(range(1501,1545))<=seen,sorted(set(range(1501,1545))-seen)
assert {27,28}<=actors,actors

# Version 18 saves retain party progress and choices.
put(View());call('engine_start',address,1)
v=get();v.state.cur_day=13;v.block=1427;v.mode=2;v.walletCents=876500
v.paidDay=12;v.state.dogpick=1;v.visible[24]=1
raw=bytes(v)
old=raw[:676]+b''.join(raw[getattr(View,n).offset:getattr(View,n).offset+108] for n in ('visible','position','face'))
old+=raw[View.saveError.offset:View.saveError.offset+12]+b'\0'*4+raw[View.annaUntil.offset:View.annaUntil.offset+72]
assert len(old)==1088
machine.mem_write(0x5120000,old)
assert call('engine_migrate',address,0x5120000,1088)==1
v=get();assert (v.state.cur_day,v.walletCents,v.paidDay,v.state.dogpick)==(13,876500,12,1)
assert v.visible[24]==1 and all(getattr(v.state,n)==0 for n in ('art6','art7','ft_any','lexi1','lexi2','truevirgilio1','truevirgilio2','truevirgilio3'))

report={'passed':True,'runs':completed,'blocks':sorted(seen),'orders':sorted(orders),
        'actors':sorted(actors),'breaks':breaks,'jukeboxes':music,'save_bytes':C.sizeof(View),
        'checks':['Day 13 to Day 14 transition','Y2K focus','Drink branches and optional Lexi scene',
                  'All 44 nonempty dialogue blocks','Break and music prompts','Once-only payroll',
                  'Version 18 save migration'],'hardware_tested':False}
(P/'day14-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
