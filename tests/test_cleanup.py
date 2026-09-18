import tempfile
import unittest
from pathlib import Path

from core.cleanup import clean_output_directory


class CleanupTests(unittest.TestCase):
    def test_only_known_generated_files_are_removed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "output"
            output.mkdir()
            (output / "network-corpus.json").write_text("{}")
            (output / "notes.txt").write_text("preserve")
            self.assertEqual(clean_output_directory(output), 1)
            self.assertFalse((output / "network-corpus.json").exists())
            self.assertTrue((output / "notes.txt").exists())


if __name__ == "__main__":
    unittest.main()