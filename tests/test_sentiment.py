from __future__ import annotations

import unittest

from sentiment_platform.sentiment import SentimentAnalyzer


class SentimentTests(unittest.TestCase):
    def setUp(self):
        self.analyzer = SentimentAnalyzer()

    def test_positive_sentiment(self):
        result = self.analyzer.analyze("Amazing progress and great results")
        self.assertEqual(result.label, "positive")
        self.assertGreater(result.polarity, 0)

    def test_negative_sentiment(self):
        result = self.analyzer.analyze("Critical issue and bad delay")
        self.assertEqual(result.label, "negative")
        self.assertLess(result.polarity, 0)

    def test_neutral_sentiment(self):
        result = self.analyzer.analyze("Monitoring the dashboard")
        self.assertEqual(result.label, "neutral")

    def test_negator_flips_score(self):
        result = self.analyzer.analyze("not good")
        self.assertEqual(result.label, "negative")


if __name__ == "__main__":
    unittest.main()
