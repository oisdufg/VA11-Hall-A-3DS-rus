"""Exercise Day 13 party choices and old-save migration on the ARM engine."""
from pathlib import Path
import ctypes as C
import json

base=Path(__file__).with_name('verify_day1.py')
exec(base.read_text(encoding='utf8').split('checks=[]')[0])
assert C.sizeof(View)==1344 and View.walletCents.offset==1256

seen,choices,actors=set(),set(),set()
completed=0
for run in range(125):
    put(View());call('engine_start',address,1)
    v=get();v.mode=2;v.state.cur_day=12;v.block=1349;v.paidDay=12
    v.walletCents=2000000;v.state.lightdl=1
    put(v);call('engine_next_day',address)
    v=get();assert (v.state.cur_day,v.block,v.mode)==(13,1426,5)
    v.mode=0;put(v)
    for step in range(2200):
        v=get();seen.add(v.block)
        assert call('engine_valid',address)==1,(run,step,v.mode,v.block,v.state.cur_client,v.state.cur_stage)
        actors.update(i for i in range(27) if v.visible[i])
        if v.mode==2:
            completed+=1;assert v.paidDay==12 and v.walletCents==2000000
            before=bytes(v);call('engine_settle',address);assert bytes(get())==before
            break
        if v.mode==8:
            stage=v.state.cur_stage
            index=(run//(5**{2:0,4:1,7:2}[stage]))%5
            if index==2 and v.state.dogpick:index=3
            choices.add((stage,index,v.state.dogpick))
            call('engine_choose',address,index)
            assert get().mode==0,(run,stage,index)
            continue
        assert v.mode==0,(run,step,v.mode,v.block)
        call('engine_advance_checkpoint',address)
    else:raise AssertionError(('Day 13 did not finish',run,get().block,get().state.cur_client,get().state.cur_stage))

assert completed==125,completed
assert set(range(1401,1428))<=seen,sorted(set(range(1401,1428))-seen)
assert {0,1,6,7,9,19,24}<=actors,actors

# Version 17 saves retain Day 12 branch decisions and visible actors.
put(View());call('engine_start',address,1)
v=get();v.state.cur_day=12;v.block=1349;v.mode=2;v.walletCents=876500
v.paidDay=12;v.state.lightdl=1;v.state.sei9=7;v.visible[25]=1
raw=bytes(v)
old=raw[:668]+b''.join(raw[getattr(View,n).offset:getattr(View,n).offset+108] for n in ('visible','position','face'))
old+=raw[View.saveError.offset:View.saveError.offset+12]+b'\0'*4+raw[View.annaUntil.offset:View.annaUntil.offset+72]
assert len(old)==1080
machine.mem_write(0x5120000,old)
assert call('engine_migrate',address,0x5120000,1080)==1
v=get();assert (v.state.cur_day,v.walletCents,v.paidDay,v.state.lightdl,v.state.sei9)==(12,876500,12,1,7)
assert v.visible[25]==1 and (v.state.dogpick,v.state.pickdare)==(0,0)

report={'passed':True,'runs':completed,'blocks':sorted(seen),'choices':sorted(choices),
        'actors':sorted(actors),'save_bytes':C.sizeof(View),
        'checks':['Day 12 to party transition','Three selectable guest rounds',
                  'All 27 nonempty party dialogue blocks','Day off without payroll',
                  'Version 17 save migration'],'hardware_tested':False}
(P/'day13-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
