import re

import requests

from stealth_driver import USER_AGENT


REQUEST_TIMEOUT = 20


def get_image_beatport(link: str) -> bytes:
    response = requests.get(
        link, headers={"User-Agent": USER_AGENT}, timeout=REQUEST_TIMEOUT
    )
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
