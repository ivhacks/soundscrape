import json
from unittest import TestCase

from spoti import format_compact, get_art_url, get_token, tool_search_spotify


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
        url = get_art_url(
            self.token,
            "Calling (Lose My Mind)",
            "Sebastian Ingrosso, Alesso, Ryan Tedder",
            single=True,
            is_album=False,
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

    def test_cli_search_title_only(self):
        results = tool_search_spotify(self.token, title="shelter")

        self.assertGreater(len(results), 0)

        first_result = results[0]
        self.assertIn("name", first_result)
        self.assertIn("id", first_result)
        self.assertIn("artists", first_result)
        self.assertIn("album", first_result)

    def test_cli_search_artist_only(self):
        results = tool_search_spotify(self.token, artist="seven lions")

        self.assertGreater(len(results), 0)

        first_result = results[0]
        self.assertIn("name", first_result)
        self.assertIn("id", first_result)
        self.assertEqual(first_result["id"], "6fcTRFpz0yH79qSKfof7lp")

    def test_cli_search_album_only(self):
        results = tool_search_spotify(self.token, album="worlds")

        self.assertGreater(len(results), 0)

        first_result = results[0]
        self.assertIn("name", first_result)
        self.assertIn("id", first_result)
        self.assertIn("artists", first_result)
        self.assertEqual(first_result["name"], "Worlds")

    def test_cli_search_title_and_artist(self):
        results = tool_search_spotify(self.token, title="higher love", artist="jason ross")

        self.assertGreater(len(results), 0)

        first_result = results[0]
        self.assertIn("name", first_result)
        self.assertIn("id", first_result)
        self.assertIn("artists", first_result)
        self.assertIn("album", first_result)
        self.assertIn("higher", first_result["name"].lower())

    def test_cli_search_title_and_album(self):
        results = tool_search_spotify(self.token, title="fellow feeling", album="worlds")

        self.assertGreater(len(results), 0)

        first_result = results[0]
        self.assertIn("name", first_result)
        self.assertIn("id", first_result)
        self.assertIn("artists", first_result)
        self.assertIn("album", first_result)
        self.assertEqual(first_result["name"], "Fellow Feeling")
        self.assertEqual(first_result["id"], "2JgbGCxtzRp6wL5H1DgxV7")

    def test_cli_search_artist_and_album(self):
        results = tool_search_spotify(self.token, artist="illenium", album="ascend")

        self.assertGreater(len(results), 0)

        first_result = results[0]
        self.assertIn("name", first_result)
        self.assertIn("id", first_result)
        self.assertIn("artists", first_result)
        self.assertEqual(first_result["name"], "ASCEND")
        self.assertEqual(first_result["id"], "60xcVwuQJAOyu11xf9mObS")

    def test_cli_search_all_params(self):
        results = tool_search_spotify(
            self.token, artist="madeon", title="finale", album="adventure"
        )

        self.assertGreater(len(results), 0)

        first_result = results[0]
        self.assertIn("name", first_result)
        self.assertIn("id", first_result)
        self.assertIn("artists", first_result)
        self.assertIn("album", first_result)
        self.assertIn("finale", first_result["name"].lower())

        artist_names = [artist["name"].lower() for artist in first_result["artists"]]
        self.assertTrue(any("madeon" in name for name in artist_names))

    def test_compact_output(self):
        results = tool_search_spotify(self.token, artist="illenium", album="ascend")

        compact_output = format_compact(results)
        json_output = json.dumps(results, indent=2)

        self.assertLess(len(compact_output), len(json_output))
        self.assertIn("ID:", compact_output)
        self.assertIn("Name:", compact_output)
        self.assertIn("ASCEND", compact_output)
