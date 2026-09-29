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
day2=re.sub(r'choose\([^)]*\)', '0', day2).replace('distractioncheck()', '1')
day3=(D/'gml_Script_day3control.gml').read_text();mix3=(D/'gml_Script_mix3control.gml').read_text()
day3=re.sub(r'choose\([^)]*\)', '0', day3).replace('distractioncheck()', '1')
day4=(D/'gml_Script_day4control.gml').read_text();mix4=(D/'gml_Script_mix4control.gml').read_text()
day4=re.sub(r'choose\([^)]*\)', '0', day4).replace('distractioncheck()', '1')
day5=(D/'gml_Script_day5control.gml').read_text();mix5=(D/'gml_Script_mix5control.gml').read_text()
day5=re.sub(r'choose\([^)]*\)', '0', day5).replace('distractioncheck()', '1')
tokens=sorted(set(re.findall(r'"([^"\n]*)"',day+mix+day2+mix2+day3+mix3+day4+mix4+day5+mix5+drinks)))
tok=json.loads((G/'v8-metadata.json').read_text(encoding='utf8'))['tokens']
for v in tokens:
 if v not in tok:tok[v]=max(tok.values())+1
(G/'tokens.h').write_text('#pragma once\n'+''.join(f'#define TOK_{k} {v}\n' for k,v in tok.items() if re.fullmatch('[a-z]+',k)))
def token(v):return str(tok[v])
fields=sorted(set(re.findall(r'global\.(\w+)',day+mix+day2+mix2+day3+mix3+day4+mix4+day5+mix5))-{'ch1','ch2','ch3','ch4','ch5','tuto'}-{f'odstr{i}' for i in range(200)})
fields+=['shouldpay','rightdrink','big_able','tipping','cash','tips','mistakes','juke','mix','drinkscore_a']
fields+=['cur_day','heldRecipe','heldK','heldIce','rightdrink1','rightdrink2','big_able1','big_able2']
legacy=json.loads((G/'v8-state-fields.json').read_text())
fields=legacy+sorted(set(fields)-set(legacy))
(G/'state.h').write_text('#pragma once\ntypedef struct {\n'+''.join('int '+f+';\n' for f in fields)+'} State;\n')
(G/'state-fields.json').write_text(json.dumps(fields))
def translate(s):
 s=re.sub(r'textbox_create\(global\.(ch1|ch2|ch3|ch4|ch5|tuto), (\d+), 1\);',lambda m:'return '+str(int(m[2])+({'tuto':0,'ch1':100,'ch2':200,'ch3':400,'ch4':500,'ch5':600}[m[1]]))+';',s)
 s=re.sub(r'instance_create\(x, y, (305|308)\);',lambda m:'return '+('-2' if m[1]=='305' else '-3')+';',s)
 s=re.sub(r'mixertips_double\((\d+), (\d+), (\d+), (\d+), (\d+), (\d+)\);',lambda m:f's->shouldpay={m[1]};s->rightdrink1={m[2]};s->rightdrink2={m[3]};s->big_able1={m[4]};s->big_able2={m[5]};s->tipping={m[6]};',s)
 s=re.sub(r'mixertips\((\d+), (\d+), (\d+), (\d+)\);',lambda m:f's->shouldpay={m[1]};s->rightdrink={m[2]};s->big_able={m[3]};s->tipping={m[4]};',s)
 s=re.sub(r'global.odstr(\d+)',r'\1',s)
 s=re.sub(r'global\.(\w+)',r's->\1',s)
 s=re.sub(r'"([^"\n]*)"',lambda m:token(m[1]),s).replace('exit;','return 0;')
 # Each outer case has its own stage switch; preserve no-match as idle.
 s=re.sub(r'\n    case ',r'\n    case ',s)
 s=s.replace('\n    case 0:', '\n        return 0;\n    case 0:')
 for i in range(1,5):s=s.replace(f'\n    case {i}:',f'\n        return 0;\n    case {i}:')
 s=re.sub(r'\{\n        return 0;\n    case (\d+):',r'{\n    case \1:',s)
 s=s.replace('\n            case ', '\n                /* fall through */\n            case ')
 return s+'\nreturn 0;'
