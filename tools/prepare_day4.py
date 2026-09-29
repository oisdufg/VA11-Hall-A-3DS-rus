"""Prepare staged Day 4 logic from the owner's game; leaves Days 1-3 intact."""
from pathlib import Path
import argparse
import json
import re


def prepare(game, decompiled, project):
    generated = project / 'generated'
    output = generated / 'day4'
    output.mkdir(exist_ok=True)
    scripts = [(decompiled / f'gml_Script_{name}4control.gml').read_text()
               for name in ('day', 'mix')]
    # Shop-related distraction remains deferred, as in Days 1-3.
    scripts[0] = re.sub(r'choose\([^)]*\)', '0', scripts[0]).replace('distractioncheck()', '1')
    prior_fields = json.loads((generated / 'state-fields.json').read_text())
    tokens = json.loads((generated / 'day1-metadata.json').read_text(encoding='utf8'))['tokens']
    old_tokens = dict(tokens)
    for word in sorted(set(re.findall(r'"([^"\n]*)"', ''.join(scripts)))):
        if word not in tokens:
            tokens[word] = max(tokens.values()) + 1
    additional = set(re.findall(r'global\.(\w+)', ''.join(scripts)))
    additional -= {'ch4'} | {f'odstr{i}' for i in range(200)}
    fields = prior_fields + sorted(additional - set(prior_fields))

    def translate(source):
        source = re.sub(r'textbox_create\(global.ch4, (\d+), 1\);',
                        lambda m: f'return {500 + int(m[1])};', source)
        source = re.sub(r'instance_create\(x, y, (305|308)\);',
                        lambda m: 'return ' + ('-2' if m[1] == '305' else '-3') + ';', source)
        source = re.sub(r'mixertips_double\((\d+), (\d+), (\d+), (\d+), (\d+), (\d+)\);',
                        lambda m: f's->shouldpay={m[1]};s->rightdrink1={m[2]};s->rightdrink2={m[3]};s->big_able1={m[4]};s->big_able2={m[5]};s->tipping={m[6]};', source)
        source = re.sub(r'mixertips\((\d+), (\d+), (\d+), (\d+)\);',
                        lambda m: f's->shouldpay={m[1]};s->rightdrink={m[2]};s->big_able={m[3]};s->tipping={m[4]};', source)
        source = re.sub(r'global.odstr(\d+)', r'\1', source)
        source = re.sub(r'global\.(\w+)', r's->\1', source)
        source = re.sub(r'"([^"\n]*)"', lambda m: str(tokens[m[1]]), source)
        source = source.replace('exit;', 'return 0;')
        # A completed client switch must not accidentally fall into the next client.
        source = re.sub(r'\n    case ', '\n        return 0;\n    case ', source)
        source = re.sub(r'\{\n        return 0;\n    case ', '{\n    case ', source, count=1)
        source = source.replace('\n            case ', '\n                /* fall through */\n            case ')
        assert not re.search(r'global\.|textbox_create|instance_create|mixertips|choose\(|distractioncheck', source)
        return source + '\nreturn 0;\n'

    (output / 'state.h').write_text('#pragma once\ntypedef struct {\n' + ''.join(f'int {f};\n' for f in fields) + '} State;\n')
    (output / 'rules.c').write_text('#include "state.h"\n' + ''.join(
        f'int {name}4_rule(State *s){{\n{translate(script)}}}\n'
        for name, script in zip(('day', 'mix'), scripts)))
    (output / 'state-fields.json').write_text(json.dumps(fields))
    (output / 'tokens.json').write_text(json.dumps(tokens))
    text = (game / 'scripts/eng/script4.txt').read_text(encoding='utf-8-sig')
    blocks = {}
    current = None
    # E tags delimit blocks even when attached to the previous spoken line.
    for part in re.split(r'(\[E:\d+\])', text):
        match = re.fullmatch(r'\[E:(\d+)\]', part)
        if match:
            current = 500 + int(match[1])
        elif current is not None and re.sub(r'\[[^\]]*\]', '', part).strip():
            blocks[current] = part
    (output / 'story.json').write_text(json.dumps(blocks, ensure_ascii=False, indent=2), encoding='utf8')
    referenced = sorted({500 + int(n) for s in scripts for n in re.findall(r'textbox_create\(global.ch4, (\d+), 1\)', s)})
    assert set(referenced) <= blocks.keys(), 'Rule refers to a missing story block'
    faces = {}
    for actor, face in re.findall(r'\[XS:(\w+)face,([^\]]*)\]', text):
        faces.setdefault(actor, set()).add(face)
    manifest = {
        'status': 'staged logic; not yet enabled in the playable build',
        'offset': 500, 'story_blocks': sorted(blocks), 'rule_blocks': referenced,
        'actors': sorted(set(re.findall(r'\[SHOWF?:[^,]+,sprite_(\w+)\]', text))),
        'faces': {a: sorted(v) for a, v in faces.items()},
        'command_types': sorted(set(re.findall(r'\[([^:\]]+):', text))),
        'state_commands': sorted(set(re.findall(r'\[XS:([^\]]+)\]', text))),
        'orders': sorted({int(n) for s in scripts for n in re.findall(r'global.odstr(\d+)', s)}),
        'new_fields': fields[len(prior_fields):],
        'new_tokens': {k: v for k, v in tokens.items() if k not in old_tokens},
        'preserved_state_prefix': len(prior_fields),
        'pending': ['Actor composition and rendering', 'Runtime commands and story pages',
                    'Second-drink kind and alcohol handling', 'Day 3 to Day 4 apartment transition',
                    'Save migration', 'Day 4 phone news', 'Full shift and console checks'],
    }
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('game', type=Path)
    parser.add_argument('decompiled', type=Path)
    args = parser.parse_args()
    prepare(args.game, args.decompiled, Path(__file__).resolve().parents[1])
