from pathlib import Path
import re,json,textwrap,sys,struct,argparse
parser=argparse.ArgumentParser(description='Prepare Day 1 from the owner game and UndertaleModTool CodeEntries directory.')
parser.add_argument('game',type=Path)
parser.add_argument('decompiled',type=Path)
args=parser.parse_args()
P=Path(__file__).resolve().parents[1]; G=P/'generated'; D=args.decompiled
sys.path.insert(0,str(P/'tools'))
from prepare import GameData,cstr
from PIL import Image
game=args.game
day=(D/'gml_Script_day1control.gml').read_text();mix=(D/'gml_Script_mix1control.gml').read_text();drinks=(D/'gml_Script_drink_a.gml').read_text()
day2=(D/'gml_Script_day2control.gml').read_text();mix2=(D/'gml_Script_mix2control.gml').read_text()
day2=re.sub(r'choose\([^)]*\)', '1000+20*global.cur_day+((global.cur_client+global.cur_stage)%11)', day2).replace('distractioncheck()', 'focused')
day3=(D/'gml_Script_day3control.gml').read_text();mix3=(D/'gml_Script_mix3control.gml').read_text()
day3=re.sub(r'choose\([^)]*\)', '1000+20*global.cur_day+((global.cur_client+global.cur_stage)%11)', day3).replace('distractioncheck()', 'focused')
day4=(D/'gml_Script_day4control.gml').read_text();mix4=(D/'gml_Script_mix4control.gml').read_text()
day4=re.sub(r'choose\([^)]*\)', '1000+20*global.cur_day+((global.cur_client+global.cur_stage)%4)', day4).replace('distractioncheck()', 'focused')
day5=(D/'gml_Script_day5control.gml').read_text();mix5=(D/'gml_Script_mix5control.gml').read_text()
day5=re.sub(r'choose\([^)]*\)', '1000+20*global.cur_day+((global.cur_client+global.cur_stage)%11)', day5).replace('distractioncheck()', 'focused')
day7=(D/'gml_Script_day7control.gml').read_text();mix7=(D/'gml_Script_mix7control.gml').read_text()
day7=re.sub(r'choose\([^)]*\)', '1000+20*global.cur_day+((global.cur_client+global.cur_stage)%11)', day7).replace('distractioncheck()', 'focused')
day8=(D/'gml_Script_day8control.gml').read_text();mix8=(D/'gml_Script_mix8control.gml').read_text()
day8=re.sub(r'choose\([^)]*\)', '1000+20*global.cur_day+((global.cur_client+global.cur_stage)%11)', day8).replace('distractioncheck()', 'focused')
# Room 29 is the original break room. The 3DS scene stays in the bar;
# the Day 8 break is represented by its dialogue block and mode 3.
before,after=day8.split('\n    case 3:',1)
middle,tail=after.split('\n    case 4:',1)
day8=before+'\n    case 3:'+middle.replace('room == 29','1')+'\n    case 4:'+tail
day8=day8.replace('room == 29','0').replace('!instance_exists(296)','0').replace('!instance_exists(300)','0').replace('instance_create(x, y, 296);','return 0;').replace('instance_create(x, y, 300);','return 0;')
day8=day8.replace('instance_create(x, y, 308);','textbox_create(global.ch8, 51, 1);')
day9=(D/'gml_Script_day9control.gml').read_text();mix9=(D/'gml_Script_mix9control.gml').read_text()
day9=re.sub(r'choose\([^)]*\)', '1000+20*global.cur_day+((global.cur_client+global.cur_stage)%11)', day9).replace('distractioncheck()', 'focused')
day9=day9.replace('room == 29','1').replace('!instance_exists(300)','0').replace('instance_create(x, y, 300);','return 0;')
day9=day9.replace('instance_create(x, y, 308);','textbox_create(global.ch9, 47, 1);')
day10=(D/'gml_Script_day10control.gml').read_text();mix10=(D/'gml_Script_mix10control.gml').read_text()
day10=re.sub(r'choose\([^)]*\)', '1000+20*global.cur_day+((global.cur_client+global.cur_stage)%11)', day10).replace('distractioncheck()', 'focused')
day10=day10.replace('instance_create(x, y, 308);','textbox_create(global.ch10, 47, 1);')
day11=(D/'gml_Script_day11control.gml').read_text();mix11=(D/'gml_Script_mix11control.gml').read_text()
day11=re.sub(r'choose\([^)]*\)', '1000+20*global.cur_day+((global.cur_client+global.cur_stage)%11)', day11).replace('distractioncheck()', 'focused')
day11=day11.replace('instance_create(x, y, 308);','textbox_create(global.ch11, 51, 1);')
day12=(D/'gml_Script_day12control.gml').read_text();mix12=(D/'gml_Script_mix12control.gml').read_text()
day12=re.sub(r'choose\([^)]*\)', '1000+20*global.cur_day+((global.cur_client+global.cur_stage)%11)', day12).replace('distractioncheck()', 'focused')
# The original pause switches rooms. Our fixed bar scene plays the break
# dialogue directly, then resumes in the bar after it.
day12=day12.replace('room == 29','0',1).replace('!instance_exists(296)','0',1).replace('instance_create(x, y, 296);','return 0;',1)
day12=day12.replace('room == 29','1',1).replace('!instance_exists(300)','0',1).replace('instance_create(x, y, 300);','return 0;',1)
day12=day12.replace('room == 29','0').replace('!instance_exists(296)','0').replace('instance_create(x, y, 296);','return 0;')
day12=day12.replace('instance_create(x, y, 308);','textbox_create(global.ch12, 49, 1);')
day14=(D/'gml_Script_day14control.gml').read_text();mix14=(D/'gml_Script_mix14control.gml').read_text()
day14=re.sub(r'choose\([^)]*\)', '1000+20*global.cur_day+((global.cur_client+global.cur_stage)%11)', day14).replace('distractioncheck()', 'focused')
day15=(D/'gml_Script_day15control.gml').read_text();mix15=(D/'gml_Script_mix15control.gml').read_text()
day15=re.sub(r'choose\([^)]*\)', '1000+20*global.cur_day+((global.cur_client+global.cur_stage)%11)', day15).replace('distractioncheck()', 'focused')
day15=day15.replace('instance_create(x, y, 308);','textbox_create(global.ch15, 48, 1);')
day16=(D/'gml_Script_day16control.gml').read_text();mix16=(D/'gml_Script_mix16control.gml').read_text()
day16=re.sub(r'choose\([^)]*\)', '1000+20*global.cur_day+((global.cur_client+global.cur_stage)%11)', day16).replace('distractioncheck()', 'focused')
# The final room transition is the end-of-day result in the 3DS port.
day17=(D/'gml_Script_day17control.gml').read_text();mix17=(D/'gml_Script_mix17control.gml').read_text()
day17=re.sub(r'choose\([^)]*\)', '1000+20*global.cur_day+((global.cur_client+global.cur_stage)%11)', day17).replace('distractioncheck()', 'focused')
day18=(D/'gml_Script_day18control.gml').read_text();mix18=(D/'gml_Script_mix18control.gml').read_text()
day18=re.sub(r'choose\([^)]*\)', '1000+20*global.cur_day+((global.cur_client+global.cur_stage)%4)', day18).replace('distractioncheck()', 'focused')
# The original break moves to another room; the 3DS bar displays its dialogue in place.
day18=day18.replace('room == 29','0',1).replace('!instance_exists(296)','0',1).replace('instance_create(x, y, 296);','return 0;',1)
day18=day18.replace('room == 29','1',1).replace('!instance_exists(300)','0',1).replace('instance_create(x, y, 300);','return 0;',1)
day19=(D/'gml_Script_day19control.gml').read_text();mix19=(D/'gml_Script_mix19control.gml').read_text()
day19=re.sub(r'choose\([^)]*\)', '1000+20*global.cur_day+((global.cur_client+global.cur_stage)%4)', day19).replace('distractioncheck()', 'focused')
day19=day19.replace('!instance_exists(313)','1').replace('instance_create(x, y, 313);','return -3;')
tokens=sorted(set(re.findall(r'"([^"\n]*)"',day+mix+day2+mix2+day3+mix3+day4+mix4+day5+mix5+day7+mix7+day8+mix8+day9+mix9+day10+mix10+day11+mix11+day12+mix12+day14+mix14+day15+mix15+day16+mix16+day17+mix17+day18+mix18+day19+mix19+drinks)+['doro','dana','alma','gil','dog']))
tok=json.loads((G/'v8-metadata.json').read_text(encoding='utf8'))['tokens']
for v in tokens:
 if v not in tok:tok[v]=max(tok.values())+1
