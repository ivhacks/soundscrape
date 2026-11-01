from unittest import TestCase

from artists_features import find_artists_and_features, unify_artist_case


class UnifyArtistCaseTest(TestCase):
    def test_hardcore_diva_hammer_split(self):
        result = unify_artist_case(
            [["ISOxo", "Rocket Rese", "8t33n"], ["Isoxo"], ["Isoxo", "Control Freak"]]
        )
        self.assertEqual(
            result, [["ISOxo", "Rocket Rese", "8t33n"], ["ISOxo"], ["ISOxo", "Control Freak"]]
        )

    def test_stylized_wins_even_when_outnumbered(self):
        result = unify_artist_case([["Isoxo"], ["Isoxo"], ["Isoxo"], ["ISOxo"]])
        self.assertEqual(result, [["ISOxo"], ["ISOxo"], ["ISOxo"], ["ISOxo"]])

    def test_lowercase_stylization_wins(self):
        result = unify_artist_case([["Deadmau5"], ["deadmau5"]])
        self.assertEqual(result, [["deadmau5"], ["deadmau5"]])

    def test_most_common_wins_between_stylized(self):
        result = unify_artist_case([["ss3bby"], ["ss3bby"], ["SS3BBY"]])
        self.assertEqual(result, [["ss3bby"], ["ss3bby"], ["ss3bby"]])

    def test_different_names_untouched(self):
        result = unify_artist_case([["Madeon", "Isoxo"], ["Knock2"]])
        self.assertEqual(result, [["Madeon", "Isoxo"], ["Knock2"]])

    def test_empty_features_list(self):
        result = unify_artist_case([["Zedd"], []])
        self.assertEqual(result, [["Zedd"], []])


class OfficialStylizationTest(TestCase):
    def test_isoxo_hammer_from_flattened_beatport_name(self):
        result = find_artists_and_features("Isoxo, Rocket Rese, 8t33n", "HAMMER")
        self.assertIn("ISOxo", result.artists)
        self.assertNotIn("Isoxo", result.artists)

    def test_isoxo_imessage_from_flattened_beatport_name(self):
        result = find_artists_and_features("Isoxo", "IMESSAGE")
        self.assertEqual(result.artists, ["ISOxo"])
