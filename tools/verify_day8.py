"""Exercise Day 8 on the compiled ARM engine using only local generated resources."""
from pathlib import Path
import ctypes as C
import json
import random

base = Path(__file__).with_name('verify_day1.py')
exec(base.read_text(encoding='utf8').split('checks=[]')[0])

assert C.sizeof(View) == 944, C.sizeof(View)
tokens = json.loads((P/'generated/day1-metadata.json').read_text(encoding='utf8'))['tokens']
want = {69:'gtemple',70:'fdream',71:'bfairy',72:'bjane',73:'gpunch',
        74:'gtemple',75:'beer',76:'bjane',77:'zstar'}
seen,orders,actors,completed,failed,breaks,jukeboxes=set(),set(),set(),0,0,0,0
rng=random.Random(8008)

def serve(v,recipe):
    v.mixer=Mixer()
    v.mixer.amount[:]=recipe['amount']
    v.mixer.ice=recipe['ice'];v.mixer.aged=recipe['aged']
    v.mixer.blended=recipe['blended'];v.mixer.ready=True
    put(v);call('engine_serve',address)

for run in range(160):
    put(View());call('engine_start',address,1)
    v=get();v.mode=2;v.state.cur_day=7;v.block=861;v.paidDay=7
    v.walletCents=150000;v.purchases=(1<<18) if run%2==0 else 0
    v.state.ing1=v.state.ing2=v.state.ing3=tokens['sweet'] if run%4==0 or run==5 else 0
    v.state.ingdrunk1=1 if run==5 else 0
    put(v);call('engine_next_day',address)
    v=get();assert (v.state.cur_day,v.block,v.mode)==(8,901,5)
    assert call('engine_focused',address)==(run%2==0)
    v.mode=0;put(v)
    for step in range(2100):
        v=get();seen.add(v.block)
        assert call('engine_valid',address)==1,(run,v.mode,v.block,v.state.cur_client,v.state.cur_stage)
        if v.visible[19]:actors.add(19)
        if v.mode in (2,6):
            if v.mode==2:
                completed+=1
                assert v.paidDay==8 and v.walletCents>=150000
                old=bytes(v);call('engine_settle',address);assert bytes(get())==old
            else:failed+=1
            if run<4:assert v.mode==2,(run,'expected completion',v.block)
            break
        if v.mode==7:
            jukeboxes+=1;call('engine_finish_jukebox',address);continue
        if v.mode==3:
            breaks+=1;call('engine_advance_checkpoint',address);continue
        if v.mode==0:
            call('engine_advance_checkpoint',address);continue
        assert v.mode==1,(run,step,v.mode,v.block)
        order=v.state.orders;orders.add(order)
        assert order in want or order>=1160,(run,order,v.block,v.state.cur_client,v.state.cur_stage)
        desired=want.get(order)
        if desired is None:
            desired={1:{3:'gtemple',5:'fdream'},2:{2:'bfairy',4:'bjane'},
                     4:{2:'gpunch',4:'gtemple',6:'beer'},5:{2:'bjane',6:'zstar'}}[v.state.cur_client][v.state.cur_stage]
        forced={4:{(4,2):'cspike',(4,4):'cspike',(4,6):'fwater',(5,6):'fwater'},
                5:{(5,2):'bfairy',(5,6):'bfairy'}}
        desired=forced.get(run,{}).get((v.state.cur_client,v.state.cur_stage),desired)
        if run>=6 and rng.random()<.23:desired=rng.choice(['beer','srush','gpunch','bfairy','zstar'])
        recipe=next(r for r in recipes if r['id']==desired and (desired!='bfairy' or r['alcohol']=='no'))
        serve(v,recipe)
    else:raise AssertionError(('Day 8 did not finish',run,get().block,get().state.cur_client,get().state.cur_stage))

assert completed>100 and actors=={19} and breaks>=160 and jukeboxes>=160
assert set(want)<=orders or len([n for n in orders if n>=1160])>0
assert set(range(901,952))<=seen,sorted(set(range(901,952))-seen)

# Version 12 save had 109 state words and nineteen character slots.
put(View());call('engine_start',address,1)
v=get();v.state.cur_day=7;v.block=861;v.mode=2;v.walletCents=543210
v.purchases=1<<18;v.paidDay=7;v.day4Download=1
raw=bytes(v)
old=raw[:80]+raw[80:80+436]
old+=raw[View.visible.offset:View.visible.offset+76]
old+=raw[View.position.offset:View.position.offset+76]
old+=raw[View.face.offset:View.face.offset+76]
old+=raw[View.saveError.offset:View.saveError.offset+12]+b'\0'*4
old+=raw[View.annaUntil.offset:View.annaUntil.offset+72]
assert len(old)==832
machine.mem_write(0x5120000,old)
assert call('engine_migrate',address,0x5120000,832)==1
v=get();assert (v.state.cur_day,v.walletCents,v.purchases,v.day4Download)==(7,543210,1<<18,1)
assert v.visible[19]==v.position[19]==v.face[19]==0

# The third cheap wrong drink still leads to Dana's failure scene.
put(View());call('engine_start',address,1)
v=get();v.state.cur_day=8;v.state.cur_client=1;v.state.cur_stage=3
v.mode=1;v.cheapErrors=2
serve(v,next(r for r in recipes if r['id']=='bfairy' and r['alcohol']=='no'))
v=get();assert (v.failed,v.block,v.mode)==(1,301,0),(v.failed,v.block,v.mode,v.cheapErrors,v.state.shouldpay,v.state.rightdrink)
assert call('engine_can_save',address)==0

report={'passed':True,'runs':160,'completed':completed,'game_overs':failed,
        'orders':sorted(orders),'blocks':sorted(seen),'breaks':breaks,'jukeboxes':jukeboxes,
        'new_actor_indices':sorted(actors),'save_bytes':C.sizeof(View),
        'checks':['Day 7 to Day 8 transition','Focused and distracted orders',
                  'Mixer outcomes and story branches','Midday break and music selection',
                  'Payroll exactly once','Game Over after three cheap wrong drinks',
                  'Version 12 save migration'],
        'hardware_tested':False}
(P/'day8-test-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
