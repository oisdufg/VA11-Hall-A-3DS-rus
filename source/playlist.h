#pragma once
#include "render.h"

#define PLAYLIST_SLOTS 12
void playlist_fill(View *v,int track);
void playlist_assign(View *v,int slot,int track);
int playlist_advance(View *v);
