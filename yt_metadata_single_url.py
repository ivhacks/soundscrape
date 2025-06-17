#!/usr/bin/env python3

import sys
from youtube_downloader import get_yt_music_metadata


def test_url(url):
    print(f"Testing URL: {url}")
    print("-" * 50)

    try:
        metadata = get_yt_music_metadata(url)
        print(f"Title: '{metadata.title}'")
        print(f"Artists: {metadata.artists}")
        print(f"Featured Artists: {metadata.featured_artists}")
        print(f"Album: '{metadata.album}'")
        print(f"Year: {metadata.year}")
    except Exception as e:
        print(f"Error: {e}")

    print("-" * 50)
    print()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_single_url.py <youtube_music_url>")
        sys.exit(1)

    test_url(sys.argv[1])
