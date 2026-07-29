import os

from openai import OpenAI
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

            RULES for the title field:
            - If the song is on an album, title MUST be the ALBUM name (never the song name).
              Example: song "fast n slow" on album "nolimit" → title="nolimit", single=false
            - If the song is only a standalone single (not on any released album), title is the single/song name and single=true.
              Example: "Bittersweet was released as a single in 2025" → title="Bittersweet", single=true
            - Omit features, "(single)", deluxe, etc. from the title. Base title only.
            - If there's anything about upcoming or unreleased albums/tracks, IGNORE IT.
            - Only base your response on music that has already been officially released.
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


def _get_grok_client() -> OpenAI:
    with open(os.environ.get("SOUNDSCRAPE_SECRETS_PATH", "secrets.yaml"), "r") as f:
        config = yaml.safe_load(f)
        xai_api_key = config["xai_api_key"]

    return OpenAI(api_key=xai_api_key, base_url="https://api.x.ai/v1")


def identify_album(artist: str, song_title: str) -> Album:
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
    print(response_text)

    # retry structure parse only (cheap); never re-run web_search
    last_err: Exception | None = None
    for _ in range(2):
        try:
            prompt = structure_prompt(artist, song_title, response_text)

            completion = client.beta.chat.completions.parse(
                model="grok-3-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format=AlbumTemplate,
            )

            parsed = completion.choices[0].message.parsed
            if not isinstance(parsed, AlbumTemplate):
                raise ValueError("Invalid response format from Grok API")

            return Album(parsed.title, parsed.single, parsed.year)
        except ValueError as e:
            last_err = e

    assert last_err is not None
    raise last_err


def most_famous_artist(artists: str) -> str:
    client = _get_grok_client()

    prompt = f"""From this list of music artists: {artists}
    
    Which artist is the most famous and well-known globally? 
    Respond with only the artist name, nothing else."""

    response = client.responses.create(
        model="grok-3-mini",
        input=prompt,
    )

    response_text = response.output_text
    if not response_text:
        raise ValueError("No response from Grok API")
    return response_text.strip()


if __name__ == "__main__":
    print(identify_album("Kevin Gates", "2 Phones"))
