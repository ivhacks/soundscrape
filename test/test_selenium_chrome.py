from unittest import TestCase

from stealth_driver import create_stealth_driver


class TestSeleniumAndChrome(TestCase):
    def test_selenium_and_chrome(self):
        driver = create_stealth_driver(headless=True)
        driver.get("https://soundcloud.com/")
