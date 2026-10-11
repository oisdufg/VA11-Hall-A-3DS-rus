# VA-11 HALL-A 3DS

VA-11 HALL-A 3DS is a fan-made port/implementation of VA-11 HALL-A: Cyberpunk Bartender Action for the Nintendo 3DS.

build with neumiraie

## Original Assets Are Not Included

The `VA11-3DS-public-source.zip` archive contains project source code and tools only. It does not contain original game artwork, logos, dialogue, music, extracted game data, generated game scripts, the Russian translation files, or a playable game binary. The separately licensed Noto font is included with its license.

You must provide your own legally obtained copy of VA-11 HALL-A. This source snapshot is not a ready-to-play release or a complete standalone build kit: the current preparation workflow still requires local game data, local decompiled input and generated compatibility metadata. A streamlined asset import workflow remains to be implemented.

Playable local archives, including `VA11-3DS-days1-19-0.26.0.zip`, DO contain game resources. Earlier local archives such as `VA11-3DS-days1-2-0.5.0-source.zip` also contain them. The asset-free statement applies only to the explicitly named public source archive. Local `.3dsx` builds embed artwork and dialogue; removing only the music files does not remove all original content.

## Unofficial Russian Translation

The Russian text and localized resources used by the local test build come from the unofficial fan translation distributed at [koshk.sbs](https://koshk.sbs/). Credit belongs to its translation team. This is not an official Russian localization provided or endorsed by Sukeban Games or Ysbryd Games. The public source archive does not redistribute the translation patch or its dialogue files.

## Requirements

- A Nintendo 3DS with homebrew capabilities and the Homebrew Launcher.
- An SD card with enough free space for the game files.
- A legally owned copy of VA-11 HALL-A.

Original Nintendo 3DS and 3DS LL models are supported. A New Nintendo 3DS or C-Stick is not required.

## Getting Started

### Controls

**Menus and dialogue**

- Select a menu item — D-Pad Up / Down or touch the item.
- Confirm / advance dialogue — A.
- Continue past developer credits and the Russian translation notice — A or touch on each screen.
- Go back — B.
- Open the pause menu — SELECT.
- Save and return to the main menu — A while paused.
- Resume the game — B while paused.
- Open the music selector — X while paused (SELECT, then X).
- Save and exit to the Homebrew Launcher — START.
- During the ending credits, scroll — D-Pad Up / Down; open the epilogue — A.

**Mixing drinks**

- Select an ingredient — D-Pad Up / Down.
- Remove / add an ingredient — D-Pad Left / Right, or touch − / +.
- Toggle ice — L.
- Toggle aging — R.
- Start / stop the shaker — A.
- Serve a finished drink — X.
- Reset the shaker — B.
- Open the recipe book — Y.
- Browse recipes — L / R or D-Pad Left / Right.
- Close the recipe book — Y or B.
- Pour Mulan Tea — open its recipe page with Y and L/R, then press A. The book closes automatically; press X to serve; no shaking is required.

Stop the shaker before 5 seconds to mix, or after at least 5 seconds to blend. The shaker holds up to 20 ingredient units. Failed drinks must be reset before trying again.

For a two-drink order, prepare the first drink and press X to store it. Prepare the second drink and press X again to serve both. B clears both drinks.

**Apartment and phone**

- Open the phone — select **Phone** in the apartment.
- Open an app or article — D-Pad Up / Down and A, or touch the item.
- Scroll an article — D-Pad Up / Down or Left / Right.
- Scroll in larger steps — touch the left or right side of the article.
- Return to the previous screen — B.
- Start the shift — select **Go to work**.

**Music**

- The jukebox opens at the scripted music-selection points, including before the first shift and after breaks.
- Choose a track — D-Pad Up / Down; change page — Left / Right.
- Play and continue — A or touch an available track. B keeps the current track and continues. Twelve bonus tracks are sold in the apartment shop.
- Change music during play — SELECT, X, choose a track, A, then B to close the pause menu.
- To make a playlist, press Y in the jukebox. Use Up/Down to choose a track and Left/Right to choose one of 12 slots. Press A to assign it, X to start the playlist, or B to return to single-track selection. Unbought bonus tracks cannot be assigned.
- The next slot starts when a track ends. Playlist slots and the current position are remembered by the next manual or end-of-day save. Choosing one track outside the editor fills all 12 slots with it.

### Running on the 3DS

#### Local Test Builds

These instructions apply to a local SD-card build prepared using your own game data. The public source archive cannot be copied directly to a console.

1. Open your locally prepared SD-card build.
2. Copy its `3ds` folder to the root of your SD card, merging it with the existing folder.
3. Insert the SD card into your console and open the Homebrew Launcher.
4. Launch **VA-11 HALL-A 3DS**.
5. Choose **Continue** to resume your save, or **New Game** to start from the apartment with or without the tutorial.

The files should be located at:

```text
SD:/3ds/va11-3ds/va11-3ds.3dsx
SD:/3ds/va11-3ds/va11-3ds.smdh
SD:/3ds/va11-3ds/music/000.pcm
SD:/3ds/va11-3ds/music/... (59 tracks plus boom.pcm)
```

You do not need to replace `boot.firm` or change your Luma settings.

Copy the entire `music` directory when updating to 0.26.0, including the `bang.pcm` and `crash.pcm` effects. Allow at least 500 MB of free space for the unpacked build. If the console reports no DSP, music cannot play until DSP support is available; dialogue remains playable. A missing track is reported as missing PCM. Older `music.pcm` is used only as a fallback for the default track.

### Saves

The game autosaves only at the end of each day. It does not write saves when advancing dialogue, entering the shaker, serving drinks or taking a break. Use START to save your current position before exiting. You can also save manually from the apartment or pause menu.

If you turn off the console without saving, progress since your last manual save or completed day will be lost.

After Game Over, A loads your last saved position (or opens a new Day 1 apartment if no save exists). B opens the title screen. Neither the failure dialogue nor the Game Over screen can overwrite your save.

Saves from earlier versions through 0.24.0 are migrated on load.

Keep `day1.sav` and `day1.bak` when updating. Starting a new game replaces your current progress.

## Project Status

This is a work-in-progress homebrew implementation. Content and features are being added gradually; it is not yet a complete port of the original game. The current dialogue and interface are primarily in Russian.

### Included in 0.26.0 beta

- Tutorial, Days 1–19, epilogue dialogue, main menu, apartment and phone. Press A at the end of a completed day to enter the next apartment. After Day 19, A opens the scrolling credits, then the epilogue dialogue.
- Days 16–18 add Tomcat and Jess, late-December phone news, new drink requests and story branches. Day 18 charges $10,000 rent; paying it affects the epilogue.
- Day 19 contains the New Year's conversation with Gaby. The epilogue selects bad-rent, curry, concert, Alma and Dorothy dialogue branches from earlier choices. Six ending illustrations and the scrolling credits are included.
- Day 6 is a day off with Dana. Press A to advance the conversation and Y to drink a beer (up to 12). Dialogue changes with the beer count and earlier Stella orders. The day has no cocktail orders or shift pay.
- Day 7 returns to the bar with Brian, Stella, Art, Virgilio and Cass. It has 61 reachable dialogue blocks, 11 scripted orders, a branch after the break based on Stella's two drinks, and December 19 news.
- Day 8 adds Rad Shiba, wounded Sei, Jamie and Ingram; 51 nonempty dialogue blocks, nine scripted orders, a break, a closing scene, two music prompts and December 20 news.
- Day 9 adds Norma, Mario, Dorothy, Gil and Gaby; 47 nonempty dialogue blocks, eight numbered requests, a break, a closing scene, two music prompts and December 21 news.
- Day 10 adds Virgilio, wounded Sei, Stella and Kim; 47 nonempty dialogue blocks, ten requests including paired drinks, a break, two music prompts and December 22 news.
- Day 11 adds Jill and Nacho, 51 dialogue blocks, branching orders, music, a break and December 23 news.
- Day 12 adds Vella and Essentia portraits, 49 dialogue blocks, Dorothy/Sei/Art branches, drinks, music, a break, December 24 news and an $8,000 electricity bill.
- Day 13 is the Christmas party: 27 dialogue blocks and three rounds of guest selection. Use Up/Down and A, or touch, to choose a guest. There is no cocktail shift or pay that day.
- Day 14 adds Anna and optional Lexi, 44 dialogue blocks, Y2K focus item, music, a break and December 26 news.
- Day 15 adds Stella, Sei, Dorothy and Mario, 48 dialogue blocks, paired drinks, Snatcher focus item, two music prompts, a break and December 27 news.
- Day 3 conversations with Alma, Donovan, Stella, Sei and Dorothy, including paired orders and branching responses.
- Day 3 news follows Donovan's Day 2 outcome. Forum and Miki pages advance throughout the game according to the original day schedule.
- Day 4 story, Art, Streaming-chan, Betty and Deal, paired orders, Game Over and branching news. Stream reactions are shown as compact text; the TV bulletin has a static indicator.
- 59 music tracks, with 12 bonus tracks unlocked through the apartment shop. Scripted jukebox stops and Day 4 gunshot cues are included. Audio streams from SD as 22.05 kHz mono PCM.
- 25 standard cocktails, Mulan Tea, rum, absinthe and Plumfume. Buy Mulan Tea in the apartment shop before pouring it from the recipe book. Open its page, press A to pour, then X to serve. Rum/absinthe unlock from Day 5 according to earlier Stella orders.
- All 30 products from the original apartment shop at their original prices: 16 room decorations, 12 bonus tracks, Mulan Tea and a shoulder massager. Owned decorations appear in the room.
- A persistent wallet, daily commission, tips and a shift bonus for implemented workdays. Days 6 and 13 have no pay.
- The original cheap-wrong-drink Game Over rule and Dana's corresponding scenes.
- Anna's scripted Day 2 TV cameo, shown as a static frame.
- Startup credits for the original developers, composer and publisher.
- A separate unofficial Russian translation notice linking to koshk.sbs.

Day 7 passed 400 ARM shift simulations covering all 61 reachable story blocks and both paths after the break. Day 8 passed 160 ARM simulations covering all 51 nonempty dialogue blocks and nine orders. Day 9 passed 180 ARM simulations covering all 47 nonempty blocks and its eight numbered requests. Day 10 passed 200 ARM simulations covering all 47 nonempty blocks, paired drinks, Game Over and version 14 save migration. Days 11–15 passed 120, 120, 125, 120 and 180 ARM simulations respectively. Days 16–19 passed 180, 240, 240 and 90 ARM routes, and the epilogues passed 17 branch combinations. Save migration checks and the test launcher passed. Real-console input, SD saves, audio playback and performance still need testing. Two unused Day 3 blocks remain unreachable as in the original scripts.

### Apartment shop

Open **Магазин** from the apartment before work. Up/Down selects a product; Left/Right moves five entries. Press A or touch a row to request a purchase, then confirm with A or a second touch. B cancels confirmation; press B again to return home. A `+` marks an owned item. Duplicate purchases and purchases without enough money are blocked.

New games start with an empty wallet. Earnings are credited once when a shift ends: tips, 5% of revenue per remaining allowance out of six mistakes, $500 for a flawless shift, and the original daily bonus ($500 on Days 1, 7 and 10; $400 on Day 4; $600 on Day 18; $300 on the other listed workdays through Day 17). Day 19 has no fixed daily bonus. Amounts retain cents. The Day 4 subscription, Day 12 electricity bill and Day 18 rent are deducted on apartment entry when due.

Purchases are stored by **Сохранить**, START, or the next end-of-day autosave. Buying does not trigger an SD write. Keep `day1.sav` and `day1.bak` when updating. Saves from earlier builds retain story progress, wallet and decoration ownership. They are granted the 12 bonus tracks and Mulan Tea to preserve access already available in those builds. Previous days' earnings cannot be reconstructed if an older save did not store them. A loaded completed shift can be paid once into the new wallet. Otherwise income begins with the next completed shift.

The complete 30-product catalog can be bought and saved. Implemented focus purchases run through Day 18. Without the day's item, Jill's thoughts replace the order hint during mixing. The spoken order and correct drink stay the same. Day 4 automatically buys an $800 subscription when the wallet can cover it; Day 12 charges an $8,000 electricity bill, and Day 18 charges $10,000 rent. The apartment shows the focus status. Old saves from before these mechanics do not receive retroactive charges. Wallpaper/table choices and interactive computer content remain in [BACKLOG.md](BACKLOG.md), along with playlists and optional character animation. Days 2–19 have passed ARM story and order checks; real-console testing is still needed.

## Credits and License

VA-11 HALL-A was created by Sukeban Games, with music by Garoad. This project is an unofficial fan-made port. It is not affiliated with or endorsed by Sukeban Games, Ysbryd Games or Garoad. Startup credits and the main menu use text attribution instead of the original logos.

Original game artwork, dialogue and music remain the property of their respective owners. Third-party components retain their own licenses; see [THIRD_PARTY.md](THIRD_PARTY.md) and the `licenses` directory.

The attribution and educational purpose of this project do not grant redistribution rights to original game content or the fan translation. This repository does not assign a new license to that material.
