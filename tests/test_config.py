from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from sentiment_platform.config import load_config


class ConfigTests(unittest.TestCase):
    def test_load_config_defaults(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            current = os.getcwd()
            os.chdir(tmpdir)
            try:
                config = load_config(env={})
                self.assertTrue(config.database_path.as_posix().endswith("var/sentiment.db"))
                self.assertTrue(
                    config.twitter_source_path.as_posix().endswith("data/sample_tweets.jsonl")
                )
            finally:
                os.chdir(current)

    def test_load_config_dotenv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dotenv = Path(tmpdir) / ".env"
            dotenv.write_text(
                "DATABASE_PATH=./custom.db\n"
                "TWITTER_SOURCE_PATH=./tweets.jsonl\n"
                "NEWS_SOURCE_PATH=./news.jsonl\n"
                "OUTPUT_DIR=./out\n"
                "MAX_RECORDS_PER_SOURCE=5\n",
                encoding="utf-8",
            )

            config = load_config(env={}, dotenv_path=dotenv)
            self.assertEqual(config.database_path, Path("./custom.db"))
            self.assertEqual(config.twitter_source_path, Path("./tweets.jsonl"))
            self.assertEqual(config.news_source_path, Path("./news.jsonl"))
            self.assertEqual(config.output_dir, Path("./out"))
            self.assertEqual(config.max_records_per_source, 5)


if __name__ == "__main__":
    unittest.main()
