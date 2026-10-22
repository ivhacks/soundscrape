import os
import shutil
import tempfile
from unittest import TestCase

from artwork import extract_artwork
from file_metadata import NoTagError
from tags import read_tags
from mutagen.flac import FLAC


class TestTags(TestCase):
    def test_yeet_mp3(self):
        expected = (
            "artist: Artist Two\n"
            "album artist: Album Artist Two\n"
            "title: Song Two\n"
            "album: Album Two\n"
            "year: 2025\n"
            "lyrics:\n"
            "Lyrics Two"
        )
        self.assertEqual(read_tags("test/yeet.mp3"), expected)

    def test_nolimit_flac_no_lyrics(self):
        expected = (
            "artist: Knock2, Lauren LaRue\n"
            "album artist: Knock2\n"
            "title: nolimit Explicit\n"
            "album: nolimit\n"
            "year: 2025\n"
            "lyrics:\n"
            "(missing)"
        )
        self.assertEqual(read_tags("test/nolimit.flac"), expected)

    def test_nothing_mp3_all_missing(self):
        expected = (
            "artist: (missing)\n"
            "album artist: (missing)\n"
            "title: (missing)\n"
            "album: (missing)\n"
            "year: (missing)\n"
            "lyrics:\n"
            "(missing)"
        )
        self.assertEqual(read_tags("test/nothing.mp3"), expected)


    def test_nolimit_flac_unsyncedlyrics(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            song = os.path.join(temp_dir, "nolimit.flac")
            shutil.copy("test/nolimit.flac", song)
            audiofile = FLAC(song)
            audiofile["UNSYNCEDLYRICS"] = "Unsynced Lyrics"
            audiofile.save()
            expected = (
                "artist: Knock2, Lauren LaRue\n"
                "album artist: Knock2\n"
                "title: nolimit Explicit\n"
                "album: nolimit\n"
                "year: 2025\n"
                "lyrics:\n"
                "Unsynced Lyrics"
            )
            self.assertEqual(read_tags(song), expected)


class TestArtwork(TestCase):
    def test_yeet_mp3(self):
        result = extract_artwork("test/yeet.mp3", "/tmp/test_yeet_mp3_cover")
        self.assertEqual(result, "/tmp/test_yeet_mp3_cover.jpg 800x800")
        self.assertTrue(os.path.getsize("/tmp/test_yeet_mp3_cover.jpg") > 0)
        os.remove("/tmp/test_yeet_mp3_cover.jpg")

    def test_nolimit_flac(self):
        result = extract_artwork("test/nolimit.flac", "/tmp/test_nolimit_flac_cover")
        self.assertEqual(result, "/tmp/test_nolimit_flac_cover.jpg 800x800")
        self.assertTrue(os.path.getsize("/tmp/test_nolimit_flac_cover.jpg") > 0)
        os.remove("/tmp/test_nolimit_flac_cover.jpg")

    def test_nothing_mp3_no_art(self):
        with self.assertRaises(NoTagError):
            extract_artwork("test/nothing.mp3", "/tmp/test_nothing_mp3_cover")
