"""Exercise both Day 17 visitor routes and version-21 save migration on ARM."""
from pathlib import Path
import ctypes as C
import json

base=Path(__file__).with_name('verify_day1.py')
exec(base.read_text(encoding='utf8').split('checks=[]')[0])
assert C.sizeof(View)==1344 and View.walletCents.offset==1256
tokens=json.loads((P/'generated/day1-metadata.json').read_text())['tokens']

def recipe(name,size=None):
    return next(r for r in recipes if r['id']==name and (size is None or r['size']==size))

def pour(r):
    v=get();v.mixer=Mixer();v.mixer.amount[:]=r['amount']
    v.mixer.ice=r['ice'];v.mixer.aged=r['aged'];v.mixer.blended=r['blended'];v.mixer.ready=True
    put(v)
    if r['id']=='tea':call('engine_pour_special',address,tokens['tea'])
    call('engine_serve',address)

def drink(client,stage,run):
    choices={
        (1,3):[('beer','big'),('beer','normal'),'cvelvet'],
        (1,6):[('moblast','big'),'beer','cvelvet'],
        (1,8):['pdriver','cvelvet'],
        (2,3):['sstar','cvelvet'],
        (2,6):['tea','scloud','cvelvet'],
        (2,10):['sstar','cvelvet'],
        (3,2):['bjane','cvelvet'],
        (3,4):['btini','cvelvet'],
        (3,8):['beer','srush'],
        (4,2):['srush','cvelvet'],
        (4,4):['btini','cvelvet'],
        (5,2):[('cvelvet','big'),('cvelvet','normal'),'srush'],
        (5,4):['srush','cvelvet'],
        (5,6):['beer','cvelvet'],
    }
    items=choices[(client,stage)]
    value=items[(run//2+stage//2)%len(items)]
    return recipe(*(value if isinstance(value,tuple) else (value,None)))

seen,orders,actors=set(),set(),set()
completed=breaks=music=0
for run in range(240):
    put(View());call('engine_start',address,1)
    v=get();v.mode=2;v.state.cur_day=16;v.block=1761;v.paidDay=16
    v.walletCents=2000000;v.purchases=(1<<2)|(1<<19) if run%2==0 else (1<<19)
    v.state.ft_stella=run%2
    v.state.dondrunk1=v.state.dondrunk3=run%2
    v.state.miki1=tokens['tea'] if run%4==0 else tokens['wrong']
    if run%3==0:
        v.state.stel1=v.state.stel2=v.state.stel4=v.state.stel5=tokens['right']
        v.state.sei5=v.state.sei6=tokens['good']
    put(v);call('engine_next_day',address)
    v=get();assert (v.state.cur_day,v.block,v.mode)==(17,1801,5)
    assert call('engine_focused',address)==int(run%2==0)
    v.mode=0;put(v)
    for step in range(4500):
        v=get();seen.add(v.block)
        assert call('engine_valid',address)==1,(run,step,v.mode,v.block,v.state.cur_client,v.state.cur_stage)
        actors.update(i for i in range(31) if v.visible[i])
        if v.mode in (2,6):
            assert v.mode==2,(run,v.block,v.state.cur_client,v.state.cur_stage)
            completed+=1;assert v.paidDay==17 and v.walletCents>=2000000
            before=bytes(v);call('engine_settle',address);assert bytes(get())==before
            break
        if v.mode==7:music+=1;call('engine_finish_jukebox',address);continue
        if v.mode==3:breaks+=1;call('engine_advance_checkpoint',address);continue
        if v.mode==0:call('engine_advance_checkpoint',address);continue
        assert v.mode==1,(run,step,v.mode,v.block,v.state.cur_client,v.state.cur_stage)
        key=(v.state.cur_client,v.state.cur_stage);orders.add(v.state.orders)
        pour(drink(*key,run))
    else:raise AssertionError(('Day 17 did not finish',run,get().block,get().state.cur_client,get().state.cur_stage))

assert completed==240 and breaks==240 and music==480,(completed,breaks,music)
assert 30 in actors,actors
assert set(range(1801,1868))<=seen,sorted(set(range(1801,1868))-seen)

# A version-21 save retains Day 16's story state, money and portraits.
put(View());call('engine_start',address,1)
v=get();v.state.cur_day=16;v.block=1761;v.mode=2;v.walletCents=876500
v.paidDay=16;v.state.ing8=7;v.visible[29]=1
raw=bytes(v)
old=raw[:772]+b''.join(raw[getattr(View,n).offset:getattr(View,n).offset+120] for n in ('visible','position','face'))
old+=raw[View.saveError.offset:View.saveError.offset+12]+raw[View.annaUntil.offset:View.annaUntil.offset+72]
assert len(old)==1216
machine.mem_write(0x5120000,old)
assert call('engine_migrate',address,0x5120000,1216)==1
v=get();assert (v.state.cur_day,v.walletCents,v.paidDay,v.state.ing8)==(16,876500,16,7)
assert v.visible[29]==1 and v.visible[30]==0 and v.state.ft_stella==0

report={'passed':True,'runs':completed,'blocks':sorted(seen),'orders':sorted(orders),
        'actors':sorted(actors),'breaks':breaks,'jukeboxes':music,'save_bytes':C.sizeof(View),
        'checks':['Day 16 to Day 17 transition','Kira Miki poster focus',
                  'Both Stella and Alma visitor routes','Jess portrait',
                  'All reachable dialogue blocks','Once-only payroll',
                  'Version 21 save migration'],'hardware_tested':False}
(P/'day17-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
