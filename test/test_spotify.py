from unittest import TestCase

from spoti import get_art_url, get_token


class SpotifyTests(TestCase):
    token = None

    @classmethod
    def setUpClass(cls):
        cls.token = get_token()

    def test_hold_my_hand_album(self):
        # Don't get single art, should get album art for nolimit
        url = get_art_url(
            self.token, "hold my hand", "knock2", single=False, is_album=False
        )
        self.assertEqual(
            url, "https://i.scdn.co/image/ab67616d0000b2737b3e13a4e21a128c0d04c789"
        )

    def test_hold_my_hand_single(self):
        # Do get single art, should get hold my hand specific art
        url = get_art_url(
            self.token, "hold my hand", "knock2", single=True, is_album=False
        )
        self.assertEqual(
            url, "https://i.scdn.co/image/ab67616d0000b2731861d1d1e0617c1e2d563278"
        )

    def test_single_and_album(self):
        # It makes no sense to request the single art for an album, this should raise an exception
        with self.assertRaises(ValueError):
            get_art_url(
                self.token, "hold my hand", "knock2", single=True, is_album=True
            )

    def test_incorrect_album_title(self):
        # hold my hand is a song and not an album, so if we request an album called "hold my hand" it shouldn't work
        with self.assertRaises(ValueError):
            get_art_url(
                self.token, "hold my hand", "knock2", single=False, is_album=True
            )

    def test_lose_my_mind(self):
        # Format of the title is a little different on Spotify so this tests the fuzzy matching
        url = get_art_url(
            self.token,
            "Ryan Tedder, Sebastian Ingrosso, Alesso",
            "Calling (Lose My Mind) (Extended Club Mix)",
            single=False,
            is_album=True,
        )
        self.assertEqual(
            url, "https://i.scdn.co/image/ab67616d0000b273182bce790811337a5b37c8af"
        )

    def test_push(self):
        # Do get single art, should get hold my hand specific art
        url = get_art_url(
            self.token,
            "Push",
            "Hamdi, Taichu, OFFAIAH, Skrillex",
            single=True,
            is_album=False,
        )
        self.assertEqual(
            url, "https://i.scdn.co/image/ab67616d0000b273f239a45be61917fd61898241"
        )
