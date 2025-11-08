from unittest import TestCase

from google import genai
from google.genai import types
import pytest
import yaml

from album_search import (
    AlbumTemplate,
    identify_album,
    most_famous_artist,
    search_prompt,
    structure_prompt,
)


@pytest.mark.xdist_group(name="album_search")
class AlbumSearchTests(TestCase):
    def test_knock2_fast_n_slow(self):
        album = identify_album("knock2", "fast n slow")
        self.assertEqual(album.title, "nolimit")
        self.assertEqual(album.single, False)
        self.assertEqual(album.year, 2025)

    def test_audien_bittersweet(self):
        album = identify_album("audien, shallou, rosie darling", "bittersweet")
        self.assertEqual(album.title, "Bittersweet")
        self.assertEqual(album.single, True)
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
    def test_ignores_unreleased_albums_first_response(self):
        # We're exercising the prompts in album_search.py
        """
        The song bittersweet is on the album first love, which is not yet released.
        The prompt should not mention first love.
        """
        prompt = search_prompt("audien, shallou, rosie darling", "bittersweet")

        with open("secrets.yaml", "r") as f:
            config = yaml.safe_load(f)
            gemini_api_key = config["gemini_api_key"]

        client = genai.Client(api_key=gemini_api_key)
        grounding_tool = types.Tool(google_search=types.GoogleSearch())
        config = types.GenerateContentConfig(tools=[grounding_tool])
        for _ in range(5):
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=config,
            )

            response_text = response.text
            self.assertIsNotNone(response_text)
            assert response_text is not None
            self.assertNotIn("first love", response_text.lower())
            self.assertNotIn("harmony", response_text.lower())

    def test_ignores_unreleased_albums_second_response(self):
        # We're exercising the prompts in album_search.py
        prompt = structure_prompt(
            "audien, shallou, rosie darling",
            "bittersweet",
            "Bittersweet was released as a single in 2025 and will be on Audien's upcoming album, Harmony.",
        )

        with open("secrets.yaml", "r") as f:
            config = yaml.safe_load(f)
            gemini_api_key = config["gemini_api_key"]

        client = genai.Client(api_key=gemini_api_key)

        for _ in range(5):
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json", response_schema=AlbumTemplate
                ),
            )

            parsed = response.parsed
            self.assertIsInstance(parsed, AlbumTemplate)
            assert isinstance(parsed, AlbumTemplate)
            self.assertEqual(parsed.title, "Bittersweet")
            self.assertEqual(parsed.single, True)
            self.assertEqual(parsed.year, 2025)
