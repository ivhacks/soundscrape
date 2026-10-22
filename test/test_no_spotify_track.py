import os
import shutil
import tempfile
from unittest import TestCase
from unittest.mock import MagicMock, patch

from file_metadata import get_cover_art
from soundscrape import process_dir


class TestNoSpotifyTrack(TestCase):
    def test_nolimit_flac_spotify_missing_keeps_embedded_art(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            song = os.path.join(temp_dir, "nolimit.flac")
            shutil.copy("test/nolimit.flac", song)
            embedded_art = get_cover_art(song)

            with (
                patch(
                    "soundscrape.search_cover_art_by_text",
                    side_effect=ValueError("No track found for 'nolimit' by 'Knock2'"),
                ),
                patch("soundscrape.search_google_images", return_value=[]),
                patch("soundscrape.create_stealth_driver", return_value=MagicMock()),
                patch("soundscrape.download_images", return_value=[]),
                patch(
                    "soundscrape.downselect_images",
                    side_effect=lambda images, reference: images,
                ),
            ):
                process_dir(
                    temp_dir,
                    no_art_select=True,
                    embed_lyrics=False,
                    resolve_artists_with_ai=False,
                )

            output = os.path.join(temp_dir, os.listdir(temp_dir)[0])
            self.assertEqual(get_cover_art(output), embedded_art)
