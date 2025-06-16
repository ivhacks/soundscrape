import stagger.stagger as stagger
from stagger.stagger.id3 import *
from PIL import Image
from io import BytesIO


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
    if not tag.date:
        raise stagger.NoTagError("Date not found")
    return int(tag.date)


def clear_year(filename: str):
    tag = stagger.read_tag(filename)
    tag.date = ""
    tag.write(filename)


def set_album_title(filename: str, album_title: str):
    tag = _read_or_create_tag(filename)
    tag["TALB"] = album_title
    tag.write(filename)


def get_album_title(filename: str) -> str:
    tag = stagger.read_tag(filename)
    try:
        return tag["TALB"].text[0]
    except KeyError:
        raise stagger.NoTagError("TALB frame not found")


def clear_album_title(filename: str):
    tag = stagger.read_tag(filename)
    del tag["TALB"]
    tag.write(filename)


def set_artist(filename: str, artist: str):
    tag = _read_or_create_tag(filename)
    tag["TPE1"] = artist
    tag.write(filename)


def get_artist(filename: str) -> str:
    tag = stagger.read_tag(filename)
    try:
        return tag["TPE1"].text[0]
    except KeyError:
        raise stagger.NoTagError("TPE1 frame not found")


def clear_artist(filename: str):
    tag = stagger.read_tag(filename)
    del tag["TPE1"]
    tag.write(filename)


def set_song_title(filename: str, song_title: str):
    tag = _read_or_create_tag(filename)
    tag["TIT2"] = song_title
    tag.write(filename)


def get_song_title(filename: str) -> str:
    tag = stagger.read_tag(filename)
    try:
        return tag["TIT2"].text[0]
    except KeyError:
        raise stagger.NoTagError("TIT2 frame not found")


def clear_song_title(filename: str):
    tag = stagger.read_tag(filename)
    del tag["TIT2"]
    tag.write(filename)


def set_lyrics(filename: str, lyrics: str):
    ascii_lyrics = lyrics.encode("ascii", "ignore")
    tag = _read_or_create_tag(filename)
    tag["USLT"] = "eng|" + ascii_lyrics.decode()
    tag.write(filename)


def get_lyrics(filename: str) -> str:
    tag = stagger.read_tag(filename)
    try:
        lyrics_data = tag["USLT"].text[0]
        if lyrics_data.startswith("eng|"):
            return lyrics_data[4:]
        return lyrics_data
    except KeyError:
        raise stagger.NoTagError("USLT frame not found")


def clear_lyrics(filename: str):
    tag = stagger.read_tag(filename)
    try:
        del tag["USLT"]
    except KeyError:
        pass
    tag.write(filename)


def get_cover_art(filename: str) -> Image.Image:
    tag = stagger.read_tag(filename)
    try:
        image_bytes = tag[APIC][0].data
        image = Image.open(BytesIO(image_bytes))
        return image
    except KeyError:
        raise stagger.NoTagError("APIC frame not found")


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Please specify a file.")
        exit()

    filename = sys.argv[1]
    data = get_title_and_artist_from_filename(filename)
    print(f"This file contains the song {data[0]} by {data[1]}.")
