import sys

from file_metadata import (
    NoTagError,
    get_album_artist,
    get_album_title,
    get_artist,
    get_lyrics,
    get_song_title,
    get_year,
)


def read_tags(filename: str) -> str:
    fields = [
        ("artist", get_artist),
        ("album artist", get_album_artist),
        ("title", get_song_title),
        ("album", get_album_title),
        ("year", get_year),
    ]
    lines = []
    for label, getter in fields:
        try:
            value = str(getter(filename))
        except NoTagError:
            value = "(missing)"
        lines.append(f"{label}: {value}")

    try:
        lyrics = get_lyrics(filename)
    except NoTagError:
        lyrics = "(missing)"
    lines.append("lyrics:")
    lines.append(lyrics)
    return "\n".join(lines)


if __name__ == "__main__":
    print(read_tags(sys.argv[1]))
