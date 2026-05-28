#include QMK_KEYBOARD_H
#include "key_combos.c"


bool caps_word_press_user(uint16_t keycode) {
    switch (keycode) {
        case KC_A ... KC_Z:
        case KC_MINS:
            add_weak_mods(MOD_BIT(KC_LSFT));
            return true;
        case KC_1 ... KC_0:
        case KC_UNDS:
        case KC_BSPC:
        case KC_LSFT:
        case KC_RSFT:
            return true;
        default:
            return false;
    }
}

bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    if (record->event.pressed && (keycode == LT(3,KC_SPC) || keycode == KC_SPC)) {
        uint8_t shift_mods = get_mods() & MOD_MASK_SHIFT;
        if (shift_mods == MOD_MASK_SHIFT) {
            // Both shifts held → underscore
            uint8_t held_mods = get_mods();
            del_mods(MOD_MASK_SHIFT);
            tap_code16(KC_UNDS);
            set_mods(held_mods);
            return false;
        } else if (shift_mods) {
            // Single shift held → hyphen (or underscore during caps_word)
            uint8_t held_mods = get_mods();
            del_mods(MOD_MASK_SHIFT);
            if (is_caps_word_on()) {
                tap_code16(KC_UNDS);
            } else {
                tap_code(KC_MINS);
            }
            set_mods(held_mods);
            return false;
        }
    }
    return true;
}
