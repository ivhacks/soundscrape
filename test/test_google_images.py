import os
from unittest import TestCase

import pytest
import requests

from google_images_search import (
    litterbox_upload,
    search_google_images,
    serpapi_reverse_image,
)
from img_diff import image_difference


@pytest.mark.xdist_group(name="google_images")
class GoogleImagesTests(TestCase):
    def test_google_images(self):
        image_path = os.path.join(os.path.dirname(__file__), "image.jpg")

        results = search_google_images(image_path)

        self.assertGreaterEqual(len(results), 5, "Very few results")

        for result in results:
            self.assertIsInstance(result, str)
            self.assertGreaterEqual(len(result), 9)
            self.assertTrue(result.startswith("http"))

    def test_litterbox_upload(self):
        image_path = os.path.join(os.path.dirname(__file__), "image.jpg")

        url = litterbox_upload(image_path)

        self.assertIsInstance(url, str)
        self.assertTrue(url.startswith("https://"))

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        downloaded_image = response.content

        with open(image_path, "rb") as f:
            original_image = f.read()

        diff = image_difference(original_image, downloaded_image)
        self.assertEqual(diff, 0)

    def test_serpapi_reverse_image(self):
        from google_images_search import download_images

        image_path = os.path.join(os.path.dirname(__file__), "image.jpg")

        url = litterbox_upload(image_path)
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
        image_path = os.path.join(os.path.dirname(__file__), "image.jpg")

        url = litterbox_upload(image_path)
        urls = serpapi_reverse_image(url, num_results=2)

        self.assertEqual(len(urls), 2)
        for url in urls:
            self.assertIsInstance(url, str)
            self.assertTrue(url.startswith("http"))

    def test_serpapi_ten_results(self):
        image_path = os.path.join(os.path.dirname(__file__), "image.jpg")

        url = litterbox_upload(image_path)
        urls = serpapi_reverse_image(url, num_results=10)

        self.assertEqual(len(urls), 10)
        for url in urls:
            self.assertIsInstance(url, str)
            self.assertTrue(url.startswith("http"))
