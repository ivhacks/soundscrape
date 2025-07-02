import re

import requests


def get_image_bandcamp(link: str, driver=None) -> bytes:
    response = requests.get(link)
    response.raise_for_status()

    pattern = r'<a class="popupImage" href="([^"]+)">'
    match = re.search(pattern, response.text)

    if not match:
        raise ValueError("Could not find Bandcamp artwork in page")

    image_url = match.group(1)

    image_response = requests.get(image_url)
    image_response.raise_for_status()

    return image_response.content
