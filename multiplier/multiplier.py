"""
multiplier.py

Core bitwise logic of a 32-bit sequential (shift-add) multiplier.

Rules for this file:
  - Inputs are 32-bit unsigned integers.
  - Output is a 64-bit unsigned integer product.
  - All additions MUST use alu.bitwise_add(...).
  - Standard arithmetic operators are strictly banned here: +, -, *, /, //, %
"""

from __future__ import annotations

from alu import bitwise_add


MASK_32 = 0xFFFFFFFF
MASK_64 = 0xFFFFFFFFFFFFFFFF


def simulate_multiplier(multiplicand: int, multiplier: int) -> int:
  
    multiplicand &= MASK_32
    multiplier &= MASK_32

    product = 0
  
    multiplicand = multiplicand & MASK_64

    for _ in range(32):
        lsb = multiplier & 1
    
        if lsb == 1:
            product = bitwise_add(product, multiplicand, 64)
          
        multiplicand = (multiplicand << 1) & MASK_64
        
        multiplier >>= 1
        

    return product & MASK_64