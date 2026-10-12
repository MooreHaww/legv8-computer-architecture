# LEGv8 Assembler

A LEGv8 assembler written in Python. It reads LEGv8 assembly (`.s`) and
outputs 32-bit machine code in hex, supporting the R, I, D, B and CB instruction formats.

| File | Purpose |
|---|---|
| `assembler.py` | Encodes each instruction; assembles every file in `tests/` into `outputs/` |
| `tests/` | Sample programs, one per instruction format plus a combined test |
| `answers/` | Expected machine code for each test |
| `run_tests.py` | Runs the assembler and compares `outputs/` with `answers/` |

## Run

```bash
python run_tests.py
```

Course project for Computer Organization, Bahçeşehir University.
