from unittest import TestCase

import pytest

from art_search import search_cover_art_by_text
from img_diff import image_difference


@pytest.mark.xdist_group(name="art_search")
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

    def test_jason_ross_one_more_day_single_path(self):
        # regression: lone file should use single path with track title.
        # festival album tag "EDC Las Vegas 2021" must not be the search query.
        result = search_cover_art_by_text(
            "Jason Ross, Blanke, Chandler Leighton",
            "One More Day",
            album=False,
        )
        self.assertGreater(len(result), 1000)

        with self.assertRaises(ValueError):
            search_cover_art_by_text(
                "Jason Ross, Blanke, Chandler Leighton",
                "EDC Las Vegas 2021",
                album=False,
            )
