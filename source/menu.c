#include <string.h>
#include "menu.h"
#include "home_assets.h"
#include "music.h"
const Sprite *menu_phone_page(const View *v,const Menu *u){
    if(v->state.cur_day==2 && u->app==0)return day2News[v->state.dondrunk1?1:0][u->article];
    if(v->state.cur_day==3 && u->app==0)return day3News[v->state.dondrunk2?1:0][u->article];
    if(v->state.cur_day==4 && u->app==0)return day4News[(v->state.dondrunk1==1 && v->state.dondrunk3==1)?1:0][u->article];
    return phonePages[u->app][u->article];
}
void menu_init(Menu *u,int hasSave){memset(u,0,sizeof(*u));u->screen=UI_TITLE;u->hasSave=hasSave;u->selection=hasSave?0:1;}
void menu_music(Menu *u,const View *v){u->app=u->screen;u->screen=UI_MUSIC;u->selection=v->musicTrack;u->notice=v->mode==7;}
int menu_input(Menu *u,View *v,unsigned keys,int tx,int ty) {
    if(u->screen==UI_MUSIC){
        if(keys&NAV_UP)u->selection=(u->selection+MUSIC_COUNT-1)%MUSIC_COUNT;
        if(keys&NAV_DOWN)u->selection=(u->selection+1)%MUSIC_COUNT;
        if(keys&NAV_LEFT)u->selection=(u->selection+MUSIC_COUNT-5)%MUSIC_COUNT;
        if(keys&NAV_RIGHT)u->selection=(u->selection+5)%MUSIC_COUNT;
        if((keys&NAV_TOUCH) && tx>=8 && tx<312 && ty>=48 && ty<188){
            int chosen=(u->selection/5)*5+(ty-48)/28;
            if(chosen<MUSIC_COUNT){u->selection=chosen;keys|=NAV_A;}
        }
        if(keys&(NAV_A|NAV_B)){
            if(keys&NAV_A)v->musicTrack=u->selection;
            if(v->mode==7)engine_finish_jukebox(v);
            u->screen=u->app;u->selection=0;u->notice=0;
        }
        return ACT_NONE;
    }
    if(u->screen==UI_CREDITS){if(keys&(NAV_A|NAV_TOUCH))u->screen=UI_TRANSLATION;return ACT_NONE;}
    if(u->screen==UI_TRANSLATION){if(keys&(NAV_A|NAV_TOUCH))u->screen=UI_TITLE;return ACT_NONE;}
    int count=u->screen==UI_TITLE?4:u->screen==UI_NEW?3:u->screen==UI_HOME?3:3;
    if(u->screen==UI_ARTICLE){
        int limit=menu_phone_page(v,u)->h-188;
        if(keys&(NAV_DOWN|NAV_RIGHT))u->scroll+=24;
        if(keys&(NAV_UP|NAV_LEFT))u->scroll-=24;
        if(keys&NAV_TOUCH){if(tx<60)u->scroll-=120;else if(tx>=260)u->scroll+=120;}
        if(u->scroll<0)u->scroll=0;
        if(u->scroll>limit)u->scroll=limit;
        if(keys&NAV_B){u->screen=UI_LIST;u->selection=u->article;}
        return ACT_NONE;
    }
    if(u->screen==UI_HELP){if(keys&(NAV_A|NAV_B))u->screen=UI_TITLE;return ACT_NONE;}
    if(keys&NAV_UP)u->selection=(u->selection+count-1)%count;
    if(keys&NAV_DOWN)u->selection=(u->selection+1)%count;
    if((keys&NAV_TOUCH) && tx>=16 && tx<304 && ty>=48 && ty<48+count*38){u->selection=(ty-48)/38;keys|=NAV_A;}
    if(keys&NAV_B){
        if(u->screen==UI_LIST)u->screen=UI_PHONE;
        else if(u->screen==UI_PHONE)u->screen=UI_HOME;
        else if(u->screen==UI_NEW || u->screen==UI_HOME)u->screen=UI_TITLE;
        u->selection=0;return ACT_NONE;
    }
    if(!(keys&NAV_A))return ACT_NONE;
    if(u->screen==UI_TITLE){
        if(u->selection==0 && u->hasSave){if(v->failed)return ACT_LOAD;u->screen=v->mode==5?UI_HOME:UI_GAME;u->selection=0;}
        else if(u->selection==1){u->screen=UI_NEW;u->selection=0;}
        else if(u->selection==2){u->screen=UI_HELP;}
        else if(u->selection==3)return ACT_EXIT;
    }else if(u->screen==UI_NEW){
        if(u->selection==2){u->screen=UI_TITLE;u->selection=1;}
        else {int tutorial=u->selection==0;engine_start(v,1);v->mode=5;v->round=tutorial;u->screen=UI_HOME;u->selection=0;u->hasSave=1;return ACT_NONE;}
    }else if(u->screen==UI_HOME){
        if(u->selection==0){u->screen=UI_PHONE;u->selection=0;}
        else if(u->selection==1){if(v->state.cur_day>=2)v->mode=0;else {int dayOnly=!v->round;engine_start(v,dayOnly);}u->screen=UI_GAME;return ACT_NONE;}
        else {u->notice=1;return ACT_SAVE;}
    }else if(u->screen==UI_PHONE){u->app=u->selection;u->screen=UI_LIST;u->selection=0;}
    else if(u->screen==UI_LIST){u->article=u->selection;u->scroll=0;u->screen=UI_ARTICLE;}
    return ACT_NONE;
}
