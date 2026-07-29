from unittest import TestCase

import pytest

from get_img_bandcamp import get_image_bandcamp
from get_img_facebook import get_image_facebook
from get_img_genius import get_image_genius
from get_img_instagram import get_image_instagram
from get_img_soundcloud import get_image_soundcloud
from get_img_threads import get_image_threads
from get_img_x import get_image_x
from img_diff import image_difference
from stealth_driver import create_stealth_driver


@pytest.mark.xdist_group(name="get_img")
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
            "https://soundcloud.com/knock2music/knock2-lauren-larue-nolimit-1"
        )

        with open("test/test_art/knock2_nolimit.jpg", "rb") as f:
            expected = f.read()
        self.assertLessEqual(image_difference(result, expected), 2)

    def test_bandcamp_beyond(self):
        result = get_image_bandcamp(
            "https://jousboxx.bandcamp.com/track/beyond-featuring-joelle-j"
        )

        with open("test/beyond.jpg", "rb") as f:
            expected = f.read()
        self.assertLessEqual(image_difference(result, expected), 2)

    def test_x_nolimit(self):
        result = get_image_x("https://x.com/Knock2Music/status/1867292451918295158")

        with open("test/test_art/knock2_nolimit.jpg", "rb") as f:
            expected = f.read()

        self.assertLessEqual(image_difference(result, expected), 2)

    def test_instagram_nolimit_post(self):
        # IG carousel/timing is flaky under parallel chrome load; retry real fetch
        with open("test/test_art/knock2_nolimit.jpg", "rb") as f:
            expected = f.read()
        last_diff = 999
        for _ in range(3):
            result = get_image_instagram("https://www.instagram.com/p/DDfmurKTFC5/")
            last_diff = image_difference(result, expected)
            if last_diff <= 2:
                break
        self.assertLessEqual(last_diff, 2)

    def test_facebook_nolimit_post(self):
        result = get_image_facebook(
            "https://www.facebook.com/photo.php?fbid=702833892070592&id=100070319619722&set=a.247825724238080",
            driver=self.driver,
        )

        with open("test/test_art/knock2_nolimit.jpg", "rb") as f:
            expected = f.read()
        self.assertLessEqual(image_difference(result, expected), 2)

    def test_genius_nolimit_album(self):
        result = get_image_genius("https://genius.com/albums/Knock2/Nolimit")

        with open("test/test_art/knock2_nolimit.jpg", "rb") as f:
            expected = f.read()
        self.assertLessEqual(image_difference(result, expected), 2)

    def test_genius_dance_or_dead_song(self):
        result = get_image_genius(
            "https://genius.com/Knock2-and-milli-dance-or-dead-lyrics"
        )

        with open("test/test_art/knock2_nolimit.jpg", "rb") as f:
            expected = f.read()
        self.assertLessEqual(image_difference(result, expected), 2)

    def test_threads_nolimit_post(self):
        result = get_image_threads(
            "https://www.threads.com/@coverartmatters/post/DFBRbWGRqjO",
            driver=self.driver,
        )

        with open("test/test_art/knock2_nolimit.jpg", "rb") as f:
            expected = f.read()
        self.assertLessEqual(image_difference(result, expected), 2)
