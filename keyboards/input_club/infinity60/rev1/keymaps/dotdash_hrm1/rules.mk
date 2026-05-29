
# Cancel out standard features for faster bootup
# BOOTMAGIC_ENABLE = no
COMMAND_ENABLE = no
CONSOLE_ENABLE = no
EXTRAKEY_ENABLE = no
MOUSEKEY_ENABLE = no
RGBLIGHT_ENABLE = no
NKRO_ENABLE = no

VIA_ENABLE = no
VIAL_ENABLE = no


# https://docs.qmk.fm/#/custom_quantum_functions?id=deferred-execution
DEFERRED_EXEC_ENABLE = yes

# https://github.com/qmk/qmk_firmware/issues/19593#issuecomment-1387476045
# NO_USB_STARTUP_CHECK = yes

# caps word
CAPS_WORD_ENABLE = yes

# key overrides & combos
COMBO_ENABLE = yes
INTROSPECTION_KEYMAP_C = keyboards/input_club/infinity60/rev1/keymaps/dotdash_hrm1/key_combos.c
SRC += keyboards/input_club/infinity60/rev1/keymaps/dotdash_hrm1/overrides.c