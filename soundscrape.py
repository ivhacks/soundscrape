from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import hashlib
from io import BytesIO
import os
import shutil
import sys
import tempfile
from typing import Dict, List

from PIL import Image
from selenium.common.exceptions import TimeoutException

from art_search import search_cover_art_by_text
from art_selector import CoverArtSelector
from artists_features import ArtistsAndFeatures, find_artists_and_features
from file_metadata import (
    NoTagError,
    clear_cover_art,
    copy_all_tags,
    get_album_title,
    get_artist,
    get_cover_art,
    get_song_title,
    set_album_artist,
    set_artist,
    set_cover_art,
    set_lyrics,
    set_song_title,
)
from google_images_search import (
    download_images,
    downselect_images,
    search_google_images,
)
from lyrics import get_lyrics_genius
from parse_and_clean import clean_artist, clean_title, parse_artists, parse_features
from stealth_driver import create_stealth_driver
from temp_host import TempHostError


HEADLESS = True


@dataclass
class Track:
    artists: List[str]
    title: str
    features: List[str]
    filepath: str

    def __repr__(self):
        if self.features:
            return f"{'; '.join(self.artists)} - {self.title} (feat. {', '.join(self.features)})"
        else:
            return f"{'; '.join(self.artists)} - {self.title}"


@dataclass
class Album:
    title: str
    artists: List[str]
    tracks: List[Track]
    art_choices: List[bytes]
    art_choice_hashes: List[bytes]
    chosen_art: bytes

    def __repr__(self):
        artists_str = "; ".join(self.artists)
        output = f"{self.title} by {artists_str}:\n"
        for track in self.tracks:
            output += f" - {track}\n"
        return output