(G/'tokens.h').write_text('#pragma once\n'+''.join(f'#define TOK_{k} {v}\n' for k,v in tok.items() if re.fullmatch('[a-z]+',k)))
def token(v):return str(tok[v])
fields=sorted(set(re.findall(r'global\.(\w+)',day+mix+day2+mix2+day3+day4+mix3+mix4+day5+mix5+day7+mix7+day8+mix8+day9+mix10+day10+mix11+day11+day12+mix12+day14+mix14+day15+mix15+day16+mix16+day17+mix17+day18+mix18+day19+mix19))-{'ch1','ch2','ch3','ch4','ch5','ch7','ch8','ch9','ch10','ch11','ch12','ch14','ch15','ch16','ch17','ch18','ch19','tuto'}-{f'odstr{i}' for i in range(200)}-{f'distract{i}' for i in range(200)})
fields+=['lightdl']
fields+=['housedl']
fields+=['dogpick','pickdare']
fields+=['shouldpay','rightdrink','big_able','tipping','cash','tips','mistakes','juke','mix','drinkscore_a']
fields+=['cur_day','heldRecipe','heldK','heldIce','rightdrink1','rightdrink2','big_able1','big_able2']
legacy=json.loads((G/'v9-state-fields.json').read_text())
v13_extra=['art3','art4','art5','brian1','brian2','ing4','ing5','ingdrunk2','jamie4','jamie5','jamie6','jilldrunk1','mod_e','rad1','rad2','sei5','sei6','stel4','stel5','virgilio3']
v14_extra=['dorodrink5','dorodrink6','dorodrunk2','mario1','mario2','mario3','norma1']
v15_extra=['kim4','kim5','sei7','stel6','stel7','stel8','virgilio4','virgilio5','virgilio6']
v16_extra=['alma7','alma8','db4','db5','jill1','jill2','nacho3']
v17_extra=['dorodrink7','dorodrink9','lightdl','sei8','sei9']
v18_extra=['dogpick','pickdare']
v19_extra=['art6','art7','ft_any','lexi1','lexi2','truevirgilio1','truevirgilio2','truevirgilio3']
fields=legacy+v13_extra+v14_extra+v15_extra+v16_extra+v17_extra+v18_extra+v19_extra+sorted(set(fields)-set(legacy)-set(v13_extra)-set(v14_extra)-set(v15_extra)-set(v16_extra)-set(v17_extra)-set(v18_extra)-set(v19_extra))
v20_fields=json.loads((G/'v20-state-fields.json').read_text())
fields=v20_fields+sorted(set(fields)-set(v20_fields))
v21_fields=json.loads((G/'v21-state-fields.json').read_text())
fields=v21_fields+sorted(set(fields)-set(v21_fields))
v22_fields=json.loads((G/'v22-state-fields.json').read_text())
fields=v22_fields+sorted(set(fields)-set(v22_fields))
v23_fields=json.loads((G/'v23-state-fields.json').read_text())
fields=v23_fields+sorted(set(fields)-set(v23_fields))
(G/'state.h').write_text('#pragma once\ntypedef struct {\n'+''.join('int '+f+';\n' for f in fields)+'} State;\n')
(G/'state-fields.json').write_text(json.dumps(fields))
def translate(s):
 s=re.sub(r'textbox_create\(global\.(ch1|ch2|ch3|ch4|ch5|ch7|ch8|ch9|ch10|ch11|ch12|ch14|ch15|ch16|ch17|ch18|ch19|tuto), (\d+), 1\);',lambda m:'return '+str(int(m[2])+({'tuto':0,'ch1':100,'ch2':200,'ch3':400,'ch4':500,'ch5':600,'ch7':800,'ch8':900,'ch9':1000,'ch10':1100,'ch11':1200,'ch12':1300,'ch14':1500,'ch15':1600,'ch16':1700,'ch17':1800,'ch18':1900,'ch19':2000}[m[1]]))+';',s)
 s=re.sub(r'instance_create\(x, y, (305|308)\);',lambda m:'return '+('-2' if m[1]=='305' else '-3')+';',s)
 s=re.sub(r'mixertips_double\((\d+), (\d+), (\d+), (\d+), (\d+), (\d+)\);',lambda m:f's->shouldpay={m[1]};s->rightdrink1={m[2]};s->rightdrink2={m[3]};s->big_able1={m[4]};s->big_able2={m[5]};s->tipping={m[6]};',s)
 s=re.sub(r'mixertips\((\d+), (\d+), (\d+), (\d+)\);',lambda m:f's->shouldpay={m[1]};s->rightdrink={m[2]};s->big_able={m[3]};s->tipping={m[4]};',s)
 s=re.sub(r'global.odstr(\d+)',r'\1',s)
 s=re.sub(r'global\.(\w+)',r's->\1',s)
 s=re.sub(r'"([^"\n]*)"',lambda m:token(m[1]),s).replace('exit;','return 0;')
 # Each outer case has its own stage switch; preserve no-match as idle.
 s=re.sub(r'\n    case ',r'\n    case ',s)
 s=s.replace('\n    case 0:', '\n        return 0;\n    case 0:')
 for i in range(1,6):s=s.replace(f'\n    case {i}:',f'\n        return 0;\n    case {i}:')
 s=re.sub(r'\{\n        return 0;\n    case (\d+):',r'{\n    case \1:',s)
 s=s.replace('\n            case ', '\n                /* fall through */\n            case ')
 return s+'\nreturn 0;'
