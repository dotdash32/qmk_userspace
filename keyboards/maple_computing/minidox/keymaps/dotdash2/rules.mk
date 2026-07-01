
# BOOTMAGIC_ENABLE = no
COMMAND_ENABLE = no
CONSOLE_ENABLE = yes
EXTRAKEY_ENABLE = yes
MOUSEKEY_ENABLE = yes
RGBLIGHT_ENABLE = no

REPEAT_KEY_ENABLE = yes

LTO_ENABLE = yes

# some simplifications
NKRO_ENABLE = no
VIA_ENABLE = no
VIAL_ENABLE = no



# https://github.com/qmk/qmk_firmware/issues/19593#issuecomment-1387476045
# NO_USB_STARTUP_CHECK = yes

# caps word
CAPS_WORD_ENABLE = yes

# key overrides & combos
COMBO_ENABLE = yes
INTROSPECTION_KEYMAP_C = keyboards/maple_computing/minidox/keymaps/dotdash2/key_combos.c
SRC += keyboards/maple_computing/minidox/keymaps/dotdash2/overrides.c
