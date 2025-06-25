import unittest
from bandcamp_search import search_bandcamp


class TestBandcampSearch(unittest.TestCase):

    def _assert_url_in_results(self, search_term: str, expected_url: str):
        results = search_bandcamp(search_term)

        # Check that we got some results
        self.assertGreater(len(results), 0, f"No results found for '{search_term}'")

        # Extract all URLs from results
        found_urls = [result["url"] for result in results]

        # Check that the expected URL is in the results
        self.assertIn(
            expected_url,
            found_urls,
            f"Expected URL '{expected_url}' not found in results for '{search_term}'. "
            f"Found URLs: {found_urls}",
        )

    def test_carbon_based_lifeforms_derelicts(self):
        self._assert_url_in_results(
            "Carbon Based Lifeforms - Derelicts",
            "https://carbonbasedlifeforms.bandcamp.com/track/derelicts",
        )

    def test_jousboxx_springtime(self):
        self._assert_url_in_results(
            "Jousboxx - Springtime", "https://jousboxx.bandcamp.com/track/springtime"
        )

    def test_au5_cataclysm(self):
        self._assert_url_in_results(
            "Au5 - Cataclysm", "https://au5music.bandcamp.com/track/cataclysm"
        )

    def test_second_flight_instead_of_one(self):
        self._assert_url_in_results(
            "Second Flight - Instead of one",
            "https://secondflight.bandcamp.com/track/instead-of-one",
        )


if __name__ == "__main__":
    unittest.main()
