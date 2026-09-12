import unittest

from diagnostics.checks import check_disk_space, check_environment


class TestDiagnostics(unittest.TestCase):

    def test_disk_space(self):
        result = check_disk_space()

        self.assertIn("total_gb", result)
        self.assertIn("used_gb", result)
        self.assertIn("free_gb", result)

        self.assertGreater(result["total_gb"], 0)
        self.assertGreaterEqual(result["used_gb"], 0)
        self.assertGreaterEqual(result["free_gb"], 0)

    def test_environment(self):
        result = check_environment()

        self.assertIn("PATH", result)
        self.assertIn("HOME", result)

    def test_missing_dependency(self):
        import shutil

        result = shutil.which("command_that_does_not_exist")

        self.assertIsNone(result)

    def test_malformed_configuration_path(self):
        import os

        config_path = "does_not_exist/config.json"

        self.assertFalse(os.path.exists(config_path))


if __name__ == "__main__":
    unittest.main()