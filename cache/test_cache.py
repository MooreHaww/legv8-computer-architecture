import io
import os
import unittest
from contextlib import redirect_stdout

import cache_student
import trace_reader
from cache_student import Cache
from config_checks import inspect_submission_cache
from performance_thresholds import MAIN_MEMORY_LATENCY


def require_submission_cache():
    cache = getattr(cache_student, "submission_cache", None)
    if cache is None:
        raise unittest.SkipTest(
            "submission_cache is not defined in cache_student.py yet"
        )
    return cache


class TestCacheLogic(unittest.TestCase):
    def test_constructor_calculations(self):
        cache = Cache(capacity=8192, block_size=64, associativity=4)

        expected_sets = 32
        expected_offset_bits = 6
        expected_index_bits = 5

        self.assertEqual(cache.sets, expected_sets)
        self.assertEqual(cache.offset_bits, expected_offset_bits)
        self.assertEqual(cache.index_bits, expected_index_bits)


class TestSubmissionCache(unittest.TestCase):
    def test_submission_cache_is_valid(self):
        submission_cache = require_submission_cache()
        valid, failures, metrics = inspect_submission_cache(submission_cache)
        self.assertTrue(
            valid,
            "Invalid submission_cache:\n- " + "\n- ".join(failures),
        )
        self.assertEqual(metrics["footprint"], 4096)


class TestTraceExecution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logic_suite = unittest.TestLoader().loadTestsFromTestCase(TestCacheLogic)
        submission_suite = unittest.TestLoader().loadTestsFromTestCase(TestSubmissionCache)
        combined = unittest.TestSuite([logic_suite, submission_suite])
        result = unittest.TextTestRunner(stream=io.StringIO()).run(combined)
        if not result.wasSuccessful():
            raise unittest.SkipTest("Constructor or submission_cache validation did not pass")

    def test_run_simulation_on_benchmark_trace(self):
        trace_path = os.path.join(os.path.dirname(__file__), "traces", "benchmark.txt")
        self.assertTrue(os.path.isfile(trace_path))

        submission_cache = require_submission_cache()
        valid, _, metrics = inspect_submission_cache(submission_cache)
        self.assertTrue(valid)

        hits = 0
        total = 0

        with open(trace_path, "r") as trace_file:
            for line in trace_file:
                line = line.strip()
                if not line:
                    continue
                address = int(line, 16)
                total += 1
                if submission_cache.access(address):
                    hits += 1

        misses = total - hits
        total_cycles = (hits * metrics["hit_cost"]) + (misses * metrics["miss_cost"])
        baseline_cycles = total * MAIN_MEMORY_LATENCY

        self.assertLess(
            total_cycles,
            baseline_cycles,
            f"Total cycles {total_cycles} must beat main-memory baseline {baseline_cycles}",
        )

        output = io.StringIO()
        with redirect_stdout(output):
            trace_reader.run_simulation(trace_path)

        printed = output.getvalue()
        self.assertIn("HIT LATENCY:", printed)
        self.assertIn("Accesses:", printed)
        self.assertIn("Hits:", printed)
        self.assertIn("Misses:", printed)
        self.assertIn("Hit Rate:", printed)
        self.assertIn("Total Cycles:", printed)
        self.assertIn("AMAT:", printed)


if __name__ == "__main__":
    unittest.main()
