import os
import sys
import shutil
from lyrics import *
from artwork_search import *
from file_metadata import *


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

    # Create output directory if needed
    if not output_is_file and not os.path.exists(output_path):
        os.makedirs(output_path)

    # Copy files to output location
    for filename in filenames:
        if output_is_file:
            shutil.copy2(filename, output_path)
            print(f"Copied {filename} to {output_path}")
        else:
            output_filename = os.path.join(output_path, os.path.basename(filename))
            shutil.copy2(filename, output_filename)
            print(f"Copied {filename} to {output_filename}")

        if not no_processing:
            # will do a bunch of processing here
            pass


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please specify input file/folder and output file/folder.")
        print("Usage: python soundscrape.py <input> <output>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    main(input_path, output_path)
