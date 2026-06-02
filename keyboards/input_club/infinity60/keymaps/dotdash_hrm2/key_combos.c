#include QMK_KEYBOARD_H

enum combos {
    UI_LPRN,
    IO_RPRN,
    OP_MINS,
    DK_TG2_,
    QW_TAB_,
    ZX_GRV_,
};

const uint16_t PROGMEM ui_combo[] = {KC_U, KC_I, COMBO_END};
const uint16_t PROGMEM io_combo[] = {KC_I, KC_O, COMBO_END};
const uint16_t PROGMEM op_combo[] = {KC_O, KC_P, COMBO_END};
const uint16_t PROGMEM dk_combo[] = {LT(2,KC_D), LT(2,KC_K), COMBO_END};
const uint16_t PROGMEM qw_combo[] = {KC_Q, KC_W, COMBO_END};
const uint16_t PROGMEM zx_combo[] = {LCTL_T(KC_Z), KC_X, COMBO_END};


combo_t key_combos[] = {
    [UI_LPRN] = COMBO(ui_combo, KC_LPRN),
    [IO_RPRN] = COMBO(io_combo, KC_RPRN),
    [OP_MINS] = COMBO(op_combo, KC_MINS),
    [DK_TG2_] = COMBO(dk_combo, TG(2)),
    [QW_TAB_] = COMBO(qw_combo, KC_TAB),
    [ZX_GRV_] = COMBO(zx_combo, KC_GRV),
};

#ifdef COMMUNITY_MODULE_CUSTOM_SHIFT_KEYS_ENABLE
#include "modules/getreuer/custom_shift_keys/custom_shift_keys.h"
const custom_shift_key_t custom_shift_keys[] = {
    {LT(3,KC_SPC), KC_UNDS},  // Shift Space is _
    {KC_SPC, KC_UNDS},         // Shift Space is _
};
#endif
