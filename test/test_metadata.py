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

    def test_get_album_title(self):
        set_album_title("test/yeet.mp3", "Test Album")
        album_title = get_album_title("test/yeet.mp3")
        self.assertEqual(album_title, "Test Album")

    def test_set_album_title(self):
        set_album_title("test/yeet.mp3", "Album One")
        album_title = get_album_title("test/yeet.mp3")
        self.assertEqual(album_title, "Album One")
        set_album_title("test/yeet.mp3", "Album Two")
        album_title = get_album_title("test/yeet.mp3")
        self.assertEqual(album_title, "Album Two")

    def test_clear_album_title(self):
        clear_album_title("test/yeet.mp3")
        with self.assertRaises(stagger.NoTagError):
            get_album_title("test/yeet.mp3")
        set_album_title("test/yeet.mp3", "Test Album")

    def test_get_artist(self):
        set_artist("test/yeet.mp3", "Test Artist")
        artist = get_artist("test/yeet.mp3")
        self.assertEqual(artist, "Test Artist")

    def test_set_artist(self):
        set_artist("test/yeet.mp3", "Artist One")
        artist = get_artist("test/yeet.mp3")
        self.assertEqual(artist, "Artist One")
        set_artist("test/yeet.mp3", "Artist Two")
        artist = get_artist("test/yeet.mp3")
        self.assertEqual(artist, "Artist Two")

    def test_clear_artist(self):
        clear_artist("test/yeet.mp3")
        with self.assertRaises(stagger.NoTagError):
            get_artist("test/yeet.mp3")
        set_artist("test/yeet.mp3", "Test Artist")

    def test_get_song_title(self):
        set_song_title("test/yeet.mp3", "Test Song")
        song_title = get_song_title("test/yeet.mp3")
        self.assertEqual(song_title, "Test Song")

    def test_set_song_title(self):
        set_song_title("test/yeet.mp3", "Song One")
        song_title = get_song_title("test/yeet.mp3")
        self.assertEqual(song_title, "Song One")
        set_song_title("test/yeet.mp3", "Song Two")
        song_title = get_song_title("test/yeet.mp3")
        self.assertEqual(song_title, "Song Two")

    def test_clear_song_title(self):
        clear_song_title("test/yeet.mp3")
        with self.assertRaises(stagger.NoTagError):
            get_song_title("test/yeet.mp3")
        set_song_title("test/yeet.mp3", "Test Song")