# Day 6 is a day off. Its original controller switches rooms between stages,
# but has no mixer rule. These are its story branches after each room transition.
day6_rule='''static int day6_rule(State *s,int beers){
switch(s->cur_stage){
case 1:return 701;
case 2:return 702;
case 3:return 703;
case 4:return s->stel1==TOK_right && s->stel2==TOK_right?705:704;
case 5:return 706;
case 6:return beers>=2?707:708;
case 7:return 709;
case 8:return beers>=4?710:711;
case 9:return 712;
case 10:return beers>=6?713:714;
case 11:return 715;
case 12:if(beers==12){s->jilldrunk1=1;return 716;}return beers>8?717:718;
case 13:return -3;
default:return 0;
}}
'''
(G/'rules.h').write_text('static int day_rule(State *s){\n'+translate(day)+'\n}\nstatic int mix_rule(State *s){\n'+translate(mix)+'\n}\nstatic int day2_rule(State *s,int focused){\n'+translate(day2)+'\n}\nstatic int mix2_rule(State *s){\n'+translate(mix2)+'\n}\nstatic int day3_rule(State *s,int focused){\n'+translate(day3)+'\n}\nstatic int mix3_rule(State *s){\n'+translate(mix3)+'\n}\nstatic int day4_rule(State *s,int focused){\n'+translate(day4)+'\n}\nstatic int mix4_rule(State *s){\n'+translate(mix4)+'\n}\nstatic int day5_rule(State *s,int focused){\n'+translate(day5)+'\n}\nstatic int mix5_rule(State *s){\n'+translate(mix5)+'\n}\n'+day6_rule+'static int day7_rule(State *s,int focused){\n'+translate(day7)+'\n}\nstatic int mix7_rule(State *s){\n'+translate(mix7)+'\n}\nstatic int day8_rule(State *s,int focused){\n'+translate(day8)+'\n}\nstatic int mix8_rule(State *s){\n'+translate(mix8)+'\n}\nstatic int day9_rule(State *s,int focused){\n'+translate(day9)+'\n}\nstatic int mix9_rule(State *s){\n'+translate(mix9)+'\n}\nstatic int day10_rule(State *s,int focused){\n'+translate(day10)+'\n}\nstatic int mix10_rule(State *s){\n'+translate(mix10)+'\n}\n')
(G/'rules.h').write_text((G/'rules.h').read_text()+'static int day11_rule(State *s,int focused){\n'+translate(day11)+'\n}\nstatic int mix11_rule(State *s){\n'+translate(mix11)+'\n}\n')
(G/'rules.h').write_text((G/'rules.h').read_text()+'static int day12_rule(State *s,int focused){\n'+translate(day12)+'\n}\nstatic int mix12_rule(State *s){\n'+translate(mix12)+'\n}\n')
day13_rule='''static int day13_rule(State *s){
switch(s->cur_client){
case 1:
    if(s->cur_stage==1)return 1426;
    if(s->cur_stage==2){s->cur_client=2;s->cur_stage=1;return 1401;}
    return 0;
case 2:
    switch(s->cur_stage){
    case 2:case 4:case 7:return -4;
    case 3:return 1407;
    case 5:
        if(s->pickdare==TOK_doro)return s->dogpick?1411:1410;
        if(s->pickdare==TOK_alma)return s->dogpick?1414:1415;
        if(s->pickdare==TOK_gil)return s->dogpick?1417:1418;
        return 0;
    case 6:return 1419;
    case 8:return 1425;
    case 9:s->cur_client=3;s->cur_stage=1;return 1427;
    default:return 0;
    }
case 3:
    if(s->cur_stage==10)return -3;
    return 0;
default:return 0;
}}
'''
(G/'rules.h').write_text((G/'rules.h').read_text()+day13_rule)
(G/'rules.h').write_text((G/'rules.h').read_text()+'static int day14_rule(State *s,int focused){\n'+translate(day14)+'\n}\nstatic int mix14_rule(State *s){\n'+translate(mix14)+'\n}\n')
(G/'rules.h').write_text((G/'rules.h').read_text()+'static int day15_rule(State *s,int focused){\n'+translate(day15)+'\n}\nstatic int mix15_rule(State *s){\n'+translate(mix15)+'\n}\n')
(G/'rules.h').write_text((G/'rules.h').read_text()+'static int day16_rule(State *s,int focused){\n'+translate(day16)+'\n}\nstatic int mix16_rule(State *s){\n'+translate(mix16)+'\n}\n')
(G/'rules.h').write_text((G/'rules.h').read_text()+'static int day17_rule(State *s,int focused){\n'+translate(day17)+'\n}\nstatic int mix17_rule(State *s){\n'+translate(mix17)+'\n}\n')
(G/'rules.h').write_text((G/'rules.h').read_text()+'static int day18_rule(State *s,int focused){\n'+translate(day18)+'\n}\nstatic int mix18_rule(State *s){\n'+translate(mix18)+'\n}\n')
(G/'rules.h').write_text((G/'rules.h').read_text()+'static int day19_rule(State *s,int focused){\n'+translate(day19)+'\n}\nstatic int mix19_rule(State *s){\n'+translate(mix19)+'\n}\n')
# Original ingredient conditions and classification, including size and optional alcohol.
recipes=[]
for m in re.finditer(r'else if \((global.mod_aa[^\n]+)\)\s*\{([\s\S]*?global.drinkscore_a = (\d+);)',drinks):
 cond,body,price=m.groups(); props=dict(re.findall(r'global\.(\w+) = "([^"]*)";',body))
 amounts=[];optional=False
 for letter in 'abcde':
  a=re.search(r'global.mod_'+letter+r'a (==|>=) (\d+)',cond);assert a,cond
  amounts.append(int(a[2]));optional|=a[1]=='>='
 recipes.append(dict(name=props['bev_a'],id=props['bevid_a'],flavor=props['flavor_a'],kind=props['kind_a'],size=props['drinksize_a'],alcohol=props['alcohol_a'],price=int(price),amount=amounts,optional=optional,ice='!global.otr_a' not in cond,aged='!global.age_a' not in cond,blended='!global.mixed_a' in cond))
