#pragma once

// ============================================================
// Layer 0 - Base (QWERTY + home row mods)
// ============================================================

// Individual home row mod keys (for use in combos & overrides)
#define DD_A  RALT_T(KC_A)
#define DD_S  RCTL_T(KC_S)
#define DD_D  LT(_NUM,KC_D)
#define DD_F  LSFT_T(KC_F)
#define DD_G  LALT_T(KC_G)
#define DD_H  LALT_T(KC_H)
#define DD_J  RSFT_T(KC_J)
#define DD_K  LT(_NUM,KC_K)
#define DD_L  RCTL_T(KC_L)
#define DD_QUOT  RALT_T(KC_QUOT)

// Individual bottom row mod keys
#define DD_Z  LSFT_T(KC_Z)
#define DD_X  LCTL_T(KC_X)
#define DD_C  LALT_T(KC_C)
#define DD_V  LGUI_T(KC_V)
#define DD_M  LGUI_T(KC_M)
#define DD_COMM  LALT_T(KC_COMM)
#define DD_DOT  LCTL_T(KC_DOT)
#define DD_SLSH  RSFT_T(KC_SLSH)

// Top row
#define DD_L0_TOP_L  KC_Q, KC_W, KC_E, KC_R, KC_T
#define DD_L0_TOP_R  KC_Y, KC_U, KC_I, KC_O, KC_P

// Home row (with home row mods)
#define DD_L0_HRM_L  DD_A, DD_S, DD_D, DD_F, DD_G
#define DD_L0_HRM_R  DD_H, DD_J, DD_K, DD_L, DD_QUOT

// Bottom row
#define DD_L0_BOT_L  DD_Z, DD_X, DD_C, DD_V, KC_B
#define DD_L0_BOT_R  KC_N, DD_M, DD_COMM, DD_DOT, DD_SLSH

// Thumbs
#define DD_L0_THM_L  SH_OS, LT(_NUMPAD,KC_S), LT(_NUM,KC_BSPC)
#define DD_L0_THM_R  TT(_NAV), LT(_NAV,KC_SPC), LT(_FN, KC_ESC)

// ============================================================
// Layer 1 - Nav
// ============================================================

#define DD_L1_TOP_L  KC_Q, KC_BSPC, KC_DEL, KC_ESC, LCTL(KC_SPC)
#define DD_L1_TOP_R  KC_HOME, KC_PGDN, KC_PGUP, KC_END, KC_BSPC

#define DD_L1_HRM_L  DD_A, DD_S, DD_D, DD_F, KC_TAB
#define DD_L1_HRM_R  KC_LEFT, RSFT_T(KC_DOWN), LT(_NUM,KC_UP), RCTL_T(KC_RGHT), RALT_T(KC_SCLN)

#define DD_L1_BOT_L  DD_Z, DD_X, DD_C, DD_V, LCTL(KC_B)
#define DD_L1_BOT_R  KC_LBRC, LGUI_T(KC_SPC), LALT_T(KC_RBRC), DD_DOT, RSFT_T(KC_ENT)

#define DD_L1_THM_L  KC_TRNS, KC_TRNS, KC_TRNS
#define DD_L1_THM_R  KC_TRNS, KC_TRNS, KC_TRNS

// ============================================================
// Layer 2 - Num/Sym
// ============================================================

#define DD_L2_TOP_L  KC_Q, KC_BSPC, KC_DEL, KC_ESC, DD_LWRD_NUM
#define DD_L2_TOP_R  CW_TOGG, KC_MINS, KC_EQL, KC_COLN, KC_BSPC

#define DD_L2_HRM_L  RALT_T(KC_1), RCTL_T(KC_2), LT(_NUM,KC_3), LSFT_T(KC_4), LALT_T(KC_5)
#define DD_L2_HRM_R  LALT_T(KC_6), RSFT_T(KC_7), LT(_NUM,KC_8), RCTL_T(KC_9), RALT_T(KC_0)

#define DD_L2_BOT_L  LSFT_T(KC_GRV), LCTL_T(DD_CODEBLK), LALT_T(KC_COPY), LGUI_T(KC_PSTE), CW_TOGG
#define DD_L2_BOT_R  KC_BSLS, LGUI_T(KC_0), LALT_T(KC_SLSH), DD_DOT, RSFT_T(KC_ENT)

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

#define DD_L4_TOP_L  OS_LSFT, KC_BSPC, KC_E, KC_ESC, DD_LWRD_PAD
#define DD_L4_TOP_R  KC_SLSH, KC_7, KC_8, KC_9, KC_BSPC

#define DD_L4_HRM_L  RALT_T(KC_A), RCTL_T(KC_DOT), LT(_NUM,KC_D), LSFT_T(KC_F), LALT_T(KC_E)
#define DD_L4_HRM_R  KC_DOT, KC_4, KC_5, KC_6, KC_0

#define DD_L4_BOT_L  LSFT_T(DD_LWRD_PAD_SWAP), DD_X, DD_C, LGUI_T(KC_G), KC_B
#define DD_L4_BOT_R  KC_COMM, KC_1, KC_2, KC_3, KC_ENT

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

#define DD_L6_TOP_L  KC_Q, KC_BSPC, KC_DEL, KC_ESC, DD_LWRD_NUM
#define DD_L6_TOP_R  KC_F11, KC_F12, KC_F13, KC_F14, KC_F15

#define DD_L6_HRM_L  RALT_T(KC_F1), RCTL_T(KC_F2), LT(_NUM,KC_F3), LSFT_T(KC_F4), LALT_T(KC_F5)
#define DD_L6_HRM_R  LALT_T(KC_F6), RSFT_T(KC_F7), LT(_NUM,KC_F8), RCTL_T(KC_F9), RALT_T(KC_F10)

#define DD_L6_BOT_L  LSFT_T(KC_GRV), LCTL_T(DD_CODEBLK), LALT_T(KC_COPY), LGUI_T(KC_PSTE), CW_TOGG
#define DD_L6_BOT_R  KC_BSLS, LGUI_T(KC_0), DD_COMM, DD_DOT, RSFT_T(KC_ENT)

#define DD_L6_THM_L  KC_TRNS, KC_TRNS, KC_TRNS
#define DD_L6_THM_R  KC_TRNS, KC_TRNS, KC_TRNS

// Variadic wrapper to force row macro expansion before LAYOUT counts args
#define DD_LAYOUT(...) LAYOUT_split_3x5_3(__VA_ARGS__)

