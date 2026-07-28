import re

import requests


REQUEST_TIMEOUT = 20


def get_image_bandcamp(link: str) -> bytes:
    response = requests.get(link, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    pattern = r'<a class="popupImage" href="([^"]+)">'
    match = re.search(pattern, response.text)

    if not match:
        raise ValueError("Could not find Bandcamp artwork in page")

    image_url = match.group(1)

    image_response = requests.get(image_url, timeout=REQUEST_TIMEOUT)
    image_response.raise_for_status()

    return image_response.content
