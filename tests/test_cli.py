from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout

from sentiment_platform.cli import main


class CliTests(unittest.TestCase):
    def test_cli_analyze(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = main(["analyze", "Great progress and good news"])
        self.assertEqual(exit_code, 0)
        self.assertIn("positive", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
