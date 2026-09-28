#pragma once
#include "render.h"
#include "assets.h"
enum {UI_GAME,UI_TITLE,UI_HOME,UI_PHONE,UI_LIST,UI_ARTICLE,UI_NEW,UI_HELP,UI_CREDITS};
enum {ACT_NONE,ACT_SAVE,ACT_EXIT,ACT_LOAD};
enum {NAV_UP=1,NAV_DOWN=2,NAV_LEFT=4,NAV_RIGHT=8,NAV_A=16,NAV_B=32,NAV_X=64,NAV_Y=128,NAV_TOUCH=256};
typedef struct {int screen,selection,app,article,scroll,hasSave,notice;} Menu;
void menu_init(Menu *u,int hasSave);
int menu_input(Menu *u,View *v,unsigned keys,int tx,int ty);
void draw_menu(uint8_t *top,uint8_t *bottom,const View *v,const Menu *u);

const Sprite *menu_phone_page(const View *v,const Menu *u);
