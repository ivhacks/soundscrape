import os
import shutil
from unittest import TestCase
from youtube_downloader import get_yt_music_metadata, TrackMetadata

class YTMusicMetadataTests(TestCase):
    def test_mameyudoufu_i_dont_know_what_im_doing(self):
        link = "https://music.youtube.com/watch?v=meR1lgaP4ew"
        expected_metadata = TrackMetadata(
            title="I don't know what I'm doing",
            artists=["Mameyudoufu"],
            featured_artists=[],
            album="I don't know what I'm doing",
            year="2021"
        )
        dest_dir = os.path.join(os.getcwd(), "temp")
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        os.chdir("./temp")
        result = get_yt_music_metadata(link)
        
        # Test individual fields to be more flexible with YouTube changes
        self.assertEqual(result.title, expected_metadata.title)
        self.assertEqual(result.artists, expected_metadata.artists)
        self.assertEqual(result.featured_artists, expected_metadata.featured_artists)
        self.assertEqual(result.album, expected_metadata.album)
        self.assertEqual(result.year, expected_metadata.year)
        
        os.chdir("..")
        shutil.rmtree(dest_dir)

    def test_atmozfears_release(self):
        link = "https://music.youtube.com/watch?v=B-7m0EfW7LM"
        expected_metadata = TrackMetadata(
            title="Release",
            artists=["Atmozfears"],
            featured_artists=["David Spekter"],
            album="Release",
            year=None
        )
        dest_dir = os.path.join(os.getcwd(), "temp")
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        os.chdir("./temp")
        result = get_yt_music_metadata(link)
        
        # Test individual fields to be more flexible with YouTube changes
        self.assertEqual(result.title, expected_metadata.title)
        self.assertEqual(result.artists, expected_metadata.artists)
        self.assertEqual(result.featured_artists, expected_metadata.featured_artists)
        self.assertEqual(result.album, expected_metadata.album)
        self.assertEqual(result.year, expected_metadata.year)