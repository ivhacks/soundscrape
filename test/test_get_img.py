from unittest import TestCase

from art_util import same_images
from get_img_bandcamp import get_image_bandcamp
from get_img_soundcloud import get_image_soundcloud


class SoundcloudTests(TestCase):
    def test_nolimit(self):
        result = get_image_soundcloud(
            "https://soundcloud.com/knock2music/knock2-lauren-larue-nolimit-1"
        )

        with open("test/image.jpg", "rb") as f:
            expected = f.read()
        self.assertGreater(same_images(result, expected), 0.8)


class BandcampTests(TestCase):
    def test_beyond(self):
        result = get_image_bandcamp(
            "https://jousboxx.bandcamp.com/track/beyond-featuring-joelle-j"
        )

        with open("test/beyond.jpg", "rb") as f:
            expected = f.read()
        self.assertGreater(same_images(result, expected), 0.8)
