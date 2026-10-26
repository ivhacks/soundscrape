import re

import requests

from get_img_soundcloud import get_image_soundcloud


REQUEST_TIMEOUT = 20


def search_cover_art_soundcloud(artist: str, title: str) -> bytes:
    # the search page is server rendered, the first /user/track link is the top hit
    response = requests.get(
        "https://soundcloud.com/search/sounds",
        params={"q": f"{artist} {title}"},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()

    match = re.search(r'<li><h2><a href="(/[^"/]+/[^"/]+)">', response.text)
    if not match:
        raise ValueError(f"No SoundCloud track found for '{artist} {title}'")

    return get_image_soundcloud("https://soundcloud.com" + match.group(1))
