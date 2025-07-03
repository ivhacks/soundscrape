import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest import TestCase

from img_diff import image_difference


class SameImageTests(TestCase):
    def test_1_vs_1_original(self):
        """Test 1.png vs itself - should return 0 (identical)"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/1.png", "rb") as f:
            image2_bytes = f.read()
        result = image_difference(image1_bytes, image2_bytes)
        self.assertLessEqual(result, 1, f"Expected <= 1, got {result}")

    def test_1_vs_1_cropped(self):
        """Test 1.png vs 1_cropped_non_square.png - should return 14"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/1_cropped_non_square.png", "rb") as f:
            image2_bytes = f.read()
        result = image_difference(image1_bytes, image2_bytes)
        self.assertLessEqual(result, 14, f"Expected <= 14, got {result}")

    def test_1_vs_1_lossy_4x(self):
        """Test 1.png vs 1_lossy_4x.png - should return 0 (identical)"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/1_lossy_4x.png", "rb") as f:
            image2_bytes = f.read()
        result = image_difference(image1_bytes, image2_bytes)
        self.assertLessEqual(result, 1, f"Expected <= 1, got {result}")

    def test_1_vs_1_low_res(self):
        """Test 1.png vs 1_low_res_300x300.png - should return 0 (identical)"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/1_low_res_300x300.png", "rb") as f:
            image2_bytes = f.read()
        result = image_difference(image1_bytes, image2_bytes)
        self.assertLessEqual(result, 1, f"Expected <= 1, got {result}")

    def test_1_vs_1_shrunk_blown_up(self):
        """Test 1.png vs 1_shrunk_blown_up.png - should return 0 (identical)"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/1_shrunk_blown_up.png", "rb") as f:
            image2_bytes = f.read()
        result = image_difference(image1_bytes, image2_bytes)
        self.assertLessEqual(result, 1, f"Expected <= 1, got {result}")

    def test_1_vs_1_very_lossy(self):
        """Test 1.png vs 1_very_lossy.png - should return 0 (identical)"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/1_very_lossy.png", "rb") as f:
            image2_bytes = f.read()
        result = image_difference(image1_bytes, image2_bytes)
        self.assertLessEqual(result, 1, f"Expected <= 1, got {result}")

    def test_x_image_vs_reference_image(self):
        """Test x_image.jpg vs image.jpg - both should be knock2 nolimit artwork, return 0 (identical)"""
        with open("test/x_image.jpg", "rb") as f:
            x_image_bytes = f.read()
        with open("test/image.jpg", "rb") as f:
            reference_image_bytes = f.read()
        result = image_difference(x_image_bytes, reference_image_bytes)
        self.assertLessEqual(result, 1, f"Expected <= 1, got {result}")


class DifferentImageTests(TestCase):
    def test_1_vs_2_original(self):
        """Test 1.png vs 2.png - should return 26 (different images)"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/2.png", "rb") as f:
            image2_bytes = f.read()
        result = image_difference(image1_bytes, image2_bytes)
        self.assertGreaterEqual(result, 26, f"Expected >= 26, got {result}")

    def test_1_vs_2_cropped(self):
        """Test 1.png vs 2_cropped_non_square.png - should return 26 (different images)"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/2_cropped_non_square.png", "rb") as f:
            image2_bytes = f.read()
        result = image_difference(image1_bytes, image2_bytes)
        self.assertGreaterEqual(result, 26, f"Expected >= 26, got {result}")

    def test_1_vs_2_lossy_4x(self):
        """Test 1.png vs 2_lossy_4x.png - should return 26 (different images)"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/2_lossy_4x.png", "rb") as f:
            image2_bytes = f.read()
        result = image_difference(image1_bytes, image2_bytes)
        self.assertGreaterEqual(result, 26, f"Expected >= 26, got {result}")

    def test_1_vs_2_low_res(self):
        """Test 1.png vs 2_low_res_300x300.png - should return 26 (different images)"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/2_low_res_300x300.png", "rb") as f:
            image2_bytes = f.read()
        result = image_difference(image1_bytes, image2_bytes)
        self.assertGreaterEqual(result, 26, f"Expected >= 26, got {result}")

    def test_1_vs_2_shrunk_blown_up(self):
        """Test 1.png vs 2_shrunk_blown_up.png - should return 26 (different images)"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/2_shrunk_blown_up.png", "rb") as f:
            image2_bytes = f.read()
        result = image_difference(image1_bytes, image2_bytes)
        self.assertGreaterEqual(result, 26, f"Expected >= 26, got {result}")

    def test_1_vs_2_very_lossy(self):
        """Test 1.png vs 2_very_lossy.png - should return 24 (different images)"""
        with open("test/images/1.png", "rb") as f:
            image1_bytes = f.read()
        with open("test/images/2_very_lossy.png", "rb") as f:
            image2_bytes = f.read()
        result = image_difference(image1_bytes, image2_bytes)
        self.assertGreaterEqual(result, 24, f"Expected >= 24, got {result}")