assert len(recipes)>50,len(recipes)
# Bottled extra: the shop controls Mulan Tea availability at runtime.
recipes.append(dict(name='Муланский чай',id='tea',flavor='sweet',kind='classic',size='normal',alcohol='yes',price=500,amount=[0]*5,optional=False,ice=False,aged=False,blended=False))
for name,title,flavor in [('rum','Ром','bitter'),('abs','Абсент','sour'),('fed','Plumfume','bubbly')]:
 recipes.append(dict(name=title,id=name,flavor=flavor,kind='classic',size='normal',alcohol='yes',price=500,amount=[0]*5,optional=False,ice=False,aged=False,blended=False))
aliases={'srush':'Сахарный прилив','sstar':'Бенгальский огонь','moblast':'Взрыв на Луне','pman':'Пианист','pwman':'Пианистка','beer':'Пиво','gpunch':'Удар по печени','pdriver':'Сваебой','splex':'Суплекс','fweaver':'Бон Развязон','btini':'Брендини'}
rows=[]
for r in recipes:
 rows.append('{'+','.join([cstr(aliases.get(r['id'],r['name'])),'{'+','.join(map(str,r['amount']))+'}',str(int(r['optional'])),str(int(r['ice'])),str(int(r['aged'])),str(int(r['blended']))]+[token(r[k]) for k in ['id','flavor','kind','size','alcohol']]+[str(r['price'])])+'}')
