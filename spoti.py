from base64 import b64encode
import json
from urllib.parse import urlencode

import requests
import yaml

from album_search import most_famous_artist


PRINT_CURL_COMMANDS = False

with open("secrets.yaml", "r") as f:
    config = yaml.safe_load(f)
    client_id = config["spotify_client_id"]
    client_secret = config["spotify_client_secret"]


def optinally_print_curl_command(url, headers=None, data=None):
    if not PRINT_CURL_COMMANDS:
        return

    curl_parts = ["curl", "-s"]

    if headers:
        for key, value in headers.items():
            curl_parts.extend(["-H", f"'{key}: {value}'"])

    if data:
        if isinstance(data, dict):
            data_str = "&".join([f"{k}={v}" for k, v in data.items()])
            curl_parts.extend(["-d", f"'{data_str}'"])

    # Encode query parameters in URL
    if "?" in url:
        base_url, query_string = url.split("?", 1)
        # Parse query string into parameters and properly encode them
        params = {}
        for param in query_string.split("&"):
            if "=" in param:
                key, value = param.split("=", 1)
                params[key] = value
        encoded_query = urlencode(params)
        encoded_url = f"{base_url}?{encoded_query}"
    else:
        encoded_url = url

    curl_parts.append(f"'{encoded_url}'")
    curl_parts.extend(["|", "jq"])

    print(" ".join(curl_parts))


def get_token() -> str:
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode()
    auth_base64 = b64encode(auth_bytes).decode()

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    optinally_print_curl_command(url, headers, data)
    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    return json_result["access_token"]


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    query = f"q={artist_name}&type=artist&limit=10"
    query_url = f"{url}?{query}"

    optinally_print_curl_command(query_url, headers)
    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


def get_art_url(token, title: str, artist: str, single: bool, is_album: bool) -> str:
    if single and is_album:
        raise ValueError("Cannot have both single_release and is_album set to True")

    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}

    current_artist = artist

    for attempt in range(2):
        try:
            if is_album:  # Title refers to an album
                query_url = (
                    f"{url}?q={title} artist:{current_artist}&type=album&limit=10"
                )
                optinally_print_curl_command(query_url, headers)
                result = requests.get(query_url, headers=headers)
                json_result = json.loads(result.content)

                albums = json_result.get("albums").get("items")

                for album in albums:
                    if album.get("album_type") == "album":
                        return album.get("images")[0]["url"]

                raise ValueError(
                    f"Couldn't find an album by '{current_artist}' entitled '{title}'"
                )

            else:  # Title refers to a track
                query_url = (
                    f"{url}?q={title} artist:{current_artist}&type=track&limit=50"
                )
                optinally_print_curl_command(query_url, headers)
                result = requests.get(query_url, headers=headers)
                json_result = json.loads(result.content)

                tracks = json_result.get("tracks").get("items")
                if not tracks:
                    raise ValueError(
                        f"No track found for '{title}' by '{current_artist}'"
                    )

                selected_album = None

                if single:  # We're looking for the single cover art
                    for track in tracks:
                        album = track.get("album")
                        if album.get("album_type") == "single":
                            selected_album = album
                            break
                    if selected_album is None:
                        raise ValueError(
                            f"Couldn't find a single by '{current_artist}' called '{title}'"
                        )

                else:  # We're looking for the cover art of the album containing this track
                    for track in tracks:
                        album = track.get("album")
                        if album.get("album_type") == "album":
                            selected_album = album
                            break

                    if selected_album is None:
                        raise ValueError(
                            f"Couldn't find an album by '{current_artist}' containing track '{title}'"
                        )

                assert selected_album is not None
                images = selected_album.get("images")
                return images[0]["url"]

        except ValueError:
            if attempt == 0:
                current_artist = most_famous_artist(artist)
            else:
                raise

    raise ValueError(f"Could not find art URL for '{title}' by '{artist}'")


def _remove_available_markets(obj):
    if isinstance(obj, dict):
        obj.pop("available_markets", None)
        for value in obj.values():
            _remove_available_markets(value)
    elif isinstance(obj, list):
        for item in obj:
            _remove_available_markets(item)


def tool_search_spotify(token, artist=None, album=None, title=None, limit=2):
    query_parts = []
    if title:
        query_parts.append(title)
    if album:
        query_parts.append(album)
    if artist:
        query_parts.append(f"artist:{artist}")

    q = " ".join(query_parts)

    if album and not title:
        search_type = "album"
    elif title:
        search_type = "track"
    elif artist:
        search_type = "artist"
    else:
        raise ValueError("Must specify at least one of: artist, album, title")

    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    query = f"q={q}&type={search_type}&limit={limit}"
    query_url = f"{url}?{query}"

    optinally_print_curl_command(query_url, headers)
    result = requests.get(query_url, headers=headers)
    data = json.loads(result.content)

    _remove_available_markets(data)

    items = data.get(f"{search_type}s", {}).get("items", [])
    return items


def format_compact(items):
    if not items:
        return "No results found"

    output = []
    for item in items:
        lines = []
        lines.append(f"ID: {item.get('id', 'N/A')}")
        lines.append(f"Name: {item.get('name', 'N/A')}")

        if "artists" in item:
            if isinstance(item["artists"], list):
                artist_names = ", ".join([a.get("name", "") for a in item["artists"]])
                lines.append(f"Artists: {artist_names}")

        if "album" in item:
            album = item["album"]
            album_name = album.get("name", "N/A")
            album_id = album.get("id", "N/A")
            lines.append(f"Album: {album_name} ({album_id})")

        if "genres" in item and item["genres"]:
            genres = ", ".join(item["genres"])
            lines.append(f"Genres: {genres}")

        output.append("\n".join(lines))

    return "\n---\n".join(output)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Search Spotify")
    parser.add_argument("--artist", help="Artist name")
    parser.add_argument("--album", help="Album name")
    parser.add_argument("--title", help="Track title")
    parser.add_argument("--compact", action="store_true", help="Show compact output")
    args = parser.parse_args()

    if not (args.artist or args.album or args.title):
        print("Must specify at least one of: --artist, --album, --title")
        exit(1)

    token = get_token()
    items = tool_search_spotify(token, args.artist, args.album, args.title, limit=2)

    if args.compact:
        print(format_compact(items))
    else:
        print(json.dumps(items, indent=2))
