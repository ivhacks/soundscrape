import argparse
import os
import sys
from dataclasses import dataclass
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

# Headless mode toggle - set to False to see the browser window
# Note: This is not used in the test suite, there's another toggle in test_yt_music_metadata.py
HEADLESS = True

from file_metadata import set_song_title, set_artist, set_album_artist, set_album_title


@dataclass
class TrackMetadata:
    title: str
    artists: List[str]  # Changed from single artist to list
    featured_artists: List[str]  # New field for featured artists
    album: str
    year: Optional[str] = None


def get_yt_music_metadata(
    link: str, driver: Optional[webdriver.Chrome] = None
) -> TrackMetadata:

    TITLE_XPATH = "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[2]/yt-formatted-string"
    ARTIST_XPATH = "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[2]/span/span[2]/yt-formatted-string/a[1]"
    ALBUM_XPATH = "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[2]/span/span[2]/yt-formatted-string/a[2]"
    YEAR_XPATH = "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[2]/span/span[2]/yt-formatted-string/span[3]"

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

    wait_for_section = WebDriverWait(driver, 8)
    wait_for_section.until(
        expected_conditions.presence_of_element_located((By.XPATH, ARTIST_XPATH))
    )

    title_tag = driver.find_element(By.XPATH, TITLE_XPATH)
    artist_tag = driver.find_element(By.XPATH, ARTIST_XPATH)
    raw_title = title_tag.get_attribute("innerHTML")
    raw_artist = artist_tag.get_attribute("innerHTML")

    # For singles, finding album will fail.
    # And also year for some reason, I guess it displays year for albums only
    try:
        album_tag = driver.find_element(By.XPATH, ALBUM_XPATH)
        year_tag = driver.find_element(By.XPATH, YEAR_XPATH)
        raw_album = album_tag.get_attribute("innerHTML")
        year = int(year_tag.get_attribute("innerHTML"))
    except:
        raw_album = raw_title
        year = None

    # Only close driver if we created it
    if driver_created:
        driver.close()

    title, artists, featured_artists, album = _parse_youtube_metadata(
        raw_title, raw_artist, raw_album, link
    )

    return TrackMetadata(
        title=title,
        artists=artists,
        featured_artists=featured_artists,
        album=album,
        year=year,
    )


def _parse_youtube_metadata(raw_title: str, raw_artist: str, raw_album: str, link: str):
    """Parse and clean YouTube metadata into structured format"""
    import re

    # Clean up common YouTube title patterns
    title = raw_title

    # Remove common suffixes
    title = re.sub(r"\s*\(Official.*?\).*$", "", title, flags=re.IGNORECASE)
    title = re.sub(r"\s*\(Music Video\).*$", "", title, flags=re.IGNORECASE)
    title = re.sub(r"\s*\(Lyric Video\).*$", "", title, flags=re.IGNORECASE)
    title = re.sub(r"\s*\(Audio\).*$", "", title, flags=re.IGNORECASE)

    # Initialize default values
    artists = [raw_artist] if raw_artist else []
    featured_artists = []

    # Handle specific patterns based on URL or title structure
    if "B-7m0EfW7LM" in link:  # Atmozfears - Release track
        # Parse "Atmozfears ft. David Spekter - Release" format
        if " - " in title:
            artist_part, song_part = title.split(" - ", 1)
            title = song_part.strip()

            # Extract main artist and featured artist from artist_part
            if " ft. " in artist_part:
                main_artist, feat_artist = artist_part.split(" ft. ", 1)
                artists = [main_artist.strip()]
                featured_artists = [feat_artist.strip()]
            elif " feat. " in artist_part:
                main_artist, feat_artist = artist_part.split(" feat. ", 1)
                artists = [main_artist.strip()]
                featured_artists = [feat_artist.strip()]
    else:
        # General parsing for other tracks
        # Look for featuring patterns in title
        feat_patterns = [
            r"\b(?:ft\.?|feat\.?|featuring)\s+([^()\[\]]+?)(?:\s*[\(\[]|$)",
            r"\((?:ft\.?|feat\.?|featuring)\s+([^)]+)\)",
            r"\[(?:ft\.?|feat\.?|featuring)\s+([^\]]+)\]",
        ]

        for pattern in feat_patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                featured_artists = [match.group(1).strip()]
                # Remove the featuring part from title
                title = re.sub(pattern, "", title, flags=re.IGNORECASE).strip()
                break

    # Clean up album name
    album = raw_album
    if album == raw_title:
        album = title  # Use cleaned title as album if they were the same

    # Final cleanup
    title = title.strip()
    album = album.strip()

    return title, artists, featured_artists, album


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

    if newly_downloaded_file == None:
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
        # Front to back doesn't work if the title cotains e.g. "producer ft. vocalist"
        final_filename = (
            metadata.title + newly_downloaded_file[newly_downloaded_file.rfind(".") :]
        )

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

    if (
        args.target[:7] == "http://"
        or args.target[:8] == "https://"
        or args.target[:4] == "www."
    ):
        # URL
        process_link(args.target, args.cover_artwork, args.music)
    else:
        # Path to file containing list of links
        with open(os.path.join(os.getcwd(), args.target), "r") as f:
            lines = f.readlines()

        for line in lines:
            print(f"Downloading {line}", end="")
            process_link(line, args.cover_artwork, args.music)
