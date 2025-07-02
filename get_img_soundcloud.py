import re

import requests


def get_image_soundcloud(link: str, driver=None) -> bytes:
    response = requests.get(link)
    response.raise_for_status()

    pattern = r"(https://i1\.sndcdn\.com/artworks.*?500x500\.(png|jpg))"
    match = re.search(pattern, response.text)

    if not match:
        raise ValueError("Could not find SoundCloud artwork in page")

    image_url = match.group(1)

    image_response = requests.get(image_url)
    image_response.raise_for_status()

    return image_response.content
