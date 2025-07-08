import os
import shutil
from unittest import TestCase

from file_metadata import get_album_artist, get_artist, get_cover_art, get_song_title
from img_diff import image_difference
from soundscrape import main


class IntegrationTests(TestCase):
    def tearDown(self):
        shutil.rmtree("test/temp_output")

    def test_knock2_nolimit_purchased(self):
        main("test/noaudio", "test/temp_output", no_art_select=True)

        with open("test/image.jpg", "rb") as f:
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

        self.assertEqual(get_song_title("test/temp_output/rookie.flac"), "rookie")
        self.assertEqual(get_artist("test/temp_output/rookie.flac"), "Knock2; Sayak Das")

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
