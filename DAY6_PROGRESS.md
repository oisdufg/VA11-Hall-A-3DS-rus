# Day 6 progress

Day 6 is playable in the local 0.9.0 beta. Completing Day 5 opens the Day 6 apartment; the TEST launcher can open it directly. The day is a day off, so there are no cocktail orders or wages.

## Implemented

- All 18 reachable dialogue blocks (701–718) from the original Day 6 script, including the previous Stella-order branch.
- Beer-count dialogue branches at 2, 4, 6 and 9–12 beers. Press Y during the day-off scene to drink one beer, up to 12; press A for the next line.
- Static scene composed locally from the owner's original game sprites, with a second Jill frame after seven beers. December 18 phone news and the ordinary apartment/shop menu remain accessible.
- End-of-day checkpoint can be saved; wallet, purchases and previous-day choices remain intact. No Day 6 pay is credited.

## Validation and limits

The ARM engine completed 12 routes that reached every dialogue block, tested the Stella branch and all beer thresholds, and checked the Day 5 transition, save eligibility and no-pay outcome. The separate TEST launcher opened all six days and checked phone/shop access. The original 3DS console has not yet been tested for frame rate, input, audio or SD save/reload.

Y drinks one whole beer per press; the original PC scene uses mouse-driven sipping. The scene uses static frames, without the original animation or room effects. Generated dialogue, sprites and playable binaries stay outside the public source archive.
