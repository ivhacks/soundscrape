import os
import re

from openai import OpenAI
from pydantic import BaseModel
import yaml


def search_prompt(artist: str, song_title: str) -> str:
    return f"""{artist} - {song_title}
official credited artists + feat. only (stream/charts).
no producers unless listed as artist. no uncredited. no alias real names. no vocaloid unless explicit feat.
one line only:
Artists: A, B. Features: C
or no feats: Artists: A, B
never write Features: alone. no song title. no chat."""


def artists_line_from_response(text: str) -> str:
    # web_search models love a chatty preamble; keep only the Artists: line
    match = re.search(r"Artists:\s*.+", text, re.IGNORECASE)
    if not match:
        raise ValueError(f"No Artists: line in response: {text}")
    return match.group(0).strip()


def structure_prompt(artist: str, song_title: str, first_response: str) -> str:
    return f"""{artist} - {song_title}
line: {first_response}
parse to artists[] + features[].
include EVERY name after Artists: and Features: (no dropping collab names).
empty features ok. clean names. data only."""


class ArtistsAndFeaturesTemplate(BaseModel):
    artists: list[str]
    features: list[str]


class ArtistsAndFeatures:
    artists: list[str]
    features: list[str]

    def __init__(self, artists: list[str], features: list[str]):
        self.artists = artists
        self.features = features


def _get_grok_client() -> OpenAI:
    with open(os.environ.get("SOUNDSCRAPE_SECRETS_PATH", "secrets.yaml"), "r") as f:
        config = yaml.safe_load(f)
        xai_api_key = config["xai_api_key"]

    return OpenAI(api_key=xai_api_key, base_url="https://api.x.ai/v1")


def find_artists_and_features(artist: str, song_title: str) -> ArtistsAndFeatures:
    client = _get_grok_client()

    prompt = search_prompt(artist, song_title)

    response = client.responses.create(
        model="grok-4.5",
        input=prompt,
        tools=[{"type": "web_search"}],
    )
    response_text = response.output_text
    if not response_text:
        raise ValueError("No response from Grok API")
    response_text = artists_line_from_response(response_text)
    print(response_text)

    # retry structure parse only (cheap); never re-run web_search
    last_err: Exception | None = None
    for _ in range(3):
        try:
            prompt = structure_prompt(artist, song_title, response_text)

            completion = client.beta.chat.completions.parse(
                model="grok-4.5",
                messages=[{"role": "user", "content": prompt}],
                response_format=ArtistsAndFeaturesTemplate,
            )

            parsed = completion.choices[0].message.parsed
            if not isinstance(parsed, ArtistsAndFeaturesTemplate):
                raise ValueError("Invalid response format from Grok API")
            if not parsed.artists:
                raise ValueError("empty artists list from structure parse")

            return ArtistsAndFeatures(parsed.artists, parsed.features)
        except ValueError as e:
            last_err = e

    assert last_err is not None
    raise last_err
