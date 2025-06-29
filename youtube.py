import argparse
from dataclasses import dataclass
import os
from typing import List, Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from file_metadata import set_album_artist, set_album_title, set_artist, set_song_title


# Headless mode toggle - set to False to see the browser window
# Note: This is not used in the test suite, there's another toggle in test_yt_music_metadata.py
HEADLESS = True


@dataclass
class TrackMetadata:
    title: str
    artists: List[str]  # Changed from single artist to list
    featured_artists: List[str]  # New field for featured artists
    album: str
    year: int | None


def get_yt_music_metadata(
    link: str, driver: Optional[webdriver.Chrome] = None
) -> TrackMetadata:
    import re

    # XPaths for reliable element location
    TITLE_XPATH = "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[2]/yt-formatted-string"
    ARTIST_XPATH = "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[2]/span/span[2]/yt-formatted-string/a[1]"

    # Use provided driver or create a new one
    driver_created = driver is None
    if driver_created:
        chrome_options = Options()
        if HEADLESS:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument(
                "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        driver = webdriver.Chrome(options=chrome_options)

    driver.get(link)

    # Wait for content to load
    wait = WebDriverWait(driver, 20)
    wait.until(
        expected_conditions.presence_of_element_located((By.XPATH, ARTIST_XPATH))
    )

    # Get basic metadata
    title_element = driver.find_element(By.XPATH, TITLE_XPATH)
    raw_title = str(title_element.get_attribute("innerHTML")).strip()

    # Get all artist links to handle multiple main artists (like "deadmau5 & Kaskade")
    all_links = driver.find_elements(
        By.XPATH,
        "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[2]/span/span[2]/yt-formatted-string/a",
    )

    # Extract main artists - typically the first few links before the album
    raw_artists = []
    for artist_link in all_links[:-1]:  # Exclude last link (likely album)
        artist_name = str(artist_link.get_attribute("innerHTML")).strip()
        raw_artists.append(artist_name)

    # Get album (last link in the player bar)
    if len(all_links) >= 2:
        raw_album = str(all_links[-1].get_attribute("innerHTML")).strip()
    else:
        raw_album = raw_title

    # Get year (search all spans for 4-digit year)
    year = None
    all_spans = driver.find_elements(
        By.XPATH,
        "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[2]/span/span[2]/yt-formatted-string/span",
    )
    for span in all_spans:
        span_text = str(span.get_attribute("innerHTML")).strip()
        year_match = re.search(r"\b(\d{4})\b", span_text)
        if year_match:
            year = int(year_match.group(1))
            break

    if driver_created:
        driver.close()

    # Parse title and extract featured artists
    title, featured_artists, main_artist = _parse_title_and_featured(raw_title)

    # Determine artists based on whether we found featured artists in title
    if main_artist:
        # If we extracted artist from title (like "Artist ft. Featured - Song"), use that
        artists = [main_artist]
    elif featured_artists:
        # If we found featured artists in title, only use first link as main artist
        artists = [raw_artists[0]] if raw_artists else []
    else:
        # No featured artists found, so all links (except last) are likely main artists
        artists = raw_artists

    # Remove any artists from the main artists list if they appear in featured_artists
    if featured_artists:
        artists = [artist for artist in artists if artist not in featured_artists]

    # Fix album if it matches the raw title - use cleaned title instead
    if raw_album == raw_title:
        album = title
    else:
        album = raw_album

    return TrackMetadata(
        title=title,
        artists=artists,
        featured_artists=featured_artists,
        album=album,
        year=year,
    )


def _parse_title_and_featured(raw_title: str):
    """Clean title and extract featured artists with improved splitting"""
    import re

    title = raw_title
    featured_artists = []
    main_artist = None

    # Handle "Artist ft. Featured - Song Title" format first
    if " - " in title and re.search(r"\bft\.?\s", title, re.IGNORECASE):
        parts = title.split(" - ", 1)
        if len(parts) == 2:
            artist_part, title = parts[0].strip(), parts[1].strip()
            # Extract main artist and featured artists from the artist part
            feat_match = re.search(r"(.+?)\s+ft\.?\s+(.+)$", artist_part, re.IGNORECASE)
            if feat_match:
                main_artist = feat_match.group(1).strip()
                feat_text = feat_match.group(2).strip()

                # Split featured artists on commas, semicolons, and 'and'
                raw_artists = re.split(
                    r"[,;]|\s+and\s+", feat_text, flags=re.IGNORECASE
                )
                featured_artists = []
                for artist in raw_artists:
                    clean_artist = artist.strip()
                    if clean_artist:
                        featured_artists.append(clean_artist)

    # Remove common suffixes
    title = re.sub(r"\s*\(Official.*?\).*$", "", title, flags=re.IGNORECASE)
    title = re.sub(
        r"\s*\((?:Music|Lyric) Video.*?\).*$", "", title, flags=re.IGNORECASE
    )
    title = re.sub(r"\s*\(Audio\).*$", "", title, flags=re.IGNORECASE)

    # Extract featured artists from parentheses format if not already found
    if not featured_artists:
        feat_match = re.search(r"\((?:feat|ft)\.?\s*([^)]+)\)", title, re.IGNORECASE)
        if feat_match:
            feat_text = feat_match.group(1)

            # Split featured artists on commas, semicolons, and 'and'
            raw_artists = re.split(r"[,;]|\s+and\s+", feat_text, flags=re.IGNORECASE)
            featured_artists = []
            for artist in raw_artists:
                clean_artist = artist.strip()
                if clean_artist:
                    featured_artists.append(clean_artist)

    # Remove featuring info from title
    title = re.sub(r"\s*\((?:feat|ft)\.?[^)]+\)", "", title, flags=re.IGNORECASE)

    return title.strip(), featured_artists, main_artist


def process_link(link: str, cover_artwork: bool = False, music: bool = False):
    listdir_before = os.listdir()

    args = "--extract-audio "
    args += "--audio-format mp3 --audio-quality 256k"

    if cover_artwork:
        args += "--embed-thumbnail "

    os.system("youtube-dl" + " " + args + " " + link)

    listdir_after = os.listdir()
    newly_downloaded_file = None
    for file in listdir_after:
        if file not in listdir_before:
            newly_downloaded_file = file

    if newly_downloaded_file is None:
        raise Exception(f"Couldn't identify downloaded file for {link}")

    if music:
        metadata = get_yt_music_metadata(link)

        # Set metadata using our API
        set_song_title(newly_downloaded_file, metadata.title)
        set_artist(newly_downloaded_file, metadata.artists[0])
        set_album_artist(newly_downloaded_file, metadata.artists[0])
        set_album_title(newly_downloaded_file, metadata.album)
        # TODO: Add year support when metadata.year is available

        # Search from back to front for "." indicating file extension
        # Front to back doesn't work if the title contains e.g. "producer ft. vocalist"
        dot_position = newly_downloaded_file.rfind(".")
        file_extension = newly_downloaded_file[dot_position:]
        final_filename = metadata.title + file_extension

        # If a file with the destination name already exists, delete it
        if os.path.exists(final_filename):
            os.remove(final_filename)

        # Rename file to title of song but keep extension
        os.rename(newly_downloaded_file, final_filename)

    print("---------------------------------------------------")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "target",
        help="YouTube link or path of a file containing a list of YouTube links",
    )
    parser.add_argument(
        "-c",
        "--cover-artwork",
        help="Embed video thumbnail as cover artwork",
        action="store_true",
    )
    parser.add_argument(
        "-m",
        "--music",
        help="Treat this as a YouTube music link (rather than e.g. a music video) and get the title, artist, and year from the webpage.",
        action="store_true",
    )

    args = parser.parse_args()

    # Download songs to the temp folder
    os.chdir("./temp")

    # Check if the target is a URL or a file path
    is_http_url = args.target.startswith("http://")
    is_https_url = args.target.startswith("https://")
    is_www_url = args.target.startswith("www.")
    is_url = is_http_url or is_https_url or is_www_url

    if is_url:
        # URL
        process_link(args.target, args.cover_artwork, args.music)
    else:
        # Path to file containing list of links
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, args.target)
        with open(file_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            print(f"Downloading {line}", end="")
            process_link(line, args.cover_artwork, args.music)
