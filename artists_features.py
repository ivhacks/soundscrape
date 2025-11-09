from google import genai
from google.genai import types
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
            ✗ Adding commentary: 'okay, i understand...'
            ✗ Adding newlines or extra formatting
            ✗ Writing "(no features)"
            ✗ Including uncredited producers (Ginger Scott is NOT credited on Ninajirachi - Battery Death)

            YOUR RESPONSE MUST BE EXACTLY ONE LINE starting with 'Artists:'
            NO acknowledgment, NO explanation, NO extra text before or after.

            CRITICAL: 
            - If there are no features, your response ends after listing the artists
            - Don't include a vocaloid in the feature list unless it's EXPLICITLY listed. Vocaloids are software used by the producer, they are not artists.
            - NEVER write the word "Features:" unless actual feature names follow it
            """


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


def find_artists_and_features(artist: str, song_title: str) -> ArtistsAndFeatures:
    with open("secrets.yaml", "r") as f:
        config = yaml.safe_load(f)
        gemini_api_key = config["gemini_api_key"]

    client = genai.Client(api_key=gemini_api_key)
    grounding_tool = types.Tool(google_search=types.GoogleSearch())
    config = types.GenerateContentConfig(tools=[grounding_tool])

    prompt = search_prompt(artist, song_title)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=config,
    )
    response_text = response.text
    if response_text is None:
        raise ValueError("No response from Gemini API")
    print(response_text)
    prompt = structure_prompt(artist, song_title, response_text)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ArtistsAndFeaturesTemplate,
        ),
    )

    parsed = response.parsed
    if not isinstance(parsed, ArtistsAndFeaturesTemplate):
        raise ValueError("Invalid response format from Gemini API")

    return ArtistsAndFeatures(parsed.artists, parsed.features)
