from unittest import TestCase

from art_search import search_cover_art_by_text
from img_diff import image_difference


class ArtSearchTests(TestCase):
    def test_knock2_feel_u_luv_me_single(self):
        with open("test/test_art/knock2_feel_u_luv_me.jpg", "rb") as f:
            expected = f.read()

        result = search_cover_art_by_text("knock2", "feel u luv me", album=False)

        delta = image_difference(expected, result)
        self.assertLessEqual(delta, 2, f"Expected <= 2, got {delta}")

    def test_knock2_feel_u_luv_me_album(self):
        with open("test/test_art/knock2_nolimit.jpg", "rb") as f:
            expected = f.read()

        result = search_cover_art_by_text("knock2", "feel u luv me", album=True)

        delta = image_difference(expected, result)
        self.assertLessEqual(delta, 2, f"Expected <= 2, got {delta}")
