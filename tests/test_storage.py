from __future__ import annotations

import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from sentiment_platform.models import SentimentRecord
from sentiment_platform.storage import fetch_counts, initialize, insert_records


class StorageTests(unittest.TestCase):
    def test_insert_and_fetch_counts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            initialize(db_path)
            records = [
                SentimentRecord(
                    record_id="r-1",
                    source="twitter",
                    text="Great progress",
                    created_at=datetime(2024, 1, 1, 0, 0, 0),
                    sentiment="positive",
                    polarity=0.6,
                    raw_payload={"id": "r-1"},
                ),
                SentimentRecord(
                    record_id="r-2",
                    source="news",
                    text="Critical issue",
                    created_at=datetime(2024, 1, 1, 0, 1, 0),
                    sentiment="negative",
                    polarity=-0.6,
                    raw_payload={"id": "r-2"},
                ),
            ]
            inserted = insert_records(db_path, records)
            self.assertEqual(inserted, 2)

            counts = dict(fetch_counts(db_path))
            self.assertEqual(counts["negative"], 1)
            self.assertEqual(counts["positive"], 1)


if __name__ == "__main__":
    unittest.main()
