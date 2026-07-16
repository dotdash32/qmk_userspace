#include QMK_KEYBOARD_H

// --- Layer lighting (all 4 LEDs) ---

const rgblight_segment_t PROGMEM rgb_base_layer[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 4, HSV_BLUE}
);

const rgblight_segment_t PROGMEM rgb_nav_layer[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 4, HSV_CYAN}
);

const rgblight_segment_t PROGMEM rgb_num_layer[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 4, HSV_PURPLE}
);

const rgblight_segment_t PROGMEM rgb_adjust_layer[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 4, HSV_RED}
);

const rgblight_segment_t PROGMEM rgb_numpad_layer[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 4, HSV_GREEN}
);

const rgblight_segment_t PROGMEM rgb_mouse_layer[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 4, HSV_YELLOW}
);

const rgblight_segment_t PROGMEM rgb_fkeys_layer[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 4, HSV_ORANGE}
);

// --- Modifier indicators (LEDs 0-1 left side, 2-3 right side) ---

const rgblight_segment_t PROGMEM rgb_mod_shift[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 1, HSV_RED},
    {3, 1, HSV_RED}
);

const rgblight_segment_t PROGMEM rgb_mod_ctrl[] = RGBLIGHT_LAYER_SEGMENTS(
    {1, 1, HSV_GREEN},
    {2, 1, HSV_GREEN}
);

const rgblight_segment_t PROGMEM rgb_mod_alt[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 1, HSV_MAGENTA},
    {3, 1, HSV_MAGENTA}
);

const rgblight_segment_t PROGMEM rgb_mod_gui[] = RGBLIGHT_LAYER_SEGMENTS(
    {1, 1, HSV_WHITE},
    {2, 1, HSV_WHITE}
);

const rgblight_segment_t PROGMEM rgb_caps_word[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 4, HSV_CORAL}
);

enum rgb_layer_index {
    RGBL_BASE,
    RGBL_NAV,
    RGBL_NUM,
    RGBL_ADJUST,
    RGBL_NUMPAD,
    RGBL_MOUSE,
    RGBL_FKEYS,
    RGBL_MOD_SHIFT,
    RGBL_MOD_CTRL,
    RGBL_MOD_ALT,
    RGBL_MOD_GUI,
    RGBL_CAPS_WORD,
};

// Layer ordering: layers > mods > caps_word (later = higher priority)
const rgblight_segment_t* const PROGMEM my_rgb_layers[] = RGBLIGHT_LAYERS_LIST(
    rgb_base_layer,     // RGBL_BASE
    rgb_nav_layer,      // RGBL_NAV
    rgb_num_layer,      // RGBL_NUM
    rgb_adjust_layer,   // RGBL_ADJUST
    rgb_numpad_layer,   // RGBL_NUMPAD
    rgb_mouse_layer,    // RGBL_MOUSE
    rgb_fkeys_layer,    // RGBL_FKEYS
    rgb_mod_shift,      // RGBL_MOD_SHIFT
    rgb_mod_ctrl,       // RGBL_MOD_CTRL
    rgb_mod_alt,        // RGBL_MOD_ALT
    rgb_mod_gui,        // RGBL_MOD_GUI
    rgb_caps_word       // RGBL_CAPS_WORD
);

void keyboard_post_init_user(void) {
    rgblight_layers = my_rgb_layers;
    rgblight_set_layer_state(RGBL_BASE, true);
}

layer_state_t layer_state_set_user(layer_state_t state) {
    state = update_tri_layer_state(state, 1, 4, 5);

    rgblight_set_layer_state(RGBL_BASE, layer_state_cmp(state, 0));
    rgblight_set_layer_state(RGBL_NAV, layer_state_cmp(state, 1));
    rgblight_set_layer_state(RGBL_NUM, layer_state_cmp(state, 2));
    rgblight_set_layer_state(RGBL_ADJUST, layer_state_cmp(state, 3));
    rgblight_set_layer_state(RGBL_NUMPAD, layer_state_cmp(state, 4));
    rgblight_set_layer_state(RGBL_MOUSE, layer_state_cmp(state, 5));
    rgblight_set_layer_state(RGBL_FKEYS, layer_state_cmp(state, 6));
    return state;
}

void housekeeping_task_user(void) {
    uint8_t mods = get_mods() | get_oneshot_mods();
    rgblight_set_layer_state(RGBL_MOD_SHIFT, mods & MOD_MASK_SHIFT);
    rgblight_set_layer_state(RGBL_MOD_CTRL, mods & MOD_MASK_CTRL);
    rgblight_set_layer_state(RGBL_MOD_ALT, mods & MOD_MASK_ALT);
    rgblight_set_layer_state(RGBL_MOD_GUI, mods & MOD_MASK_GUI);
}

void caps_word_set_user(bool active) {
    rgblight_set_layer_state(RGBL_CAPS_WORD, active);
}
