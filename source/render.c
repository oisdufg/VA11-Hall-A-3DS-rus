#include "render.h"
#include "assets.h"
#include "font.h"
#include "story.h"
#include "actors.h"
#include "recipes.h"
#include "tokens.h"
#include <stdio.h>
#include "menu.h"
#include "home_assets.h"

typedef struct {uint8_t *p;int w;} Screen;
static const uint32_t BG=0x110e1d, PANEL=0x21172e, INK=0xf0e6ec, MUTED=0xaa96b5, PINK=0xf56ea9, CYAN=0x6edbda;
static void pixel(Screen s,int x,int y,uint32_t c) {
    if(x<0 || x>=s.w || y<0 || y>=240)return;
    int n=(x*240+239-y)*3;
    s.p[n]=(uint8_t)c;s.p[n+1]=(uint8_t)(c>>8);s.p[n+2]=(uint8_t)(c>>16);
}
static void rect(Screen s,int x,int y,int w,int h,uint32_t c) {
    int x1=x<0?0:x,y1=y<0?0:y,x2=x+w>s.w?s.w:x+w,y2=y+h>240?240:y+h;
    for(int xx=x1;xx<x2;++xx){
        uint8_t *p=s.p+(xx*240+240-y2)*3;
        for(int yy=y1;yy<y2;++yy){*p++=(uint8_t)c;*p++=(uint8_t)(c>>8);*p++=(uint8_t)(c>>16);}
    }
}
static unsigned codepoint(const char **p) {
    const unsigned char *s=(const unsigned char *)*p;
    unsigned c=*s++;
    if(c>=0xc0 && c<0xe0){c=((c&31)<<6)|(*s++&63);}
    else if(c>=0xe0 && c<0xf0){c=((c&15)<<12)|((s[0]&63)<<6)|(s[1]&63);s+=2;}
    *p=(const char *)s;return c;
}
static void text(Screen s,int x,int y,const char *str,uint32_t color) {
    int left=x;
    while(*str) {
        unsigned cp=codepoint(&str);
        if(cp=='\n'){x=left;y+=16;continue;}
        int index=-1;
        if(cp>=32 && cp<127)index=(int)cp-32;
        else if(cp>=0x400 && cp<0x460)index=95+(int)cp-0x400;
        else for(unsigned i=191;i<sizeof(fontCodes)/sizeof(fontCodes[0]);++i)if(fontCodes[i]==cp){index=(int)i;break;}
        if(index<0)index='?'-32;
        for(int yy=0;yy<15;++yy)for(int xx=0;xx<8;++xx)if(fontBits[index][yy]&(1<<(7-xx)))pixel(s,x+xx,y+yy,color);
        x+=8;
    }
}
static void number(Screen s,int x,int y,int n,uint32_t c) {
    char buf[24];int k=23;buf[k]=0;unsigned value=n<0?(unsigned)-n:(unsigned)n;
    do{buf[--k]=(char)('0'+value%10);value/=10;}while(value);
    if(n<0)buf[--k]='-';
    text(s,x,y,buf+k,c);
}
static void sprite(Screen s,int x,int y,const Sprite *im) {
    const uint8_t *p=im->rgba;
    for(int yy=0;yy<im->h;++yy)for(int xx=0;xx<im->w;++xx,p+=4)if(p[3]>127)pixel(s,x+xx,y+yy,((uint32_t)p[0]<<16)|((uint32_t)p[1]<<8)|p[2]);
}
static void button(Screen s,int x,int y,int w,const char *label,bool active) {
    rect(s,x,y,w,25,active?0x44304f:0x211c2b);
    rect(s,x,y,w,1,active?PINK:0x51405a);text(s,x+6,y+5,label,active?INK:MUTED);
}
static const char *order(int n) {
    switch(n) {
    case 1:return "Сахарный прилив";case 2:return "Взрыв на Луне";
    case 3:case 4:return "Большое пиво";case 5:case 7:return "Пиво";
    case 6:return "Большой горький, без алкоголя";
    case 8:return "Большой Удар по печени";
    case 9:return "Сваебой (или Суплекс)";
    case 10:return "Бон Развязон";
    case 11:return "Маленький сладкий со льдом";
    case 12:return "Изысканный напиток (classy)";
    case 13:case 16:return "Брендини";
    case 14:return "Что-нибудь успокаивающее";
    case 15:return "Пианист / Пианистка";
    case 17:return "Как обычно: пиво";
    case 18:case 23:return "Взрыв на Марсе (Marsblast)";
    case 19:case 26:return "Что-нибудь горькое";
    case 20:return "Пианистка";
    case 21:return "Взрыв на Луне";
    case 22:return "Большой Sunshine Cloud + Gut Punch";
    case 24:return "Похожий на чай: горький, женственный";
    case 25:return "Что-нибудь мягкое";
    case 174:return "Пиво или другой алкоголь";
    default:return "Заказ посетителя";
    }
}
void draw_screens(uint8_t *top,uint8_t *bottom,const View *v) {
    Screen t={top,400},b={bottom,320};
    rect(t,0,0,400,240,BG);rect(b,0,0,320,240,BG);
    text(t,12,3,"VA-11 HALL-A",PINK);text(t,224,3,v->state.cur_day==2?"ДЕНЬ 2 / 0.5.0":"ДЕНЬ 1 / 0.5.0",MUTED);
    sprite(t,10,22,&background);
    /* The original bar backdrop is drawn at (11,18) in room coordinates. */
    if(v->annaUntil)sprite(t,10+(239-11)*264/338,22+(44-18)*264/338,&anna_tv);
    int ln=blockStart[v->block]+v->line;
    const Line *line=&story[ln];
    for(int i=0;i<9;++i)if(v->visible[i]) {
        const Sprite *im=actors[i][v->face[i]];
        if(im)sprite(t,10+v->position[i]*264/338-im->w/2,148-im->h,im);
    }
    rect(t,274,22,7,126,BG);
    rect(t,281,25,108,122,PANEL);sprite(t,290,43,&jill);
    text(t,291,27,"ДЖИЛЛ",PINK);
    rect(t,8,148,384,91,0x171121);rect(t,8,148,384,1,PINK);
    if(v->mode==0) {
        text(t,16,151,line->name,CYAN);
        text(t,16,168,line->text,INK);
        text(t,335,151,"A >>",PINK);
    } else if(v->mode==1) {
        text(t,16,153,"ЗАКАЗ",CYAN);
        text(t,16,174,order(v->state.orders),INK);
        text(t,16,196,v->state.slotamount==2?(v->state.heldRecipe?"Напиток 2/2. X: подать оба":"Напиток 1/2. X: отложить в слот"):"Y: рецепт   A: шейкер   X: подать",MUTED);
        text(t,16,215,"B: сброс   L: лёд   R: выдержка",MUTED);
    } else if(v->mode==6) {
        text(t,16,153,"GAME OVER",PINK);
        text(t,16,177,"Дана отправила Джилл домой.",INK);
        text(t,16,199,"A: загрузить / начать заново",CYAN);
        text(t,16,219,"B: главное меню",MUTED);
    } else if(v->mode==3) {
        text(t,16,153,"ПЕРЕРЫВ",CYAN);
        text(t,16,178,"Время немного отдохнуть.",INK);
        text(t,16,210,"A: продолжить смену",PINK);
    } else if(v->mode==2) {
        text(t,16,153,v->state.cur_day==2?"ВТОРОЙ ДЕНЬ ЗАВЕРШЁН":"ПЕРВЫЙ ДЕНЬ ЗАВЕРШЁН",CYAN);
        text(t,16,178,"Выручка:",INK);number(t,120,178,v->state.cash,INK);
        text(t,196,178,"Чаевые:",INK);number(t,268,178,v->state.tips,INK);
        text(t,16,198,"Ошибки:",MUTED);number(t,88,198,v->state.mistakes,MUTED);
        text(t,16,219,v->state.cur_day==1?"A: домой, день 2   START: выход":"SELECT: меню   START: выход",PINK);
    } else {
        text(t,16,160,"Ошибка перехода. SELECT: меню",PINK);
        number(t,16,190,v->state.cur_client,INK);number(t,70,190,v->state.cur_stage,INK);
    }
    if(v->mode==6){
        text(b,16,22,"СМЕНА ОКОНЧЕНА ДОСРОЧНО",PINK);
        text(b,16,63,"Последний сейв сохранён.",INK);
        text(b,16,94,"A: загрузить сохранение",CYAN);
        text(b,16,118,"Без сейва: новый первый день.",MUTED);
        text(b,16,158,"B: главное меню",INK);
        text(b,16,198,"START: выход",MUTED);
        return;
    }
    text(b,8,4,v->state.cur_client==0?"БАР / ОБУЧЕНИЕ":v->state.cur_day==2?"БАР / ДЕНЬ 2":"БАР / ДЕНЬ 1",PINK);
    if(v->mode==1) {
        if(v->mixer.running) {
            text(b,8,25,v->now-v->mixer.started>=5000?"Взболтано! A: остановить":"Смешиваем... A: остановить",CYAN);
        } else if(v->mixer.ready)text(b,8,25,mixer_identify(&v->mixer)?recipes[mixer_identify(&v->mixer)-1].name:"Неудачный коктейль: B сброс",CYAN);
        else text(b,8,25,"Добавь ингредиенты. Y: рецепт",MUTED);
    } else text(b,8,25,"A: читать дальше   Y: рецепты",MUTED);
    const char *names[]={"Адельгид","Бронсон-экстракт","Порошковая дельта","Фланергид","Кармотрин"};
    uint32_t colors[]={0xf16c97,0xdbc167,0x7299e7,0x82d092,0xc695dd};
    for(int i=0;i<5;++i) {
        int y=49+i*23;
        rect(b,7,y,306,21,i==v->selected?0x35253f:PANEL);rect(b,7,y,3,21,colors[i]);
        text(b,15,y+3,names[i],colors[i]);
        text(b,224,y+3,"-",MUTED);number(b,252,y+3,v->mixer.amount[i],INK);text(b,292,y+3,"+",INK);
    }
    button(b,8,168,145,v->mixer.ice?"L: Лёд [ДА]":"L: Лёд [нет]",v->mixer.ice);
    button(b,160,168,152,v->mixer.aged?"R: Выдержка [ДА]":"R: Выдержка [-]",v->mixer.aged);
    button(b,8,198,96,"B: Сброс",v->mode==1);
    button(b,110,198,100,v->mixer.running?"A: Стоп":"A: Шейкер",v->mode==1&&!v->mixer.ready);
    button(b,216,198,96,"X: Подать",v->mode==1&&v->mixer.ready);
    text(b,8,226,"START: выход",MUTED);
    text(b,168,226,v->audio==1?"Звук: включён":v->audio==2?"Звук: нет PCM":"Звук: нет DSP",MUTED);
    if(v->saveError)text(b,8,226,"Ошибка записи SD!",PINK);
    if(v->overlay==1) {
        rect(b,0,0,320,240,BG);rect(b,4,3,312,2,PINK);
        const Recipe *r=&recipes[recipeBook[v->recipe]];
        text(b,12,12,"РЕЦЕПТЫ   < L / R >",PINK);
        text(b,12,36,r->name,CYAN);
        if(r->id==TOK_tea){
            text(b,12,65,"Готовый напиток: чай Мулан.",INK);
            text(b,12,90,"Шейкер не нужен.",MUTED);
            text(b,12,120,v->mode==1?"A: налить   X: затем подать":"Наливать можно при заказе.",CYAN);
            text(b,12,155,"Доступен без покупки в бете.",MUTED);
        }else{
        for(int i=0;i<5;++i){text(b,12,60+i*16,names[i],INK);if(i==4 && r->optional)text(b,172,60+i*16,"по вкусу",INK);else number(b,172,60+i*16,r->amount[i],INK);}
        text(b,12,146,r->ice?"Лёд: да":"Лёд: нет",CYAN);
        text(b,124,146,r->aged?"Выдержка: да":"Выдержка: нет",CYAN);
        text(b,12,166,r->blended?"Взболтать: 5 секунд и дольше.":"Смешать: менее 5 секунд.",INK);
        text(b,12,184,r->size==TOK_big?"Уже большой. Максимум 20 частей.":"Большой: удвой. Максимум 20.",MUTED);
        const char *flavor=r->flavor==TOK_sweet?"Сладкий":r->flavor==TOK_bitter?"Горький":r->flavor==TOK_spicy?"Острый":r->flavor==TOK_bubbly?"Газовый":"Кислый";
        text(b,12,200,flavor,CYAN);
        text(b,100,200,r->kind==TOK_classy?"Изысканный":r->kind==TOK_girly?"Женственный":r->kind==TOK_manly?"Мужественный":"Классический",CYAN);
        }
        text(b,12,220,"Y / B: закрыть   L/R: листать",PINK);
    } else if(v->overlay==2) {
        rect(b,4,60,312,125,BG);rect(b,4,60,312,2,PINK);
        text(b,18,80,"ПАУЗА",INK);
        text(b,18,110,v->failed?"A: главное меню":"A: сохранить и открыть меню",PINK);
        text(b,18,143,"B: вернуться к игре",MUTED);
    }
}

