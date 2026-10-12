# LEGv8 Single-Cycle Datapath

A Python simulator of a single-cycle LEGv8 CPU. Each instruction is fetched, decoded,
routed through the control unit, ALU, register file and memory, and written back in one
cycle. Programs are pre-encoded `.hex` files and stop at `0x00000000` (HALT).

Supported instructions: `ADD`, `SUB` (R), `ADDI`, `SUBI` (I), `LDUR`, `STUR` (D), `CBZ` (CB), `B` (B).

| File | Purpose |
|---|---|
| `cpu.py` | Simulation loop, fetch, and datapath wiring |
| `control.py` | Main control unit and ALU control |
| `alu.py`, `registers.py`, `memory.py` | ALU, 32×64-bit register file (X31 = XZR), instruction/data memory |
| `run_cpu.py` | Runs one program and prints the final state |
| `auto_grade.py` | Course test runner: checks every program in `test_cases/` against `expected_outputs/` |

## Run

```bash
python auto_grade.py                       # all 13 tests
python run_cpu.py test_cases/test_all.hex  # a single program
```

Course project for Computer Organization, Bahçeşehir University.
