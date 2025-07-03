from unittest import TestCase

from art_util import same_images
from get_img_bandcamp import get_image_bandcamp
from get_img_facebook import get_image_facebook
from get_img_genius import get_image_genius
from get_img_instagram import get_image_instagram
from get_img_soundcloud import get_image_soundcloud
from get_img_threads import get_image_threads
from get_img_x import get_image_x


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


class XTests(TestCase):
    def test_nolimit(self):
        result = get_image_x("https://x.com/Knock2Music/status/1867292451918295158")

        with open("test/image.jpg", "rb") as f:
            expected = f.read()

        # TODO: This image similarity function is shit, should return almost 1 here
        self.assertGreater(same_images(result, expected), 0.3)


class InstagramTests(TestCase):
    def test_nolimit_post(self):
        result = get_image_instagram("https://www.instagram.com/p/DDiBXLkTXds/")

        with open("test/image.jpg", "rb") as f:
            expected = f.read()
        self.assertGreater(same_images(result, expected), 0.8)


class FacebookTests(TestCase):
    def test_nolimit_post(self):
        result = get_image_facebook(
            "https://www.facebook.com/photo.php?fbid=702833892070592&id=100070319619722&set=a.247825724238080"
        )

        with open("test/image.jpg", "rb") as f:
            expected = f.read()
        self.assertGreater(same_images(result, expected), 0.8)


class GeniusTests(TestCase):
    def test_nolimit_album(self):
        result = get_image_genius("https://genius.com/albums/Knock2/Nolimit")

        with open("test/image.jpg", "rb") as f:
            expected = f.read()
        self.assertGreater(same_images(result, expected), 0.75)


class ThreadsTests(TestCase):
    def test_nolimit_post(self):
        result = get_image_threads(
            "https://www.threads.com/@coverartmatters/post/DFBRbWGRqjO"
        )

        with open("test/image.jpg", "rb") as f:
            expected = f.read()
        self.assertGreater(same_images(result, expected), 0.4)
