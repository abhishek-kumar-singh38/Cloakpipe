import unittest

from core.network_evasion import CANARY, generate_network_corpus


class NetworkCorpusTests(unittest.TestCase):
    def test_corpus_is_deterministic_and_uses_fixed_canary(self):
        corpus = generate_network_corpus()
        self.assertEqual(corpus["canary"], CANARY)
        self.assertGreaterEqual(len(corpus["cases"]), 7)
        self.assertTrue(all(case["expected"] == CANARY for case in corpus["cases"]))

    def test_label_is_metadata_only(self):
        corpus = generate_network_corpus("lab-a")
        self.assertEqual(corpus["label"], "lab-a")
        self.assertEqual(corpus["canary"], CANARY)


if __name__ == "__main__":
    unittest.main()