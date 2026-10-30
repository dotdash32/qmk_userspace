## include userpsace shared config
USER_NAME := dotdash

REPEAT_KEY_ENABLE = no

LTO_ENABLE = yes

# some simplifications
NKRO_ENABLE = no
VIA_ENABLE = no
VIAL_ENABLE = no
COMMAND_ENABLE = no
RGBLIGHT_ENABLE = no

# https://github.com/qmk/qmk_firmware/issues/19593#issuecomment-1387476045
# NO_USB_STARTUP_CHECK = yes

# board specific files
SRC += keyboards/maple_computing/minidox/keymaps/dotdash_c1/board_config.c # swap hands
