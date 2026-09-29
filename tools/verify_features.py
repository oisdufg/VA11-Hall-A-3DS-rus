from verify_menu import *
import struct

def initial(day=1,client=1,stage=4,errors=0):
 put(View());call('engine_start',address,1);v=get()
 v.state.cur_day=day;v.state.cur_client=client;v.state.cur_stage=stage;v.mode=1;v.cheapErrors=errors
 return v

def pour(v,name,size='normal'):
 r=next(r for r in recipes if r['id']==name and r['size']==size and (name not in ('srush','sstar','gpunch') or r['alcohol']=='no'))
 v.mixer=Mixer();v.mixer.amount[:]=r['amount'];v.mixer.ice=r['ice'];v.mixer.aged=r['aged'];v.mixer.blended=r['blended'];v.mixer.ready=True
 put(v);call('engine_serve',address);return get()

# First two errors do not fail, the third cheap incorrect paid drink does.
for day,client,stage,ending in [(1,1,4,301),(2,1,4,305),(2,4,8,301),(3,1,3,304),(3,3,2,301),(4,1,3,301)]:
 v=initial(day,client,stage)
 for count in (1,2,3):
  v.mode=1;v.state.cur_client=client;v.state.cur_stage=stage
  v=pour(v,'srush')
  assert v.cheapErrors==count and bool(v.failed)==(count==3),(day,client,stage,count,v.cheapErrors,v.failed)
 assert v.block==ending and v.mode==0
 assert call('engine_can_save',address)==0
 snapshot(v,f'gameover-day{day}-client{client}')
 for i in range(80):
  if get().mode==6:break
  assert call('engine_advance_checkpoint',address)==0
  assert call('engine_can_save',address)==0
 else:raise AssertionError('Game Over dialogue failed to finish')
 snapshot(get(),f'gameover-end{ending}')
 call('menu_init',ui,1)
 assert action(16)==3, 'Continue after failure must reload safe checkpoint'
 assert get().failed, 'Menu must not resume failed run in memory'
# Correct paid order clears; incorrect expensive order leaves queue untouched.
v=pour(initial(errors=2),'beer');assert v.cheapErrors==0 and not v.failed
v=pour(initial(2,4,8,2),'moblast');assert v.cheapErrors==2 and not v.failed
# Tutorial and unpaid Ingram orders do not contribute to Game Over.
v=pour(initial(1,0,2,2),'sstar');assert v.cheapErrors==2 and not v.failed
v=pour(initial(1,2,2,2),'sstar');assert v.cheapErrors==2 and not v.failed
# End of shift before break clears queue (Day 1 client -1).
v=initial();v.state.cur_client=-1;v.state.cur_stage=1;v.cheapErrors=2
# Locate a real page that enters the break through the controller.
put(View());call('engine_start',address,1)
for i in range(1200):
 v=get()
 if v.mode==3:assert v.cheapErrors==0;break
 if v.mode==1:
  # Use correct known route already verified by the main suite.
  requested={3:'beer',4:'beer',5:'beer',7:'beer',6:'gpunch',8:'gpunch',9:'pdriver',10:'fweaver',11:'moblast',12:'btini',13:'btini',14:'srush',15:'pwman',16:'btini',174:'beer'}
  name=requested[v.state.orders];size='big' if v.state.orders in (3,4,6,8) else 'normal'
  pour(v,name,size)
 elif v.mode==7:call('engine_finish_jukebox',address)
 else:
  v.cheapErrors=2;put(v);call('engine_advance_checkpoint',address)
else:raise AssertionError('No break reached')
# Two-drink orders count at most once; storing the first drink counts nothing.
v=initial(2,2,7,2);v.state.slotamount=2
v=pour(v,'sstar');assert v.cheapErrors==2 and not v.failed and v.state.heldRecipe
v=pour(v,'sstar');assert v.cheapErrors==3 and v.failed and v.block==305
v=initial(2,2,7,2);v.state.slotamount=2
v=pour(v,'scloud','big');v=pour(v,'gpunch');assert v.cheapErrors==0 and not v.failed
# Tea is poured directly, selects the original Miki response and resets errors.
v=initial(2,4,2,2);v.overlay=1;put(v);call('engine_pour_special',address,json.loads((P/'generated/day1-metadata.json').read_text(encoding='utf8'))['tokens']['tea']);v=get()
assert v.overlay==0 and v.mixer.ready and sum(v.mixer.amount)==0
call('engine_serve',address);v=get();assert v.block==251 and v.state.rightdrink and v.cheapErrors==0
snapshot(v,'mulan-tea-response')
v.overlay=1;v.recipe=25;put(v);snapshot(v,'mulan-tea-book')
# Anna is triggered by the original script tag and expires after 100 frames at 30 Hz.
put(View());call('engine_start',address,1);v=get();v.mode=2;put(v);call('engine_next_day',address);v=get();v.mode=0;v.now=10000;put(v)
for i in range(1300):
 v=get()
 if v.annaUntil:
  assert v.annaUntil==13334;snapshot(v,'anna-tv')
  v.now=13333;put(v);call('engine_tick',address);assert get().annaUntil
  v=get();v.now=13334;put(v);call('engine_tick',address);assert not get().annaUntil
  break
 if v.mode==1:
  want={17:'beer',18:'mablast',19:'gpunch',20:'pwman',21:'moblast',23:'mablast',24:'tea',25:'bfairy',26:'gpunch'}
  name=want.get(v.state.orders,'gpunch' if v.state.heldRecipe else 'scloud')
  size='big' if v.state.orders==22 and not v.state.heldRecipe else next(r['size'] for r in recipes if r['id']==name)
  pour(v,name,size)
 elif v.mode==7:call('engine_finish_jukebox',address)
 else:call('engine_advance_checkpoint',address)
else:raise AssertionError('Anna tag never triggered')
# Preserve 0.4.1's 432-byte save prefix, initialize new fields safely.
v=initial(2,4,2);v.mode=0;v.state.dondrunk1=1;v.face[0]=1
legacy=bytes(v)[:80]+bytes(v.state)[:240]+bytes(v.visible)[:36]+bytes(v.position)[:36]+bytes(v.face)[:36]+bytes(v.saveError.to_bytes(4,"little",signed=True));machine.mem_write(0x5120000,legacy)
assert call('engine_migrate',address,0x5120000,432)==1
m=get();assert m.state.dondrunk1==1 and m.face[0]==1 and m.block==v.block and not m.failed and not m.cheapErrors and not m.annaUntil
legacy5=legacy+(2).to_bytes(4,'little')+bytes(4)+(1234).to_bytes(8,'little')
machine.mem_write(0x5120000,legacy5);assert call('engine_migrate',address,0x5120000,448)==1
m=get();assert m.cheapErrors==2 and m.annaUntil==1234 and m.state.dondrunk1==1 and m.face[0]==1
assert C.sizeof(View)>448
assert call('engine_can_save',address)==1
report={'passed':True,'checks':['Both original Game Over scenes and safe-menu reload action','Three cheap wrong drinks; correct, expensive and unpaid cases','Break queue reset','Paired-order counting','Mulan Tea original block 251','Anna scripted TV appearance and expiry','432/448-byte legacy save migration','Save eligibility rejects every page of Game Over'],'hardware_tested':False}
(P/'features-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
