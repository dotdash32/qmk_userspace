#pragma once

#include QMK_KEYBOARD_H

// ============================================================
// Layer 0 - Base (QWERTY + home row mods)
// ============================================================

// Top row
#define DD_L0_TOP_L  KC_Q, KC_W, KC_E, KC_R, KC_T
#define DD_L0_TOP_R  KC_Y, KC_U, KC_I, KC_O, KC_P

// Home row (with home row mods)
#define DD_L0_HRM_L  RALT_T(KC_A), RCTL_T(KC_S), LT(2,KC_D), LSFT_T(KC_F), LALT_T(KC_G)
#define DD_L0_HRM_R  LALT_T(KC_H), RSFT_T(KC_J), LT(2,KC_K), RCTL_T(KC_L), RALT_T(KC_QUOT)

// Bottom row
#define DD_L0_BOT_L  LSFT_T(KC_Z), LCTL_T(KC_X), LALT_T(KC_C), LGUI_T(KC_V), KC_B
#define DD_L0_BOT_R  KC_N, LGUI_T(KC_M), LALT_T(KC_COMM), LCTL_T(KC_DOT), RSFT_T(KC_SLSH)

// Thumbs
#define DD_L0_THM_L  SH_OS, LT(4,KC_S), LT(2,KC_BSPC)
#define DD_L0_THM_R  TT(1), LT(1,KC_SPC), LT(6, KC_ESC)

// ============================================================
// Layer 1 - Nav
// ============================================================

#define DD_L1_TOP_L  KC_Q, KC_BSPC, KC_DEL, KC_ESC, LCTL(KC_SPC)
#define DD_L1_TOP_R  KC_HOME, KC_PGDN, KC_PGUP, KC_END, KC_BSPC

#define DD_L1_HRM_L  RALT_T(KC_A), RCTL_T(KC_S), LT(2,KC_D), LSFT_T(KC_F), KC_TAB
#define DD_L1_HRM_R  KC_LEFT, RSFT_T(KC_DOWN), LT(2,KC_UP), RCTL_T(KC_RGHT), RALT_T(KC_SCLN)

#define DD_L1_BOT_L  LSFT_T(KC_Z), LCTL_T(KC_X), LALT_T(KC_C), LGUI_T(KC_V), LCTL(KC_B)
#define DD_L1_BOT_R  KC_LBRC, LGUI_T(KC_SPC), LALT_T(KC_RBRC), LCTL_T(KC_DOT), RSFT_T(KC_ENT)

#define DD_L1_THM_L  KC_TRNS, KC_TRNS, KC_TRNS
#define DD_L1_THM_R  KC_TRNS, KC_TRNS, KC_TRNS

// ============================================================
// Layer 2 - Num/Sym
// ============================================================

#define DD_L2_TOP_L  KC_Q, KC_BSPC, KC_DEL, KC_ESC, QK_USER_1
#define DD_L2_TOP_R  CW_TOGG, KC_MINS, KC_EQL, KC_COLN, KC_BSPC

#define DD_L2_HRM_L  RALT_T(KC_1), RCTL_T(KC_2), LT(2,KC_3), LSFT_T(KC_4), LALT_T(KC_5)
#define DD_L2_HRM_R  LALT_T(KC_6), RSFT_T(KC_7), LT(2,KC_8), RCTL_T(KC_9), RALT_T(KC_0)

#define DD_L2_BOT_L  LSFT_T(KC_GRV), LCTL_T(QK_USER_0), LALT_T(KC_COPY), LGUI_T(KC_PSTE), CW_TOGG
#define DD_L2_BOT_R  KC_BSLS, LGUI_T(KC_0), LALT_T(KC_SLSH), LCTL_T(KC_DOT), RSFT_T(KC_ENT)

#define DD_L2_THM_L  KC_TRNS, KC_TRNS, KC_TRNS
#define DD_L2_THM_R  KC_TRNS, KC_TRNS, KC_TRNS

// ============================================================
// Layer 3 - System/Media
// ============================================================

#define DD_L3_TOP_L  CG_RSWP, CG_RNRM, QK_BOOT, DB_TOGG, KC_NO
#define DD_L3_TOP_R  KC_NO, KC_NO, KC_NO, KC_VOLU, LGUI(KC_L)

#define DD_L3_HRM_L  KC_NO, KC_NO, KC_NO, KC_NO, KC_NO
#define DD_L3_HRM_R  KC_NO, KC_NO, KC_MUTE, KC_VOLD, KC_NO

#define DD_L3_BOT_L  KC_NO, KC_NO, KC_NO, KC_NO, KC_NO
#define DD_L3_BOT_R  KC_NO, KC_NO, KC_MPRV, KC_MNXT, KC_MPLY

#define DD_L3_THM_L  KC_TRNS, KC_TRNS, KC_TRNS
#define DD_L3_THM_R  KC_TRNS, KC_TRNS, KC_TRNS

// ============================================================
// Layer 4 - Numpad
// ============================================================

#define DD_L4_TOP_L  OS_LSFT, KC_BSPC, KC_E, KC_ESC, QK_USER_2
#define DD_L4_TOP_R  KC_SLSH, KC_7, KC_8, KC_9, KC_BSPC

