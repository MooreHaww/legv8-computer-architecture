"""
codec.py

This file defines the "encoder/decoder" for the file-based test format.

Test cases are plain text files with **binary strings**:
  - Inputs:  "a b"  (two unsigned 32-bit binary integers)
  - Outputs: "p"    (one unsigned 64-bit binary integer)

Functions:
  - decode_u32(token: str) -> int
  - decode_test_case_file(contents: str) -> tuple[int, int]
  - encode_u64(value: int) -> str

Hardware rule:
  - Always mask inputs to 32-bit, outputs to 64-bit.
"""

from __future__ import annotations


MASK_32 = 0xFFFFFFFF
MASK_64 = 0xFFFFFFFFFFFFFFFF


def decode_u32(token: str) -> int:
    value = int(token, 2)
    return value & MASK_32


def decode_test_case_file(contents: str) -> tuple[int, int]:
    tokens = contents.split()

    if len(tokens) != 2:
        raise ValueError(f"Expected exactly 2 binary strings, but found {len(tokens)}.")

    try:
        a = decode_u32(tokens[0])
        b = decode_u32(tokens[1])
    except ValueError as e:
        raise ValueError(f"Invalid binary format in test case: {e}")

    return (a, b)


def encode_u64(value: int) -> str:
    masked_value = value & MASK_64
    
    # Format as binary string ('b'), padded with zeros ('0'), 
    # to a width of 64 characters ('64')
    return f"{masked_value:064b}"