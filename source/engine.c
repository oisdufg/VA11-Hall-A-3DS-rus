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

static void block(View *v,int n) {
    if(n==-2){v->cheapErrors=0;v->mode=3;return;}
    if(n==-3){v->mode=2;engine_settle(v);return;}
    if(n<=0 || n>=662 || !blockCount[n]){v->mode=4;return;}
    v->block=n;v->line=0;v->mode=0;page_enter(v);
}
static void dispatch(View *v) {
    State *s=&v->state;
    if(v->failed){v->mode=6;return;}
    if(s->juke==1){v->mode=7;return;}
    if(s->juke) {
        s->juke=0;
        if(s->cur_day==5){
            if(s->cur_client==-2){s->cur_client=2;s->cur_stage=1;}
            else {block(v,609);return;}
        }
        else if(s->cur_day==2){
            if(s->cur_client==-3){s->cur_client=4;s->cur_stage=1;}
            else {block(v,s->kimdrunk1?202:203);return;}
        }
        else if(s->cur_day==4){
            if(s->cur_client==-2){s->cur_client=3;s->cur_stage=1;}
            else {block(v,502);return;}
        }
        else if(s->cur_day==3){
            if(s->cur_client==-2){s->cur_client=3;s->cur_stage=1;}
            else {block(v,402);return;}
        }
        else if(s->cur_client==-2){s->cur_client=3;s->cur_stage=1;}
        else {block(v,102);return;}
    }
    if(s->mix){v->mode=1;mixer_reset(&v->mixer);return;}
    for(int i=0;i<3;++i) {
        int client=s->cur_client,phase=s->cur_stage;
        int n=s->cur_day==5?day5_rule(s):s->cur_day==4?day4_rule(s):s->cur_day==3?day3_rule(s):s->cur_day==2?day2_rule(s):day_rule(s);
        if(n){block(v,n);return;}
        if(client==s->cur_client && phase==s->cur_stage)break;
    }
    v->mode=4;
}
void engine_start(View *v,int dayOnly) {
    int audio=v->audio,track=v->musicTrack;memset(v,0,sizeof(*v));v->audio=audio;v->musicTrack=track;
    v->state.cur_client=dayOnly?1:0;v->state.cur_stage=1;
    v->state.cur_day=1;v->state.slotamount=1;
    if(!dayOnly){v->visible[0]=1;v->position[0]=185;}
    dispatch(v);
}
void engine_next_day(View *v) {
    if(v->mode!=2 || (v->state.cur_day<1 || v->state.cur_day>=5))return;
    engine_settle(v);
    State *s=&v->state;++s->cur_day;s->cur_client=1;s->cur_stage=1;
    s->cash=0;s->tips=0;s->mistakes=0;s->mix=0;s->juke=0;s->heldRecipe=0;s->slotamount=1;
    memset(v->visible,0,sizeof(v->visible));memset(v->face,0,sizeof(v->face));
    v->cheapErrors=0;v->annaUntil=0;v->round=0;v->overlay=0;mixer_reset(&v->mixer);dispatch(v);v->mode=5;
}
void engine_advance(View *v) {
    if(v->mode==3){v->state.cur_client=-2;v->state.cur_stage=1;dispatch(v);return;}
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
        s->bevid_b=r->id;s->drinksize_b=r->size;s->kind_b=r->kind;
        r=&recipes[s->heldRecipe-1];
    }
    s->bevid_a=r->id;s->flavor_a=r->flavor;s->kind_a=r->kind;
    s->drinksize_a=r->size;s->alcohol_a=r->alcohol;s->otr_a=s->slotamount==2?s->heldIce:v->mixer.ice;
    s->drinkscore_a=r->price;s->mix=0;
    int client=s->cur_client;
    s->exdrink_a=(r->id==TOK_tea || r->id==TOK_rum || r->id==TOK_abs || r->id==TOK_fed)?r->id:0;
    s->mod_aa=v->mixer.amount[0];s->mod_ba=v->mixer.amount[1];s->mod_ca=v->mixer.amount[2];s->mod_da=v->mixer.amount[3];s->mod_ea=v->mixer.amount[4];
    s->rightdrink=s->rightdrink1=s->rightdrink2=0;
    int n=s->cur_day==5?mix5_rule(s):s->cur_day==4?mix4_rule(s):s->cur_day==3?mix3_rule(s):s->cur_day==2?mix2_rule(s):mix_rule(s);
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
    if(v->block<1 || v->block>=662 || !blockCount[v->block])return 0;
    if(v->line<0 || v->line>=blockCount[v->block] || v->mode<0 || v->mode>7 || v->mode==4)return 0;
    if(v->recipe<0 || v->recipe>=BOOK_COUNT || v->selected<0 || v->selected>4)return 0;
    if(v->state.cur_day<1 || v->state.cur_day>5 || v->state.heldRecipe<0 || v->state.heldRecipe>RECIPE_COUNT)return 0;
    for(int i=0;i<ACTOR_COUNT;++i)if(v->face[i]<0 || v->face[i]>=actorFaceCount[i] || v->position[i]<-200 || v->position[i]>600)return 0;
    return 1;
}
int engine_migrate(View *v,const void *legacy,unsigned size){
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
void engine_tick(View *v){if(v->annaUntil && v->now>=v->annaUntil)v->annaUntil=0;if(v->shakeUntil && v->now>=v->shakeUntil)v->shakeUntil=0;}
int engine_can_save(const View *v){return !v->failed && engine_valid(v);}

void engine_settle(View *v){
    int day=v->state.cur_day;
    if(v->mode!=2 || v->failed || day<1 || day>5 || v->paidDay>=day)return;
    int errors=v->state.mistakes;
    if(errors<0 || v->state.cash<0 || v->state.cash>1000000 || v->state.tips<0 || v->state.tips>1000000)return;
    static const int bonus[]={0,500,300,300,400,300};
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
int engine_extra_available(const View *v,int token){
    if(token==TOK_tea || token==TOK_fed)return 1;
    int gift=v->state.stel1==TOK_right && v->state.stel2==TOK_right;
    return v->state.cur_day>=5 && ((token==TOK_rum && gift) || (token==TOK_abs && !gift));
}
void engine_pour_special(View *v,int token){
    if(v->mode!=1 || v->failed || !engine_extra_available(v,token))return;
    for(int i=59;i<RECIPE_COUNT;++i)if(recipes[i].id==token){
        mixer_reset(&v->mixer);v->mixer.special=i+1;v->mixer.ready=true;v->overlay=0;return;
    }
}
