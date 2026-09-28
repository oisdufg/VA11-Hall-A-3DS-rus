#pragma once
#include <stdint.h>
#include "game.h"
#include "state.h"
typedef struct {
    int block, line, mode, round, selected, recipe, overlay, audio;
    uint64_t now;
    Mixer mixer;
    State state;
    int visible[9],position[9],face[9];
    int saveError;
    int cheapErrors,failed;
    uint64_t annaUntil;
} View;
// mode: 0 dialogue, 1 mixing, 2 finished, 3 break, 4 error, 5 apartment, 6 Game Over.
// overlay: 1 recipes, 2 pause. Legacy saves are converted by engine_migrate.
void draw_screens(uint8_t *top, uint8_t *bottom, const View *view);
void engine_start(View *v,int dayOnly);
void engine_advance(View *v);
int engine_advance_checkpoint(View *v);
void engine_serve(View *v);
int engine_valid(const View *v);
void engine_next_day(View *v);
int engine_migrate(View *v,const void *legacy,unsigned size);
void engine_pour_tea(View *v);
void engine_tick(View *v);
int engine_can_save(const View *v);
