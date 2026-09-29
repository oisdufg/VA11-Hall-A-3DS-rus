"""Execute Day 3 on the actual ARM binary; no host reimplementation of rules."""
from verify_day1 import *

seen3=set();new_faces=set();endings=0
for run in range(800):
 put(View());call('engine_start',address,1);v=get();v.mode=2;v.state.cur_day=2
 for i,field in enumerate(('dondrunk1','dondrunk2','kimdrunk1','drunkmiki1','dorodrunk1')):setattr(v.state,field,(run>>i)&1)
 put(v);call('engine_next_day',address);v=get()
 assert v.mode==5 and v.state.cur_day==3 and v.block==401
 assert v.state.dondrunk2==((run>>1)&1)
 v.mode=0;put(v)
 for step in range(2200):
  v=get();seen3.add(v.block)
  assert v.mode!=4,('stuck',run,v.block,v.line,v.state.cur_client,v.state.cur_stage)
  assert call('engine_valid',address)==1,('invalid',run,v.block,v.line)
  for actor in (6,9,10):
   if v.visible[actor] and (actor,v.face[actor]) not in new_faces:
    snapshot(v,f'day3-actor{actor}-face{v.face[actor]}');new_faces.add((actor,v.face[actor]))
  if v.mode in (2,6):
   if run==0:assert v.mode==2
   if v.mode==2:endings+=1
   break
  if v.mode==7:
   call('engine_finish_jukebox',address);continue
  if v.mode in (0,3):
   checkpoint=call('engine_advance_checkpoint',address)
   assert checkpoint==int(get().mode==2),('save outside day end',v.block,v.line)
   continue
  assert v.mode==1
  if run==0 or (run%4==0 and rng.random()<0.7):
   wanted={27:'btouch',28:'scloud',29:'btini',30:'beer',31:'bjane',32:'pwman',33:'pman',34:'fweaver',35:'bfairy'}[v.state.orders]
   r=next(r for r in recipes if r['id']==wanted and (v.state.orders!=29 or r['size']=='big'))
  else:r=rng.choice(recipes)
  v.mixer=Mixer();v.mixer.amount[:]=r['amount'];v.mixer.ice=r['ice'];v.mixer.aged=r['aged'];v.mixer.blended=r['blended'];v.mixer.ready=True
  put(v);call('engine_serve',address)
 else:raise AssertionError(('loop',run,get().block))
 if run==0:print('Day 3 first complete shift:',step,'steps',flush=True)
# Block 12 has no rule; all three Donovan exits set stage 9, skipping block 30.
expected=set(range(401,475))-{412,430}
assert expected<=seen3,('uncovered Day 3 blocks',sorted(expected-seen3))
assert endings>0
report={'shift_simulations':800,'completed_shifts':endings,'day3_blocks':sorted(seen3),'unreachable_original_blocks':[412,430],'new_actor_faces':sorted(new_faces),'hardware_tested':False}
(P/'day3-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
