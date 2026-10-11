"""Run the New Year's finale through the compiled ARM engine."""
from pathlib import Path
import ctypes as C
import json

base=Path(__file__).with_name('verify_day1.py')
exec(base.read_text(encoding='utf8').split('checks=[]')[0])
assert C.sizeof(View)==1344 and View.walletCents.offset==1256
tokens=json.loads((P/'generated/day1-metadata.json').read_text())['tokens']

def recipe(name,alcohol=None):
    return next(r for r in recipes if r['id']==name and (alcohol is None or r['alcohol']==alcohol))

seen=set();completed=0;portrait_seen=False
for run in range(90):
    put(View());call('engine_start',address,1)
    v=get();v.mode=2;v.state.cur_day=18;v.block=1956;v.paidDay=18
    v.walletCents=1000000;put(v);call('engine_next_day',address)
    v=get();assert (v.state.cur_day,v.block,v.mode)==(19,2001,5)
    v.mode=0;put(v)
    for step in range(2000):
        v=get();seen.add(v.block)
        if run==0 and v.visible[22] and not portrait_seen:
            snapshot(v,'day19-gaby');portrait_seen=True
        assert call('engine_valid',address)==1,(run,step,v.block,v.line,v.mode,v.state.cur_stage)
        if v.mode==2:
            assert v.paidDay==19
            completed+=1;break
        if v.mode==0:
            call('engine_advance_checkpoint',address);continue
        assert v.mode==1,(run,step,v.block,v.state.cur_stage)
        r=[recipe('srush','yes'),recipe('srush','no'),recipe('beer')][run%3]
        v.mixer=Mixer();v.mixer.amount[:]=r['amount'];v.mixer.ice=r['ice'];v.mixer.aged=r['aged'];v.mixer.blended=r['blended'];v.mixer.ready=True
        put(v);call('engine_serve',address)
        v=get();assert v.state.gabyorder==tokens[['alcohol','soft','nonsweet'][run%3]]
    else:raise AssertionError(('Finale did not finish',run,get().block,get().state.cur_stage))

assert completed==90 and set(range(2001,2010))<=seen,(completed,sorted(seen))

epilogue_seen=set()
for flags in range(17):
    put(View());call('engine_start',address,1)
    v=get();v.mode=2;v.state.cur_day=19;v.block=2009;v.paidDay=19
    s=v.state;s.housedl=2 if flags==16 else 1
    s.sei5=s.sei6=tokens['good'];s.stel1=s.stel2=s.stel4=s.stel5=tokens['right']
    if flags&1:s.truevirgilio2=tokens['right']
    if flags&2:s.miki1=s.miki5=tokens['tea']
    if flags&4:s.alma7=tokens['btini']
    if flags&8:s.dorodrink1=tokens['pwman'];s.dorodrink7=tokens['woman'];s.dorodrink9=tokens['sweet']
    put(v);call('engine_next_day',address)
    v=get();assert v.state.cur_day==20 and v.mode==9,(flags,v.block,v.mode)
    if flags==0:
        snapshot(v,'end-credits')
        call('engine_scroll_credits',address,64)
        assert get().selected==64
    call('engine_finish_credits',address)
    assert get().mode==0
    path=set()
    for step in range(1500):
        v=get();assert call('engine_valid',address)==1,(flags,step,v.block,v.state.cur_stage)
        path.add(v.block);epilogue_seen.add(v.block)
        if flags in (1,2,4,8,16) and step==0:snapshot(v,f'ending-{flags}')
        if v.mode==2:break
        assert v.mode==0,(flags,step,v.block,v.mode)
        call('engine_advance_checkpoint',address)
    else:raise AssertionError(('Epilogue did not finish',flags,get().block,get().state.cur_stage))
    expected={2106} if flags==16 else {2105}|{n for bit,n in ((1,2101),(2,2102),(4,2104),(8,2103)) if flags&bit}
    assert path==expected,(flags,path,expected)
assert epilogue_seen==set(range(2101,2107)),epilogue_seen

# Version 23 save: the extra Day 19 branch flag must not shift wallet or portraits.
put(View());call('engine_start',address,1)
v=get();v.state.cur_day=18;v.block=1956;v.mode=2;v.walletCents=876500
v.paidDay=18;v.state.housedl=1;v.visible[27]=1
raw=bytes(v)
old=raw[:832]+b''.join(raw[getattr(View,n).offset:getattr(View,n).offset+124] for n in ('visible','position','face'))
old+=raw[View.saveError.offset:View.saveError.offset+12]+raw[View.annaUntil.offset:View.annaUntil.offset+72]
assert len(old)==1288
machine.mem_write(0x5120000,old)
assert call('engine_migrate',address,0x5120000,1288)==1
v=get();assert (v.state.cur_day,v.walletCents,v.paidDay,v.state.housedl,v.visible[27],v.state.gabyorder)==(18,876500,18,1,1,0)

report={'passed':True,'runs':completed,'blocks':sorted(seen),'epilogue_blocks':sorted(epilogue_seen),'save_bytes':C.sizeof(View),
        'checks':['Day 18 to Day 19 transition','All three drink outcomes','All finale dialogue blocks','All epilogue branches',
                  'Once-only payroll','Version 23 save migration'],'hardware_tested':False}
(P/'day19-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
