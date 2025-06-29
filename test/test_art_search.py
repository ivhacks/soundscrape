from unittest import TestCase

from art_search import search_cover_art_by_text
from art_util import same_images


class ArtSearchTests(TestCase):
    def test_knock2_feel_u_luv_me_single(self):
        with open("test/test_art/knock2_feel_u_luv_me.jpg", "rb") as f:
            expected = f.read()

        result = search_cover_art_by_text("knock2", "feel u luv me", album=False)

        self.assertTrue(same_images(expected, result))

    def test_knock2_feel_u_luv_me_album(self):
        with open("test/test_art/knock2_nolimit.jpg", "rb") as f:
            expected = f.read()

        result = search_cover_art_by_text("knock2", "feel u luv me", album=True)

        self.assertTrue(same_images(expected, result))
