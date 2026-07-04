#pragma  once

#define EE_HANDS

/* QMK Home Row Mods settings */
#define TAPPING_TERM 175
#define PERMISSIVE_HOLD
#define FLOW_TAP_TERM 150 // aka require-prior-idle-ms
#define FLOW_TAP_TERM_FAST 125 // for faster taps
#define CHORDAL_HOLD

/* Mousekey: kinetic speed with sniper/accel via MS_ACL0/MS_ACL2 */
#define MK_COMBINED
#define MOUSEKEY_DELAY 5
#define MOUSEKEY_INTERVAL 20
#define MOUSEKEY_MOVE_DELTA 4
#define MOUSEKEY_MAX_SPEED 12 
#define MOUSEKEY_TIME_TO_MAX 100 
#define MOUSEKEY_WHEEL_MAX_SPEED 8
#define MOUSEKEY_FRICTION 24

/* Custom shift keys: disable when any mod besides shift is held */
#define CUSTOM_SHIFT_KEYS_NEGMODS 0xDD // (MOD_MASK_CG | MOD_MASK_ALT)

/* Caps word */
#define DOUBLE_TAP_SHIFT_TURNS_ON_CAPS_WORD
