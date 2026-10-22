import os
import shutil
import tempfile
from unittest import TestCase

from file_metadata import clear_album_title, get_album_title
from soundscrape import process_dir


class TestMissingAlbum(TestCase):
    def test_nolimit_flac_no_album_uses_title(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            song = os.path.join(temp_dir, "nolimit.flac")
            shutil.copy("test/nolimit.flac", song)
            clear_album_title(song)

            process_dir(
                temp_dir,
                embed_lyrics=False,
                resolve_artists_with_ai=False,
                skip_web=True,
            )

            output = os.path.join(temp_dir, os.listdir(temp_dir)[0])
            self.assertEqual(get_album_title(output), "nolimit")
