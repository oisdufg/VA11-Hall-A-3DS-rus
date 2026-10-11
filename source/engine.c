#include <string.h>
#include "render.h"
#include "story.h"
#include "recipes.h"
#include "tokens.h"
#include "rules.h"
#include "commands.h"
#include "assets.h"
#include "actors.h"
#include "music.h"
#include "shop_assets.h"
#include "ending_assets.h"
#include "playlist.h"

int engine_focused(const View *v){
    switch(v->state.cur_day){
    case 2:return (v->purchases&(1u<<12))!=0; /* Holo-Plant */
    case 3:return (v->purchases&(1u<<16))!=0; /* Miki's song */
    case 4:return v->day4Download==1;
    case 5:return (v->purchases&(1u<<11))!=0; /* Fan */
    case 7:return (v->purchases&(1u<<5))!=0;  /* Daruma */
    case 8:return (v->purchases&(1u<<18))!=0; /* Shoulder massager */
    case 9:return (v->purchases&(1u<<13))!=0; /* Beer discount */
    case 10:return (v->purchases&(1u<<3))!=0; /* Poster */
    case 11:return (v->purchases&(1u<<8))!=0; /* Christmas tree */
    case 12:return v->state.lightdl==1;
    case 14:return (v->purchases&(1u<<6))!=0; /* Y2K game */
    case 15:return (v->purchases&(1u<<7))!=0; /* Snatcher */
    case 16:return (v->purchases&(1u<<1))!=0; /* Maneki-neko */
    case 17:return (v->purchases&(1u<<2))!=0; /* Kira Miki poster */
    case 18:return v->state.housedl==1; /* Rent */
    default:return 1;
    }
}
void engine_day4_download(View *v){
    if(v->state.cur_day!=4 || v->day4Download)return;
    if(v->walletCents>=80000){v->walletCents-=80000;v->day4Download=1;}
    else v->day4Download=2;
}
void engine_day12_download(View *v){
    if(v->state.cur_day!=12 || v->state.lightdl)return;
    if(v->walletCents>=800000){v->walletCents-=800000;v->state.lightdl=1;}
    else v->state.lightdl=2;
}
void engine_day18_rent(View *v){
    if(v->state.cur_day!=18 || v->state.housedl)return;
    if(v->walletCents>=1000000){v->walletCents-=1000000;v->state.housedl=1;}
    else v->state.housedl=2;
}

