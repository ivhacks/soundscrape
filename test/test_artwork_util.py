import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest import TestCase

from artwork_util import same_images


class SameImageTests(TestCase):
    def test_1_vs_1_original(self):
        """Test 1.png vs itself - should return close to 1"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/1.png", "rb") as f:
            image2_bytes = f.read()
        result = same_images(image1_bytes, image2_bytes)
        self.assertGreaterEqual(result, 0.9, f"Expected >= 0.9, got {result}")

    def test_1_vs_1_cropped(self):
        """Test 1.png vs 1_cropped_non_square.png - should return close to 1"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/1_cropped_non_square.png", "rb") as f:
            image2_bytes = f.read()
        result = same_images(image1_bytes, image2_bytes)
        self.assertGreaterEqual(result, 0.7, f"Expected >= 0.7, got {result}")

    def test_1_vs_1_lossy_4x(self):
        """Test 1.png vs 1_lossy_4x.png - should return close to 1"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/1_lossy_4x.png", "rb") as f:
            image2_bytes = f.read()
        result = same_images(image1_bytes, image2_bytes)
        self.assertGreaterEqual(result, 0.7, f"Expected >= 0.7, got {result}")

    def test_1_vs_1_low_res(self):
        """Test 1.png vs 1_low_res_300x300.png - should return close to 1"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/1_low_res_300x300.png", "rb") as f:
            image2_bytes = f.read()
        result = same_images(image1_bytes, image2_bytes)
        self.assertGreaterEqual(result, 0.25, f"Expected >= 0.25, got {result}")

    def test_1_vs_1_shrunk_blown_up(self):
        """Test 1.png vs 1_shrunk_blown_up.png - should return close to 1"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/1_shrunk_blown_up.png", "rb") as f:
            image2_bytes = f.read()
        result = same_images(image1_bytes, image2_bytes)
        self.assertGreaterEqual(result, 0.4, f"Expected >= 0.4, got {result}")

    def test_1_vs_1_very_lossy(self):
        """Test 1.png vs 1_very_lossy.png - should return close to 1"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/1_very_lossy.png", "rb") as f:
            image2_bytes = f.read()
        result = same_images(image1_bytes, image2_bytes)
        self.assertGreaterEqual(result, 0.5, f"Expected >= 0.5, got {result}")


class DifferentImageTests(TestCase):
    def test_1_vs_2_original(self):
        """Test 1.png vs 2.png - should return lower similarity"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/2.png", "rb") as f:
            image2_bytes = f.read()
        result = same_images(image1_bytes, image2_bytes)
        self.assertLessEqual(result, 0.55, f"Expected <= 0.55, got {result}")

    def test_1_vs_2_cropped(self):
        """Test 1.png vs 2_cropped_non_square.png - should return lower similarity"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/2_cropped_non_square.png", "rb") as f:
            image2_bytes = f.read()
        result = same_images(image1_bytes, image2_bytes)
        self.assertLessEqual(result, 0.55, f"Expected <= 0.55, got {result}")

    def test_1_vs_2_lossy_4x(self):
        """Test 1.png vs 2_lossy_4x.png - should return lower similarity"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/2_lossy_4x.png", "rb") as f:
            image2_bytes = f.read()
        result = same_images(image1_bytes, image2_bytes)
        self.assertLessEqual(result, 0.55, f"Expected <= 0.55, got {result}")

    def test_1_vs_2_low_res(self):
        """Test 1.png vs 2_low_res_300x300.png - should return lower similarity"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/2_low_res_300x300.png", "rb") as f:
            image2_bytes = f.read()
        result = same_images(image1_bytes, image2_bytes)
        self.assertLessEqual(result, 0.55, f"Expected <= 0.55, got {result}")

    def test_1_vs_2_shrunk_blown_up(self):
        """Test 1.png vs 2_shrunk_blown_up.png - should return lower similarity"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/2_shrunk_blown_up.png", "rb") as f:
            image2_bytes = f.read()
        result = same_images(image1_bytes, image2_bytes)
        self.assertLessEqual(result, 0.55, f"Expected <= 0.55, got {result}")

    def test_1_vs_2_very_lossy(self):
        """Test 1.png vs 2_very_lossy.png - should return lower similarity"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/2_very_lossy.png", "rb") as f:
            image2_bytes = f.read()
        result = same_images(image1_bytes, image2_bytes)
        self.assertLessEqual(result, 0.55, f"Expected <= 0.55, got {result}")
