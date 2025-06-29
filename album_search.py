from google import genai
from google.genai import types
from pydantic import BaseModel
import yaml


def search_prompt(artist: str, song_title: str) -> str:
    return f"""What album is the song {artist} - {song_title} on, and what year was it released?
            Note that the song may have been released as a standalone single and then later on an album.
            for these songs, please try to search out and respond with the album and year that it was released on the album.
            Some tracks may have already been released as singles, but are set to be re-released on upcoming albums.
            Only respond with an album if it's already been released.
            If the album is not yet released, but the track has been released as a single, say 'single' and do not mention the album.
            Respond as if you have no knowledge of the upcoming album, and are only aware of the already released single.
            Be concise and brief, give no other information or context. Respond with a single sentence.

            Examples of good responses:
            'Bittersweet was released as a single in 2025.'
            'fast n slow is on knock2's 2025 album nolimit.'

            examples of BAD, UNACCEPTABLE responses:
            'Bittersweet was released as a single in 2025 and will be on Audien's upcoming album, Harmony.'
            'fast n slow is on knock2's 2025 album nolimit and will be re-released in 2026 as a bonus track on 2HEARTS (Deluxe)'
            """


def structure_prompt(artist: str, song_title: str, first_response: str) -> str:
    return f"""The following is a response to a query about what album the song {artist} - {song_title} is on.
            Provide the album title, year, and whether it's a standalone single in the expected format.
            In the title field, only give the base album title. Omit features, "(single)", etc.
            If there's anything in the given text about upcoming or unreleased albums/tracks, IGNORE IT.
            Only base your response on music that has already been officially released.
            --------------------------------------------------------------------------------------
            {first_response}"""


class AlbumTemplate(BaseModel):
    title: str
    single: bool
    year: int


class Album:
    title: str
    single: bool
    year: int

    def __init__(self, title: str, single: bool, year: int):
        self.title = title
        self.single = single
        self.year = year

    def __str__(self):
        if self.single:
            return f"{self.title} (single) ({self.year})"
        else:
            return f"{self.title} ({self.year})"


def identify_album(artist: str, song_title: str) -> str | None:
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
    print(response.text)
    prompt = structure_prompt(artist, song_title, response.text)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json", response_schema=AlbumTemplate
        ),
    )

    song_title = response.parsed.title
    single = response.parsed.single
    year = response.parsed.year

    return Album(song_title, single, year)


if __name__ == "__main__":
    print(identify_album("Kevin Gates", "2 Phones"))
