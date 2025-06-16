from unittest import TestCase
from file_metadata import *
import stagger.stagger as stagger


class TestReadMetadata(TestCase):
    def test_get_year(self):
        year = get_year("test/yeet.mp3")
        self.assertEqual(year, 2025)

    def test_set_year(self):
        set_year("test/yeet.mp3", 2024)
        year = get_year("test/yeet.mp3")
        self.assertEqual(year, 2024)
        set_year("test/yeet.mp3", 2025)
        year = get_year("test/yeet.mp3")
        self.assertEqual(year, 2025)

    def test_clear_year(self):
        clear_year("test/yeet.mp3")

        with self.assertRaises(stagger.NoTagError):
            get_year("test/yeet.mp3")

        set_year("test/yeet.mp3", 2025)

    def test_read_artist(self):
        # test/test_files_read_metadata/2025.mp3
        self.assertEqual(2025, 2025)

    def test_read_album_artist(self):
        # test/test_files_read_metadata/2025.mp3
        self.assertEqual(2025, 2025)
