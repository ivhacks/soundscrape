import os
import shutil
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


def _find_output_track(needle: str) -> str:
    matches = [f for f in os.listdir("test/temp_output") if needle.lower() in f.lower() and f.lower().endswith((".mp3", ".flac"))]
    if len(matches) != 1:
        raise AssertionError(f"expected exactly 1 file matching {needle!r}, got {matches!r}")
    return os.path.join("test/temp_output", matches[0])


@pytest.mark.xdist_group(name="serial_metadata_tests")
class IntegrationTests(TestCase):
    def tearDown(self):
        try:
            shutil.rmtree("test/temp_output")
        except FileNotFoundError:
            pass

    def test_knock2_nolimit_purchased(self):
        main("test/noaudio/Knock2_nolimit", "test/temp_output", no_art_select=True)

        with open("test/test_art/knock2_nolimit.jpg", "rb") as f:
            expected_art = f.read()

        for filename in os.listdir("test/temp_output"):
            if filename.lower().endswith((".mp3", ".flac")):
                filepath = os.path.join("test/temp_output", filename)

                album_artist = get_album_artist(filepath)
                self.assertEqual(album_artist, "Knock2", "Album artist not Knock2! :(")

                actual_art = get_cover_art(filepath)
                diff = image_difference(expected_art, actual_art)
                self.assertLessEqual(diff, 2, "Wrong cover art!")

        # Check individual song titles and artists
        self.assertEqual(
            get_song_title("test/temp_output/come aliv3 (feat. Abi Flynn).flac"),
            "come aliv3 (feat. Abi Flynn)",
        )
        self.assertEqual(
            get_artist("test/temp_output/come aliv3 (feat. Abi Flynn).flac"),
            "RL Grime; Knock2",
        )

        self.assertEqual(
            get_song_title("test/temp_output/crank the bass, play the muzik.flac"),
            "crank the bass, play the muzik",
        )
        self.assertEqual(get_artist("test/temp_output/crank the bass, play the muzik.flac"), "Knock2")

        self.assertEqual(get_song_title("test/temp_output/dance or dead.flac"), "dance or dead")
        self.assertEqual(get_artist("test/temp_output/dance or dead.flac"), "Knock2; MILLI")

        self.assertEqual(get_song_title("test/temp_output/day1s.flac"), "day1s")
        self.assertEqual(get_artist("test/temp_output/day1s.flac"), "Knock2; Bee-B; XAELO")

        self.assertEqual(get_song_title("test/temp_output/fast n slow.flac"), "fast n slow")
        self.assertEqual(get_artist("test/temp_output/fast n slow.flac"), "Knock2; Vedo")

        self.assertEqual(get_song_title("test/temp_output/feel U luv Me.flac"), "feel U luv Me")
        self.assertEqual(get_artist("test/temp_output/feel U luv Me.flac"), "Knock2")

        self.assertEqual(get_song_title("test/temp_output/fw me.flac"), "fw me")
        self.assertEqual(get_artist("test/temp_output/fw me.flac"), "Knock2; Rhea Raj")

        self.assertEqual(get_song_title("test/temp_output/hold my hand.flac"), "hold my hand")
        self.assertEqual(get_artist("test/temp_output/hold my hand.flac"), "Knock2; Sophia Gripari")

        self.assertEqual(get_song_title("test/temp_output/lights down low.flac"), "lights down low")
        self.assertEqual(get_artist("test/temp_output/lights down low.flac"), "Knock2; RemK; XAELO")

        self.assertEqual(get_song_title("test/temp_output/my melody.flac"), "my melody")
        self.assertEqual(get_artist("test/temp_output/my melody.flac"), "Knock2; Sophia Gripari")

        self.assertEqual(get_song_title("test/temp_output/nolimit.flac"), "nolimit")
        self.assertEqual(get_artist("test/temp_output/nolimit.flac"), "Knock2; Lauren LaRue")

        self.assertEqual(get_song_title("test/temp_output/party!.flac"), "party!")
        self.assertEqual(get_artist("test/temp_output/party!.flac"), "Knock2; Riovaz; cade clair")

        self.assertEqual(get_song_title("test/temp_output/ready 2.flac"), "ready 2")
        self.assertEqual(get_artist("test/temp_output/ready 2.flac"), "Knock2")

        rookie_path = _find_output_track("rookie")
        self.assertEqual(get_song_title(rookie_path), "rookie")
        self.assertEqual(get_artist(rookie_path), "Knock2; Sayak Das")

        self.assertEqual(get_song_title("test/temp_output/select@.flac"), "select@")
        self.assertEqual(get_artist("test/temp_output/select@.flac"), "Knock2")

        self.assertEqual(get_song_title("test/temp_output/shake!the!city!.flac"), "shake!the!city!")
        self.assertEqual(get_artist("test/temp_output/shake!the!city!.flac"), "Knock2; Naliya")

        self.assertEqual(
            get_song_title("test/temp_output/shyne 4 me (feat. PIAO).flac"),
            "shyne 4 me (feat. PIAO)",
        )
        self.assertEqual(
            get_artist("test/temp_output/shyne 4 me (feat. PIAO).flac"),
            "Knock2; Warren Hue; HOLLY",
        )
        shutil.rmtree("test/temp_output")

    def test_porter_robinson_worlds_purchased(self):
        main(
            "test/noaudio/Porter_Robinson_Worlds",
            "test/temp_output",
            no_art_select=True,
        )

        with open("test/test_art/porter_robinson_worlds.jpg", "rb") as f:
            expected_art = f.read()

        for filename in os.listdir("test/temp_output"):
            if filename.lower().endswith((".mp3", ".flac")):
                filepath = os.path.join("test/temp_output", filename)

                album_artist = get_album_artist(filepath)
                self.assertEqual(
                    album_artist,
                    "Porter Robinson",
                    "Album artist not Porter Robinson! :(",
                )

                actual_art = get_cover_art(filepath)
                diff = image_difference(expected_art, actual_art)
                self.assertLessEqual(diff, 2, "Wrong cover art!")

        # Check individual song titles and artists
        self.assertEqual(
            get_song_title("test/temp_output/Divinity (feat. Amy Millan).flac"),
            "Divinity (feat. Amy Millan)",
        )
        self.assertEqual(
            get_artist("test/temp_output/Divinity (feat. Amy Millan).flac"),
            "Porter Robinson",
        )

        self.assertEqual(get_song_title("test/temp_output/Sad Machine.flac"), "Sad Machine")
        self.assertEqual(get_artist("test/temp_output/Sad Machine.flac"), "Porter Robinson")

        years_path = _find_output_track("years of war")
        self.assertEqual(
            get_song_title(years_path),
            "Years Of War (feat. Breanne Düren, Sean Caskey)",
        )
        self.assertEqual(get_artist(years_path), "Porter Robinson")

        self.assertEqual(get_song_title("test/temp_output/Flicker.flac"), "Flicker")
        self.assertEqual(get_artist("test/temp_output/Flicker.flac"), "Porter Robinson")

        self.assertEqual(
            get_song_title("test/temp_output/Fresh Static Snow.flac"),
            "Fresh Static Snow",
        )
        self.assertEqual(get_artist("test/temp_output/Fresh Static Snow.flac"), "Porter Robinson")

        self.assertEqual(
            get_song_title("test/temp_output/Polygon Dust (feat. Lemaitre).flac"),
            "Polygon Dust (feat. Lemaitre)",
        )
        self.assertEqual(
            get_artist("test/temp_output/Polygon Dust (feat. Lemaitre).flac"),
            "Porter Robinson",
        )

        self.assertEqual(
            get_song_title("test/temp_output/Hear The Bells (feat. Imaginary Cities).flac"),
            "Hear The Bells (feat. Imaginary Cities)",
        )
        self.assertEqual(
            get_artist("test/temp_output/Hear The Bells (feat. Imaginary Cities).flac"),
            "Porter Robinson",
        )

        self.assertEqual(get_song_title("test/temp_output/Natural Light.flac"), "Natural Light")
        self.assertEqual(get_artist("test/temp_output/Natural Light.flac"), "Porter Robinson")

        self.assertEqual(
            get_song_title("test/temp_output/Lionhearted (feat. Urban Cone).flac"),
            "Lionhearted (feat. Urban Cone)",
        )
        self.assertEqual(
            get_artist("test/temp_output/Lionhearted (feat. Urban Cone).flac"),
            "Porter Robinson",
        )

        self.assertEqual(get_song_title("test/temp_output/Sea Of Voices.flac"), "Sea Of Voices")
        self.assertEqual(get_artist("test/temp_output/Sea Of Voices.flac"), "Porter Robinson")

        self.assertEqual(get_song_title("test/temp_output/Fellow Feeling.flac"), "Fellow Feeling")
        self.assertEqual(get_artist("test/temp_output/Fellow Feeling.flac"), "Porter Robinson")

        self.assertEqual(
            get_song_title("test/temp_output/Goodbye To A World.flac"),
            "Goodbye To A World",
        )
        self.assertEqual(get_artist("test/temp_output/Goodbye To A World.flac"), "Porter Robinson")

        shutil.rmtree("test/temp_output")

    def test_no_embedded_cover_art(self):
        # fixture has tags but no embedded cover (stripped from a real track)
        with self.assertRaises(NoTagError):
            get_cover_art("test/noaudio/no_cover_art/Knock2 - feel U luv Me.flac")

        main(
            "test/noaudio/no_cover_art",
            "test/temp_output",
            no_art_select=True,
        )

        # single-file input uses single art path (feel u luv me single cover)
        with open("test/test_art/knock2_feel_u_luv_me.jpg", "rb") as f:
            expected_art = f.read()

        out_files = [f for f in os.listdir("test/temp_output") if f.lower().endswith((".mp3", ".flac"))]
        self.assertEqual(len(out_files), 1)
        out_path = os.path.join("test/temp_output", out_files[0])

        actual_art = get_cover_art(out_path)
        diff = image_difference(expected_art, actual_art)
        self.assertLessEqual(diff, 2, "Should find cover art when file has none")

        self.assertEqual(get_album_artist(out_path), "Knock2")
        self.assertIn("feel u luv me", get_song_title(out_path).lower())

        shutil.rmtree("test/temp_output")