(G/'rules.h').write_text('static int day_rule(State *s){\n'+translate(day)+'\n}\nstatic int mix_rule(State *s){\n'+translate(mix)+'\n}\nstatic int day2_rule(State *s){\n'+translate(day2)+'\n}\nstatic int mix2_rule(State *s){\n'+translate(mix2)+'\n}\nstatic int day3_rule(State *s){\n'+translate(day3)+'\n}\nstatic int mix3_rule(State *s){\n'+translate(mix3)+'\n}\nstatic int day4_rule(State *s){\n'+translate(day4)+'\n}\nstatic int mix4_rule(State *s){\n'+translate(mix4)+'\n}\nstatic int day5_rule(State *s){\n'+translate(day5)+'\n}\nstatic int mix5_rule(State *s){\n'+translate(mix5)+'\n}\n')
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
# Bottled extra: available directly until the shop is implemented.
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
actors=['gil','dana','kim','donovan','ingram','sei','doro','jamie','miki','alma','stella','art','stream','betty','deal','taylor','virgilio'];short={'gil':'gil','dan':'dana','dana':'dana','kim':'kim','don':'donovan','in':'ingram','sei':'sei','doro':'doro','jamie':'jamie','miki':'miki','alma':'alma','stel':'stella','art':'art','stream':'stream','betty':'betty','deal':'deal','taylor':'taylor','virgilio':'virgilio'}
previous=json.loads((G/'v8-metadata.json').read_text(encoding='utf8'))['faces']
variants={a:list(previous.get(a,[''])) for a in actors}
for filename in ['tutorial.txt','script1.txt','script2.txt','script3.txt','script4.txt','script5.txt']:
 for key,val in re.findall(r'\[XS:(\w+)face,([^\]]*)\]',(game/'scripts/eng'/filename).read_text(encoding='utf-8-sig')):
  actor=short[key]
  if val not in variants[actor]:variants[actor].append(val)
assert variants['dana'][3]=='mask'
def command(tag):
 if tag.startswith(('SHOW:','SHOWF:')) and 'doro_shake' in tag:
  return command(tag.replace('doro_shake','doro'))+'v->shakeUntil=v->now+500;'
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
  x,a=tag.split(':')[1].split(',');a=a.replace('sprite_','');masked=a in ('seimask','danamask');a={'seimask':'sei','danamask':'dana'}.get(a,a);i=actors.index(a)
  return f'v->visible[{i}]=1;v->position[{i}]={x};v->face[{i}]={variants[a].index('mask') if masked else 0};'
 if tag.startswith('XS:'):
  key,val=tag[3:].split(',')
  if key in ['ph','client','mix','juke']:return f's->{dict(ph="cur_stage",client="cur_client").get(key,key)}={val};'
  if key.endswith('face') and key[:-4] in short:
   a=short[key[:-4]];return f'v->face[{actors.index(a)}]={variants[a].index(val)};'
  if key.endswith('hide') and key[:-4] in short:return f'v->visible[{actors.index(short[key[:-4]])}]=0;'
 if tag.startswith('DON1'):return 's->orders=174;'
 if tag.startswith('DON2'):return 's->orders=4;'
 return ''
