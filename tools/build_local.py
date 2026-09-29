"""Build on this Windows workspace using Arm GCC plus devkitPro runtime libraries."""
from pathlib import Path
import argparse,subprocess,os,json,sys
from elf2_3dsx import convert

def build(toolchain,project,test_mode=False):
    base=Path(toolchain).resolve();project=Path(project).resolve()
    gcc=base/'bin/arm-none-eabi-gcc.exe';os.environ['PATH']=str(gcc.parent)+os.pathsep+os.environ['PATH']
    dkp=base/'opt/devkitpro';arm=dkp/'devkitARM/arm-none-eabi'
    lib=arm/'lib/armv6k/fpu';gcc_lib=dkp/'devkitARM/lib/gcc/arm-none-eabi/16.1.0/armv6k/fpu'
    output=project/('build-test' if test_mode else 'build');output.mkdir(exist_ok=True)
    flags=['-march=armv6k','-mtune=mpcore','-mfloat-abi=hard','-mfpu=vfp','-marm','-mword-relocations','-D__3DS__','-O2','-g','-Wall','-Wextra','-Werror','-ffunction-sections','-fdata-sections','-fno-strict-aliasing','-isystem',str(arm/'include'),'-I'+str(dkp/'libctru/include'),'-I'+str(project/'generated'),'-I'+str(project/'source')]
    if test_mode:flags.append('-DVA11_TEST_MODE=1')
    log=[]
    def run(args):
        p=subprocess.run([str(gcc),*args],capture_output=True,text=True)
        log.append(' '.join(map(str,args))+'\n'+p.stdout+p.stderr)
        (output/'build.log').write_text('\n'.join(log),encoding='utf8')
        if p.stdout or p.stderr:print(p.stdout+p.stderr,flush=True)
        p.check_returncode()
    objects=[]
    for source in [*sorted((project/'source').glob('*.c')),*sorted((project/'generated').glob('*.c'))]:
        obj=output/(source.stem+'.o');print('Compiling',source.name,flush=True);run([*flags,'-c',str(source),'-o',str(obj)]);objects.append(str(obj))
    elf=output/'va11-3ds.elf'
    run([*flags,'-nostdlib','-Wl,-T,'+str(arm/'lib/3dsx.ld'),'-Wl,--emit-relocs,--gc-sections,--use-blx','-Wl,--defsym=__sync_synchronize=__sync_synchronize_dmb','-Wl,-Map,'+str(output/'va11-3ds.map'),'-o',str(elf),str(lib/'3dsx_crt0.o'),str(gcc_lib/'crti.o'),str(gcc_lib/'crtbegin.o'),*objects,'-L'+str(dkp/'libctru/lib'),'-L'+str(lib),'-L'+str(gcc_lib),'-Wl,--start-group','-lctru','-lc','-lm','-lgcc','-lsysbase','-Wl,--end-group',str(gcc_lib/'crtend.o'),str(gcc_lib/'crtn.o')])
    target=project/'sd/3ds'/('va11-3ds-test/va11-3ds-test.3dsx' if test_mode else 'va11-3ds/va11-3ds.3dsx')
    target.parent.mkdir(parents=True,exist_ok=True)
    report=convert(elf,target)
    report['compiler']=subprocess.check_output([str(gcc),'--version'],text=True).splitlines()[0]
    report['target']='ARMv6K / MPCore / VFP hard-float; original 3DS';report['hardware_tested']=False
    report['test_mode']=test_mode
    (project/('test-build-report.json' if test_mode else 'build-report.json')).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('toolchain');p.add_argument('--project',default=Path(__file__).resolve().parents[1]);p.add_argument('--test-mode',action='store_true');a=p.parse_args();build(a.toolchain,a.project,a.test_mode)
