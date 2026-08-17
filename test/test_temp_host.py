from unittest import TestCase

import pytest
import requests

from img_diff import image_difference
from temp_host import (
    TempHostError,
    scale_down_image,
    upload_litterbox,
    upload_temp_image,
    upload_uguu,
)


IMAGE_PATH = "test/test_art/knock2_nolimit.jpg"


@pytest.mark.xdist_group(name="temp_host")
class TempHostTests(TestCase):
    def test_upload_litterbox(self):
        with open(IMAGE_PATH, "rb") as f:
            original_image = f.read()
        url = upload_litterbox(scale_down_image(original_image))

        self.assertIsInstance(url, str)
        self.assertTrue(url.startswith("https://"))

        response = requests.get(url, timeout=30)
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(image_difference(original_image, response.content), 2)

    def test_upload_uguu(self):
        with open(IMAGE_PATH, "rb") as f:
            original_image = f.read()
        url = upload_uguu(scale_down_image(original_image))

        self.assertIsInstance(url, str)
        self.assertTrue(url.startswith("https://"))

        response = requests.get(url, timeout=30)
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(image_difference(original_image, response.content), 2)

    def test_upload_temp_image(self):
        url = upload_temp_image(IMAGE_PATH)
        self.assertIsInstance(url, str)
        self.assertTrue(url.startswith("https://"))

        response = requests.get(url, timeout=30)
        self.assertEqual(response.status_code, 200)

        with open(IMAGE_PATH, "rb") as f:
            original_image = f.read()
        self.assertLessEqual(image_difference(original_image, response.content), 2)

    def test_upload_temp_image_tries_next_host(self):
        def dead(_image_bytes):
            raise Exception("down")

        url = upload_temp_image(IMAGE_PATH, uploaders=[dead, upload_litterbox])
        self.assertTrue(url.startswith("https://"))
        self.assertIn("litter.catbox.moe", url)

    def test_upload_temp_image_all_fail(self):
        def dead(_image_bytes):
            raise Exception("down")

        with self.assertRaises(TempHostError) as ctx:
            upload_temp_image(IMAGE_PATH, uploaders=[dead, dead])
        self.assertIn("all temp hosts failed", str(ctx.exception))
        self.assertIn("dead: down", str(ctx.exception))
