import re
import time
from typing import Dict, List
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def create_driver(headless: bool = False) -> webdriver.Chrome:
    # Set up Chrome options with stealth settings
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    # Additional stealth options
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Set Chrome binary location on macOS
    chrome_options.binary_location = (
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    )

    # Create driver with webdriver-manager - fix path issue
    chromedriver_path = ChromeDriverManager().install()

    # Fix the path if webdriver-manager returns wrong file
    if chromedriver_path.endswith("THIRD_PARTY_NOTICES.chromedriver"):
        chromedriver_path = chromedriver_path.replace(
            "THIRD_PARTY_NOTICES.chromedriver", "chromedriver"
        )

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)

    # Hide webdriver property to avoid detection
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver


def string_match(a: str, b: str) -> bool:
    def process_string(s: str) -> str:
        s = s.lower()
        s = s.strip()
        s = re.sub(r"[^a-z0-9\s]", " ", s)
        s = s.replace("explicit", "")
        s = re.sub(r"\s+", " ", s)
        s = s.strip()
        return s

    processed_a = process_string(a)
    processed_b = process_string(b)

    return processed_a == processed_b


def search_album_for_track(driver, album_url: str, track_title: str) -> bool:
    """Search within an album page for a specific track title"""
    try:
        driver.get(album_url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Look for track listings on the album page
        track_elements = soup.find_all(["span", "div", "a"], string=True)

        for element in track_elements:
            element_text = element.get_text(strip=True)
            if element_text and string_match(element_text, track_title):
                return True

        return False
    except Exception:
        return False


def search_7digital(artist: str, title: str, driver=None) -> List[Dict]:
    """Search 7digital for tracks/albums, checking albums for specific tracks"""
    if driver is None:
        driver = create_driver()

    # Navigate to search page with combined query
    query = f"{artist} {title}"
    search_url = f"https://us.7digital.com/search?q={quote_plus(query)}"
    driver.get(search_url)

    # Wait for page to load and bot protection to complete with longer timeout
    try:
        WebDriverWait(driver, 30).until(
            lambda d: "Client Challenge" not in d.page_source
        )
    except Exception:
        # If timeout, try clicking somewhere on the page to trigger challenge completion
        try:
            driver.execute_script("document.body.click()")
            time.sleep(5)
            # Continue anyway - sometimes the page works even after timeout
        except:
            pass

    # Give it a bit more time to fully load the search results
    time.sleep(3)

    # Parse the page content
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Separate albums and tracks from results
    albums = []
    tracks = []

    links = soup.find_all("a", href=True)

    for link in links:
        href = link.get("href", "")
        if any(path in href for path in ["/artist/", "/album/", "/track/"]):
            if href.startswith("/"):
                full_url = f"https://us.7digital.com{href}"
            else:
                full_url = href

            # Remove query parameters
            if "?" in full_url:
                full_url = full_url.split("?")[0]

            link_title = link.get_text(strip=True)
            if link_title and len(link_title) > 0:
                result = {
                    "title": link_title,
                    "url": full_url,
                    "source": "7digital",
                }

                # Categorize as album or track based on URL pattern
                if "/release/" in full_url:
                    albums.append(result)
                else:
                    tracks.append(result)

    # Remove duplicates from albums
    seen_album_urls = set()
    unique_albums = []
    for album in albums:
        if album["url"] not in seen_album_urls:
            seen_album_urls.add(album["url"])
            unique_albums.append(album)

    # Check if any album title matches the search title (user searching for album)
    for album in unique_albums:
        if string_match(album["title"], title):
            return [album]

    # Search top 3 albums for the track
    for album in unique_albums[:3]:
        if search_album_for_track(driver, album["url"], title):
            return [album]

    # If no album contains the track, return track results or any results
    if tracks:
        return tracks[:10]
    elif unique_albums:
        return unique_albums[:10]
    else:
        # Fallback: No results found, search for artist only
        return search_artist_albums_for_track(driver, artist, title)


def search_artist_albums_for_track(driver, artist: str, title: str) -> List[Dict]:
    """Fallback search: search for artist only and check their albums and singles for the track"""
    try:
        # Search for just the artist name
        search_url = f"https://us.7digital.com/search?q={quote_plus(artist)}"
        driver.get(search_url)

        # Wait for page load
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find all release links and categorize them
        links = soup.find_all("a", href=True)
        albums = []
        singles = []

        for link in links:
            href = link.get("href", "")
            if "/release/" in href:
                if href.startswith("/"):
                    full_url = f"https://us.7digital.com{href}"
                else:
                    full_url = href

                # Remove query parameters
                if "?" in full_url:
                    full_url = full_url.split("?")[0]

                link_title = link.get_text(strip=True)
                if link_title and len(link_title) > 0:
                    release = {
                        "title": link_title,
                        "url": full_url,
                        "source": "7digital",
                    }

                    # Categorize as single or album based on title patterns
                    title_lower = link_title.lower()
                    is_single = any(
                        keyword in title_lower
                        for keyword in [
                            "single",
                            "- single",
                            "ep",
                            "- ep",
                            "remix",
                            "- remix",
                            "feat.",
                            "feat ",
                            "vs.",
                            "vs ",
                            "ft.",
                            "ft ",
                        ]
                    )

                    if is_single:
                        singles.append(release)
                    else:
                        albums.append(release)

        # Remove duplicates from both lists
        albums = remove_duplicates(albums)
        singles = remove_duplicates(singles)

        # Alternate between albums and singles: album1, single1, album2, single2, etc.
        max_items = max(len(albums), len(singles))

        for i in range(max_items):
            # Check album at index i
            if i < len(albums):
                if check_release_for_track(driver, albums[i], artist, title):
                    return [albums[i]]

            # Check single at index i
            if i < len(singles):
                if check_release_for_track(driver, singles[i], artist, title):
                    return [singles[i]]

        # No releases contained the track
        return []

    except Exception:
        return []


def remove_duplicates(releases: List[Dict]) -> List[Dict]:
    """Remove duplicate releases based on URL"""
    seen_urls = set()
    unique_releases = []
    for release in releases:
        if release["url"] not in seen_urls:
            seen_urls.add(release["url"])
            unique_releases.append(release)
    return unique_releases


def check_release_for_track(driver, release: Dict, artist: str, title: str) -> bool:
    """Check if a release (album or single) is by the artist and contains the track"""
    try:
        driver.get(release["url"])
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Check if this release is actually by the artist we're looking for
        artist_found = False

        # Look for artist links or mentions
        artist_links = soup.find_all("a", href=True)
        for artist_link in artist_links:
            if "/artist/" in artist_link.get("href", ""):
                artist_text = artist_link.get_text(strip=True)
                if string_match(artist_text, artist):
                    artist_found = True
                    break

        # If we can't find artist links, check page text
        if not artist_found:
            page_text = soup.get_text().lower()
            if artist.lower() in page_text:
                artist_found = True

        # If this is the right artist, check for the track
        if artist_found:
            # For singles, check if the release title matches the track title
            if string_match(release["title"], title):
                return True

            # For albums (or if title doesn't match), search within the release for the track
            return search_album_for_track(driver, release["url"], title)

    except Exception:
        return False

    return False
