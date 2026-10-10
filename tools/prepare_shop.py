"""Extract local room decorations and original shop prices from the owner's game."""
from pathlib import Path
import argparse,json,re
from prepare import GameData

def prepare(game,scripts,project):
    gd=GameData(game/'data.win');gen=project/'generated'
    # Persistent bit order: never reorder the first 16 products from older saves.
    items=[('casitas',500,'Глиняные домики'),('maneki',501,'Манэки-нэко'),
           ('miki',502,'Плакат Киры Мики'),('poster',503,'Плакат с ведьмой'),
           ('carts',504,'Картриджи'),('daruma',505,'Дарума'),
           ('yiik',506,'Фигурка Алекса'),('snatcher',507,'Киноплакат'),
           ('christmas',508,'Праздничная ёлка'),('turing',509,'Игрушечный Тьюринг'),
           ('crt',510,'Компьютер PC-9X'),('fan',511,'Вентилятор'),
           ('plant',512,'Голорастение'),('beer',513,'Пиво со скидкой'),
           ('lamp',515,'Бумажный фонарь'),('banner',516,'Знамя Киры Мики')]
    # Music products have no room sprite. The track indices refer to music.h.
    extras=[('mikisong','Your Love is a...',26),('staff','Meet the Staff',44),
            ('shoulder','Массажёр для плеч',-1),('tea','Чай Мулан',-1),
            ('song1','Hopes and Dreams',1),('song2',"JC Elton's",13),
            ('song3','Safe Haven',21),('song4','Through the Storm',27),
            ('song5','Last Call',33),('song6','Believe in Me',35),
            ('song7','Friendly Conversation',10),('song8',"You've Got Me",11),
            ('frontiersong','A New Frontier',42),('ironheart','The Girl with the Iron Heart',37)]
    header=['#pragma once','#include "assets.h"',f'#define SHOP_COUNT {len(items)}',
            'typedef struct {const char *name; int price; const Sprite *decoration; int musicTrack;} ShopItem;',
            'extern const ShopItem shopItems[SHOP_COUNT];']
    body=['#include <stddef.h>','#include "shop_assets.h"'];rows=[];metadata=[]
    for key,sprite_id,title in items:
        src=(scripts/f'gml_Object_shopbutton_{key}_Create_0.gml').read_text()
        price=int(re.search(r'price = (\d+);',src)[1])
        name=gd.string(gd.u(gd.pointers('SPRT')[sprite_id]));im=gd.sprite(name)
        body.append(f'static const uint8_t px_{key}[]={{'+','.join(map(str,im.tobytes()))+'};')
        body.append(f'static const Sprite decor_{key}={{{im.width},{im.height},px_{key}}};')
        rows.append('{'+json.dumps(title,ensure_ascii=False)+f',{price},&decor_{key},-1'+'}')
        metadata.append(dict(key=key,price=price,sprite=name))
    for key,title,track in extras:
        src=(scripts/f'gml_Object_shopbutton_{key}_Create_0.gml').read_text()
        price=int(re.search(r'price = (\d+);',src)[1])
        rows.append('{'+json.dumps(title,ensure_ascii=False)+f',{price},NULL,{track}'+'}')
        metadata.append(dict(key=key,price=price,sprite=None,musicTrack=track))
    header[2]=f'#define SHOP_COUNT {len(metadata)}'
    header.insert(3,'#define SHOP_TEA_INDEX 19')
    body.append('const ShopItem shopItems[SHOP_COUNT]={'+','.join(rows)+'};')
    (gen/'shop_assets.h').write_text('\n'.join(header),encoding='utf8')
    (gen/'shop_assets.c').write_text('\n'.join(body),encoding='utf8')
    (gen/'shop.json').write_text(json.dumps(metadata,indent=2),encoding='utf8')
    print(f'Prepared {len(metadata)} shop products, including {len(items)} room decorations (local assets only).')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('game',type=Path);p.add_argument('scripts',type=Path);a=p.parse_args()
    prepare(a.game,a.scripts,Path(__file__).resolve().parents[1])
