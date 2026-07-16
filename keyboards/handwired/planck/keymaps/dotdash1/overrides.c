#include QMK_KEYBOARD_H
#include "print.h"

/* Note on defined keys:
 ** QK_USER_0: paste code block (``` paste ```)
 ** QK_USER_1: Layer word for numbers (L2)
 ** QK_USER_2: layer word for numpad (L4)
 ** QK_USER_3: layer word for numpad (L4) && Swap hands (cad num entry)
 */

bool remember_last_key_user(uint16_t keycode, keyrecord_t *record, uint8_t *remembered_mods) {
    switch (keycode) {
        case LALT_T(KC_R):
            return false;
    }
    return true;
}

bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    switch (keycode) {
        case LT(4, KC_S):
            if (record->tap.count && record->event.pressed) {
                set_oneshot_mods(MOD_BIT(KC_LSFT));
                return false;
            }
            return true;
        case QK_USER_0:
        case LCTL_T(QK_USER_0):
            if (record->event.pressed) {
                SEND_STRING(SS_LSFT(SS_TAP(X_ENT)) SS_DELAY(100));
                SEND_STRING("```" SS_LSFT(SS_TAP(X_ENT)) SS_DELAY(100));
                tap_code(KC_PSTE);
                SEND_STRING(SS_DELAY(50) SS_LSFT(SS_TAP(X_ENT)) "```");
            }
            return false;
        default:
            break;
    }

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
        case RSFT_T(KC_J):
            is_shift_mt = true;
            term = FLOW_TAP_TERM_FAST;
            break;
        case LT(1, KC_SPC):
            term = FLOW_TAP_TERM_FAST;
            break;
        default:
            term = FLOW_TAP_TERM;
            break;
    }

    if (is_shift_mt && prev_keycode == LT(1, KC_SPC)) {
        return 0;
    }
    return term;
}

// Layer Word callbacks
uint8_t get_layerword_layer_from_trigger(uint16_t keycode) {
    switch (keycode) {
        case QK_USER_1:
            return 2;
        case QK_USER_2:
            return 4;
        case QK_USER_3:
        case LSFT_T(QK_USER_3):
            dprintf("numpad SWAP hands ON");
            swap_hands_on();
            return 4;
        default:
            return 0;
    }
}

bool should_continue_layerword(uint8_t layer, uint16_t keycode, keyrecord_t *record) {
    switch (layer) {
        case 2:
            switch (keycode) {
                case KC_1 ... KC_0:
                case KC_MINS:
                case KC_EQL:
                case KC_BSLS:
                case KC_GRV:
                case KC_DOT:
                case KC_COMM:
                case KC_SLSH:
                case KC_BSPC:
                case KC_DEL:
                    return true;
                default:
                    return false;
            }
        case 4:
            switch(keycode) {
                case KC_A ... KC_F:
                case KC_1 ... KC_0:
                case KC_MINS:
                case KC_EQL:
                case KC_BSLS:
                case KC_GRV:
                case KC_DOT:
                case KC_COMM:
                case KC_SLSH:
                case KC_BSPC:
                case KC_DEL:
                case KC_TAB:
                    return true;
                default:
                    dprintf("numpad SWAP hands OFF, %d / %s", keycode, keycode);
                    swap_hands_off();
                    return false;
            }
    }
    return false;
}

// layer_state_set_user is in rgb_layers.c (includes tri-layer logic)

const keypos_t PROGMEM hand_swap_config[MATRIX_ROWS][MATRIX_COLS] = {
    {{11, 0}, {10, 0}, {9, 0}, {8, 0}, {7, 0}, {6, 0}, {5, 0}, {4, 0}, {3, 0}, {2, 0}, {1, 0}, {0, 0}},
    {{11, 1}, {10, 1}, {9, 1}, {8, 1}, {7, 1}, {6, 1}, {5, 1}, {4, 1}, {3, 1}, {2, 1}, {1, 1}, {0, 1}},
    {{11, 2}, {10, 2}, {9, 2}, {8, 2}, {7, 2}, {6, 2}, {5, 2}, {4, 2}, {3, 2}, {2, 2}, {1, 2}, {0, 2}},
    {{11, 3}, {10, 3}, {9, 3}, {8, 3}, {7, 3}, {6, 3}, {5, 3}, {4, 3}, {3, 3}, {2, 3}, {1, 3}, {0, 3}},
};
