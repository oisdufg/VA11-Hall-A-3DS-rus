"""Exercise Day 9 story routes on the compiled ARM engine."""
from pathlib import Path
import ctypes as C
import json
import random

base=Path(__file__).with_name('verify_day1.py')
exec(base.read_text(encoding='utf8').split('checks=[]')[0])

assert C.sizeof(View)==1344,C.sizeof(View)
seen,orders,actors=set(),set(),set()
completed=failed=breaks=music=0
rng=random.Random(9009)

def pour(v,r):
    v.mixer=Mixer();v.mixer.amount[:]=r['amount']
    v.mixer.ice=r['ice'];v.mixer.aged=r['aged']
    v.mixer.blended=r['blended'];v.mixer.ready=True
    put(v);call('engine_serve',address)

gold={(1,3):('fdream','no','normal'),
      (2,2):('pwman',None,'big'),(2,4):('moblast',None,'normal'),
      (2,6):('fweaver',None,'normal'),(3,2):('bjane',None,'normal'),
      (3,4):('bfairy',None,'big'),(3,6):('cvelvet',None,'normal'),
      (4,2):('beer',None,'normal')}
for run in range(180):
    put(View());call('engine_start',address,1)
    v=get();v.mode=2;v.state.cur_day=8;v.block=951;v.paidDay=8
    v.walletCents=173200;v.purchases=(1<<13) if run%2==0 else 0
    v.state.kimdrunk1=run%2
    put(v);call('engine_next_day',address)
    v=get();assert (v.state.cur_day,v.block,v.mode)==(9,1001,5)
    assert call('engine_focused',address)==int(run%2==0)
    v.mode=0;put(v)
    for step in range(2300):
        v=get();seen.add(v.block)
        assert call('engine_valid',address)==1,(run,step,v.mode,v.block,v.state.cur_client,v.state.cur_stage)
        actors.update(i for i in (20,21,22) if v.visible[i])
        if v.mode in (2,6):
            if v.mode==2:
                completed+=1;assert v.paidDay==9 and v.walletCents>=173200
                old=bytes(v);call('engine_settle',address);assert bytes(get())==old
            else:failed+=1
            if run<4:assert v.mode==2,(run,v.block)
            break
        if v.mode==7:
            music+=1;call('engine_finish_jukebox',address);continue
        if v.mode==3:
            breaks+=1;call('engine_advance_checkpoint',address);continue
        if v.mode==0:
            call('engine_advance_checkpoint',address);continue
        assert v.mode==1,(run,step,v.mode,v.block)
        orders.add(v.state.orders)
        key=(v.state.cur_client,v.state.cur_stage)
        assert key in gold,(run,key,v.block,v.state.orders)
        id,alcohol,size=gold[key]
        if run>=5 and rng.random()<.31:
            id=rng.choice(['beer','srush','moblast','bfairy','fwater'])
            alcohol=None;size='normal'
        if run==4 and key==(2,2):id,size='mablast','big'
        if run==4 and key==(2,4):id,size='gpunch','normal'
        if run==4 and key==(2,6):id,size='cspike','normal'
        options=[q for q in recipes if q['id']==id and q['size']==size and (alcohol is None or q['alcohol']==alcohol)]
        assert options,(run,key,id,alcohol,size)
        r=options[0]
        pour(v,r)
    else:raise AssertionError(('Day 9 did not finish',run,get().block,get().state.cur_client,get().state.cur_stage))

assert completed>150 and actors=={20,21,22} and breaks>=180 and music>=360
assert set(range(1001,1048))<=seen,sorted(set(range(1001,1048))-seen)

# Version 13 saves retain their Day 8 choices, actors, wallet and purchases.
put(View());call('engine_start',address,1)
v=get();v.state.cur_day=8;v.block=951;v.mode=2;v.walletCents=876500
v.purchases=1<<18;v.paidDay=8;v.day4Download=1;v.visible[19]=1
raw=bytes(v)
old=raw[:80]+raw[80:556]
old+=raw[View.visible.offset:View.visible.offset+80]
old+=raw[View.position.offset:View.position.offset+80]
old+=raw[View.face.offset:View.face.offset+80]
old+=raw[View.saveError.offset:View.saveError.offset+12]
old+=raw[View.annaUntil.offset:View.annaUntil.offset+72]
assert len(old)==880
machine.mem_write(0x5120000,old)
assert call('engine_migrate',address,0x5120000,880)==1
v=get();assert (v.state.cur_day,v.walletCents,v.purchases,v.paidDay,v.day4Download)==(8,876500,1<<18,8,1)
assert v.visible[19]==1 and all(v.visible[i]==0 for i in (20,21,22))

# A third cheap wrong paid drink triggers the shared Game Over scene.
put(View());call('engine_start',address,1)
v=get();v.state.cur_day=9;v.state.cur_client=3;v.state.cur_stage=4
v.mode=1;v.cheapErrors=2
pour(v,next(r for r in recipes if r['id']=='fwater' and r['size']=='normal'))
v=get();assert (v.failed,v.block,v.mode)==(1,301,0),(v.failed,v.block,v.mode,v.cheapErrors)
assert call('engine_can_save',address)==0

report={'passed':True,'runs':180,'completed':completed,'game_overs':failed,
        'blocks':sorted(seen),'orders':sorted(orders),'new_actor_indices':sorted(actors),
        'breaks':breaks,'jukeboxes':music,'save_bytes':C.sizeof(View),
        'checks':['Day 8 to Day 9 transition','Focused and distracted orders',
                  'Norma, Mario and Gaby portraits','Mixer outcomes and story branches',
                  'Midday break and two music prompts','Payroll exactly once',
                  'Game Over after three cheap wrong drinks',
                  'Version 13 save migration'],'hardware_tested':False}
(P/'day9-test-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
