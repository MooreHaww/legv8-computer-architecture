"""Assemble every tests/*.s file and compare the result with answers/*.hex."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    subprocess.run([sys.executable, "assembler.py"], cwd=HERE, check=True)
    tests = sorted(f[:-2] for f in os.listdir(os.path.join(HERE, "tests")) if f.endswith(".s"))
    passed = 0
    for name in tests:
        with open(os.path.join(HERE, "outputs", name + ".hex")) as f:
            got = f.read().split()
        with open(os.path.join(HERE, "answers", name + ".hex")) as f:
            expected = f.read().split()
        if [x.upper() for x in got] == [x.upper() for x in expected]:
            passed += 1
        else:
            print(f"FAIL {name}: expected {expected}, got {got}")
    print(f"{passed}/{len(tests)} tests passed")
    sys.exit(0 if passed == len(tests) else 1)


if __name__ == "__main__":
    main()
