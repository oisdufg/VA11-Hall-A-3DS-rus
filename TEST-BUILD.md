# Test launcher 0.8.0

Install the regular 0.8.0 package first, then extract the test archive onto the SD card. The test executable lives in `3ds/va11-3ds-test/`, alongside the regular installation. It uses music from `3ds/va11-3ds/music/`.

Launch **VA-11 HALL-A TEST** in Homebrew Launcher. After the startup notices, choose **Тест: выбрать день** and select Day 1–5. Each selection starts a fresh test apartment with $20,000, no purchased decorations and default previous-day story flags. Day 5 starts without the earlier Stella rum gift, so its extra bottle is absinthe. A normal playthrough retains your actual previous choices.

- **Телефон** opens the phone apps.
- **Магазин** opens the shop. A or touch selects a product; confirm again to buy. B cancels or returns home.
- **Сохранить** saves the test session. START saves and exits.
- **На работу** starts the selected day's shift.
- From the apartment, B returns to the title. During a shift, SELECT then A saves and returns to the title.
- **Продолжить** resumes the test session. Choosing a day again resets the in-memory test progress; it becomes persistent on the next save.

The test build reads and writes only `test-day1.sav`, `test-day1.bak` and `test-day1.tmp` in `3ds/va11-3ds/`. It does not load or overwrite the regular `day1.sav`/`day1.bak`. The test archive contains no saves and does not replace the regular executable.

Useful console check: select Day 2, buy a decoration, return home and verify it appears, save, exit, launch TEST again and choose Continue. The decoration and wallet balance should survive. Then visit the phone and start work.

This local playable binary contains original game resources. It is not the asset-free public source archive. It has been compiled and checked in ARM emulation; real-console rendering and SD persistence still need testing.
