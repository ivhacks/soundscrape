import os
import sys
import shutil
import tempfile
from unittest import TestCase

# Add parent directory to path to import soundscrape
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from soundscrape import main


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
        shutil.copy2("test/yeet.mp3", os.path.join(self.test_input_dir, "song2.flac"))

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
