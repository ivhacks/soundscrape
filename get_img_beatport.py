import re

import requests


REQUEST_TIMEOUT = 20
# beatport 403s the default python-requests user agent
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
}


def get_image_beatport(link: str) -> bytes:
    response = requests.get(link, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    match = re.search(
        r'property="og:image" content="(https://geo-media\.beatport\.com/[^"]+)"',
        response.text,
    )
    if not match:
        raise ValueError("Could not find Beatport artwork in page")

    # track pages have a {w}x{h} template here, 0x0 means the original upload
    # (any other size gets resized, even upscaled)
    image_url = re.sub(r"/image_size/[^/]+/", "/image_size/0x0/", match.group(1))

    image_response = requests.get(image_url, timeout=REQUEST_TIMEOUT)
    image_response.raise_for_status()

    return image_response.content
