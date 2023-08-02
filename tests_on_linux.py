import subprocess
from pathlib import Path
from typing import Iterable
from dataclasses import dataclass


BASE_DIR = Path(__file__).parent
ENTRY_POINT = BASE_DIR / "tetris.sh"



@dataclass
class TestCase:
    name: str
    sample_input: bytes
    sample_output: Iterable[int]


def run_test(test_case: TestCase):
    p = subprocess.run(
        ['/bin/bash', ENTRY_POINT, test_case.sample_input],
        input=test_case.sample_input,
        capture_output=True, shell=True
    )
    output = int(p.stdout.decode().strip())  # Convert stdout to an integer
    assert output == test_case.sample_output, f"The test with name `{test_case.name}` failed."

# Execute this script with `python3 starter_tests.py`
if __name__ == "__main__":
    test_cases = [
        TestCase("simple test", b'Q0', 2),
        TestCase("Many blocks test", ",".join(["Q0"] * 50).encode("utf-8"), 100),
    ]
    for test_case in test_cases:
        run_test(test_case)
