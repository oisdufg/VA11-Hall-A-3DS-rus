"""Stage static Day 4 visitor sprites from owned game data, outside the release."""
from pathlib import Path
import argparse
import json
import struct
from PIL import Image
from prepare import GameData


def prepare(game, project):
    folder = project / 'generated/day4'
    folder.mkdir(exist_ok=True)
    gd = GameData(game / 'data.win')
    pointers = gd.pointers('SPRT')
    # Sprite indices and draw order from the original Create/Draw events.
    layers = {
        'art': {'normal': [370, 372, 371], 'sigh': [373, 374]},
        'betty': {'normal': [375, 377, 376], 'grumpy': [378, 380, 379],
                  'sigh': [381, 382], 'drunk': [383, 385, 384]},
        'deal': {'normal': [386, 388, 387]},
        'stream': {'normal': [287, 289, 288], 'ex': [291, 289],
                   'pout': [295, 297, 296], 'drunk': [292, 294, 293], 'drunkex': [298]},
    }
    def sprite(index):
        p = pointers[index]
        return gd.sprite(gd.string(gd.u(p))), struct.unpack_from('<ii', gd.data, p + 48)

    manifest = {}
    preview = Image.new('RGBA', (5 * 200, 4 * 270), (27, 17, 38, 255))
    for row, (actor, variants) in enumerate(layers.items()):
        for column, (face, ids) in enumerate(variants.items()):
            base, (ox, oy) = sprite(ids[0])
            for index in ids[1:]:
                overlay, (x, y) = sprite(index)
                base.alpha_composite(overlay, (ox - x, oy - y))
            if actor == 'stream':
                camera, (x, y) = sprite(290)
                base.alpha_composite(camera, (ox - x - 19, oy - y - 220))
            image = base.resize((round(base.width / 2), round(base.height / 2)), Image.Resampling.NEAREST)
            filename = f'{actor}-{face}.png'
            image.save(folder / filename)
            manifest[filename] = {'width': image.width, 'height': image.height, 'layers': ids}
            preview.alpha_composite(image, (column * 200 + (200 - image.width) // 2, row * 270 + 250 - image.height))
    preview.convert('RGB').save(folder / 'actors-preview.png')
    (folder / 'assets-manifest.json').write_text(json.dumps(manifest, indent=2))
    print(f'Prepared {len(manifest)} full-body static sprites in {folder}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('game', type=Path)
    args = parser.parse_args()
    prepare(args.game, Path(__file__).resolve().parents[1])
