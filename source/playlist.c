#include "playlist.h"
#include "music.h"

void playlist_fill(View *v,int track){
    if(track<0 || track>=MUSIC_COUNT)track=0;
    for(int i=0;i<PLAYLIST_SLOTS;++i)v->playlist[i]=track;
    v->playlistPos=0;v->musicTrack=track;
}
void playlist_assign(View *v,int slot,int track){
    if(slot>=0 && slot<PLAYLIST_SLOTS && track>=0 && track<MUSIC_COUNT)v->playlist[slot]=track;
}
int playlist_advance(View *v){
    v->playlistPos=(v->playlistPos+1)%PLAYLIST_SLOTS;
    v->musicTrack=v->playlist[v->playlistPos];
    return v->musicTrack;
}
