"""Tests for main.py: run it as the grader does (an output dir, twice) and
check the file it writes against the contest's limits."""

import os
import pathlib
import struct
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent


def run_main(out_dir):
    env = dict(os.environ, MAKEFUN_OUTPUT_DIR=str(out_dir))
    subprocess.run([sys.executable, str(ROOT / "main.py")], env=env, check=True,
                   cwd=tempfile.gettempdir(), timeout=60)
    return (pathlib.Path(out_dir) / "entry.png").read_bytes()


class MainTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.data = run_main(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_writes_a_png(self):
        self.assertEqual(self.data[:8], b"\x89PNG\r\n\x1a\n")

    def test_at_most_one_mebibyte(self):
        self.assertLessEqual(len(self.data), 1048576)

    def test_at_most_1024_square(self):
        width, height = struct.unpack(">II", self.data[16:24])
        self.assertLessEqual(width, 1024)
        self.assertLessEqual(height, 1024)

    def test_ends_with_iend_chunk(self):
        self.assertEqual(self.data[-12:], b"\x00\x00\x00\x00IEND\xaeB`\x82")

    def test_two_runs_write_identical_bytes(self):
        with tempfile.TemporaryDirectory() as second:
            self.assertEqual(run_main(second), self.data)


if __name__ == "__main__":
    unittest.main()
