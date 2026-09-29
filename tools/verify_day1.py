from pathlib import Path
import io,ctypes as C,json,random
from elftools.elf.elffile import ELFFile
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM
from unicorn.arm_const import *
from PIL import Image
P=Path(__file__).resolve().parents[1]
class Mixer(C.LittleEndianStructure):
 _fields_=[('amount',C.c_int32*5),('ice',C.c_bool),('aged',C.c_bool),('running',C.c_bool),('ready',C.c_bool),('blended',C.c_bool),('started',C.c_uint64)]
class State(C.LittleEndianStructure):
 _fields_=[(x,C.c_int32) for x in json.loads((P/'generated/state-fields.json').read_text())]
class View(C.LittleEndianStructure):
 _fields_=[(n,C.c_int32) for n in ['block','line','mode','round','selected','recipe','overlay','audio']]+[('now',C.c_uint64),('mixer',Mixer),('state',State),('visible',C.c_int32*15),('position',C.c_int32*15),('face',C.c_int32*15),('saveError',C.c_int32),('cheapErrors',C.c_int32),('failed',C.c_int32),('annaUntil',C.c_uint64)]+[(n,C.c_int32) for n in ['musicTrack','chat','news','rum','boom']]
elf=ELFFile(io.BytesIO((P/'build/va11-3ds.elf').read_bytes()))
machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.mem_map(0x100000,0x3000000)
machine.reg_write(UC_ARM_REG_C1_C0_2,0xf00000)
machine.reg_write(UC_ARM_REG_FPEXC,0x40000000)
for seg in elf.iter_segments():
 if seg['p_type']=='PT_LOAD':machine.mem_write(seg['p_vaddr'],seg.data())
machine.mem_map(0x4000000,0x100000);machine.mem_map(0x5000000,0x200000)
symbols={s.name:s['st_value'] for s in elf.get_section_by_name('.symtab').iter_symbols()}
address=0x5100000
def call(name,*args):
 machine.reg_write(UC_ARM_REG_CPSR,0x10)
 for reg,arg in zip([UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3],args):machine.reg_write(reg,arg&0xffffffff)
 machine.reg_write(UC_ARM_REG_SP,0x40fff00);machine.reg_write(UC_ARM_REG_LR,0x4100000)
 for i,arg in enumerate(args[4:]):machine.mem_write(0x40fff00+i*4,int(arg).to_bytes(4,'little',signed=True))
 machine.emu_start(symbols[name],0x4100000,count=100000000)
 assert machine.reg_read(UC_ARM_REG_PC)==0x4100000,name
 return machine.reg_read(UC_ARM_REG_R0)
def put(v):machine.mem_write(address,bytes(v))
def get():return View.from_buffer_copy(machine.mem_read(address,C.sizeof(View)))
def snapshot(v,name):
 put(v);call('draw_screens',0x5000000,0x5050000,address)
 canvas=Image.new('RGB',(416,512),(8,7,12))
 for base,w,y in [(0x5000000,400,8),(0x5050000,320,264)]:
  raw=bytes(machine.mem_read(base,w*240*3));im=Image.frombytes('RGB',(240,w),raw,'raw','BGR').transpose(Image.Transpose.ROTATE_90);canvas.paste(im,((416-w)//2,y))
 (P/'previews').mkdir(exist_ok=True);canvas.save(P/'previews'/f'day1-{name}.png')
recipes=json.loads((P/'generated/recipes.json').read_text());story=json.loads((P/'generated/story.json').read_text(encoding='utf8'))
checks=[]
for i,r in enumerate(recipes):
 m=Mixer();m.amount[:]=r['amount'];m.ice=r['ice'];m.aged=r['aged'];m.blended=r['blended'];m.ready=True
 expected=next(j+1 for j,q in enumerate(recipes) if q['amount'][:4]==r['amount'][:4] and (r['amount'][4]>=q['amount'][4] if q['optional'] else r['amount'][4]==q['amount'][4]) and all(q[k]==r[k] for k in ('ice','aged','blended')))
 machine.mem_write(address,bytes(m));assert call('mixer_identify',address)==expected,(i,r)
checks.append(f'{len(recipes)} original recipe variants recognized by ARM binary')
seen=set();states=set();rng=random.Random(1101);screens=set();runs=1000
for run in range(runs):
 put(View());call('engine_start',address,run%2);steps=0;served=0
 while True:
  v=get();steps+=1;seen.add(v.block);states.add((v.state.cur_client,v.state.cur_stage))
  assert steps<2000,('loop',run,v.block,v.line,v.state.cur_client,v.state.cur_stage)
  assert v.mode!=4,('stuck',run,v.block,v.line,v.state.cur_client,v.state.cur_stage)
  assert call('engine_valid',address)==1,('invalid',run,v.block)
  if run==0:
   for actor in range(6):
    if v.visible[actor] and actor not in screens:snapshot(v,str(actor));screens.add(actor)
  if v.mode in (2,6):
   if run==0:
    assert v.mode==2
    snapshot(v,'end')
   break
  if v.mode==7:
   call('engine_finish_jukebox',address);continue
  if v.mode in (0,3):
   result=call('engine_advance_checkpoint',address)
   assert result==int(get().mode==2),('save outside end of day',v.block,v.line)
   continue
  assert v.mode==1
  if run==0:
   requested={1:'srush',2:'moblast',3:'beer',4:'beer',5:'beer',7:'beer',6:'gpunch',8:'gpunch',9:'pdriver',10:'fweaver',11:'moblast',12:'btini',13:'btini',14:'srush',15:'pwman',16:'btini',174:'beer'}
   wanted=requested[v.state.orders];r=next(r for r in recipes if r['id']==wanted and (v.state.orders not in (3,4,6,8) or r['size']=='big') and (v.state.orders!=6 or r['alcohol']=='no'))
  else:r=rng.choice(recipes)
  v.mixer=Mixer();v.mixer.amount[:]=r['amount'];v.mixer.ice=r['ice'];v.mixer.aged=r['aged'];v.mixer.blended=r['blended'];v.mixer.ready=True
  put(v);call('engine_serve',address);served+=1
 if run<3:print('Completed',run,'pages',steps,'drinks',served,flush=True)
checks.append(f'{runs} shift simulations ending in completion or Game Over with original branching, alternating tutorial/direct start')
checks.append(f'{len(seen)} narrative blocks reached')
report=dict(checks=checks,blocks=sorted(seen),states=sorted(states),hardware_tested=False,limits='ARM engine and renderer only; console launch, SD saves, audio, touch and frame rate need hardware testing.')
(P/'test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
