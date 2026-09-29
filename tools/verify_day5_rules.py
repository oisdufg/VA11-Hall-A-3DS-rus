"""Compile and execute staged Day 5 controllers; this is not a full-shift test."""
from pathlib import Path
import argparse,ctypes as C,io,json,os,subprocess,random,re
from elftools.elf.elffile import ELFFile
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC

def verify(toolchain,project):
    folder=project/'generated/day5';gcc=toolchain/'bin/arm-none-eabi-gcc.exe';target=folder/'rules.elf'
    env=dict(os.environ,PATH=str(gcc.parent)+os.pathsep+os.environ['PATH'])
    subprocess.run([str(gcc),'-march=armv6k','-mtune=mpcore','-marm','-O2','-Wall','-Wextra','-Werror','-nostdlib','-Wl,-Ttext=0x100000','-Wl,-e,day5_rule',str(folder/'rules.c'),'-o',str(target)],env=env,check=True)
    fields=json.loads((folder/'state-fields.json').read_text());tokens=json.loads((folder/'tokens.json').read_text())
    old=json.loads((project/'generated/state-fields.json').read_text());assert fields[:len(old)]==old
    prior=json.loads((project/'generated/day1-metadata.json').read_text(encoding='utf8'))['tokens'];assert all(tokens[k]==v for k,v in prior.items())
    class State(C.LittleEndianStructure):
        _fields_=[(f,C.c_int32) for f in fields]
    elf=ELFFile(io.BytesIO(target.read_bytes()));uc=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    uc.mem_map(0x10000,0x200000);uc.mem_map(0x300000,0x100000)
    for segment in elf.iter_segments():
        if segment['p_type']=='PT_LOAD':uc.mem_write(segment['p_vaddr'],segment.data())
    symbols={s.name:s['st_value'] for s in elf.get_section_by_name('.symtab').iter_symbols()}
    seen=set();calls=0
    def run(name,s):
        nonlocal calls
        uc.mem_write(0x300000,bytes(s));uc.reg_write(UC_ARM_REG_R0,0x300000);uc.reg_write(UC_ARM_REG_SP,0x3fff00);uc.reg_write(UC_ARM_REG_LR,0x200000)
        uc.emu_start(symbols[name],0x200000,count=100000);assert uc.reg_read(UC_ARM_REG_PC)==0x200000
        result=C.c_int32(uc.reg_read(UC_ARM_REG_R0)).value;calls+=1
        if result>0:seen.add(result)
        return result,State.from_buffer_copy(uc.mem_read(0x300000,C.sizeof(State)))
    recipes=json.loads((project/'generated/recipes.json').read_text())
    for r in recipes:
        for client,stage in [(1,n) for n in (5,10,12,15,20,21,24,25)]+[(2,5),(3,2),(3,4)]:
            s=State(cur_client=client,cur_stage=stage)
            for field,key in [('bevid_a','id'),('kind_a','kind'),('alcohol_a','alcohol'),('flavor_a','flavor')]:setattr(s,field,tokens[r[key]])
            for field,value in zip(('mod_aa','mod_ba','mod_ca','mod_da','mod_ea'),r['amount']):setattr(s,field,value)
            block,out=run('mix5_rule',s);assert 601<=block<=661
            if (client,stage)==(2,5):assert bool(out.rightdrink)==(r['flavor']=='sweet' and r['alcohol']=='no')
    # Special drinks are required for branches missing from the current book.
    for stage,drink,expected in [(5,'rum',605),(20,'rum',629),(21,'abs',632)]:
        block,s=run('mix5_rule',State(cur_client=1,cur_stage=stage,bevid_a=tokens[drink],exdrink_a=tokens[drink]))
        assert block==expected
    block,s=run('mix5_rule',State(cur_client=3,cur_stage=4,bevid_a=tokens['fed']))
    assert block==658 and s.rightdrink==1
    for total in range(1,21):
        block,s=run('mix5_rule',State(cur_client=3,cur_stage=2,mod_aa=1,mod_ea=total-1))
        assert block==(655 if total==17 else 656) and bool(s.rightdrink)==(total==17)
    # Enumerate prior-day flags and the bottle-dependent Alma branches.
    for client in (-2,1,2,3):
        for stage in range(1,29):
            for flags in range(64):
                s=State(cur_client=client,cur_stage=stage,streamdrunk1=flags&1,almadrunk1=(flags>>1)&1,almadrunk2=(flags>>2)&1)
                s.stel1=tokens['right' if flags&8 else 'wrong'];s.stel2=tokens['right' if flags&16 else 'wrong']
                s.alma5=tokens['abs' if flags&32 else 'other'];s.alma6=tokens['alcohol' if flags&4 else 'btini']
                result,out=run('day5_rule',s);assert result in (0,-2,-3) or 601<=result<=661
                if client==2 and stage==3 and flags&32 and flags&4:assert result==647 and out.almadrunk2==1
    expected=set(json.loads((folder/'manifest.json').read_text(encoding='utf8'))['rule_blocks'])
    assert expected<=seen,('uncovered blocks',sorted(expected-seen))
    # Follow complete story/controller routes, not just isolated stage inputs.
    # This driver does not implement the playable UI, payroll or cheap-drink Game Over.
    story=json.loads((folder/'story.json').read_text(encoding='utf8'))
    special=json.loads((folder/'assets-manifest.json').read_text())['special_drinks']
    options=list(recipes)
    for r in recipes:
        if r['optional'] and sum(r['amount'])<=17:
            amounts=list(r['amount']);amounts[4]+=17-sum(amounts)
            options.append(dict(r,amount=amounts,alcohol='yes' if amounts[4] else r['alcohol']))
    assert any(sum(r['amount'])==17 for r in options), 'No valid 17-unit cocktail'
    for r in special:
        options.append(dict(id=r['bevid'],kind=r['kind'],flavor=r['flavor'],alcohol=r['alcohol'],amount=[0]*5,special=True))
    rng=random.Random(1505);routes=set();served_orders=set();jukeboxes=0;breaks=0
    for trial in range(1000):
        s=State(cur_day=5,cur_client=1,cur_stage=1,streamdrunk1=trial%2,almadrunk1=(trial//2)%2)
        s.stel1=tokens['right' if trial&4 else 'wrong'];s.stel2=tokens['right' if trial&8 else 'wrong']
        block,s=run('day5_rule',s)
        for step in range(100):
            if block==-3:break
            if block==-2:
                breaks+=1;s.cur_client=-2;s.cur_stage=1;block,s=run('day5_rule',s);continue
            assert str(block) in story,('missing route',trial,block,s.cur_client,s.cur_stage)
            routes.add(block)
            for key,value in re.findall(r'\[XS:(ph|client|mix|juke),(-?\d+)\]',story[str(block)]):
                setattr(s,{'ph':'cur_stage','client':'cur_client'}.get(key,key),int(value))
            if s.juke:
                jukeboxes+=1;s.juke=0
                if s.cur_client==-2:s.cur_client=2;s.cur_stage=1;block,s=run('day5_rule',s)
                else:block=609
                continue
            if s.mix:
                served_orders.add(s.orders)
                gift=s.stel1==tokens['right'] and s.stel2==tokens['right']
                available=[r for r in options if r['id']!=('abs' if gift else 'rum')]
                r=rng.choice(available)
                if gift and s.cur_client==1 and s.cur_stage==5 and trial%3==0:
                    r=next(r for r in available if r['id']=='rum')
                for field,key in [('bevid_a','id'),('kind_a','kind'),('alcohol_a','alcohol'),('flavor_a','flavor')]:setattr(s,field,tokens[r[key]])
                for field,value in zip(('mod_aa','mod_ba','mod_ca','mod_da','mod_ea'),r['amount']):setattr(s,field,value)
                s.exdrink_a=tokens[r['id']] if r.get('special') else 0
                s.mix=0;block,s=run('mix5_rule',s)
            else:block,s=run('day5_rule',s)
        else:raise AssertionError(('story route loop',trial,block,s.cur_client,s.cur_stage))
    assert expected<=routes,('blocks missing from story flow',sorted(expected-routes))
    assert served_orders==set(range(47,58)),served_orders
    assert breaks==1000 and jukeboxes==2000,(breaks,jukeboxes)
    flow={'passed':True,'routes':1000,'blocks':len(routes),'orders':sorted(served_orders),'breaks':breaks,'jukeboxes':jukeboxes,
          'scope':'Original story tags plus compiled ARM controllers. Game Over, UI, rendering, save integration and hardware are not exercised.'}
    (folder/'flow-test-report.json').write_text(json.dumps(flow,indent=2));print(json.dumps(flow,indent=2))
    report={'passed':True,'arm_calls':calls,'controller_blocks':len(seen),'preserved_state_prefix':len(old),'checks':['Rum, absinthe and Plumfume branches','Exactly 17 ingredient units','Sweet non-alcoholic order','Previous-day flags and Alma branches'],'scope':'Isolated controller rules; playable Day 5 and new drink preparation are not yet integrated.'}
    (folder/'test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('toolchain',type=Path);a=p.parse_args()
    verify(a.toolchain.resolve(),Path(__file__).resolve().parents[1])
