#include "game.h"
#include "recipes.h"
#include <string.h>

void mixer_reset(Mixer *m) { memset(m, 0, sizeof(*m)); }
bool mixer_add(Mixer *m, int ingredient, int delta) {
    if (ingredient < 0 || ingredient >= 5 || m->running || m->ready) return false;
    int total = 0;
    for (int i=0; i<5; ++i) total += m->amount[i];
    int value = m->amount[ingredient] + delta;
    if (value < 0 || value > 20 || total+delta > 20) return false;
    m->amount[ingredient] = value;
    return true;
}
bool mixer_toggle(Mixer *m, uint64_t now) {
    if (m->ready) return false;
    if (m->running) {
        m->blended = now-m->started >= 5000;
        m->running = false; m->ready = true;
    } else {
        int total=0; for(int i=0;i<5;++i) total+=m->amount[i];
        if (!total) return false;
        m->started=now; m->running=true;
    }
    return true;
}
int mixer_identify(const Mixer *m) {
    if(!m->ready)return 0;
    if(m->special)return m->special>=60 && m->special<=RECIPE_COUNT?m->special:0;
    for(int r=0;r<RECIPE_COUNT;++r) {
        const Recipe *p=&recipes[r];
        if(m->ice!=p->ice || m->aged!=p->aged || m->blended!=p->blended)continue;
        bool ok=true;
        for(int i=0;i<5;++i)if(i==4 && p->optional){if(m->amount[i]<p->amount[i])ok=false;}
            else if(m->amount[i]!=p->amount[i])ok=false;
        if(ok)return r+1;
    }
    return 0;
}
