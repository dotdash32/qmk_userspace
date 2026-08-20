#include "dotdash.h"

enum combos {
    DK_TG2_,
    L2_TG2_,
    WS_TAB_,
    DSLH_ENT_,
    PUNC_TAB_,
    ZX_TERM_,
    CV_UNDS,
    UJ_LPRN,
    IK_RPRN,
    JM_LBRC,
    KCOM_RBRC,
    OL_MINS,
    QWET_BOOT,
    YIOP_BOOT,
    QET_OSL3,
    YIP_OSL3,
    TG_WBAK,
    PQOT_COLN,
    ED_EQL,
    RF_COLN,
};

const uint16_t PROGMEM uj_combo[] = {KC_U, DD_J, COMBO_END};
const uint16_t PROGMEM ik_combo[] = {KC_I, DD_K, COMBO_END};
const uint16_t PROGMEM jm_combo[] = {DD_J, DD_M, COMBO_END};
const uint16_t PROGMEM kcom_combo[] = {DD_K, DD_COMM, COMBO_END};
const uint16_t PROGMEM ol_combo[] = {KC_O, DD_L, COMBO_END};
const uint16_t PROGMEM dk_combo[] = {DD_D, DD_K, COMBO_END};
const uint16_t PROGMEM L2_combo[] = {LT(_NUM,KC_3), LT(_NUM,KC_8), COMBO_END};  // return from L2
const uint16_t PROGMEM ws_combo[] = {KC_W, DD_S, COMBO_END};
const uint16_t PROGMEM punc_combo[] = {DD_COMM, DD_DOT, COMBO_END};
const uint16_t PROGMEM dslh_combo[] = {DD_DOT, DD_SLSH, COMBO_END};
const uint16_t PROGMEM zx_combo[] = {DD_Z, DD_X, COMBO_END};
const uint16_t PROGMEM cv_combo[] = {DD_C, DD_V, COMBO_END};
const uint16_t PROGMEM qwet_combo[] = {KC_Q, KC_W, KC_E, KC_T, COMBO_END};
const uint16_t PROGMEM yiop_combo[] = {KC_Y, KC_I, KC_O, KC_P, COMBO_END};
const uint16_t PROGMEM qet_combo[] = {KC_Q, KC_E, KC_T, COMBO_END};
const uint16_t PROGMEM yip_combo[] = {KC_Y, KC_I, KC_P, COMBO_END};
const uint16_t PROGMEM tg_combo[] = {KC_T, DD_G, COMBO_END};
const uint16_t PROGMEM pqot_combo[] = {KC_P, DD_QUOT, COMBO_END};
const uint16_t PROGMEM ed_combo[] = {KC_E, DD_D, COMBO_END};
const uint16_t PROGMEM rf_combo[] = {KC_R, DD_F, COMBO_END};


combo_t key_combos[] = {
    [UJ_LPRN] = COMBO(uj_combo, KC_LPRN),
    [IK_RPRN] = COMBO(ik_combo, KC_RPRN),
    [JM_LBRC] = COMBO(jm_combo, KC_LBRC),
    [KCOM_RBRC] = COMBO(kcom_combo, KC_RBRC),
    [OL_MINS] = COMBO(ol_combo, KC_MINS),
    [DK_TG2_] = COMBO(dk_combo, TG(_NUM)),
    [L2_TG2_] = COMBO(dk_combo, TG(_NUM)),
    [WS_TAB_] = COMBO(ws_combo, KC_TAB),
    [DSLH_ENT_] = COMBO(dslh_combo, KC_ENT),
    [PUNC_TAB_] = COMBO(punc_combo, KC_TAB),
    [ZX_TERM_] = COMBO(zx_combo, LCTL(KC_GRV)),
    [CV_UNDS] = COMBO(cv_combo, KC_UNDS),
    [QWET_BOOT] = COMBO(qwet_combo, QK_BOOT),
    [YIOP_BOOT] = COMBO(yiop_combo, QK_BOOT),
    [QET_OSL3] = COMBO(qet_combo, OSL(_SYS)),
    [YIP_OSL3] = COMBO(yip_combo, OSL(_SYS)),
    [TG_WBAK] = COMBO(tg_combo, KC_WBAK),
    [PQOT_COLN] = COMBO(pqot_combo, KC_COLN),
    [ED_EQL] = COMBO(ed_combo, KC_EQL),
    [RF_COLN] = COMBO(rf_combo, KC_COLN),
};

#ifdef COMMUNITY_MODULE_CUSTOM_SHIFT_KEYS_ENABLE
#include "modules/getreuer/custom_shift_keys/custom_shift_keys.h"
const custom_shift_key_t custom_shift_keys[] = {
    {LT(_NAV,KC_SPC), KC_UNDS},  // Shift Space is _
    {KC_SPC, KC_UNDS},           // Shift Space is _
    {RALT_T(KC_0), KC_COLN},     // Shift 0 -> :
    {KC_COLN, KC_SCLN},          // Shift P+' combo -> ;
};
#endif
