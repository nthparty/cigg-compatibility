"""Load and confirm compatibility of CIGG for current environment."""

import canaries

lib = canaries.load({
    'Linux': ['./cigg.linux.so']
})

assert(lib is not None)
