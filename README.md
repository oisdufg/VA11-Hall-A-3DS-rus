# VA-11 HALL-A 3DS

VA-11 HALL-A 3DS is a fan-made port/implementation of VA-11 HALL-A: Cyberpunk Bartender Action for the Nintendo 3DS.

build with neumiraie

## Original Assets Are Not Included

The `VA11-3DS-public-source.zip` archive contains project source code and tools only. It does not contain original game artwork, logos, dialogue, music, extracted game data, generated game scripts, the Russian translation files, or a playable game binary. The separately licensed Noto font is included with its license.

You must provide your own legally obtained copy of VA-11 HALL-A. This source snapshot is not a ready-to-play release or a complete standalone build kit: the current preparation workflow still requires local game data, local decompiled input and generated compatibility metadata. A streamlined asset import workflow remains to be implemented.

Playable local archives, including `VA11-3DS-days1-4-0.7.0.zip`, DO contain game resources. Earlier local archives such as `VA11-3DS-days1-2-0.5.0-source.zip` also contain them. The asset-free statement applies only to the explicitly named public source archive. Local `.3dsx` builds embed artwork and dialogue; removing only the music files does not remove all original content.

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
- Play and continue — A or touch a track. B keeps the current track and continues.
- Change music during play — SELECT, X, choose a track, A, then B to close the pause menu.
- The selected track loops and is remembered by the next manual or end-of-day save. The original 12-slot playlist is not implemented yet.

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

Copy the entire `music` directory when updating to 0.7.0. Allow at least 450 MB of free space for the unpacked build. If the console reports no DSP, music cannot play until DSP support is available; dialogue remains playable. A missing track is reported as missing PCM. Older `music.pcm` is used only as a fallback for the default track.

### Saves

The game autosaves only at the end of each day. It does not write saves when advancing dialogue, entering the shaker, serving drinks or taking a break. Use START to save your current position before exiting. You can also save manually from the apartment or pause menu.

If you turn off the console without saving, progress since your last manual save or completed day will be lost.

After Game Over, A loads your last saved position (or opens a new Day 1 apartment if no save exists). B opens the title screen. Neither the failure dialogue nor the Game Over screen can overwrite your save.

Saves from versions 0.2, 0.3, 0.4.1, 0.5.0 and 0.6.0 are migrated on load.

Keep `day1.sav` and `day1.bak` when updating. Starting a new game replaces your current progress.

## Project Status

This is a work-in-progress homebrew implementation. Content and features are being added gradually; it is not yet a complete port of the original game. The current dialogue and interface are primarily in Russian.

### Included in 0.7.0 beta

- Tutorial, Days 1–4, main menu, apartment and phone. Press A at the end of a completed day to enter the next apartment, through Day 4.
- Day 3 conversations with Alma, Donovan, Stella, Sei and Dorothy, including paired orders and branching responses.
- Day 3 news follows Donovan's Day 2 outcome. Forum and Miki pages still use the earlier selection.
- Day 4 story, Art, Streaming-chan, Betty and Deal, paired orders, Game Over and branching news. Stream reactions are shown as compact text; the TV bulletin has a static indicator.
- 59 selectable music tracks, scripted jukebox stops and Day 4 gunshot cues. Audio streams from SD as 22.05 kHz mono PCM.
- 25 standard cocktails and Mulan Tea (available without purchase while the shop is deferred).
- The original cheap-wrong-drink Game Over rule and Dana's corresponding scenes.
- Anna's scripted Day 2 TV cameo, shown as a static frame.
- Startup credits for the original developers, composer and publisher.
- A separate unofficial Russian translation notice linking to koshk.sbs.

Day 4 has passed 1,200 ARM shift simulations covering all 72 story blocks. Jukebox navigation and migration of the 0.6.0 save layout also passed. Real-console input, SD saves, audio playback and performance still need testing. Two unused Day 3 blocks remain unreachable as in the original scripts.

See [BACKLOG.md](BACKLOG.md) for deferred features, including the shop, playlists, salary/expenses and character animation. Existing revenue and tip totals are preliminary; full payroll and financial failure conditions are deferred.

## Credits and License

VA-11 HALL-A was created by Sukeban Games, with music by Garoad. This project is an unofficial fan-made port. It is not affiliated with or endorsed by Sukeban Games, Ysbryd Games or Garoad. Startup credits and the main menu use text attribution instead of the original logos.

Original game artwork, dialogue and music remain the property of their respective owners. Third-party components retain their own licenses; see [THIRD_PARTY.md](THIRD_PARTY.md) and the `licenses` directory.

The attribution and educational purpose of this project do not grant redistribution rights to original game content or the fan translation. This repository does not assign a new license to that material.