# One page per regular recipe; optional K shown as zero minimum.
book=[]
for i,r in enumerate(recipes):
 if r['id'] not in [recipes[x]['id'] for x in book]:book.append(i)
(G/'recipes.h').write_text('#pragma once\ntypedef struct {const char *name;int amount[5],optional,ice,aged,blended,id,flavor,kind,size,alcohol,price;} Recipe;\nstatic const Recipe recipes[]={\n'+',\n'.join(rows)+'};\nstatic const int recipeBook[]={'+','.join(map(str,book))+'};\n#define RECIPE_COUNT '+str(len(recipes))+'\n#define BOOK_COUNT '+str(len(book))+'\n',encoding='utf8')
(G/'recipes.json').write_text(json.dumps(recipes,indent=2))
# Commands are compiled to explicit entry/exit functions for each page.
actors=['gil','dana','kim','donovan','ingram','sei','doro','jamie','miki','alma','stella','art','stream','betty','deal','taylor','virgilio','brian','cass','rad','norma','mario','gaby','jill','nacho','vella','essentia','anna','lexi','tomcat','jess'];short={'gil':'gil','dan':'dana','dana':'dana','kim':'kim','don':'donovan','in':'ingram','sei':'sei','doro':'doro','jamie':'jamie','miki':'miki','alma':'alma','stel':'stella','art':'art','stream':'stream','strea':'stream','betty':'betty','deal':'deal','taylor':'taylor','virgilio':'virgilio','brian':'brian','cass':'cass','rad':'rad','norma':'norma','mario':'mario','gaby':'gaby','jill':'jill','nacho':'nacho','na':'nacho','vella':'vella','essentia':'essentia','an':'anna','anna':'anna','lexi':'lexi','tom':'tomcat','tomcat':'tomcat','jess':'jess'}
previous=json.loads((G/'v8-metadata.json').read_text(encoding='utf8'))['faces']
variants={a:list(previous.get(a,[''])) for a in actors}
variants['sei'].append('wound_base')
for filename in ['tutorial.txt','script1.txt','script2.txt','script3.txt','script4.txt','script5.txt','script6.txt','script7.txt','script8.txt','script9.txt','script10.txt','script11.txt','script12.txt','script13.txt','script14.txt','script15.txt','script16.txt','script17.txt','script18.txt','script19.txt','epilogues.txt']:
 for key,val in re.findall(r'\[XS:(\w+)face,([^\]]*)\]',(game/'scripts/eng'/filename).read_text(encoding='utf-8-sig')):
  actor=short[key]
  if filename in ('script8.txt','script10.txt','script12.txt','script15.txt') and actor=='sei':val='wound_'+(val or 'base')
  if val not in variants[actor]:variants[actor].append(val)
assert variants['dana'][3]=='mask'
def command(tag):
 if tag.startswith(('SHOW:','SHOWF:')) and ('doro_shake' in tag or 'dana_shake' in tag):
  return command(tag.replace('_shake',''))+'v->shakeUntil=v->now+500;'
 if tag.startswith(('SHOW:','SHOWF:')) and 'codec_' in tag:
  return '' # Day 6 room props are represented by the static apartment scene.
 if tag.startswith('HIDEALL:'):return 'memset(v->visible,0,sizeof(v->visible));'
 if tag.startswith('BANG:'):return '++v->bang;'
 if tag.startswith('CRASH:'):return '++v->crash;v->shakeUntil=v->now+500;'
 if tag.startswith('SHAKE:'):return 'v->shakeUntil=v->now+500;'
 if tag.startswith('BOOM:'):return '++v->boom;'
 if tag.startswith('CHAT:'):return f'v->chat={dict(pachi=1,yeah=2,boo=3,no=4,w=5,aw=6).get(tag[5:],0)};'
 if tag.startswith('CHANNEL:'):return 'v->news=1;'
 if tag.startswith('CHANGE:'):return 'v->news=2;'
 if tag.startswith('RUM:'):return 'v->rum=1;'
 if tag.startswith('ANNA:'):return 'v->annaUntil=v->now+3334;'
 if tag.startswith('SHOW:') or tag.startswith('SHOWF:'):
  x,a=tag.split(':')[1].split(',');a=a.replace('sprite_','')
  if a in ('minicg_alma','hack_obj','minicg_anna','minicg_doro','wdigfh_play','ending_playlist','curry_end_obj','concert_end_obj','doro_end_obj','hair_end_obj','vacation_end_obj','bad_end_obj'):return ''
  masked=a in ('seimask','danamask');wounded=a=='seiwound';a={'seimask':'sei','seiwound':'sei','danamask':'dana','brien':'brian'}.get(a,a);i=actors.index(a)
  return f'v->visible[{i}]=1;v->position[{i}]={x};v->face[{i}]={variants[a].index('mask') if masked else variants[a].index('wound_base') if wounded else 0};'
 if tag.startswith('XS:'):
  key,val=tag[3:].split(',')
  if key in ['ph','client','mix','juke']:return f's->{dict(ph="cur_stage",client="cur_client").get(key,key)}={val};'
  if key.endswith('face') and key[:-4] in short:
   a=short[key[:-4]];face='wound_'+(val or 'base') if current_script in ('script8.txt','script10.txt','script12.txt','script15.txt') and a=='sei' else val
   return f'v->face[{actors.index(a)}]={variants[a].index(face)};'
  if key.endswith('hide') and key[:-4] in short:return f'v->visible[{actors.index(short[key[:-4]])}]=0;'
 if tag.startswith('DON1'):return 's->orders=174;'
 if tag.startswith('DON2'):return 's->orders=4;'
 return ''
