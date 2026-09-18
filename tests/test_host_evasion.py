import unittest

from core.host_evasion import generate_host_source
from core.network_evasion import CANARY


class HostSourceTests(unittest.TestCase):
    def test_source_is_transparent_and_contains_no_loader_primitives(self):
        source = generate_host_source()
        self.assertIn(CANARY, source)
        self.assertIn("puts(", source)
        self.assertNotIn("VirtualAlloc", source)
        self.assertNotIn("CreateThread", source)
        self.assertNotIn("shellcode", source.lower())


if __name__ == "__main__":
    unittest.main()