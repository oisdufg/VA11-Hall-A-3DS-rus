#include "render.h"
#include "ui_text.h"
#include "assets.h"
#include "font.h"
#include "story.h"
#include "actors.h"
#include "music.h"
#include "recipes.h"
#include "tokens.h"
#include <stdio.h>
#include "menu.h"
#include "home_assets.h"
#include "shop_assets.h"
#include "day6_assets.h"

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
static void money(Screen s,int x,int y,int cents,uint32_t color){
    char buf[24];int k=23;buf[k]=0;
    unsigned value=(unsigned)cents;
    buf[--k]=(char)('0'+value%10);value/=10;
    buf[--k]=(char)('0'+value%10);value/=10;buf[--k]='.';
    do{buf[--k]=(char)('0'+value%10);value/=10;}while(value);
    buf[--k]='$';text(s,x,y,buf+k,color);
}
static void sprite(Screen s,int x,int y,const Sprite *im) {
    const uint8_t *p=im->rgba;
    for(int yy=0;yy<im->h;++yy)for(int xx=0;xx<im->w;++xx,p+=4)if(p[3]>127)pixel(s,x+xx,y+yy,((uint32_t)p[0]<<16)|((uint32_t)p[1]<<8)|p[2]);
}
static void sprite_scaled(Screen s,int x,int y,int w,int h,const Sprite *im) {
    for(int yy=0;yy<h;++yy)for(int xx=0;xx<w;++xx) {
        const uint8_t *p=im->rgba+4*((yy*im->h/h)*im->w+xx*im->w/w);
        if(p[3]>127)pixel(s,x+xx,y+yy,((uint32_t)p[0]<<16)|((uint32_t)p[1]<<8)|p[2]);
    }
}
static void button(Screen s,int x,int y,int w,const char *label,bool active) {
    rect(s,x,y,w,25,active?0x44304f:0x211c2b);
    rect(s,x,y,w,1,active?PINK:0x51405a);text(s,x+6,y+5,label,active?INK:MUTED);
}
void draw_screens(uint8_t *top,uint8_t *bottom,const View *v) {
    Screen t={top,400},b={bottom,320};
    rect(t,0,0,400,240,BG);rect(b,0,0,320,240,BG);
    text(t,12,3,uiStrings[UI_VA_11_HALL_A],PINK);text(t,224,3,ui_day_badge(v->state.cur_day),MUTED);
    int shake=v->shakeUntil?((v->now/50)%2?2:-2):0;
    bool day6Home=v->state.cur_day==6 && v->block>=702;
    if(day6Home)sprite_scaled(t,10,22,264,151,v->day6Beers>=7?&day6_scene_drunk:&day6_scene);
    else sprite(t,10+shake,22,&background);
    /* The original bar backdrop is drawn at (11,18) in room coordinates. */
    if(v->annaUntil)sprite(t,10+(239-11)*264/338,22+(44-18)*264/338,&anna_tv);
    if(v->news){rect(t,198,39,72,25,0x15233c);text(t,202,44,uiStrings[UI_NOVOSTI],CYAN);}
    int ln=blockStart[v->block]+v->line;
    const Line *line=&story[ln];
    for(int i=0;i<ACTOR_COUNT;++i)if(v->visible[i] && !day6Home) {
        const Sprite *im=actors[i][v->face[i]];
        if(im)sprite(t,10+shake+v->position[i]*264/338-im->w/2,148-im->h,im);
    }
    rect(t,274,22,7,126,BG);
    rect(t,281,25,108,122,PANEL);sprite(t,290,43,&jill);
    text(t,291,27,uiStrings[UI_DZHILL],PINK);
    if(v->chat){rect(t,285,115,108,32,PANEL);text(t,290,115,uiStrings[UI_CHAT_STRIMA],PINK);text(t,290,131,ui_chat_reaction(v->chat),CYAN);}
    rect(t,8,148,384,91,0x171121);rect(t,8,148,384,1,PINK);
    if(v->mode==0) {
        text(t,16,151,line->name,CYAN);
        text(t,16,168,line->text,INK);
        text(t,335,151,uiStrings[UI_A],PINK);
    } else if(v->mode==1) {
        text(t,16,153,uiStrings[UI_ZAKAZ],CYAN);
        text(t,16,174,ui_order_hint(v->state.orders),INK);
        text(t,16,196,v->state.slotamount==2?(v->state.heldRecipe?uiStrings[UI_NAPITOK_2_2_X_PODAT_OBA]:uiStrings[UI_NAPITOK_1_2_X_OTLOZHIT_V_SLOT]):uiStrings[UI_Y_RETSEPT_A_SHEYKER_X_PODAT],MUTED);
        text(t,16,215,uiStrings[UI_B_SBROS_L_LD_R_VYDERZHKA],MUTED);
    } else if(v->mode==6) {
        text(t,16,153,uiStrings[UI_GAME_OVER],PINK);
        text(t,16,177,uiStrings[UI_DANA_OTPRAVILA_DZHILL_DOMOY],INK);
        text(t,16,199,uiStrings[UI_A_ZAGRUZIT_NACHAT_ZANOVO],CYAN);
        text(t,16,219,uiStrings[UI_B_GLAVNOE_MENYU],MUTED);
    } else if(v->mode==3) {
        text(t,16,153,uiStrings[UI_PERERYV],CYAN);
        text(t,16,178,uiStrings[UI_VREMYA_NEMNOGO_OTDOHNUT],INK);
        text(t,16,210,uiStrings[UI_A_PRODOLZHIT_SMENU],PINK);
    } else if(v->mode==2) {
        text(t,16,153,ui_day_completed(v->state.cur_day),CYAN);
        if(v->state.cur_day==6)text(t,16,184,uiStrings[UI_DAY6_NO_SHIFT],INK);
        else {
            text(t,16,178,uiStrings[UI_VYRUCHKA],INK);number(t,120,178,v->state.cash,INK);
            text(t,196,178,uiStrings[UI_CHAEVYE],INK);number(t,268,178,v->state.tips,INK);
            text(t,16,198,uiStrings[UI_OSHIBKI],MUTED);number(t,88,198,v->state.mistakes,MUTED);
            text(t,144,198,uiStrings[UI_ZARABOTOK],CYAN);money(t,232,198,v->lastPayCents,CYAN);
        }
        text(t,16,219,ui_next_day_hint(v->state.cur_day),PINK);
    } else {
        text(t,16,160,uiStrings[UI_OSHIBKA_PEREHODA_SELECT_MENYU],PINK);
        number(t,16,190,v->state.cur_client,INK);number(t,70,190,v->state.cur_stage,INK);
    }
    if(v->mode==6){
        text(b,16,22,uiStrings[UI_SMENA_OKONCHENA_DOSROCHNO],PINK);
        text(b,16,63,uiStrings[UI_POSLEDNIY_SEYV_SOHRANN],INK);
        text(b,16,94,uiStrings[UI_A_ZAGRUZIT_SOHRANENIE],CYAN);
        text(b,16,118,uiStrings[UI_BEZ_SEYVA_NOVYY_PERVYY_DEN],MUTED);
        text(b,16,158,uiStrings[UI_B_GLAVNOE_MENYU],INK);
        text(b,16,198,uiStrings[UI_START_VYHOD],MUTED);
        return;
    }
    if(v->state.cur_day==6){
        text(b,12,12,uiStrings[UI_DAY6_SCENE],PINK);
        text(b,12,44,uiStrings[UI_DAY6_BEER_LABEL],INK);number(b,148,44,v->day6Beers,CYAN);
        for(int i=0;i<12;++i)rect(b,12+i*25,73,19,12,i<v->day6Beers?PINK:PANEL);
        if(v->mode==0 && v->block>=702)text(b,12,115,uiStrings[UI_DAY6_DRINK_HINT],CYAN);
        if(v->mode==0)text(b,12,151,uiStrings[UI_DAY6_DIALOGUE_HINT],INK);
        text(b,12,218,uiStrings[UI_START_VYHOD],MUTED);
        if(v->overlay==2){
            rect(b,4,60,312,125,BG);rect(b,4,60,312,2,PINK);
            text(b,18,80,uiStrings[UI_PAUZA],INK);
            text(b,18,110,uiStrings[UI_A_SOHRANIT_I_OTKRYT_MENYU],PINK);
            text(b,18,143,uiStrings[UI_B_VERNUTSYA_K_IGRE],MUTED);
            text(b,18,165,uiStrings[UI_X_VYBRAT_MUZYKU],CYAN);
        }
        return;
    }
    text(b,8,4,ui_bar_heading(v->state.cur_day,v->state.cur_client==0),PINK);
    if(v->mode==1) {
        if(v->mixer.running) {
            text(b,8,25,v->now-v->mixer.started>=5000?uiStrings[UI_VZBOLTANO_A_OSTANOVIT]:uiStrings[UI_SMESHIVAEM_A_OSTANOVIT],CYAN);
        } else if(v->mixer.ready)text(b,8,25,mixer_identify(&v->mixer)?recipes[mixer_identify(&v->mixer)-1].name:uiStrings[UI_NEUDACHNYY_KOKTEYL_B_SBROS],CYAN);
        else text(b,8,25,uiStrings[UI_DOBAV_INGREDIENTY_Y_RETSEPT],MUTED);
    } else text(b,8,25,uiStrings[UI_A_CHITAT_DALSHE_Y_RETSEPTY],MUTED);
    uint32_t colors[]={0xf16c97,0xdbc167,0x7299e7,0x82d092,0xc695dd};
    for(int i=0;i<5;++i) {
        int y=49+i*23;
        rect(b,7,y,306,21,i==v->selected?0x35253f:PANEL);rect(b,7,y,3,21,colors[i]);
        text(b,15,y+3,ui_ingredient_name(i),colors[i]);
        text(b,224,y+3,uiStrings[UI_EMPTY_2],MUTED);number(b,252,y+3,v->mixer.amount[i],INK);text(b,292,y+3,uiStrings[UI_EMPTY_3],INK);
    }
    button(b,8,168,145,v->mixer.ice?uiStrings[UI_L_LD_DA]:uiStrings[UI_L_LD_NET],v->mixer.ice);
    button(b,160,168,152,v->mixer.aged?uiStrings[UI_R_VYDERZHKA_DA]:uiStrings[UI_R_VYDERZHKA],v->mixer.aged);
    button(b,8,198,96,uiStrings[UI_B_SBROS],v->mode==1);
    button(b,110,198,100,v->mixer.running?uiStrings[UI_A_STOP]:uiStrings[UI_A_SHEYKER],v->mode==1&&!v->mixer.ready);
    button(b,216,198,96,uiStrings[UI_X_PODAT],v->mode==1&&v->mixer.ready);
    text(b,8,226,uiStrings[UI_START_VYHOD],MUTED);
    text(b,168,226,v->audio==1?uiStrings[UI_ZVUK_VKLYUCHN]:v->audio==2?uiStrings[UI_ZVUK_NET_PCM]:uiStrings[UI_ZVUK_NET_DSP],MUTED);
    if(v->saveError)text(b,8,226,uiStrings[UI_OSHIBKA_ZAPISI_SD],PINK);
    if(v->overlay==1) {
        rect(b,0,0,320,240,BG);rect(b,4,3,312,2,PINK);
        const Recipe *r=&recipes[recipeBook[v->recipe]];
        text(b,12,12,uiStrings[UI_RETSEPTY_L_R],PINK);
        text(b,12,36,r->name,CYAN);
        if(r->id==TOK_tea || r->id==TOK_rum || r->id==TOK_abs || r->id==TOK_fed){
            text(b,12,65,uiStrings[UI_GOTOVYY_NAPITOK_IZ_BUTYLKI],INK);
            text(b,12,90,uiStrings[UI_SHEYKER_NE_NUZHEN],MUTED);
            text(b,12,120,!engine_extra_available(v,r->id)?uiStrings[UI_POKA_NEDOSTUPNO]:v->mode==1?uiStrings[UI_A_NALIT_X_ZATEM_PODAT]:uiStrings[UI_NALIVAT_MOZHNO_PRI_ZAKAZE],CYAN);
            text(b,12,155,r->id==TOK_tea?uiStrings[UI_DOSTUPEN_BEZ_POKUPKI_V_BETE]:r->id==TOK_fed?uiStrings[UI_KLASSICHESKIY_S_ALKOGOLEM]:uiStrings[UI_DOSTUPNOST_ZAVISIT_OT_STELLY],MUTED);
        }else{
        for(int i=0;i<5;++i){text(b,12,60+i*16,ui_ingredient_name(i),INK);if(i==4 && r->optional)text(b,172,60+i*16,uiStrings[UI_PO_VKUSU],INK);else number(b,172,60+i*16,r->amount[i],INK);}
        text(b,12,146,r->ice?uiStrings[UI_LD_DA]:uiStrings[UI_LD_NET],CYAN);
        text(b,124,146,r->aged?uiStrings[UI_VYDERZHKA_DA]:uiStrings[UI_VYDERZHKA_NET],CYAN);
        text(b,12,166,r->blended?uiStrings[UI_VZBOLTAT_5_SEKUND_I_DOLSHE]:uiStrings[UI_SMESHAT_MENEE_5_SEKUND],INK);
        text(b,12,184,r->size==TOK_big?uiStrings[UI_UZHE_BOLSHOY_MAKSIMUM_20_CHASTEY]:uiStrings[UI_BOLSHOY_UDVOY_MAKSIMUM_20],MUTED);
        const char *flavor=r->flavor==TOK_sweet?uiStrings[UI_SLADKIY]:r->flavor==TOK_bitter?uiStrings[UI_GORKIY]:r->flavor==TOK_spicy?uiStrings[UI_OSTRYY]:r->flavor==TOK_bubbly?uiStrings[UI_GAZOVYY]:uiStrings[UI_KISLYY];
        text(b,12,200,flavor,CYAN);
        text(b,100,200,r->kind==TOK_classy?uiStrings[UI_IZYSKANNYY]:r->kind==TOK_girly?uiStrings[UI_ZHENSTVENNYY]:r->kind==TOK_manly?uiStrings[UI_MUZHESTVENNYY]:r->kind==TOK_promo?uiStrings[UI_REKLAMNYY_PROMO]:uiStrings[UI_KLASSICHESKIY],CYAN);
        }
        text(b,12,220,uiStrings[UI_Y_B_ZAKRYT_L_R_LISTAT],PINK);
    } else if(v->overlay==2) {
        rect(b,4,60,312,125,BG);rect(b,4,60,312,2,PINK);
        text(b,18,80,uiStrings[UI_PAUZA],INK);
        text(b,18,110,v->failed?uiStrings[UI_A_GLAVNOE_MENYU]:uiStrings[UI_A_SOHRANIT_I_OTKRYT_MENYU],PINK);
        text(b,18,143,uiStrings[UI_B_VERNUTSYA_K_IGRE],MUTED);
        text(b,18,165,uiStrings[UI_X_VYBRAT_MUZYKU],CYAN);
    }
}

