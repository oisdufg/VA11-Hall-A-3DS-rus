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

static void block(View *v,int n) {
    if(n==-2){v->cheapErrors=0;v->mode=3;return;}
    if(n==-3){v->mode=2;return;}
    if(n<=0 || n>=573 || !blockCount[n]){v->mode=4;return;}
    v->block=n;v->line=0;v->mode=0;page_enter(v);
}
static void dispatch(View *v) {
    State *s=&v->state;
    if(v->failed){v->mode=6;return;}
    if(s->juke==1){v->mode=7;return;}
    if(s->juke) {
        s->juke=0;
        if(s->cur_day==2){
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
        int n=s->cur_day==4?day4_rule(s):s->cur_day==3?day3_rule(s):s->cur_day==2?day2_rule(s):day_rule(s);
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
    if(v->mode!=2 || (v->state.cur_day<1 || v->state.cur_day>=4))return;
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
    s->exdrink_a=r->id==TOK_tea?TOK_tea:0;
    s->rightdrink=s->rightdrink1=s->rightdrink2=0;
    int n=s->cur_day==4?mix4_rule(s):s->cur_day==3?mix3_rule(s):s->cur_day==2?mix2_rule(s):mix_rule(s);
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
        mixer_reset(&v->mixer);block(v,client<3 && s->cur_day==3?304:s->cur_day==2 && client<3?305:301);return;
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
    if(v->musicTrack<0 || v->musicTrack>=MUSIC_COUNT || v->chat<0 || v->chat>6 || v->news<0 || v->news>2 || v->boom<0)return 0;
    if(v->cheapErrors<0 || v->cheapErrors>3 || (v->failed!=0 && v->failed!=1))return 0;
    if(v->block<1 || v->block>=573 || !blockCount[v->block])return 0;
    if(v->line<0 || v->line>=blockCount[v->block] || v->mode<0 || v->mode>7 || v->mode==4)return 0;
    if(v->recipe<0 || v->recipe>=BOOK_COUNT || v->selected<0 || v->selected>4)return 0;
    if(v->state.cur_day<1 || v->state.cur_day>4 || v->state.heldRecipe<0 || v->state.heldRecipe>RECIPE_COUNT)return 0;
    for(int i=0;i<ACTOR_COUNT;++i)if(v->face[i]<0 || v->face[i]>=actorFaceCount[i] || v->position[i]<-200 || v->position[i]>600)return 0;
    return 1;
}
int engine_migrate(View *v,const void *legacy,unsigned size){
    if(size==520){
        const unsigned char *p=legacy;memset(v,0,sizeof(*v));
        memcpy(v,p,80);memcpy(&v->state,p+80,288);
        memcpy(v->visible,p+368,44);memcpy(v->position,p+412,44);memcpy(v->face,p+456,44);
        memcpy(&v->saveError,p+500,4);memcpy(&v->cheapErrors,p+504,4);memcpy(&v->failed,p+508,4);memcpy(&v->annaUntil,p+512,8);
        return engine_valid(v);
    }
    if(size==432 || size==448){
        const unsigned char *p=legacy;memset(v,0,sizeof(*v));
        memcpy(v,p,80);memcpy(&v->state,p+80,240);
        memcpy(v->visible,p+320,36);memcpy(v->position,p+356,36);memcpy(v->face,p+392,36);
        memcpy(&v->saveError,p+428,4);
        if(size==448){memcpy(&v->cheapErrors,p+432,4);memcpy(&v->failed,p+436,4);memcpy(&v->annaUntil,p+440,8);}
        return engine_valid(v);
    }
    if(size!=296)return 0;
    const unsigned char *p=legacy;memset(v,0,sizeof(*v));
    memcpy(v,p,80);memcpy(&v->state,p+80,140);
    memcpy(v->visible,p+220,24);memcpy(v->position,p+244,24);memcpy(v->face,p+268,24);
    memcpy(&v->saveError,p+292,4);v->state.cur_day=1;v->state.slotamount=1;
    return engine_valid(v);
}

void engine_finish_jukebox(View *v){if(v->mode==7){v->state.juke=2;dispatch(v);}}
void engine_pour_tea(View *v){
    if(v->mode!=1 || v->failed)return;
    mixer_reset(&v->mixer);v->mixer.ready=true;v->overlay=0;
}
void engine_tick(View *v){if(v->annaUntil && v->now>=v->annaUntil)v->annaUntil=0;}
int engine_can_save(const View *v){return !v->failed && engine_valid(v);}
