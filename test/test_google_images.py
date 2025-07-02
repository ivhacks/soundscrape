import os
from unittest import TestCase

from google_images_search import ImageResult, search_google_images


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
