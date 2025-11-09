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
    parsed = response.parsed
    assert isinstance(parsed, ArtistsAndFeaturesTemplate)
    print(f"Artists: {parsed.artists}")
    print(f"Features: {parsed.features}")
    return parsed


@pytest.mark.xdist_group(name="artists_and_features")
class ArtistsAndFeaturesTest(TestCase):
    def test_porter_robinson_divinity(self):
        result = find_artists_and_features(
            "Porter Robinson", "Divinity (feat. Amy Millan)"
        )
        self.assertEqual(result.artists, ["Porter Robinson"])
        self.assertEqual(result.features, ["Amy Millan"])

    def test_porter_robinson_sad_machine(self):
        result = find_artists_and_features("Porter Robinson", "Sad Machine")
        self.assertEqual(result.artists, ["Porter Robinson"])
        self.assertEqual(result.features, [])

    def test_porter_robinson_years_of_war(self):
        result = find_artists_and_features(
            "Porter Robinson", "Years Of War (feat. Breanne Düren & Sean Caskey)"
        )
        self.assertEqual(result.artists, ["Porter Robinson"])
        self.assertEqual(result.features, ["Breanne Düren", "Sean Caskey"])

    def test_porter_robinson_flicker(self):
        result = find_artists_and_features("Porter Robinson", "Flicker")
        self.assertEqual(result.artists, ["Porter Robinson"])
        self.assertEqual(result.features, [])

    def test_porter_robinson_fresh_static_snow(self):
        result = find_artists_and_features("Porter Robinson", "Fresh Static Snow")
        self.assertEqual(result.artists, ["Porter Robinson"])
        self.assertEqual(result.features, [])

    def test_porter_robinson_polygon_dust(self):
        result = find_artists_and_features(
            "Porter Robinson", "Polygon Dust (feat. Lemaitre)"
        )
        self.assertEqual(result.artists, ["Porter Robinson"])
        self.assertEqual(result.features, ["Lemaitre"])

    def test_porter_robinson_hear_the_bells(self):
        result = find_artists_and_features(
            "Porter Robinson", "Hear the Bells (feat. Imaginary Cities)"
        )
        self.assertEqual(result.artists, ["Porter Robinson"])
        self.assertEqual(result.features, ["Imaginary Cities"])

    def test_porter_robinson_natural_light(self):
        result = find_artists_and_features("Porter Robinson", "Natural Light")
        self.assertEqual(result.artists, ["Porter Robinson"])
        self.assertEqual(result.features, [])

    def test_porter_robinson_lionhearted(self):
        result = find_artists_and_features(
            "Porter Robinson", "Lionhearted (feat. Urban Cone)"
        )
        self.assertEqual(result.artists, ["Porter Robinson"])
        self.assertEqual(result.features, ["Urban Cone"])

    def test_porter_robinson_sea_of_voices(self):
        result = find_artists_and_features("Porter Robinson", "Sea of Voices")
        self.assertEqual(result.artists, ["Porter Robinson"])
        self.assertEqual(result.features, [])

    def test_porter_robinson_fellow_feeling(self):
        result = find_artists_and_features("Porter Robinson", "Fellow Feeling")
        self.assertEqual(result.artists, ["Porter Robinson"])
        self.assertEqual(result.features, [])

    def test_porter_robinson_goodbye_to_a_world(self):
        result = find_artists_and_features("Porter Robinson", "Goodbye to a World")
        self.assertEqual(result.artists, ["Porter Robinson"])
        self.assertEqual(result.features, [])


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
        self.assertEqual(result.artists, ["ISOKNOCK", "Knock2", "ISOxo"])
        self.assertEqual(result.features, [])

    def test_ninajirachi_battery_death_single_artist(self):
        result = find_artists_and_features("Ninajirachi", "Battery Death")
        self.assertEqual(result.artists, ["Ninajirachi"])
        self.assertEqual(result.features, [])

    def test_skrillex_rumble_multiple_artists(self):
        result = find_artists_and_features("Skrillex", "Rumble")
        self.assertEqual(result.artists, ["Skrillex", "Fred again..", "Flowdan"])
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
            self.assertEqual(response.artists, ["Daft Punk"])
            self.assertEqual(response.features, ["Pharrell Williams", "Nile Rodgers"])

    def test_multiple_artists_no_features(self):
        prompt = structure_prompt(
            "Porter Robinson", "Shelter", "Artists: Porter Robinson, Madeon"
        )
        for _ in range(5):
            response = _call_gemini_structure(
                self.client, prompt, ArtistsAndFeaturesTemplate
            )
            self.assertEqual(response.artists, ["Porter Robinson", "Madeon"])
            self.assertEqual(response.features, [])

    def test_single_artist_no_features(self):
        prompt = structure_prompt("Deadmau5", "Strobe", "Artists: Deadmau5")
        for _ in range(5):
            response = _call_gemini_structure(
                self.client, prompt, ArtistsAndFeaturesTemplate
            )
            self.assertEqual(response.artists, ["Deadmau5"])
            self.assertEqual(response.features, [])

    def test_multiple_artists_with_features(self):
        prompt = structure_prompt(
            "Major Lazer", "Lean On", "Artists: Major Lazer, DJ Snake. Features: MØ"
        )
        for _ in range(5):
            response = _call_gemini_structure(
                self.client, prompt, ArtistsAndFeaturesTemplate
            )
            self.assertEqual(response.artists, ["Major Lazer", "DJ Snake"])
            self.assertEqual(response.features, ["MØ"])
