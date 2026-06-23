#pragma  once

#define EE_HANDS

/* QMK Home Row Mods settings */
#define TAPPING_TERM 175
#define HOLD_ON_OTHER_KEY_PRESS
#define FLOW_TAP_TERM 150 // aka require-prior-idle-ms
#define CHORDAL_HOLD

/* Custom shift keys: disable when any mod besides shift is held */
#define CUSTOM_SHIFT_KEYS_NEGMODS 0xDD // (MOD_MASK_CG | MOD_MASK_ALT)

/* Caps word */
#define DOUBLE_TAP_SHIFT_TURNS_ON_CAPS_WORD
