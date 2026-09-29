"""Shop, payroll and save-layout checks against the actual ARM build."""
from verify_menu import *

assert C.sizeof(View)==760 and View.walletCents.offset==728
catalog=json.loads((P/'generated/shop.json').read_text())
assert len(catalog)==16
# Salary matches original commission, tips, flawless bonus and daily bonus.
for day,bonus in enumerate((500,300,300,400),1):
 for errors in range(9):
  put(View());call('engine_start',address,1);v=get()
  v.state.cur_day=day;v.state.cash=1255;v.state.tips=180;v.state.mistakes=errors;v.mode=2;put(v)
  call('engine_settle',address)
  expected=1255*max(0,6-errors)*5+18000+(bonus+(500 if errors==0 else 0))*100
  assert get().walletCents==expected and get().paidDay==day
  before=bytes(get());call('engine_settle',address);assert bytes(get())==before
  if day<4:
   call('engine_next_day',address);assert get().walletCents==expected and get().state.cash==0
# Legacy v7 save preserves story/music and starts with no invented historical income.
put(View());call('engine_start',address,1);v=get();v.musicTrack=12;v.state.cur_day=3
legacy=bytes(v)[:80]+bytes(v.state)[:336]+bytes(v.visible)[:60]+bytes(v.position)[:60]+bytes(v.face)[:60]+bytes(v)[680:692]+bytes(v)[696:724]+b'\0'*4;machine.mem_write(0x5120000,legacy)
assert call('engine_migrate',address,0x5120000,640)==1
assert get().musicTrack==12 and get().state.cur_day==3 and get().walletCents==0 and get().purchases==0
# Every decoration: insufficient funds, exact funds, duplicate, wrong mode and index.
for i,item in enumerate(catalog):
 v=get();v.mode=5;v.purchases=0;v.walletCents=item['price']*100-1;put(v)
 assert call('engine_buy',address,i)==0
 v.walletCents+=1;put(v);assert call('engine_buy',address,i)==1
 assert get().walletCents==0 and get().purchases==1<<i
 assert call('engine_buy',address,i)==0
assert call('engine_buy',address,16)==0 and call('engine_buy',address,-1)==0
v=get();v.mode=0;v.walletCents=10000000;v.purchases=0;put(v)
assert call('engine_buy',address,0)==0
v.failed=1;v.mode=5;put(v);assert call('engine_buy',address,0)==0
# UI: confirmation, cancellation, selected-item changes, touch, sold/out-of-funds.
v.failed=0;v.state.cur_day=2;v.paidDay=1;put(v);call('menu_init',ui,1);action(16)
action(1);assert getmenu().selection==3
action(16);assert getmenu().screen==11
shot('shop-empty');original=bytes(get());action(16);assert getmenu().notice==1 and bytes(get())==original
shot('shop-confirm');action(32);assert getmenu().screen==11 and getmenu().notice==0
action(16);action(2);assert getmenu().notice==0 and not get().purchases
action(16);assert getmenu().notice==1
assert action(16)==0 and get().purchases==2
action(16);assert getmenu().notice==4
v=get();v.walletCents=0;put(v);action(2);action(16);assert getmenu().notice==3
shot('shop-no-funds')
v.walletCents=10000000;put(v)
action(256,50,48);assert getmenu().selection==0 and getmenu().notice==1
action(256,50,48);assert get().purchases==3
for i in range(16):call('engine_buy',address,i)
shot('shop-owned');action(32);assert getmenu().screen==2
shot('shop-decorated-home');saved=bytes(get());assert call('engine_valid',address)==1
# New-format payload round trip and transition retain wallet and ownership.
put(View.from_buffer_copy(saved));assert bytes(get())==saved
u=getmenu();u.selection=1;machine.mem_write(ui,bytes(u));action(16)
assert get().mode==0 and get().purchases==65535
assert get().walletCents==View.from_buffer_copy(saved).walletCents
# Starting a new game clears purchases and wallet; corrupt economic fields rejected.
call('engine_start',address,1);assert get().purchases==0 and get().walletCents==0
for field,value in [('walletCents',-1),('purchases',1<<16),('paidDay',5),('lastPayCents',-1)]:
 v=get();setattr(v,field,value);put(v);assert call('engine_valid',address)==0;call('engine_start',address,1)
report={'passed':True,'decorations':16,'save_bytes':C.sizeof(View),'checks':['Original daily payroll with cents and once-only settlement','16 purchases: exact funds, insufficient funds, duplicate and eligibility guards','Confirmation/cancel/touch/selection changes','Room decoration rendering','640-byte migration and new payload round trip','New game and invalid economy fields'],'hardware_tested':False}
(P/'shop-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
