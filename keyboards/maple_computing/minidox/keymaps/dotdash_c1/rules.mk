
# BOOTMAGIC_ENABLE = no
COMMAND_ENABLE = no
CONSOLE_ENABLE = yes
EXTRAKEY_ENABLE = yes
MOUSEKEY_ENABLE = yes
RGBLIGHT_ENABLE = no

REPEAT_KEY_ENABLE = no

LTO_ENABLE = yes

# some simplifications
NKRO_ENABLE = no
VIA_ENABLE = no
VIAL_ENABLE = no

# https://github.com/qmk/qmk_firmware/issues/19593#issuecomment-1387476045
# NO_USB_STARTUP_CHECK = yes

# caps word
CAPS_WORD_ENABLE = yes

# swap hands (CAD use)
SWAP_HANDS_ENABLE = yes

# key overrides & combos
COMBO_ENABLE = yes
INTROSPECTION_KEYMAP_C = users/dotdash/dotdash_combos.c
SRC += users/dotdash/dotdash_overrides.c
SRC += keyboards/maple_computing/minidox/keymaps/dotdash_c1/board_config.c
