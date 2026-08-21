#include QMK_KEYBOARD_H
#include "users/dotdash/dotdash.h"

// Cameldox38 thumbs: 4 per side (outer to inner)
#define DD_C38_THM_L0  KC_LALT, KC_LGUI, LT(_NUMPAD,KC_S), LT(_NUM,KC_BSPC)
#define DD_C38_THM_R0  TT(_NAV), LT(_NAV,KC_SPC), LT(_FN,KC_ESC), KC_RALT

#define DD_C38_THM_L1  KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS
#define DD_C38_THM_R1  KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [_BASE] = DD_APPLY(LAYOUT_ortho_3x10_8,
        DD_L0_TOP_L, DD_L0_TOP_R,
        DD_L0_HRM_L, DD_L0_HRM_R,
        DD_L0_BOT_L, DD_L0_BOT_R,
        DD_LTB_INN0, DD_LTB_PRIM, DD_LTB_SECD, DD_LTB_OUT0, DD_RTB_OUT0, DD_RTB_SECD, DD_RTB_PRIM, DD_RTB_INN0
    ),
    [_NAV] = DD_APPLY(LAYOUT_ortho_3x10_8,
        DD_L1_TOP_L, DD_L1_TOP_R,
        DD_L1_HRM_L, DD_L1_HRM_R,
        DD_L1_BOT_L, DD_L1_BOT_R,
        DD_C38_THM_L1, DD_C38_THM_R1
    ),
    [_NUM] = DD_APPLY(LAYOUT_ortho_3x10_8,
        DD_L2_TOP_L, DD_L2_TOP_R,
        DD_L2_HRM_L, DD_L2_HRM_R,
        DD_L2_BOT_L, DD_L2_BOT_R,
        DD_C38_THM_L1, DD_C38_THM_R1
    ),
    [_SYS] = DD_APPLY(LAYOUT_ortho_3x10_8,
        DD_L3_TOP_L, DD_L3_TOP_R,
        DD_L3_HRM_L, DD_L3_HRM_R,
        DD_L3_BOT_L, DD_L3_BOT_R,
        DD_C38_THM_L1, DD_C38_THM_R1
    ),
    [_NUMPAD] = DD_APPLY(LAYOUT_ortho_3x10_8,
        DD_L4_TOP_L, DD_L4_TOP_R,
        DD_L4_HRM_L, DD_L4_HRM_R,
        DD_L4_BOT_L, DD_L4_BOT_R,
        DD_C38_THM_L1, DD_C38_THM_R1
    ),
    [_MOUSE] = DD_APPLY(LAYOUT_ortho_3x10_8,
        DD_L5_TOP_L, DD_L5_TOP_R,
        DD_L5_HRM_L, DD_L5_HRM_R,
        DD_L5_BOT_L, DD_L5_BOT_R,
        DD_C38_THM_L1, DD_C38_THM_R1
    ),
    [_FN] = DD_APPLY(LAYOUT_ortho_3x10_8,
        DD_L6_TOP_L, DD_L6_TOP_R,
        DD_L6_HRM_L, DD_L6_HRM_R,
        DD_L6_BOT_L, DD_L6_BOT_R,
        DD_C38_THM_L1, DD_C38_THM_R1
    ),
};
