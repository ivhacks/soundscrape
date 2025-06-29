from unittest import TestCase

from spoti import get_cover_artwork_url, get_token


class SpotifyTests(TestCase):
    token = None

    @classmethod
    def setUpClass(cls):
        cls.token = get_token()

    def test_hold_my_hand_album(self):
        # Don't get single artwork, should get album artwork for nolimit
        url = get_cover_artwork_url(
            self.token, "hold my hand", "knock2", single=False, is_album=False
        )
        self.assertEqual(
            url, "https://i.scdn.co/image/ab67616d0000b2737b3e13a4e21a128c0d04c789"
        )

    def test_hold_my_hand_single(self):
        # Do get single artwork, should get hold my hand specific artwork
        url = get_cover_artwork_url(
            self.token, "hold my hand", "knock2", single=True, is_album=False
        )
        self.assertEqual(
            url, "https://i.scdn.co/image/ab67616d0000b2731861d1d1e0617c1e2d563278"
        )

    def test_single_and_album(self):
        # It makes no sense to request the single artwork for an album, this should raise an exception
        with self.assertRaises(ValueError):
            get_cover_artwork_url(
                self.token, "hold my hand", "knock2", single=True, is_album=True
            )

    def test_incorrect_album_title(self):
        # hold my hand is a song and not an album, so if we request an album called "hold my hand" it shouldn't work
        with self.assertRaises(ValueError):
            get_cover_artwork_url(
                self.token, "hold my hand", "knock2", single=False, is_album=True
            )
