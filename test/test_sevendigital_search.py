import unittest
from sevendigital_search import search_7digital


class TestSevendigitalSearch(unittest.TestCase):

    def _assert_url_in_results(self, artist: str, title: str, expected_url: str):
        results = search_7digital(artist, title)

        # Check that we got some results
        self.assertGreater(
            len(results), 0, f"No results found for '{artist} - {title}'"
        )

        # Extract all URLs from results
        found_urls = [result["url"] for result in results]

        # Check that the expected URL is in the results
        self.assertIn(
            expected_url,
            found_urls,
            f"Expected URL '{expected_url}' not found in results for '{artist} - {title}'. "
            f"Found URLs: {found_urls}",
        )

    def test_knock2_jade(self):
        self._assert_url_in_results(
            "Knock2",
            "JADE",
            "https://us.7digital.com/artist/knock2/release/jade-45577393",
        )

    def test_martin_garrix_album_search(self):
        """Test that searching for an album returns the album when found"""
        self._assert_url_in_results(
            "Martin Garrix",
            "Bylaw EP",
            "https://us.7digital.com/artist/martin-garrix/release/bylaw-ep-8536371",
        )

    def test_charli_xcx_360_track(self):
        """Test searching for a track within an album (360 from BRAT)"""
        self._assert_url_in_results(
            "Charli XCX",
            "360",
            "https://us.7digital.com/artist/charli-xcx/release/brat-explicit-42231205",
        )

    def test_charli_xcx_brat_album(self):
        """Test searching for an album directly (BRAT album)"""
        self._assert_url_in_results(
            "Charli XCX",
            "BRAT",
            "https://us.7digital.com/artist/charli-xcx/release/brat-explicit-42231205",
        )

    def test_one_direction_little_white_lies(self):
        """Test fallback search when initial search returns no results"""
        self._assert_url_in_results(
            "One Direction",
            "Little White Lies",
            "https://us.7digital.com/artist/one-direction-1/release/midnight-memories-deluxe-3081541",
        )

    def test_martin_garrix_dont_look_down(self):
        """Test fallback search for a single track that doesn't appear in initial search"""
        self._assert_url_in_results(
            "Martin Garrix",
            "Don't Look Down",
            "https://us.7digital.com/artist/martin-garrix-feat-usher/release/dont-look-down-4265082",
        )


if __name__ == "__main__":
    unittest.main()
