import unittest

from beatport_search import search_beatport


class TestBeatportSearch(unittest.TestCase):
    def _assert_url_in_results(self, search_term: str, expected_url: str):
        results = search_beatport(search_term)

        self.assertGreater(len(results), 0, f"No results found for '{search_term}'")

        found_urls = [result["url"] for result in results]

        self.assertIn(
            expected_url,
            found_urls,
            f"Expected URL '{expected_url}' not found in results for '{search_term}'. "
            f"Found URLs: {found_urls}",
        )

    def test_knock2_feel_u_luv_me(self):
        self._assert_url_in_results(
            "knock2 - feel u luv me",
            "https://www.beatport.com/track/feel-u-luv-me/19431109",
        )

    def test_zedd_martin_garrix_follow(self):
        self._assert_url_in_results(
            "zedd, martin garrix - follow",
            "https://www.beatport.com/track/follow/16355909",
        )

    def test_rl_grime_bea_miller_slow_dive(self):
        self._assert_url_in_results(
            "rl grime, bea miller - slow dive",
            "https://www.beatport.com/track/slow-dive/18112497",
        )

    def test_zedd_clarity(self):
        self._assert_url_in_results(
            "zedd - clarity", "https://www.beatport.com/track/clarity/15726860"
        )


if __name__ == "__main__":
    unittest.main()
