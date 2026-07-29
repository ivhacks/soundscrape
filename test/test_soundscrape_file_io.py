import os
import shutil
import sys
import tempfile
from unittest import TestCase

import pytest


# Add parent directory to path to import soundscrape
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from file_metadata import (
    get_album_artist,
    get_album_title,
    get_artist,
    get_cover_art,
    get_song_title,
    set_album_artist,
    set_album_title,
    set_artist,
    set_cover_art,
    set_song_title,
)
from soundscrape import create_noaudio_files, main


# share worker with metadata tests — both touch test/yeet.* fixtures
@pytest.mark.xdist_group(name="serial_metadata_tests")
class SoundScrapeFileIOTests(TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()

        # Create all directories
        self.test_input_dir = os.path.join(self.test_dir, "input_dir")
        self.existing_output_dir = os.path.join(self.test_dir, "existing_output")
        os.makedirs(self.test_input_dir)
        os.makedirs(self.existing_output_dir)

        # Create a test file for testing file input error
        self.test_input_file = os.path.join(self.test_dir, "test_input.mp3")
        shutil.copy2("test/yeet.mp3", self.test_input_file)

        # Copy test files to input directory
        shutil.copy2("test/yeet.mp3", os.path.join(self.test_input_dir, "song1.mp3"))
        shutil.copy2("test/yeet.flac", os.path.join(self.test_input_dir, "song2.flac"))

    def tearDown(self):
        # Clean up temporary directory
        shutil.rmtree(self.test_dir)

    def test_input_dir_output_dir_exists(self):
        """Test input dir, output dir that exists"""
        main(self.test_input_dir, self.existing_output_dir, no_processing=True)

        expected_output1 = os.path.join(self.existing_output_dir, "song1.mp3")
        expected_output2 = os.path.join(self.existing_output_dir, "song2.flac")

        self.assertTrue(os.path.exists(expected_output1))
        self.assertTrue(os.path.exists(expected_output2))

        # Verify file sizes match
        original1 = os.path.join(self.test_input_dir, "song1.mp3")
        original2 = os.path.join(self.test_input_dir, "song2.flac")
        self.assertEqual(os.path.getsize(original1), os.path.getsize(expected_output1))
        self.assertEqual(os.path.getsize(original2), os.path.getsize(expected_output2))

    def test_input_dir_output_dir_not_exists(self):
        """Test input dir, output dir that doesn't exist"""
        new_output_dir = os.path.join(self.test_dir, "new_output_dir2")

        # Verify directory doesn't exist yet
        self.assertFalse(os.path.exists(new_output_dir))

        main(self.test_input_dir, new_output_dir, no_processing=True)

        expected_output1 = os.path.join(new_output_dir, "song1.mp3")
        expected_output2 = os.path.join(new_output_dir, "song2.flac")

        self.assertTrue(os.path.exists(new_output_dir))
        self.assertTrue(os.path.exists(expected_output1))
        self.assertTrue(os.path.exists(expected_output2))

        # Verify file sizes match
        original1 = os.path.join(self.test_input_dir, "song1.mp3")
        original2 = os.path.join(self.test_input_dir, "song2.flac")
        self.assertEqual(os.path.getsize(original1), os.path.getsize(expected_output1))
        self.assertEqual(os.path.getsize(original2), os.path.getsize(expected_output2))

    def test_invalid_input_path(self):
        """Test error case: nonexistent input path"""
        invalid_input = os.path.join(self.test_dir, "nonexistent_dir")
        output_dir = os.path.join(self.test_dir, "output")

        with self.assertRaises(FileNotFoundError):
            main(invalid_input, output_dir, no_processing=True)

        self.assertFalse(os.path.exists(output_dir))

    def test_input_file_instead_of_directory_error(self):
        """Test error case: input is a file instead of directory"""
        output_dir = os.path.join(self.test_dir, "output")

        with self.assertRaises(ValueError):
            main(self.test_input_file, output_dir, no_processing=True)

        self.assertFalse(os.path.exists(output_dir))

    def test_noaudio_basic(self):
        """Test creating noaudio files with basic tag copying"""
        output_dir = os.path.join(self.test_dir, "noaudio_output")

        create_noaudio_files(self.test_input_dir, output_dir)

        output1 = os.path.join(output_dir, "song1.mp3")
        output2 = os.path.join(output_dir, "song2.flac")

        self.assertTrue(os.path.exists(output1))
        self.assertTrue(os.path.exists(output2))

        original1 = os.path.join(self.test_input_dir, "song1.mp3")
        original2 = os.path.join(self.test_input_dir, "song2.flac")
        self.assertLess(os.path.getsize(output1), os.path.getsize(original1))
        self.assertLess(os.path.getsize(output2), os.path.getsize(original2))

    def test_noaudio_preserves_all_tags(self):
        """Test that all metadata is preserved when creating noaudio files"""
        input_dir = os.path.join(self.test_dir, "tagged_input")
        output_dir = os.path.join(self.test_dir, "noaudio_tagged_output")
        os.makedirs(input_dir)

        # yeet.flac is a small tagged fixture (nolimit.flac is huge/flaky under parallel IO)
        source = os.path.join(input_dir, "test_song.flac")
        shutil.copy2("test/yeet.flac", source)
        set_artist(source, "Tag Artist")
        set_song_title(source, "Tag Title")
        set_album_title(source, "Tag Album")
        set_album_artist(source, "Tag Album Artist")
        with open("test/cat.jpg", "rb") as f:
            set_cover_art(source, f.read())

        create_noaudio_files(input_dir, output_dir)

        output_file = os.path.join(output_dir, "test_song.flac")
        self.assertTrue(os.path.exists(output_file))

        self.assertEqual(get_artist(output_file), "Tag Artist")
        self.assertEqual(get_song_title(output_file), "Tag Title")
        self.assertEqual(get_album_title(output_file), "Tag Album")
        self.assertEqual(get_album_artist(output_file), "Tag Album Artist")
        self.assertEqual(get_cover_art(output_file), get_cover_art(source))

        self.assertLess(os.path.getsize(output_file), os.path.getsize(source))

    def test_noaudio_multiple_files(self):
        """Test creating noaudio files for multiple songs"""
        input_dir = os.path.join(self.test_dir, "multi_input")
        output_dir = os.path.join(self.test_dir, "noaudio_multi_output")
        os.makedirs(input_dir)

        input_files = [
            ("test/yeet.flac", "song1.flac"),
            ("test/yeet.mp3", "song2.mp3"),
            ("test/yeet.flac", "song3.flac"),
        ]

        for src, dest in input_files:
            shutil.copy2(src, os.path.join(input_dir, dest))

        create_noaudio_files(input_dir, output_dir)

        output1 = os.path.join(output_dir, "song1.flac")
        output2 = os.path.join(output_dir, "song2.mp3")
        output3 = os.path.join(output_dir, "song3.flac")

        self.assertTrue(os.path.exists(output1))
        self.assertTrue(os.path.exists(output2))
        self.assertTrue(os.path.exists(output3))

        # noaudio rewrites audio body; output must be smaller than real flac source
        self.assertLess(os.path.getsize(output1), os.path.getsize("test/yeet.flac"))
        self.assertLess(os.path.getsize(output2), os.path.getsize("test/yeet.mp3"))
        self.assertLess(os.path.getsize(output3), os.path.getsize("test/yeet.flac"))
