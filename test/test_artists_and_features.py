from unittest import TestCase

from google import genai
from google.genai import types
from pydantic import BaseModel
import pytest
import yaml

from artists_features import (
    ArtistsAndFeaturesTemplate,
    find_artists_and_features,
    search_prompt,
    structure_prompt,
)


def _get_gemini_client():
    with open("secrets.yaml", "r") as f:
        config = yaml.safe_load(f)
        gemini_api_key = config["gemini_api_key"]
    return genai.Client(api_key=gemini_api_key)


def _call_gemini_search(client: genai.Client, prompt: str):
    grounding_tool = types.Tool(google_search=types.GoogleSearch())
    config = types.GenerateContentConfig(tools=[grounding_tool])
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=config,
    )
    assert response.text is not None
    return response


def _call_gemini_structure(client: genai.Client, prompt: str, schema: type[BaseModel]):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
        ),
    )
    return response


@pytest.mark.xdist_group(name="artists_and_features")
class ArtistsAndFeaturesTest(TestCase):
    pass


@pytest.mark.xdist_group(name="artists_and_features")
class PromptTests(TestCase):
    def setUp(self):
        self.client = _get_gemini_client()

    def test_one_artist_one_feature(self):
        prompt = search_prompt("Zedd", "Spectrum (feat. Matthew Koma)")
        response = _call_gemini_search(self.client, prompt)
        assert response.text is not None
        self.assertIn("zedd", response.text.lower())
        self.assertIn("matthew koma", response.text.lower())
        print(response.text)
        self.assertLess(len(response.text), 40)

    def test_no_features(self):
        prompt = search_prompt("Ninajirachi", "Battery Death")
        for _ in range(5):
            response = _call_gemini_search(self.client, prompt)
            assert response.text is not None
            self.assertIn("ninajirachi", response.text.lower())
            self.assertNotIn("battery death", response.text.lower())
            self.assertLess(len(response.text), 25)

    def test_zedd_clarity_with_features(self):
        result = find_artists_and_features("Zedd", "Clarity")
        self.assertEqual(result.artists, ["Zedd"])
        self.assertEqual(result.features, ["Foxes"])

    def test_isoknock_pain_multiple_artists(self):
        result = find_artists_and_features("ISOKNOCK", "PAIN")
        self.assertIn("ISOKNOCK", result.artists)
        self.assertIn("Knock2", result.artists)
        self.assertIn("ISOxo", result.artists)
        self.assertEqual(len(result.artists), 3)
        self.assertEqual(result.features, [])

    def test_ninajirachi_battery_death_single_artist(self):
        result = find_artists_and_features("Ninajirachi", "Battery Death")
        self.assertEqual(result.artists, ["Ninajirachi"])
        self.assertEqual(result.features, [])

    def test_skrillex_rumble_multiple_artists(self):
        result = find_artists_and_features("Skrillex", "Rumble")
        self.assertIn("Skrillex", result.artists)
        self.assertIn("Fred again..", result.artists)
        self.assertIn("Flowdan", result.artists)
        self.assertEqual(len(result.artists), 3)
        self.assertEqual(result.features, [])

    def test_single_artist_with_feature(self):
        prompt = structure_prompt(
            "Daft Punk",
            "Get Lucky",
            "Artists: Daft Punk. Features: Pharrell Williams, Nile Rodgers",
        )
        for _ in range(5):
            response = _call_gemini_structure(
                self.client, prompt, ArtistsAndFeaturesTemplate
            )
            parsed = response.parsed
            self.assertIsInstance(parsed, ArtistsAndFeaturesTemplate)
            assert isinstance(parsed, ArtistsAndFeaturesTemplate)
            self.assertEqual(parsed.artists, ["Daft Punk"])
            self.assertIn("Pharrell Williams", parsed.features)
            self.assertIn("Nile Rodgers", parsed.features)

    def test_multiple_artists_no_features(self):
        prompt = structure_prompt(
            "Porter Robinson", "Shelter", "Artists: Porter Robinson, Madeon"
        )
        for _ in range(5):
            response = _call_gemini_structure(
                self.client, prompt, ArtistsAndFeaturesTemplate
            )
            parsed = response.parsed
            self.assertIsInstance(parsed, ArtistsAndFeaturesTemplate)
            assert isinstance(parsed, ArtistsAndFeaturesTemplate)
            self.assertIn("Porter Robinson", parsed.artists)
            self.assertIn("Madeon", parsed.artists)
            self.assertEqual(len(parsed.artists), 2)
            self.assertEqual(parsed.features, [])

    def test_single_artist_no_features(self):
        prompt = structure_prompt("Deadmau5", "Strobe", "Artists: Deadmau5")
        for _ in range(5):
            response = _call_gemini_structure(
                self.client, prompt, ArtistsAndFeaturesTemplate
            )
            parsed = response.parsed
            self.assertIsInstance(parsed, ArtistsAndFeaturesTemplate)
            assert isinstance(parsed, ArtistsAndFeaturesTemplate)
            self.assertEqual(parsed.artists, ["Deadmau5"])
            self.assertEqual(parsed.features, [])

    def test_multiple_artists_with_features(self):
        prompt = structure_prompt(
            "Major Lazer", "Lean On", "Artists: Major Lazer, DJ Snake. Features: MØ"
        )
        for _ in range(5):
            response = _call_gemini_structure(
                self.client, prompt, ArtistsAndFeaturesTemplate
            )
            parsed = response.parsed
            self.assertIsInstance(parsed, ArtistsAndFeaturesTemplate)
            assert isinstance(parsed, ArtistsAndFeaturesTemplate)
            self.assertIn("Major Lazer", parsed.artists)
            self.assertIn("DJ Snake", parsed.artists)
            self.assertEqual(len(parsed.artists), 2)
            self.assertEqual(parsed.features, ["MØ"])
            self.assertEqual(len(parsed.artists), 1)
