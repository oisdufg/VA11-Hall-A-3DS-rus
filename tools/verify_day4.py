"""Full Day 4 runs on the built ARM engine, including scripted jukebox stops."""
from verify_day1 import *
seen4=set();faces4=set();done=0;jukeboxes=0
want={36:'gpunch',37:'gtemple',38:'scloud',39:'btouch',40:'fweaver',41:'beer',42:'zstar',43:'btini',44:'gpunch',45:'mablast',46:'beer'}
tokens=json.loads((P/'generated/day1-metadata.json').read_text(encoding='utf8'))['tokens']
for run in range(1200):
 put(View());call('engine_start',address,1);v=get();v.mode=2;v.state.cur_day=3
 v.state.stel1=tokens['right' if run%2 else 'wrong'];v.state.stel2=tokens['right' if run%3 else 'wrong'];v.state.ingdrunk1=run%2
 put(v);call('engine_next_day',address);v=get();assert v.mode==5 and v.block==501 and v.state.cur_day==4
 v.mode=0;put(v)
 for step in range(2400):
  v=get();seen4.add(v.block)
  assert v.mode!=4 and call('engine_valid',address)==1,('invalid',run,v.block,v.line,v.mode,v.state.cur_client,v.state.cur_stage)
  for actor in (1,11,12,13,14):
   key=(actor,v.face[actor])
   if v.visible[actor] and key not in faces4:snapshot(v,f'day4-actor{actor}-face{v.face[actor]}');faces4.add(key)
  if v.mode in (2,6):
   if run==0:assert v.mode==2
   if v.mode==2:done+=1
   break
  if v.mode==7:
   jukeboxes+=1;call('engine_finish_jukebox',address);continue
  if v.mode in (0,3):
   result=call('engine_advance_checkpoint',address);assert result==int(get().mode==2)
   continue
  assert v.mode==1
  if run<12 or (run%3==0 and rng.random()<0.8):
   name=want[v.state.orders]
   if run in (1,3,5,7,9,11) and v.state.orders==42:name='fweaver'
   if run==1 and v.state.orders==42:name='beer'
   if run in (2,4,6,8,10) and v.state.orders==45:name='gpunch'
   r=next(r for r in recipes if r['id']==name and (v.state.orders!=39 or r['size']=='big') and (v.state.orders!=41 or run%2==0 or r['size']=='big') and (name!='fweaver' or r['size']=='big'))
  else:r=rng.choice(recipes)
  v.mixer=Mixer();v.mixer.amount[:]=r['amount'];v.mixer.ice=r['ice'];v.mixer.aged=r['aged'];v.mixer.blended=r['blended'];v.mixer.ready=True
  put(v);call('engine_serve',address)
 else:raise AssertionError(('loop',run,get().block,get().state.cur_stage))
 if run==0:print('Day 4 complete:',step,'steps',flush=True)
expected=set(range(501,573))
assert expected<=seen4,('uncovered Day 4 blocks',sorted(expected-seen4))
report={'shift_simulations':1200,'completed_shifts':done,'day4_blocks':sorted(seen4),'jukebox_stops':jukeboxes,'actor_faces':sorted(faces4),'hardware_tested':False}
(P/'day4-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