allblocks={};entries=[];enter={};leave={}
for filename,offset in [('tutorial.txt',0),('script1.txt',100),('script2.txt',200),('gameover.txt',300),('script3.txt',400),('script4.txt',500),('script5.txt',600),('script6.txt',700),('script7.txt',800),('script8.txt',900),('script9.txt',1000),('script10.txt',1100),('script11.txt',1200),('script12.txt',1300),('script13.txt',1400),('script14.txt',1500),('script15.txt',1600),('script16.txt',1700),('script17.txt',1800),('script18.txt',1900),('script19.txt',2000),('epilogues.txt',2100)]:
 current_script=filename
 block=offset;pending=''
 for raw in (game/'scripts/eng'/filename).read_text(encoding='utf-8-sig').replace('[XS:ph,1}', '[XS:ph,1]').splitlines():
  clean=' '.join(re.sub(r'\[[^\]]*\]','',raw).replace('#',' ').split())
  cmds=[(m.start(),command(m[1]),m[1]) for m in re.finditer(r'\[([^\]]*)\]',raw)]
  visual=''.join(c for _,c,t in cmds if not t.startswith(('XS:ph,','XS:client,','XS:mix,','XS:juke,','DON')) and 'visible[' not in c or False)
  # SHOW and emotion take effect at entry. Hides take effect after the spoken line.
  maskedraw=re.sub(r'\[[^\]]*\]',lambda m:' '*len(m[0]),raw)
  firsttext=next((i for i,c in enumerate(maskedraw) if not c.isspace()),len(raw))
  def isbefore(pos,t):return t.startswith(('HIDEALL','ANNA','SHOW','XS:gilface','XS:danaface','XS:kimface','XS:donface','XS:seiface','XS:doroface','XS:jamieface','XS:mikiface','XS:almaface','XS:stelface','XS:artface','XS:streamface','XS:bettyface','XS:virgilioface','XS:marioface','XS:gabyface','XS:jillface','XS:anface','XS:lexiface','BANG','CRASH','SHAKE','BOOM','CHAT','CHANNEL','RUM')) or ('hide,' in t and pos<firsttext)
  before=''.join(c for pos,c,t in cmds if isbefore(pos,t))
  after=''.join(c for pos,c,t in cmds if c and not isbefore(pos,t))
  if clean:
   name,sep,body=clean.partition(':')
   if not sep:name,body='',clean
   wrapped=textwrap.wrap(body.strip(),46,break_long_words=True,break_on_hyphens=False) or ['']
   first=len(entries)
   for k in range(0,len(wrapped),4):
    idx=len(entries);entries.append(dict(name=name,text='\n'.join(wrapped[k:k+4]),face=0));allblocks.setdefault(block,[]).append(idx)
   enter[first]=pending+before;leave[len(entries)-1]=after;pending=''
  else:pending+=before+after
  for n in re.findall(r'\[E:(\d+)\]',raw):block=offset+int(n)
