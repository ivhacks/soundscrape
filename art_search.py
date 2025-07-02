from io import BytesIO
from typing import List

from PIL import Image
import requests

from spoti import get_cover_art_url, get_token


MAX_NUM_THUMBNAILS = 5


def search_cover_art_by_text(artist: str, title: str, album: bool = False) -> bytes:
    token = get_token()

    if album:
        art_url = get_cover_art_url(token, title, artist, single=False, is_album=False)
    else:
        art_url = get_cover_art_url(token, title, artist, single=True, is_album=False)

    response = requests.get(art_url)
    response.raise_for_status()

    return response.content


def search_cover_art_by_text_musicbrainz(
    artist: str, title: str, album: bool = False
) -> List[Image.Image]:
    # MusicBrainz requires a User-Agent header
    headers = {"User-Agent": "soundscrape/1.0 (https://github.com/user/soundscrape)"}

    # Build search query for MusicBrainz
    if album:
        # Search for album releases
        query = f'artist:"{artist}" AND release:"{title}"'
    else:
        # Search for any release containing the track
        query = f'artist:"{artist}" AND recording:"{title}"'

    # Search MusicBrainz for releases
    mb_url = "https://musicbrainz.org/ws/2/release"
    params = {
        "query": query,
        "fmt": "json",
        "limit": 25,  # Get more results to increase chances of finding cover art
    }

    try:
        response = requests.get(mb_url, params=params, headers=headers)
        response.raise_for_status()
        releases = response.json().get("releases", [])
    except OSError:
        return []

    cover_images = []

    # Try to get cover art for each release
    for release in releases:
        if len(cover_images) >= MAX_NUM_THUMBNAILS:
            break

        mbid = release.get("id")
        if not mbid:
            continue

        # Try Cover Art Archive
        caa_url = f"https://coverartarchive.org/release/{mbid}"

        try:
            caa_response = requests.get(caa_url, headers=headers)
            caa_response.raise_for_status()
            art_data = caa_response.json()

            # Get the front cover image, or first image if no front cover
            images = art_data.get("images", [])
            if not images:
                continue

            # Prefer front cover
            front_cover = None
            for img in images:
                if img.get("front", False):
                    front_cover = img
                    break

            # Use front cover if found, otherwise use first image
            selected_image = front_cover if front_cover else images[0]
            image_url = selected_image.get("image")

            if image_url:
                # Download the image
                img_response = requests.get(image_url, headers=headers)
                img_response.raise_for_status()

                # Convert to PIL Image
                img = Image.open(BytesIO(img_response.content))
                cover_images.append(img)

        except OSError:
            # Cover art not available for this release, continue to next
            continue

    return cover_images
