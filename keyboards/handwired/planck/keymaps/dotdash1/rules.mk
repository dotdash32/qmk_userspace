
# BOOTMAGIC_ENABLE = no
COMMAND_ENABLE = no
CONSOLE_ENABLE = yes
EXTRAKEY_ENABLE = yes
MOUSEKEY_ENABLE = yes
RGBLIGHT_ENABLE = yes
NKRO_ENABLE = no

REPEAT_KEY_ENABLE = no

LTO_ENABLE = yes # maybe not needed?

VIA_ENABLE = no
VIAL_ENABLE = no

# https://docs.qmk.fm/#/custom_quantum_functions?id=deferred-execution
DEFERRED_EXEC_ENABLE = yes

# caps word
CAPS_WORD_ENABLE = yes

# swap hands (CAD use)
SWAP_HANDS_ENABLE = yes

# key overrides & combos
COMBO_ENABLE = yes
INTROSPECTION_KEYMAP_C = keyboards/handwired/planck/keymaps/dotdash1/key_combos.c
SRC += keyboards/handwired/planck/keymaps/dotdash1/overrides.c
SRC += keyboards/handwired/planck/keymaps/dotdash1/rgb_layers.c
