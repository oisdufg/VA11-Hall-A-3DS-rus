"""Exercise Day 18's paired orders, rent and version-22 migration on ARM."""
from pathlib import Path
import ctypes as C
import json

base=Path(__file__).with_name('verify_day1.py')
exec(base.read_text(encoding='utf8').split('checks=[]')[0])
assert C.sizeof(View)==1344 and View.walletCents.offset==1256
tokens=json.loads((P/'generated/day1-metadata.json').read_text())['tokens']

def recipe(name,size=None,alcohol=None):
    return next(r for r in recipes if r['id']==name and (size is None or r['size']==size)
                and (alcohol is None or r['alcohol']==alcohol))

def pour(r):
    v=get();v.mixer=Mixer();v.mixer.amount[:]=r['amount']
    v.mixer.ice=r['ice'];v.mixer.aged=r['aged'];v.mixer.blended=r['blended'];v.mixer.ready=True
    put(v);call('engine_serve',address)

def drinks(client,stage,run):
    k=run//2
    choices={
        (1,6):[[recipe('beer','big')],[recipe('beer','normal')],[recipe('cvelvet')]],
        (1,8):[[recipe('blight'),recipe('srush',alcohol='no')],
               [recipe('srush',alcohol='no'),recipe('blight')],
               [recipe('srush',alcohol='no'),recipe('cvelvet')],
               [recipe('blight'),recipe('beer')],
               [recipe('beer'),recipe('cvelvet')]],
        (1,12):[[recipe('pman'),recipe('pwman')],[recipe('pwman'),recipe('pman')],
                [recipe('pman'),recipe('beer')],[recipe('pwman'),recipe('beer')],
                [recipe('pwman'),recipe('pwman')],
                [recipe('beer'),recipe('cvelvet')]],
        (2,2):[[recipe('gpunch')],[recipe('blight')],[recipe('cvelvet')]],
        (2,4):[[recipe('srush')],[recipe('cvelvet')]],
        (4,2):[[recipe('gpunch')],[recipe('cvelvet')]],
        (4,4):[[recipe('srush')],[recipe('cvelvet')]],
        (4,6):[[recipe('srush')],[recipe('cvelvet')]],
        (5,2):[[recipe('srush')],[recipe('cvelvet')]],
        (5,4):[[recipe('beer','big'),recipe('beer','big')],
               [recipe('beer'),recipe('beer')],
               [recipe('beer'),recipe('cvelvet')],
               [recipe('cvelvet'),recipe('beer')],
               [recipe('cvelvet'),recipe('cvelvet')]],
    }
    items=choices[(client,stage)]
    return items[(k+client+stage//2)%len(items)]

seen,orders,actors=set(),set(),set()
completed=breaks=music=0
for run in range(240):
    put(View());call('engine_start',address,1)
    v=get();v.mode=2;v.state.cur_day=17;v.block=1856;v.paidDay=17
    v.walletCents=2000000 if run%2==0 else 500000
    v.state.streamdrunk1=run%2
    v.state.db1=tokens['right'] if run%3==0 else 0
    if run%4==0:
        v.state.dorodrink7=tokens['woman']
        v.state.dorodrink9=tokens['sweet']
    put(v);call('engine_next_day',address)
    v=get();assert (v.state.cur_day,v.block,v.mode)==(18,1901,5)
    assert v.state.housedl==(1 if run%2==0 else 2)
    assert v.walletCents==(1000000 if run%2==0 else 500000)
    assert call('engine_focused',address)==int(run%2==0)
    v.mode=0;put(v)
    trace=[]
    for step in range(4000):
        v=get();seen.add(v.block)
        trace.append((v.block,v.line,v.mode,v.state.cur_client,v.state.cur_stage))
        assert call('engine_valid',address)==1,(run,step,trace[-12:])
        actors.update(i for i in range(31) if v.visible[i])
        if v.mode in (2,6):
            assert v.mode==2,(run,v.block,v.state.cur_client,v.state.cur_stage)
            completed+=1;assert v.paidDay==18
            before=bytes(v);call('engine_settle',address);assert bytes(get())==before
            break
        if v.mode==7:music+=1;call('engine_finish_jukebox',address);continue
        if v.mode==3:breaks+=1;call('engine_advance_checkpoint',address);continue
        if v.mode==0:call('engine_advance_checkpoint',address);continue
        assert v.mode==1,(run,step,v.mode,v.block,v.state.cur_client,v.state.cur_stage)
        key=(v.state.cur_client,v.state.cur_stage);orders.add(v.state.orders)
        for r in drinks(*key,run):pour(r)
    else:raise AssertionError(('Day 18 did not finish',run,get().block,get().state.cur_client,get().state.cur_stage))

assert completed==240 and breaks==240 and music==480,(completed,breaks,music)
assert set(range(1901,1957))<=seen,sorted(set(range(1901,1957))-seen)

# A version-22 save retains Day 17's story state and wallet.
put(View());call('engine_start',address,1)
v=get();v.state.cur_day=17;v.block=1856;v.mode=2;v.walletCents=876500
v.paidDay=17;v.state.ft_stella=1;v.visible[30]=1
raw=bytes(v)
old=raw[:784]+b''.join(raw[getattr(View,n).offset:getattr(View,n).offset+124] for n in ('visible','position','face'))
old+=raw[View.saveError.offset:View.saveError.offset+12]+raw[View.annaUntil.offset:View.annaUntil.offset+72]
assert len(old)==1240
machine.mem_write(0x5120000,old)
assert call('engine_migrate',address,0x5120000,1240)==1
v=get();assert (v.state.cur_day,v.walletCents,v.paidDay,v.state.ft_stella)==(17,876500,17,1)
assert v.visible[30]==1 and v.state.housedl==0

report={'passed':True,'runs':completed,'blocks':sorted(seen),'orders':sorted(orders),
        'actors':sorted(actors),'breaks':breaks,'jukeboxes':music,'save_bytes':C.sizeof(View),
        'checks':['Day 17 to Day 18 transition','Rent payment and insufficient funds',
                  'Paired drinks and all reachable dialogue blocks','Break and closing scene',
                  'Once-only payroll','Version 22 save migration'],'hardware_tested':False}
(P/'day18-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
