from contextlib import redirect_stdout
from io import StringIO
import os
import shutil
import tempfile
from unittest import TestCase
from unittest.mock import patch

import pytest
from selenium.common.exceptions import TimeoutException

from artists_features import find_artists_and_features
from file_metadata import (
    NoTagError,
    clear_lyrics,
    get_artist,
    get_cover_art,
    get_lyrics,
    get_song_title,
    set_album_title,
    set_artist,
    set_song_title,
)
from lyrics import (
    LyricsLookupFailed,
    LyricsNotFound,
    genius_page_blocked,
    get_html_genius,
    get_lyrics_genius,
    lyrics_failure_reason,
)
from parse_and_clean import clean_title
from soundscrape import process_dir, process_file


@pytest.mark.xdist_group(name="genius_online_c")
class LyricsFromFileTests(TestCase):
    @pytest.mark.timeout(300)
    def test_knock2_rookie(self):
        filepath = "test/noaudio/Knock2_nolimit/Knock2 - 01. rookie (Explicit).flac"
        artist = get_artist(filepath)
        title = clean_title(get_song_title(filepath))
        artists_and_features = find_artists_and_features(artist, title)

        actual = get_lyrics_genius(
            ", ".join(artists_and_features.artists), title, cache=False
        )

        expected_path = os.path.join("test/test_output_genius", "knock2_rookie.txt")
        with open(expected_path, "r", encoding="utf-8") as f:
            expected = f.read()

        self.assertEqual(actual, expected)


def stage_tagged_song(work):
    dest = os.path.join(work, "song.mp3")
    shutil.copy2("test/yeet.mp3", dest)
    set_artist(dest, "Skrillex; Bobby Raps")
    set_song_title(dest, "Leave Me Like This")
    set_album_title(dest, "Quest For Fire")
    clear_lyrics(dest)
    return dest


class MissingGeniusLyricsTests(TestCase):
    def test_process_dir_skips_missing_genius_lyrics(self):
        work = tempfile.mkdtemp()
        try:
            stage_tagged_song(work)

            def no_match(artist, title, cache=False):
                raise LyricsNotFound(f"No Genius match for {artist} - {title}")

            output = StringIO()
            with patch("soundscrape.get_lyrics_genius", no_match):
                with redirect_stdout(output):
                    process_dir(
                        work,
                        no_art_select=True,
                        embed_lyrics=True,
                        resolve_artists_with_ai=False,
                        skip_web=True,
                        agentic=True,
                    )

            text = output.getvalue()
            self.assertIn("WARNING: no lyrics found for Leave Me Like This.", text)
            self.assertNotIn("lookup failed", text)
            out = os.path.join(work, "Leave Me Like This.mp3")
            self.assertTrue(os.path.exists(out))
            self.assertEqual(get_artist(out), "Skrillex; Bobby Raps")
            self.assertEqual(get_song_title(out), "Leave Me Like This")
            self.assertGreater(len(get_cover_art(out)), 0)
            with self.assertRaises(NoTagError):
                get_lyrics(out)
        finally:
            shutil.rmtree(work)

    def test_process_dir_browser_timeout_is_not_missing_lyrics(self):
        work = tempfile.mkdtemp()
        try:
            stage_tagged_song(work)

            def timed_out(artist, title, cache=False):
                raise TimeoutException(msg="", stacktrace=["at chrome.secret.stack"])

            output = StringIO()
            with patch("soundscrape.get_lyrics_genius", timed_out):
                with redirect_stdout(output):
                    with self.assertRaises(LyricsLookupFailed):
                        process_dir(
                            work,
                            no_art_select=True,
                            embed_lyrics=True,
                            resolve_artists_with_ai=False,
                            skip_web=True,
                            agentic=True,
                        )

            text = output.getvalue()
            self.assertIn("WARNING: lyrics lookup failed for Leave Me Like This.", text)
            self.assertIn("not verified missing", text)
            self.assertIn("Genius page timed out", text)
            self.assertNotIn("no lyrics found", text)
            self.assertNotIn("Stacktrace", text)
            self.assertNotIn("chrome.secret.stack", text)
            out = os.path.join(work, "Leave Me Like This.mp3")
            self.assertTrue(os.path.exists(out))
            self.assertEqual(get_artist(out), "Skrillex; Bobby Raps")
            self.assertEqual(get_song_title(out), "Leave Me Like This")
            self.assertGreater(len(get_cover_art(out)), 0)
            with self.assertRaises(NoTagError):
                get_lyrics(out)
        finally:
            shutil.rmtree(work)

    def test_process_dir_empty_page_is_not_a_lookup_failure(self):
        work = tempfile.mkdtemp()
        try:
            stage_tagged_song(work)

            def empty_page(artist, title, cache=False):
                return ""

            output = StringIO()
            with patch("soundscrape.get_lyrics_genius", empty_page):
                with redirect_stdout(output):
                    process_dir(
                        work,
                        no_art_select=True,
                        embed_lyrics=True,
                        resolve_artists_with_ai=False,
                        skip_web=True,
                        agentic=True,
                    )

            text = output.getvalue()
            self.assertNotIn("lookup failed", text)
            self.assertNotIn("no lyrics found", text)
            out = os.path.join(work, "Leave Me Like This.mp3")
            self.assertTrue(os.path.exists(out))
            self.assertEqual(get_song_title(out), "Leave Me Like This")
            with self.assertRaises(NoTagError):
                get_lyrics(out)
        finally:
            shutil.rmtree(work)

    def test_process_file_keeps_file_when_lyrics_lookup_fails(self):
        work = tempfile.mkdtemp()
        try:
            src = stage_tagged_song(work)

            class DummyDriver:
                def quit(self):
                    return None

            def timed_out(artist, title, cache=False):
                raise LyricsLookupFailed("Genius page timed out")

            with patch("soundscrape.get_lyrics_genius", timed_out):
                with patch("soundscrape.search_cover_art_by_text", return_value=None):
                    with patch(
                        "soundscrape.search_cover_art_soundcloud", return_value=None
                    ):
                        with patch(
                            "soundscrape.search_google_images", return_value=None
                        ):
                            with patch(
                                "soundscrape.create_stealth_driver",
                                return_value=DummyDriver(),
                            ):
                                with self.assertRaises(LyricsLookupFailed):
                                    process_file(
                                        src,
                                        no_art_select=True,
                                        resolve_artists_with_ai=False,
                                        agentic=True,
                                    )

            out = os.path.join(work, "Leave Me Like This.mp3")
            self.assertTrue(os.path.exists(out))
            self.assertFalse(os.path.exists(src))
            self.assertEqual(get_artist(out), "Skrillex; Bobby Raps")
            self.assertEqual(get_song_title(out), "Leave Me Like This")
            self.assertGreater(len(get_cover_art(out)), 0)
            with self.assertRaises(NoTagError):
                get_lyrics(out)
        finally:
            shutil.rmtree(work)