def process_dir(
    output_dir: str,
    no_art_select: bool = False,
    fast_search: bool = True,
    embed_lyrics: bool = True,
    resolve_artists_with_ai: bool = True,
    skip_web: bool = False,
):
    albums: Dict[str, Album] = {}

    files = []
    for filename in os.listdir(output_dir):
        if filename.lower().endswith((".mp3", ".flac")):
            filepath = os.path.join(output_dir, filename)
            artist = get_artist(filepath)
            title = get_song_title(filepath)
            album_name = get_album_title(filepath)
            print(f"{artist} - {title} ({album_name})")
            files.append((filepath, artist, title, album_name))

    def resolve_file(item):
        filepath, artist, title, album_name = item
        cleaned_title = clean_title(title)
        if resolve_artists_with_ai:
            artists_and_features = find_artists_and_features(artist, cleaned_title)
        else:
            artists_and_features = ArtistsAndFeatures(
                parse_artists(artist), parse_features(title)
            )
        try:
            art = get_cover_art(filepath)
        except NoTagError:
            art = None
        return (filepath, album_name, cleaned_title, artists_and_features, art)

    with ThreadPoolExecutor() as pool:
        resolved_files = list(pool.map(resolve_file, files))

    for (
        filepath,
        album_name,
        cleaned_title,
        artists_and_features,
        art,
    ) in resolved_files:
        if album_name not in albums:
            albums[album_name] = Album(
                title=album_name,
                artists=[],
                tracks=[],
                art_choices=[],
                art_choice_hashes=[],
                chosen_art=b"",
            )

        albums[album_name].tracks.append(
            Track(
                artists=artists_and_features.artists,
                title=cleaned_title,
                features=artists_and_features.features,
                filepath=filepath,
            )
        )

        if art is not None:
            hash = hashlib.sha256(art).digest()
            if hash not in albums[album_name].art_choice_hashes:
                albums[album_name].art_choices.append(art)
                albums[album_name].art_choice_hashes.append(hash)

    albums_list = list(albums.values())

    for album in albums_list:
        common_artists = set(album.tracks[0].artists)
        for track in album.tracks[1:]:
            common_artists = common_artists.intersection(set(track.artists))

        album.artists = list(common_artists)
        if not album.artists:
            album.artists = ["Various Artists"]

    if not skip_web:

        def fetch_text_art(album):
            search_as_album = len(album.tracks) > 1
            return search_cover_art_by_text(
                ", ".join(album.artists),
                album.tracks[0].title,
                search_as_album,
            )

        with ThreadPoolExecutor() as pool:
            text_arts = list(pool.map(fetch_text_art, albums_list))
        for album, searched_art in zip(albums_list, text_arts):
            hash = hashlib.sha256(searched_art).digest()
            album.art_choices.append(searched_art)
            album.art_choice_hashes.append(hash)

    for album in albums_list:
        print(album)

    if not skip_web:
        albums_with_art = []
        for album in albums_list:
            if album.art_choices:
                albums_with_art.append(album)

        def reverse_search(album):
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
                temp_file.write(album.art_choices[0])
                temp_path = temp_file.name
            try:
                print(
                    f"Searching for similar images for {album.title}...",
                    flush=True,
                )
                return search_google_images(temp_path)
            except TempHostError as e:
                print(
                    f"WARNING: reverse image search skipped for {album.title}; "
                    f"using the cover already on the file. ({e})",
                    flush=True,
                )
                return None
            finally:
                os.unlink(temp_path)

        with ThreadPoolExecutor() as pool:
            reverse_results = list(pool.map(reverse_search, albums_with_art))

        driver = create_stealth_driver(headless=HEADLESS)
        try:
            for album, results in zip(albums_with_art, reverse_results):
                if results is None:
                    continue

                print(
                    f"Found {len(results)} reverse-image results for {album.title}",
                    flush=True,
                )

                downloaded_images = download_images(results, driver)
                print(
                    f"Downloaded {len(downloaded_images)} images for {album.title}",
                    flush=True,
                )

                all_images = album.art_choices + downloaded_images
                print(f"Downselecting cover art for {album.title}...", flush=True)
                selected_images = downselect_images(all_images, album.art_choices[0])
                print(
                    f"Kept {len(selected_images)} cover choices for {album.title}",
                    flush=True,
                )
                album.art_choices = selected_images
        finally:
            driver.quit()

    # Apply cover art for each album
    for album in albums.values():
        print(f"Applying tags/art for album {album.title}...", flush=True)
        if no_art_select or skip_web:
            # Pick the highest resolution artwork
            highest_resolution = 0
            chosen_art = album.art_choices[0]
            for artwork_bytes in album.art_choices:
                image = Image.open(BytesIO(artwork_bytes))
                resolution = image.width * image.height
                if resolution > highest_resolution:
                    highest_resolution = resolution
                    chosen_art = artwork_bytes
        else:
            print(f"Opening cover art selector for {album.title}...", flush=True)
            selector = CoverArtSelector(album.art_choices)
            chosen_art = album.art_choices[selector.show_selection_window()]

        for track in album.tracks:
            if track.features:
                title_with_features = (
                    f"{track.title} (feat. {', '.join(track.features)})"
                )
            else:
                title_with_features = track.title

            print(f"Writing tags for {title_with_features}...", flush=True)

            original_extension = os.path.splitext(track.filepath)[1]
            new_filename = f"{title_with_features}{original_extension}"
            new_filepath = os.path.join(os.path.dirname(track.filepath), new_filename)

            os.rename(track.filepath, new_filepath)

            artist_string = "; ".join(track.artists)
            set_artist(new_filepath, artist_string)
            set_album_artist(new_filepath, "; ".join(album.artists))

            set_song_title(new_filepath, title_with_features)

            if embed_lyrics:
                print(
                    f"Fetching lyrics for {artist_string} - {track.title}...",
                    flush=True,
                )
                try:
                    lyrics = get_lyrics_genius(", ".join(track.artists), track.title)
                    if lyrics:
                        set_lyrics(new_filepath, lyrics)
                        print(f"Embedded lyrics for {title_with_features}", flush=True)
                except (ValueError, TimeoutException) as e:
                    print(
                        f"WARNING: lyrics skipped for {title_with_features}. ({e})",
                        flush=True,
                    )

            clear_cover_art(new_filepath)
            set_cover_art(new_filepath, chosen_art)
            print(f"Done {title_with_features}", flush=True)


