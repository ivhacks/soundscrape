from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import time


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


def search_7digital(artist: str, title: str) -> List[Dict]:
    """Search 7digital for tracks/albums, checking albums for specific tracks"""
    driver = None
    try:
        # Set up Chrome options with stealth settings
        chrome_options = Options()
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

    except Exception as e:
        print(f"Error searching 7digital: {e}")
        return []
    finally:
        if driver:
            driver.quit()


def search_artist_albums_for_track(driver, artist: str, title: str) -> List[Dict]:
    """Fallback search: search for artist only and check their albums for the track"""
    try:
        # Search for just the artist name
        search_url = f"https://us.7digital.com/search?q={quote_plus(artist)}"
        driver.get(search_url)

        # Wait for page load
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find all album links
        links = soup.find_all("a", href=True)
        artist_albums = []

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
                    artist_albums.append(
                        {"title": link_title, "url": full_url, "source": "7digital"}
                    )

        # Remove duplicates
        seen_urls = set()
        unique_artist_albums = []
        for album in artist_albums:
            if album["url"] not in seen_urls:
                seen_urls.add(album["url"])
                unique_artist_albums.append(album)

        # Check each album to see if it's actually by this artist and contains the track
        for album in unique_artist_albums:
            try:
                driver.get(album["url"])
                time.sleep(2)

                album_soup = BeautifulSoup(driver.page_source, "html.parser")

                # Check if this album is actually by the artist we're looking for
                # Look for artist name in the page
                page_text = album_soup.get_text().lower()
                artist_found = False

                # Look for artist links or mentions
                artist_links = album_soup.find_all("a", href=True)
                for artist_link in artist_links:
                    if "/artist/" in artist_link.get("href", ""):
                        artist_text = artist_link.get_text(strip=True)
                        if string_match(artist_text, artist):
                            artist_found = True
                            break

                # If we can't find artist links, check page text
                if not artist_found and artist.lower() in page_text:
                    artist_found = True

                # If this is the right artist, search for the track
                if artist_found:
                    if search_album_for_track(driver, album["url"], title):
                        return [album]

            except Exception:
                # Continue to next album if this one fails
                continue

        # No albums contained the track
        return []

    except Exception:
        return []
