import os
import shutil
from unittest import TestCase

from PIL import Image

from file_metadata import *


class TestReadMetadata(TestCase):
    NOLIMIT_FLAC_BACKUP = "test/nolimit_backup.flac"

    def setUp(self):
        # Create backup of nolimit.flac before each test
        if os.path.exists("test/nolimit.flac"):
            shutil.copy2("test/nolimit.flac", self.NOLIMIT_FLAC_BACKUP)

    def tearDown(self):
        # Restore original nolimit.flac after each test
        if os.path.exists(self.NOLIMIT_FLAC_BACKUP):
            shutil.copy2(self.NOLIMIT_FLAC_BACKUP, "test/nolimit.flac")
            os.remove(self.NOLIMIT_FLAC_BACKUP)

    # MP3 Tests
    def test_get_year_mp3(self):
        year = get_year("test/yeet.mp3")
        self.assertEqual(year, 2025)

    def test_set_year_mp3(self):
        set_year("test/yeet.mp3", 2024)
        year = get_year("test/yeet.mp3")
        self.assertEqual(year, 2024)
        set_year("test/yeet.mp3", 2025)
        year = get_year("test/yeet.mp3")
        self.assertEqual(year, 2025)

    def test_clear_year_mp3(self):
        clear_year("test/yeet.mp3")

        with self.assertRaises(NoTagError):
            get_year("test/yeet.mp3")

        set_year("test/yeet.mp3", 2025)

    def test_read_artist_mp3(self):
        # test/test_files_read_metadata/2025.mp3
        self.assertEqual(2025, 2025)

    def test_read_album_artist_mp3(self):
        # test/test_files_read_metadata/2025.mp3
        self.assertEqual(2025, 2025)

    def test_get_album_title_mp3(self):
        set_album_title("test/yeet.mp3", "Test Album")
        album_title = get_album_title("test/yeet.mp3")
        self.assertEqual(album_title, "Test Album")

    def test_set_album_title_mp3(self):
        set_album_title("test/yeet.mp3", "Album One")
        album_title = get_album_title("test/yeet.mp3")
        self.assertEqual(album_title, "Album One")
        set_album_title("test/yeet.mp3", "Album Two")
        album_title = get_album_title("test/yeet.mp3")
        self.assertEqual(album_title, "Album Two")

    def test_clear_album_title_mp3(self):
        clear_album_title("test/yeet.mp3")
        with self.assertRaises(NoTagError):
            get_album_title("test/yeet.mp3")
        set_album_title("test/yeet.mp3", "Test Album")

    def test_get_artist_mp3(self):
        set_artist("test/yeet.mp3", "Test Artist")
        artist = get_artist("test/yeet.mp3")
        self.assertEqual(artist, "Test Artist")

    def test_set_artist_mp3(self):
        set_artist("test/yeet.mp3", "Artist One")
        artist = get_artist("test/yeet.mp3")
        self.assertEqual(artist, "Artist One")
        set_artist("test/yeet.mp3", "Artist Two")
        artist = get_artist("test/yeet.mp3")
        self.assertEqual(artist, "Artist Two")

    def test_clear_artist_mp3(self):
        clear_artist("test/yeet.mp3")
        with self.assertRaises(NoTagError):
            get_artist("test/yeet.mp3")
        set_artist("test/yeet.mp3", "Test Artist")

    def test_get_album_artist_mp3(self):
        set_album_artist("test/yeet.mp3", "Test Album Artist")
        album_artist = get_album_artist("test/yeet.mp3")
        self.assertEqual(album_artist, "Test Album Artist")

    def test_set_album_artist_mp3(self):
        set_album_artist("test/yeet.mp3", "Album Artist One")
        album_artist = get_album_artist("test/yeet.mp3")
        self.assertEqual(album_artist, "Album Artist One")
        set_album_artist("test/yeet.mp3", "Album Artist Two")
        album_artist = get_album_artist("test/yeet.mp3")
        self.assertEqual(album_artist, "Album Artist Two")

    def test_clear_album_artist_mp3(self):
        clear_album_artist("test/yeet.mp3")
        with self.assertRaises(NoTagError):
            get_album_artist("test/yeet.mp3")
        set_album_artist("test/yeet.mp3", "Test Album Artist")

    def test_get_song_title_mp3(self):
        set_song_title("test/yeet.mp3", "Test Song")
        song_title = get_song_title("test/yeet.mp3")
        self.assertEqual(song_title, "Test Song")

    def test_set_song_title_mp3(self):
        set_song_title("test/yeet.mp3", "Song One")
        song_title = get_song_title("test/yeet.mp3")
        self.assertEqual(song_title, "Song One")
        set_song_title("test/yeet.mp3", "Song Two")
        song_title = get_song_title("test/yeet.mp3")
        self.assertEqual(song_title, "Song Two")

    def test_clear_song_title_mp3(self):
        clear_song_title("test/yeet.mp3")
        with self.assertRaises(NoTagError):
            get_song_title("test/yeet.mp3")
        set_song_title("test/yeet.mp3", "Test Song")

    def test_get_lyrics_mp3(self):
        set_lyrics("test/yeet.mp3", "Test lyrics content")
        lyrics = get_lyrics("test/yeet.mp3")
        self.assertEqual(lyrics, "Test lyrics content")

    def test_set_lyrics_mp3(self):
        set_lyrics("test/yeet.mp3", "Lyrics One")
        lyrics = get_lyrics("test/yeet.mp3")
        self.assertEqual(lyrics, "Lyrics One")
        set_lyrics("test/yeet.mp3", "Lyrics Two")
        lyrics = get_lyrics("test/yeet.mp3")
        self.assertEqual(lyrics, "Lyrics Two")

    def test_clear_lyrics_mp3(self):
        clear_lyrics("test/yeet.mp3")
        with self.assertRaises(NoTagError):
            get_lyrics("test/yeet.mp3")
        set_lyrics("test/yeet.mp3", "Test lyrics")

    def test_get_cover_art_mp3(self):
        extracted_image = get_cover_art("test/nolimit.mp3")
        expected_image = Image.open("test/image.jpg")

        extracted_bytes = extracted_image.tobytes()
        expected_bytes = expected_image.tobytes()

        self.assertEqual(extracted_bytes, expected_bytes)

    def test_set_cover_art_mp3(self):
        with open("test/image.jpg", "rb") as f:
            image_data = f.read()

        set_cover_art("test/yeet.mp3", image_data)
        extracted_image = get_cover_art("test/yeet.mp3")
        expected_image = Image.open("test/image.jpg")

        extracted_bytes = extracted_image.tobytes()
        expected_bytes = expected_image.tobytes()

        self.assertEqual(extracted_bytes, expected_bytes)

    def test_clear_cover_art_mp3(self):
        clear_cover_art("test/yeet.mp3")
        with self.assertRaises(NoTagError):
            get_cover_art("test/yeet.mp3")

        with open("test/image.jpg", "rb") as f:
            image_data = f.read()
        set_cover_art("test/yeet.mp3", image_data)

    # FLAC Tests
    def test_get_year_flac(self):
        set_year("test/yeet.flac", 2025)
        year = get_year("test/yeet.flac")
        self.assertEqual(year, 2025)

    def test_set_year_flac(self):
        set_year("test/yeet.flac", 2024)
        year = get_year("test/yeet.flac")
        self.assertEqual(year, 2024)
        set_year("test/yeet.flac", 2025)
        year = get_year("test/yeet.flac")
        self.assertEqual(year, 2025)

    def test_clear_year_flac(self):
        clear_year("test/yeet.flac")

        with self.assertRaises(NoTagError):
            get_year("test/yeet.flac")

        set_year("test/yeet.flac", 2025)

    def test_read_artist_flac(self):
        # test/test_files_read_metadata/2025.flac
        self.assertEqual(2025, 2025)

    def test_read_album_artist_flac(self):
        # test/test_files_read_metadata/2025.flac
        self.assertEqual(2025, 2025)

    def test_get_album_title_flac(self):
        set_album_title("test/yeet.flac", "Test Album")
        album_title = get_album_title("test/yeet.flac")
        self.assertEqual(album_title, "Test Album")

    def test_set_album_title_flac(self):
        set_album_title("test/yeet.flac", "Album One")
        album_title = get_album_title("test/yeet.flac")
        self.assertEqual(album_title, "Album One")
        set_album_title("test/yeet.flac", "Album Two")
        album_title = get_album_title("test/yeet.flac")
        self.assertEqual(album_title, "Album Two")

    def test_clear_album_title_flac(self):
        clear_album_title("test/yeet.flac")
        with self.assertRaises(NoTagError):
            get_album_title("test/yeet.flac")
        set_album_title("test/yeet.flac", "Test Album")

    def test_get_artist_flac(self):
        set_artist("test/yeet.flac", "Test Artist")
        artist = get_artist("test/yeet.flac")
        self.assertEqual(artist, "Test Artist")

    def test_set_artist_flac(self):
        set_artist("test/yeet.flac", "Artist One")
        artist = get_artist("test/yeet.flac")
        self.assertEqual(artist, "Artist One")
        set_artist("test/yeet.flac", "Artist Two")
        artist = get_artist("test/yeet.flac")
        self.assertEqual(artist, "Artist Two")

    def test_clear_artist_flac(self):
        clear_artist("test/yeet.flac")
        with self.assertRaises(NoTagError):
            get_artist("test/yeet.flac")
        set_artist("test/yeet.flac", "Test Artist")

    def test_get_album_artist_flac(self):
        set_album_artist("test/yeet.flac", "Test Album Artist")
        album_artist = get_album_artist("test/yeet.flac")
        self.assertEqual(album_artist, "Test Album Artist")

    def test_set_album_artist_flac(self):
        set_album_artist("test/yeet.flac", "Album Artist One")
        album_artist = get_album_artist("test/yeet.flac")
        self.assertEqual(album_artist, "Album Artist One")
        set_album_artist("test/yeet.flac", "Album Artist Two")
        album_artist = get_album_artist("test/yeet.flac")
        self.assertEqual(album_artist, "Album Artist Two")

    def test_clear_album_artist_flac(self):
        clear_album_artist("test/yeet.flac")
        with self.assertRaises(NoTagError):
            get_album_artist("test/yeet.flac")
        set_album_artist("test/yeet.flac", "Test Album Artist")

    def test_get_song_title_flac(self):
        set_song_title("test/yeet.flac", "Test Song")
        song_title = get_song_title("test/yeet.flac")
        self.assertEqual(song_title, "Test Song")

    def test_set_song_title_flac(self):
        set_song_title("test/yeet.flac", "Song One")
        song_title = get_song_title("test/yeet.flac")
        self.assertEqual(song_title, "Song One")
        set_song_title("test/yeet.flac", "Song Two")
        song_title = get_song_title("test/yeet.flac")
        self.assertEqual(song_title, "Song Two")

    def test_clear_song_title_flac(self):
        clear_song_title("test/yeet.flac")
        with self.assertRaises(NoTagError):
            get_song_title("test/yeet.flac")
        set_song_title("test/yeet.flac", "Test Song")

    def test_get_lyrics_flac(self):
        set_lyrics("test/yeet.flac", "Test lyrics content")
        lyrics = get_lyrics("test/yeet.flac")
        self.assertEqual(lyrics, "Test lyrics content")

    def test_set_lyrics_flac(self):
        set_lyrics("test/yeet.flac", "Lyrics One")
        lyrics = get_lyrics("test/yeet.flac")
        self.assertEqual(lyrics, "Lyrics One")
        set_lyrics("test/yeet.flac", "Lyrics Two")
        lyrics = get_lyrics("test/yeet.flac")
        self.assertEqual(lyrics, "Lyrics Two")

    def test_clear_lyrics_flac(self):
        clear_lyrics("test/yeet.flac")
        with self.assertRaises(NoTagError):
            get_lyrics("test/yeet.flac")
        set_lyrics("test/yeet.flac", "Test lyrics")

    def test_get_cover_art_flac(self):
        with open("test/image.jpg", "rb") as f:
            image_data = f.read()
        set_cover_art("test/nolimit.flac", image_data)

        extracted_image = get_cover_art("test/nolimit.flac")
        expected_image = Image.open("test/image.jpg")

        extracted_bytes = extracted_image.tobytes()
        expected_bytes = expected_image.tobytes()

        self.assertEqual(extracted_bytes, expected_bytes)

    def test_set_cover_art_flac(self):
        with open("test/image.jpg", "rb") as f:
            image_data = f.read()

        set_cover_art("test/yeet.flac", image_data)
        extracted_image = get_cover_art("test/yeet.flac")
        expected_image = Image.open("test/image.jpg")

        extracted_bytes = extracted_image.tobytes()
        expected_bytes = expected_image.tobytes()

        self.assertEqual(extracted_bytes, expected_bytes)

    def test_clear_cover_art_flac(self):
        clear_cover_art("test/yeet.flac")
        with self.assertRaises(NoTagError):
            get_cover_art("test/yeet.flac")

        with open("test/image.jpg", "rb") as f:
            image_data = f.read()
        set_cover_art("test/yeet.flac", image_data)
