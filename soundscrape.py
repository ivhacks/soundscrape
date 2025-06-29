import os
import sys
import shutil
from dataclasses import dataclass
from typing import List
from lyrics import *
from artwork_search import *
from file_metadata import *
from parse_and_clean import *


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
    tracks: List[Track]

    def __repr__(self):
        output = f"{self.title}:\n"
        for track in self.tracks:
            output += f" - {track}\n"
        return output


def process_dir(output_dir: str):
    # Process all files in the output directory
    albums = {}
    for filename in os.listdir(output_dir):
        if filename.lower().endswith((".mp3", ".flac")):
            filepath = os.path.join(output_dir, filename)
            artist = get_artist(filepath)
            title = get_song_title(filepath)
            album_name = get_album_title(filepath)

            print(f"{artist} - {title} ({album_name})")
            if album_name not in albums.keys():
                albums[album_name] = Album(title=album_name, tracks=[])

            cleaned_title = clean_title(title)
            albums[album_name].tracks.append(
                Track(
                    artists=parse_artists(artist),
                    title=cleaned_title,
                    features=parse_features(title),
                    filepath=filepath,
                )
            )

    for album in albums.values():
        print(album)


def main(input_path: str, output_path: str, no_processing: bool = False):
    # Determine if input and output are files or dirs
    output_is_file = output_path.lower().endswith((".mp3", ".flac"))

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input path '{input_path}' does not exist")

    input_is_file = not os.path.isdir(input_path)

    filenames = []

    if input_is_file:
        filenames.append(input_path)
    else:
        # Input is a folder
        dir_list = os.listdir(input_path)
        for file in dir_list:
            if file.lower().endswith((".mp3", ".flac")):
                filenames.append(os.path.join(input_path, file))

    if output_is_file and len(filenames) > 1:
        raise ValueError("Cannot copy multiple files to a single output filename")

    print("About to process the following files:")
    for filename in filenames:
        print(filename)

    # Clear the landing zone
    if not output_is_file:
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
        os.makedirs(output_path)

    # Copy files to output location
    for filename in filenames:
        if output_is_file:
            shutil.copy2(filename, output_path)
        else:
            output_filename = os.path.join(output_path, os.path.basename(filename))
            shutil.copy2(filename, output_filename)

    # Process the output directory if we're working with a directory input
    if not no_processing:
        if not input_is_file:
            process_dir(output_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please specify input file/folder and output file/folder.")
        print("Usage: python soundscrape.py <input> <output>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    main(input_path, output_path)
