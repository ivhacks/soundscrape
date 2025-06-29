from dataclasses import dataclass
import hashlib
import os
import shutil
import sys
from typing import Dict, List

from art_search import search_cover_art_by_text
from art_selector import CoverArtSelector
from file_metadata import (
    clear_cover_art,
    get_album_title,
    get_artist,
    get_cover_art,
    get_song_title,
    set_artist,
    set_cover_art,
    set_song_title,
)
from lyrics import clean_title
from parse_and_clean import parse_artists, parse_features


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


def process_dir(output_dir: str):
    albums: Dict[str, Album] = {}
    for filename in os.listdir(output_dir):
        if filename.lower().endswith((".mp3", ".flac")):
            filepath = os.path.join(output_dir, filename)
            artist = get_artist(filepath)
            title = get_song_title(filepath)
            album_name = get_album_title(filepath)

            print(f"{artist} - {title} ({album_name})")
            if album_name not in albums.keys():
                albums[album_name] = Album(
                    title=album_name,
                    artists=[],
                    tracks=[],
                    art_choices=[],
                    art_choice_hashes=[],
                    chosen_art=b"",
                )

            cleaned_title = clean_title(title)
            albums[album_name].tracks.append(
                Track(
                    artists=parse_artists(artist),
                    title=cleaned_title,
                    features=parse_features(title),
                    filepath=filepath,
                )
            )
            # Hash each new cover artwork so we can check for duplicates without doing a byte-by-byte comparison between all the images
            art = get_cover_art(filepath)
            hash = hashlib.sha256(art).digest()

            if hash not in albums[album_name].art_choice_hashes:
                albums[album_name].art_choices.append(art)
                albums[album_name].art_choice_hashes.append(hash)

    for album in albums.values():
        # Set album artists to artists who appear in every track
        common_artists = set(album.tracks[0].artists)

        # Keep only artists that appear in all tracks
        for track in album.tracks[1:]:
            common_artists = common_artists.intersection(set(track.artists))

        album.artists = list(common_artists)

        if not album.artists:
            album.artists = ["Various Artists"]

        searched_art = search_cover_art_by_text(
            ", ".join(album.artists), album.title, True
        )
        hash = hashlib.sha256(searched_art).digest()
        album.art_choices.append(searched_art)
        album.art_choice_hashes.append(hash)

    for album in albums.values():
        print(album)

    for album in albums.values():
        selector = CoverArtSelector(album.art_choices)
        chosen_art = album.art_choices[selector.show_selection_window()]
        for track in album.tracks:
            if track.features:
                new_filename_base = f"{track.title} (feat. {', '.join(track.features)})"
            else:
                new_filename_base = track.title

            original_extension = os.path.splitext(track.filepath)[1]
            new_filename = f"{new_filename_base}{original_extension}"
            new_filepath = os.path.join(os.path.dirname(track.filepath), new_filename)

            os.rename(track.filepath, new_filepath)

            artist_string = "; ".join(track.artists)
            set_artist(new_filepath, artist_string)

            set_song_title(new_filepath, new_filename_base)

            clear_cover_art(new_filepath)
            set_cover_art(new_filepath, chosen_art)


def main(input_path: str, output_path: str, no_processing: bool = False):
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
        process_dir(output_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please specify input file/folder and output file/folder.")
        print("Usage: python soundscrape.py <input> <output>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    main(input_path, output_path)
