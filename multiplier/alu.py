"""
alu.py (Instructor Provided)

This module provides a bitwise-only adder to simulate a hardware ALU.
"""

from __future__ import annotations


def bitwise_add(a: int, b: int, width: int = 64) -> int:
    """
    Add two unsigned integers using strictly bitwise operations.

    - Uses XOR for partial sum, AND+shift for carry propagation.
    - Masks intermediate results to 'width' bits at each step to emulate
      fixed-width hardware behavior.
    """

    if width <= 0:
        raise ValueError("width must be a positive integer")

    mask = (1 << width) - 1
    a &= mask
    b &= mask

    while b != 0:
        carry = (a & b) & mask
        a = (a ^ b) & mask
        b = (carry << 1) & mask

    return a & mask

