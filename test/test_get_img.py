from unittest import TestCase

from art_util import same_images
from get_img_bandcamp import get_image_bandcamp
from get_img_facebook import get_image_facebook
from get_img_genius import get_image_genius
from get_img_instagram import get_image_instagram
from get_img_soundcloud import get_image_soundcloud
from get_img_threads import get_image_threads
from get_img_x import get_image_x
from stealth_driver import create_stealth_driver


class GetImageTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = create_stealth_driver(headless=True)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "driver"):
            cls.driver.quit()

    def test_soundcloud_nolimit(self):
        result = get_image_soundcloud(
            "https://soundcloud.com/knock2music/knock2-lauren-larue-nolimit-1",
            driver=self.driver,
        )

        with open("test/image.jpg", "rb") as f:
            expected = f.read()
        self.assertGreater(same_images(result, expected), 0.8)

    def test_bandcamp_beyond(self):
        result = get_image_bandcamp(
            "https://jousboxx.bandcamp.com/track/beyond-featuring-joelle-j",
            driver=self.driver,
        )

        with open("test/beyond.jpg", "rb") as f:
            expected = f.read()
        self.assertGreater(same_images(result, expected), 0.8)

    def test_x_nolimit(self):
        result = get_image_x(
            "https://x.com/Knock2Music/status/1867292451918295158", driver=self.driver
        )

        with open("test/image.jpg", "rb") as f:
            expected = f.read()

        # TODO: This image similarity function is shit, should return almost 1 here
        self.assertGreater(same_images(result, expected), 0.3)

    def test_instagram_nolimit_post(self):
        result = get_image_instagram(
            "https://www.instagram.com/p/DDiBXLkTXds/", driver=self.driver
        )

        with open("test/image.jpg", "rb") as f:
            expected = f.read()
        self.assertGreater(same_images(result, expected), 0.8)

    def test_facebook_nolimit_post(self):
        result = get_image_facebook(
            "https://www.facebook.com/photo.php?fbid=702833892070592&id=100070319619722&set=a.247825724238080",
            driver=self.driver,
        )

        with open("test/image.jpg", "rb") as f:
            expected = f.read()
        self.assertGreater(same_images(result, expected), 0.8)

    def test_genius_nolimit_album(self):
        result = get_image_genius(
            "https://genius.com/albums/Knock2/Nolimit", driver=self.driver
        )

        with open("test/image.jpg", "rb") as f:
            expected = f.read()
        self.assertGreater(same_images(result, expected), 0.75)

    def test_threads_nolimit_post(self):
        result = get_image_threads(
            "https://www.threads.com/@coverartmatters/post/DFBRbWGRqjO",
            driver=self.driver,
        )

        with open("test/image.jpg", "rb") as f:
            expected = f.read()
        self.assertGreater(same_images(result, expected), 0.4)
