"""Run Day 7 routes on the compiled ARM engine without game assets in Git."""
from pathlib import Path
import ctypes as C,json,random,struct

base=Path(__file__).with_name('verify_day1.py')
exec(base.read_text(encoding='utf8').split('checks=[]')[0])

tokens=json.loads((P/'generated/day1-metadata.json').read_text(encoding='utf8'))['tokens']
want={58:'srush',59:'splex',60:'beer',61:'zstar',62:'btouch',63:'pman',
      64:'beer',65:'mablast',66:'pman',67:'fwater',68:'beer',69:'srush'}
seen=set();orders=set();faces=set();completed=0;failed=0;music=0
rng=random.Random(7017)
forced={20:{69:'beer',64:'beer',65:'moblast',66:'pdriver'},
        21:{69:'beer',65:'moblast',66:'pwman'},
        22:{69:'srush',63:'pwman'},
        23:{59:'pdriver',69:'srush'},
        24:{69:'srush',67:'moblast'},
        25:{69:'srush',67:'gpunch'}}

def pour(v,recipe):
    v.mixer=Mixer()
    v.mixer.amount[:]=recipe['amount']
    v.mixer.ice=recipe['ice'];v.mixer.aged=recipe['aged']
    v.mixer.blended=recipe['blended'];v.mixer.ready=True
    put(v);call('engine_serve',address)

for run in range(400):
    put(View());call('engine_start',address,1)
    v=get();v.mode=2;v.state.cur_day=6;v.paidDay=5
    v.state.jilldrunk1=run%2
    v.state.stel1=v.state.stel2=tokens['right' if run%3 else 'wrong']
    v.walletCents=123450;v.purchases=4096|(1<<5)
    put(v);call('engine_next_day',address)
    v=get();assert (v.state.cur_day,v.block,v.mode)==(7,801,5)
    assert (v.walletCents,v.purchases,v.state.jilldrunk1)==(123450,4096|(1<<5),run%2)
    v.mode=0;put(v)
    for step in range(1900):
        v=get();seen.add(v.block)
        assert call('engine_valid',address)==1,(run,v.block,v.mode,v.state.cur_client,v.state.cur_stage)
        for actor in (17,18):
            if v.visible[actor] and actor not in faces:
                faces.add(actor);snapshot(v,f'day7-actor{actor}')
        if v.mode in (2,6):
            if v.mode==2:
                completed+=1
                assert v.paidDay==7 and v.walletCents>123450
                old=bytes(v);call('engine_settle',address);assert bytes(get())==old
            else:failed+=1
            if run<8:assert v.mode==2,(run,'golden route',v.block)
            break
        if v.mode==7:
            music+=1;call('engine_finish_jukebox',address);continue
        if v.mode in (0,3):
            checkpoint=call('engine_advance_checkpoint',address)
            assert checkpoint==int(get().mode==2)
            continue
        assert v.mode==1,(run,step,v.block,v.mode)
        order=v.state.orders;orders.add(order)
        assert order in want,(run,order,v.block)
        correct=run<8 or run in forced or rng.random()<0.72
        desired=forced.get(run,{}).get(order,want[order] if correct else rng.choice(['beer','srush','mablast','btouch','fwater']))
        size='big' if run==20 and order in (64,65,66) else None
        recipe=next(r for r in recipes if r['id']==desired and (size is None or r['size']==size))
        pour(v,recipe)
    else:raise AssertionError(('Day 7 did not finish',run,get().block,get().state.cur_client,get().state.cur_stage))

assert completed>200 and faces=={17,18},(completed,faces)
assert orders==set(range(58,70)),sorted(orders)
assert set(range(801,862))<=seen,sorted(set(range(801,862))-seen)

# A version 9 save used 760 bytes and 17 actors. Migrating it preserves
# wallet, ownership and Day 6 beer choices while zeroing new Day 7 fields.
put(View());call('engine_start',address,1)
v=get();v.state.cur_day=6;v.mode=2;v.block=718;v.day6Beers=9
v.walletCents=765432;v.purchases=1024;v.paidDay=5
old=bytes(v)[:80]+bytes(v.state)[:396]
old+=bytes(v.visible)[:68]+bytes(v.position)[:68]+bytes(v.face)[:68]
old+=bytes(v)[View.saveError.offset:View.saveError.offset+12]+b'\0'*4
old+=bytes(v)[View.annaUntil.offset:View.annaUntil.offset+64]
assert len(old)==760
machine.mem_write(0x5120000,old);assert call('engine_migrate',address,0x5120000,760)==1,(len(old),get().state.cur_day,get().block,get().mode,get().walletCents,get().day6Beers)
v=get();assert (v.walletCents,v.purchases,v.day6Beers,v.state.cur_day)==(765432,1024,9,6)
assert v.state.jilldrunk1==0 and v.visible[17]==v.visible[18]==0
old12=bytearray(old)
struct.pack_into('<i',old12,724,12)
machine.mem_write(0x5120000,bytes(old12));assert call('engine_migrate',address,0x5120000,760)==1
assert get().state.jilldrunk1==1

report={'passed':True,'routes':400,'completed':completed,'failed':failed,
        'blocks':sorted(seen),'orders':sorted(orders),'new_actor_indices':sorted(faces),
        'jukebox_prompts':music,'save_bytes':C.sizeof(View),
        'checks':['Day 6 to Day 7 transition and Jill drinking flag','All Day 7 dialogue blocks and orders',
                  'Brian and Cass portraits','Payroll once and Game Over routes','Version 9 save migration'],
        'hardware_tested':False}
(P/'day7-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
