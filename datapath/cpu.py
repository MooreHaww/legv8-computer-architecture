# Name: Mohammad
# Surname: Hawwari

from memory import InstructionMemory, DataMemory
from registers import RegisterFile
from control import MainControl, ALUControl
from alu import ALU



def sign_extend(value, width):
    sign_bit = 1 << (width - 1)
    if value & sign_bit:
        value -= (1 << width)
    return value


class LEGv8_CPU:
    def __init__(self, hex_file_path):
        self.pc = 0
        self.imem = InstructionMemory(hex_file_path)
        self.dmem = DataMemory()
        self.reg_file = RegisterFile()
        self.main_ctrl = MainControl()
        self.alu_ctrl = ALUControl()
        self.alu = ALU()
        self.halted = False

        self.current_instr = 0
        self.ctrl_signals = {}

    def run(self):
        cycle = 0
        print("--- Simulation Start ---")
        while not self.halted:
            self.step()
            if not self.halted:
                self.log_state(cycle)
            cycle += 1
        print("--- Simulation Halted ---")

    def step(self):
        self.current_instr = self.imem.read(self.pc)

        if self.current_instr == 0:
            self.halted = True
            return

        instr = self.current_instr

        # --- Fetch & decode fields ---
        opcode11 = (instr >> 21) & 0x7FF          # top 11 bits: R/D-format opcode
        Rm = (instr >> 16) & 0x1F                 # bits[20:16]
        Rn = (instr >> 5) & 0x1F                  # bits[9:5]
        Rd = instr & 0x1F                         # bits[4:0]  (Rd / Rt)

        self.ctrl_signals = self.main_ctrl.decode(opcode11)
        sig = self.ctrl_signals

        is_cbz = (opcode11 >> 3) == self.main_ctrl.CB_CBZ
        is_b = (opcode11 >> 5) == self.main_ctrl.B_B

        # --- Register reads ---
        # Read register 1 is normally Rn, except CBZ, whose tested register
        # sits in the Rt/Rd bit position (bits[4:0]).
        read1_addr = Rd if is_cbz else Rn
        read2_addr = Rd if sig['Reg2Loc'] else Rm
        reg1, reg2 = self.reg_file.read(read1_addr, read2_addr)

        # --- Immediate / offset generation ---
        imm12 = sign_extend((instr >> 10) & 0xFFF, 12)   # I-format immediate
        addr9 = sign_extend((instr >> 12) & 0x1FF, 9)   # D-format byte offset
        cb_off19 = sign_extend((instr >> 5) & 0x7FFFF, 19)
        b_off26 = sign_extend(instr & 0x3FFFFFF, 26)

        is_dformat = opcode11 in (self.main_ctrl.D_LDUR, self.main_ctrl.D_STUR)

        if sig['ALUSrc']:
            alu_b = addr9 if is_dformat else imm12
        elif is_cbz:
            alu_b = 0   # force the comparison to be against zero only
        else:
            alu_b = reg2

        # --- ALU ---
        alu_control = self.alu_ctrl.get_alu_control(sig['ALUOp'], opcode11)
        alu_result, zero_flag = self.alu.execute(reg1, alu_b, alu_control)
        alu_result &= 0xFFFFFFFFFFFFFFFF

        # --- Memory stage ---
        if sig['MemWrite']:
            self.dmem.write_word(alu_result, reg2)

        mem_data = self.dmem.read_word(alu_result) if sig['MemRead'] else 0

        # --- Write-back ---
        if sig['RegWrite']:
            write_data = mem_data if sig['MemtoReg'] else alu_result
            self.reg_file.write(Rd, write_data)

        # --- PC update ---
        # LEGv8 branch targets are PC-relative to the branch instruction's
        # OWN address (current self.pc), not PC+4.
        branch_base = self.pc
        if sig['Branch'] and (sig['ALUOp'] == 0 or zero_flag):
            offset_words = b_off26 if is_b else cb_off19
            self.pc = branch_base + (offset_words * 4)
        else:
            self.pc = self.pc + 4

    def log_state(self, cycle):
        print(f"Cycle: {cycle}")
        print(f"PC: {self.pc}")
        print(f"Instruction: 0x{self.current_instr:08X}")

        if self.ctrl_signals:
            print("Control Signals:")
            for key, value in self.ctrl_signals.items():
                 print(f"  {key}: {value}")
        else:
            print("Control Signals: [MISSING - Check step() implementation]")

        print("Registers (Non-Zero):")
        for i in range(32):
            val = self.reg_file.read(i, 31)[0]
            if val != 0:
                print(f"  X{i}: {val}")
        print("-" * 20)
