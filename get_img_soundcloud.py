import re

import requests


REQUEST_TIMEOUT = 20


def get_image_soundcloud(link: str) -> bytes:
    response = requests.get(link, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    # [^"] keeps the match inside one attribute, m.soundcloud.com lists the 1080 url first
    pattern = r'(https://i1\.sndcdn\.com/artworks-[^"]*?-t500x500\.(png|jpg))'
    match = re.search(pattern, response.text)

    if not match:
        raise ValueError("Could not find SoundCloud artwork in page")

    # "original" is the full-size upload, the page only links the 500x500 thumbnail
    image_url = match.group(1).replace("t500x500", "original")

    image_response = requests.get(image_url, timeout=REQUEST_TIMEOUT)
    image_response.raise_for_status()

    return image_response.content
