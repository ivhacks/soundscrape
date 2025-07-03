from io import BytesIO

import imagehash
from PIL import Image


def image_difference(image1_bytes: bytes, image2_bytes: bytes) -> int:
    """
    Calculate similarity between two images using perceptual hashes.
    0 indicates identical images, low values (<5) indicate similar, high values are different.
    """
    hash1 = imagehash.phash(Image.open(BytesIO(image1_bytes)))
    hash2 = imagehash.phash(Image.open(BytesIO(image2_bytes)))
    return abs(hash1 - hash2)
