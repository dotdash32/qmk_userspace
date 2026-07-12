
# Cancel out standard features for faster bootup
# BOOTMAGIC_ENABLE = no
COMMAND_ENABLE = no
CONSOLE_ENABLE = yes
EXTRAKEY_ENABLE = yes
MOUSEKEY_ENABLE = no
RGBLIGHT_ENABLE = yes
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
INTROSPECTION_KEYMAP_C = keyboards/handwired/planck/keymaps/dotdash1/key_combos.c
SRC += keyboards/handwired/planck/keymaps/dotdash1/overrides.c
