from lyrics import *
from artwork import *
from util import *

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please specify a file or folder.")
        exit()
    filenames = []

    if os.path.isfile(sys.argv[1]):
        # This is a single file
        filenames.append(sys.argv[1])

    elif os.path.isdir(sys.argv[1]):
        dir_list = os.listdir(sys.argv[1])
        for file in dir_list:
            filenames.append(os.path.join(sys.argv[1], file))

    print("About to process the following files:")
    for filename in filenames:
        print(filename)

    for filename in filenames:

        scanned_title, scanned_artist = get_title_and_artist_from_filename(filename)
        cleaned_title = clean_title(scanned_title)
        cleaned_artist = clean_artist(scanned_artist)

        # If one song fails, just ignore it and keep going
        try:

            lyrics = get_lyrics_genius(cleaned_artist, cleaned_title)
            edited_lyrics = notepad(cleaned_artist, cleaned_title, lyrics)
            add_lyrics_to_song_file(filename, edited_lyrics)
        except:
            print(f"Failed to retrieve lyrics for {scanned_artist} - {scanned_title}.")

        # Do cover artwork
        extracted_artwork = get_image_from_song_file(filename)
        searched_images_pillow, searched_images_raw = search_cover_artwork_by_image(
            extracted_artwork
        )
        selector = CoverArtSelector(searched_images_pillow)
        chosen_image_index = selector.show_selection_window()
        put_image_in_song_file(searched_images_raw[chosen_image_index], filename)
