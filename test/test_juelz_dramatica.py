import os
import shutil
import tempfile
from unittest import TestCase

import pytest

from file_metadata import get_album_artist, get_artist, get_song_title
from soundscrape import process_dir


DIR = "test/noaudio/Juelz_DRAMATICA"


def _path_for_title(work, title):
    for name in os.listdir(work):
        if not name.lower().endswith(".flac"):
            continue
        path = os.path.join(work, name)
        if get_song_title(path) == title:
            return path
    raise AssertionError(f"{title!r} not in {os.listdir(work)}")


def _run(credit_mode):
    work = tempfile.mkdtemp()
    for name in os.listdir(DIR):
        shutil.copy2(os.path.join(DIR, name), os.path.join(work, name))
    process_dir(
        work,
        no_art_select=True,
        embed_lyrics=False,
        skip_web=True,
        credit_mode=credit_mode,
    )
    return work


@pytest.mark.xdist_group(name="juelz_dramatica")
class JuelzAllArtistsTests(TestCase):
    work: str

    @classmethod
    def setUpClass(cls):
        cls.work = _run("all_artists")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.work)

    def test_3peat(self):
        path = _path_for_title(self.work, "3PEAT")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "3PEAT")

    def test_direct_it_2_the_roof(self):
        path = _path_for_title(self.work, "DIRECT IT 2 THE ROOF")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "DIRECT IT 2 THE ROOF")

    def test_dont_say_a_word(self):
        path = _path_for_title(self.work, "DON'T SAY A WORD")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "DON'T SAY A WORD")

    def test_higher(self):
        path = _path_for_title(self.work, "HIGHER")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "HIGHER")

    def test_inconvenient(self):
        path = _path_for_title(self.work, "Inconvenient")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "Inconvenient")

    def test_motion_detected(self):
        path = _path_for_title(self.work, "Motion Detected")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "Motion Detected")

    def test_shinigami_flow(self):
        path = _path_for_title(self.work, "SHINIGAMI FLOW")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "SHINIGAMI FLOW")

    def test_someone_like_u(self):
        path = _path_for_title(self.work, "SOMEONE LIKE U")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "SOMEONE LIKE U")

    def test_spiralling(self):
        path = _path_for_title(self.work, "Spiralling")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "Spiralling")

    def test_start_the_drama(self):
        path = _path_for_title(self.work, "start the drama")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "start the drama")

    def test_wakeup(self):
        path = _path_for_title(self.work, "wakeup")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz; Angst")
        self.assertEqual(get_song_title(path), "wakeup")

    def test_options(self):
        path = _path_for_title(self.work, "options")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz; Hex Cougar; Adam Fadi")
        self.assertEqual(get_song_title(path), "options")

    def test_go_baby(self):
        path = _path_for_title(self.work, "GO baby")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz; Nef The Pharoah")
        self.assertEqual(get_song_title(path), "GO baby")

    def test_my_my_my(self):
        path = _path_for_title(self.work, "MY MY MY")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz; Z3LLA")
        self.assertEqual(get_song_title(path), "MY MY MY")

    def test_in_the_am(self):
        path = _path_for_title(self.work, "In the AM")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz; midwxst")
        self.assertEqual(get_song_title(path), "In the AM")

    def test_lucky(self):
        path = _path_for_title(self.work, "Lucky")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz; Titus")
        self.assertEqual(get_song_title(path), "Lucky")


@pytest.mark.xdist_group(name="juelz_dramatica")
class JuelzAllFeaturesTests(TestCase):
    work: str

    @classmethod
    def setUpClass(cls):
        cls.work = _run("all_features")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.work)

    def test_3peat(self):
        path = _path_for_title(self.work, "3PEAT")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "3PEAT")

    def test_direct_it_2_the_roof(self):
        path = _path_for_title(self.work, "DIRECT IT 2 THE ROOF")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "DIRECT IT 2 THE ROOF")

    def test_dont_say_a_word(self):
        path = _path_for_title(self.work, "DON'T SAY A WORD")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "DON'T SAY A WORD")

    def test_higher(self):
        path = _path_for_title(self.work, "HIGHER")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "HIGHER")

    def test_inconvenient(self):
        path = _path_for_title(self.work, "Inconvenient")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "Inconvenient")

    def test_motion_detected(self):
        path = _path_for_title(self.work, "Motion Detected")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "Motion Detected")

    def test_shinigami_flow(self):
        path = _path_for_title(self.work, "SHINIGAMI FLOW")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "SHINIGAMI FLOW")

    def test_someone_like_u(self):
        path = _path_for_title(self.work, "SOMEONE LIKE U")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "SOMEONE LIKE U")

    def test_spiralling(self):
        path = _path_for_title(self.work, "Spiralling")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "Spiralling")

    def test_start_the_drama(self):
        path = _path_for_title(self.work, "start the drama")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz")
        self.assertEqual(get_song_title(path), "start the drama")

    def test_wakeup(self):
        path = _path_for_title(self.work, "wakeup (feat. Angst)")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz; Angst")
        self.assertEqual(get_song_title(path), "wakeup (feat. Angst)")

    def test_options(self):
        path = _path_for_title(self.work, "options (feat. Hex Cougar, Adam Fadi)")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz; Hex Cougar; Adam Fadi")
        self.assertEqual(get_song_title(path), "options (feat. Hex Cougar, Adam Fadi)")

    def test_go_baby(self):
        path = _path_for_title(self.work, "GO baby (feat. Nef The Pharoah)")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz; Nef The Pharoah")
        self.assertEqual(get_song_title(path), "GO baby (feat. Nef The Pharoah)")

    def test_my_my_my(self):
        path = _path_for_title(self.work, "MY MY MY (feat. Z3LLA)")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz; Z3LLA")
        self.assertEqual(get_song_title(path), "MY MY MY (feat. Z3LLA)")

    def test_in_the_am(self):
        path = _path_for_title(self.work, "In the AM (feat. midwxst)")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz; midwxst")
        self.assertEqual(get_song_title(path), "In the AM (feat. midwxst)")

    def test_lucky(self):
        path = _path_for_title(self.work, "Lucky (feat. Titus)")
        self.assertEqual(get_album_artist(path), "Juelz")
        self.assertEqual(get_artist(path), "Juelz; Titus")
        self.assertEqual(get_song_title(path), "Lucky (feat. Titus)")
