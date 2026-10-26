import re
import time

import requests


REQUEST_TIMEOUT = 20


def get_image_deezer(link: str) -> bytes:
    match = re.search(r"/(track|album)/(\d+)", link)
    if not match:
        raise ValueError(f"Not a Deezer track or album link: {link}")

    # api.deezer.com randomly 403s ("Access Denied") about 1 in 6 requests, so retry
    for attempt in range(5):
        try:
            response = requests.get(
                f"https://api.deezer.com/{match.group(1)}/{match.group(2)}",
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            break
        except requests.RequestException:
            if attempt == 4:
                raise
            time.sleep(1)
    data = response.json()
    if "error" in data:
        raise ValueError(f"Deezer api error: {data['error']}")

    if match.group(1) == "track":
        image_id = data["album"]["md5_image"]
    else:
        image_id = data["md5_image"]

    # the api's biggest size is 1000x1000, but the cdn serves up to 1800x1800
    # (never bigger than what deezer actually has)
    image_response = requests.get(
        f"https://cdn-images.dzcdn.net/images/cover/{image_id}/1800x1800-000000-100-0-0.jpg",
        timeout=REQUEST_TIMEOUT,
    )
    image_response.raise_for_status()

    return image_response.content
