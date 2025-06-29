from io import BytesIO

from mutagen import File
from mutagen.id3 import APIC, TALB, TDRC, TIT2, TPE1, TPE2, USLT
from mutagen.mp3 import MP3
from PIL import Image


class NoTagError(Exception):
    pass


def get_title_and_artist_from_filename(filename):
    audiofile = File(filename)
    if audiofile is None:
        raise NoTagError("No tag found")

    if isinstance(audiofile, MP3):
        title = audiofile["TIT2"].text[0]
        artist = audiofile["TPE1"].text[0]
    else:
        title = audiofile.get("TITLE", [None])[0]
        artist = audiofile.get("ARTIST", [None])[0]

    if title is None or artist is None:
        raise NoTagError("Title or artist not found")

    return (title, artist)


def _read_or_create_tag(filename: str):
    try:
        audiofile = File(filename)
        if audiofile is None:
            audiofile = MP3(filename)
            audiofile.add_tags()
        return audiofile
    except:
        audiofile = MP3(filename)
        audiofile.add_tags()
        return audiofile


def set_year(filename: str, year: int):
    audiofile = _read_or_create_tag(filename)
    if isinstance(audiofile, MP3):
        audiofile["TDRC"] = TDRC(encoding=3, text=str(year))
    else:
        audiofile["DATE"] = str(year)
    audiofile.save()


def get_year(filename: str) -> int:
    audiofile = File(filename)
    if audiofile is None:
        raise NoTagError("No tag found")

    if isinstance(audiofile, MP3):
        if "TDRC" not in audiofile:
            raise NoTagError("Date not found")
        timestamp = audiofile["TDRC"].text[0]
        return int(str(timestamp).split("-")[0])
    else:
        date_val = audiofile.get("DATE")
        if not date_val:
            raise NoTagError("Date not found")
        return int(date_val[0])


def clear_year(filename: str):
    audiofile = File(filename)
    if audiofile is None:
        raise NoTagError("No tag found")

    if isinstance(audiofile, MP3):
        if "TDRC" in audiofile:
            del audiofile["TDRC"]
    else:
        if "DATE" in audiofile:
            del audiofile["DATE"]
    audiofile.save()


def set_album_title(filename: str, album_title: str):
    audiofile = _read_or_create_tag(filename)
    if isinstance(audiofile, MP3):
        audiofile["TALB"] = TALB(encoding=3, text=album_title)
    else:
        audiofile["ALBUM"] = album_title
    audiofile.save()


def get_album_title(filename: str) -> str:
    audiofile = File(filename)
    if audiofile is None:
        raise NoTagError("No tag found")

    if isinstance(audiofile, MP3):
        if "TALB" not in audiofile:
            raise NoTagError("TALB frame not found")
        return audiofile["TALB"].text[0]
    else:
        album_val = audiofile.get("ALBUM")
        if not album_val:
            raise NoTagError("Album not found")
        return album_val[0]


def clear_album_title(filename: str):
    audiofile = File(filename)
    if audiofile is None:
        raise NoTagError("No tag found")

    if isinstance(audiofile, MP3):
        if "TALB" in audiofile:
            del audiofile["TALB"]
    else:
        if "ALBUM" in audiofile:
            del audiofile["ALBUM"]
    audiofile.save()


def set_artist(filename: str, artist: str):
    audiofile = _read_or_create_tag(filename)
    if isinstance(audiofile, MP3):
        audiofile["TPE1"] = TPE1(encoding=3, text=artist)
    else:
        audiofile["ARTIST"] = artist
    audiofile.save()


def get_artist(filename: str) -> str:
    audiofile = File(filename)
    if audiofile is None:
        raise NoTagError("No tag found")

    if isinstance(audiofile, MP3):
        if "TPE1" not in audiofile:
            raise NoTagError("TPE1 frame not found")
        return audiofile["TPE1"].text[0]
    else:
        artist_val = audiofile.get("ARTIST")
        if not artist_val:
            raise NoTagError("Artist not found")
        return artist_val[0]


def clear_artist(filename: str):
    audiofile = File(filename)
    if audiofile is None:
        raise NoTagError("No tag found")

    if isinstance(audiofile, MP3):
        if "TPE1" in audiofile:
            del audiofile["TPE1"]
    else:
        if "ARTIST" in audiofile:
            del audiofile["ARTIST"]
    audiofile.save()


def set_album_artist(filename: str, album_artist: str):
    audiofile = _read_or_create_tag(filename)
    if isinstance(audiofile, MP3):
        audiofile["TPE2"] = TPE2(encoding=3, text=album_artist)
    else:
        audiofile["ALBUMARTIST"] = album_artist
    audiofile.save()


def get_album_artist(filename: str) -> str:
    audiofile = File(filename)
    if audiofile is None:
        raise NoTagError("No tag found")

    if isinstance(audiofile, MP3):
        if "TPE2" not in audiofile:
            raise NoTagError("TPE2 frame not found")
        return audiofile["TPE2"].text[0]
    else:
        albumartist_val = audiofile.get("ALBUMARTIST")
        if not albumartist_val:
            raise NoTagError("Album artist not found")
        return albumartist_val[0]


