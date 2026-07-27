import os
from unittest import TestCase

from openai import OpenAI
from pydantic import BaseModel
import pytest
import yaml

from album_search import (
    AlbumTemplate,
    identify_album,
    most_famous_artist,
    structure_prompt,
)


def _get_grok_client() -> OpenAI:
    with open(os.environ.get("SOUNDSCRAPE_SECRETS_PATH", "secrets.yaml"), "r") as f:
        config = yaml.safe_load(f)
        xai_api_key = config["xai_api_key"]
    return OpenAI(api_key=xai_api_key, base_url="https://api.x.ai/v1")


def _call_grok_search(client: OpenAI, prompt: str) -> str:
    response = client.responses.create(
        model="grok-4.5",
        input=prompt,
        tools=[{"type": "web_search"}],
    )
    assert response.output_text
    return response.output_text


def _call_grok_structure(client: OpenAI, prompt: str, schema: type[BaseModel]):
    completion = client.beta.chat.completions.parse(
        model="grok-4.5",
        messages=[{"role": "user", "content": prompt}],
        response_format=schema,
    )
    return completion.choices[0].message.parsed


@pytest.mark.xdist_group(name="album_search")
class AlbumSearchTests(TestCase):
    def test_knock2_fast_n_slow(self):
        album = identify_album("knock2", "fast n slow")
        self.assertEqual(album.title, "nolimit")
        self.assertEqual(album.single, False)
        self.assertEqual(album.year, 2025)

    def test_audien_bittersweet(self):
        # was a 2025 single, then landed on First Love (released Oct 3 2025)
        album = identify_album("audien, shallou, rosie darling", "bittersweet")
        self.assertEqual(album.title, "First Love")
        self.assertEqual(album.single, False)
        self.assertEqual(album.year, 2025)

    def test_kevin_gates_2_phones(self):
        album = identify_album("Kevin Gates", "2 Phones")
        self.assertEqual(album.title, "Islah")
        self.assertEqual(album.single, False)
        self.assertEqual(album.year, 2016)

    def test_most_famous_artist_skrillex(self):
        # Test the exact scenario from test_push - Skrillex should be identified as most famous
        artist = most_famous_artist("Hamdi, Taichu, OFFAIAH, Skrillex")
        self.assertEqual(artist, "Skrillex")


@pytest.mark.xdist_group(name="album_search")
class PromptTests(TestCase):
    def setUp(self):
        self.client = _get_grok_client()

    # def test_ignores_unreleased_albums_first_response(self):
    #     """
    #     The song bittersweet is on the album first love, which is not yet released.
    #     The prompt should not mention first love.
    #     """
    #     prompt = search_prompt("audien, shallou, rosie darling", "bittersweet")
    #     for _ in range(5):
    #         response = _call_grok_search(self.client, prompt)
    #         self.assertIsNotNone(response)
    #         assert response is not None
    #         self.assertNotIn("first love", response.lower())
    #         self.assertNotIn("harmony", response.lower())

    def test_ignores_unreleased_albums_second_response(self):
        prompt = structure_prompt(
            "audien, shallou, rosie darling",
            "bittersweet",
            "Bittersweet was released as a single in 2025 and will be on Audien's upcoming album, Harmony.",
        )
        for _ in range(5):
            parsed = _call_grok_structure(self.client, prompt, AlbumTemplate)
            self.assertIsInstance(parsed, AlbumTemplate)
            assert isinstance(parsed, AlbumTemplate)
            self.assertEqual(parsed.title, "Bittersweet")
            self.assertEqual(parsed.single, True)
            self.assertEqual(parsed.year, 2025)
