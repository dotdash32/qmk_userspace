## common rules.mk setup
CONSOLE_ENABLE = yes
EXTRAKEY_ENABLE = yes
MOUSEKEY_ENABLE = yes

LTO_ENABLE = yes

# caps word
CAPS_WORD_ENABLE = yes

# swap hands (CAD use)
SWAP_HANDS_ENABLE = yes

# key overrides & combos
COMBO_ENABLE = yes
INTROSPECTION_KEYMAP_C = dotdash_combos.c
SRC += dotdash_overrides.c
# SRC += keyboards/maple_computing/minidox/keymaps/dotdash_c1/board_config.c
