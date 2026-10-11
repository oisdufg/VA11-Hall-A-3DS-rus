"""Compare daily payroll with the original game's bonuspaycheck schedule."""
from pathlib import Path
import json

base=Path(__file__).with_name('verify_day1.py')
exec(base.read_text(encoding='utf8').split('checks=[]')[0])

bonuses={1:500,2:300,3:300,4:400,5:300,7:500,8:300,9:300,10:500,
         11:300,12:300,14:300,15:300,16:300,17:300,18:600}
checks=0
for day in range(1,20):
    for mistakes in (0,1,6,7):
        v=View();v.state.cur_day=day;v.state.cash=1255;v.state.tips=180
        v.state.mistakes=mistakes;v.mode=2;v.paidDay=day-1;put(v)
        call('engine_settle',address)
        result=get()
        expected=0 if day in (6,13) else (1255*max(0,6-mistakes)*5+18000+(bonuses.get(day,0)+(500 if mistakes==0 else 0))*100)
        assert (result.walletCents,result.lastPayCents,result.paidDay)==(expected,expected,day if expected else day-1),(day,mistakes,result.walletCents,expected)
        call('engine_settle',address)
        assert get().walletCents==expected,(day,mistakes,'duplicate pay')
        checks+=2

report={'passed':True,'checks':checks,'days':'1-19','description':'Commission, tips, flawless pay, daily bonuses, days off, once-only settlement','hardware_tested':False}
(P/'finance-test-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
