class ALU:
    def execute(self, operand_a, operand_b, alu_control):
        mask = 0xFFFFFFFFFFFFFFFF

        if alu_control == 0:       # ADD
            result = (operand_a + operand_b) & mask
        elif alu_control == 1:     # SUBTRACT
            result = (operand_a - operand_b) & mask
        else:
            result = 0

        zero_flag = (result == 0)
        return result, zero_flag
