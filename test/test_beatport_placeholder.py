import os
import unittest

from beatport_placeholder import is_beatport_placeholder

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestBeatportPlaceholder(unittest.TestCase):
    def test_placeholder_logo_detected(self):
        with open(os.path.join(TEST_DIR, "beatport_placeholder_1500.jpg"), "rb") as f:
            self.assertTrue(is_beatport_placeholder(f.read()))

    def test_real_cover_not_detected(self):
        with open(os.path.join(TEST_DIR, "test_art", "skrillex_push.jpg"), "rb") as f:
            self.assertFalse(is_beatport_placeholder(f.read()))

    def test_garbage_bytes_not_detected(self):
        self.assertFalse(is_beatport_placeholder(b"not an image"))
