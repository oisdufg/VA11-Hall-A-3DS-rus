# Changes

## 0.7.0 beta

- Enabled Day 4: 72 story blocks, Art, Streaming-chan, Betty and Deal; 11 order hints, paired orders, branches, break and Game Over. The second drink's category is now passed to order rules. Alcohol accumulation follows the original single-order rule.
- Day 3 completion opens the Day 4 apartment. News uses the earlier Donovan flags.
- Added 59 selectable tracks streamed from SD, with a scripted jukebox prompt before shifts and after breaks. SELECT then X opens music selection during play. One chosen track loops; 12-slot playlists remain deferred.
- Added Day 4 gunshot cues, compact stream-chat reactions, a static news indicator and a saved flag for Stella's rum gift. These are adapted presentation elements, not the original animated UI.
- Preserved the previous field, token and expression indices, including Dana's masked face. Added migration from 0.6.0's 520-byte save layout. Music selection is stored in normal saves; selecting a track does not autosave.
- Built for original 3DS ARMv6K. Day 4: 1,200 full-shift simulations, all 72 blocks reached. Music UI, touch selection, old saves and phone branches tested on the ARM binary. Hardware audio, SD I/O and frame rate remain unverified.

## 0.6.0 beta

- Added a separate Russian translation notice after developer credits, with koshk.sbs attribution. A or touch advances each screen without changing the save.
- Added Day 3, Alma and Stella, additional Dorothy expressions, nine orders, paired drinks, branching dialogue and the corresponding Game Over scenes.
- Day 2 now leads to the Day 3 apartment. News articles use the previous day's Donovan outcome; forum and Miki selections remain unchanged.
- Preserved released token and state-field indices. Save migration supports 296-, 432- and 448-byte layouts; the new layout includes Day 3 flags and two new actors.
- Autosaves remain restricted to day completion. Shop-related distraction, purchases, payroll, music selection and character animation remain deferred.
- Validation: ARMv6K compilation; 1,000 Day 1, 700 Day 2 and 800 Day 3 simulations; all 72 reachable Day 3 blocks; startup navigation, legacy saves and Game Over checks. Hardware testing remains pending.

## Unreleased — source packaging and attribution

- Added an explicit public source archive that excludes original game resources, translation files, generated game code and playable binaries. Existing local test archives remain unchanged and still contain game resources.
- Expanded Git ignore rules for downloaded media, game containers, extracted scripts and archives.
- Replaced original title artwork/logos on startup and menu screens with text attribution and an unofficial fan-port notice.
- Credited the unofficial Russian translation from koshk.sbs in the README, provenance file and startup screen.

## 0.5.0

- Added startup credits: Sukeban Games, Garoad and Ysbryd Games, plus the requested port attribution. A or touch opens the title screen.
- Added original Game Over scenes for Days 1–2. Three incorrect cheap paid drinks trigger failure; a correct paid order or a break clears the counter. Incorrect expensive drinks and unpaid orders leave the counter unchanged. Paired orders count once.
- Failed runs cannot overwrite saves. A on Game Over loads the last save; without one, it starts a fresh Day 1 apartment. Continue from the title also reloads after failure.
- Added Mulan Tea as a prepared drink: Y, select its page, A to pour, X to serve. It is available without purchase until the shop is implemented. This enables Miki's original tea response.
- Added the scripted Day 2 Anna cameo on the television, using a static original frame for 100 game frames (about 3.33 seconds).
- Preserved end-of-day-only autosaves and manual saves. Added migration from the 0.4.1 save layout; older 0.2/0.3 migration remains.
- Added BACKLOG.md for shop/purchases, music, full salary/expenses, mouth movement and blinking.

Validation reports are included in the source package. These are ARM execution and rendering checks; this release still needs testing on real 3DS hardware.

## 0.4.1

### Save timing

- Autosave runs only when a day is completed.
- Opening the shaker, serving either drink, advancing dialogue and taking a break do not request a save.
- Starting work and returning to the apartment do not request a save.
- Manual saving remains available in the apartment, from the pause menu and when exiting with START.
- Background saving is retained. Exit waits for any pending write to finish.

The reported pauses happened at order checkpoints, where older builds requested SD writes. Those requests have been removed. Actual input latency still needs testing on a console; ARM emulation does not reproduce SD-card delays.

### Second day

- Added Donovan, Dorothy, Jamie and Kira Miki's second-day dialogue and orders.
- Added paired drinks: X stores the first drink, then X serves both after preparing the second. B clears the pair.
- Press A on the first day's results to enter the apartment before Day 2. Select Go to work to begin the second shift.
- Day 2 dialogue and news retain relevant outcomes from Day 1.
- Saves from 0.2 and 0.3 are migrated when loaded. Keep both day1.sav and day1.bak when updating.

### Checks and remaining scope

- Compiled for original 3DS with warnings treated as errors.
- ARM tests completed 1,000 first-day shifts and 700 second-day shifts, with autosave requests checked at every dialogue transition.
- Tested all 3,481 pairs of recognized recipe variants and migration from the old save layout.
- 67 of 68 second-day blocks are reachable with the available shaker ingredients. The extra tea branch requires an item not provided by this build.
- Shop purchases, the distraction system, the brief ANNA visual effect, later days, full payroll, music selection and original game-over penalties remain outside this build. Order hints remain readable rather than depending on shopping.
- Console I/O, audio timing and performance have not been verified on hardware for this version.

The project README now follows the requested format, includes current controls and “build with neumiraie”, and omits manual build instructions.
