#pragma once
#include <stdint.h>
#include "game.h"
#include "state.h"
typedef struct {
    int block, line, mode, round, selected, recipe, overlay, audio;
    uint64_t now;
    Mixer mixer;
    State state;
    int visible[31],position[31],face[31];
    int saveError;
    int cheapErrors,failed;
    uint64_t annaUntil;
    int musicTrack,chat,news,rum,boom;
    int day6Beers; /* Reuses a zeroed save field; the binary save layout stays the same. */
    int walletCents;
    unsigned purchases;
    int paidDay,lastPayCents;
    uint64_t shakeUntil;
    int bang,crash;
    int day4Download; /* 0 pending, 1 paid, 2 insufficient funds. */
    int playlist[12],playlistPos;
} View;
// mode: 0 dialogue, 1 mixing, 2 finished, 3 break, 4 error, 5 apartment, 6 Game Over, 7 jukebox, 8 party choice, 9 credits.
// overlay: 1 recipes, 2 pause. Legacy saves are converted by engine_migrate.
void draw_screens(uint8_t *top, uint8_t *bottom, const View *view);
void engine_start(View *v,int dayOnly);
void engine_advance(View *v);
int engine_advance_checkpoint(View *v);
void engine_serve(View *v);
int engine_valid(const View *v);
void engine_next_day(View *v);
void engine_finish_jukebox(View *v);
int engine_migrate(View *v,const void *legacy,unsigned size);
void engine_pour_tea(View *v);
void engine_tick(View *v);
int engine_can_save(const View *v);
void engine_settle(View *v);
int engine_buy(View *v,int item);
int engine_shop_music_unlocked(const View *v,int track);
void engine_grandfather_shop(View *v);
int engine_focused(const View *v);
void engine_day4_download(View *v);
void engine_day12_download(View *v);
void engine_day18_rent(View *v);
void engine_finish_credits(View *v);
void engine_scroll_credits(View *v,int delta);
void engine_choose(View *v,int choice);
int engine_extra_available(const View *v,int token);
void engine_pour_special(View *v,int token);
void engine_day6_drink(View *v);
