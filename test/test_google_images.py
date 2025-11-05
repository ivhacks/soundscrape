import os
from unittest import TestCase

from bs4 import BeautifulSoup
import requests

from google_images_search import (
    ImageResult,
    _detect_captcha,
    litterbox_upload,
    search_google_images,
    serpapi_reverse_image,
)
from img_diff import image_difference


class GoogleImagesTests(TestCase):
    def test_google_images(self):
        image_path = os.path.join(os.path.dirname(__file__), "image.jpg")

        results = search_google_images(image_path, min_size=700)

        self.assertGreaterEqual(len(results), 5, "Very few results")

        for result in results:
            self.assertIsInstance(result, ImageResult)
            self.assertIsInstance(result.link, str)

            self.assertGreaterEqual(len(result.link), 9)

            self.assertIsInstance(result.x_dimension, int)
            self.assertIsInstance(result.y_dimension, int)
            self.assertGreaterEqual(result.x_dimension, 700)
            self.assertGreaterEqual(result.y_dimension, 700)

    def test_detect_captcha_positive(self):
        captcha_path = os.path.join(os.path.dirname(__file__), "captcha.html")
        with open(captcha_path, "r") as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        result = _detect_captcha(soup)
        self.assertTrue(result)

    def test_detect_captcha_negative(self):
        no_captcha_path = os.path.join(os.path.dirname(__file__), "no_captcha.html")
        with open(no_captcha_path, "r") as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        result = _detect_captcha(soup)
        self.assertFalse(result)

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
        urls = serpapi_reverse_image(url)

        self.assertIsInstance(urls, list)
        self.assertGreater(len(urls), 0)

        for result_url in urls:
            self.assertIsInstance(result_url, str)
            self.assertTrue(result_url.startswith("http"))

        downloaded_image = None
        for result_url in urls:
            images = download_images([result_url], driver=None, fast_dl=False)
            if images:
                downloaded_image = images[0]
                break

        self.assertIsNotNone(downloaded_image)

        with open(image_path, "rb") as f:
            original_image = f.read()

        diff = image_difference(original_image, downloaded_image)
        self.assertLessEqual(diff, 5)
