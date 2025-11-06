import unittest

import pytest

from sevendigital_search import search_7digital
from stealth_driver import create_stealth_driver


HEADLESS = True


@pytest.mark.xdist_group(name="sevendigital_search")
class TestSevendigitalSearch(unittest.TestCase):
    driver = None

    @classmethod
    def setUpClass(cls):
        cls.driver = create_stealth_driver(HEADLESS)

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def test_knock2_jade(self):
        results = search_7digital("Knock2", "JADE", self.driver)
        found_urls = [result["url"] for result in results]
        self.assertIn(
            "https://us.7digital.com/artist/knock2/release/jade-45577393", found_urls
        )

    def test_martin_garrix_album_search(self):
        results = search_7digital("Martin Garrix", "Bylaw EP", self.driver)
        found_urls = [result["url"] for result in results]
        self.assertIn(
            "https://us.7digital.com/artist/martin-garrix/release/bylaw-ep-8536371",
            found_urls,
        )

    def test_charli_xcx_360_track(self):
        results = search_7digital("Charli XCX", "360", self.driver)
        found_urls = [result["url"] for result in results]
        self.assertIn(
            "https://us.7digital.com/artist/charli-xcx/release/360-44761123",
            found_urls,
        )

    def test_charli_xcx_brat_album(self):
        results = search_7digital("Charli XCX", "BRAT", self.driver)
        found_urls = [result["url"] for result in results]
        self.assertIn(
            "https://us.7digital.com/artist/charli-xcx/release/brat-explicit-42231205",
            found_urls,
        )

    def test_one_direction_little_white_lies(self):
        results = search_7digital("One Direction", "Little White Lies", self.driver)
        found_urls = [result["url"] for result in results]
        self.assertIn(
            "https://us.7digital.com/artist/one-direction-1/release/midnight-memories-deluxe-3081541",
            found_urls,
        )

    def test_martin_garrix_dont_look_down(self):
        results = search_7digital("Martin Garrix", "Don't Look Down", self.driver)
        found_urls = [result["url"] for result in results]
        self.assertIn(
            "https://us.7digital.com/artist/martin-garrix-feat-usher/release/dont-look-down-4265082",
            found_urls,
        )

    def test_rl_grime_ucla(self):
        results = search_7digital("RL Grime", "UCLA", self.driver)
        found_urls = [result["url"] for result in results]
        self.assertIn(
            "https://us.7digital.com/artist/rl-grime/release/nova-45573752", found_urls
        )
