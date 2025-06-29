from base64 import b64encode
import json
from urllib.parse import urlencode

import requests
import yaml


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


def get_cover_art_url(
    token, title: str, artist: str, single: bool, is_album: bool
) -> str:
    if single and is_album:
        raise ValueError("Cannot have both single_release and is_album set to True")

    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}

    if is_album:  # Title refers to an album
        query_url = f"{url}?q={title} artist:{artist}&type=album&limit=10"
        optinally_print_curl_command(query_url, headers)
        result = requests.get(query_url, headers=headers)
        json_result = json.loads(result.content)

        albums = json_result.get("albums").get("items")

        for album in albums:
            if album.get("album_type") == "album":
                return album.get("images")[0]["url"]

        raise ValueError(f"Couldn't find an album by '{artist}' entitled '{title}'")

    else:  # Title refers to a track
        query_url = f"{url}?q={title} artist:{artist}&type=track&limit=50"
        optinally_print_curl_command(query_url, headers)
        result = requests.get(query_url, headers=headers)
        json_result = json.loads(result.content)

        tracks = json_result.get("tracks").get("items")
        if not tracks:
            raise ValueError(f"No track found for '{title}' by '{artist}'")

        found = False

        if single:  # We're looking for the single cover art
            for track in tracks:
                album = track.get("album")
                if album.get("album_type") == "single":
                    selected_album = album
                    found = True
                    break
            if not found:
                raise ValueError(
                    f"Couldn't find a single by '{artist}' called '{title}'"
                )

        else:  # We're looking for the cover art of the album containing this track
            for track in tracks:
                album = track.get("album")
                if album.get("album_type") == "album":
                    selected_album = album
                    found = True
                    break

        if not found:
            raise ValueError(
                f"Couldn't find an album by '{artist}' containing track '{title}'"
            )
        else:
            images = selected_album.get("images")
            return images[0]["url"]
