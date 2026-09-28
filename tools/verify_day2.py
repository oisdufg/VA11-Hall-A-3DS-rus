from verify_day1 import *
import struct
seen2=set();screens2=set();pairs=0
for run in range(700):
 put(View());call('engine_start',address,1);v=get();v.mode=2
 v.state.dondrunk1=run%2;v.state.kimdrunk1=(run//2)%2;v.state.ingdrunk1=(run//4)%2
 put(v);call('engine_next_day',address);v=get()
 assert v.mode==5 and v.state.cur_day==2 and v.block==201
 assert v.state.dondrunk1==run%2
 v.mode=0;put(v);steps=0
 while True:
  v=get();steps+=1;seen2.add(v.block)
  assert steps<1700 and v.mode!=4,('stuck',run,steps,v.block,v.line,v.state.cur_client,v.state.cur_stage)
  assert call('engine_valid',address)==1
  if run==0:
   for a in (6,7,8):
    if v.visible[a] and a not in screens2:snapshot(v,'day2-actor'+str(a));screens2.add(a)
  if v.mode in (2,6):
   if run==0:assert v.mode==2
   break
  if v.mode in (0,3):
   result=call('engine_advance_checkpoint',address)
   assert result==int(get().mode==2),('save outside end of day',v.block,v.line)
   continue
  assert v.mode==1
  if run==0:
   want={17:'beer',18:'mablast',19:'gpunch',20:'pwman',21:'moblast',23:'mablast',24:'scloud',25:'bfairy',26:'gpunch'}
   name=want.get(v.state.orders,'gpunch' if v.state.heldRecipe else 'scloud')
   r=next(r for r in recipes if r['id']==name and (v.state.orders!=22 or v.state.heldRecipe or r['size']=='big'))
  else:r=rng.choice(recipes)
  v.mixer=Mixer();v.mixer.amount[:]=r['amount'];v.mixer.ice=r['ice'];v.mixer.aged=r['aged'];v.mixer.blended=r['blended'];v.mixer.ready=True
  if v.state.slotamount==2:
   pairs+=1
   if run==0:snapshot(v,'day2-pair'+str(bool(v.state.heldRecipe)))
  put(v);call('engine_serve',address)
 if run<2:print('Day 2 completed',run,steps,flush=True)
# Exhaustively check both recipe-slot orders and every recipe pair at Dorothy's order.
for a in recipes:
 for b in recipes:
  v=View();put(v);call('engine_start',address,1);v=get()
  v.state.cur_day=2;v.state.cur_client=2;v.state.cur_stage=7;v.state.slotamount=2;v.mode=1
  for r in (a,b):
   v.mixer=Mixer();v.mixer.amount[:]=r['amount'];v.mixer.ice=r['ice'];v.mixer.aged=r['aged'];v.mixer.blended=r['blended'];v.mixer.ready=True
   put(v);call('engine_serve',address);v=get()
  assert 232<=v.block<=236 and v.mode==0 and not v.state.heldRecipe
  seen2.add(v.block)
# Migrate an authentic 0.2/0.3 binary layout and retain both emotion and branching flags.
legacy=bytearray(296);struct.pack_into('<8i',legacy,0,119,0,0,0,0,0,0,1)
lf=json.loads((P/'generated/legacy-state-fields.json').read_text())
for field,val in {'cur_client':1,'cur_stage':9,'dondrunk1':1,'kimdrunk1':1,'bevid_a':37}.items():struct.pack_into('<i',legacy,80+lf.index(field)*4,val)
struct.pack_into('<i',legacy,220,1);struct.pack_into('<i',legacy,244,185);struct.pack_into('<i',legacy,268,1)
machine.mem_write(0x1120000,bytes(legacy));assert call('engine_migrate',address,0x1120000,296)==1
v=get();assert v.block==119 and v.line==0 and v.face[0]==1 and v.state.dondrunk1==1 and v.state.cur_day==1 and v.state.slotamount==1
assert call('engine_migrate',address,0x1120000,295)==0
expected=set(range(201,269))
assert expected<=seen2,('uncovered blocks',sorted(expected-seen2))
report={'shift_simulations':700,'recipe_pairs':len(recipes)**2,'day2_blocks':sorted(seen2),'legacy_migration_tested':True,'notes':'All 68 Day 2 blocks reached, including Mulan Tea. Runs may finish the shift or reach Game Over. ARM execution; console I/O not emulated.'}
(P/'day2-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