def clear_album_artist(filename: str):
    audiofile = File(filename)
    if audiofile is None:
        raise NoTagError("No tag found")

    if isinstance(audiofile, MP3):
        if "TPE2" in audiofile:
            del audiofile["TPE2"]
    else:
        if "ALBUMARTIST" in audiofile:
            del audiofile["ALBUMARTIST"]
    audiofile.save()


def set_song_title(filename: str, song_title: str):
    audiofile = _read_or_create_tag(filename)
    if isinstance(audiofile, MP3):
        audiofile["TIT2"] = TIT2(encoding=3, text=song_title)
    else:
        audiofile["TITLE"] = song_title
    audiofile.save()


def get_song_title(filename: str) -> str:
    audiofile = File(filename)
    if audiofile is None:
        raise NoTagError("No tag found")

    if isinstance(audiofile, MP3):
        if "TIT2" not in audiofile:
            raise NoTagError("TIT2 frame not found")
        return audiofile["TIT2"].text[0]
    else:
        title_val = audiofile.get("TITLE")
        if not title_val:
            raise NoTagError("Title not found")
        return title_val[0]


def clear_song_title(filename: str):
    audiofile = File(filename)
    if audiofile is None:
        raise NoTagError("No tag found")

    if isinstance(audiofile, MP3):
        if "TIT2" in audiofile:
            del audiofile["TIT2"]
    else:
        if "TITLE" in audiofile:
            del audiofile["TITLE"]
    audiofile.save()


def set_lyrics(filename: str, lyrics: str):
    ascii_lyrics = lyrics.encode("ascii", "ignore")
    audiofile = _read_or_create_tag(filename)
    if isinstance(audiofile, MP3):
        audiofile["USLT::eng"] = USLT(
            encoding=3, lang="eng", desc="", text=ascii_lyrics.decode()
        )
    else:
        audiofile["LYRICS"] = ascii_lyrics.decode()
    audiofile.save()


def get_lyrics(filename: str) -> str:
    audiofile = File(filename)
    if audiofile is None:
        raise NoTagError("No tag found")

    if isinstance(audiofile, MP3):
        # Look for any USLT frame
        uslt_frames = [key for key in audiofile.keys() if key.startswith("USLT")]
        if not uslt_frames:
            raise NoTagError("USLT frame not found")
        return audiofile[uslt_frames[0]].text
    else:
        lyrics_val = audiofile.get("LYRICS")
        if not lyrics_val:
            raise NoTagError("Lyrics not found")
        return lyrics_val[0]


def clear_lyrics(filename: str):
    audiofile = File(filename)
    if audiofile is None:
        return

    if isinstance(audiofile, MP3):
        # Remove all USLT frames
        uslt_frames = [key for key in audiofile.keys() if key.startswith("USLT")]
        for key in uslt_frames:
            del audiofile[key]
    else:
        if "LYRICS" in audiofile:
            del audiofile["LYRICS"]
    audiofile.save()


def get_cover_art(filename: str) -> Image.Image:
    audiofile = File(filename)
    if audiofile is None:
        raise NoTagError("No tag found")

    if isinstance(audiofile, MP3):
        # Look for any APIC frame
        apic_frames = [key for key in audiofile.keys() if key.startswith("APIC")]
        if not apic_frames:
            raise NoTagError("APIC frame not found")

        # Get the first APIC frame
        image_bytes = audiofile[apic_frames[0]].data
        image = Image.open(BytesIO(image_bytes))
        return image
    else:
        # For FLAC and other formats, look for embedded pictures
        if hasattr(audiofile, "pictures") and audiofile.pictures:
            image_bytes = audiofile.pictures[0].data
            image = Image.open(BytesIO(image_bytes))
            return image
        raise NoTagError("No cover art found")


def set_cover_art(filename: str, raw_image: bytes):
    audiofile = _read_or_create_tag(filename)
    if isinstance(audiofile, MP3):
        audiofile["APIC"] = APIC(
            encoding=3, mime="image/jpeg", type=3, desc="Cover", data=raw_image
        )
    else:
        # For FLAC files, we need to handle pictures differently
        from mutagen.flac import Picture

        picture = Picture()
        picture.data = raw_image
        picture.type = 3  # Cover (front)
        picture.mime = "image/jpeg"
        picture.desc = "Cover"
        if hasattr(audiofile, "add_picture"):
            audiofile.add_picture(picture)
        elif hasattr(audiofile, "pictures"):
            audiofile.pictures = [picture]
    audiofile.save()


def clear_cover_art(filename: str):
    audiofile = File(filename)
    if audiofile is None:
        return

    if isinstance(audiofile, MP3):
        # Remove all APIC frames
        keys_to_remove = [key for key in audiofile.keys() if key.startswith("APIC")]
        for key in keys_to_remove:
            del audiofile[key]
    else:
        # For FLAC and other formats
        if hasattr(audiofile, "clear_pictures"):
            audiofile.clear_pictures()
    audiofile.save()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Please specify a file.")
        exit()

    filename = sys.argv[1]
    data = get_title_and_artist_from_filename(filename)
    print(f"This file contains the song {data[0]} by {data[1]}.")
