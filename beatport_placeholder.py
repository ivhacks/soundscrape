import os

from img_diff import image_difference

# beatport embeds its logo as the cover when a release has no artwork uploaded.
# it isn't the album's art, and if it seeds the reverse image search and
# downselect we only ever get more copies of the logo back
PLACEHOLDER_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "beatport_placeholder.jpg"
)

with open(PLACEHOLDER_PATH, "rb") as f:
    PLACEHOLDER_BYTES = f.read()


def is_beatport_placeholder(image_bytes: bytes) -> bool:
    try:
        return image_difference(image_bytes, PLACEHOLDER_BYTES) < 5
    except Exception:
        return False
