# Day 5 progress

Day 5 is playable in 0.8.0. Day 4 completion opens its apartment; the TEST launcher can start it directly with default prior-day flags.

## Implemented

- All 61 blocks (601–661), 11 orders (47–57), branches, break, two jukebox stops and Day 5 Game Over.
- Taylor, four Virgilio expressions and Dorothy's `wah`, composed using original sprite origins.
- Rum, absinthe and Plumfume can be poured from the recipe book. Rum requires both earlier Stella orders to be correct and Day >= 5; otherwise absinthe is available from Day 5. Plumfume is always available.
- The 17-unit order reads actual shaker contents. Optional Karmotrine can bring a valid recipe to 17 units.
- BANG and CRASH effects, brief screen shaking, December 17 news, shop continuity and Day 5 earnings.
- Version 9 saves migrate version 8's wallet and decorations, as well as older story layouts.

## Validation

`tools/verify_day5.py` exercises the built ARM engine. 1,200 simulations reach all 61 blocks and all 11 orders; 1,198 finish the day and two finish in Game Over. Correct paths with and without Stella's rum gift pass. Other checks cover failure routes, save protection, once-only payroll and authentic version 8 migration. Actor previews were inspected.

The earlier isolated controller driver passed 1,000 routes. Use the integrated test above for release validation; staged files are development intermediates.

## Remaining verification and shared limitations

Test input, audio, SD persistence, rendering and performance on original 3DS hardware. Mouth/blink animation, full original TV presentation, bills and distraction penalties remain deferred. Forum and Miki phone pages still use the earlier selection.

Generated dialogue, portraits, PCM and playable binaries contain original resources and remain excluded from the public source archive.
