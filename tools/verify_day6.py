"""Exercise Day 6's day-off dialogue, beer branches and end-of-day save on ARM."""
from verify_day1 import *

tokens=json.loads((P/'generated/day1-metadata.json').read_text(encoding='utf8'))['tokens']
seen=set();completed=0
for beers in (0,2,4,6,9,12):
 for gift in (False,True):
  put(View());call('engine_start',address,1)
  v=get();v.mode=2;v.state.cur_day=5;v.paidDay=5
  v.walletCents=123450;v.purchases=8192
  v.state.stel1=v.state.stel2=tokens['right' if gift else 'wrong']
  put(v);call('engine_next_day',address);v=get()
  assert (v.state.cur_day,v.mode,v.block,v.day6Beers)==(6,5,701,0)
  assert (v.walletCents,v.purchases,v.paidDay)==(123450,8192,5)
  v.mode=0;put(v)
  for step in range(1800):
   v=get();seen.add(v.block)
   assert call('engine_valid',address)==1,(beers,gift,v.block,v.mode)
   assert call('engine_can_save',address)==1
   if v.block==701 and v.line==0 and beers==0 and not gift:snapshot(v,'day6-bar-opening')
   if v.block==702 and v.day6Beers==0:
    for _ in range(beers):call('engine_day6_drink',address)
    v=get();assert v.day6Beers==beers
    if beers==12:
     for _ in range(3):call('engine_day6_drink',address)
     assert get().day6Beers==12
    if beers==12 and gift:snapshot(v,'day6-apartment-beer')
   if v.mode==2:
    completed+=1
    assert v.block in (716,717,718)
    assert v.walletCents==123450 and v.paidDay==5 and v.day6Beers==beers
    assert v.state.jilldrunk1==int(beers==12)
    old=bytes(v);call('engine_settle',address);assert bytes(get())==old
    assert call('engine_advance_checkpoint',address)==0
    break
   assert v.mode==0,(beers,gift,v.block,v.mode)
   checkpoint=call('engine_advance_checkpoint',address)
   if get().mode==2:assert checkpoint==1
  else:raise AssertionError(('Day 6 did not finish',beers,gift,get().block,get().state.cur_stage))
assert set(range(701,719))<=seen,sorted(set(range(701,719))-seen)
assert completed==12
report={'passed':True,'day6_blocks':sorted(seen),'routes':completed,'beer_counts':[0,2,4,6,9,12],
        'checks':['All dialogue branches and Stella gift outcomes','Beer cap and saved count',
                  'Day 5 to Day 6 apartment transition','End-of-day checkpoint without shift pay',
                  'Wallet, purchases and save eligibility'], 'hardware_tested':False}
(P/'day6-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
