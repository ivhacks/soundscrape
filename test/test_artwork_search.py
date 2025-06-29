from unittest import TestCase

from artwork_search import search_cover_artwork_by_text
from artwork_util import same_images


class ArtworkSearchTests(TestCase):
    def test_knock2_feel_u_luv_me_single(self):
        with open("test/test_artwork/knock2_feel_u_luv_me.jpg", "rb") as f:
            expected = f.read()

        result = search_cover_artwork_by_text("knock2", "feel u luv me", album=False)

        self.assertTrue(same_images(expected, result))

    def test_knock2_feel_u_luv_me_album(self):
        with open("test/test_artwork/knock2_nolimit.jpg", "rb") as f:
            expected = f.read()

        result = search_cover_artwork_by_text("knock2", "feel u luv me", album=True)

        self.assertTrue(same_images(expected, result))
