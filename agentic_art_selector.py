from io import BytesIO
import os
import tempfile
from typing import List

from PIL import Image


def pick_art_agentic(images_bytes: List[bytes]) -> int:
    art_dir = tempfile.mkdtemp(prefix="soundscrape-art-")
    paths = []
    for i, image_bytes in enumerate(images_bytes):
        image = Image.open(BytesIO(image_bytes))
        filename = f"{i}_{image.width}x{image.height}.{image.format.lower()}"
        path = os.path.join(art_dir, filename)
        with open(path, "wb") as f:
            f.write(image_bytes)
        paths.append(path)

    print(f"ART CHOICES in {art_dir}:", flush=True)
    for path in paths:
        print(path, flush=True)

    while True:
        print("ENTER CHOSEN ART PATH:", flush=True)
        answer = input().strip()
        if answer in paths:
            return paths.index(answer)
        print(f"Not one of the art choices: {answer}", flush=True)
