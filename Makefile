# Standard devkitPro build (3ds-dev packages installed).
ifndef DEVKITARM
$(error Set DEVKITARM to the installed devkitARM directory)
endif
CC := $(DEVKITARM)/bin/arm-none-eabi-gcc
THREEDSXTOOL := $(DEVKITPRO)/tools/bin/3dsxtool
TARGET := sd/3ds/va11-3ds/va11-3ds
SOURCES := source/main.c source/engine.c source/game.c source/render.c source/menu.c generated/assets.c generated/home_assets.c generated/shop_assets.c
OBJECTS := $(patsubst %.c,build/%.o,$(SOURCES))
ARCH := -march=armv6k -mtune=mpcore -mfloat-abi=hard -mfpu=vfp -marm
CFLAGS := $(ARCH) -O2 -g -Wall -Wextra -Werror -mword-relocations -ffunction-sections -fdata-sections -fno-strict-aliasing -D__3DS__ -Isource -Igenerated -I$(DEVKITPRO)/libctru/include
LDFLAGS := $(ARCH) -specs=3dsx.specs -Wl,--gc-sections -L$(DEVKITPRO)/libctru/lib

.PHONY: all
all: $(TARGET).3dsx

build/%.o: %.c source/game.h source/render.h generated/assets.h generated/font.h generated/story.h
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c $< -o $@

build/va11-3ds.elf: $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -lctru -lm -o $@

$(TARGET).3dsx: build/va11-3ds.elf
	@mkdir -p $(dir $@)
	$(THREEDSXTOOL) $< $@
