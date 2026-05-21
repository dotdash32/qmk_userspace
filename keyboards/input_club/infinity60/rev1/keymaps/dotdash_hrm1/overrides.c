#include QMK_KEYBOARD_H

const key_override_t space_underscore_override = ko_make_with_layers_negmods_and_options(
    MOD_MASK_SHIFT,
    LT(3,KC_SPC),
    KC_UNDS,
    ~0,
    MOD_MASK_CAG,
    ko_options_default
);

const key_override_t *key_overrides[] = {
    &space_underscore_override,
};

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
    if (is_caps_word_on() && record->event.pressed) {
        if ((get_mods() & MOD_MASK_SHIFT) && (keycode == LT(3,KC_SPC) || keycode == KC_SPC)) {
            uint8_t held_mods = get_mods();
            del_mods(MOD_MASK_SHIFT);
            tap_code16(KC_UNDS);
            set_mods(held_mods);
            return false;
        }
    }
    return true;
}
