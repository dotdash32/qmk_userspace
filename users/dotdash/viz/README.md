# Keymaps visualized

Separately maintained keymap visualizations to make it easier to see what's happening under the hood.  These are based
on the `dotdash.h` and `dotash_layers.h` files, and represent the main alphanumeric "core" set of keys.

### building

```bash
cd qmk_userspace
keymap -c users/dotdash/viz/config.yaml draw users/dotdash/viz/keymap_3x5_3.yaml \
    > users/dotdash/viz/keymap_3x5_3.svg
 
```
