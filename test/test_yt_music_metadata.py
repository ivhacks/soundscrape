from unittest import TestCase

import pytest

from stealth_driver import create_stealth_driver
from youtube import TrackMetadata, get_yt_music_metadata


HEADLESS = True


class YTMusicMetadataTests(TestCase):
    driver = None

    @classmethod
    def setUpClass(cls):
        # Create a shared driver instance for all tests
        cls.driver = create_stealth_driver(headless=HEADLESS)

    @classmethod
    def tearDownClass(cls):
        # Clean up the shared driver
        if cls.driver:
            cls.driver.quit()

    def _assert_metadata_matches(self, link: str, expected_metadata: TrackMetadata):
        result = get_yt_music_metadata(link, self.driver)

        # Test individual fields to be more flexible with YouTube changes
        self.assertEqual(result.title, expected_metadata.title)
        self.assertEqual(result.artists, expected_metadata.artists)
        self.assertEqual(result.featured_artists, expected_metadata.featured_artists)
        self.assertEqual(result.album, expected_metadata.album)
        self.assertEqual(result.year, expected_metadata.year)

    @pytest.mark.timeout(30)
    def test_mameyudoufu_i_dont_know_what_im_doing(self):
        link = "https://music.youtube.com/watch?v=meR1lgaP4ew"
        expected_metadata = TrackMetadata(
            title="I don't know what I'm doing",
            artists=["Mameyudoufu"],
            featured_artists=[],
            album="I don't know what I'm doing",
            year=2021,
        )
        self._assert_metadata_matches(link, expected_metadata)

    @pytest.mark.timeout(30)
    def test_atmozfears_release(self):
        link = "https://music.youtube.com/watch?v=B-7m0EfW7LM"
        expected_metadata = TrackMetadata(
            title="Release",
            artists=["Atmozfears"],
            featured_artists=["David Spekter"],
            album="Release",
            year=None,
        )
        self._assert_metadata_matches(link, expected_metadata)

    @pytest.mark.timeout(30)
    def test_ghosts_n_stuff(self):
        link = "https://music.youtube.com/watch?v=MUBf64EQA5I"
        expected_metadata = TrackMetadata(
            title="Ghosts 'n' Stuff (Extended Mix)",
            artists=["deadmau5"],
            featured_artists=["Rob Swire"],
            album="For Lack of A Better Name (The Extended Mixes)",
            year=2009,
        )
        self._assert_metadata_matches(link, expected_metadata)

    @pytest.mark.timeout(30)
    def test_clarity(self):
        link = "https://music.youtube.com/watch?v=Lur-rvf6A1c"
        expected_metadata = TrackMetadata(
            title="Clarity",
            artists=["Zedd"],
            featured_artists=["Foxes"],
            album="Clarity",
            year=2012,
        )
        self._assert_metadata_matches(link, expected_metadata)

    @pytest.mark.timeout(30)
    def test_dont_you_worry_child(self):
        link = "https://music.youtube.com/watch?v=3mWbRB3Y4R8"
        expected_metadata = TrackMetadata(
            title="Don't You Worry Child (Radio Edit)",
            artists=["Swedish House Mafia"],
            featured_artists=["John Martin"],
            album="Don't You Worry Child",
            year=2012,
        )
        self._assert_metadata_matches(link, expected_metadata)

    @pytest.mark.timeout(30)
    def test_get_lucky(self):
        link = "https://music.youtube.com/watch?v=4D7u5KF7SP8"
        expected_metadata = TrackMetadata(
            title="Get Lucky",
            artists=["Daft Punk"],
            featured_artists=["Pharrell Williams", "Nile Rodgers"],
            album="Random Access Memories",
            year=2013,
        )
        self._assert_metadata_matches(link, expected_metadata)

    @pytest.mark.timeout(30)
    def test_i_remember(self):
        link = "https://music.youtube.com/watch?v=9BND-QKR-7c"
        expected_metadata = TrackMetadata(
            title="I Remember (Vocal Mix)",
            artists=["deadmau5", "Kaskade"],
            featured_artists=[],
            album="Random Album Title (Unmixed Extended Versions)",
            year=2008,
        )
        self._assert_metadata_matches(link, expected_metadata)

    @pytest.mark.timeout(30)
    def test_heroes(self):
        link = "https://music.youtube.com/watch?v=y0VAozNZN3Q"
        expected_metadata = TrackMetadata(
            title="Heroes (we could be)",
            artists=["Alesso"],
            featured_artists=["Tove Lo"],
            album="Forever",
            year=2015,
        )
        self._assert_metadata_matches(link, expected_metadata)
