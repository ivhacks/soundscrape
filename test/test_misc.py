import os
import shutil
from unittest import TestCase
from lyrics import search_term_preprocessing, generate_lyrics_filename
from file_metadata import set_lyrics, get_lyrics


class MiscTests(TestCase):
    def test_predownloaded_html(self):
        input = "cool & good"
        expected_output = "cool %26 good"

        self.assertEqual(search_term_preprocessing(input), expected_output)

    def test_generate_lyrics_filename(self):
        input_artist = "\\\\The Backslashes\\\\   "
        input_title = "   OwO, what's this?"
        expected_output = "the_backslashes_owo,_what's_this.txt"

        self.assertEqual(
            generate_lyrics_filename(input_artist, input_title), expected_output
        )

    # This test doesn't properly isolate the issue
    def test_lyrics_properly_terminated(self):
        dest_dir = os.path.join(os.getcwd(), "temp")
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        src = os.path.join(os.getcwd(), "test/yeet.mp3")
        dest = os.path.join(os.getcwd(), "temp/yeet.mp3")
        shutil.copyfile(src, dest)

        lyrics = "yeet"

        set_lyrics(dest, lyrics)

        tag_lyrics = get_lyrics(dest)
        self.assertEqual(tag_lyrics, lyrics)
        os.remove(dest)
        shutil.rmtree(dest_dir)
