# Cache Performance Simulator

A set-associative cache simulator with LRU replacement, tuned under a fixed 4096-byte budget.

The chosen design, **1024-byte blocks, 2-way set associative**, came from testing every
valid block-size/associativity combination against the benchmark trace and picking the one
with the fewest total cycles. Large blocks capture the sequential and strided access
patterns, and 2-way associativity stops the two alternating "ping-pong" arrays from
evicting each other.

Result on `traces/benchmark.txt`: **85.71% hit rate, 3392 total cycles, AMAT 30.29 cycles/access.**

| File | Purpose |
|---|---|
| `cache_student.py` | The cache (valid bit, tag, LRU) and the chosen configuration |
| `autograder.py` | Course benchmark runner and scoring |
| `test_cache.py` | Unit tests |
| `config.py`, `config_checks.py`, `performance_thresholds.py`, `trace_reader.py` | Course-provided support files |

## Run

```bash
python autograder.py
python -m unittest test_cache
```

Course project for Computer Organization, Bahçeşehir University.