#define DD_L4_HRM_L  RALT_T(KC_A), RCTL_T(KC_DOT), LT(2,KC_D), LSFT_T(KC_F), LALT_T(KC_E)
#define DD_L4_HRM_R  KC_DOT, KC_4, KC_5, KC_6, KC_TAB

#define DD_L4_BOT_L  LSFT_T(QK_USER_3), LCTL_T(KC_X), LALT_T(KC_C), LGUI_T(KC_G), KC_B
#define DD_L4_BOT_R  KC_0, KC_1, KC_2, KC_3, KC_ENT

#define DD_L4_THM_L  SH_OS, KC_TRNS, KC_TRNS
#define DD_L4_THM_R  KC_TRNS, KC_TRNS, KC_TRNS

// ============================================================
// Layer 5 - Mouse
// ============================================================

#define DD_L5_TOP_L  KC_TRNS, KC_TRNS, KC_TRNS, KC_WBAK, KC_WFWD
#define DD_L5_TOP_R  MS_WHLL, MS_WHLD, MS_WHLU, MS_WHLR, KC_NO

#define DD_L5_HRM_L  MS_BTN4, MS_BTN2, MS_BTN3, MS_BTN1, MS_BTN5
#define DD_L5_HRM_R  MS_LEFT, MS_DOWN, MS_UP, MS_RGHT, MS_BTN1

#define DD_L5_BOT_L  KC_LSFT, MS_ACL2, MS_ACL1, MS_ACL0, KC_RCTL
#define DD_L5_BOT_R  KC_RCTL, KC_LGUI, KC_LALT, KC_LCTL, KC_RSFT

#define DD_L5_THM_L  KC_TRNS, KC_TRNS, KC_TRNS
#define DD_L5_THM_R  KC_TRNS, KC_TRNS, KC_TRNS

// ============================================================
// Layer 6 - Function keys
// ============================================================

#define DD_L6_TOP_L  KC_Q, KC_BSPC, KC_DEL, KC_ESC, QK_USER_1
#define DD_L6_TOP_R  KC_F11, KC_F12, KC_F13, KC_F14, KC_F15

#define DD_L6_HRM_L  RALT_T(KC_F1), RCTL_T(KC_F2), LT(2,KC_F3), LSFT_T(KC_F4), LALT_T(KC_F5)
#define DD_L6_HRM_R  LALT_T(KC_F6), RSFT_T(KC_F7), LT(2,KC_F8), RCTL_T(KC_F9), RALT_T(KC_F10)

#define DD_L6_BOT_L  LSFT_T(KC_GRV), LCTL_T(QK_USER_0), LALT_T(KC_COPY), LGUI_T(KC_PSTE), CW_TOGG
#define DD_L6_BOT_R  KC_BSLS, LGUI_T(KC_0), LALT_T(KC_COMM), LCTL_T(KC_DOT), RSFT_T(KC_ENT)

#define DD_L6_THM_L  KC_TRNS, KC_TRNS, KC_TRNS
#define DD_L6_THM_R  KC_TRNS, KC_TRNS, KC_TRNS

// ============================================================
// Full-layer convenience macros (for 3x5+3 layouts)
// ============================================================

#define DD_LAYER_0  DD_L0_TOP_L, DD_L0_TOP_R, DD_L0_HRM_L, DD_L0_HRM_R, DD_L0_BOT_L, DD_L0_BOT_R, DD_L0_THM_L, DD_L0_THM_R
#define DD_LAYER_1  DD_L1_TOP_L, DD_L1_TOP_R, DD_L1_HRM_L, DD_L1_HRM_R, DD_L1_BOT_L, DD_L1_BOT_R, DD_L1_THM_L, DD_L1_THM_R
#define DD_LAYER_2  DD_L2_TOP_L, DD_L2_TOP_R, DD_L2_HRM_L, DD_L2_HRM_R, DD_L2_BOT_L, DD_L2_BOT_R, DD_L2_THM_L, DD_L2_THM_R
#define DD_LAYER_3  DD_L3_TOP_L, DD_L3_TOP_R, DD_L3_HRM_L, DD_L3_HRM_R, DD_L3_BOT_L, DD_L3_BOT_R, DD_L3_THM_L, DD_L3_THM_R
#define DD_LAYER_4  DD_L4_TOP_L, DD_L4_TOP_R, DD_L4_HRM_L, DD_L4_HRM_R, DD_L4_BOT_L, DD_L4_BOT_R, DD_L4_THM_L, DD_L4_THM_R
#define DD_LAYER_5  DD_L5_TOP_L, DD_L5_TOP_R, DD_L5_HRM_L, DD_L5_HRM_R, DD_L5_BOT_L, DD_L5_BOT_R, DD_L5_THM_L, DD_L5_THM_R
#define DD_LAYER_6  DD_L6_TOP_L, DD_L6_TOP_R, DD_L6_HRM_L, DD_L6_HRM_R, DD_L6_BOT_L, DD_L6_BOT_R, DD_L6_THM_L, DD_L6_THM_R
