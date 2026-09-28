#include <3ds.h>
#include <stdio.h>
#include <string.h>
#include "game.h"
#include "render.h"
#include "recipes.h"
#include "tokens.h"
#include "menu.h"

#define AUDIO_FRAMES 4096
static FILE *music;
static ndspWaveBuf waves[3];
static int16_t *audioBuffer;
static bool dspReady;
static int audio_init(void) {
    music=fopen("sdmc:/3ds/va11-3ds/music.pcm","rb");
    if(!music)return 2;
    if(R_FAILED(ndspInit())){fclose(music);music=NULL;return 0;}
    dspReady=true;
    audioBuffer=linearAlloc(3*AUDIO_FRAMES*sizeof(int16_t));
    if(!audioBuffer){ndspExit();dspReady=false;fclose(music);music=NULL;return 0;}
    ndspSetOutputMode(NDSP_OUTPUT_STEREO);
    ndspChnReset(0);ndspChnSetInterp(0,NDSP_INTERP_LINEAR);ndspChnSetRate(0,22050);ndspChnSetFormat(0,NDSP_FORMAT_MONO_PCM16);
    float mix[12]={0};mix[0]=mix[1]=0.55f;ndspChnSetMix(0,mix);
    for(int i=0;i<3;++i){waves[i].data_vaddr=audioBuffer+i*AUDIO_FRAMES;waves[i].status=NDSP_WBUF_FREE;}
    return 1;
}
static void audio_tick(void) {
    if(!music || !dspReady)return;
    for(int i=0;i<3;++i) {
        if(waves[i].status!=NDSP_WBUF_DONE && waves[i].status!=NDSP_WBUF_FREE)continue;
        int16_t *dst=audioBuffer+i*AUDIO_FRAMES;
        size_t n=fread(dst,sizeof(int16_t),AUDIO_FRAMES,music);
        if(n<AUDIO_FRAMES){rewind(music);n+=fread(dst+n,sizeof(int16_t),AUDIO_FRAMES-n,music);}
        if(!n)continue;
        waves[i].nsamples=n;waves[i].looping=false;
        DSP_FlushDataCache(dst,n*sizeof(int16_t));ndspChnWaveBufAdd(0,&waves[i]);
    }
}
static void audio_exit(void) {
    if(dspReady){ndspChnWaveBufClear(0);ndspExit();}
    if(audioBuffer)linearFree(audioBuffer);
    if(music)fclose(music);
}
static uint32_t checksum_bytes(const void *data,unsigned size) {
    const unsigned char *p=(const unsigned char *)data;uint32_t h=2166136261u;
    for(unsigned i=0;i<size;++i)h=(h^p[i])*16777619u;
    return h;
}
static void write_save(View *v) {
    if(!engine_can_save(v))return;
    View copy=*v;copy.overlay=0;copy.now=0;copy.annaUntil=0;
    if(copy.mixer.running)mixer_reset(&copy.mixer);
    const char *tmp="sdmc:/3ds/va11-3ds/day1.tmp";
    FILE *f=fopen(tmp,"wb");if(!f){v->saveError=1;return;}
    uint32_t header[3]={0x56413135,sizeof(copy),checksum_bytes(&copy,sizeof(copy))};
    int ok=fwrite(header,sizeof(header),1,f)==1 && fwrite(&copy,sizeof(copy),1,f)==1;
    if(fclose(f))ok=0;
    if(ok){remove("sdmc:/3ds/va11-3ds/day1.bak");rename("sdmc:/3ds/va11-3ds/day1.sav","sdmc:/3ds/va11-3ds/day1.bak");ok=rename(tmp,"sdmc:/3ds/va11-3ds/day1.sav")==0;}
    v->saveError=!ok;
}
static Thread saveThread;
static LightLock saveLock;
static LightEvent saveEvent;
static View queuedSave;
static int savePending,saveStopping,saveResult;
static void save_worker(void *unused) {
    (void)unused;
    for(;;){
        LightEvent_Wait(&saveEvent);
        for(;;){
            View copy;LightLock_Lock(&saveLock);
            int pending=savePending,stop=saveStopping;
            if(pending){copy=queuedSave;savePending=0;}
            LightLock_Unlock(&saveLock);
            if(!pending){if(stop)return;break;}
            write_save(&copy);
            LightLock_Lock(&saveLock);saveResult=copy.saveError;LightLock_Unlock(&saveLock);
        }
    }
}
static void save(View *v) {
    if(!engine_can_save(v))return;
    if(!saveThread){write_save(v);return;}
    LightLock_Lock(&saveLock);queuedSave=*v;savePending=1;LightLock_Unlock(&saveLock);
    LightEvent_Signal(&saveEvent);
}
static void save_shutdown(void) {
    if(!saveThread)return;
    LightLock_Lock(&saveLock);saveStopping=1;LightLock_Unlock(&saveLock);
    LightEvent_Signal(&saveEvent);threadJoin(saveThread,U64_MAX);threadFree(saveThread);
}
static int load_file(View *v,const char *path) {
    FILE *f=fopen(path,"rb");if(!f)return 0;
    View copy;uint32_t h[3];unsigned char data[sizeof(View)];
    int ok=fread(h,sizeof(h),1,f)==1 && ((h[0]==0x56413132 && h[1]==296) || (h[0]==0x56413134 && h[1]==432) || (h[0]==0x56413135 && h[1]==sizeof(copy))) && fread(data,h[1],1,f)==1;
    fclose(f);
    if(!ok || h[2]!=checksum_bytes(data,h[1]))return 0;
    if(h[0]!=0x56413135){if(!engine_migrate(&copy,data,h[1]))return 0;}
    else {memcpy(&copy,data,sizeof(copy));if(!engine_valid(&copy) || copy.failed)return 0;}
    int audio=v->audio;*v=copy;v->audio=audio;v->overlay=0;v->saveError=0;return 1;
}
static void recover(View *v,Menu *menu){
    if(!load_file(v,"sdmc:/3ds/va11-3ds/day1.sav") && !load_file(v,"sdmc:/3ds/va11-3ds/day1.bak")){
        engine_start(v,1);v->mode=5;
    }
    menu_init(menu,1);menu->screen=v->mode==5?UI_HOME:UI_GAME;
}
static void advance(View *v){
    if(engine_advance_checkpoint(v))save(v);
}
static void serve(View *v){engine_serve(v);}
int main(void) {
    gfxInitDefault();gfxSet3D(false);
    View v={0};v.audio=audio_init();engine_start(&v,0);
    int loaded=load_file(&v,"sdmc:/3ds/va11-3ds/day1.sav");
    if(!loaded)loaded=load_file(&v,"sdmc:/3ds/va11-3ds/day1.bak");
    Menu menu;menu_init(&menu,loaded);menu.screen=UI_CREDITS;
    LightLock_Init(&saveLock);LightEvent_Init(&saveEvent,RESET_ONESHOT);
    saveThread=threadCreate(save_worker,NULL,16384,0x31,0,false);
    View lastView={0};Menu lastMenu={0};int redraw=2,lastBlended=-1;
    while(aptMainLoop()) {
        hidScanInput();u32 keys=hidKeysDown();v.now=osGetTime();engine_tick(&v);
        if(saveThread){LightLock_Lock(&saveLock);v.saveError=saveResult;LightLock_Unlock(&saveLock);}
        if(keys&KEY_START){if(menu.hasSave)save(&v);break;}
        if(menu.screen!=UI_GAME){
            unsigned nav=0;
            if(keys&KEY_DUP)nav|=NAV_UP;
            if(keys&KEY_DDOWN)nav|=NAV_DOWN;
            if(keys&KEY_DLEFT)nav|=NAV_LEFT;
            if(keys&KEY_DRIGHT)nav|=NAV_RIGHT;
            if(keys&KEY_A)nav|=NAV_A;
            if(keys&KEY_B)nav|=NAV_B;
            int tx=0,ty=0;
            if(keys&KEY_TOUCH){touchPosition p;hidTouchRead(&p);tx=p.px;ty=p.py;nav|=NAV_TOUCH;}
            int action=menu_input(&menu,&v,nav,tx,ty);
            if(action==ACT_SAVE)save(&v);
            if(action==ACT_LOAD)recover(&v,&menu);
            if(action==ACT_EXIT){if(menu.hasSave)save(&v);break;}
        }else if(v.overlay==2) {
            if(keys&KEY_A){v.overlay=0;save(&v);menu_init(&menu,1);}
            if(keys&KEY_B)v.overlay=0;
        } else if(v.overlay==1) {
            if(keys&(KEY_Y|KEY_B))v.overlay=0;
            if((keys&KEY_A) && recipes[recipeBook[v.recipe]].id==TOK_tea)engine_pour_tea(&v);
            if(keys&(KEY_L|KEY_DLEFT))v.recipe=(v.recipe+BOOK_COUNT-1)%BOOK_COUNT;
            if(keys&(KEY_R|KEY_DRIGHT))v.recipe=(v.recipe+1)%BOOK_COUNT;
        } else if(v.mode==6){if(keys&KEY_A)recover(&v,&menu);if(keys&KEY_B)menu_init(&menu,1);}
        else if(keys&KEY_SELECT)v.overlay=2;
        else if(keys&KEY_Y)v.overlay=1;
        else if(v.mode==2 && v.state.cur_day==1){if(keys&KEY_A){engine_next_day(&v);menu.screen=UI_HOME;menu.selection=0;}}
        else if(v.mode==0 || v.mode==3) {if(keys&KEY_A)advance(&v);}
        else if(v.mode==1) {
            if(keys&KEY_DUP)v.selected=(v.selected+4)%5;
            if(keys&KEY_DDOWN)v.selected=(v.selected+1)%5;
            if(keys&KEY_DLEFT)mixer_add(&v.mixer,v.selected,-1);
            if(keys&KEY_DRIGHT)mixer_add(&v.mixer,v.selected,1);
            if(keys&KEY_B){mixer_reset(&v.mixer);v.state.heldRecipe=0;}
            if(keys&KEY_A)mixer_toggle(&v.mixer,v.now);
            if(keys&KEY_X)serve(&v);
            if(!v.mixer.running&&!v.mixer.ready){if(keys&KEY_L)v.mixer.ice=!v.mixer.ice;if(keys&KEY_R)v.mixer.aged=!v.mixer.aged;}
            if(keys&KEY_TOUCH) {
                touchPosition p;hidTouchRead(&p);
                if(p.py>=49 && p.py<164 && p.px>=7 && p.px<313) {
                    int i=(p.py-49)/23;v.selected=i;
                    if(p.px>=280)mixer_add(&v.mixer,i,1);
                    else if(p.px>=213 && p.px<247)mixer_add(&v.mixer,i,-1);
                } else if(p.py>=168 && p.py<193 && !v.mixer.running && !v.mixer.ready) {
                    if(p.px>=8 && p.px<153)v.mixer.ice=!v.mixer.ice;
                    if(p.px>=160 && p.px<312)v.mixer.aged=!v.mixer.aged;
                } else if(p.py>=198 && p.py<223) {
                    if(p.px>=8 && p.px<104){mixer_reset(&v.mixer);v.state.heldRecipe=0;}
                    if(p.px>=110 && p.px<210)mixer_toggle(&v.mixer,v.now);
                    if(p.px>=216 && p.px<312)serve(&v);
                }
            }
        }
        audio_tick();
        View compare=v;compare.now=0;
        int blended=v.mixer.running && v.now-v.mixer.started>=5000;
        if(memcmp(&lastView,&compare,sizeof(v)) || memcmp(&lastMenu,&menu,sizeof(menu)) || blended!=lastBlended){redraw=2;lastView=compare;lastMenu=menu;lastBlended=blended;}
        if(redraw){
            uint8_t *top=gfxGetFramebuffer(GFX_TOP,GFX_LEFT,NULL,NULL),*bottom=gfxGetFramebuffer(GFX_BOTTOM,GFX_LEFT,NULL,NULL);
            if(menu.screen==UI_GAME)draw_screens(top,bottom,&v);else draw_menu(top,bottom,&v,&menu);
            gfxFlushBuffers();gfxSwapBuffers();--redraw;
        }
        gspWaitForVBlank();
    }
    save_shutdown();audio_exit();gfxExit();return 0;
}
