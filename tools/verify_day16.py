"""Exercise Day 16 routes, drinks, Tomcat, and version-20 migration on ARM."""
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
    v.mixer.ice=r['ice'];v.mixer.aged=r['aged'];v.mixer.blended=r['blended']
    v.mixer.ready=True;put(v);call('engine_serve',address)

def drink(client,stage,run):
    wrong='cvelvet'
    choices={
        (1,3):['mablast','srush',wrong],
        (1,6):['splex','fweaver','srush',wrong],
        (1,8):['gpunch','srush',wrong],
        (2,2):['btouch',wrong],
        (2,4):['btini',wrong],
        (2,6):['beer',wrong],
        (3,4):['bjane',wrong],
        (3,6):['beer','fwater',wrong],
        (3,8):['fdream',wrong],
        (4,3):['btini',wrong],
        (4,5):['zstar',wrong],
    }
    variant=run//3 if (client,stage)==(1,8) else run
    name=choices[(client,stage)][variant%len(choices[(client,stage)])]
    return recipe(name,'big' if name in ('mablast','zstar') else None)

seen,orders,actors=set(),set(),set()
completed=breaks=music=0
for run in range(180):
    put(View());call('engine_start',address,1)
    v=get();v.mode=2;v.state.cur_day=15;v.block=1648;v.paidDay=15
    v.walletCents=2000000;v.purchases=(1<<1) if run%2==0 else 0
    v.state.ft_alma=run%2
    v.state.ingdrunk1=run%3==0
    if run%3==0:
        v.state.ing1=v.state.ing2=v.state.ing3=v.state.ing4=v.state.ing5=tokens['sweet']
    else:v.state.ing4=v.state.ing5=tokens['wrong']
    v.state.norma1=tokens['right'] if run%2 else 0
    v.state.dorodrink7=tokens['woman'] if run%2 else 0
    v.state.dorodrink9=tokens['sweet'] if run%2 else tokens['other']
    put(v);call('engine_next_day',address)
    v=get();assert (v.state.cur_day,v.block,v.mode)==(16,1701,5)
    assert call('engine_focused',address)==int(run%2==0)
    v.mode=0;put(v)
    for step in range(3500):
        v=get();seen.add(v.block)
        assert call('engine_valid',address)==1,(run,step,v.mode,v.block,v.state.cur_client,v.state.cur_stage)
        actors.update(i for i in range(30) if v.visible[i])
        if v.mode in (2,6):
            assert v.mode==2,(run,v.block,v.state.cur_client,v.state.cur_stage)
            completed+=1;assert v.paidDay==16 and v.walletCents>=2000000
            before=bytes(v);call('engine_settle',address);assert bytes(get())==before
            break
        if v.mode==7:music+=1;call('engine_finish_jukebox',address);continue
        if v.mode==3:breaks+=1;call('engine_advance_checkpoint',address);continue
        if v.mode==0:call('engine_advance_checkpoint',address);continue
        assert v.mode==1,(run,step,v.mode,v.block,v.state.cur_client,v.state.cur_stage)
        key=(v.state.cur_client,v.state.cur_stage);orders.add(v.state.orders)
        pour(drink(*key,run//2))
    else:raise AssertionError(('Day 16 did not finish',run,get().block,get().state.cur_client,get().state.cur_stage))

assert completed==180 and breaks==180 and music==360,(completed,breaks,music)
assert 29 in actors,actors
assert set(range(1701,1762))<=seen,sorted(set(range(1701,1762))-seen)

# A version-20 save retains Day 15 state, wallet and portrait flags.
put(View());call('engine_start',address,1)
v=get();v.state.cur_day=15;v.block=1648;v.mode=2;v.walletCents=876500
v.paidDay=15;v.state.stel9=7;v.visible[28]=1
raw=bytes(v)
old=raw[:744]+b''.join(raw[getattr(View,n).offset:getattr(View,n).offset+116] for n in ('visible','position','face'))
old+=raw[View.saveError.offset:View.saveError.offset+12]+raw[View.annaUntil.offset:View.annaUntil.offset+72]
assert len(old)==1176
machine.mem_write(0x5120000,old)
assert call('engine_migrate',address,0x5120000,1176)==1
v=get();assert (v.state.cur_day,v.walletCents,v.paidDay,v.state.stel9)==(15,876500,15,7)
assert v.visible[28]==1 and v.visible[29]==0 and v.state.ft_alma==0

report={'passed':True,'runs':completed,'blocks':sorted(seen),'orders':sorted(orders),
        'actors':sorted(actors),'breaks':breaks,'jukeboxes':music,'save_bytes':C.sizeof(View),
        'checks':['Day 15 to Day 16 transition','Maneki-neko focus','All reachable dialogue blocks',
                  'Tomcat portrait','Drink and story branches','Once-only payroll',
                  'Version 20 save migration'],'hardware_tested':False}
(P/'day16-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