assert 0 not in allblocks and 100 not in allblocks
starts=[0]*2108;counts=[0]*2108
for b,ids in allblocks.items():starts[b]=ids[0];counts[b]=len(ids)
(G/'story.h').write_text('#pragma once\ntypedef struct {const char *name,*text;int face;} Line;\nstatic const Line story[]={'+',\n'.join('{'+cstr(e['name'])+','+cstr(e['text'])+',0}' for e in entries)+'};\nstatic const int blockStart[]={'+','.join(map(str,starts))+'};\nstatic const int blockCount[]={'+','.join(map(str,counts))+'};\n',encoding='utf8')
(G/'story.json').write_text(json.dumps({b:[entries[i] for i in ids] for b,ids in allblocks.items()},ensure_ascii=False,indent=2),encoding='utf8')
def cases(commands):return '\n'.join(f'case {i}: {s} break;' for i,s in commands.items() if s)
(G/'commands.h').write_text('static void page_enter(View *v){State *s=&v->state;v->chat=0;(void)s;switch(blockStart[v->block]+v->line){'+cases(enter)+'}}\nstatic void page_leave(View *v){State *s=&v->state;(void)s;switch(blockStart[v->block]+v->line){'+cases(leave)+'}}\n')
# Composite full character bodies and facial layers at their original origins.
gd=GameData(game/'data.win');sp={gd.string(gd.u(p)):p for p in gd.pointers('SPRT')}
def origin(name):return struct.unpack_from('<ii',gd.data,sp[name]+48)
def composite(names):
 base=gd.sprite(names[0][0]);ox,oy=origin(names[0][0])
 for part in names[1:]:
  name,dx,dy=part[:3];im=gd.sprite(name,part[3] if len(part)>3 else 0);x,y=origin(name);base.alpha_composite(im,(ox-x+dx,oy-y+dy))
 return base.resize((round(base.width*.5),round(base.height*.5)),Image.Resampling.NEAREST)
layers={
 'gil':{'':['gil_spr','gil_eyes','gil_lips'],'cods':['gil_cods','gil_cods_eyes','gil_cods_lips'],'surprise':['gil_surprised','gil_surprised_eyes','gil_surprised_lips'],'fucked':['gil_spr','gil_fucked_up'],'angry':['gil_angry_spr','gil_angry_eyes','gil_lips']},
 'dana':{'':['dana_spr','dana_eyes','dana_lips'],'mask':['danamask_spr'],'eee':['dana_spr_oops','dana_eyes_oops','dana_lips_oops'],'worry':['dana_spr_serious',('dana_eyes_serious',-34,-160),'dana_lips_serious']},
 'kim':{'':['kim_spr','kim_eyes','kim_lips'],'mad':['kim_mad'],'murder':['kim_murder'],'sad':['kim_spr_sad','kim_eyes_sad','kim_lips_sad'],'sleep':['kim_sleep']},
 'donovan':{'':['donovan_spr','donovan_eyes','donovan_lips'],'shitgrin':['donovan_spr_smileopen','donovan_eyes'],'smile':['donovan_spr_smileclosed']},
 'ingram':{'':['ingram_spr',('ingram_eyes',11,-156),('ingram_lips',9,-125)]},
 'sei':{'':['sei_spr','sei_eyes','sei_lips'],'mask':['sei_mask_spr'],'worried':['sei_spr','sei_eyes_worried','sei_lips'],'smile':['sei_spr_smile','sei_eyes','sei_lips_smile'],'drunk':['sei_spr_drunk','sei_eyes_drunk','sei_lips_drunk']}}
layers['doro']={'':['dorothy_spr','dorothy_eyes','dorothy_lips'],'pachi':['dorothy_spr_pachi','dorothy_lips_pachi']}
for f in ['angry','dogs','drunk','smug','think']:layers['doro'][f]=['dorothy_spr_'+f,'dorothy_eyes_'+f,'dorothy_lips_'+f]
layers['jamie']={'':['jamie_spr','jamie_eyes','jamie_lips'],'surprise':['jamie_spr_surprised','jamie_eyes_surprised'],'shy':['jamie_spr_shy','jamie_eyes_shy']}
layers['miki']={'':['miki_spr','miki_eyes','miki_lips'],'smile':['miki_spr','miki_smile_spr'],'edgy':['miki_edgy_spr','miki_edgy_eyes','miki_edgy_lips'],'edgelord':['miki_edgelord_spr','miki_edgy_eyes','miki_edgy_lips']}

def sprite_names(indices):return [gd.string(gd.u(gd.pointers('SPRT')[i])) for i in indices]
layers['alma']={f:sprite_names(ids) for f,ids in {
 '':[308,310,309], 'drunk':[311,312,313], 'confused':[314,315,316],
 'drunkconcern':[317,318,319], 'serious':[320,321,322], 'sigh':[323,324],
 'worried':[325,326,327], 'smile':[328,329], 'smug':[330,331,332], 'concern':[333,335,334]}.items()}
layers['stella']={f:sprite_names(ids) for f,ids in {
 '':[336,339,342,338,337], 'surprise':[343,341,345,338,344],
 'concern':[346,339,348,338,347], 'baka':[349,340,351,338,350],
 'sad':[352,340,353,338,354], 'happy':[336,341,355,338]}.items()}
