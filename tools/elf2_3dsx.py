"""Small ELF32 -> 3DSX packer, following devkitPro's documented 3DSX format.

Requires pyelftools. Rejects unsupported relocation kinds instead of silently
producing a non-relocatable binary. Assets are linked into rodata; audio uses SD.
"""
from pathlib import Path
import io,struct
from elftools.elf.elffile import ELFFile

def align(n):return (n+4095)&~4095
def relocation_runs(addresses,start,end):
    runs=[];cursor=start
    for address in sorted(addresses):
        if not start<=address<end:continue
        skip=(address-cursor)//4
        while skip>65535:runs.append((65535,0));skip-=65535;cursor+=65535*4
        if skip==0 and runs and runs[-1][1]<65535:
            a,b=runs[-1];runs[-1]=(a,b+1)
        else:runs.append((skip,1))
        cursor=address+4
    return runs

def convert(source,target):
    data=bytearray(Path(source).read_bytes());elf=ELFFile(io.BytesIO(data))
    assert elf.elfclass==32 and elf.little_endian and elf['e_machine']=='EM_ARM' and elf['e_type']=='ET_EXEC'
    segments=[s for s in elf.iter_segments() if s['p_type']=='PT_LOAD' and s['p_memsz']]
    assert len(segments)==3 and [s['p_flags'] for s in segments]==[5,4,6]
    base=segments[0]['p_vaddr'];top=segments[-1]['p_vaddr']+align(segments[-1]['p_memsz'])
    assert elf['e_entry']==base
    for i,s in enumerate(segments):
        assert s['p_filesz']%4==0 and s['p_memsz']%4==0
        if i<2:assert s['p_filesz']==s['p_memsz']
        if i:assert s['p_vaddr']==segments[i-1]['p_vaddr']+align(segments[i-1]['p_memsz'])
    starts=[s['p_vaddr'] for s in segments]+[top];absrel=set();relrel=set();expected={}
    def seg(addr):return 0 if addr<starts[1] else 1 if addr<starts[2] else 2
    # ARM instructions, TLS local offsets and address-independent branches need no loader fixup.
    nofix={0,1,10,27,28,29,30,40,42,43,44,45,46,47,48,50,51,108,109}
    observed={}
    for section in elf.iter_sections():
        if section['sh_type']=='SHT_RELA':raise ValueError('RELA is unsupported')
        if section['sh_type']!='SHT_REL':continue
        dest=elf.get_section(section['sh_info'])
        if not dest['sh_flags']&2:continue
        symtab=elf.get_section(section['sh_link'])
        for r in section.iter_relocations():
            address=r['r_offset'];kind=r['r_info_type'];observed[kind]=observed.get(kind,0)+1
            if not dest['sh_addr']<=address<dest['sh_addr']+dest['sh_size']:continue
            if address in absrel or address in relrel:continue
            if kind in nofix and kind!=42:continue
            if address%4:raise ValueError('Unaligned data relocation')
            offset=dest['sh_offset']+address-dest['sh_addr'];value=struct.unpack_from('<I',data,offset)[0]
            symbol=symtab.get_symbol(r['r_info_sym'])
            if kind in (2,38):
                if symbol['st_info']['bind']=='STB_WEAK' and symbol['st_value']==0:continue
                if not base<=value<=top:raise ValueError(('Invalid absolute relocation',hex(address),hex(value)))
                expected[address]=(value,False,False);value-=base;absrel.add(address)
            elif kind in (3,41,42,107):
                if kind==42 and value&0x80000000:continue
                displacement=value
                if kind==42 and value&0x40000000:displacement|=0x80000000
                if displacement&0x80000000:displacement-=1<<32
                target_address=address+displacement
                if not base<=target_address<=top:raise ValueError('Invalid relative relocation')
                if seg(target_address)==seg(address):continue
                expected[address]=(target_address,True,kind==42)
                value=target_address-base
                if kind==42:value|=1<<28
                relrel.add(address)
            else:raise ValueError(f'Unsupported relocation {kind}')
            struct.pack_into('<I',data,offset,value)
    # The ARM compiler is used in ARM mode throughout, so interworking veneers
    # must be identified explicitly if a future source change introduces them.
    symtab=elf.get_section_by_name('.symtab')
    for symbol in symtab.iter_symbols():
        if symbol.name.endswith('_from_arm'):raise ValueError('Interworking veneer needs explicit support')
    tables=[];counts=[]
    for i in range(3):
        a=relocation_runs(absrel,starts[i],starts[i+1]);r=relocation_runs(relrel,starts[i],starts[i+1]);counts.append((len(a),len(r)));tables.extend(a+r)
    sizes=[s['p_memsz'] for s in segments];bss=sizes[2]-segments[2]['p_filesz']
    result=struct.pack('<4sHH6I',b'3DSX',32,8,0,0,*sizes,bss)
    result+=b''.join(struct.pack('<II',*c) for c in counts)
    result+=b''.join(data[s['p_offset']:s['p_offset']+s['p_filesz']] for s in segments)
    result+=b''.join(struct.pack('<HH',*r) for r in tables)
    Path(target).write_bytes(result)
    verify(result,segments,expected,base)
    return {'bytes':len(result),'code':sizes[0],'rodata':sizes[1],'data':sizes[2],'bss':bss,'absolute_relocations':len(absrel),'relative_relocations':len(relrel),'elf_relocation_types':observed}

def verify(blob,segments,expected,base):
    """Apply emitted relocation tables at separated addresses and check ELF targets."""
    h=struct.unpack_from('<4sHH6I',blob);sizes=list(h[5:8]);bss=h[8]
    count=[struct.unpack_from('<II',blob,32+i*8) for i in range(3)]
    pos=56;buffers=[]
    for i,n in enumerate(sizes):
        file_size=n-(bss if i==2 else 0);buffers.append(bytearray(blob[pos:pos+file_size])+bytearray(n-file_size));pos+=file_size
    bases=[0x10000000,0x18000000,0x20000000];old=[s['p_vaddr'] for s in segments]
    def target(value):
        oldaddr=base+value
        j=0 if oldaddr<old[1] else 1 if oldaddr<old[2] else 2
        return bases[j]+oldaddr-old[j]
    patched=set()
    for i in range(3):
        for typ in range(2):
            cursor=0
            for _ in range(count[i][typ]):
                skip,n=struct.unpack_from('<HH',blob,pos);pos+=4;cursor+=skip*4
                for _ in range(n):
                    value=struct.unpack_from('<I',buffers[i],cursor)[0]
                    mask=0x7fffffff if typ and value>>28 else 0xffffffff
                    value=target(value&0x0fffffff) if typ else target(value)
                    if typ:value=(value-(bases[i]+cursor))&mask
                    struct.pack_into('<I',buffers[i],cursor,value)
                    address=old[i]+cursor;assert address in expected
                    wanted,relative,prel31=expected[address]
                    want=target(wanted-base)
                    if relative:want=(want-(bases[i]+cursor))&(0x7fffffff if prel31 else 0xffffffff)
                    assert value==want,(address,value,want)
                    patched.add(address);cursor+=4
    assert pos==len(blob) and patched==set(expected)

if __name__=='__main__':
    import sys,json
    print(json.dumps(convert(sys.argv[1],sys.argv[2]),indent=2))
