import os
import shutil
import tempfile
from unittest import TestCase
from unittest.mock import patch

import pytest

from artists_features import find_artists_and_features
from file_metadata import (
    NoTagError,
    clear_lyrics,
    get_artist,
    get_cover_art,
    get_lyrics,
    get_song_title,
    set_album_title,
    set_artist,
    set_song_title,
)
from lyrics import get_lyrics_genius
from parse_and_clean import clean_title
from soundscrape import process_dir


@pytest.mark.xdist_group(name="genius_online_c")
class LyricsFromFileTests(TestCase):
    @pytest.mark.timeout(300)
    def test_knock2_rookie(self):
        filepath = "test/noaudio/Knock2_nolimit/Knock2 - 01. rookie (Explicit).flac"
        artist = get_artist(filepath)
        title = clean_title(get_song_title(filepath))
        artists_and_features = find_artists_and_features(artist, title)

        actual = get_lyrics_genius(
            ", ".join(artists_and_features.artists), title, cache=False
        )

        expected_path = os.path.join("test/test_output_genius", "knock2_rookie.txt")
        with open(expected_path, "r", encoding="utf-8") as f:
            expected = f.read()

        self.assertEqual(actual, expected)


class MissingGeniusLyricsTests(TestCase):
    def test_process_dir_skips_missing_genius_lyrics(self):
        work = tempfile.mkdtemp()
        try:
            dest = os.path.join(work, "song.mp3")
            shutil.copy2("test/yeet.mp3", dest)
            set_artist(dest, "Skrillex; Bobby Raps")
            set_song_title(dest, "Leave Me Like This")
            set_album_title(dest, "Quest For Fire")
            clear_lyrics(dest)

            def no_match(artist, title, cache=False):
                raise ValueError(f"No Genius match for {artist} - {title}")

            with patch("soundscrape.get_lyrics_genius", no_match):
                process_dir(
                    work,
                    no_art_select=True,
                    embed_lyrics=True,
                    resolve_artists_with_ai=False,
                    skip_web=True,
                )

            out = os.path.join(work, "Leave Me Like This.mp3")
            self.assertTrue(os.path.exists(out))
            self.assertEqual(get_artist(out), "Skrillex; Bobby Raps")
            self.assertEqual(get_song_title(out), "Leave Me Like This")
            self.assertGreater(len(get_cover_art(out)), 0)
            with self.assertRaises(NoTagError):
                get_lyrics(out)
        finally:
            shutil.rmtree(work)
