from io import BytesIO
from unittest import TestCase

from PIL import Image
import pytest
import requests

from google_images_search import (
    download_images,
    search_google_images,
    serpapi_reverse_image,
)
from img_diff import image_difference
from temp_host import scale_down_image, upload_temp_image


@pytest.mark.xdist_group(name="google_images")
class GoogleImagesTests(TestCase):
    def test_google_images(self):
        image_path = "test/test_art/knock2_nolimit.jpg"

        results = search_google_images(image_path)

        self.assertGreaterEqual(len(results), 5, "Very few results")

        for result in results:
            self.assertIsInstance(result, str)
            self.assertGreaterEqual(len(result), 9)
            self.assertTrue(result.startswith("http"))

    def test_upload_temp_image(self):
        image_path = "test/test_art/knock2_nolimit.jpg"

        url = upload_temp_image(image_path)

        self.assertIsInstance(url, str)
        self.assertTrue(url.startswith("https://"))

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        downloaded_image = response.content

        with open(image_path, "rb") as f:
            original_image = f.read()

        diff = image_difference(original_image, downloaded_image)
        self.assertLessEqual(diff, 2)

        response_verified = requests.get(url, verify=True)
        self.assertEqual(response_verified.status_code, 200)

        downloaded_image_verified = response_verified.content

        diff_verified = image_difference(original_image, downloaded_image_verified)
        self.assertLessEqual(diff_verified, 2)

    def test_serpapi_reverse_image(self):
        image_path = "test/test_art/knock2_nolimit.jpg"

        url = upload_temp_image(image_path)
        urls = serpapi_reverse_image(url, num_results=10)

        self.assertIsInstance(urls, list)
        self.assertGreater(len(urls), 9)

        for url in urls:
            self.assertIsInstance(url, str)
            self.assertTrue(url.startswith("http"))

        downloaded_image = None
        for url in urls:
            images = download_images([url], driver=None)
            if images:
                downloaded_image = images[0]
                break

        self.assertIsNotNone(downloaded_image)
        assert downloaded_image is not None

        with open(image_path, "rb") as f:
            original_image = f.read()

        diff = image_difference(original_image, downloaded_image)
        self.assertLessEqual(diff, 5)

    def test_serpapi_two_results(self):
        image_path = "test/test_art/knock2_nolimit.jpg"

        url = upload_temp_image(image_path)
        urls = serpapi_reverse_image(url, num_results=2)

        self.assertEqual(len(urls), 2)
        for url in urls:
            self.assertIsInstance(url, str)
            self.assertTrue(url.startswith("http"))

    def test_serpapi_ten_results(self):
        image_path = "test/test_art/knock2_nolimit.jpg"

        url = upload_temp_image(image_path)
        urls = serpapi_reverse_image(url, num_results=10)

        self.assertEqual(len(urls), 10)
        for url in urls:
            self.assertIsInstance(url, str)
            self.assertTrue(url.startswith("http"))

    def test_scale_down_image_1(self):
        with open("test/images/1.png", "rb") as f:
            original_bytes = f.read()

        scaled_bytes = scale_down_image(original_bytes)

        scaled_img = Image.open(BytesIO(scaled_bytes))
        width, height = scaled_img.size
        self.assertEqual(width, 300)
        self.assertEqual(height, 300)

        diff = image_difference(original_bytes, scaled_bytes)
        self.assertLessEqual(diff, 2)

    def test_scale_down_image_2(self):
        with open("test/images/2.png", "rb") as f:
            original_bytes = f.read()

        scaled_bytes = scale_down_image(original_bytes)

        scaled_img = Image.open(BytesIO(scaled_bytes))
        width, height = scaled_img.size
        self.assertEqual(width, 300)
        self.assertEqual(height, 300)

        diff = image_difference(original_bytes, scaled_bytes)
        self.assertLessEqual(diff, 2)
