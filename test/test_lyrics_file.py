import os
from unittest import TestCase

import pytest

from artists_features import find_artists_and_features
from file_metadata import get_artist, get_song_title
from lyrics import get_lyrics_genius
from parse_and_clean import clean_title


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
