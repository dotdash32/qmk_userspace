#include QMK_KEYBOARD_H
#include "print.h"

bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    if (debug_enable) {
        switch (keycode) {
            case LSFT_T(KC_F):
            case RSFT_T(KC_J):
            case LSFT_T(KC_Z):
            case RSFT_T(KC_SLSH):
                if (record->event.pressed) {
                    dprintf("SFT_DN:0x%04X t=%u\n", keycode, record->event.time);
                } else {
                    dprintf("SFT_UP:0x%04X t=%u tap=%u\n", keycode, record->event.time,
                            record->tap.count);
                }
                break;
            case KC_BSPC:
                if (record->event.pressed) {
                    dprintf("BSPC t=%u\n", record->event.time);
                }
                break;
        }
    }
    return true;
}

bool caps_word_press_user(uint16_t keycode) {
    switch (keycode) {
        case KC_A ... KC_Z:
            add_weak_mods(MOD_BIT(KC_LSFT));
            return true;
        case KC_MINS: // don't turn into underscore
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
    }
    return false;
}

uint16_t get_flow_tap_term(uint16_t keycode, keyrecord_t *record, uint16_t prev_keycode) {
    if (prev_keycode == KC_BSPC) {
        return 0;
    }

    bool is_shift_mt = false;
    uint16_t term;
    switch (keycode) {
        case LSFT_T(KC_F):
            is_shift_mt = true;
            term = 100;
            break;
        case RSFT_T(KC_J):
            is_shift_mt = true;
            term = 125;
            break;
        default:
            term = FLOW_TAP_TERM;
            break;
    }

    if (is_shift_mt && prev_keycode == LT(3, KC_SPC)) {
        return 0;
    }
    return term;
}
