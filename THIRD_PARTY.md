# Components and provenance

- Game artwork, dialogue and music: the user's local VA-11 HALL-A installation, read without changes. Original game by Sukeban Games; music by Garoad. These resources are not covered by a new project license.
- Unofficial Russian translation used by local builds: https://koshk.sbs/ . Credit belongs to the translation team listed there. The public source archive excludes translation files and localized game assets; attribution is not a grant of redistribution permission.
- Font: Noto Sans Mono, SIL Open Font License 1.1. Source: https://github.com/notofonts/noto-fonts . License: `tools/font/LICENSE.txt`.
- Console runtime: libctru from the official https://hub.docker.com/r/devkitpro/devkitarm image. Source and license: https://github.com/devkitPro/libctru . Includes its zlib license in `licenses/libctru.txt`.
- ARM C runtime and startup libraries: official devkitPro image, GCC runtime/newlib/devkitarm-crtls. Upstream: https://github.com/devkitPro/newlib and https://github.com/devkitPro/devkitarm-crtls . The startup linker script is under MPL 2.0. Runtime licensing information from the image is in `licenses/`.
- Compiler used: Arm GNU Toolchain 14.3.Rel1 for Windows, downloaded from Arm's official distribution endpoint. SHA-256: `864c0c8815857d68a1bbba2e5e2782255bb922845c71c97636004a3d74f60986`, verified against the vendor checksum.
- 3DSX and SMDH format reference: https://github.com/devkitPro/3dstools . The Python writer uses the documented segment sizes and skip/patch relocation tables. It validates the emitted relocation records against ELF targets.
- Tools used for asset preparation and verification: Pillow, NumPy, SoundFile/libsndfile, pyelftools and Unicorn. These host tools are not part of the SD-card application.

The renderer writes RGB framebuffers through libctru. It does not currently use Citro2D, avoiding a texture conversion tool dependency for this first prototype.
