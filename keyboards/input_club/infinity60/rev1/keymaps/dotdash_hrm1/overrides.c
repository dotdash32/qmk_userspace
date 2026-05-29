#include QMK_KEYBOARD_H


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

bool is_flow_tap_key(uint16_t keycode) {
    if ((get_mods() & (MOD_MASK_CG | MOD_BIT_LALT)) != 0) {
        return false; // Disable Flow Tap on hotkeys.
    }
    switch (get_tap_keycode(keycode)) {
        case KC_A ... KC_Z:
        case KC_DOT:
        case KC_COMM:
        case KC_SCLN:
        case KC_SLSH:
            return true;
        // explicitly disable space (spaceFN)
        case KC_SPC:
        case LT(3,KC_SPC):
            return false;
    }
    return false;
}

bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    if (record->event.pressed && (keycode == LT(3,KC_SPC) || keycode == KC_SPC)) {
        // Don't intercept if ctrl/alt/gui are also held
        if (get_mods() & (MOD_MASK_CG | MOD_MASK_ALT)) {
            return true;
        }
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
    // Mod-tap/layer-tap can't send shifted keycodes on tap, so handle parens manually
    switch (keycode) {
        case RCTL_T(KC_LPRN):
            if (record->tap.count && record->event.pressed) {
                tap_code16(KC_LPRN);
                return false;
            }
            break;
        case LT(2,KC_RPRN):
            if (record->tap.count && record->event.pressed) {
                tap_code16(KC_RPRN);
                return false;
            }
            break;
    }

    return true;
}
