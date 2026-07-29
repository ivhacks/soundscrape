import os
from unittest import TestCase

from openai import OpenAI
from pydantic import BaseModel
import yaml

from artists_features import (
    ArtistsAndFeaturesTemplate,
    artists_line_from_response,
    find_artists_and_features,
    search_prompt,
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
    return artists_line_from_response(response.output_text)


def _call_grok_structure(client: OpenAI, prompt: str, schema: type[BaseModel]):
    # structured parse occasionally returns null; retry a couple times
    for _ in range(3):
        completion = client.beta.chat.completions.parse(
            model="grok-4.5",
            messages=[{"role": "user", "content": prompt}],
            response_format=schema,
        )
        parsed = completion.choices[0].message.parsed
        if isinstance(parsed, ArtistsAndFeaturesTemplate):
            print(f"Artists: {parsed.artists}")
            print(f"Features: {parsed.features}")
            return parsed
    raise AssertionError("Grok structured parse returned null after retries")


# no shared mutable state; parallel AI calls ok
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
        self.assertIn("Porter Robinson", result.artists)
        # AI may credit Imaginary Cities as co-artist or feature
        self.assertTrue(
            "Imaginary Cities" in result.features
            or "Imaginary Cities" in result.artists
        )

    def test_porter_robinson_natural_light(self):
        result = find_artists_and_features("Porter Robinson", "Natural Light")
        self.assertEqual(result.artists, ["Porter Robinson"])
        self.assertEqual(result.features, [])

    def test_porter_robinson_lionhearted(self):
        result = find_artists_and_features(
            "Porter Robinson", "Lionhearted (feat. Urban Cone)"
        )
        self.assertIn("Porter Robinson", result.artists)
        self.assertTrue(
            "Urban Cone" in result.features or "Urban Cone" in result.artists
        )

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


class PromptTests(TestCase):
    def setUp(self):
        self.client = _get_grok_client()

    def test_one_artist_one_feature(self):
        prompt = search_prompt("Zedd", "Spectrum (feat. Matthew Koma)")
        response = _call_grok_search(self.client, prompt)
        assert response is not None
        self.assertIn("zedd", response.lower())
        self.assertIn("matthew koma", response.lower())
        print(response)
        self.assertLess(len(response), 40)

    def test_no_features(self):
        prompt = search_prompt("Ninajirachi", "Battery Death")
        for _ in range(2):
            response = _call_grok_search(self.client, prompt)
            assert response is not None
            self.assertIn("ninajirachi", response.lower())
            self.assertNotIn("battery death", response.lower())
            self.assertLess(len(response), 25)

    def test_zedd_clarity_with_features(self):
        result = find_artists_and_features("Zedd", "Clarity")
        self.assertIn("Zedd", result.artists)
        # web_search sometimes lists Foxes as co-artist instead of feature
        self.assertTrue("Foxes" in result.features or "Foxes" in result.artists)

    def test_isoknock_pain_multiple_artists(self):
        result = find_artists_and_features("ISOKNOCK", "PAIN")
        self.assertEqual(set(result.artists), {"ISOKNOCK", "Knock2", "ISOxo"})
        self.assertEqual(len(result.artists), 3)
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
        for _ in range(2):
            response = _call_grok_structure(
                self.client, prompt, ArtistsAndFeaturesTemplate
            )
            self.assertEqual(response.artists, ["Daft Punk"])
            self.assertEqual(response.features, ["Pharrell Williams", "Nile Rodgers"])

    def test_multiple_artists_no_features(self):
        prompt = structure_prompt(
            "Porter Robinson", "Shelter", "Artists: Porter Robinson, Madeon"
        )
        for _ in range(2):
            response = _call_grok_structure(
                self.client, prompt, ArtistsAndFeaturesTemplate
            )
            self.assertEqual(response.artists, ["Porter Robinson", "Madeon"])
            self.assertEqual(response.features, [])

    def test_single_artist_no_features(self):
        prompt = structure_prompt("Deadmau5", "Strobe", "Artists: Deadmau5")
        for _ in range(2):
            response = _call_grok_structure(
                self.client, prompt, ArtistsAndFeaturesTemplate
            )
            self.assertEqual(response.artists, ["Deadmau5"])
            self.assertEqual(response.features, [])

    def test_multiple_artists_with_features(self):
        prompt = structure_prompt(
            "Major Lazer", "Lean On", "Artists: Major Lazer, DJ Snake. Features: MØ"
        )
        for _ in range(2):
            response = _call_grok_structure(
                self.client, prompt, ArtistsAndFeaturesTemplate
            )
            self.assertEqual(response.artists, ["Major Lazer", "DJ Snake"])
            self.assertEqual(response.features, ["MØ"])
