import sys

from config_checks import inspect_submission_cache
from performance_thresholds import MAIN_MEMORY_LATENCY


def get_submission_cache():
    import cache_student

    cache = getattr(cache_student, "submission_cache", None)
    if cache is None:
        raise ValueError(
            "submission_cache is not defined in cache_student.py. "
            "Add: submission_cache = Cache(4096, block_size, associativity)"
        )
    return cache


def format_latency_banner(hit_cost, miss_cost, associativity, accesses):
    compare_cycles = max(0, associativity - 1)
    baseline_cycles = accesses * MAIN_MEMORY_LATENCY
    lines = [
        "=" * 60,
        f"HIT LATENCY: {hit_cost} cycles per hit",
        f"  (1 base cycle + {compare_cycles} tag-compare cycles for {associativity}-way set)",
        f"MISS LATENCY: {miss_cost} cycles per miss",
        f"MAIN-MEMORY BASELINE: {accesses} x {MAIN_MEMORY_LATENCY} = {baseline_cycles} cycles",
        "=" * 60,
    ]
    return "\n".join(lines)


def run_simulation(trace_file_path):
    submission_cache = get_submission_cache()
    valid, failures, metrics = inspect_submission_cache(submission_cache)
    if not valid:
        raise ValueError("Invalid submission_cache:\n- " + "\n- ".join(failures))

    cache = submission_cache
    hit_cost = metrics["hit_cost"]
    miss_cost = metrics["miss_cost"]
    associativity = metrics["associativity"]

    total = 0
    hits = 0
    misses = 0

    with open(trace_file_path, "r") as trace_file:
        for line in trace_file:
            line = line.strip()
            if not line:
                continue
            address = int(line, 16)
            total += 1
            if cache.access(address):
                hits += 1
            else:
                misses += 1

    total_cycles = (hits * hit_cost) + (misses * miss_cost)
    hit_rate = (hits / total) * 100 if total > 0 else 0.0
    amat = total_cycles / total if total > 0 else 0.0

    print(format_latency_banner(hit_cost, miss_cost, associativity, total))
    print()
    print(f"Accesses: {total}")
    print(f"Hits: {hits}")
    print(f"Misses: {misses}")
    print(f"Hit Rate: {hit_rate:.2f}%")
    print(f"Total Cycles: {total_cycles}")
    print(f"AMAT: {amat:.2f} cycles/access")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <trace_file>")
        return 1

    try:
        run_simulation(sys.argv[1])
    except (ValueError, OSError) as exc:
        print(exc)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
