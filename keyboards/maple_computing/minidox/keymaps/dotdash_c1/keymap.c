#include QMK_KEYBOARD_H
#include "users/dotdash/dotdash_layers.h"

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [_BASE]   = LAYOUT_split_3x5_3(DD_LAYER_0),
    [_NAV]    = LAYOUT_split_3x5_3(DD_LAYER_1),
    [_NUM]    = LAYOUT_split_3x5_3(DD_LAYER_2),
    [_SYS]    = LAYOUT_split_3x5_3(DD_LAYER_3),
    [_NUMPAD] = LAYOUT_split_3x5_3(DD_LAYER_4),
    [_MOUSE]  = LAYOUT_split_3x5_3(DD_LAYER_5),
    [_FN]     = LAYOUT_split_3x5_3(DD_LAYER_6),
};
