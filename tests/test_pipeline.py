from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sentiment_platform.config import Config
from sentiment_platform.pipeline import Pipeline


class PipelineTests(unittest.TestCase):
    def test_pipeline_run(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(__file__).resolve().parents[1] / "data"
            config = Config(
                database_path=Path(tmpdir) / "sentiment.db",
                twitter_source_path=data_dir / "sample_tweets.jsonl",
                news_source_path=data_dir / "sample_news.jsonl",
                output_dir=Path(tmpdir) / "output",
                max_records_per_source=5,
            )
            pipeline = Pipeline(config)
            summary = pipeline.run()
            self.assertEqual(summary["inserted"], 10)
            self.assertTrue(summary["counts"])


if __name__ == "__main__":
    unittest.main()
