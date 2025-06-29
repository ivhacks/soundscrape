from unittest import TestCase

from parse_and_clean import (
    clean_artist,
    clean_title,
    parse_artists,
    parse_features,
    remove_explicit,
)


class CleanTitleTests(TestCase):
    def test_clean_title_parens(self):
        input_title = "Downfall (feat. Lexi Norton)"
        expected_output = "Downfall"
        self.assertEqual(clean_title(input_title), expected_output)

    def test_clean_title_ft(self):
        input_title = "Clarity ft. Foxes"
        expected_output = "Clarity"
        self.assertEqual(clean_title(input_title), expected_output)

    def test_clean_title_feat(self):
        input_title = "Emotional feat. Matthew Koma"
        expected_output = "Emotional"
        self.assertEqual(clean_title(input_title), expected_output)

    def test_clean_title_capital_feat(self):
        input_title = "Song Title Feat. Another Artist"
        expected_output = "Song Title"
        self.assertEqual(clean_title(input_title), expected_output)

    def test_clean_title_brackets(self):
        input_title = "Song Title [Remix]"
        expected_output = "Song Title"
        self.assertEqual(clean_title(input_title), expected_output)

    def test_clean_title_mixed(self):
        input_title = "Talk About It Feat. Desirée Dawson [Virtual Riot Remix]"
        expected_output = "Talk About It"
        self.assertEqual(clean_title(input_title), expected_output)

    def test_clean_title_no_features(self):
        input_title = "Simple Song Title"
        expected_output = "Simple Song Title"
        self.assertEqual(clean_title(input_title), expected_output)

    def test_clean_title_whitespace(self):
        input_title = "  Song Title  "
        expected_output = "Song Title"
        self.assertEqual(clean_title(input_title), expected_output)

    def test_explicit_removal(self):
        input_title = "Downfall (feat. Lexi Norton)"
        expected_output = "Downfall"
        self.assertEqual(clean_title(input_title), expected_output)


class CleanArtistTests(TestCase):
    def test_clean_artist_semicolons_and_commas(self):
        input_artist = "Virual Riot; Submatik, Holly Drummond"
        expected_output = "Virual Riot Submatik Holly Drummond"
        self.assertEqual(clean_artist(input_artist), expected_output)

    def test_clean_artist_semicolons_only(self):
        input_artist = "Artist One; Artist Two"
        expected_output = "Artist One Artist Two"
        self.assertEqual(clean_artist(input_artist), expected_output)

    def test_clean_artist_commas_only(self):
        input_artist = "Artist One, Artist Two"
        expected_output = "Artist One Artist Two"
        self.assertEqual(clean_artist(input_artist), expected_output)

    def test_clean_artist_no_separators(self):
        input_artist = "Single Artist"
        expected_output = "Single Artist"
        self.assertEqual(clean_artist(input_artist), expected_output)

    def test_clean_artist_whitespace(self):
        input_artist = "  Artist Name  "
        expected_output = "Artist Name"
        self.assertEqual(clean_artist(input_artist), expected_output)


class RemoveExplicitTests(TestCase):
    def test_parens(self):
        input_title = "Downfall (explicit)"
        expected_output = "Downfall"
        self.assertEqual(remove_explicit(input_title), expected_output)

    def test_brackets(self):
        input_title = "Song Title [explicit]"
        expected_output = "Song Title"
        self.assertEqual(remove_explicit(input_title), expected_output)

    def test_explicit_end(self):
        input_title = "Song Title explicit"
        expected_output = "Song Title"
        self.assertEqual(remove_explicit(input_title), expected_output)

    def test_no_explicit(self):
        input_title = "Song Title"
        expected_output = "Song Title"
        self.assertEqual(remove_explicit(input_title), expected_output)

    def test_legit_explicit(self):
        input_title = "hongdae guy explicit thoughts"
        expected_output = "hongdae guy explicit thoughts"
        self.assertEqual(remove_explicit(input_title), expected_output)


class FindFeaturesTests(TestCase):
    def test_parens(self):
        input_title = "Downfall (feat. Lexi Norton)"
        expected_output = ["Lexi Norton"]
        self.assertEqual(parse_features(input_title), expected_output)

    def test_parens_capital_feat(self):
        input_title = "Bass Drop Madness (Feat. DJ Sleepless)"
        expected_output = ["DJ Sleepless"]
        self.assertEqual(parse_features(input_title), expected_output)

    def test_parens_ft(self):
        input_title = "Bangarang (ft. Sirah)"
        expected_output = ["Sirah"]
        self.assertEqual(parse_features(input_title), expected_output)

    def test_parens_featuring(self):
        input_title = "twelfth dimension (featuring 3 White Monsters)"
        expected_output = ["3 White Monsters"]
        self.assertEqual(parse_features(input_title), expected_output)

    def test_no_parens_feat(self):
        input_title = "Wake Me Up feat. Aloe Blacc"
        expected_output = ["Aloe Blacc"]
        self.assertEqual(parse_features(input_title), expected_output)

    def test_no_parens_capital_feat(self):
        input_title = "Stay Feat. Alessia Cara"
        expected_output = ["Alessia Cara"]
        self.assertEqual(parse_features(input_title), expected_output)

    def test_no_parens_ft(self):
        input_title = "Titanium ft. Sia"
        expected_output = ["Sia"]
        self.assertEqual(parse_features(input_title), expected_output)

    def test_no_parens_featuring(self):
        input_title = "Scared to be Lonely featuring Dua Lipa"
        expected_output = ["Dua Lipa"]
        self.assertEqual(parse_features(input_title), expected_output)

    def test_no_features_found(self):
        input_title = "Solo Bangers Only"
        expected_output = []
        self.assertEqual(parse_features(input_title), expected_output)


class ParseArtistsTests(TestCase):
    def test_ampersand(self):
        input = "Essgener & knock tuah"
        expected_output = ["Essgener", "knock tuah"]
        self.assertEqual(parse_artists(input), expected_output)

    def test_comma(self):
        input = "jousboxx, jousbocc"
        expected_output = ["jousboxx", "jousbocc"]
        self.assertEqual(parse_artists(input), expected_output)

    def test_semicolon(self):
        input = "Virtual Riot; Skrillex"
        expected_output = ["Virtual Riot", "Skrillex"]
        self.assertEqual(parse_artists(input), expected_output)
