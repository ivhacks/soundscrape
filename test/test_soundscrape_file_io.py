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

        # Define file paths
        self.test_input_file = os.path.join(self.test_dir, "test_input.mp3")
        self.test_input_file2 = os.path.join(self.test_dir, "test_input2.flac")

        # Copy all test files
        shutil.copy2("test/yeet.mp3", self.test_input_file)
        shutil.copy2("test/yeet.mp3", self.test_input_file2)
        shutil.copy2("test/yeet.mp3", os.path.join(self.test_input_dir, "song1.mp3"))
        shutil.copy2("test/yeet.mp3", os.path.join(self.test_input_dir, "song2.flac"))

    def tearDown(self):
        # Clean up temporary directory
        shutil.rmtree(self.test_dir)

    def test_single_input_file_single_output_file(self):
        """Test single input file, single output file"""
        output_file = os.path.join(self.test_dir, "output.mp3")

        main(self.test_input_file, output_file, no_processing=True)

        self.assertTrue(os.path.exists(output_file))
        # Verify file sizes match (indicating successful copy)
        self.assertEqual(
            os.path.getsize(self.test_input_file), os.path.getsize(output_file)
        )

    def test_single_input_file_output_dir_exists(self):
        """Test single input file, output dir that exists"""
        main(self.test_input_file, self.existing_output_dir, no_processing=True)

        expected_output = os.path.join(self.existing_output_dir, "test_input.mp3")

        self.assertTrue(os.path.exists(expected_output))
        self.assertEqual(
            os.path.getsize(self.test_input_file), os.path.getsize(expected_output)
        )

    def test_single_input_file_output_dir_not_exists(self):
        """Test single input file, output dir that doesn't exist (should create)"""
        new_output_dir = os.path.join(self.test_dir, "new_output_dir")

        # Verify directory doesn't exist yet
        self.assertFalse(os.path.exists(new_output_dir))

        main(self.test_input_file, new_output_dir, no_processing=True)

        expected_output = os.path.join(new_output_dir, "test_input.mp3")

        self.assertTrue(os.path.exists(new_output_dir))
        self.assertTrue(os.path.exists(expected_output))
        self.assertEqual(
            os.path.getsize(self.test_input_file), os.path.getsize(expected_output)
        )

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

    def test_multiple_files_to_single_output_file_error(self):
        """Test error case: multiple files to single output filename"""
        output_file = os.path.join(self.test_dir, "output.mp3")

        with self.assertRaises(ValueError):
            main(self.test_input_dir, output_file, no_processing=True)

        self.assertFalse(os.path.exists(output_file))

    def test_invalid_input_path(self):
        """Test error case: invalid input path"""
        invalid_input = os.path.join(self.test_dir, "nonexistent.mp3")
        output_file = os.path.join(self.test_dir, "output.mp3")

        with self.assertRaises(FileNotFoundError):
            main(invalid_input, output_file, no_processing=True)

        self.assertFalse(os.path.exists(output_file))
