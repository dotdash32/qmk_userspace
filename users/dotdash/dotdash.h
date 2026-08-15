#pragma once

#include QMK_KEYBOARD_H

enum dotdash_layers {
    _BASE,
    _NAV,
    _NUM,
    _SYS,
    _NUMPAD,
    _MOUSE,
    _FN,
};

enum dotdash_keycodes {
    DD_CODEBLK = SAFE_RANGE,  // paste code block (``` paste ```)  // ensure this is unique
    DD_LWRD_NUM,              // layer word: number layer (_NUM)
    DD_LWRD_PAD,              // layer word: numpad layer (_NUMPAD)
    DD_LWRD_PAD_SWAP,         // layer word: numpad + swap hands (CAD entry)
};
