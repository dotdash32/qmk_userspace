#include QMK_KEYBOARD_H
#include "users/dotdash/dotdash.h"

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [_BASE] = DD_LAYOUT(
        DD_L0_TOP_L, DD_L0_TOP_R,
        DD_L0_HRM_L, DD_L0_HRM_R,
        DD_L0_BOT_L, DD_L0_BOT_R,
        DD_L0_THM_L, DD_L0_THM_R
    ),
    [_NAV] = DD_LAYOUT(
        DD_L1_TOP_L, DD_L1_TOP_R,
        DD_L1_HRM_L, DD_L1_HRM_R,
        DD_L1_BOT_L, DD_L1_BOT_R,
        DD_L1_THM_L, DD_L1_THM_R
    ),
    [_NUM] = DD_LAYOUT(
        DD_L2_TOP_L, DD_L2_TOP_R,
        DD_L2_HRM_L, DD_L2_HRM_R,
        DD_L2_BOT_L, DD_L2_BOT_R,
        DD_L2_THM_L, DD_L2_THM_R
    ),
    [_SYS] = DD_LAYOUT(
        DD_L3_TOP_L, DD_L3_TOP_R,
        DD_L3_HRM_L, DD_L3_HRM_R,
        DD_L3_BOT_L, DD_L3_BOT_R,
        DD_L3_THM_L, DD_L3_THM_R
    ),
    [_NUMPAD] = DD_LAYOUT(
        DD_L4_TOP_L, DD_L4_TOP_R,
        DD_L4_HRM_L, DD_L4_HRM_R,
        DD_L4_BOT_L, DD_L4_BOT_R,
        DD_L4_THM_L, DD_L4_THM_R
    ),
    [_MOUSE] = DD_LAYOUT(
        DD_L5_TOP_L, DD_L5_TOP_R,
        DD_L5_HRM_L, DD_L5_HRM_R,
        DD_L5_BOT_L, DD_L5_BOT_R,
        DD_L5_THM_L, DD_L5_THM_R
    ),
    [_FN] = DD_LAYOUT(
        DD_L6_TOP_L, DD_L6_TOP_R,
        DD_L6_HRM_L, DD_L6_HRM_R,
        DD_L6_BOT_L, DD_L6_BOT_R,
        DD_L6_THM_L, DD_L6_THM_R
    ),
};
