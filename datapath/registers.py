class RegisterFile:
    def __init__(self):
        # 32 general-purpose 64-bit registers. X31 is XZR (always reads as 0).
        self.regs = [0] * 32

    def read(self, reg1, reg2):
        v1 = 0 if reg1 == 31 else self.regs[reg1]
        v2 = 0 if reg2 == 31 else self.regs[reg2]
        return v1, v2

    def write(self, reg, value):
        if reg == 31:
            return  # writes to XZR are discarded
        # keep values modeled as 64-bit two's complement
        self.regs[reg] = value & 0xFFFFFFFFFFFFFFFF
