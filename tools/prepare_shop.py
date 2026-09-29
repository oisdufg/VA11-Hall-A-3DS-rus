"""Extract local room decorations and original shop prices from the owner's game."""
from pathlib import Path
import argparse,json,re
from prepare import GameData

def prepare(game,scripts,project):
    gd=GameData(game/'data.win');gen=project/'generated'
    # Persistent bit order: append future products; never reorder these entries.
    items=[('casitas',500,'Глиняные домики'),('maneki',501,'Манэки-нэко'),
           ('miki',502,'Плакат Киры Мики'),('poster',503,'Плакат с ведьмой'),
           ('carts',504,'Картриджи'),('daruma',505,'Дарума'),
           ('yiik',506,'Фигурка Алекса'),('snatcher',507,'Киноплакат'),
           ('christmas',508,'Праздничная ёлка'),('turing',509,'Игрушечный Тьюринг'),
           ('crt',510,'Компьютер PC-9X'),('fan',511,'Вентилятор'),
           ('plant',512,'Голорастение'),('beer',513,'Пиво со скидкой'),
           ('lamp',515,'Бумажный фонарь'),('banner',516,'Знамя Киры Мики')]
    header=['#pragma once','#include "assets.h"',f'#define SHOP_COUNT {len(items)}',
            'typedef struct {const char *name; int price; const Sprite *decoration;} ShopItem;',
            'extern const ShopItem shopItems[SHOP_COUNT];']
    body=['#include "shop_assets.h"'];rows=[];metadata=[]
    for key,sprite_id,title in items:
        src=(scripts/f'gml_Object_shopbutton_{key}_Create_0.gml').read_text()
        price=int(re.search(r'price = (\d+);',src)[1])
        name=gd.string(gd.u(gd.pointers('SPRT')[sprite_id]));im=gd.sprite(name)
        body.append(f'static const uint8_t px_{key}[]={{'+','.join(map(str,im.tobytes()))+'};')
        body.append(f'static const Sprite decor_{key}={{{im.width},{im.height},px_{key}}};')
        rows.append('{'+json.dumps(title,ensure_ascii=False)+f',{price},&decor_{key}'+'}')
        metadata.append(dict(key=key,price=price,sprite=name))
    body.append('const ShopItem shopItems[SHOP_COUNT]={'+','.join(rows)+'};')
    (gen/'shop_assets.h').write_text('\n'.join(header),encoding='utf8')
    (gen/'shop_assets.c').write_text('\n'.join(body),encoding='utf8')
    (gen/'shop.json').write_text(json.dumps(metadata,indent=2),encoding='utf8')
    print(f'Prepared {len(items)} shop decorations and prices (local assets only).')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('game',type=Path);p.add_argument('scripts',type=Path);a=p.parse_args()
    prepare(a.game,a.scripts,Path(__file__).resolve().parents[1])
