#pragma once
#include <stdbool.h>
#include <stdint.h>

typedef struct {
    int amount[5];
    bool ice, aged, running, ready, blended;
    uint64_t started;
} Mixer;
void mixer_reset(Mixer *m);
bool mixer_add(Mixer *m, int ingredient, int delta);
bool mixer_toggle(Mixer *m, uint64_t now);
int mixer_identify(const Mixer *m);
