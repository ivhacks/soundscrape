# This file is exclusively meant for AI agent use, as humans can just use a browser
# Raw HTML of a site is often massive, overwhelms the AI's context, and is mostly noise.
# Here, we define bespoke functionality for sites we care about to help the AI see what it's working with

import sys
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support.ui import WebDriverWait

from stealth_driver import create_stealth_driver


def _normalize_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    parsed = urlparse(url)
    site = parsed.netloc
    path = parsed.path
    query = parsed.query

    if site.startswith("www."):
        site = site[4:]

    result = site
    if path:
        result += path
    if query:
        result += "?" + query

    return result


def _strip_unneeded_elements(soup):
    for style in soup.find_all("style"):
        style.decompose()
    for script in soup.find_all("script"):
        script.decompose()
    for link in soup.find_all("link"):
        link.decompose()
    for noscript in soup.find_all("noscript"):
        noscript.decompose()

    return soup


def _strip_youtube_noise(head):
    noise_patterns = [
        ("name", "twitter:app:name:iphone"),
        ("name", "twitter:app:id:iphone"),
        ("name", "twitter:app:url:iphone"),
        ("name", "twitter:app:name:ipad"),
        ("name", "twitter:app:id:ipad"),
        ("name", "twitter:app:url:ipad"),
        ("name", "twitter:app:name:googleplay"),
        ("name", "twitter:app:id:googleplay"),
        ("name", "twitter:app:url:googleplay"),
        ("name", "apple-itunes-app"),
        ("name", "viewport"),
        ("name", "twitter:card"),
        ("name", "twitter:site"),
        ("name", "twitter:url"),
        ("name", "twitter:image"),
        ("property", "al:ios:app_store_id"),
        ("property", "al:ios:app_name"),
        ("property", "al:ios:url"),
        ("property", "al:android:url"),
        ("property", "al:android:app_name"),
        ("property", "al:android:package"),
        ("property", "al:web:should_fallback"),
        ("property", "fb:app_id"),
        ("property", "og:image:width"),
        ("property", "og:image:height"),
        ("property", "og:site_name"),
        ("property", "og:type"),
        ("property", "og:url"),
        ("property", "og:image"),
    ]

    for attr, value in noise_patterns:
        for meta in head.find_all("meta", {attr: value}):
            meta.decompose()

    for title in head.find_all("title"):
        if not title.get_text().strip() or "deprecated" in title.get_text().lower():
            title.decompose()

    return head


def view_link(url):
    normalized = _normalize_url(url)
    base = normalized.split("/")[0]

    if "music.youtube.com" in base:
        # Proper JS rendered YouTube music is like 4K lines
        # Using the no-JS version for now and seeing how it goes
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        head = _strip_unneeded_elements(soup.head)
        head = _strip_youtube_noise(head)
        return_string = head.prettify().strip()
        return_string += "\n\nNOTE TO AI: This isn't the real page.\n"
        return_string += (
            "The actual page rendered with JavaScript is thousands of lines.\n"
        )
        return_string += "You're getting the no-JS version for brevity. Song info should be the same.\n"

        return return_string

    elif "beatport.com" in base:
        # Proper JS rendered YouTube music is like 4K lines
        # Using the no-JS version for now and seeing how it goes
        driver = create_stealth_driver()
        driver.get(url)
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        html = driver.page_source
        driver.quit()
        soup = BeautifulSoup(html, "html.parser")

        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        head = _strip_unneeded_elements(soup.head)

        return head.prettify().strip()

    elif "bandcamp.com" in base:
        print(f"bandcamp: {url}")

    elif "soundcloud.com" in base:
        print(f"soundcloud: {url}")

    else:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.prettify().strip()


if __name__ == "__main__":
    print(view_link(sys.argv[1]))
