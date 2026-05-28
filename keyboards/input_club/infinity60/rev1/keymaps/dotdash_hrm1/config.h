#pragma  once


//----------------------------------------------------------------------------
// home row mods
//----------------------------------------------------------------------------
// https://sunaku.github.io/home-row-mods.html

/* QMK */
#define TAPPING_TERM 200
#define PERMISSIVE_HOLD
#define FLOW_TAP_TERM 150 // aka require-prior-idle-ms
#define CHORDAL_HOLD // does this conflict with BILATERAL_COMBINATIONS?


/* Miryoku */
#define BILATERAL_COMBINATIONS
#define BILATERAL_COMBINATIONS_LIMIT_CHORD_TO_N_KEYS 4 /* GUI, Alt, Ctrl, Shift */
#define BILATERAL_COMBINATIONS_DELAY_MODS_THAT_MATCH MOD_MASK_GUI
#define BILATERAL_COMBINATIONS_DELAY_MATCHED_MODS_BY 120  /* ms */
#define BILATERAL_COMBINATIONS_ALLOW_CROSSOVER_AFTER 80   /* ms */
#define BILATERAL_COMBINATIONS_ALLOW_SAMESIDED_AFTER 3000 /* ms */
#define BILATERAL_COMBINATIONS_TYPING_STREAK_TIMEOUT 160  /* ms */
#define BILATERAL_COMBINATIONS_TYPING_STREAK_MODMASK (~MOD_MASK_SHIFT)

/* Caps word */
#define DOUBLE_TAP_SHIFT_TURNS_ON_CAPS_WORD