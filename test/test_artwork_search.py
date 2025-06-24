from unittest import TestCase
from PIL import Image
from artwork_util import same_images
from artwork import search_cover_artwork_by_text


class ArtworkSearchTests(TestCase):
    def test_knock2_feel_u_luv_me_single(self):
        image1 = Image.open("test/test_artwork/knock2_feel_u_luv_me.jpg")
        search_results = search_cover_artwork_by_text("knock2", "feel u luv me", album=False)
        self.assertGreater(len(search_results), 0)
        self.assertTrue(same_images(image1, search_results[0]))

    def test_knock2_feel_u_luv_me_album(self):
        image1 = Image.open("test/test_artwork/knock2_nolimit.jpg")
        search_results = search_cover_artwork_by_text("knock2", "feel u luv me", album=True)
        self.assertGreater(len(search_results), 0)
        self.assertTrue(same_images(image1, search_results[0]))
