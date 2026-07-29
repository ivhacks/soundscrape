import os
from unittest import TestCase

import pytest

from lyrics import get_lyrics_genius


def real_song_online_test(tester: TestCase, name, artist, title):
    expected_output_filename = os.path.join("test/test_output_genius", name + ".txt")

    with open(expected_output_filename, "r", encoding="utf-8") as f:
        expected_output = f.read()

    actual_output = get_lyrics_genius(artist, title, cache=False)
    tester.assertEqual(actual_output, expected_output)


# Cap concurrent chromes: 3 groups of 3 (full ungroup thrash under -n auto)
@pytest.mark.xdist_group(name="genius_online_a")
class RealSongOnlineGroupA(TestCase):
    @pytest.mark.timeout(300)
    def test_chase_atlantic_beauty_in_death(self):
        real_song_online_test(
            self, "beauty_in_death", "Chase Atlantic", "Beauty In Death"
        )

    @pytest.mark.timeout(300)
    def test_chase_atlantic_cassie(self):
        real_song_online_test(self, "cassie", "Chase Atlantic", "Cassie")

    @pytest.mark.timeout(300)
    def test_chase_atlantic_call_me_back(self):
        real_song_online_test(self, "call_me_back", "Chase Atlantic", "Call Me Back")


@pytest.mark.xdist_group(name="genius_online_b")
class RealSongOnlineGroupB(TestCase):
    @pytest.mark.timeout(300)
    def test_lil_nas_x_old_town_road(self):
        real_song_online_test(
            self, "lil_nas_x_old_town_road", "Lil Nas X", "Old Town Road"
        )

    @pytest.mark.timeout(300)
    def test_cloudfield_artificial(self):
        real_song_online_test(self, "cloudfield_artificial", "Cloudfield", "Artificial")

    @pytest.mark.timeout(300)
    def test_chase_atlantic_escort(self):
        real_song_online_test(self, "chase_atlantic_escort", "Chase Atlantic", "Escort")


@pytest.mark.xdist_group(name="genius_online_c")
class RealSongOnlineGroupC(TestCase):
    @pytest.mark.timeout(300)
    def test_chase_atlantic_i_never_existed(self):
        real_song_online_test(
            self, "chase_atlantic_i_never_existed", "Chase Atlantic", "I Never Existed"
        )

    @pytest.mark.timeout(300)
    def test_chase_atlantic_obsessive(self):
        real_song_online_test(
            self, "chase_atlantic_obsessive", "Chase Atlantic", "Obsessive"
        )

    @pytest.mark.timeout(300)
    def test_essenger_lexi_norton_downfall(self):
        real_song_online_test(
            self, "essenger_lexi_norton_downfall", "Essenger, Lexi Norton", "Downfall"
        )


@pytest.mark.xdist_group(name="genius_online_d")
class RealSongOnlineGroupD(TestCase):
    @pytest.mark.timeout(300)
    def test_porter_robinson_goodbye_to_a_world(self):
        real_song_online_test(
            self,
            "porter_robinson_goodbye_to_a_world",
            "Porter Robinson",
            "Goodbye To A World",
        )

    @pytest.mark.timeout(300)
    def test_eminem_lose_yourself(self):
        real_song_online_test(self, "eminem_lose_yourself", "Eminem", "Lose Yourself")

    @pytest.mark.timeout(300)
    def test_doja_cat_say_so(self):
        real_song_online_test(self, "doja_cat_say_so", "Doja Cat", "Say So")

    @pytest.mark.timeout(300)
    def test_zedd_epos_instrumental(self):
        lyrics = get_lyrics_genius("Zedd", "Epos", cache=False)
        self.assertEqual(lyrics, "")
