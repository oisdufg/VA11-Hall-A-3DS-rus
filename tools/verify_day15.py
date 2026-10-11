"""Exercise Day 15 story and drink branches in the ARM engine."""
from pathlib import Path
import ctypes as C
import json

base=Path(__file__).with_name('verify_day1.py')
exec(base.read_text(encoding='utf8').split('checks=[]')[0])
assert C.sizeof(View)==1344 and View.walletCents.offset==1256
tokens=json.loads((P/'generated/day1-metadata.json').read_text())['tokens']

def recipe(id,size='normal',alcohol=None):
    return next(r for r in recipes if r['id']==id and r['size']==size
                and (alcohol is None or r['alcohol']==alcohol))

def pour(r):
    v=get();v.mixer=Mixer();v.mixer.amount[:]=r['amount']
    v.mixer.ice=r['ice'];v.mixer.aged=r['aged'];v.mixer.blended=r['blended']
    v.mixer.ready=True;put(v);call('engine_serve',address)

def drinks(key,run):
    if key==(1,3):return [recipe('cvelvet' if run%3 else 'beer')]
    if key==(1,5):return [recipe('moblast' if run%9==1 else ['moblast','scloud','beer'][run%3])]
    if key==(1,8):return [recipe(x) for x in (('beer','beer') if run%9==1 else [('beer','beer'),('beer','gpunch'),('gpunch','gpunch')][run%3])]
    if key==(2,2):return [recipe('fweaver' if run%2 else 'gpunch')]
    if key==(2,4):return [recipe('beer' if run%2 else 'gpunch')]
    if key==(3,3):return [recipe(['srush','pwman','btini','gpunch'][run%4], 'big' if run%4==1 else 'normal')]
    if key==(3,5):return [recipe('beer' if run%2 else 'gpunch')]
    if key==(4,3):return [recipe('cvelvet','big') if run%7==0 else recipe('mablast','big') if run%3==1 else recipe('scloud' if run%3==0 else 'gpunch')]
    if key==(4,5):return [recipe('cvelvet','big') if run%7==0 else recipe('pman','big') if run%3==0 else recipe('pwman','big') if run%3==1 else recipe('beer')]
    raise AssertionError(key)

seen,orders,actors=set(),set(),set()
completed=breaks=music=0
for run in range(180):
    put(View());call('engine_start',address,1)
    v=get();v.mode=2;v.state.cur_day=14;v.block=1544;v.paidDay=14
    v.walletCents=2000000;v.purchases=(1<<7) if run%2==0 else 0
    if run%2==0:
        v.state.sei5=v.state.sei6=tokens['good']
        v.state.stel1=v.state.stel2=v.state.stel4=v.state.stel5=tokens['right']
        v.state.dorodrink7=tokens['woman'];v.state.dorodrink9=tokens['right']
        v.state.mario1=tokens['woman'];v.state.mario2=tokens['moon'];v.state.mario3=tokens['weav']
    put(v);call('engine_next_day',address)
    v=get();assert (v.state.cur_day,v.block,v.mode)==(15,1601,5)
    assert call('engine_focused',address)==int(run%2==0)
    v.mode=0;put(v)
    for step in range(2500):
        v=get();seen.add(v.block)
        assert call('engine_valid',address)==1,(run,step,v.mode,v.block,v.state.cur_client,v.state.cur_stage)
        actors.update(i for i in range(29) if v.visible[i])
        if v.mode in (2,6):
            assert v.mode==2,(run,v.block,v.state.cur_client,v.state.cur_stage)
            completed+=1;assert v.paidDay==15 and v.walletCents>=2000000
            before=bytes(v);call('engine_settle',address);assert bytes(get())==before
            break
        if v.mode==7:music+=1;call('engine_finish_jukebox',address);continue
        if v.mode==3:breaks+=1;call('engine_advance_checkpoint',address);continue
        if v.mode==0:call('engine_advance_checkpoint',address);continue
        assert v.mode==1,(run,step,v.mode,v.block)
        orders.add(v.state.orders)
        for r in drinks((v.state.cur_client,v.state.cur_stage),run):pour(r)
    else:raise AssertionError(('Day 15 did not finish',run,get().block,get().state.cur_client,get().state.cur_stage))

assert completed==180 and breaks==180 and music>=360,(completed,breaks,music)
assert set(range(1601,1649))<=seen,sorted(set(range(1601,1649))-seen)

# Version 19 saves retain Day 14 story, money and portraits.
put(View());call('engine_start',address,1)
v=get();v.state.cur_day=14;v.block=1544;v.mode=2;v.walletCents=876500
v.paidDay=14;v.state.lexi2=7;v.visible[28]=1
raw=bytes(v)
old=raw[:708]+b''.join(raw[getattr(View,n).offset:getattr(View,n).offset+116] for n in ('visible','position','face'))
old+=raw[View.saveError.offset:View.saveError.offset+12]+b'\0'*4+raw[View.annaUntil.offset:View.annaUntil.offset+72]
assert len(old)==1144
machine.mem_write(0x5120000,old)
assert call('engine_migrate',address,0x5120000,1144)==1
v=get();assert (v.state.cur_day,v.walletCents,v.paidDay,v.state.lexi2)==(14,876500,14,7)
assert v.visible[28]==1 and all(getattr(v.state,n)==0 for n in ('stel9','stel10','stel11','sei10','sei11','dorothy10','dorothy11','mario4','mario5'))

report={'passed':True,'runs':completed,'blocks':sorted(seen),'orders':sorted(orders),
        'actors':sorted(actors),'breaks':breaks,'jukeboxes':music,'save_bytes':C.sizeof(View),
        'checks':['Day 14 to Day 15 transition','Snatcher focus','Paired drink and story branches',
                  'All nonempty dialogue blocks','Break and two music prompts','Once-only payroll',
                  'Version 19 save migration'],'hardware_tested':False}
(P/'day15-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
