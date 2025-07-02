from unittest import TestCase

from art_util import same_images
from get_img_soundcloud import get_image_soundcloud


class SoundcloudTests(TestCase):
    def test_nolimit(self):
        result = get_image_soundcloud(
            "https://soundcloud.com/knock2music/knock2-lauren-larue-nolimit-1"
        )

        with open("test/image.jpg", "rb") as f:
            expected = f.read()
        self.assertTrue(same_images(result, expected))