layers['doro']['cry']=sprite_names([224]);layers['doro']['sad']=sprite_names([239,240,241])
for f in ['concern','confused','sigh']:layers['doro'][f]=layers['doro']['']
layers['dana']['closedsmile']=['dana_spr',('dana_eyes',0,0,1),'dana_lips']
layers['art']={'':sprite_names([370,372,371]),'sigh':sprite_names([373,374])}
layers['art']['sight']=layers['art']['sigh']
layers['betty']={f:sprite_names(ids) for f,ids in {'':[375,377,376],'grumpy':[378,380,379],'sigh':[381,382],'drunk':[383,385,384]}.items()}
layers['deal']={'':sprite_names([386,388,387])}
layers['stream']={f:sprite_names(ids)+[(sprite_names([290])[0],-19,-220)] for f,ids in {'':[287,289,288],'ex':[291,289],'pout':[295,297,296],'drunk':[292,294,293],'drunkex':[298]}.items()}
layers['taylor']={'':sprite_names([399])}
layers['virgilio']={f:sprite_names(ids) for f,ids in {'':[389,391,390],'smug':[392,393],'serious':[394,395,396],'dissapoint':[397,398]}.items()}
layers['brian']={'':sprite_names([467,468,469])}
layers['cass']={'':sprite_names([470,471,472])}
layers['doro']['wah']=sprite_names([249,250,251])
layers['rad']={'':['rad_spr','rad_lips']}
layers['dana']['intensify']=layers['dana']['']
layers['sei'].update({
 'wound_base':sprite_names([189,190,192]),
 'wound_happy':sprite_names([189,195,192]),
 'wound_smile':sprite_names([189,190,192]),
 'wound_pain':sprite_names([193,194]),
 'wound_sad':sprite_names([196,197,198]),
 'wound_sorry':sprite_names([199,200,201])})
layers['sei']['wound_sleepy']=sprite_names([189,191,192])
layers['norma']={'':sprite_names([412,413,414])}
layers['mario']={f:sprite_names(ids) for f,ids in {
 '':[415,416,417], 'surprise':[418,419,420],
 'smile':[421,422], 'nothet':[423,425,424]}.items()}
layers['gaby']={f:sprite_names(ids) for f,ids in {
 '':[426,427,428], 'angry':[429,430,431],
 'sad':[432,433,434], 'pain':[432,433,434],
 'shy':[440,441,443], 'surprise':[437,438,439]}.items()}
layers['gaby'].update({f:layers['gaby']['shy'] for f in ('shyclosed','shysad','shysmile','smile')})
layers['alma']['seiours']=layers['alma']['']
layers['nacho']={'':sprite_names([274,275,276])}
layers['jill']={f:sprite_names(ids) for f,ids in {
 '':[445,446,447], 'smile':[448,449,450], 'surprise':[451,452,453],
 'uh':[454,455,456], 'sad':[457,446,458], 'baka':[445,446,447],
 'think':[445,446,447]}.items()}
layers['doro']['heart']=layers['doro']['pachi']
layers['vella']={'':sprite_names([459,460,461])}
layers['essentia']={'':sprite_names([462,463,464])}
layers['anna']={f:sprite_names(ids) for f,ids in {
 '':[254,260,261], 'away':[254,257,261], 'awayhalf':[254,258,261],
 'happy':[255,260,261], 'sad':[254,256,261], 'smug':[254,259,261],
 'smugsmile':[255,259,261]}.items()}
layers['lexi']={'':sprite_names([479,480,481])}
layers['tomcat']={'':['tomcat_spr','tomcat_eyes','tomcat_lips']}
layers['jess']={'':['jess_spr','jess_ears','jess_lips']}
layers['stella']['pain']=layers['stella']['sad']
layers['doro']['cat']=layers['doro']['pachi']
layers['anna']['awayclosed']=layers['anna']['away']
layers['anna']['sadhalf']=layers['anna']['sad']
defs=[];tables=[]
for a in actors:
 names=[]
 for i,f in enumerate(variants[a]):
  ls=layers[a][f];im=composite([(x,0,0) if isinstance(x,str) else x for x in ls]);name=f'actor_{a}_{i}';names.append('&'+name)
  im.save(G/(name+'.png'));defs.append('static const uint8_t px_'+name+'[]={'+','.join(map(str,im.tobytes()))+'};\nstatic const Sprite '+name+'={'+f'{im.width},{im.height},px_{name}'+'};')
 tables.append('{'+','.join(names+['NULL']*(16-len(names)))+'}')
(G/'actors.h').write_text(f'#pragma once\n#define ACTOR_COUNT {len(actors)}\nextern const Sprite *const actors[{len(actors)}][16];\n')
im=gd.sprite('anna_channel').resize((round(gd.sprite('anna_channel').width*264/338),round(gd.sprite('anna_channel').height*264/338)),Image.Resampling.NEAREST)
im.save(G/'anna_tv.png')
defs.append('static const uint8_t px_anna_tv[]={'+','.join(map(str,im.tobytes()))+'};\nconst Sprite anna_tv={'+f'{im.width},{im.height},px_anna_tv'+'};')
(G/'actors.h').write_text((G/'actors.h').read_text()+f'extern const Sprite anna_tv;\nstatic const int actorFaceCount[{len(actors)}]={{'+','.join(str(len(variants[a])) for a in actors)+'};\n')
old=(G/'assets.c').read_text().split('\n#include <stddef.h>')[0]
(G/'assets.c').write_text(old+'\n#include <stddef.h>\n'+'\n'.join(defs)+f'\nconst Sprite *const actors[{len(actors)}][16]={{'+','.join(tables)+'};\n')
(G/'day1-metadata.json').write_text(json.dumps({'pages':len(entries),'blocks':len(allblocks),'recipes':len(book),'recipe_variants':len(recipes),'faces':variants,'tokens':tok},ensure_ascii=False,indent=2),encoding='utf8')
print('Generated',len(entries),'pages,',len(book),'recipes,',variants)
