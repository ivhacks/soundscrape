from unittest import TestCase
from album_search import search_prompt, structure_prompt
from album_search import identify_album
from album_search import AlbumTemplate
from google import genai
from google.genai import types


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


class PromptTests(TestCase):
    def test_ignores_unreleased_albums_first_response(self):
        """
        The song bittersweet is on the album first love, which is not yet released.
        The prompt should not mention first love.
        """
        prompt = search_prompt("audien, shallou, rosie darling", "bittersweet")

        with open(".env", "r") as f:
            gemini_api_key = f.read()

        client = genai.Client(api_key=gemini_api_key)
        grounding_tool = types.Tool(google_search=types.GoogleSearch())
        config = types.GenerateContentConfig(tools=[grounding_tool])
        for _ in range(10):
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=config,
            )

            self.assertNotIn("first love", response.text.lower())
            self.assertNotIn("harmony", response.text.lower())

    def test_ignores_unreleased_albums_second_response(self):
        prompt = structure_prompt(
            "audien, shallou, rosie darling",
            "bittersweet",
            "Bittersweet was released as a single in 2025 and will be on Audien's upcoming album, Harmony.",
        )

        with open(".env", "r") as f:
            gemini_api_key = f.read()

        client = genai.Client(api_key=gemini_api_key)

        for _ in range(10):
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json", response_schema=AlbumTemplate
                ),
            )

            self.assertEqual(response.parsed.title, "Bittersweet")
            self.assertEqual(response.parsed.single, True)
            self.assertEqual(response.parsed.year, 2025)
