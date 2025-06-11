import unittest
from sevendigital_search import search_7digital


class TestSevendigitalSearch(unittest.TestCase):

    def _assert_url_in_results(self, search_term: str, expected_url: str):
        results = search_7digital(search_term)

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

    def test_knock2_jade(self):
        self._assert_url_in_results(
            "Knock2 - JADE",
            "https://us.7digital.com/artist/knock2/release/jade-45577393",
        )


if __name__ == "__main__":
    unittest.main() 