#include QMK_KEYBOARD_H

enum combos {
    UI_LPRN,
    IO_RPRN,
    OP_MINS,
    DK_TG2_,
};

const uint16_t PROGMEM ui_combo[] = {KC_U, KC_I, COMBO_END};
const uint16_t PROGMEM io_combo[] = {KC_I, KC_O, COMBO_END};
const uint16_t PROGMEM op_combo[] = {KC_O, KC_P, COMBO_END};
const uint16_t PROGMEM dk_combo[] = {LT(2,KC_D), LT(2,KC_K), COMBO_END};


combo_t key_combos[] = {
    [UI_LPRN] = COMBO(ui_combo, KC_LPRN),
    [IO_RPRN] = COMBO(io_combo, KC_RPRN),
    [OP_MINS] = COMBO(op_combo, KC_MINS),
    [DK_TG2_] = COMBO(dk_combo, TG(2)),
};
