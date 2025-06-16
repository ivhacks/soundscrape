import stagger.stagger as stagger
from stagger.stagger.id3 import *


def get_title_and_artist_from_filename(filename):
    # Open tag on song file
    tag = stagger.read_tag(filename)

    title = tag["TIT2"].text[0]
    artist = tag["TPE1"].text[0]

    return (title, artist)


def _read_or_create_tag(filename: str) -> stagger.tags.Tag:
    try:
        # Open tag on song file
        tag = stagger.read_tag(filename)
    except:
        # File had no tag, make a new one
        tag = stagger.default_tag()
    return tag


def set_year(filename: str, year: int):
    tag = _read_or_create_tag(filename)
    tag.date = str(year)
    tag.write(filename)


def get_year(filename: str) -> int:
    tag = stagger.read_tag(filename)
    return int(tag.date)


def clear_year(filename: str):
    tag = stagger.read_tag(filename)
    tag.date = ""
    tag.write(filename)


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Please specify a file.")
        exit()

    filename = sys.argv[1]
    data = get_title_and_artist_from_filename(filename)
    print(f"This file contains the song {data[0]} by {data[1]}.")
