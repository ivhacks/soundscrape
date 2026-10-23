import requests


REQUEST_TIMEOUT = 20


def get_image_spotify(link: str) -> bytes:
    response = requests.get(
        "https://open.spotify.com/oembed", params={"url": link}, timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()

    # the thumbnail is 300x300, ab67616d000082c1 is the same image at full size
    image_id = response.json()["thumbnail_url"].split("/")[-1]
    if not image_id.startswith("ab67616d00001e02"):
        raise ValueError(f"Not a Spotify album cover: {image_id}")
    image_id = image_id.replace("ab67616d00001e02", "ab67616d000082c1")

    image_response = requests.get(
        f"https://i.scdn.co/image/{image_id}", timeout=REQUEST_TIMEOUT
    )
    image_response.raise_for_status()

    return image_response.content
