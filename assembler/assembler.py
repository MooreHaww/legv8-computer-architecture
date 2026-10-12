# Student information
# Name: MOHAMMAD AMMAR
# Surname: HAWWARI

import sys
import glob
import os


def load_opcode_map():
    """Return a dictionary mapping instruction names to format and opcode."""
    opcode_map = {
        "ADD":  {"format": "R",  "opcode": 0x458},
        "SUB":  {"format": "R",  "opcode": 0x658},
        "ADDI": {"format": "I",  "opcode": 0x244},
        "SUBI": {"format": "I",  "opcode": 0x344},
        "LDUR": {"format": "D",  "opcode": 0x7C2},
        "STUR": {"format": "D",  "opcode": 0x7C0},
        "CBZ":  {"format": "CB", "opcode": 0xB4},
        "B":    {"format": "B",  "opcode": 0x5},
    }
    return opcode_map


def to_twos_complement(val, bits):
    """Convert signed integer to two's complement representation in 'bits' width."""
    return val & ((1 << bits) - 1)


def parse_register(token):
    """Parse a register token like X1, X2, XZR and return its number (0-31)."""
    token = token.strip().upper()
    if token == "XZR":
        return 31
    if token.startswith("X"):
        return int(token[1:])
    raise ValueError(f"Unknown register: {token}")


def parse_immediate(token):
    """Parse an immediate token like #5 or #-3 and return its integer value."""
    token = token.strip()
    if token.startswith("#"):
        token = token[1:]
    return int(token)


def encode_instruction(line, opcode_map):
    """Return 32-bit integer encoding for *line*."""

    # Tokenize: remove commas, split on whitespace
    tokens = line.replace(",", " ").split()
    if not tokens:
        return None

    mnemonic = tokens[0].upper()

    if mnemonic not in opcode_map:
        raise ValueError(f"Unknown instruction: {mnemonic}")

    fmt    = opcode_map[mnemonic]["format"]
    opcode = opcode_map[mnemonic]["opcode"]

    # ------------------------------------------------------------------ #
    #  R-format: ADD / SUB                                                 #
    #  Bits: opcode[31:21] | Rm[20:16] | shamt[15:10] | Rn[9:5] | Rd[4:0]#
    # ------------------------------------------------------------------ #
    if fmt == "R":
        # Syntax: ADD Rd, Rn, Rm
        Rd = parse_register(tokens[1])
        Rn = parse_register(tokens[2])
        Rm = parse_register(tokens[3])
        shamt = 0
        machine_code = (
            (opcode & 0x7FF) << 21 |
            (Rm     & 0x1F)  << 16 |
            (shamt  & 0x3F)  << 10 |
            (Rn     & 0x1F)  << 5  |
            (Rd     & 0x1F)
        )

    # ------------------------------------------------------------------ #
    #  I-format: ADDI / SUBI                                               #
    #  Bits: opcode[31:22] | imm12[21:10] | Rn[9:5] | Rd[4:0]            #
    # ------------------------------------------------------------------ #
    elif fmt == "I":
        # Syntax: ADDI Rd, Rn, #imm
        Rd  = parse_register(tokens[1])
        Rn  = parse_register(tokens[2])
        imm = parse_immediate(tokens[3])
        imm12 = to_twos_complement(imm, 12)
        machine_code = (
            (opcode & 0x3FF) << 22 |
            (imm12  & 0xFFF) << 10 |
            (Rn     & 0x1F)  << 5  |
            (Rd     & 0x1F)
        )

    # ------------------------------------------------------------------ #
    #  D-format: LDUR / STUR                                               #
    #  Bits: opcode[31:21] | offset9[20:12] | op2[11:10] | Rn[9:5] | Rt[4:0]#
    # ------------------------------------------------------------------ #
    elif fmt == "D":
        # Syntax: LDUR Rt, [Rn, #offset]
        Rt = parse_register(tokens[1])
        # tokens[2] = "[Rn,"  tokens[3] = "#offset]"
        rn_tok  = tokens[2].replace("[", "").replace("]", "").replace(",", "")
        imm_tok = tokens[3].replace("[", "").replace("]", "").replace(",", "")
        Rn     = parse_register(rn_tok)
        offset = parse_immediate(imm_tok)
        offset9 = to_twos_complement(offset, 9)
        op2 = 1 if mnemonic == "LDUR" else 3
        machine_code = (
            (opcode   & 0x7FF) << 21 |
            (offset9  & 0x1FF) << 12 |
            (op2      & 0x3)   << 10 |
            (Rn       & 0x1F)  << 5  |
            (Rt       & 0x1F)
        )

    # ------------------------------------------------------------------ #
    #  CB-format: CBZ                                                       #
    #  Bits: opcode[31:24] | offset19[23:5] | Rt[4:0]                     #
    # ------------------------------------------------------------------ #
    elif fmt == "CB":
        # Syntax: CBZ Rt, #offset
        Rt     = parse_register(tokens[1])
        offset = parse_immediate(tokens[2])
        offset19 = to_twos_complement(offset, 19)
        machine_code = (
            (opcode   & 0xFF)   << 24 |
            (offset19 & 0x7FFFF) << 5 |
            (Rt       & 0x1F)
        )

    # ------------------------------------------------------------------ #
    #  B-format: B                                                          #
    #  Bits: opcode[31:26] | offset26[25:0]                                #
    # ------------------------------------------------------------------ #
    elif fmt == "B":
        # Syntax: B #offset
        offset = parse_immediate(tokens[1])
        offset26 = to_twos_complement(offset, 26)
        machine_code = (
            (opcode   & 0x3F)     << 26 |
            (offset26 & 0x3FFFFFF)
        )

    else:
        raise ValueError(f"Unknown format: {fmt}")

    return machine_code & 0xFFFFFFFF


def main():
    """Assemble every .s file under tests/ and write a corresponding .hex file."""
    opcode_map = load_opcode_map()

    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    test_files = sorted(glob.glob("tests/*.s"))
    if not test_files:
        print("No test files found", file=sys.stderr)
        sys.exit(1)

    for input_file in test_files:
        base = os.path.splitext(os.path.basename(input_file))[0]
        out_path = f"outputs/{base}.hex"
        with open(input_file) as fin, open(out_path, 'w') as fout:
            for line in fin:
                line = line.strip()
                if not line or line.startswith('//'):
                    continue
                code = encode_instruction(line, opcode_map)
                if code is not None:
                    fout.write(f"0x{code:08X}\n")


if __name__ == "__main__":
    main()