void draw_menu(uint8_t *top,uint8_t *bottom,const View *v,const Menu *u) {
    Screen t={top,400},b={bottom,320};rect(t,0,0,400,240,BG);rect(b,0,0,320,240,BG);
    if(u->screen==UI_SHOP){
        text(t,16,8,uiStrings[UI_MAGAZIN_UKRASHENIYA_DLYA_DOMA],PINK);
        sprite(t,62,27,&home_room);
        for(int i=0;i<SHOP_COUNT;++i)if(v->purchases&(1u<<i))sprite(t,62,48,shopItems[i].decoration);
        text(t,16,220,uiStrings[UI_KOSHELK],CYAN);money(t,96,220,v->walletCents,CYAN);
        text(b,12,8,shopItems[u->selection].name,PINK);
        text(b,12,28,uiStrings[UI_TSENA],MUTED);money(b,64,28,shopItems[u->selection].price*100,MUTED);
        int first=(u->selection/5)*5;
        for(int i=0;i<5 && first+i<SHOP_COUNT;++i){
            int n=first+i;rect(b,8,48+i*28,304,25,n==u->selection?0x35253f:PANEL);
            text(b,16,53+i*28,shopItems[n].name,(v->purchases&(1u<<n))?MUTED:n==u->selection?CYAN:INK);
            if(v->purchases&(1u<<n))text(b,284,53+i*28,uiStrings[UI_EMPTY_3],CYAN);
        }
        const char *notice=u->notice==1?uiStrings[UI_KUPIT_A_DA_B_OTMENA]:u->notice==2?uiStrings[UI_KUPLENO_SOHRANIS_DOMA]:u->notice==3?uiStrings[UI_NEDOSTATOCHNO_DENEG]:u->notice==4?uiStrings[UI_UZHE_KUPLENO]:uiStrings[UI_A_KASANIE_VYBRAT_POKUPKU];
        text(b,12,196,notice,CYAN);text(b,12,220,uiStrings[UI_B_DOMOY_STRANITSA],PINK);return;
    }
    if(u->screen==UI_MUSIC){
        text(t,24,30,uiStrings[UI_MUZYKALNYY_AVTOMAT],PINK);
        text(t,24,68,u->notice?uiStrings[UI_VYBERI_MUZYKU_PERED_SMENOY]:uiStrings[UI_MUZYKA_DLYA_ETOY_SMENY],INK);
        text(t,24,108,uiStrings[UI_SEYCHAS_VYBRANO],MUTED);
        text(t,24,134,musicTitles[v->musicTrack],CYAN);
        text(t,24,180,uiStrings[UI_VYBRANNYY_TREK_IGRAET_PO_KRUGU],MUTED);
        text(b,12,14,uiStrings[UI_VVERH_VNIZ_TREK_STRANITSA],PINK);
        int first=(u->selection/5)*5;
        for(int i=0;i<5 && first+i<MUSIC_COUNT;++i){
            rect(b,8,48+i*28,304,25,first+i==u->selection?0x35253f:PANEL);
            text(b,16,53+i*28,musicTitles[first+i],first+i==u->selection?CYAN:INK);
        }
        text(b,12,198,uiStrings[UI_A_KASANIE_IGRAT],PINK);
        text(b,12,220,uiStrings[UI_B_OSTAVIT_TEKUSCHIY_TREK],MUTED);return;
    }
    if(u->screen==UI_CREDITS){
        rect(t,24,35,352,2,PINK);
        text(t,32,57,uiStrings[UI_VA_11_HALL_A_3DS],PINK);
        text(t,32,94,uiStrings[UI_ORIGINAL_GAME_DEVELOPED_BY],MUTED);
        text(t,32,116,uiStrings[UI_SUKEBAN_GAMES],INK);
        text(t,32,149,uiStrings[UI_MUSIC_BY_GAROAD],INK);
        text(t,32,174,uiStrings[UI_PUBLISHED_BY_YSBRYD_GAMES],INK);
        text(t,32,211,uiStrings[UI_UNOFFICIAL_FAN_MADE_PORT],CYAN);
        text(b,16,21,uiStrings[UI_BUILD_WITH_NEUMIRAIE],PINK);
        text(b,16,57,uiStrings[UI_NOT_AFFILIATED_WITH_OR_ENDORSED],MUTED);
        text(b,16,75,uiStrings[UI_BY_THE_ORIGINAL_CREATORS],MUTED);
        rect(b,16,105,288,1,0x51405a);
        text(b,16,216,uiStrings[UI_A_TOUCH_CONTINUE],PINK);
        return;
    }
    if(u->screen==UI_TRANSLATION){
        rect(t,24,35,352,2,PINK);
        text(t,32,57,uiStrings[UI_RUSSKIY_PEREVOD],PINK);
        text(t,32,101,uiStrings[UI_V_PORTE_ISPOLZUETSYA],INK);
        text(t,32,124,uiStrings[UI_NEOFITSIALNYY_RUSSKIY_PEREVOD],INK);
        text(t,32,164,uiStrings[UI_ISTOCHNIK_PEREVODA],MUTED);
        text(t,32,189,uiStrings[UI_HTTPS_KOSHK_SBS],CYAN);
        text(b,16,42,uiStrings[UI_SPASIBO_KOMANDE_PEREVODA],INK);
        text(b,16,91,uiStrings[UI_PEREVOD_SOZDAN_FANATAMI],MUTED);
        text(b,16,114,uiStrings[UI_I_NE_YAVLYAETSYA_OFITSIALNOY],MUTED);
        text(b,16,137,uiStrings[UI_LOKALIZATSIEY_SUKEBAN_GAMES],MUTED);
        text(b,16,216,uiStrings[UI_A_KASANIE_GLAVNOE_MENYU],PINK);
        return;
    }
    if(u->screen==UI_TITLE || u->screen==UI_NEW || u->screen==UI_HELP || u->screen==UI_TEST_DAYS){
        rect(t,24,48,352,2,PINK);
        text(t,48,82,uiStrings[UI_VA_11_HALL_A_NINTENDO_3DS],PINK);
        text(t,48,126,uiStrings[UI_UNOFFICIAL_FAN_MADE_PORT],CYAN);
        text(t,48,167,uiStrings[UI_BUILD_WITH_NEUMIRAIE],MUTED);
#ifdef VA11_TEST_MODE
        text(t,24,192,uiStrings[UI_TEST_DNI_1_5_KOSHELK_20000],CYAN);
        text(t,24,215,uiStrings[UI_OTDELNOE_TESTOVOE_SOHRANENIE],PINK);
#endif
    }else{
        text(t,12,6,ui_apartment_heading(v->state.cur_day),PINK);
        sprite(t,62,27,&home_room);
        for(int i=0;i<SHOP_COUNT;++i)if(v->purchases&(1u<<i))sprite(t,62,48,shopItems[i].decoration);
        text(t,24,219,uiStrings[UI_KOSHELK],CYAN);money(t,104,219,v->walletCents,CYAN);
    }
    if(u->screen==UI_ARTICLE){
        const Sprite *im=menu_phone_page(v,u);
        for(int yy=0;yy<188;++yy)for(int xx=0;xx<im->w;++xx){
            const uint8_t *p=im->rgba+((yy+u->scroll)*im->w+xx)*4;
            if(p[3]>127)pixel(b,60+xx,24+yy,((uint32_t)p[0]<<16)|((uint32_t)p[1]<<8)|p[2]);
        }
        text(b,8,3,u->app==0?uiStrings[UI_DOPOLNENNAYA_PRAVDA]:u->app==1?uiStrings[UI_DANGER_U]:uiStrings[UI_BLOG_KIRY_MIKI],PINK);
        text(b,12,96,uiStrings[UI_VVERH],MUTED);text(b,270,96,uiStrings[UI_VNIZ],MUTED);
        text(b,12,220,uiStrings[UI_B_NAZAD_VVERH_VNIZ_LISTAT],PINK);
        return;
    }
    if(u->screen==UI_HELP){
        text(b,12,8,uiStrings[UI_UPRAVLENIE],PINK);
        text(b,12,36,uiStrings[UI_A_DIALOG_SHEYKER_NX_PODAT_B_SBROS_NY_RETSEPTY_L_R_LD],INK);
        text(b,12,146,uiStrings[UI_SMESHAT_MENEE_5_SEKUND_NVZBOLTAT_OT_5_SEKUND_NAVTOSE],CYAN);
        text(b,12,218,uiStrings[UI_A_B_NAZAD],PINK);return;
    }
    const char *title=uiStrings[UI_EMPTY],*items[6]={0};int count=3;
    if(u->screen==UI_TITLE){title=uiStrings[UI_VA_11_HALL_A_3DS_0_8_0];items[0]=u->hasSave?uiStrings[UI_PRODOLZHIT]:uiStrings[UI_PRODOLZHIT_NET_SOHRANENIYA];items[1]=uiStrings[UI_NOVAYA_IGRA];items[2]=uiStrings[UI_UPRAVLENIE_2];items[3]=uiStrings[UI_VYHOD];count=4;}
#ifdef VA11_TEST_MODE
    if(u->screen==UI_TITLE){title=uiStrings[UI_VA_11_HALL_A_0_8_0_TEST];items[2]=uiStrings[UI_TEST_VYBRAT_DEN];}
    if(u->screen==UI_TEST_DAYS){title=uiStrings[UI_TEST_KVARTIRA_PERED_SMENOY];items[0]=uiStrings[UI_DEN_1];items[1]=uiStrings[UI_DEN_2];items[2]=uiStrings[UI_DEN_3];items[3]=uiStrings[UI_DEN_4];items[4]=uiStrings[UI_DEN_5];items[5]=uiStrings[UI_DAY6_TEST_LABEL];count=6;}
#endif
    if(u->screen==UI_NEW){title=uiStrings[UI_NOVAYA_IGRA_2];items[0]=uiStrings[UI_S_OBUCHENIEM];items[1]=uiStrings[UI_SRAZU_PERVYY_DEN];items[2]=uiStrings[UI_OTMENA];}
    if(u->screen==UI_HOME){title=ui_apartment_date(v->state.cur_day);items[0]=uiStrings[UI_TELEFON];items[1]=uiStrings[UI_NA_RABOTU];items[2]=uiStrings[UI_SOHRANIT];items[3]=uiStrings[UI_MAGAZIN];count=4;}
    if(u->screen==UI_PHONE){title=uiStrings[UI_TELEFON_2];items[0]=uiStrings[UI_DOPOLNENNAYA_PRAVDA_2];items[1]=uiStrings[UI_DANGER_U_2];items[2]=uiStrings[UI_BLOG_KIRY_MIKI_2];}
    if(u->screen==UI_LIST){
        const char *names[3][3]={{uiStrings[UI_MASSOVAYA_EMIGRATSIYA],uiStrings[UI_NOVAYA_UGROZA_VANDERLENDERY],uiStrings[UI_KIBORG_NA_KABLUKAH]},{uiStrings[UI_KONTSERT_MIKI],uiStrings[UI_POGOVORIM_OB_ALICE_RABBIT],uiStrings[UI_KONTSERT_MIKI_2]},{uiStrings[UI_KAK_YA_OTDYHAYU],uiStrings[UI_KONTSERT_POD_KUPOLOM],uiStrings[UI_SPASIBO_GLITCH_SITI]}};
        title=u->app==0?uiStrings[UI_NOVOSTI]:u->app==1?uiStrings[UI_DANGER_U]:uiStrings[UI_KIRA_MIKI];
        for(int i=0;i<3;++i)items[i]=names[u->app][i];
        if(v->state.cur_day==4 && u->app==0){items[0]=uiStrings[UI_NOVOSTI_16_DEKABRYA];items[1]=uiStrings[UI_VTORAYA_STATYA];items[2]=uiStrings[UI_TRETYA_STATYA];}
        if(v->state.cur_day==3 && u->app==0){items[0]=uiStrings[UI_NOVOSTI_15_DEKABRYA];items[1]=uiStrings[UI_VTORAYA_STATYA];items[2]=uiStrings[UI_TRETYA_STATYA];}
        if(v->state.cur_day==2 && u->app==0){items[0]=uiStrings[UI_MESTNAYA_GEROINYA];items[1]=v->state.dondrunk1?uiStrings[UI_70_NASHIH_CHITATELEY]:uiStrings[UI_BESPORYADKI_USILIVAYUTSYA];items[2]=v->state.dondrunk1?uiStrings[UI_KEM_MOZHET_BYT_ALICE_RABBIT]:uiStrings[UI_LECHENIE_TOKIYSKOGO_GRIPPA];}
    }
    if(u->screen==UI_LIST && v->state.cur_day==5 && u->app==0){items[0]=uiStrings[UI_NOVOSTI_17_DEKABRYA];items[1]=uiStrings[UI_VTORAYA_STATYA];items[2]=uiStrings[UI_TRETYA_STATYA];}
    if(u->screen==UI_LIST && v->state.cur_day==6 && u->app==0){items[0]=uiStrings[UI_DAY6_NEWS_TITLE];items[1]=uiStrings[UI_VTORAYA_STATYA];items[2]=uiStrings[UI_TRETYA_STATYA];}
    text(b,12,10,title,PINK);
    for(int i=0;i<count;++i)button(b,16,48+i*(u->screen==UI_TEST_DAYS?26:38),288,items[i],u->selection==i);
    if(u->screen==UI_NEW && u->hasSave)text(b,12,174,uiStrings[UI_TEKUSCHIY_PROGRESS_BUDET_ZAMENN],MUTED);
    if(u->screen==UI_HOME && u->notice)text(b,12,198,uiStrings[UI_SOHRANENIE_OTPRAVLENO_NA_SD],CYAN);
    text(b,12,218,uiStrings[UI_A_VYBRAT_B_NAZAD],PINK);
    if(v->saveError)text(b,12,196,uiStrings[UI_OSHIBKA_ZAPISI_SD],PINK);
}
