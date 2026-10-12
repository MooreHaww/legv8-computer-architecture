# Computer Organization Projects AKA legv8-computer-architecture

Four Python projects that build up the pieces of a simple LEGv8 computer, from the
encoding of instructions down to the cache.

| Folder | What it does | Tests |
|---|---|---|
| [`assembler/`](assembler) | LEGv8 assembler: assembly → 32-bit machine code (R, I, D, B, CB formats) | `python run_tests.py` |
| [`multiplier/`](multiplier) | 32-bit shift-add multiplier built on a bitwise-only adder | `python run_tests.py` |
| [`datapath/`](datapath) | Single-cycle LEGv8 CPU simulator | `python auto_grade.py` |
| [`cache/`](cache) | Set-associative LRU cache simulator, tuned for a 4 KB budget | `python autograder.py` |

Requires Python 3.10+, no external packages. Run each command from inside its folder.

Course projects for Computer Organization (CMP2008), Bahçeşehir University.
