import os
import re

from openai import OpenAI
from pydantic import BaseModel
import yaml


def search_prompt(artist: str, song_title: str) -> str:
    return f"""
            Given: {artist} - {song_title}

            List the officially credited artists and features as they appear on streaming platforms/charts.

            RULES:
            - Artists = collaborators formally listed in the artist field (producers, co-writers, vocalists who are credited as artists)
            - Features = vocalists/guests marked with "feat." or "ft."
            - ONLY include names that are officially credited
            - DO NOT include: producers who aren't credited as artists, uncredited vocalists, real names of aliased artists
            - If no features exist, write "(no features)"
            - Format: "Artists: X, Y. Features: Z" or "Artists: X, Y" (if no features)

            EXACT FORMAT:
            With features: "Artists: X, Y. Features: Z"
            Without features: "Artists: X, Y"

            EXAMPLES:
            ✓ Zedd - Clarity (feat. Foxes) → "Artists: Zedd. Features: Foxes"
            ✓ ISOKNOCK - PAIN → "Artists: ISOKNOCK, Knock2, ISOxo"
            ✓ Skrillex - Rumble → "Artists: Skrillex, Fred again.., Flowdan"
            ✓ Ninajirachi - Battery Death → "Artists: Ninajirachi"

            WRONG - DO NOT DO THIS:
            ✗ Adding commentary: 'okay, i understand...' or 'i'll check...'
            ✗ Adding newlines or extra formatting
            ✗ Writing "(no features)"
            ✗ Including uncredited producers (Ginger Scott is NOT credited on Ninajirachi - Battery Death)
            ✗ Repeating the song title anywhere in the response

            YOUR ENTIRE RESPONSE MUST BE EXACTLY ONE LINE starting with 'Artists:'
            NO acknowledgment, NO explanation, NO extra text before or after.
            Do NOT write the song title in the response.

            CRITICAL: 
            - If there are no features, your response ends after listing the artists
            - Don't include a vocaloid in the feature list unless it's EXPLICITLY listed. Vocaloids are software used by the producer, they are not artists.
            - NEVER write the word "Features:" unless actual feature names follow it
            """


def artists_line_from_response(text: str) -> str:
    # web_search models love a chatty preamble; keep only the Artists: line
    match = re.search(r"Artists:\s*.+", text, re.IGNORECASE)
    if not match:
        raise ValueError(f"No Artists: line in response: {text}")
    return match.group(0).strip()


def structure_prompt(artist: str, song_title: str, first_response: str) -> str:
    return f"""The following is a response about the artists and features for the song {artist} - {song_title}:
            
            {first_response}
            
            Parse this into the expected format:
            - Extract all artist names into an "artists" list
            - Extract all feature names into a "features" list (empty list if no features)
            - Clean up artist/feature names (remove extra spaces, fix capitalization if needed)
            
            Return only the structured data, no explanation."""


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

    prompt = structure_prompt(artist, song_title, response_text)

    completion = client.beta.chat.completions.parse(
        model="grok-4.5",
        messages=[{"role": "user", "content": prompt}],
        response_format=ArtistsAndFeaturesTemplate,
    )

    parsed = completion.choices[0].message.parsed
    if not isinstance(parsed, ArtistsAndFeaturesTemplate):
        raise ValueError("Invalid response format from Grok API")

    return ArtistsAndFeatures(parsed.artists, parsed.features)
