#pragma  once


//----------------------------------------------------------------------------
// home row mods
//----------------------------------------------------------------------------
// https://sunaku.github.io/home-row-mods.html

/* QMK */
#define TAPPING_TERM 175
#define PERMISSIVE_HOLD_PER_KEY
#define HOLD_ON_OTHER_KEY_PRESS_PER_KEY // only f & j
#define FLOW_TAP_TERM 150 // aka require-prior-idle-ms
#define CHORDAL_HOLD

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