static void block(View *v,int n) {
    if(n==-2){v->cheapErrors=0;v->mode=3;return;}
    if(n==-3){v->mode=2;engine_settle(v);return;}
    if(n==-4){v->selected=0;v->mode=8;return;}
    if(n<=0 || n>=2108 || !blockCount[n]){v->mode=4;return;}
    v->block=n;v->line=0;v->mode=0;page_enter(v);
}
static int epilogue_rule(State *s){
    int seiGood=s->seidrunk1!=TOK_drunk && s->sei5==TOK_good && s->sei6==TOK_good;
    int stellaGood=s->stel1==TOK_right && s->stel2==TOK_right && s->stel4==TOK_right && s->stel5==TOK_right;
    switch(s->cur_stage){
    case 1:if(s->housedl==2)return 2106;s->cur_stage=3;return 0;
    case 3:if(seiGood && stellaGood && s->truevirgilio2==TOK_right)return 2101;s->cur_stage=5;return 0;
    case 5:if(seiGood && stellaGood && s->miki1==TOK_tea && s->miki5==TOK_tea)return 2102;s->cur_stage=7;return 0;
    case 7:if(s->alma7==TOK_btini && !s->almadrunk2)return 2104;s->cur_stage=9;return 0;
    case 9:if(s->dorodrink1==TOK_pwman && s->dorodrink7==TOK_woman && s->dorodrink9!=TOK_other && s->dorodrink9!=TOK_alcohol && s->dorodrink9!=TOK_right)return 2103;s->cur_stage=11;return 0;
    case 11:return 2105;
    case 13:return -3;
    default:return 0;
    }
}
static int day_rule_for(View *v) {
    State *s=&v->state;
    if(s->cur_day==8 && s->cur_client==-2){s->cur_client=4;s->cur_stage=1;return 0;}
    if(s->cur_day==12 && s->cur_client==-2 && s->cur_stage==1){s->cur_client=4;return 0;}
    if(s->cur_day==14 && s->cur_client==3 && s->cur_stage==1 && !s->ft_any)return 1525;
    if(s->cur_day==14 && s->cur_client==5 && s->cur_stage==2 && v->block==1533)return 1534;
    if(s->cur_day==14 && s->cur_client==5 && s->cur_stage==1 && v->block==1544)return -3;
    if(s->cur_day==16 && s->cur_client==4 && s->cur_stage==8)return 1761;
    if(s->cur_day==17 && s->cur_client==4 && s->cur_stage==7)return 1856;
    if(s->cur_day==18 && s->cur_client==-2 && s->cur_stage==1 && v->block==1934){s->cur_client=4;s->cur_stage=1;return 0;}
    if(s->cur_day==18 && s->cur_client==5 && s->cur_stage==7)return v->block==1956?1957:1956;
    switch(s->cur_day) {
    case 2:return day2_rule(s,engine_focused(v));
    case 3:return day3_rule(s,engine_focused(v));
    case 4:return day4_rule(s,engine_focused(v));
    case 5:return day5_rule(s,engine_focused(v));
    case 6:return day6_rule(s,v->day6Beers);
    case 7:return day7_rule(s,engine_focused(v));
    case 8:return s->cur_stage==-1?-3:day8_rule(s,engine_focused(v));
    case 9:return day9_rule(s,engine_focused(v));
    case 10:return day10_rule(s,engine_focused(v));
    case 11:return day11_rule(s,engine_focused(v));
    case 12:return day12_rule(s,engine_focused(v));
    case 13:return day13_rule(s);
    case 14:return day14_rule(s,engine_focused(v));
    case 15:return day15_rule(s,engine_focused(v));
    case 16:return day16_rule(s,engine_focused(v));
    case 17:return day17_rule(s,engine_focused(v));
    case 18:return day18_rule(s,engine_focused(v));
    case 19:return day19_rule(s,engine_focused(v));
    case 20:return epilogue_rule(s);
    default:return day_rule(s);
    }
}
static int mix_rule_for(State *s) {
    switch(s->cur_day) {
    case 2:return mix2_rule(s);
    case 3:return mix3_rule(s);
    case 4:return mix4_rule(s);
    case 5:return mix5_rule(s);
    case 7:return mix7_rule(s);
    case 8:return mix8_rule(s);
    case 9:return mix9_rule(s);
    case 10:return mix10_rule(s);
    case 11:return mix11_rule(s);
    case 12:return mix12_rule(s);
    case 14:return mix14_rule(s);
    case 15:return mix15_rule(s);
    case 16:return mix16_rule(s);
    case 17:return mix17_rule(s);
    case 18:return mix18_rule(s);
    case 19:return mix19_rule(s);
    default:return mix_rule(s);
    }
}
static int resume_after_music(View *v) {
    State *s=&v->state;
    s->juke=0;
    switch(s->cur_day) {
    case 18:
        if(s->cur_stage==-2)return -3;
        return 1905;
    case 19:return 2001;
    case 17:
        if(s->cur_stage==-1 && s->cur_client==4)return -3;
        return 1802;
    case 16:
        if(s->cur_stage==-1 && s->cur_client==4)return -3;
        return 1702;
    case 15:
        if(s->cur_stage==-1 && s->cur_client==4)return -3;
        return 1602;
    case 14:
        if(s->cur_client==5){s->cur_client=4;s->cur_stage=1;return 0;}
        return 1502;
    case 12:
        if(s->cur_stage==-1 && s->cur_client==5)return -3;
        return 1302;
    case 11:
        if(s->cur_stage==-1 && s->cur_client==3)return -3;
        return 1202;
    case 10:
        if(s->cur_stage==-1)return -3;
        return 1102;
    case 9:
        if(s->cur_stage==-1)return s->cur_client==5?-3:1002;
        return 1002;
    case 8:
        if(s->cur_stage==-1)return -3;
        if(s->cur_client==-2){s->cur_client=1;s->cur_stage=2;return 0;}
        return 902;
    case 7:
        if(s->cur_client==-2){
            s->cur_client=s->stel4==TOK_right && s->stel5==TOK_right?3:4;
            s->cur_stage=1;return 0;
        }
        return 804;
    case 5:
        if(s->cur_client==-2){s->cur_client=2;s->cur_stage=1;return 0;}
        return 609;
    case 2:
        if(s->cur_client==-3){s->cur_client=4;s->cur_stage=1;return 0;}
        return s->kimdrunk1?202:203;
    case 4:
        if(s->cur_client==-2){s->cur_client=3;s->cur_stage=1;return 0;}
        return 502;
    case 3:
        if(s->cur_client==-2){s->cur_client=3;s->cur_stage=1;return 0;}
        return 402;
    default:
        if(s->cur_client==-2){s->cur_client=3;s->cur_stage=1;return 0;}
        return 102;
    }
}
static void dispatch(View *v) {
    State *s=&v->state;
    if(v->failed){v->mode=6;return;}
    if(s->juke==1){v->mode=7;return;}
    if(s->juke) {
        int next=resume_after_music(v);
        if(next){block(v,next);return;}
    }
    if(s->mix){
        if(s->cur_day==7 && s->cur_client==2 && s->cur_stage==3)s->orders=69;
        v->mode=1;mixer_reset(&v->mixer);return;
    }
    for(int i=0;i<8;++i) {
        int client=s->cur_client,phase=s->cur_stage;
        int n=day_rule_for(v);
        if(n){block(v,n);return;}
        if(client==s->cur_client && phase==s->cur_stage)break;
    }
    v->mode=4;
}
void engine_start(View *v,int dayOnly) {
    int audio=v->audio,track=v->musicTrack;memset(v,0,sizeof(*v));v->audio=audio;playlist_fill(v,track);
    v->state.cur_client=dayOnly?1:0;v->state.cur_stage=1;
    v->state.cur_day=1;v->state.slotamount=1;
    if(!dayOnly){v->visible[0]=1;v->position[0]=185;}
    dispatch(v);
}
void engine_next_day(View *v) {
    if(v->mode!=2 || (v->state.cur_day<1 || v->state.cur_day>=20))return;
    engine_settle(v);
    State *s=&v->state;++s->cur_day;s->cur_client=1;s->cur_stage=1;
    s->cash=0;s->tips=0;s->mistakes=0;s->mix=0;s->juke=0;s->heldRecipe=0;s->slotamount=1;
    memset(v->visible,0,sizeof(v->visible));memset(v->face,0,sizeof(v->face));
    v->cheapErrors=0;v->annaUntil=0;v->round=0;v->overlay=0;v->day6Beers=0;mixer_reset(&v->mixer);engine_day4_download(v);engine_day12_download(v);engine_day18_rent(v);dispatch(v);
    if(s->cur_day==20){v->mode=9;v->selected=0;}else v->mode=5;
}
void engine_advance(View *v) {
    if(v->mode==3){v->state.cur_client=v->state.cur_day==10?2:(v->state.cur_day==8 || v->state.cur_day==9 || v->state.cur_day==11 || v->state.cur_day==12 || v->state.cur_day==14 || v->state.cur_day==15 || v->state.cur_day==16 || v->state.cur_day==17 || v->state.cur_day==18)?3:-2;v->state.cur_stage=1;dispatch(v);return;}
    if(v->mode!=0)return;
    page_leave(v);
    if(v->line+1<blockCount[v->block]){++v->line;page_enter(v);return;}
    dispatch(v);
}
int engine_advance_checkpoint(View *v) {
    int previous=v->mode;
    engine_advance(v);
    return previous!=2 && v->mode==2;
}
void engine_choose(View *v,int choice){
    if(v->mode!=8 || v->state.cur_day!=13 || choice<0 || choice>4)return;
    State *s=&v->state;
    if(choice==2 && s->dogpick)return;
    static const int people[]={TOK_dana,TOK_doro,TOK_dog,TOK_alma,TOK_gil};
    static const int first[]={1402,1403,1404,1405,1406};
    static const int second[]={1408,1409,1412,1413,1416};
    static const int third[]={1420,1421,1422,1423,1424};
    s->pickdare=people[choice];if(choice==2)s->dogpick=1;
    int n=s->cur_stage==2?first[choice]:s->cur_stage==4?second[choice]:s->cur_stage==7?third[choice]:0;
    if(n)block(v,n);
}
void engine_serve(View *v) {
    if(v->mode!=1)return;
    int id=mixer_identify(&v->mixer);
    if(!id)return;
    const Recipe *r=&recipes[id-1];State *s=&v->state;
    if(v->mixer.special && !engine_extra_available(v,r->id))return;
    if(s->slotamount==2 && !s->heldRecipe){
        s->heldRecipe=id;s->heldK=v->mixer.amount[4];s->heldIce=v->mixer.ice;
        mixer_reset(&v->mixer);return;
    }
    if(s->slotamount==2){
        s->bevid_b=r->id;s->drinksize_b=r->size;s->kind_b=r->kind;s->alcohol_b=r->alcohol;
        r=&recipes[s->heldRecipe-1];
    }
    s->bevid_a=r->id;s->flavor_a=r->flavor;s->kind_a=r->kind;
    if(r->id==TOK_fmoai){s->ft_any=1;if((s->cur_day==3 && s->cur_client==1) || (s->cur_day==5 && s->cur_client==1 && s->cur_stage>=20) || (s->cur_day==11 && s->cur_client==3 && s->cur_stage<=7) || (s->cur_day==16 && s->cur_client==2))s->ft_alma=1;if((s->cur_day==3 && s->cur_client==3) || (s->cur_day==7 && s->cur_client==2) || (s->cur_day==10 && s->cur_client==10 && s->cur_stage==2) || (s->cur_day==15 && s->cur_client==1 && s->cur_stage<8) || (s->cur_day==17 && s->cur_client==3))s->ft_stella=1;}
    s->drinksize_a=r->size;s->alcohol_a=r->alcohol;s->otr_a=s->slotamount==2?s->heldIce:v->mixer.ice;
    s->drinkscore_a=r->price;s->mix=0;
    int client=s->cur_client;
    s->exdrink_a=(r->id==TOK_tea || r->id==TOK_rum || r->id==TOK_abs || r->id==TOK_fed)?r->id:0;
    s->mod_aa=v->mixer.amount[0];s->mod_ba=v->mixer.amount[1];s->mod_ca=v->mixer.amount[2];s->mod_da=v->mixer.amount[3];s->mod_ea=v->mixer.amount[4];s->mod_e=v->mixer.amount[4];
    s->rightdrink=s->rightdrink1=s->rightdrink2=0;
    int n=mix_rule_for(s);
    if(s->shouldpay){
        int correct=s->slotamount==2?(s->rightdrink1 && s->rightdrink2):s->rightdrink;
        if(correct)v->cheapErrors=0;
        else {
            int wrong=s->slotamount==2 && !s->rightdrink2?s->bevid_b:s->bevid_a;
            if(wrong==TOK_rum || wrong==TOK_abs || wrong==TOK_tea || wrong==TOK_fed || wrong==TOK_srush || wrong==TOK_sstar || wrong==TOK_bfairy || wrong==TOK_scloud || wrong==TOK_fwater)++v->cheapErrors;
        }
    }
    if(v->cheapErrors>=3){
        v->failed=1;s->mix=0;s->juke=0;s->heldRecipe=0;v->annaUntil=0;
        mixer_reset(&v->mixer);block(v,s->cur_day==5 && (client==1 || s->cur_stage==5)?302:client<3 && s->cur_day==3?304:s->cur_day==2 && client<3?305:301);return;
    }
    if(s->slotamount==2 && s->shouldpay){
        const Recipe *b=&recipes[id-1];
        if(s->rightdrink1)s->cash+=r->price;else ++s->mistakes;
        if(s->rightdrink2)s->cash+=b->price;else ++s->mistakes;
        if(s->rightdrink1 || s->rightdrink2)s->tips+=s->tipping;
        if(s->rightdrink1 && s->rightdrink2){if(s->big_able1 && s->big_able2)s->cash+=200;}
        else if(s->rightdrink1 && s->big_able1)s->cash+=100;
        else if(s->rightdrink2 && s->big_able2)s->cash+=100;
    }else if(s->shouldpay) {
        if(s->rightdrink){
            int bonus=s->big_able;
            /* These full-size drinks do not receive the large-order bonus. */
            if(r->id==TOK_mablast || r->id==TOK_zstar || r->id==TOK_pman || r->id==TOK_pwman)bonus=0;
            s->cash+=r->price+(bonus?100:0);s->tips+=s->tipping;
        }
        else ++s->mistakes;
    }
    if(s->slotamount!=2)s->drunklevel_a+=v->mixer.amount[4];
    s->heldRecipe=0;
    mixer_reset(&v->mixer);block(v,n);
}
int engine_valid(const View *v) {
    if(v->walletCents<0 || v->walletCents>100000000 || (v->purchases>>SHOP_COUNT) || v->paidDay<0 || v->paidDay>v->state.cur_day || v->lastPayCents<0 || v->lastPayCents>100000000)return 0;
    if(v->musicTrack<0 || v->musicTrack>=MUSIC_COUNT || v->chat<0 || v->chat>6 || v->news<0 || v->news>2 || v->boom<0)return 0;
    if(v->cheapErrors<0 || v->cheapErrors>3 || (v->failed!=0 && v->failed!=1))return 0;
    if(v->bang<0 || v->crash<0 || v->mixer.special<0 || (v->mixer.special && (v->mixer.special<60 || v->mixer.special>RECIPE_COUNT)))return 0;
    if(v->day6Beers<0 || v->day6Beers>12 || v->day4Download<0 || v->day4Download>2)return 0;
    if(v->block<1 || v->block>=2108 || !blockCount[v->block])return 0;
    if(v->line<0 || v->line>=blockCount[v->block] || v->mode<0 || v->mode>9 || v->mode==4)return 0;
    if(v->recipe<0 || v->recipe>=BOOK_COUNT || v->selected<0 || v->selected>(v->mode==9?endingCredits.h-240:4))return 0;
    if(v->state.cur_day<1 || v->state.cur_day>20 || v->state.heldRecipe<0 || v->state.heldRecipe>RECIPE_COUNT || v->state.lightdl<0 || v->state.lightdl>2 || v->state.housedl<0 || v->state.housedl>2 || v->state.dogpick<0 || v->state.dogpick>1 || v->state.ft_any<0 || v->state.ft_any>1 || v->state.ft_alma<0 || v->state.ft_alma>1 || v->state.ft_stella<0 || v->state.ft_stella>1)return 0;
    if(v->playlistPos<0 || v->playlistPos>=PLAYLIST_SLOTS)return 0;
    for(int i=0;i<PLAYLIST_SLOTS;++i)if(v->playlist[i]<0 || v->playlist[i]>=MUSIC_COUNT)return 0;
    for(int i=0;i<ACTOR_COUNT;++i)if(v->face[i]<0 || v->face[i]>=actorFaceCount[i] || v->position[i]<-200 || v->position[i]>600)return 0;
    return 1;
}
int engine_migrate(View *v,const void *legacy,unsigned size){
    if(size==1296){
        memset(v,0,sizeof(*v));memcpy(v,legacy,1296);
        playlist_fill(v,v->musicTrack);
        return engine_valid(v);
    }
    if(size==1288){
        const unsigned char *p=legacy;memset(v,0,sizeof(*v));
        memcpy(v,p,80);memcpy(&v->state,p+80,752);
        memcpy(v->visible,p+832,124);memcpy(v->position,p+956,124);memcpy(v->face,p+1080,124);
        memcpy(&v->saveError,p+1204,12);memcpy(&v->annaUntil,p+1216,72);
        return engine_valid(v);
    }
    if(size==1240){
        const unsigned char *p=legacy;memset(v,0,sizeof(*v));
        memcpy(v,p,80);memcpy(&v->state,p+80,704);
        memcpy(v->visible,p+784,124);memcpy(v->position,p+908,124);memcpy(v->face,p+1032,124);
        memcpy(&v->saveError,p+1156,12);memcpy(&v->annaUntil,p+1168,72);
        return engine_valid(v);
    }
    if(size==1216){
        const unsigned char *p=legacy;memset(v,0,sizeof(*v));
        memcpy(v,p,80);memcpy(&v->state,p+80,692);
        memcpy(v->visible,p+772,120);memcpy(v->position,p+892,120);memcpy(v->face,p+1012,120);
        memcpy(&v->saveError,p+1132,12);memcpy(&v->annaUntil,p+1144,72);
        return engine_valid(v);
    }
    if(size==1176){
        const unsigned char *p=legacy;memset(v,0,sizeof(*v));
        memcpy(v,p,80);memcpy(&v->state,p+80,664);
        memcpy(v->visible,p+744,116);memcpy(v->position,p+860,116);memcpy(v->face,p+976,116);
        memcpy(&v->saveError,p+1092,12);memcpy(&v->annaUntil,p+1104,72);
        return engine_valid(v);
    }
    if(size==1144){
        const unsigned char *p=legacy;memset(v,0,sizeof(*v));
        memcpy(v,p,80);memcpy(&v->state,p+80,628);
        memcpy(v->visible,p+708,116);memcpy(v->position,p+824,116);memcpy(v->face,p+940,116);
        memcpy(&v->saveError,p+1056,12);memcpy(&v->annaUntil,p+1072,72);
        return engine_valid(v);
    }
    if(size==1088){
        const unsigned char *p=legacy;memset(v,0,sizeof(*v));
        memcpy(v,p,80);memcpy(&v->state,p+80,596);
        memcpy(v->visible,p+676,108);memcpy(v->position,p+784,108);memcpy(v->face,p+892,108);
        memcpy(&v->saveError,p+1000,12);memcpy(&v->annaUntil,p+1016,72);
        return engine_valid(v);
    }
    if(size==1080){
        const unsigned char *p=legacy;memset(v,0,sizeof(*v));
        memcpy(v,p,80);memcpy(&v->state,p+80,588);
        memcpy(v->visible,p+668,108);memcpy(v->position,p+776,108);memcpy(v->face,p+884,108);
        memcpy(&v->saveError,p+992,12);memcpy(&v->annaUntil,p+1008,72);
        return engine_valid(v);
    }
    if(size==1032){
        const unsigned char *p=legacy;memset(v,0,sizeof(*v));
        memcpy(v,p,80);memcpy(&v->state,p+80,568);
        memcpy(v->visible,p+648,100);memcpy(v->position,p+748,100);memcpy(v->face,p+848,100);
        memcpy(&v->saveError,p+948,12);memcpy(&v->annaUntil,p+960,72);
        return engine_valid(v);
    }
    if(size==984){
        const unsigned char *p=legacy;memset(v,0,sizeof(*v));
        memcpy(v,p,80);memcpy(&v->state,p+80,540);
        memcpy(v->visible,p+620,92);memcpy(v->position,p+712,92);memcpy(v->face,p+804,92);
        memcpy(&v->saveError,p+896,12);memcpy(&v->annaUntil,p+912,72);
        return engine_valid(v);
    }
    if(size==944){
        const unsigned char *p=legacy;memset(v,0,sizeof(*v));
        memcpy(v,p,80);memcpy(&v->state,p+80,504);
        memcpy(v->visible,p+584,92);memcpy(v->position,p+676,92);memcpy(v->face,p+768,92);
        memcpy(&v->saveError,p+860,12);memcpy(&v->annaUntil,p+872,72);
        return engine_valid(v);
    }
    if(size==880){
        const unsigned char *p=legacy;memset(v,0,sizeof(*v));
        memcpy(v,p,80);memcpy(&v->state,p+80,476);
        memcpy(v->visible,p+556,80);memcpy(v->position,p+636,80);memcpy(v->face,p+716,80);
        memcpy(&v->saveError,p+796,12);memcpy(&v->annaUntil,p+808,72);
        return engine_valid(v);
    }
    if(size==832 || size==824){
        const unsigned char *p=legacy;memset(v,0,sizeof(*v));
        memcpy(v,p,80);memcpy(&v->state,p+80,436);
        memcpy(v->visible,p+516,76);memcpy(v->position,p+592,76);memcpy(v->face,p+668,76);
        memcpy(&v->saveError,p+744,12);memcpy(&v->annaUntil,p+760,size-760);
        return engine_valid(v);
    }
    if(size==760){
        const unsigned char *p=legacy;memset(v,0,sizeof(*v));
        memcpy(v,p,80);memcpy(&v->state,p+80,396);
        memcpy(v->visible,p+476,68);memcpy(v->position,p+544,68);memcpy(v->face,p+612,68);
        memcpy(&v->saveError,p+680,12);memcpy(&v->annaUntil,p+696,64);
        if(v->state.cur_day==6 && v->mode==2 && v->day6Beers==12)v->state.jilldrunk1=1;
        return engine_valid(v);
    }
    if(size==640 || size==656){
        const unsigned char *p=legacy;memset(v,0,sizeof(*v));
        memcpy(v,p,80);v->mixer.special=0;memcpy(&v->state,p+80,336);
        memcpy(v->visible,p+416,60);memcpy(v->position,p+476,60);memcpy(v->face,p+536,60);
        memcpy(&v->saveError,p+596,4);memcpy(&v->cheapErrors,p+600,4);memcpy(&v->failed,p+604,4);memcpy(&v->annaUntil,p+608,8);
        memcpy(&v->musicTrack,p+616,20);
        if(size==656)memcpy(&v->walletCents,p+640,16);
        return engine_valid(v);
    }
    if(size==520){
        const unsigned char *p=legacy;memset(v,0,sizeof(*v));
        memcpy(v,p,80);v->mixer.special=0;memcpy(&v->state,p+80,288);
        memcpy(v->visible,p+368,44);memcpy(v->position,p+412,44);memcpy(v->face,p+456,44);
        memcpy(&v->saveError,p+500,4);memcpy(&v->cheapErrors,p+504,4);memcpy(&v->failed,p+508,4);memcpy(&v->annaUntil,p+512,8);
        return engine_valid(v);
    }
    if(size==432 || size==448){
        const unsigned char *p=legacy;memset(v,0,sizeof(*v));
        memcpy(v,p,80);v->mixer.special=0;memcpy(&v->state,p+80,240);
        memcpy(v->visible,p+320,36);memcpy(v->position,p+356,36);memcpy(v->face,p+392,36);
        memcpy(&v->saveError,p+428,4);
        if(size==448){memcpy(&v->cheapErrors,p+432,4);memcpy(&v->failed,p+436,4);memcpy(&v->annaUntil,p+440,8);}
        return engine_valid(v);
    }
    if(size!=296)return 0;
    const unsigned char *p=legacy;memset(v,0,sizeof(*v));
    memcpy(v,p,80);v->mixer.special=0;memcpy(&v->state,p+80,140);
    memcpy(v->visible,p+220,24);memcpy(v->position,p+244,24);memcpy(v->face,p+268,24);
    memcpy(&v->saveError,p+292,4);v->state.cur_day=1;v->state.slotamount=1;
    return engine_valid(v);
}

