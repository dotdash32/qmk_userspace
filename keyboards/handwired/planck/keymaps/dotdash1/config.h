#pragma  once


//----------------------------------------------------------------------------
// home row mods
//----------------------------------------------------------------------------
// https://sunaku.github.io/home-row-mods.html

/* QMK Home Row Mods settings */
#define TAPPING_TERM 175
#define PERMISSIVE_HOLD
#define FLOW_TAP_TERM 150 // aka require-prior-idle-ms
#define FLOW_TAP_TERM_FAST 125
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

/* RGB Underglow */
#define WS2812_DI_PIN D5
#define RGBLIGHT_LED_COUNT 4
#define RGBLIGHT_LAYERS
#define RGBLIGHT_LAYERS_OVERRIDE_RGB_OFF
#define RGBLIGHT_LAYERS_RETAIN_VAL
#define RGBLIGHT_MAX_LAYERS 12
#define RGBLIGHT_EFFECT_BREATHING

/* Caps word */
#define DOUBLE_TAP_SHIFT_TURNS_ON_CAPS_WORD
