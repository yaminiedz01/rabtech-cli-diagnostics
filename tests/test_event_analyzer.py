import unittest

from diagnostics.event_analyzer import analyze_events


class TestEventAnalyzer(unittest.TestCase):

    def test_analyze_events(self):
        events = [
            {"level": "INFO", "latency_ms": 100, "status_code": 200},
            {"level": "WARN", "latency_ms": 500, "status_code": 200},
            {"level": "ERROR", "latency_ms": 1000, "status_code": 503}
        ]

        result = analyze_events(events)

        self.assertEqual(result["total_events"], 3)
        self.assertEqual(result["error_count"], 1)
        self.assertEqual(result["warning_count"], 1)
        self.assertEqual(result["status_5xx_count"], 1)
        self.assertEqual(result["average_latency_ms"], 533.33)


if __name__ == "__main__":
    unittest.main()