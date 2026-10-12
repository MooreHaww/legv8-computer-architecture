import argparse
import importlib.util
import os
import sys

from config_checks import inspect_submission_cache
from performance_thresholds import (
    MAIN_MEMORY_LATENCY,
    MAX_SCORE,
    PASSING_SCORE,
    SCORE_TIERS,
)

TRACE_PATH = os.path.join(os.path.dirname(__file__), "traces", "benchmark.txt")


def read_trace_addresses(trace_path):
    addresses = []
    with open(trace_path, "r") as trace_file:
        for line in trace_file:
            line = line.strip()
            if line:
                addresses.append(int(line, 16))
    return addresses


def run_trace(cache, addresses):
    hits = 0
    misses = 0
    for address in addresses:
        if cache.access(address):
            hits += 1
        else:
            misses += 1
    return hits, misses


def build_performance(hits, misses, metrics):
    total = hits + misses
    hit_cost = metrics["hit_cost"]
    miss_cost = metrics["miss_cost"]
    total_cycles = (hits * hit_cost) + (misses * miss_cost)
    return {
        "accesses": total,
        "hits": hits,
        "misses": misses,
        "hit_rate": (hits / total) * 100 if total else 0.0,
        "total_cycles": total_cycles,
        "amat": total_cycles / total if total else 0.0,
        "hit_cost": hit_cost,
        "miss_cost": miss_cost,
        "block_size": metrics["block_size"],
        "associativity": metrics["associativity"],
        "sets": metrics["sets"],
        "footprint": metrics["footprint"],
    }


def compute_tier_score(total_cycles, baseline_cycles):
    if total_cycles >= baseline_cycles:
        return 0, None

    earned = 0
    label = None
    for tier in SCORE_TIERS:
        if total_cycles <= tier["max_total_cycles"]:
            earned = tier["score"]
            label = tier["label"]

    return earned, label


def next_tier_target(earned_score):
    for tier in SCORE_TIERS:
        if tier["score"] > earned_score:
            return tier
    return None


def format_latency_banner(performance, baseline_cycles):
    hit_cost = performance["hit_cost"]
    assoc = performance["associativity"]
    compare_cycles = max(0, assoc - 1)
    lines = [
        "=" * 60,
        f"HIT LATENCY: {hit_cost} cycles per hit",
        f"  (1 base cycle + {compare_cycles} tag-compare cycles for {assoc}-way set)",
        f"MISS LATENCY: {performance['miss_cost']} cycles per miss",
        (
            f"MAIN-MEMORY BASELINE: {performance['accesses']} x "
            f"{MAIN_MEMORY_LATENCY} = {baseline_cycles} cycles"
        ),
        "=" * 60,
    ]
    return "\n".join(lines)


def load_submission(submission_path):
    path = os.path.abspath(submission_path)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Submission file not found: {path}")

    spec = importlib.util.spec_from_file_location("cache_student", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["cache_student"] = module
    spec.loader.exec_module(module)

    return path, getattr(module, "submission_cache", None)


def print_validation_report(valid, failures, metrics):
    if not valid:
        print("Validation: FAIL")
        for message in failures:
            print(f"  - {message}")
        return

    print(
        "Validation: PASS — "
        f"{metrics['footprint']}-byte footprint, "
        f"{metrics['associativity']}-way, block_size={metrics['block_size']}"
    )


def print_performance_report(performance, baseline_cycles, earned, label):
    print(format_latency_banner(performance, baseline_cycles))
    print()
    print(f"Accesses: {performance['accesses']}")
    print(f"Hits: {performance['hits']}")
    print(f"Misses: {performance['misses']}")
    print(f"Hit Rate: {performance['hit_rate']:.2f}%")
    print(f"Total Cycles: {performance['total_cycles']}")
    print(f"AMAT: {performance['amat']:.2f} cycles/access")
    print()

    if earned:
        line = f"Score: {earned}/{MAX_SCORE} ({label})"
        next_tier = next_tier_target(earned)
        if next_tier:
            line += (
                f". Next: <= {next_tier['max_total_cycles']} cycles "
                f"for {next_tier['score']} pts"
            )
        print(line)
    else:
        print(
            f"Score: 0/{MAX_SCORE} — {performance['total_cycles']} cycles "
            f"does not beat main-memory baseline ({baseline_cycles})"
        )


def main():
    parser = argparse.ArgumentParser(description="Grade a cache simulator submission out of 100.")
    parser.add_argument("--submission", default="cache_student.py")
    args = parser.parse_args()

    print("CACHE SIMULATOR AUTOGRADER")
    print()

    try:
        submission_path, submission_cache = load_submission(args.submission)
    except (FileNotFoundError, ImportError, SyntaxError) as exc:
        print(f"Autograder failed: {exc}")
        return 1

    print(f"Submission: {os.path.basename(submission_path)}")
    print()

    valid, failures, metrics = inspect_submission_cache(submission_cache)
    print_validation_report(valid, failures, metrics)
    print()

    if not valid:
        print(f"FINAL SCORE: 0/{MAX_SCORE}")
        return 1

    if not os.path.isfile(TRACE_PATH):
        print(f"Autograder failed: trace not found: {TRACE_PATH}")
        return 1

    addresses = read_trace_addresses(TRACE_PATH)
    hits, misses = run_trace(submission_cache, addresses)
    performance = build_performance(hits, misses, metrics)
    baseline_cycles = performance["accesses"] * MAIN_MEMORY_LATENCY
    earned, label = compute_tier_score(performance["total_cycles"], baseline_cycles)

    print_performance_report(performance, baseline_cycles, earned, label)
    print()
    print(f"FINAL SCORE: {earned}/{MAX_SCORE}")

    return 0 if earned >= PASSING_SCORE else 1


if __name__ == "__main__":
    sys.exit(main())
