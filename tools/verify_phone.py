"""Check late phone pages in the compiled ARM build."""
from pathlib import Path
import ctypes as C
import json

base=Path(__file__).with_name('verify_day1.py')
exec(base.read_text(encoding='utf8').split('checks=[]')[0])

class Menu(C.LittleEndianStructure):
    _fields_=[(name,C.c_int32) for name in ('screen','selection','app','article','scroll','hasSave','notice')]

menu_address=0x5110000
forum_offsets=(0,0,0,3,4,7,7,10,11,12,13,14,15,15,16,17,18,19,19,20)
miki_offsets=(0,0,0,0,0,0,0,0,1,1,1,1,1,2,2,2,2,2,3,3)
checks=0
for day in range(1,20):
    for app in (0,1,2):
        for article in range(3):
            v=View();v.state.cur_day=day;put(v)
            u=Menu();u.app=app;u.article=article
            machine.mem_write(menu_address,bytes(u))
            if app==0:
                index=3*((18 if day==19 else day)-1)+article+1
                # Days 2-4 can select news branches; test their default pages.
                expected={2:(4,5,6),3:(7,8,9),4:(10,11,12)}.get(day)
                if expected:index=expected[article]
                name=f'home_news{index}'
            elif app==1:name=f'home_forum{forum_offsets[day]+article+1}'
            else:name=f'home_miki{miki_offsets[day]+article+1}'
            assert call('menu_phone_page',address,menu_address)==symbols[name],(day,app,article,name)
            checks+=1

v=View();v.state.cur_day=5;v.state.streamdrunk1=1;put(v)
u=Menu();u.app=1;u.article=1;machine.mem_write(menu_address,bytes(u))
assert call('menu_phone_page',address,menu_address)==symbols['home_forum24']

report={'passed':True,'checks':checks+1,'description':'All 19 days, three phone apps, three articles, and alternate forum thread','hardware_tested':False}
(P/'phone-test-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
