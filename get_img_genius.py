import re

import requests

from art_selector import CoverArtSelector


REQUEST_TIMEOUT = 20


def get_image_genius(link: str) -> bytes:
    response = requests.get(link, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    html_content = response.text

    pattern = r'content="(https://images\.genius\.com/[^"]*\d+x\d+x\d+[^"]*)"'
    match = re.search(pattern, html_content)

    if not match:
        raise ValueError("Could not find Genius image in page")

    image_url = match.group(1)

    size_match = re.search(r"(\d+)x(\d+)x\d+\.png", image_url)
    if size_match:
        width = size_match.group(1)
        image_url = re.sub(r"/\d+x\d+/", f"/{width}x0/", image_url)

    image_response = requests.get(image_url, timeout=REQUEST_TIMEOUT)
    image_response.raise_for_status()

    return image_response.content


if __name__ == "__main__":
    result = get_image_genius("https://genius.com/albums/Knock2/Nolimit")
    selector = CoverArtSelector([result])
    selected_index = selector.show_selection_window()
