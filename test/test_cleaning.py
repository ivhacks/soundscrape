from unittest import TestCase
from cleaning import clean_title, clean_artist, remove_explicit


class CleanTitleTests(TestCase):
    def test_parens(self):
        input_title = "Downfall (feat. Lexi Norton)"
        expected_output = "Downfall"
        self.assertEqual(clean_title(input_title), expected_output)

    def test_ft(self):
        input_title = "Clarity ft. Foxes"
        expected_output = "Clarity"
        self.assertEqual(clean_title(input_title), expected_output)

    def test_feat(self):
        input_title = "Emotional feat. Matthew Koma"
        expected_output = "Emotional"
        self.assertEqual(clean_title(input_title), expected_output)

    def test_capital_feat(self):
        input_title = "Song Title Feat. Another Artist"
        expected_output = "Song Title"
        self.assertEqual(clean_title(input_title), expected_output)

    def test_brackets(self):
        input_title = "Song Title [Remix]"
        expected_output = "Song Title"
        self.assertEqual(clean_title(input_title), expected_output)

    def test_mixed(self):
        input_title = "Talk About It Feat. Desirée Dawson [Virtual Riot Remix]"
        expected_output = "Talk About It"
        self.assertEqual(clean_title(input_title), expected_output)

    def test_no_features(self):
        input_title = "Simple Song Title"
        expected_output = "Simple Song Title"
        self.assertEqual(clean_title(input_title), expected_output)

    def test_whitespace(self):
        input_title = "  Song Title  "
        expected_output = "Song Title"
        self.assertEqual(clean_title(input_title), expected_output)

    def test_explicit_removal(self):
        input_title = "Downfall (feat. Lexi Norton)"
        expected_output = "Downfall"
        self.assertEqual(clean_title(input_title), expected_output)


class CleanArtistTests(TestCase):
    def test_semicolons_and_commas(self):
        input_artist = "Virual Riot; Submatik, Holly Drummond"
        expected_output = "Virual Riot Submatik Holly Drummond"
        self.assertEqual(clean_artist(input_artist), expected_output)

    def test_semicolons_only(self):
        input_artist = "Artist One; Artist Two"
        expected_output = "Artist One Artist Two"
        self.assertEqual(clean_artist(input_artist), expected_output)

    def test_commas_only(self):
        input_artist = "Artist One, Artist Two"
        expected_output = "Artist One Artist Two"
        self.assertEqual(clean_artist(input_artist), expected_output)

    def test_no_separators(self):
        input_artist = "Single Artist"
        expected_output = "Single Artist"
        self.assertEqual(clean_artist(input_artist), expected_output)

    def test_whitespace(self):
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

    def test_explicit_word(self):
        input_title = "Song Title explicit"
        expected_output = "Song Title"
        self.assertEqual(remove_explicit(input_title), expected_output)

    def test_no_explicit(self):
        input_title = "Song Title"
        expected_output = "Song Title"
        self.assertEqual(remove_explicit(input_title), expected_output)

    def test_no_explicit(self):
        input_title = "hongdae guy explicit thoughts"
        expected_output = "hongdae guy explicit thoughts"
        self.assertEqual(remove_explicit(input_title), expected_output)