void engine_finish_jukebox(View *v){if(v->mode==7){v->state.juke=2;dispatch(v);}}
void engine_pour_tea(View *v){
    if(v->mode!=1 || v->failed)return;
    mixer_reset(&v->mixer);v->mixer.ready=true;v->overlay=0;
}
void engine_tick(View *v){
    if(v->mode==9){
        if(v->now>=v->annaUntil){if(v->selected<endingCredits.h-240)++v->selected;v->annaUntil=v->now+50;}
    }else if(v->annaUntil && v->now>=v->annaUntil)v->annaUntil=0;
    if(v->shakeUntil && v->now>=v->shakeUntil)v->shakeUntil=0;
}
void engine_finish_credits(View *v){if(v->mode==9){v->mode=0;v->selected=0;v->annaUntil=0;}}
void engine_scroll_credits(View *v,int delta){
    if(v->mode!=9)return;
    int position=v->selected+delta;
    if(position<0)position=0;
    if(position>endingCredits.h-240)position=endingCredits.h-240;
    v->selected=position;
}
int engine_can_save(const View *v){return !v->failed && engine_valid(v);}

void engine_settle(View *v){
    int day=v->state.cur_day;
    if(v->mode!=2 || v->failed || day<1 || day>19 || day==6 || day==13 || v->paidDay>=day)return;
    int errors=v->state.mistakes;
    if(errors<0 || v->state.cash<0 || v->state.cash>1000000 || v->state.tips<0 || v->state.tips>1000000)return;
    static const int bonus[]={0,500,300,300,400,300,0,500,300,300,500,300,300,0,300,300,300,300,600,0};
    int commission=errors<6?(6-errors)*5:0;
    int pay=v->state.cash*commission+v->state.tips*100+(bonus[day]+(errors==0?500:0))*100;
    if(pay>100000000-v->walletCents)return;
    v->walletCents+=pay;v->lastPayCents=pay;v->paidDay=day;
}
int engine_buy(View *v,int item){
    if(v->mode!=5 || v->failed || item<0 || item>=SHOP_COUNT)return 0;
    unsigned bit=1u<<item;int price=shopItems[item].price*100;
    if((v->purchases&bit) || v->walletCents<price)return 0;
    v->walletCents-=price;v->purchases|=bit;return 1;
}
int engine_shop_music_unlocked(const View *v,int track){
    for(int i=0;i<SHOP_COUNT;++i)
        if(shopItems[i].musicTrack==track)return (v->purchases&(1u<<i))!=0;
    return 1;
}
void engine_grandfather_shop(View *v){
    /* Earlier builds allowed every bonus track and Mulan Tea without a purchase. */
    v->purchases|=1u<<SHOP_TEA_INDEX;
    for(int i=0;i<SHOP_COUNT;++i)
        if(shopItems[i].musicTrack>=0)v->purchases|=1u<<i;
    if(v->state.cur_day>=4 && !v->day4Download)v->day4Download=1;
}
int engine_extra_available(const View *v,int token){
    if(token==TOK_tea)return (v->purchases&(1u<<SHOP_TEA_INDEX))!=0;
    if(token==TOK_fed)return 1;
    int gift=v->state.stel1==TOK_right && v->state.stel2==TOK_right;
    return v->state.cur_day>=5 && ((token==TOK_rum && gift) || (token==TOK_abs && !gift));
}
void engine_pour_special(View *v,int token){
    if(v->mode!=1 || v->failed || !engine_extra_available(v,token))return;
    for(int i=59;i<RECIPE_COUNT;++i)if(recipes[i].id==token){
        mixer_reset(&v->mixer);v->mixer.special=i+1;v->mixer.ready=true;v->overlay=0;return;
    }
}
void engine_day6_drink(View *v){
    if(v->mode==0 && v->state.cur_day==6 && v->block>=702 && v->block<=718 && v->day6Beers<12)
        ++v->day6Beers;
}
