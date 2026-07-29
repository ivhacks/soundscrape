import os
import shutil
import tempfile
from unittest import TestCase

import pytest

from file_metadata import get_album_title, get_artist, get_song_title
from parse_and_clean import clean_title, parse_artists, parse_features
from soundscrape import process_dir


DIR = "test/noaudio/Porter_Robinson_Worlds"

TRACKS = [
    ("Porter Robinson - 01. Divinity.flac", "Divinity"),
    ("Porter Robinson - 02. Sad Machine.flac", "Sad Machine"),
    ("Porter Robinson - 03. Years Of War.flac", "Years Of War"),
    ("Porter Robinson - 04. Flicker.flac", "Flicker"),
    ("Porter Robinson - 05. Fresh Static Snow.flac", "Fresh Static Snow"),
    ("Porter Robinson - 06. Polygon Dust.flac", "Polygon Dust"),
    ("Porter Robinson - 07. Hear The Bells.flac", "Hear The Bells"),
    ("Porter Robinson - 08. Natural Light.flac", "Natural Light"),
    ("Porter Robinson - 09. Lionhearted.flac", "Lionhearted"),
    ("Porter Robinson - 10. Sea Of Voices.flac", "Sea Of Voices"),
    ("Porter Robinson - 11. Fellow Feeling.flac", "Fellow Feeling"),
    ("Porter Robinson - 12. Goodbye To A World.flac", "Goodbye To A World"),
]


@pytest.mark.xdist_group(name="parse_clean")
class PorterWorldsParseTests(TestCase):
    def _check_tags(self, filename: str, expected_title: str):
        path = f"{DIR}/{filename}"
        artist = get_artist(path)
        title = get_song_title(path)
        album = get_album_title(path)

        self.assertEqual(parse_artists(artist), ["Porter Robinson"])
        self.assertEqual(clean_title(title), expected_title)
        self.assertEqual(parse_features(title), [])
        self.assertEqual(album, "Worlds")

    def test_divinity(self):
        self._check_tags("Porter Robinson - 01. Divinity.flac", "Divinity")

    def test_sad_machine(self):
        self._check_tags("Porter Robinson - 02. Sad Machine.flac", "Sad Machine")

    def test_years_of_war(self):
        self._check_tags("Porter Robinson - 03. Years Of War.flac", "Years Of War")

    def test_flicker(self):
        self._check_tags("Porter Robinson - 04. Flicker.flac", "Flicker")

    def test_fresh_static_snow(self):
        self._check_tags(
            "Porter Robinson - 05. Fresh Static Snow.flac", "Fresh Static Snow"
        )

    def test_polygon_dust(self):
        self._check_tags("Porter Robinson - 06. Polygon Dust.flac", "Polygon Dust")

    def test_hear_the_bells(self):
        self._check_tags("Porter Robinson - 07. Hear The Bells.flac", "Hear The Bells")

    def test_natural_light(self):
        self._check_tags("Porter Robinson - 08. Natural Light.flac", "Natural Light")

    def test_lionhearted(self):
        self._check_tags("Porter Robinson - 09. Lionhearted.flac", "Lionhearted")

    def test_sea_of_voices(self):
        self._check_tags("Porter Robinson - 10. Sea Of Voices.flac", "Sea Of Voices")

    def test_fellow_feeling(self):
        self._check_tags("Porter Robinson - 11. Fellow Feeling.flac", "Fellow Feeling")

    def test_goodbye_to_a_world(self):
        self._check_tags(
            "Porter Robinson - 12. Goodbye To A World.flac", "Goodbye To A World"
        )


@pytest.mark.xdist_group(name="parse_clean")
class PorterWorldsFilenameTests(TestCase):
    work: str

    @classmethod
    def setUpClass(cls):
        cls.work = tempfile.mkdtemp()
        for filename, _ in TRACKS:
            shutil.copy2(os.path.join(DIR, filename), os.path.join(cls.work, filename))
        process_dir(
            cls.work,
            no_art_select=True,
            embed_lyrics=False,
            resolve_artists_with_ai=False,
            skip_web=True,
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.work)

    def _check_renamed(self, expected_title: str):
        expected_name = f"{expected_title}.flac"
        path = os.path.join(self.work, expected_name)
        self.assertTrue(os.path.exists(path), f"missing {expected_name}")
        self.assertEqual(get_song_title(path), expected_title)
        self.assertEqual(get_artist(path), "Porter Robinson")
        self.assertEqual(get_album_title(path), "Worlds")

    def test_divinity(self):
        self._check_renamed("Divinity")

    def test_sad_machine(self):
        self._check_renamed("Sad Machine")

    def test_years_of_war(self):
        self._check_renamed("Years Of War")

    def test_flicker(self):
        self._check_renamed("Flicker")

    def test_fresh_static_snow(self):
        self._check_renamed("Fresh Static Snow")

    def test_polygon_dust(self):
        self._check_renamed("Polygon Dust")

    def test_hear_the_bells(self):
        self._check_renamed("Hear The Bells")

    def test_natural_light(self):
        self._check_renamed("Natural Light")

    def test_lionhearted(self):
        self._check_renamed("Lionhearted")

    def test_sea_of_voices(self):
        self._check_renamed("Sea Of Voices")

    def test_fellow_feeling(self):
        self._check_renamed("Fellow Feeling")

    def test_goodbye_to_a_world(self):
        self._check_renamed("Goodbye To A World")

    def test_no_numbered_filenames_left(self):
        names = os.listdir(self.work)
        for name in names:
            self.assertNotIn("Porter Robinson -", name)
            self.assertNotRegex(name, r"^\d+\.")
