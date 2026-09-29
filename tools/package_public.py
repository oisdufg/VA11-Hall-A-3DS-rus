"""Package an explicit source-only file list, never local game resources."""
from pathlib import Path
import hashlib
import json
import zipfile


def package_public(project):
    project = Path(project).resolve()
    relative = [Path(name) for name in (
        '.gitignore', 'README.md', 'THIRD_PARTY.md', 'CHANGELOG.md',
        'BACKLOG.md', 'Makefile', 'DAY4_PROGRESS.md',
        'source/engine.c', 'source/game.c', 'source/game.h', 'source/main.c',
        'source/menu.c', 'source/menu.h', 'source/render.c', 'source/render.h',
        'tools/build_local.py', 'tools/elf2_3dsx.py', 'tools/package_public.py',
        'tools/prepare.py', 'tools/prepare_day1.py', 'tools/prepare_home.py',
        'tools/verify_day1.py', 'tools/verify_day2.py', 'tools/verify_menu.py',
        'tools/verify_features.py', 'tools/verify_day3.py',
        'tools/prepare_day4.py', 'tools/prepare_day4_assets.py', 'tools/verify_day4_rules.py',
        'tools/prepare_music.py', 'tools/verify_day4.py', 'tools/verify_music.py',
        'tools/font/LICENSE.txt', 'tools/font/NotoSansMono-Regular.ttf',
    )]
    # Only third-party license notices are included from this directory.
    relative += [f.relative_to(project) for f in sorted((project / 'licenses').glob('*.txt'))]
    for path in relative:
        if not (project / path).is_file() or (project / path).is_symlink():
            raise ValueError(f'Missing or symlinked source file: {path}')
    manifest = {
        'scope': 'Source snapshot without original game assets, translation files, generated game scripts or playable binaries. Not a standalone build kit.',
        'files': {p.as_posix(): hashlib.sha256((project / p).read_bytes()).hexdigest() for p in relative},
    }
    dest = project.parent / 'VA11-3DS-public-source.zip'
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in relative:
            archive.write(project / path, path.as_posix())
        archive.writestr('PUBLIC-SOURCE-MANIFEST.json', json.dumps(manifest, indent=2))
    with zipfile.ZipFile(dest) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == {p.as_posix() for p in relative} | {'PUBLIC-SOURCE-MANIFEST.json'}
        for path, digest in manifest['files'].items():
            assert hashlib.sha256(archive.read(path)).hexdigest() == digest
    print(f'Verified {len(relative)} source/license files: {dest}')


if __name__ == '__main__':
    package_public(Path(__file__).resolve().parents[1])
