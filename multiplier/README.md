# 32-bit Shift-Add Multiplier

Simulates a 32-bit sequential (shift-add) hardware multiplier in Python. The multiplier
uses no arithmetic operators: every addition goes through a bitwise ripple adder
(XOR for the sum, AND + shift for the carry), the way an ALU does it in hardware.

| File | Purpose |
|---|---|
| `multiplier.py` | 32-cycle shift-add loop producing a 64-bit product |
| `codec.py` | Reads/writes the binary-string test format |
| `alu.py` | Bitwise-only adder (provided by the course) |
| `run_tests.py` | Runs all 50 cases in `test_cases/` and checks them against `expected_outputs/` |

## Run

```bash
python run_tests.py
```

Course project for Computer Organization, Bahçeşehir University.
