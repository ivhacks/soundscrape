import os
import shutil
import tempfile
from unittest import TestCase

import pytest

from file_metadata import (
    NoTagError,
    get_album_artist,
    get_artist,
    get_cover_art,
    get_song_title,
)
from img_diff import image_difference
from soundscrape import main


def _find_output_track(out_dir: str, needle: str) -> str:
    matches = [f for f in os.listdir(out_dir) if needle.lower() in f.lower() and f.lower().endswith((".mp3", ".flac"))]
    if len(matches) != 1:
        raise AssertionError(f"expected exactly 1 file matching {needle!r}, got {matches!r}")
    return os.path.join(out_dir, matches[0])


class IntegrationTests(TestCase):
    def setUp(self):
        self.out_dir = tempfile.mkdtemp(prefix="ss_int_")

    def tearDown(self):
        shutil.rmtree(self.out_dir, ignore_errors=True)

    @pytest.mark.timeout(600)
    def test_knock2_nolimit_purchased(self):
        main(
            "test/noaudio/Knock2_nolimit",
            self.out_dir,
            no_art_select=True,
            embed_lyrics=False,
            resolve_artists_with_ai=False,
        )

        with open("test/test_art/knock2_nolimit.jpg", "rb") as f:
            expected_art = f.read()

        for filename in os.listdir(self.out_dir):
            if filename.lower().endswith((".mp3", ".flac")):
                filepath = os.path.join(self.out_dir, filename)

                album_artist = get_album_artist(filepath)
                self.assertEqual(album_artist, "Knock2", "Album artist not Knock2! :(")

                actual_art = get_cover_art(filepath)
                diff = image_difference(expected_art, actual_art)
                self.assertLessEqual(diff, 2, "Wrong cover art!")

        # Check individual song titles and artists
        self.assertEqual(
            get_song_title(os.path.join(self.out_dir, "come aliv3 (feat. Abi Flynn).flac")),
            "come aliv3 (feat. Abi Flynn)",
        )
        self.assertEqual(
            get_artist(os.path.join(self.out_dir, "come aliv3 (feat. Abi Flynn).flac")),
            "RL Grime; Knock2",
        )

        self.assertEqual(
            get_song_title(os.path.join(self.out_dir, "crank the bass, play the muzik.flac")),
            "crank the bass, play the muzik",
        )
        self.assertEqual(
            get_artist(os.path.join(self.out_dir, "crank the bass, play the muzik.flac")),
            "Knock2",
        )

        self.assertEqual(
            get_song_title(os.path.join(self.out_dir, "dance or dead.flac")),
            "dance or dead",
        )
        self.assertEqual(
            get_artist(os.path.join(self.out_dir, "dance or dead.flac")),
            "Knock2; MILLI",
        )

        self.assertEqual(get_song_title(os.path.join(self.out_dir, "day1s.flac")), "day1s")
        self.assertEqual(get_artist(os.path.join(self.out_dir, "day1s.flac")), "Knock2; Bee-B; XAELO")

        self.assertEqual(
            get_song_title(os.path.join(self.out_dir, "fast n slow.flac")),
            "fast n slow",
        )
        self.assertEqual(get_artist(os.path.join(self.out_dir, "fast n slow.flac")), "Knock2; Vedo")

        self.assertEqual(
            get_song_title(os.path.join(self.out_dir, "feel U luv Me.flac")),
            "feel U luv Me",
        )
        self.assertEqual(get_artist(os.path.join(self.out_dir, "feel U luv Me.flac")), "Knock2")

        self.assertEqual(get_song_title(os.path.join(self.out_dir, "fw me.flac")), "fw me")
        self.assertEqual(get_artist(os.path.join(self.out_dir, "fw me.flac")), "Knock2; Rhea Raj")

        self.assertEqual(
            get_song_title(os.path.join(self.out_dir, "hold my hand.flac")),
            "hold my hand",
        )
        self.assertEqual(
            get_artist(os.path.join(self.out_dir, "hold my hand.flac")),
            "Knock2; Sophia Gripari",
        )

        self.assertEqual(
            get_song_title(os.path.join(self.out_dir, "lights down low.flac")),
            "lights down low",
        )
        self.assertEqual(
            get_artist(os.path.join(self.out_dir, "lights down low.flac")),
            "Knock2; RemK; XAELO",
        )

        self.assertEqual(get_song_title(os.path.join(self.out_dir, "my melody.flac")), "my melody")
        self.assertEqual(
            get_artist(os.path.join(self.out_dir, "my melody.flac")),
            "Knock2; Sophia Gripari",
        )

        self.assertEqual(get_song_title(os.path.join(self.out_dir, "nolimit.flac")), "nolimit")
        self.assertEqual(
            get_artist(os.path.join(self.out_dir, "nolimit.flac")),
            "Knock2; Lauren LaRue",
        )

        self.assertEqual(get_song_title(os.path.join(self.out_dir, "party!.flac")), "party!")
        self.assertEqual(
            get_artist(os.path.join(self.out_dir, "party!.flac")).lower(),
            "knock2; riovaz; cade clair",
        )

        self.assertEqual(get_song_title(os.path.join(self.out_dir, "ready 2.flac")), "ready 2")
        self.assertEqual(get_artist(os.path.join(self.out_dir, "ready 2.flac")), "Knock2")

        rookie_path = _find_output_track(self.out_dir, "rookie")
        self.assertEqual(get_song_title(rookie_path), "rookie")
        self.assertEqual(get_artist(rookie_path).lower(), "knock2; sayak das")

        self.assertEqual(get_song_title(os.path.join(self.out_dir, "select@.flac")), "select@")
        self.assertEqual(get_artist(os.path.join(self.out_dir, "select@.flac")), "Knock2")

        self.assertEqual(
            get_song_title(os.path.join(self.out_dir, "shake!the!city!.flac")),
            "shake!the!city!",
        )
        self.assertEqual(
            get_artist(os.path.join(self.out_dir, "shake!the!city!.flac")),
            "Knock2; Naliya",
        )

        self.assertEqual(
            get_song_title(os.path.join(self.out_dir, "shyne 4 me (feat. PIAO).flac")),
            "shyne 4 me (feat. PIAO)",
        )
        # AI may title-case HOLLY as Holly
        self.assertEqual(
            get_artist(os.path.join(self.out_dir, "shyne 4 me (feat. PIAO).flac")).lower(),
            "knock2; warren hue; holly",
        )

    @pytest.mark.timeout(600)
    def test_porter_robinson_worlds_purchased(self):
        main(
            "test/noaudio/Porter_Robinson_Worlds",
            self.out_dir,
            no_art_select=True,
            embed_lyrics=False,
            resolve_artists_with_ai=False,
        )

        with open("test/test_art/porter_robinson_worlds.jpg", "rb") as f:
            expected_art = f.read()

        for filename in os.listdir(self.out_dir):
            if filename.lower().endswith((".mp3", ".flac")):
                filepath = os.path.join(self.out_dir, filename)

                album_artist = get_album_artist(filepath)
                self.assertEqual(
                    album_artist,
                    "Porter Robinson",
                    "Album artist not Porter Robinson! :(",
                )

                actual_art = get_cover_art(filepath)
                diff = image_difference(expected_art, actual_art)
                self.assertLessEqual(diff, 2, "Wrong cover art!")

        # Tag-only artist resolve: fixtures only have "Porter Robinson" (no feat in tags).
        # AI path is covered by artists_and_features tests.
        expected_titles = {
            "Divinity",
            "Sad Machine",
            "Years Of War",
            "Flicker",
            "Fresh Static Snow",
            "Polygon Dust",
            "Hear The Bells",
            "Natural Light",
            "Lionhearted",
            "Sea Of Voices",
            "Fellow Feeling",
            "Goodbye To A World",
        }
        found_titles = set()
        for filename in os.listdir(self.out_dir):
            if not filename.lower().endswith((".mp3", ".flac")):
                continue
            filepath = os.path.join(self.out_dir, filename)
            found_titles.add(get_song_title(filepath))
            self.assertEqual(get_artist(filepath), "Porter Robinson")
        self.assertEqual(found_titles, expected_titles)

    @pytest.mark.timeout(600)
    def test_no_embedded_cover_art(self):
        # fixture has tags but no embedded cover (stripped from a real track)
        with self.assertRaises(NoTagError):
            get_cover_art("test/noaudio/no_cover_art/Knock2 - feel U luv Me.flac")

        main(
            "test/noaudio/no_cover_art",
            self.out_dir,
            no_art_select=True,
            embed_lyrics=False,
            resolve_artists_with_ai=False,
        )

        # single-file input uses single art path (feel u luv me single cover)
        with open("test/test_art/knock2_feel_u_luv_me.jpg", "rb") as f:
            expected_art = f.read()

        out_files = [f for f in os.listdir(self.out_dir) if f.lower().endswith((".mp3", ".flac"))]
        self.assertEqual(len(out_files), 1)
        out_path = os.path.join(self.out_dir, out_files[0])

        actual_art = get_cover_art(out_path)
        diff = image_difference(expected_art, actual_art)
        self.assertLessEqual(diff, 2, "Should find cover art when file has none")

        self.assertEqual(get_album_artist(out_path), "Knock2")
        self.assertIn("feel u luv me", get_song_title(out_path).lower())
