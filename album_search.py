import os

from openai import OpenAI
from pydantic import BaseModel
import yaml


def search_prompt(artist: str, song_title: str) -> str:
    return f"""{artist} - {song_title}
web-check: is track on a RELEASED album (not upcoming)?
if yes: "TRACK is on ARTIST YEAR album ALBUM."
if no: "TRACK was released as a single in YEAR."
prefer album over prior single when album already out.
1 sentence. no chat. no unreleased albums.
ex: bittersweet → Audien 2025 album First Love
ex: fast n slow → knock2 2025 album nolimit"""


def structure_prompt(artist: str, song_title: str, first_response: str) -> str:
    return f"""{artist} - {song_title}
text: {first_response}
fill title/year/single:
- released album → title=ALBUM name (not song), single=false
- only single → title=song name, single=true
keep title casing from text (nolimit stays nolimit). strip feat/deluxe. ignore unreleased."""


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
                model="grok-4.5",
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

    prompt = f"""most famous artist in: {artists}
reply ONLY that name."""

    response = client.responses.create(
        model="grok-4.5",
        input=prompt,
    )

    response_text = response.output_text
    if not response_text:
        raise ValueError("No response from Grok API")
    return response_text.strip()


if __name__ == "__main__":
    print(identify_album("Kevin Gates", "2 Phones"))
