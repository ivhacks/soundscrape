import os
from unittest import TestCase

from bs4 import BeautifulSoup

from google_images_search import ImageResult, _detect_captcha, search_google_images


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
