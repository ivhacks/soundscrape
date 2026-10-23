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

    # _0 is the full-size upload, the popup image (_10) is capped at 1200x1200
    image_url = match.group(1).replace("_10.", "_0.")

    image_response = requests.get(image_url, timeout=REQUEST_TIMEOUT)
    image_response.raise_for_status()

    return image_response.content
