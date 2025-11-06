from unittest import TestCase

import pytest

from stealth_driver import create_stealth_driver


@pytest.mark.xdist_group(name="selenium_chrome")
class TestSeleniumAndChrome(TestCase):
    def test_selenium_and_chrome(self):
        driver = create_stealth_driver(headless=True)
        driver.get("https://soundcloud.com/")
