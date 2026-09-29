"""Exercise Day 5 on the actual ARM engine, including migration and special drinks."""
from verify_day1 import *
import struct
tokens=json.loads((P/'generated/day1-metadata.json').read_text(encoding='utf8'))['tokens']
assert C.sizeof(Mixer)==40 and C.sizeof(View)==760 and View.walletCents.offset==728
seen5=set();faces5=set();done=0;effects=set();orders=set();jukeboxes=0
want={47:'rum',48:'bfairy',49:'beer',50:'cvelvet',51:'fweaver',52:'abs',53:'beer',54:'btini',55:'srush',56:'srush',57:'fed'}
def pour(v,r,seventeen=False):
 v.mixer=Mixer();v.mixer.amount[:]=r['amount'];v.mixer.ice=r['ice'];v.mixer.aged=r['aged'];v.mixer.blended=r['blended'];v.mixer.ready=True
 if seventeen:
  assert r['optional'] and sum(r['amount'])<=17
  v.mixer.amount[4]+=17-sum(r['amount'])
 put(v)
 if r['id'] in ('rum','abs','fed','tea'):call('engine_pour_special',address,tokens[r['id']])
 call('engine_serve',address)
for run in range(1200):
 put(View());call('engine_start',address,1);v=get();v.mode=2;v.state.cur_day=4
 v.state.stel1=tokens['right' if run&1 else 'wrong'];v.state.stel2=tokens['right' if run&1 else 'wrong']
 v.state.streamdrunk1=(run>>1)&1;v.state.almadrunk1=(run>>2)&1;v.walletCents=123450;v.purchases=4096;v.paidDay=4
 put(v);call('engine_next_day',address);v=get()
 assert v.mode==5 and v.block==601 and v.walletCents==123450 and v.purchases==4096
 v.mode=0;put(v)
 for step in range(2000):
  v=get();seen5.add(v.block);assert call('engine_valid',address)==1,(run,v.block,v.mode)
  for a in (6,15,16):
   if v.visible[a] and (a,v.face[a]) not in faces5:
    faces5.add((a,v.face[a]));snapshot(v,f'day5-actor{a}-face{v.face[a]}')
  if v.bang:effects.add('bang')
  if v.crash:effects.add('crash')
  if v.shakeUntil:effects.add('shake')
  if v.mode in (2,6):
   if v.mode==2:
    done+=1;assert v.paidDay==5 and v.walletCents>=123450
    old=bytes(v);call('engine_settle',address);assert bytes(get())==old
   if run<8:assert v.mode==2,(run,'golden path failed')
   break
  if v.mode==7:jukeboxes+=1;call('engine_finish_jukebox',address);continue
  if v.mode in (0,3):
   checkpoint=call('engine_advance_checkpoint',address);assert checkpoint==int(get().mode==2);continue
  assert v.mode==1,(run,step,v.block,v.mode)
  orders.add(v.state.orders)
  available=[r for r in recipes if r['id'] not in ('abs','rum') or call('engine_extra_available',address,tokens[r['id']])]
  correct=run<8 or rng.random()<0.7
  if correct:
   r=next(r for r in available if r['id']==want[v.state.orders] and r['size']=='normal' and (v.state.orders!=55 or r['alcohol']=='no'))
  else:r=rng.choice(available)
  pour(v,r,correct and v.state.orders==56)
 else:raise AssertionError(('Day 5 loop',run,get().block))
assert set(range(601,662))<=seen5,('uncovered',sorted(set(range(601,662))-seen5))
assert orders==set(range(47,58)) and effects=={'bang','crash','shake'}
# Game Over protects saves for early shift, Dorothy, and Virgilio.
for client,stage,drink,ending in [(1,10,'srush',302),(2,5,'fwater',302),(3,2,'srush',301)]:
 put(View());call('engine_start',address,1);v=get();v.state.cur_day=5;v.state.cur_client=client;v.state.cur_stage=stage;v.cheapErrors=2;v.mode=1
 r=next(r for r in recipes if r['id']==drink and r['size']=='normal');pour(v,r)
 assert get().failed and get().block==ending and call('engine_can_save',address)==0
# Authentic version 8 layout with wallet, owned decorations and old actor indices.
put(View());call('engine_start',address,1);v=get();v.state.cur_day=4;v.block=501;v.face[1]=3
legacy=bytes(v)[:80]+bytes(v.state)[:336]+bytes(v.visible)[:60]+bytes(v.position)[:60]+bytes(v.face)[:60]+struct.pack('<iii',0,1,0)+struct.pack('<Q5iI4i',0,12,2,1,1,3,0,456789,4096,3,78000)
assert len(legacy)==656
machine.mem_write(0x5120000,legacy);assert call('engine_migrate',address,0x5120000,656)==1
v=get();assert v.walletCents==456789 and v.purchases==4096 and v.paidDay==3 and v.lastPayCents==78000 and v.face[1]==3 and v.musicTrack==12
assert v.state.alma4==0 and v.mixer.special==0 and v.visible[16]==0
report={'passed':True,'shift_simulations':1200,'completed_shifts':done,'day5_blocks':sorted(seen5),'orders':sorted(orders),'effects':sorted(effects),'jukebox_prompts':jukeboxes,'save_bytes':760,'checks':['Golden routes with and without Stella rum gift','All story blocks and order hints','17 actual ingredients and bottled drinks','Day 5 Game Over and safe saves','Once-only payout','Version 8 shop wallet/ownership migration'],'hardware_tested':False}
(P/'day5-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
