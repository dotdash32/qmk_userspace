#include QMK_KEYBOARD_H

enum combos {
    DK_TG2_,
    L2_TG2_,
    QW_TAB_,
    WS_TAB_,
    PUNC_TAB_,
    DSLH_TERM,
    ZX_GRV_,
    CV_UNDS,
    UJ_LPRN,
    IK_RPRN,
    OL_MINS,
    FJ_OSS_,
    QWET_BOOT,
    YIOP_BOOT,
    QET_OSL3,
    YIP_OSL3,
    TG_WBAK,
};

const uint16_t PROGMEM uj_combo[] = {KC_U, RSFT_T(KC_J), COMBO_END};
const uint16_t PROGMEM ik_combo[] = {KC_I, LT(2,KC_K), COMBO_END};
const uint16_t PROGMEM ol_combo[] = {KC_O, RCTL_T(KC_L), COMBO_END};
const uint16_t PROGMEM dk_combo[] = {LT(2,KC_D), LT(2,KC_K), COMBO_END};
const uint16_t PROGMEM L2_combo[] = {LT(2,KC_3), LT(2,KC_8), COMBO_END};
const uint16_t PROGMEM qw_combo[] = {KC_Q, KC_W, COMBO_END};
const uint16_t PROGMEM ws_combo[] = {KC_W, RCTL_T(KC_S), COMBO_END};
const uint16_t PROGMEM punc_combo[] = {LALT_T(KC_COMM), LCTL_T(KC_DOT), COMBO_END};
const uint16_t PROGMEM dslh_combo[] = {LCTL_T(KC_DOT), RSFT_T(KC_SLSH), COMBO_END};
const uint16_t PROGMEM zx_combo[] = {LSFT_T(KC_Z), LCTL_T(KC_X), COMBO_END};
const uint16_t PROGMEM cv_combo[] = {LALT_T(KC_C), LGUI_T(KC_V), COMBO_END};
const uint16_t PROGMEM fj_combo[] = {LSFT_T(KC_F), RSFT_T(KC_J), COMBO_END};
const uint16_t PROGMEM qwet_combo[] = {KC_Q, KC_W, KC_E, KC_T, COMBO_END};
const uint16_t PROGMEM yiop_combo[] = {KC_Y, KC_I, KC_O, KC_P, COMBO_END};
const uint16_t PROGMEM qet_combo[] = {KC_Q, KC_E, KC_T, COMBO_END};
const uint16_t PROGMEM yip_combo[] = {KC_Y, KC_I, KC_P, COMBO_END};
const uint16_t PROGMEM tg_combo[] = {KC_T, LALT_T(KC_G), COMBO_END};


combo_t key_combos[] = {
    [UJ_LPRN] = COMBO(uj_combo, KC_LPRN),
    [IK_RPRN] = COMBO(ik_combo, KC_RPRN),
    [OL_MINS] = COMBO(ol_combo, KC_MINS),
    [DK_TG2_] = COMBO(dk_combo, TG(2)),
    [L2_TG2_] = COMBO(dk_combo, TG(2)),
    [QW_TAB_] = COMBO(qw_combo, KC_TAB),
    [WS_TAB_] = COMBO(ws_combo, KC_TAB),
    [PUNC_TAB_] = COMBO(punc_combo, KC_TAB),
    [DSLH_TERM] = COMBO(dslh_combo, LCTL(KC_GRV)),
    [ZX_GRV_] = COMBO(zx_combo, KC_GRV),
    [CV_UNDS] = COMBO(cv_combo, KC_UNDS),
    [FJ_OSS_] = COMBO(fj_combo, OSM(MOD_LSFT)),
    [QWET_BOOT] = COMBO(qwet_combo, QK_BOOT),
    [YIOP_BOOT] = COMBO(yiop_combo, QK_BOOT),
    [QET_OSL3] = COMBO(qet_combo, OSL(3)),
    [YIP_OSL3] = COMBO(yip_combo, OSL(3)),
    [TG_WBAK] = COMBO(tg_combo, KC_WBAK),
};

#ifdef COMMUNITY_MODULE_CUSTOM_SHIFT_KEYS_ENABLE
#include "modules/getreuer/custom_shift_keys/custom_shift_keys.h"
const custom_shift_key_t custom_shift_keys[] = {
    {LT(1,KC_SPC), KC_UNDS},  // Shift Space is _
    {KC_SPC, KC_UNDS},         // Shift Space is _
    {RALT_T(KC_0), KC_COLN},   // Shift 0 → :
};
#endif