void draw_menu(uint8_t *top,uint8_t *bottom,const View *v,const Menu *u) {
    Screen t={top,400},b={bottom,320};rect(t,0,0,400,240,BG);rect(b,0,0,320,240,BG);
    if(u->screen==UI_CREDITS){
        rect(t,24,35,352,2,PINK);
        text(t,32,57,"VA-11 HALL-A / 3DS",PINK);
        text(t,32,94,"Original game developed by",MUTED);
        text(t,32,116,"Sukeban Games",INK);
        text(t,32,149,"Music by Garoad",INK);
        text(t,32,174,"Published by Ysbryd Games",INK);
        text(t,32,211,"Unofficial fan-made port",CYAN);
        text(b,16,21,"build with neumiraie",PINK);
        text(b,16,57,"Not affiliated with or endorsed",MUTED);
        text(b,16,75,"by the original creators.",MUTED);
        rect(b,16,105,288,1,0x51405a);
        text(b,16,125,"Unofficial Russian translation",INK);
        text(b,16,148,"Source: https://koshk.sbs/",CYAN);
        text(b,16,174,"Credit to its translation team.",MUTED);
        text(b,16,216,"A / touch: main menu",PINK);
        return;
    }
    if(u->screen==UI_TITLE || u->screen==UI_NEW || u->screen==UI_HELP){
        rect(t,24,48,352,2,PINK);
        text(t,48,82,"VA-11 HALL-A / NINTENDO 3DS",PINK);
        text(t,48,126,"Unofficial fan-made port",CYAN);
        text(t,48,167,"build with neumiraie",MUTED);
    }else{
        text(t,12,6,v->state.cur_day==2?"КВАРТИРА ДЖИЛЛ / ДЕНЬ 2":"КВАРТИРА ДЖИЛЛ / ДЕНЬ 1",PINK);
        sprite(t,62,27,&home_room);
        text(t,48,219,"Почитаю перед работой...",CYAN);
    }
    if(u->screen==UI_ARTICLE){
        const Sprite *im=menu_phone_page(v,u);
        for(int yy=0;yy<188;++yy)for(int xx=0;xx<im->w;++xx){
            const uint8_t *p=im->rgba+((yy+u->scroll)*im->w+xx)*4;
            if(p[3]>127)pixel(b,60+xx,24+yy,((uint32_t)p[0]<<16)|((uint32_t)p[1]<<8)|p[2]);
        }
        text(b,8,3,u->app==0?"ДОПОЛНЕННАЯ ПРАВДА":u->app==1?"DANGER/U/":"БЛОГ КИРЫ МИКИ",PINK);
        text(b,12,96,"ВВЕРХ",MUTED);text(b,270,96,"ВНИЗ",MUTED);
        text(b,12,220,"B: назад   вверх/вниз: листать",PINK);
        return;
    }
    if(u->screen==UI_HELP){
        text(b,12,8,"УПРАВЛЕНИЕ",PINK);
        text(b,12,36,"A: диалог / шейкер\nX: подать   B: сброс\nY: рецепты   L/R: лёд/выдержка\nКрестовина: ингредиенты\nSELECT: пауза и главное меню\nSTART: сохранить и выйти",INK);
        text(b,12,146,"Смешать: менее 5 секунд.\nВзболтать: от 5 секунд.\nАвтосейв: в конце дня.",CYAN);
        text(b,12,218,"A / B: назад",PINK);return;
    }
    const char *title="",*items[4]={0};int count=3;
    if(u->screen==UI_TITLE){title="VA-11 HALL-A / 3DS 0.5.0";items[0]=u->hasSave?"Продолжить":"Продолжить (нет сохранения)";items[1]="Новая игра";items[2]="Управление";items[3]="Выход";count=4;}
    if(u->screen==UI_NEW){title="НОВАЯ ИГРА";items[0]="С обучением";items[1]="Сразу первый день";items[2]="Отмена";}
    if(u->screen==UI_HOME){title=v->state.cur_day==2?"ДОМ / 14 ДЕКАБРЯ":"ДОМ / 13 ДЕКАБРЯ";items[0]="Телефон";items[1]="На работу";items[2]="Сохранить";}
    if(u->screen==UI_PHONE){title="ТЕЛЕФОН";items[0]="Дополненная правда";items[1]="danger/u/";items[2]="Блог Киры Мики";}
    if(u->screen==UI_LIST){
        static const char *names[3][3]={{"Массовая эмиграция","Новая угроза: вандерлендеры","Киборг на каблуках"},{"Концерт Мики","Поговорим об Alice_Rabbit","Концерт Мики 2"},{"Как я отдыхаю","Концерт под куполом!","Спасибо, Глитч-Сити!"}};
        title=u->app==0?"НОВОСТИ":u->app==1?"DANGER/U/":"КИРА МИКИ";
        for(int i=0;i<3;++i)items[i]=names[u->app][i];
        if(v->state.cur_day==2 && u->app==0){items[0]="Местная героиня";items[1]=v->state.dondrunk1?"70% наших читателей...":"Беспорядки усиливаются";items[2]=v->state.dondrunk1?"Кем может быть Alice_Rabbit?":"Лечение токийского гриппа";}
    }
    text(b,12,10,title,PINK);
    for(int i=0;i<count;++i)button(b,16,48+i*38,288,items[i],u->selection==i);
    if(u->screen==UI_NEW && u->hasSave)text(b,12,174,"Текущий прогресс будет заменён.",MUTED);
    if(u->screen==UI_HOME && u->notice)text(b,12,174,"Сохранение отправлено на SD.",CYAN);
    text(b,12,218,"A: выбрать   B: назад",PINK);
    if(v->saveError)text(b,12,196,"Ошибка записи SD!",PINK);
}
