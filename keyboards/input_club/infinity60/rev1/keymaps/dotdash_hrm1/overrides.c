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