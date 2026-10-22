import io
import os
import sys

from PIL import Image

from file_metadata import get_cover_art


def extract_artwork(filename: str, out_path: str) -> str:
    raw_image = get_cover_art(filename)
    image = Image.open(io.BytesIO(raw_image))
    extension = "jpg"
    if image.format == "PNG":
        extension = "png"
    out_file = f"{out_path}.{extension}"
    with open(out_file, "wb") as f:
        f.write(raw_image)
    return f"{out_file} {image.width}x{image.height}"


if __name__ == "__main__":
    filename = sys.argv[1]
    # Default puts the art next to the song so it's easy to find
    out_path = os.path.splitext(filename)[0] + "_cover"
    if len(sys.argv) > 2:
        out_path = sys.argv[2]
    print(extract_artwork(filename, out_path))