class GeniusLookupFailureTests(TestCase):
    def test_failure_reason_empty_timeout_is_not_blank(self):
        reason = lyrics_failure_reason(TimeoutException(msg=""))
        self.assertEqual(reason, "Genius page timed out")

    def test_failure_reason_drops_stacktrace(self):
        err = TimeoutException(msg="", stacktrace=["at chrome.secret.stack"])
        reason = lyrics_failure_reason(err)
        self.assertEqual(reason, "Genius page timed out")
        self.assertNotIn("chrome.secret.stack", reason)
        self.assertNotIn("Stacktrace", reason)
        self.assertNotIn("chrome.secret.stack", str(LyricsLookupFailed(reason)))

    def test_human_check_page_is_blocked(self):
        html = "<html><body>Sorry, we have to make sure you're a human</body></html>"
        self.assertTrue(genius_page_blocked(html, "Genius"))

    def test_cloudflare_challenge_page_is_blocked(self):
        html = "<html><script src='/cdn-cgi/challenge-platform/h/g/orchestrate/jsch/v1'></script></html>"
        self.assertTrue(genius_page_blocked(html, "Just a moment..."))

    def test_lyric_page_is_not_blocked(self):
        html = "<div class='Lyrics__Container'>synthetic line</div>"
        self.assertFalse(genius_page_blocked(html, "Synthetic Song Lyrics | Genius"))

    def test_human_check_is_a_lookup_failure(self):
        created = []

        class FakeDriver:
            def __init__(self):
                self.page_source = (
                    "<html>Sorry, we have to make sure you're a human</html>"
                )
                self.title = "Genius"
                created.append(self)

            def get(self, url):
                return None

            def quit(self):
                return None

        class InstantWait:
            def __init__(self, driver, timeout):
                return None

            def until(self, condition):
                raise TimeoutException(msg="", stacktrace=["at chrome.secret.stack"])

        with patch("lyrics.create_stealth_driver", side_effect=FakeDriver):
            with patch("lyrics.WebDriverWait", InstantWait):
                with self.assertRaises(LyricsLookupFailed) as caught:
                    get_html_genius("Synthetic Artist", "Synthetic Title")

        self.assertEqual(len(created), 2)
        self.assertIn("human check", str(caught.exception))
        self.assertNotIn("Stacktrace", str(caught.exception))
        self.assertNotIn("chrome.secret.stack", str(caught.exception))

    def test_timeout_does_not_report_selenium_stacktrace(self):
        class FakeDriver:
            def __init__(self):
                self.page_source = "<html><body>search</body></html>"
                self.title = "Genius Search"

            def get(self, url):
                return None

            def quit(self):
                return None

        class InstantWait:
            def __init__(self, driver, timeout):
                return None

            def until(self, condition):
                raise TimeoutException(msg="", stacktrace=["at chrome.secret.stack"])

        with patch("lyrics.create_stealth_driver", side_effect=FakeDriver):
            with patch("lyrics.WebDriverWait", InstantWait):
                with self.assertRaises(LyricsLookupFailed) as caught:
                    get_html_genius("Synthetic Artist", "Synthetic Title")

        message = str(caught.exception)
        self.assertIn("Genius page timed out", message)
        self.assertNotIn("chrome.secret.stack", message)
        self.assertNotIn("Stacktrace", message)
        self.assertNotEqual(message.strip(), "")

    def test_no_html_is_not_found_not_empty_lyrics(self):
        with patch("lyrics.get_html_genius", return_value=None):
            with self.assertRaises(LyricsNotFound):
                get_lyrics_genius("Synthetic Artist", "Synthetic Title")

    def test_loaded_page_returns_synthetic_lyric_line(self):
        html_path = os.path.join("test", "test_html_genius_basic", "text.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        with patch("lyrics.get_html_genius", return_value=html):
            lyrics = get_lyrics_genius("Synthetic Artist", "Synthetic Title")
        self.assertEqual(lyrics, "These are the lyrics")
