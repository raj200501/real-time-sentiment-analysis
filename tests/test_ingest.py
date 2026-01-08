from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sentiment_platform.ingest import IngestionError, load_records


class IngestTests(unittest.TestCase):
    def test_load_records_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            payload = Path(tmpdir) / "tweets.jsonl"
            payload.write_text(
                """{"id": "t-1", "text": "Great news", "created_at": "2024-01-01T00:00:00Z"}\n""",
                encoding="utf-8",
            )
            records = load_records(payload, "twitter", "text", "created_at")
            self.assertEqual(records[0].record_id, "t-1")
            self.assertEqual(records[0].text, "Great news")

    def test_load_records_missing_field(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            payload = Path(tmpdir) / "tweets.jsonl"
            payload.write_text(
                """{"id": "t-1", "created_at": "2024-01-01T00:00:00Z"}\n""",
                encoding="utf-8",
            )
            with self.assertRaises(IngestionError):
                load_records(payload, "twitter", "text", "created_at")


if __name__ == "__main__":
    unittest.main()