def create_noaudio_files(input_path: str, output_path: str):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input path '{input_path}' does not exist")

    if not os.path.isdir(input_path):
        raise ValueError(f"Input path '{input_path}' must be a directory")

    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)

    for filename in os.listdir(input_path):
        if filename.lower().endswith((".mp3", ".flac")):
            source_filepath = os.path.join(input_path, filename)
            dest_filepath = os.path.join(output_path, filename)

            if filename.lower().endswith(".mp3"):
                template_file = os.path.join("test", "nothing.mp3")
            else:
                template_file = os.path.join("test", "nothing.flac")

            shutil.copy2(template_file, dest_filepath)
            copy_all_tags(source_filepath, dest_filepath)
            print(f"Created {dest_filepath}")


def main(
    input_path: str,
    output_path: str,
    no_processing: bool = False,
    no_art_select: bool = False,
    fast_search: bool = True,
    embed_lyrics: bool = True,
    resolve_artists_with_ai: bool = True,
    skip_web: bool = False,
):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input path '{input_path}' does not exist")

    if not os.path.isdir(input_path):
        raise ValueError(f"Input path '{input_path}' must be a directory")

    # Collect audio files from input directory
    filenames = []
    dir_list = os.listdir(input_path)
    for file in dir_list:
        if file.lower().endswith((".mp3", ".flac")):
            filenames.append(os.path.join(input_path, file))

    print("About to process the following files:")
    for filename in filenames:
        print(filename)

    # Clear the landing zone
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)

    # Copy files to output location
    for filename in filenames:
        output_filename = os.path.join(output_path, os.path.basename(filename))
        shutil.copy2(filename, output_filename)

    if not no_processing:
        process_dir(
            output_path,
            no_art_select=no_art_select,
            fast_search=fast_search,
            embed_lyrics=embed_lyrics,
            resolve_artists_with_ai=resolve_artists_with_ai,
            skip_web=skip_web,
        )


def process_file(
    file_path: str,
    no_art_select: bool = False,
    fast_search: bool = True,
    embed_lyrics: bool = True,
    resolve_artists_with_ai: bool = True,
):
    file_path = os.path.abspath(file_path)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File '{file_path}' does not exist")

    if not file_path.lower().endswith((".mp3", ".flac")):
        raise ValueError(f"Not an mp3/flac file: {file_path}")

    parent = os.path.dirname(file_path)
    work = tempfile.mkdtemp(prefix="soundscrape_")
    try:
        shutil.copy2(file_path, os.path.join(work, os.path.basename(file_path)))
        process_dir(
            work,
            no_art_select=no_art_select,
            fast_search=fast_search,
            embed_lyrics=embed_lyrics,
            resolve_artists_with_ai=resolve_artists_with_ai,
        )

        results = []
        for name in os.listdir(work):
            if name.lower().endswith((".mp3", ".flac")):
                results.append(name)

        if not results:
            raise Exception(f"No output file produced for {file_path}")

        for name in results:
            dest = os.path.join(parent, name)
            shutil.move(os.path.join(work, name), dest)

        # original name may have changed after title cleanup
        if os.path.basename(file_path) not in results and os.path.exists(file_path):
            os.remove(file_path)
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "--lyrics":
        if len(sys.argv) < 4:
            print("Usage: soundscrape --lyrics <artist> <title>")
            print('       soundscrape --lyrics "Porter Robinson" "Goodbye To A World"')
            sys.exit(1)
        artist = clean_artist(sys.argv[2])
        title = clean_title(sys.argv[3])
        print(get_lyrics_genius(artist, title, cache=False))
    elif len(sys.argv) >= 2 and sys.argv[1] == "--noaudio":
        if len(sys.argv) < 4:
            print("Usage: soundscrape --noaudio <input_dir> <output_dir>")
            sys.exit(1)
        create_noaudio_files(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 2:
        process_file(sys.argv[1])
    elif len(sys.argv) >= 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Usage: soundscrape <file.mp3|file.flac>")
        print("       soundscrape <input_dir> <output_dir>")
        print("       soundscrape --noaudio <input_dir> <output_dir>")
        print("       soundscrape --lyrics <artist> <title>")
        sys.exit(1)
