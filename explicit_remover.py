import os
from file_metadata import (
    get_song_title,
    set_song_title,
    get_album_title,
    set_album_title,
)


# TODO: This whole script needs work
def clean_filename(input_name):
    if "[Explicit]" in input_name:
        return input_name[
            input_name.find(" - ") + 3 : input_name.find("[Explicit]") - 1
        ]
    else:
        return input_name[input_name.find(" - ") + 3 : input_name.find(".mp3")]


def clean(input_name):
    if "[Explicit]" in input_name:
        return input_name[: input_name.find("[Explicit]") - 1]
    else:
        return input_name


if __name__ == "__main__":
    dir_list = os.listdir(os.path.join(os.getcwd(), "temp"))
    for file in dir_list:
        if ".mp3" in file:
            print("doing " + file)
            file_path = os.path.join(os.getcwd(), "temp", file)

            title = get_song_title(file_path)
            album = get_album_title(file_path)

            set_song_title(file_path, clean(title))
            set_album_title(file_path, clean(album))
            os.rename(
                os.path.join(os.getcwd(), "temp", file),
                os.path.join(os.getcwd(), "temp", clean(file) + ".mp3"),
            )
