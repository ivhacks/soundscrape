import os
import shutil
from unittest import TestCase

from file_metadata import get_album_artist, get_cover_art
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
