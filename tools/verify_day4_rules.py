"""Compile staged Day 4 rules for ARMv6K and execute order tests with Unicorn."""
from pathlib import Path
import argparse
import ctypes as C
import io
import json
import os
import subprocess
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC


def verify(toolchain, project):
    folder = project / 'generated/day4'
    gcc = toolchain / 'bin/arm-none-eabi-gcc.exe'
    target = folder / 'rules.elf'
    env = dict(os.environ, PATH=str(gcc.parent) + os.pathsep + os.environ['PATH'])
    command = [str(gcc), '-march=armv6k', '-mtune=mpcore', '-marm', '-O2',
               '-Wall', '-Wextra', '-Werror', '-nostdlib', '-Wl,-Ttext=0x100000',
               '-Wl,-e,day4_rule', str(folder / 'rules.c'), '-o', str(target)]
    subprocess.run(command, check=True, env=env)
    fields = json.loads((folder / 'state-fields.json').read_text())
    tokens = json.loads((folder / 'tokens.json').read_text())
    old_fields = json.loads((project / 'generated/state-fields.json').read_text())
    old_tokens = json.loads((project / 'generated/day1-metadata.json').read_text(encoding='utf8'))['tokens']
    assert fields[:len(old_fields)] == old_fields
    assert all(tokens[k] == v for k, v in old_tokens.items())

    class State(C.LittleEndianStructure):
        _fields_ = [(f, C.c_int32) for f in fields]

    elf = ELFFile(io.BytesIO(target.read_bytes()))
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.mem_map(0x10000, 0x200000)
    uc.mem_map(0x300000, 0x100000)
    for segment in elf.iter_segments():
        if segment['p_type'] == 'PT_LOAD':
            uc.mem_write(segment['p_vaddr'], segment.data())
    symbols = {s.name: s['st_value'] for s in elf.get_section_by_name('.symtab').iter_symbols()}
    seen = set()
    calls = 0

    def run(name, state):
        nonlocal calls
        uc.mem_write(0x300000, bytes(state))
        uc.reg_write(UC_ARM_REG_R0, 0x300000)
        uc.reg_write(UC_ARM_REG_SP, 0x3fff00)
        uc.reg_write(UC_ARM_REG_LR, 0x200000)
        uc.emu_start(symbols[name], 0x200000, count=100000)
        assert uc.reg_read(UC_ARM_REG_PC) == 0x200000
        result = C.c_int32(uc.reg_read(UC_ARM_REG_R0)).value
        changed = State.from_buffer_copy(uc.mem_read(0x300000, C.sizeof(State)))
        calls += 1
        if result > 0:
            seen.add(result)
        return result, changed

    recipes = json.loads((project / 'generated/recipes.json').read_text())
    def order(client, stage, a, b=None):
        s = State(cur_client=client, cur_stage=stage)
        for suffix, recipe in [('a', a), ('b', b)]:
            if recipe is None:
                continue
            for field, prop in [('bevid', 'id'), ('drinksize', 'size'), ('kind', 'kind')]:
                setattr(s, field + '_' + suffix, tokens[recipe[prop]])
        return run('mix4_rule', s)

    for a in recipes:
        for client, stage in [(1, 3), (1, 5), (2, 7), (2, 9), (2, 14), (3, 7), (4, 4), (4, 9)]:
            block, s = order(client, stage, a)
            assert 501 <= block <= 572 and s.shouldpay == 1
            if (client, stage) == (2, 7):
                assert bool(s.rightdrink) == (a['kind'] in ('promo', 'manly'))
            if (client, stage) == (2, 14):
                assert s.rightdrink == 1, 'Streaming accepts any recognized final drink'
        for b in recipes:
            for stage, wanted, both, one, neither in [(2, 'beer', 524, 526, 527), (8, 'btini', 537, 538, 539)]:
                result, s = order(3, stage, a, b)
                correct = [a['id'] == wanted, b['id'] == wanted]
                expected = both if all(correct) else one if any(correct) else neither
                if stage == 2 and all(correct) and a['size'] == b['size'] == 'big':
                    expected = 525
                assert result == expected
                assert [s.rightdrink1, s.rightdrink2] == list(map(int, correct))
            result, s = order(3, 11, a, b)
            count = int(a['kind'] == 'manly') + int(b['kind'] == 'manly')
            assert result == {0: 545, 1: 544, 2: 543}[count]
            # The original accepts both slots when at least one drink is manly.
            assert s.rightdrink1 == s.rightdrink2 == int(count > 0)

    # Enumerate controller branches, including flags carried from previous days.
    for client in (-2, 1, 2, 3, 4):
        for stage in range(1, 19):
            for bits in range(64):
                s = State(cur_client=client, cur_stage=stage, drunklevel_a=30 if bits & 1 else 0)
                for field, bit in [('streamdrunk1', 2), ('ingdrunk1', 4)]:
                    setattr(s, field, int(bool(bits & bit)))
                for field, bit in [('stream1', 8), ('stream2', 16), ('stel1', 8), ('stel2', 16), ('jamie2', 32)]:
                    setattr(s, field, tokens['right' if bits & bit else 'wrong'])
                s.db1 = tokens['bbeer' if bits & 8 else '2beer']
                s.db2 = tokens['1btini' if bits & 16 else '2btini']
                result, changed = run('day4_rule', s)
                assert result in (0, -2, -3) or 501 <= result <= 572
                if client == 3 and stage == 6:
                    assert (result, changed.slotamount) == ((532, 1) if bits & 8 else (536, 2))
    assert seen == set(range(501, 573)), ('uncovered rules', sorted(set(range(501, 573)) - seen))
    report = {'passed': True, 'arm_rule_calls': calls, 'recipe_pairs': len(recipes) ** 2,
              'rule_blocks': len(seen), 'existing_state_and_tokens_preserved': True,
              'scope': 'Isolated ARM rules only; full runtime, story command sequence, sprites and console not tested.'}
    (folder / 'test-report.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('toolchain', type=Path)
    args = parser.parse_args()
    verify(args.toolchain.resolve(), Path(__file__).resolve().parents[1])
