from unittest import TestCase
from cleaning import clean_title, clean_artist


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
