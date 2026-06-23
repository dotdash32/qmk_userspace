#pragma  once


//----------------------------------------------------------------------------
// home row mods
//----------------------------------------------------------------------------
// https://sunaku.github.io/home-row-mods.html

/* QMK */
#define TAPPING_TERM 200
#define PERMISSIVE_HOLD
#define FLOW_TAP_TERM 150 // aka require-prior-idle-ms
#define CHORDAL_HOLD

/* Custom shift keys: disable when any mod besides shift is held */
#define CUSTOM_SHIFT_KEYS_NEGMODS (MOD_MASK_CG | MOD_MASK_ALT)

/* Caps word */
#define DOUBLE_TAP_SHIFT_TURNS_ON_CAPS_WORD
