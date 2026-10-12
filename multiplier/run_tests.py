"""Run the shift-add multiplier on every test case and compare with expected_outputs/."""
import os
import sys

from codec import MASK_64, decode_test_case_file, encode_u64
from multiplier import simulate_multiplier

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    test_dir = os.path.join(HERE, "test_cases")
    expected_dir = os.path.join(HERE, "expected_outputs")
    cases = sorted(f for f in os.listdir(test_dir) if f.endswith(".txt"))
    passed = 0
    for filename in cases:
        with open(os.path.join(test_dir, filename), encoding="utf-8") as f:
            a, b = decode_test_case_file(f.read())
        got = encode_u64(simulate_multiplier(a, b) & MASK_64)
        exp_path = os.path.join(expected_dir, os.path.splitext(filename)[0] + ".out")
        with open(exp_path, encoding="utf-8") as f:
            expected = f.read().strip()
        if got == expected:
            passed += 1
        else:
            print(f"FAIL {filename}: expected {expected}, got {got}")
    print(f"{passed}/{len(cases)} test cases passed")
    sys.exit(0 if passed == len(cases) else 1)


if __name__ == "__main__":
    main()
