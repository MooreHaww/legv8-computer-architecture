class MainControl:
    # Exact 11-bit opcodes for R-format and D-format (these formats use the
    # full top 11 bits as a fixed opcode).
    R_ADD = 0b10001011000   # 0x458
    R_SUB = 0b11001011000   # 0x658
    D_STUR = 0b11111000000  # 0x7C0
    D_LDUR = 0b11111000010  # 0x7C2

    # I-format opcodes are only 10 bits wide; compare the top 10 bits
    # (i.e. the 11-bit field shifted right by 1) so the sign bit of the
    # immediate doesn't affect the match.
    I_ADDI = 0b1001000100   # 0x244
    I_SUBI = 0b1101000100   # 0x344

    # CB-format opcode is only 8 bits wide.
    CB_CBZ = 0b10110100     # 0xB4

    # B-format opcode is only 6 bits wide.
    B_B = 0b000101          # 0x05

    def decode(self, opcode):
        signals = {
            'Reg2Loc': False, 'Branch': False, 'MemRead': False,
            'MemtoReg': False, 'ALUOp': 0, 'MemWrite': False,
            'ALUSrc': False, 'RegWrite': False
        }

        if opcode == self.R_ADD or opcode == self.R_SUB:
            signals['ALUOp'] = 2
            signals['RegWrite'] = True

        elif opcode == self.D_LDUR:
            signals['MemRead'] = True
            signals['MemtoReg'] = True
            signals['ALUSrc'] = True
            signals['RegWrite'] = True
            signals['ALUOp'] = 0

        elif opcode == self.D_STUR:
            signals['Reg2Loc'] = True
            signals['MemWrite'] = True
            signals['ALUSrc'] = True
            signals['ALUOp'] = 0

        elif (opcode >> 1) == self.I_ADDI or (opcode >> 1) == self.I_SUBI:
            signals['ALUSrc'] = True
            signals['RegWrite'] = True
            signals['ALUOp'] = 2

        elif (opcode >> 3) == self.CB_CBZ:
            signals['Branch'] = True
            signals['ALUOp'] = 1

        elif (opcode >> 5) == self.B_B:
            signals['Branch'] = True
            signals['ALUOp'] = 0

        return signals


class ALUControl:
    # Internal convention (only used between MainControl/ALUControl/ALU):
    # 0 = ADD, 1 = SUBTRACT
    ADD = 0
    SUB = 1

    def get_alu_control(self, alu_op, opcode):
        if alu_op == 0:
            return self.ADD
        if alu_op == 1:
            return self.SUB
        # alu_op == 2: R-format or I-format -> look at the opcode bits
        if opcode == MainControl.R_SUB or (opcode >> 1) == MainControl.I_SUBI:
            return self.SUB
        return self.ADD
