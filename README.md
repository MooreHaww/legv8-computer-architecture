<div align="center">

# 🧠 LEGv8 Computer Architecture

**Four Python projects that build a simple computer from the bottom up: instruction encoding, arithmetic, the CPU, and the cache.**

![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/dependencies-0-success?style=for-the-badge)
![Tests](https://img.shields.io/badge/tests-all%20passing-brightgreen?style=for-the-badge)
![Course](https://img.shields.io/badge/course-CMP2008-8A2BE2?style=for-the-badge)

</div>

---

## 💡 Why this project exists

A processor can feel like magic until you build one. These four projects came from my **Computer Organization** course (CMP2008, Bahçeşehir University). Each one is a layer of the same machine, so together they answer one question: *what actually happens between a line of assembly and a result in memory?*

## 🔎 What it does

| Layer | Folder | What it does | Result |
|---|---|---|---|
| 1. Language | [`assembler/`](assembler) | Turns LEGv8 assembly into 32-bit machine code (R, I, D, B and CB formats) | 6 test programs match the expected hex |
| 2. Arithmetic | [`multiplier/`](multiplier) | 32-bit shift-add multiplier built only from a bitwise adder (XOR for the sum, AND plus shift for the carry) | 50/50 test cases pass |
| 3. CPU | [`datapath/`](datapath) | Single-cycle CPU: fetch, decode, control, ALU, registers, memory, write-back | 13/13 tests, 100/100 |
| 4. Memory | [`cache/`](cache) | Set-associative LRU cache simulator tuned for a 4 KB budget | **85.71% hit rate**, AMAT 30.29 cycles |

The CPU supports `ADD`, `SUB`, `ADDI`, `SUBI`, `LDUR`, `STUR`, `CBZ` and `B`. It also runs edge-case tests: negative immediates, subtraction wrap-around, reading uninitialised memory, branches taken and not taken, and writes to the zero register (X31).

## ⚙️ Setup

You need Python 3.10 or newer. There are no packages to install. Run each command from inside its folder.

```bash
git clone https://github.com/MooreHaww/legv8-computer-architecture.git
cd legv8-computer-architecture

cd assembler  && python run_tests.py   && cd ..
cd multiplier && python run_tests.py   && cd ..
cd datapath   && python auto_grade.py  && cd ..
cd cache      && python autograder.py  && cd ..
```

Run one program on the CPU and print its final state:

```bash
cd datapath
python run_cpu.py test_cases/test_all.hex
```

## 🎯 What I wanted to learn

- How assembly turns into bits: opcode, register and immediate fields for each instruction format.
- How hardware really does arithmetic: addition and multiplication using only bit operations.
- How the pieces of a CPU connect: the control unit decides, the ALU computes, the register file and memory store, and a single clock cycle ties them together.
- Why caches work: block size and associativity trade against each other, and the best choice depends on the access pattern.
- How to test hardware-style code with expected outputs, including the nasty edge cases.

## 🏗️ How it was built

Each project is independent and has its own README. They share one idea: build the real mechanism, then check it against expected output.

- **Assembler:** one function per instruction format that packs fields into 32 bits. Output files are compared with answer files by `run_tests.py`.
- **Multiplier:** a 32-cycle loop. If the lowest bit of the multiplier is 1, add the multiplicand to the product; then shift the multiplicand left and the multiplier right. Every addition goes through the bitwise adder, and `+ - * /` are not used in the multiplier file.
- **Datapath:** separate modules for the control unit, ALU, 32×64-bit register file (X31 is hard-wired to zero) and memory. Programs are pre-encoded `.hex` files that stop at `0x00000000`.
- **Cache:** I tested every valid block-size and associativity pair against the benchmark trace and kept the one with the fewest total cycles: **1024-byte blocks, 2-way set associative**. Large blocks capture the sequential and strided accesses, and 2-way stops the two alternating arrays from evicting each other.

Some support files (the multiplier's adder, the cache autograder and config checks) were given by the course. The student-written parts are the assembler, multiplier loop, datapath and cache design.

## 🗺️ Plan / what's next

- [x] Assembler for five instruction formats
- [x] Shift-add multiplier
- [x] Single-cycle datapath with edge-case tests
- [x] Cache tuned under a 4 KB budget
- [ ] Support more instructions in the assembler and datapath (`AND`, `ORR`, `LSL`, `BL`)
- [ ] Connect the assembler to the datapath so a `.s` file runs without hand-made `.hex`
- [ ] Add a pipelined version with hazard handling
- [ ] Add a plot of hit rate against block size and associativity

## 📄 Notes

Course projects for Computer Organization (CMP2008), Bahçeşehir University. Provided support files belong to the course.
