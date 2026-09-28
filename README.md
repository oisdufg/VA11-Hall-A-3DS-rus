# VA-11 HALL-A 3DS

VA-11 HALL-A 3DS is a fan-made port/implementation of VA-11 HALL-A: Cyberpunk Bartender Action for the Nintendo 3DS.

build with neumiraie

## Original Assets Are Not Included

The `VA11-3DS-public-source.zip` archive contains project source code and tools only. It does not contain original game artwork, logos, dialogue, music, extracted game data, generated game scripts, the Russian translation files, or a playable game binary. The separately licensed Noto font is included with its license.

You must provide your own legally obtained copy of VA-11 HALL-A. This source snapshot is not a ready-to-play release or a complete standalone build kit: the current preparation workflow still requires local game data, local decompiled input and generated compatibility metadata. A streamlined asset import workflow remains to be implemented.

Earlier local test archives, including `VA11-3DS-days1-2-0.5.0.zip` and `VA11-3DS-days1-2-0.5.0-source.zip`, DO contain game resources. This asset-free statement does not apply to those archives. Local `.3dsx` builds currently embed artwork and dialogue; removing only the music file does not remove all original content.

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
- Continue past startup credits — A or touch.
- Go back — B.
- Open the pause menu — SELECT.
- Save and return to the main menu — A while paused.
- Resume the game — B while paused.
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
SD:/3ds/va11-3ds/music.pcm
```

You do not need to replace `boot.firm` or change your Luma settings.

### Saves

The game autosaves only at the end of each day. It does not write saves when advancing dialogue, entering the shaker, serving drinks or taking a break. Use START to save your current position before exiting. You can also save manually from the apartment or pause menu.

If you turn off the console without saving, progress since your last manual save or completed day will be lost.

After Game Over, A loads your last saved position (or opens a new Day 1 apartment if no save exists). B opens the title screen. Neither the failure dialogue nor the Game Over screen can overwrite your save.

Saves from versions 0.2, 0.3 and 0.4.1 are migrated on load.

Keep `day1.sav` and `day1.bak` when updating. Starting a new game replaces your current progress.

## Project Status

This is a work-in-progress homebrew implementation. Content and features are being added gradually; it is not yet a complete port of the original game. The current dialogue and interface are primarily in Russian.

### Included in 0.5.0

- Tutorial, Days 1–2, main menu, apartment and phone.
- 25 standard cocktails and Mulan Tea (available without purchase while the shop is deferred).
- The original cheap-wrong-drink Game Over rule and Dana's corresponding scenes.
- Anna's scripted Day 2 TV cameo, shown as a static frame.
- Startup credits for the original developers, composer and publisher.

See [BACKLOG.md](BACKLOG.md) for deferred features, including the shop, music selection, salary/expenses and character animation. Existing revenue and tip totals are preliminary; full payroll and financial failure conditions are deferred.

## Credits and License

VA-11 HALL-A was created by Sukeban Games, with music by Garoad. This project is an unofficial fan-made port. It is not affiliated with or endorsed by Sukeban Games, Ysbryd Games or Garoad. Startup credits and the main menu use text attribution instead of the original logos.

Original game artwork, dialogue and music remain the property of their respective owners. Third-party components retain their own licenses; see [THIRD_PARTY.md](THIRD_PARTY.md) and the `licenses` directory.

The attribution and educational purpose of this project do not grant redistribution rights to original game content or the fan translation. This repository does not assign a new license to that material.
