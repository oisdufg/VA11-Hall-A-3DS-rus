# Day 9 progress

Day 9 is playable in the local 0.14.0 beta. Completing Day 8 opens its apartment, and the separate TEST launcher can start it directly with default earlier choices.

## Implemented

- All 47 nonempty Russian dialogue blocks (1001–1047), including Norma, Mario, Dorothy, Gil, Gaby, the break and the closing scene. Block 48 is an empty script marker.
- Seven numbered order hints (78–84), Gil's beer request (178), alternate mixer responses, Game Over, two music prompts and the Day 9 shift payout.
- The original beer-discount purchase is Day 9's focus item. Without it, Jill's distracted thoughts replace the order hint; the spoken request and correct drink stay unchanged.
- Static portraits of Norma, Mario and Gaby assembled from the original sprite layers, plus December 21 phone news.
- Save version 14 adds Day 9 story state and three actor slots. Version 13 saves retain Day 8 progress, wallet, purchases and earlier choices.

## Validation and limits

The compiled ARM engine completed 180 Day 9 routes covering all 47 nonempty blocks, every order hint, focused and distracted states, the break, both music prompts and version 13 save migration. A separate check triggered Game Over after three cheap wrong drinks. Hardware input, frame rate, audio and SD persistence still need testing on an original 3DS.

Generated dialogue, portraits and playable binaries stay outside the public source archive.
