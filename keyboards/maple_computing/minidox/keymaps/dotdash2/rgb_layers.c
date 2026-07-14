#include QMK_KEYBOARD_H

// --- Layer lighting (all 12 LEDs) ---

const rgblight_segment_t PROGMEM rgb_base_layer[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 12, HSV_BLUE}
);

const rgblight_segment_t PROGMEM rgb_nav_layer[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 12, HSV_CYAN}
);

const rgblight_segment_t PROGMEM rgb_num_layer[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 12, HSV_PURPLE}
);

const rgblight_segment_t PROGMEM rgb_adjust_layer[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 12, HSV_RED}
);

const rgblight_segment_t PROGMEM rgb_numpad_layer[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 12, HSV_GREEN}
);

const rgblight_segment_t PROGMEM rgb_mouse_layer[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 12, HSV_YELLOW}
);

const rgblight_segment_t PROGMEM rgb_fkeys_layer[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 12, HSV_ORANGE}
);

// --- Modifier indicators (LEDs 0-1 left side, 10-11 right side) ---

const rgblight_segment_t PROGMEM rgb_mod_shift[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 1, HSV_RED},
    {11, 1, HSV_RED}
);

const rgblight_segment_t PROGMEM rgb_mod_ctrl[] = RGBLIGHT_LAYER_SEGMENTS(
    {1, 1, HSV_GREEN},
    {10, 1, HSV_GREEN}
);

const rgblight_segment_t PROGMEM rgb_mod_alt[] = RGBLIGHT_LAYER_SEGMENTS(
    {2, 1, HSV_MAGENTA},
    {9, 1, HSV_MAGENTA}
);

const rgblight_segment_t PROGMEM rgb_mod_gui[] = RGBLIGHT_LAYER_SEGMENTS(
    {3, 1, HSV_WHITE},
    {8, 1, HSV_WHITE}
);

const rgblight_segment_t PROGMEM rgb_caps_word[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 6, HSV_CORAL},
    {6, 6, HSV_CORAL}
);

// Layer ordering: layers > mods > caps_word (later = higher priority)
const rgblight_segment_t* const PROGMEM my_rgb_layers[] = RGBLIGHT_LAYERS_LIST(
    rgb_base_layer,     // 0
    rgb_nav_layer,      // 1
    rgb_num_layer,      // 2
    rgb_adjust_layer,   // 3
    rgb_numpad_layer,   // 4
    rgb_mouse_layer,    // 5
    rgb_fkeys_layer,    // 6
    rgb_mod_shift,      // 7
    rgb_mod_ctrl,       // 8
    rgb_mod_alt,        // 9
    rgb_mod_gui,        // 10
    rgb_caps_word       // 11
);

void keyboard_post_init_user(void) {
    rgblight_layers = my_rgb_layers;
    rgblight_set_layer_state(0, true);
}

layer_state_t layer_state_set_user(layer_state_t state) {
    state = update_tri_layer_state(state, 1, 4, 5);

    rgblight_set_layer_state(0, layer_state_cmp(state, 0));
    rgblight_set_layer_state(1, layer_state_cmp(state, 1));
    rgblight_set_layer_state(2, layer_state_cmp(state, 2));
    rgblight_set_layer_state(3, layer_state_cmp(state, 3));
    rgblight_set_layer_state(4, layer_state_cmp(state, 4));
    rgblight_set_layer_state(5, layer_state_cmp(state, 5));
    rgblight_set_layer_state(6, layer_state_cmp(state, 6));
    return state;
}

void housekeeping_task_user(void) {
    uint8_t mods = get_mods() | get_oneshot_mods();
    rgblight_set_layer_state(7, mods & MOD_MASK_SHIFT);
    rgblight_set_layer_state(8, mods & MOD_MASK_CTRL);
    rgblight_set_layer_state(9, mods & MOD_MASK_ALT);
    rgblight_set_layer_state(10, mods & MOD_MASK_GUI);
}

void caps_word_set_user(bool active) {
    rgblight_set_layer_state(11, active);
}