allblocks={};entries=[];enter={};leave={}
for filename,offset in [('tutorial.txt',0),('script1.txt',100),('script2.txt',200),('gameover.txt',300),('script3.txt',400),('script4.txt',500),('script5.txt',600)]:
 block=offset;pending=''
 for raw in (game/'scripts/eng'/filename).read_text(encoding='utf-8-sig').splitlines():
  clean=' '.join(re.sub(r'\[[^\]]*\]','',raw).replace('#',' ').split())
  cmds=[(m.start(),command(m[1]),m[1]) for m in re.finditer(r'\[([^\]]*)\]',raw)]
  visual=''.join(c for _,c,t in cmds if not t.startswith(('XS:ph,','XS:client,','XS:mix,','XS:juke,','DON')) and 'visible[' not in c or False)
  # SHOW and emotion take effect at entry. Hides take effect after the spoken line.
  maskedraw=re.sub(r'\[[^\]]*\]',lambda m:' '*len(m[0]),raw)
  firsttext=next((i for i,c in enumerate(maskedraw) if not c.isspace()),len(raw))
  def isbefore(pos,t):return t.startswith(('HIDEALL','ANNA','SHOW','XS:gilface','XS:danaface','XS:kimface','XS:donface','XS:seiface','XS:doroface','XS:jamieface','XS:mikiface','XS:almaface','XS:stelface','XS:artface','XS:streamface','XS:bettyface','XS:virgilioface','BANG','CRASH','SHAKE','BOOM','CHAT','CHANNEL','RUM')) or ('hide,' in t and pos<firsttext)
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
starts=[0]*662;counts=[0]*662
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
layers['betty']={f:sprite_names(ids) for f,ids in {'':[375,377,376],'grumpy':[378,380,379],'sigh':[381,382],'drunk':[383,385,384]}.items()}
layers['deal']={'':sprite_names([386,388,387])}
layers['stream']={f:sprite_names(ids)+[(sprite_names([290])[0],-19,-220)] for f,ids in {'':[287,289,288],'ex':[291,289],'pout':[295,297,296],'drunk':[292,294,293],'drunkex':[298]}.items()}
layers['taylor']={'':sprite_names([399])}
layers['virgilio']={f:sprite_names(ids) for f,ids in {'':[389,391,390],'smug':[392,393],'serious':[394,395,396],'dissapoint':[397,398]}.items()}
layers['doro']['wah']=sprite_names([249,250,251])
defs=[];tables=[]
for a in actors:
 names=[]
 for i,f in enumerate(variants[a]):
  ls=layers[a][f];im=composite([(x,0,0) if isinstance(x,str) else x for x in ls]);name=f'actor_{a}_{i}';names.append('&'+name)
  im.save(G/(name+'.png'));defs.append('static const uint8_t px_'+name+'[]={'+','.join(map(str,im.tobytes()))+'};\nstatic const Sprite '+name+'={'+f'{im.width},{im.height},px_{name}'+'};')
 tables.append('{'+','.join(names+['NULL']*(16-len(names)))+'}')
(G/'actors.h').write_text('#pragma once\n#define ACTOR_COUNT 17\nextern const Sprite *const actors[17][16];\n')
im=gd.sprite('anna_channel').resize((round(gd.sprite('anna_channel').width*264/338),round(gd.sprite('anna_channel').height*264/338)),Image.Resampling.NEAREST)
im.save(G/'anna_tv.png')
defs.append('static const uint8_t px_anna_tv[]={'+','.join(map(str,im.tobytes()))+'};\nconst Sprite anna_tv={'+f'{im.width},{im.height},px_anna_tv'+'};')
(G/'actors.h').write_text((G/'actors.h').read_text()+'extern const Sprite anna_tv;\nstatic const int actorFaceCount[17]={'+','.join(str(len(variants[a])) for a in actors)+'};\n')
old=(G/'assets.c').read_text().split('\n#include <stddef.h>')[0]
(G/'assets.c').write_text(old+'\n#include <stddef.h>\n'+'\n'.join(defs)+'\nconst Sprite *const actors[17][16]={'+','.join(tables)+'};\n')
(G/'day1-metadata.json').write_text(json.dumps({'pages':len(entries),'blocks':len(allblocks),'recipes':len(book),'recipe_variants':len(recipes),'faces':variants,'tokens':tok},ensure_ascii=False,indent=2),encoding='utf8')
print('Generated',len(entries),'pages,',len(book),'recipes,',variants)
