"""Check purchase-dependent order hints and the Day 4 automatic download."""
from pathlib import Path
import ctypes as C
import json

base=Path(__file__).with_name('verify_day1.py')
exec(base.read_text(encoding='utf8').split('checks=[]')[0])

assert C.sizeof(View)==1344
def first_order():
    v=get();v.mode=0;put(v)
    for _ in range(500):
        v=get()
        if v.mode==1:return v
        if v.mode==7:call('engine_finish_jukebox',address)
        else:
            assert v.mode in (0,3),(v.mode,v.block)
            call('engine_advance_checkpoint',address)
    raise AssertionError('No first order')

cases={2:12,3:16,5:11,7:5,8:18,9:13}
for day,item in cases.items():
    for owned in (False,True):
        put(View());call('engine_start',address,1)
        v=get();v.mode=2;v.state.cur_day=day-1;v.paidDay=day-1
        v.walletCents=200000;v.purchases=(1<<item) if owned else 0
        put(v);call('engine_next_day',address);v=get()
        assert v.state.cur_day==day and v.mode==5
        assert call('engine_focused',address)==int(owned)
        v=first_order()
        assert (v.state.orders>=1000)==(not owned),(day,owned,v.state.orders)
        assert call('engine_valid',address)==1

for cents,status,focused in ((80000,1,True),(79999,2,False)):
    put(View());call('engine_start',address,1)
    v=get();v.mode=2;v.state.cur_day=3;v.paidDay=3;v.walletCents=cents
    put(v);call('engine_next_day',address);v=get()
    assert v.state.cur_day==4 and v.day4Download==status
    assert v.walletCents==cents-(80000 if focused else 0)
    assert call('engine_focused',address)==int(focused)
    v=first_order()
    assert (v.state.orders>=1000)==(not focused)
    assert call('engine_valid',address)==1

put(View());call('engine_start',address,1)
v=get();v.state.cur_day=4;v.mode=5;v.walletCents=123000;v.purchases=0
raw=bytes(v)
old=raw[:80]+raw[80:516]
old+=raw[View.visible.offset:View.visible.offset+76]
old+=raw[View.position.offset:View.position.offset+76]
old+=raw[View.face.offset:View.face.offset+76]
old+=raw[View.saveError.offset:View.saveError.offset+12]+b'\0'*4
old+=raw[View.annaUntil.offset:View.annaUntil.offset+64]
assert len(old)==824
machine.mem_write(0x5120000,old)
assert call('engine_migrate',address,0x5120000,824)==1
assert get().day4Download==0 and get().walletCents==123000
call('engine_grandfather_shop',address)
assert get().day4Download==1 and get().walletCents==123000
assert call('engine_valid',address)==1

report={'passed':True,'days':[2,3,4,5,7,8,9],
        'checks':['Purchased focus item restores order hints','Missing item shows distraction hints',
                  'Day 4 automatic $800 charge','Insufficient funds cause Day 4 distraction',
                  '824-byte legacy save migrates without another charge'],
        'save_bytes':C.sizeof(View),'hardware_tested':False}
(P/'distraction-test-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
