from besttest import Stage, run

WORKER = "http://192.168.122.234:9009"
IMAGE = "soundscrape-test"


class TestAlbumSearch(Stage):
    @staticmethod
    def task_knock2_fast_n_slow():
        run(WORKER, IMAGE, "pytest -xvs test/test_album_search.py::AlbumSearchTests::test_knock2_fast_n_slow")

    @staticmethod
    def task_audien_bittersweet():
        run(WORKER, IMAGE, "pytest -xvs test/test_album_search.py::AlbumSearchTests::test_audien_bittersweet")

    @staticmethod
    def task_kevin_gates_2_phones():
        run(WORKER, IMAGE, "pytest -xvs test/test_album_search.py::AlbumSearchTests::test_kevin_gates_2_phones")

    @staticmethod
    def task_most_famous_artist_skrillex():
        run(WORKER, IMAGE, "pytest -xvs test/test_album_search.py::AlbumSearchTests::test_most_famous_artist_skrillex")

    @staticmethod
    def task_ignores_unreleased_albums_first_response():
        run(WORKER, IMAGE, "pytest -xvs test/test_album_search.py::PromptTests::test_ignores_unreleased_albums_first_response")

    @staticmethod
    def task_ignores_unreleased_albums_second_response():
        run(WORKER, IMAGE, "pytest -xvs test/test_album_search.py::PromptTests::test_ignores_unreleased_albums_second_response")


class TestAnthropicApi(Stage):
    @staticmethod
    def task_basic():
        run(WORKER, IMAGE, "pytest -xvs test/test_anthropic_api.py::AnthropicApiTests::test_basic")

    @staticmethod
    def task_image_comprehension():
        run(WORKER, IMAGE, "pytest -xvs test/test_anthropic_api.py::AnthropicApiTests::test_image_comprehension")


class TestArtSearch(Stage):
    @staticmethod
    def task_knock2_feel_u_luv_me_single():
        run(WORKER, IMAGE, "pytest -xvs test/test_art_search.py::ArtSearchTests::test_knock2_feel_u_luv_me_single")

    @staticmethod
    def task_knock2_feel_u_luv_me_album():
        run(WORKER, IMAGE, "pytest -xvs test/test_art_search.py::ArtSearchTests::test_knock2_feel_u_luv_me_album")


class TestArtistsAndFeatures(Stage):
    @staticmethod
    def task_porter_robinson_divinity():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::ArtistsAndFeaturesTest::test_porter_robinson_divinity")

    @staticmethod
    def task_porter_robinson_sad_machine():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::ArtistsAndFeaturesTest::test_porter_robinson_sad_machine")

    @staticmethod
    def task_porter_robinson_years_of_war():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::ArtistsAndFeaturesTest::test_porter_robinson_years_of_war")

    @staticmethod
    def task_porter_robinson_flicker():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::ArtistsAndFeaturesTest::test_porter_robinson_flicker")

    @staticmethod
    def task_porter_robinson_fresh_static_snow():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::ArtistsAndFeaturesTest::test_porter_robinson_fresh_static_snow")

    @staticmethod
    def task_porter_robinson_polygon_dust():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::ArtistsAndFeaturesTest::test_porter_robinson_polygon_dust")

    @staticmethod
    def task_porter_robinson_hear_the_bells():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::ArtistsAndFeaturesTest::test_porter_robinson_hear_the_bells")

    @staticmethod
    def task_porter_robinson_natural_light():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::ArtistsAndFeaturesTest::test_porter_robinson_natural_light")

    @staticmethod
    def task_porter_robinson_lionhearted():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::ArtistsAndFeaturesTest::test_porter_robinson_lionhearted")

    @staticmethod
    def task_porter_robinson_sea_of_voices():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::ArtistsAndFeaturesTest::test_porter_robinson_sea_of_voices")

    @staticmethod
    def task_porter_robinson_fellow_feeling():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::ArtistsAndFeaturesTest::test_porter_robinson_fellow_feeling")

    @staticmethod
    def task_porter_robinson_goodbye_to_a_world():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::ArtistsAndFeaturesTest::test_porter_robinson_goodbye_to_a_world")

    @staticmethod
    def task_one_artist_one_feature():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::PromptTests::test_one_artist_one_feature")

    @staticmethod
    def task_no_features():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::PromptTests::test_no_features")

    @staticmethod
    def task_zedd_clarity_with_features():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::PromptTests::test_zedd_clarity_with_features")

    @staticmethod
    def task_isoknock_pain_multiple_artists():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::PromptTests::test_isoknock_pain_multiple_artists")

    @staticmethod
    def task_ninajirachi_battery_death_single_artist():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::PromptTests::test_ninajirachi_battery_death_single_artist")

    @staticmethod
    def task_skrillex_rumble_multiple_artists():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::PromptTests::test_skrillex_rumble_multiple_artists")

    @staticmethod
    def task_single_artist_with_feature():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::PromptTests::test_single_artist_with_feature")

    @staticmethod
    def task_multiple_artists_no_features():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::PromptTests::test_multiple_artists_no_features")

    @staticmethod
    def task_single_artist_no_features():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::PromptTests::test_single_artist_no_features")

    @staticmethod
    def task_multiple_artists_with_features():
        run(WORKER, IMAGE, "pytest -xvs test/test_artists_and_features.py::PromptTests::test_multiple_artists_with_features")


class TestBandcampSearch(Stage):
    @staticmethod
    def task_carbon_based_lifeforms_derelicts():
        run(WORKER, IMAGE, "pytest -xvs test/test_bandcamp_search.py::TestBandcampSearch::test_carbon_based_lifeforms_derelicts")

    @staticmethod
    def task_jousboxx_springtime():
        run(WORKER, IMAGE, "pytest -xvs test/test_bandcamp_search.py::TestBandcampSearch::test_jousboxx_springtime")

    @staticmethod
    def task_au5_cataclysm():
        run(WORKER, IMAGE, "pytest -xvs test/test_bandcamp_search.py::TestBandcampSearch::test_au5_cataclysm")

    @staticmethod
    def task_second_flight_instead_of_one():
        run(WORKER, IMAGE, "pytest -xvs test/test_bandcamp_search.py::TestBandcampSearch::test_second_flight_instead_of_one")


class TestBeatportSearch(Stage):
    @staticmethod
    def task_knock2_feel_u_luv_me():
        run(WORKER, IMAGE, "pytest -xvs test/test_beatport_search.py::TestBeatportSearch::test_knock2_feel_u_luv_me")

    @staticmethod
    def task_zedd_martin_garrix_follow():
        run(WORKER, IMAGE, "pytest -xvs test/test_beatport_search.py::TestBeatportSearch::test_zedd_martin_garrix_follow")

    @staticmethod
    def task_rl_grime_bea_miller_slow_dive():
        run(WORKER, IMAGE, "pytest -xvs test/test_beatport_search.py::TestBeatportSearch::test_rl_grime_bea_miller_slow_dive")

    @staticmethod
    def task_zedd_clarity():
        run(WORKER, IMAGE, "pytest -xvs test/test_beatport_search.py::TestBeatportSearch::test_zedd_clarity")


class TestDb(Stage):
    @staticmethod
    def task_connect():
        run(WORKER, IMAGE, "pytest -xvs test/test_db.py::DatabaseTests::test_connect")


class TestGeniusBasic(Stage):
    @staticmethod
    def task_remove_newlines_basic():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::RemoveNewlineTests::test_remove_newlines_basic")

    @staticmethod
    def task_remove_newlines_advanced():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::RemoveNewlineTests::test_remove_newlines_advanced")

    @staticmethod
    def task_text():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_text")

    @staticmethod
    def task_start_newline():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_start_newline")

    @staticmethod
    def task_start_break():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_start_break")

    @staticmethod
    def task_mid_break():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_mid_break")

    @staticmethod
    def task_end_newline():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_end_newline")

    @staticmethod
    def task_end_break():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_end_break")

    @staticmethod
    def task_many_mid_breaks():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_many_mid_breaks")

    @staticmethod
    def task_parens():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_parens")

    @staticmethod
    def task_italics():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_italics")

    @staticmethod
    def task_italic_parens():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_italic_parens")

    @staticmethod
    def task_italic_parens_inverted():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_italic_parens_inverted")

    @staticmethod
    def task_square_brackets():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_square_brackets")

    @staticmethod
    def task_square_brackets_italics():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_square_brackets_italics")

    @staticmethod
    def task_square_brackets_italics_newlines():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_square_brackets_italics_newlines")

    @staticmethod
    def task_annotation():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_annotation")

    @staticmethod
    def task_annotation_same_line():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_annotation_same_line")

    @staticmethod
    def task_annotation_same_line_followed_by_punctuation():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_annotation_same_line_followed_by_punctuation")

    @staticmethod
    def task_annotation_break_outside_break():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_annotation_break_outside_break")

    @staticmethod
    def task_annotation_mid_breaks():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_annotation_mid_breaks")

    @staticmethod
    def task_annotation_mid_mixed():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_annotation_mid_mixed")

    @staticmethod
    def task_span():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_span")

    @staticmethod
    def task_multiple_lines():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_multiple_lines")

    @staticmethod
    def task_mid_breaks_with_square_brackets():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_mid_breaks_with_square_brackets")

    @staticmethod
    def task_mid_breaks_with_annotated_square_brackets():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_mid_breaks_with_annotated_square_brackets")

    @staticmethod
    def task_dumb_stupid_useless_div_between_lyric_divs():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_dumb_stupid_useless_div_between_lyric_divs")

    @staticmethod
    def task_annotated_sqaure_brackets():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_annotated_sqaure_brackets")

    @staticmethod
    def task_bold():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_bold")

    @staticmethod
    def task_italic_normal_parens_nested():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_italic_normal_parens_nested")

    @staticmethod
    def task_inline_parenthesized_italics():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_inline_parenthesized_italics")

    @staticmethod
    def task_inline_parenthesized_italics_inverted():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_inline_parenthesized_italics_inverted")

    @staticmethod
    def task_replace_on_unicode_apostrophe():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_replace_on_unicode_apostrophe")

    @staticmethod
    def task_replace_with_unicode_space():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_replace_with_unicode_space")

    @staticmethod
    def task_bold_with_space():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_basic.py::BasicTests::test_bold_with_space")


class TestGeniusRealSongs(Stage):
    @staticmethod
    def task_chase_atlantic_beauty_in_death():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_real_songs.py::RealSongTests::test_chase_atlantic_beauty_in_death")

    @staticmethod
    def task_chase_atlantic_cassie():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_real_songs.py::RealSongTests::test_chase_atlantic_cassie")

    @staticmethod
    def task_chase_atlantic_call_me_back():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_real_songs.py::RealSongTests::test_chase_atlantic_call_me_back")

    @staticmethod
    def task_lil_nas_x_old_town_road():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_real_songs.py::RealSongTests::test_lil_nas_x_old_town_road")

    @staticmethod
    def task_cloudfield_artificial():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_real_songs.py::RealSongTests::test_cloudfield_artificial")

    @staticmethod
    def task_chase_atlantic_escort():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_real_songs.py::RealSongTests::test_chase_atlantic_escort")

    @staticmethod
    def task_chase_atlantic_i_never_existed():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_real_songs.py::RealSongTests::test_chase_atlantic_i_never_existed")

    @staticmethod
    def task_chase_atlantic_obsessive():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_real_songs.py::RealSongTests::test_chase_atlantic_obsessive")

    @staticmethod
    def task_essenger_lexi_norton_downfall():
        run(WORKER, IMAGE, "pytest -xvs test/test_genius_real_songs.py::RealSongTests::test_essenger_lexi_norton_downfall")


class TestGetImg(Stage):
    @staticmethod
    def task_soundcloud_nolimit():
        run(WORKER, IMAGE, "pytest -xvs test/test_get_img.py::GetImageTests::test_soundcloud_nolimit")

    @staticmethod
    def task_bandcamp_beyond():
        run(WORKER, IMAGE, "pytest -xvs test/test_get_img.py::GetImageTests::test_bandcamp_beyond")

    @staticmethod
    def task_x_nolimit():
        run(WORKER, IMAGE, "pytest -xvs test/test_get_img.py::GetImageTests::test_x_nolimit")

    @staticmethod
    def task_instagram_nolimit_post():
        run(WORKER, IMAGE, "pytest -xvs test/test_get_img.py::GetImageTests::test_instagram_nolimit_post")

    @staticmethod
    def task_facebook_nolimit_post():
        run(WORKER, IMAGE, "pytest -xvs test/test_get_img.py::GetImageTests::test_facebook_nolimit_post")

    @staticmethod
    def task_genius_nolimit_album():
        run(WORKER, IMAGE, "pytest -xvs test/test_get_img.py::GetImageTests::test_genius_nolimit_album")

    @staticmethod
    def task_genius_dance_or_dead_song():
        run(WORKER, IMAGE, "pytest -xvs test/test_get_img.py::GetImageTests::test_genius_dance_or_dead_song")

    @staticmethod
    def task_threads_nolimit_post():
        run(WORKER, IMAGE, "pytest -xvs test/test_get_img.py::GetImageTests::test_threads_nolimit_post")


class TestGoogleImages(Stage):
    @staticmethod
    def task_google_images():
        run(WORKER, IMAGE, "pytest -xvs test/test_google_images.py::GoogleImagesTests::test_google_images")

    @staticmethod
    def task_litterbox_upload():
        run(WORKER, IMAGE, "pytest -xvs test/test_google_images.py::GoogleImagesTests::test_litterbox_upload")

    @staticmethod
    def task_serpapi_reverse_image():
        run(WORKER, IMAGE, "pytest -xvs test/test_google_images.py::GoogleImagesTests::test_serpapi_reverse_image")

    @staticmethod
    def task_serpapi_two_results():
        run(WORKER, IMAGE, "pytest -xvs test/test_google_images.py::GoogleImagesTests::test_serpapi_two_results")

    @staticmethod
    def task_serpapi_ten_results():
        run(WORKER, IMAGE, "pytest -xvs test/test_google_images.py::GoogleImagesTests::test_serpapi_ten_results")

    @staticmethod
    def task_scale_down_image_1():
        run(WORKER, IMAGE, "pytest -xvs test/test_google_images.py::GoogleImagesTests::test_scale_down_image_1")

    @staticmethod
    def task_scale_down_image_2():
        run(WORKER, IMAGE, "pytest -xvs test/test_google_images.py::GoogleImagesTests::test_scale_down_image_2")


class TestImgDiff(Stage):
    @staticmethod
    def task_1_vs_1_original():
        run(WORKER, IMAGE, "pytest -xvs test/test_img_diff.py::SameImageTests::test_1_vs_1_original")

    @staticmethod
    def task_1_vs_1_cropped():
        run(WORKER, IMAGE, "pytest -xvs test/test_img_diff.py::SameImageTests::test_1_vs_1_cropped")

    @staticmethod
    def task_1_vs_1_lossy_4x():
        run(WORKER, IMAGE, "pytest -xvs test/test_img_diff.py::SameImageTests::test_1_vs_1_lossy_4x")

    @staticmethod
    def task_1_vs_1_low_res():
        run(WORKER, IMAGE, "pytest -xvs test/test_img_diff.py::SameImageTests::test_1_vs_1_low_res")

    @staticmethod
    def task_1_vs_1_shrunk_blown_up():
        run(WORKER, IMAGE, "pytest -xvs test/test_img_diff.py::SameImageTests::test_1_vs_1_shrunk_blown_up")

    @staticmethod
    def task_1_vs_1_very_lossy():
        run(WORKER, IMAGE, "pytest -xvs test/test_img_diff.py::SameImageTests::test_1_vs_1_very_lossy")

    @staticmethod
    def task_x_image_vs_reference_image():
        run(WORKER, IMAGE, "pytest -xvs test/test_img_diff.py::SameImageTests::test_x_image_vs_reference_image")

    @staticmethod
    def task_1_vs_2_original():
        run(WORKER, IMAGE, "pytest -xvs test/test_img_diff.py::DifferentImageTests::test_1_vs_2_original")

    @staticmethod
    def task_1_vs_2_cropped():
        run(WORKER, IMAGE, "pytest -xvs test/test_img_diff.py::DifferentImageTests::test_1_vs_2_cropped")

    @staticmethod
    def task_1_vs_2_lossy_4x():
        run(WORKER, IMAGE, "pytest -xvs test/test_img_diff.py::DifferentImageTests::test_1_vs_2_lossy_4x")

    @staticmethod
    def task_1_vs_2_low_res():
        run(WORKER, IMAGE, "pytest -xvs test/test_img_diff.py::DifferentImageTests::test_1_vs_2_low_res")

    @staticmethod
    def task_1_vs_2_shrunk_blown_up():
        run(WORKER, IMAGE, "pytest -xvs test/test_img_diff.py::DifferentImageTests::test_1_vs_2_shrunk_blown_up")

    @staticmethod
    def task_1_vs_2_very_lossy():
        run(WORKER, IMAGE, "pytest -xvs test/test_img_diff.py::DifferentImageTests::test_1_vs_2_very_lossy")


class TestIntegration(Stage):
    @staticmethod
    def task_knock2_nolimit_purchased():
        run(WORKER, IMAGE, "pytest -xvs test/test_integration.py::IntegrationTests::test_knock2_nolimit_purchased")

    @staticmethod
    def task_porter_robinson_worlds_purchased():
        run(WORKER, IMAGE, "pytest -xvs test/test_integration.py::IntegrationTests::test_porter_robinson_worlds_purchased")


class TestMetadata(Stage):
    @staticmethod
    def task_get_year_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_get_year_mp3")

    @staticmethod
    def task_set_year_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_set_year_mp3")

    @staticmethod
    def task_clear_year_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_clear_year_mp3")

    @staticmethod
    def task_read_artist_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_read_artist_mp3")

    @staticmethod
    def task_read_album_artist_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_read_album_artist_mp3")

    @staticmethod
    def task_get_album_title_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_get_album_title_mp3")

    @staticmethod
    def task_set_album_title_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_set_album_title_mp3")

    @staticmethod
    def task_clear_album_title_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_clear_album_title_mp3")

    @staticmethod
    def task_get_artist_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_get_artist_mp3")

    @staticmethod
    def task_set_artist_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_set_artist_mp3")

    @staticmethod
    def task_clear_artist_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_clear_artist_mp3")

    @staticmethod
    def task_get_album_artist_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_get_album_artist_mp3")

    @staticmethod
    def task_set_album_artist_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_set_album_artist_mp3")

    @staticmethod
    def task_clear_album_artist_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_clear_album_artist_mp3")

    @staticmethod
    def task_get_song_title_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_get_song_title_mp3")

    @staticmethod
    def task_set_song_title_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_set_song_title_mp3")

    @staticmethod
    def task_clear_song_title_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_clear_song_title_mp3")

    @staticmethod
    def task_get_lyrics_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_get_lyrics_mp3")

    @staticmethod
    def task_set_lyrics_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_set_lyrics_mp3")

    @staticmethod
    def task_clear_lyrics_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_clear_lyrics_mp3")

    @staticmethod
    def task_get_cover_art_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_get_cover_art_mp3")

    @staticmethod
    def task_set_cover_art_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_set_cover_art_mp3")

    @staticmethod
    def task_clear_cover_art_mp3():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_clear_cover_art_mp3")

    @staticmethod
    def task_get_year_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_get_year_flac")

    @staticmethod
    def task_set_year_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_set_year_flac")

    @staticmethod
    def task_clear_year_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_clear_year_flac")

    @staticmethod
    def task_read_artist_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_read_artist_flac")

    @staticmethod
    def task_read_album_artist_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_read_album_artist_flac")

    @staticmethod
    def task_get_album_title_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_get_album_title_flac")

    @staticmethod
    def task_set_album_title_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_set_album_title_flac")

    @staticmethod
    def task_clear_album_title_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_clear_album_title_flac")

    @staticmethod
    def task_get_artist_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_get_artist_flac")

    @staticmethod
    def task_set_artist_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_set_artist_flac")

    @staticmethod
    def task_clear_artist_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_clear_artist_flac")

    @staticmethod
    def task_get_album_artist_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_get_album_artist_flac")

    @staticmethod
    def task_set_album_artist_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_set_album_artist_flac")

    @staticmethod
    def task_clear_album_artist_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_clear_album_artist_flac")

    @staticmethod
    def task_get_song_title_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_get_song_title_flac")

    @staticmethod
    def task_set_song_title_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_set_song_title_flac")

    @staticmethod
    def task_clear_song_title_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_clear_song_title_flac")

    @staticmethod
    def task_get_lyrics_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_get_lyrics_flac")

    @staticmethod
    def task_set_lyrics_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_set_lyrics_flac")

    @staticmethod
    def task_clear_lyrics_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_clear_lyrics_flac")

    @staticmethod
    def task_get_cover_art_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_get_cover_art_flac")

    @staticmethod
    def task_set_cover_art_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_set_cover_art_flac")

    @staticmethod
    def task_clear_cover_art_flac():
        run(WORKER, IMAGE, "pytest -xvs test/test_metadata.py::TestReadMetadata::test_clear_cover_art_flac")


class TestMisc(Stage):
    @staticmethod
    def task_predownloaded_html():
        run(WORKER, IMAGE, "pytest -xvs test/test_misc.py::MiscTests::test_predownloaded_html")

    @staticmethod
    def task_generate_lyrics_filename():
        run(WORKER, IMAGE, "pytest -xvs test/test_misc.py::MiscTests::test_generate_lyrics_filename")

    @staticmethod
    def task_lyrics_properly_terminated():
        run(WORKER, IMAGE, "pytest -xvs test/test_misc.py::MiscTests::test_lyrics_properly_terminated")


class TestParseClean(Stage):
    @staticmethod
    def task_clean_title_parens():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::CleanTitleTests::test_clean_title_parens")

    @staticmethod
    def task_clean_title_ft():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::CleanTitleTests::test_clean_title_ft")

    @staticmethod
    def task_clean_title_feat():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::CleanTitleTests::test_clean_title_feat")

    @staticmethod
    def task_clean_title_capital_feat():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::CleanTitleTests::test_clean_title_capital_feat")

    @staticmethod
    def task_clean_title_brackets():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::CleanTitleTests::test_clean_title_brackets")

    @staticmethod
    def task_clean_title_mixed():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::CleanTitleTests::test_clean_title_mixed")

    @staticmethod
    def task_clean_title_no_features():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::CleanTitleTests::test_clean_title_no_features")

    @staticmethod
    def task_clean_title_whitespace():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::CleanTitleTests::test_clean_title_whitespace")

    @staticmethod
    def task_explicit_removal():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::CleanTitleTests::test_explicit_removal")

    @staticmethod
    def task_clean_title_push():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::CleanTitleTests::test_clean_title_push")

    @staticmethod
    def task_clean_artist_semicolons_and_commas():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::CleanArtistTests::test_clean_artist_semicolons_and_commas")

    @staticmethod
    def task_clean_artist_semicolons_only():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::CleanArtistTests::test_clean_artist_semicolons_only")

    @staticmethod
    def task_clean_artist_commas_only():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::CleanArtistTests::test_clean_artist_commas_only")

    @staticmethod
    def task_clean_artist_no_separators():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::CleanArtistTests::test_clean_artist_no_separators")

    @staticmethod
    def task_clean_artist_whitespace():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::CleanArtistTests::test_clean_artist_whitespace")

    @staticmethod
    def task_brackets():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::RemoveExplicitTests::test_brackets")

    @staticmethod
    def task_explicit_end():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::RemoveExplicitTests::test_explicit_end")

    @staticmethod
    def task_no_explicit():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::RemoveExplicitTests::test_no_explicit")

    @staticmethod
    def task_legit_explicit():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::RemoveExplicitTests::test_legit_explicit")

    @staticmethod
    def task_parens():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::FindFeaturesTests::test_parens")

    @staticmethod
    def task_parens_capital_feat():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::FindFeaturesTests::test_parens_capital_feat")

    @staticmethod
    def task_parens_ft():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::FindFeaturesTests::test_parens_ft")

    @staticmethod
    def task_parens_featuring():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::FindFeaturesTests::test_parens_featuring")

    @staticmethod
    def task_no_parens_feat():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::FindFeaturesTests::test_no_parens_feat")

    @staticmethod
    def task_no_parens_capital_feat():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::FindFeaturesTests::test_no_parens_capital_feat")

    @staticmethod
    def task_no_parens_ft():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::FindFeaturesTests::test_no_parens_ft")

    @staticmethod
    def task_no_parens_featuring():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::FindFeaturesTests::test_no_parens_featuring")

    @staticmethod
    def task_no_features_found():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::FindFeaturesTests::test_no_features_found")

    @staticmethod
    def task_ampersand():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::ParseArtistsTests::test_ampersand")

    @staticmethod
    def task_comma():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::ParseArtistsTests::test_comma")

    @staticmethod
    def task_semicolon():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::ParseArtistsTests::test_semicolon")

    @staticmethod
    def task_and():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::ParseArtistsTests::test_and")

    @staticmethod
    def task_and_with_exception_ampersand():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::ParseArtistsTests::test_and_with_exception_ampersand")

    @staticmethod
    def task_and_with_exception_and():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::ParseArtistsTests::test_and_with_exception_and")

    @staticmethod
    def task_ampersand_with_exception_ampersand():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::ParseArtistsTests::test_ampersand_with_exception_ampersand")

    @staticmethod
    def task_ampersand_with_exception_and():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::ParseArtistsTests::test_ampersand_with_exception_and")

    @staticmethod
    def task_exception_solo():
        run(WORKER, IMAGE, "pytest -xvs test/test_parse_clean.py::ParseArtistsTests::test_exception_solo")


class TestSeleniumChrome(Stage):
    @staticmethod
    def task_selenium_and_chrome():
        run(WORKER, IMAGE, "pytest -xvs test/test_selenium_chrome.py::TestSeleniumAndChrome::test_selenium_and_chrome")


class TestSevendigitalSearch(Stage):
    @staticmethod
    def task_knock2_jade():
        run(WORKER, IMAGE, "pytest -xvs test/test_sevendigital_search.py::TestSevendigitalSearch::test_knock2_jade")

    @staticmethod
    def task_martin_garrix_album_search():
        run(WORKER, IMAGE, "pytest -xvs test/test_sevendigital_search.py::TestSevendigitalSearch::test_martin_garrix_album_search")

    @staticmethod
    def task_charli_xcx_360_track():
        run(WORKER, IMAGE, "pytest -xvs test/test_sevendigital_search.py::TestSevendigitalSearch::test_charli_xcx_360_track")

    @staticmethod
    def task_charli_xcx_brat_album():
        run(WORKER, IMAGE, "pytest -xvs test/test_sevendigital_search.py::TestSevendigitalSearch::test_charli_xcx_brat_album")

    @staticmethod
    def task_one_direction_little_white_lies():
        run(WORKER, IMAGE, "pytest -xvs test/test_sevendigital_search.py::TestSevendigitalSearch::test_one_direction_little_white_lies")

    @staticmethod
    def task_martin_garrix_dont_look_down():
        run(WORKER, IMAGE, "pytest -xvs test/test_sevendigital_search.py::TestSevendigitalSearch::test_martin_garrix_dont_look_down")

    @staticmethod
    def task_rl_grime_ucla():
        run(WORKER, IMAGE, "pytest -xvs test/test_sevendigital_search.py::TestSevendigitalSearch::test_rl_grime_ucla")


class TestSoundscrapeFileIo(Stage):
    @staticmethod
    def task_input_dir_output_dir_exists():
        run(WORKER, IMAGE, "pytest -xvs test/test_soundscrape_file_io.py::SoundScrapeFileIOTests::test_input_dir_output_dir_exists")

    @staticmethod
    def task_input_dir_output_dir_not_exists():
        run(WORKER, IMAGE, "pytest -xvs test/test_soundscrape_file_io.py::SoundScrapeFileIOTests::test_input_dir_output_dir_not_exists")

    @staticmethod
    def task_invalid_input_path():
        run(WORKER, IMAGE, "pytest -xvs test/test_soundscrape_file_io.py::SoundScrapeFileIOTests::test_invalid_input_path")

    @staticmethod
    def task_input_file_instead_of_directory_error():
        run(WORKER, IMAGE, "pytest -xvs test/test_soundscrape_file_io.py::SoundScrapeFileIOTests::test_input_file_instead_of_directory_error")

    @staticmethod
    def task_noaudio_basic():
        run(WORKER, IMAGE, "pytest -xvs test/test_soundscrape_file_io.py::SoundScrapeFileIOTests::test_noaudio_basic")

    @staticmethod
    def task_noaudio_preserves_all_tags():
        run(WORKER, IMAGE, "pytest -xvs test/test_soundscrape_file_io.py::SoundScrapeFileIOTests::test_noaudio_preserves_all_tags")

    @staticmethod
    def task_noaudio_multiple_files():
        run(WORKER, IMAGE, "pytest -xvs test/test_soundscrape_file_io.py::SoundScrapeFileIOTests::test_noaudio_multiple_files")


class TestSpotify(Stage):
    @staticmethod
    def task_hold_my_hand_album():
        run(WORKER, IMAGE, "pytest -xvs test/test_spotify.py::SpotifyTests::test_hold_my_hand_album")

    @staticmethod
    def task_hold_my_hand_single():
        run(WORKER, IMAGE, "pytest -xvs test/test_spotify.py::SpotifyTests::test_hold_my_hand_single")

    @staticmethod
    def task_single_and_album():
        run(WORKER, IMAGE, "pytest -xvs test/test_spotify.py::SpotifyTests::test_single_and_album")

    @staticmethod
    def task_incorrect_album_title():
        run(WORKER, IMAGE, "pytest -xvs test/test_spotify.py::SpotifyTests::test_incorrect_album_title")

    @staticmethod
    def task_lose_my_mind():
        run(WORKER, IMAGE, "pytest -xvs test/test_spotify.py::SpotifyTests::test_lose_my_mind")

    @staticmethod
    def task_push():
        run(WORKER, IMAGE, "pytest -xvs test/test_spotify.py::SpotifyTests::test_push")

    @staticmethod
    def task_cli_search_title_only():
        run(WORKER, IMAGE, "pytest -xvs test/test_spotify.py::SpotifyTests::test_cli_search_title_only")

    @staticmethod
    def task_cli_search_artist_only():
        run(WORKER, IMAGE, "pytest -xvs test/test_spotify.py::SpotifyTests::test_cli_search_artist_only")

    @staticmethod
    def task_cli_search_album_only():
        run(WORKER, IMAGE, "pytest -xvs test/test_spotify.py::SpotifyTests::test_cli_search_album_only")

    @staticmethod
    def task_cli_search_title_and_artist():
        run(WORKER, IMAGE, "pytest -xvs test/test_spotify.py::SpotifyTests::test_cli_search_title_and_artist")

    @staticmethod
    def task_cli_search_title_and_album():
        run(WORKER, IMAGE, "pytest -xvs test/test_spotify.py::SpotifyTests::test_cli_search_title_and_album")

    @staticmethod
    def task_cli_search_artist_and_album():
        run(WORKER, IMAGE, "pytest -xvs test/test_spotify.py::SpotifyTests::test_cli_search_artist_and_album")

    @staticmethod
    def task_cli_search_all_params():
        run(WORKER, IMAGE, "pytest -xvs test/test_spotify.py::SpotifyTests::test_cli_search_all_params")

    @staticmethod
    def task_compact_output():
        run(WORKER, IMAGE, "pytest -xvs test/test_spotify.py::SpotifyTests::test_compact_output")


class TestViewLink(Stage):
    @staticmethod
    def task_full_url():
        run(WORKER, IMAGE, "pytest -xvs test/test_view_link.py::TestNormalizeUrl::test_full_url")

    @staticmethod
    def task_no_protocol():
        run(WORKER, IMAGE, "pytest -xvs test/test_view_link.py::TestNormalizeUrl::test_no_protocol")

    @staticmethod
    def task_with_www():
        run(WORKER, IMAGE, "pytest -xvs test/test_view_link.py::TestNormalizeUrl::test_with_www")

    @staticmethod
    def task_www_no_protocol():
        run(WORKER, IMAGE, "pytest -xvs test/test_view_link.py::TestNormalizeUrl::test_www_no_protocol")

    @staticmethod
    def task_bandcamp_subdomain():
        run(WORKER, IMAGE, "pytest -xvs test/test_view_link.py::TestNormalizeUrl::test_bandcamp_subdomain")

    @staticmethod
    def task_http_protocol():
        run(WORKER, IMAGE, "pytest -xvs test/test_view_link.py::TestNormalizeUrl::test_http_protocol")

    @staticmethod
    def task_unknown_site():
        run(WORKER, IMAGE, "pytest -xvs test/test_view_link.py::TestViewLink::test_unknown_site")


class TestYtMusicMetadata(Stage):
    @staticmethod
    def task_mameyudoufu_i_dont_know_what_im_doing():
        run(WORKER, IMAGE, "pytest -xvs test/test_yt_music_metadata.py::YTMusicMetadataTests::test_mameyudoufu_i_dont_know_what_im_doing")

    @staticmethod
    def task_atmozfears_release():
        run(WORKER, IMAGE, "pytest -xvs test/test_yt_music_metadata.py::YTMusicMetadataTests::test_atmozfears_release")

    @staticmethod
    def task_ghosts_n_stuff():
        run(WORKER, IMAGE, "pytest -xvs test/test_yt_music_metadata.py::YTMusicMetadataTests::test_ghosts_n_stuff")

    @staticmethod
    def task_clarity():
        run(WORKER, IMAGE, "pytest -xvs test/test_yt_music_metadata.py::YTMusicMetadataTests::test_clarity")

    @staticmethod
    def task_dont_you_worry_child():
        run(WORKER, IMAGE, "pytest -xvs test/test_yt_music_metadata.py::YTMusicMetadataTests::test_dont_you_worry_child")

    @staticmethod
    def task_get_lucky():
        run(WORKER, IMAGE, "pytest -xvs test/test_yt_music_metadata.py::YTMusicMetadataTests::test_get_lucky")

    @staticmethod
    def task_i_remember():
        run(WORKER, IMAGE, "pytest -xvs test/test_yt_music_metadata.py::YTMusicMetadataTests::test_i_remember")

    @staticmethod
    def task_heroes():
        run(WORKER, IMAGE, "pytest -xvs test/test_yt_music_metadata.py::YTMusicMetadataTests::test_heroes")


if __name__ == "__main__":
    TestAlbumSearch.task_knock2_fast_n_slow()
    TestAlbumSearch.task_audien_bittersweet()
    TestAlbumSearch.task_kevin_gates_2_phones()
    TestAlbumSearch.task_most_famous_artist_skrillex()
    TestAlbumSearch.task_ignores_unreleased_albums_first_response()
    TestAlbumSearch.task_ignores_unreleased_albums_second_response()
    TestAnthropicApi.task_basic()
    TestAnthropicApi.task_image_comprehension()
    TestArtSearch.task_knock2_feel_u_luv_me_single()
    TestArtSearch.task_knock2_feel_u_luv_me_album()
    TestArtistsAndFeatures.task_porter_robinson_divinity()
    TestArtistsAndFeatures.task_porter_robinson_sad_machine()
    TestArtistsAndFeatures.task_porter_robinson_years_of_war()
    TestArtistsAndFeatures.task_porter_robinson_flicker()
    TestArtistsAndFeatures.task_porter_robinson_fresh_static_snow()
    TestArtistsAndFeatures.task_porter_robinson_polygon_dust()
    TestArtistsAndFeatures.task_porter_robinson_hear_the_bells()
    TestArtistsAndFeatures.task_porter_robinson_natural_light()
    TestArtistsAndFeatures.task_porter_robinson_lionhearted()
    TestArtistsAndFeatures.task_porter_robinson_sea_of_voices()
    TestArtistsAndFeatures.task_porter_robinson_fellow_feeling()
    TestArtistsAndFeatures.task_porter_robinson_goodbye_to_a_world()
    TestArtistsAndFeatures.task_one_artist_one_feature()
    TestArtistsAndFeatures.task_no_features()
    TestArtistsAndFeatures.task_zedd_clarity_with_features()
    TestArtistsAndFeatures.task_isoknock_pain_multiple_artists()
    TestArtistsAndFeatures.task_ninajirachi_battery_death_single_artist()
    TestArtistsAndFeatures.task_skrillex_rumble_multiple_artists()
    TestArtistsAndFeatures.task_single_artist_with_feature()
    TestArtistsAndFeatures.task_multiple_artists_no_features()
    TestArtistsAndFeatures.task_single_artist_no_features()
    TestArtistsAndFeatures.task_multiple_artists_with_features()
    TestBandcampSearch.task_carbon_based_lifeforms_derelicts()
    TestBandcampSearch.task_jousboxx_springtime()
    TestBandcampSearch.task_au5_cataclysm()
    TestBandcampSearch.task_second_flight_instead_of_one()
    TestBeatportSearch.task_knock2_feel_u_luv_me()
    TestBeatportSearch.task_zedd_martin_garrix_follow()
    TestBeatportSearch.task_rl_grime_bea_miller_slow_dive()
    TestBeatportSearch.task_zedd_clarity()
    TestDb.task_connect()
    TestGeniusBasic.task_remove_newlines_basic()
    TestGeniusBasic.task_remove_newlines_advanced()
    TestGeniusBasic.task_text()
    TestGeniusBasic.task_start_newline()
    TestGeniusBasic.task_start_break()
    TestGeniusBasic.task_mid_break()
    TestGeniusBasic.task_end_newline()
    TestGeniusBasic.task_end_break()
    TestGeniusBasic.task_many_mid_breaks()
    TestGeniusBasic.task_parens()
    TestGeniusBasic.task_italics()
    TestGeniusBasic.task_italic_parens()
    TestGeniusBasic.task_italic_parens_inverted()
    TestGeniusBasic.task_square_brackets()
    TestGeniusBasic.task_square_brackets_italics()
    TestGeniusBasic.task_square_brackets_italics_newlines()
    TestGeniusBasic.task_annotation()
    TestGeniusBasic.task_annotation_same_line()
    TestGeniusBasic.task_annotation_same_line_followed_by_punctuation()
    TestGeniusBasic.task_annotation_break_outside_break()
    TestGeniusBasic.task_annotation_mid_breaks()
    TestGeniusBasic.task_annotation_mid_mixed()
    TestGeniusBasic.task_span()
    TestGeniusBasic.task_multiple_lines()
    TestGeniusBasic.task_mid_breaks_with_square_brackets()
    TestGeniusBasic.task_mid_breaks_with_annotated_square_brackets()
    TestGeniusBasic.task_dumb_stupid_useless_div_between_lyric_divs()
    TestGeniusBasic.task_annotated_sqaure_brackets()
    TestGeniusBasic.task_bold()
    TestGeniusBasic.task_italic_normal_parens_nested()
    TestGeniusBasic.task_inline_parenthesized_italics()
    TestGeniusBasic.task_inline_parenthesized_italics_inverted()
    TestGeniusBasic.task_replace_on_unicode_apostrophe()
    TestGeniusBasic.task_replace_with_unicode_space()
    TestGeniusBasic.task_bold_with_space()
    TestGeniusRealSongs.task_chase_atlantic_beauty_in_death()
    TestGeniusRealSongs.task_chase_atlantic_cassie()
    TestGeniusRealSongs.task_chase_atlantic_call_me_back()
    TestGeniusRealSongs.task_lil_nas_x_old_town_road()
    TestGeniusRealSongs.task_cloudfield_artificial()
    TestGeniusRealSongs.task_chase_atlantic_escort()
    TestGeniusRealSongs.task_chase_atlantic_i_never_existed()
    TestGeniusRealSongs.task_chase_atlantic_obsessive()
    TestGeniusRealSongs.task_essenger_lexi_norton_downfall()
    TestGetImg.task_soundcloud_nolimit()
    TestGetImg.task_bandcamp_beyond()
    TestGetImg.task_x_nolimit()
    TestGetImg.task_instagram_nolimit_post()
    TestGetImg.task_facebook_nolimit_post()
    TestGetImg.task_genius_nolimit_album()
    TestGetImg.task_genius_dance_or_dead_song()
    TestGetImg.task_threads_nolimit_post()
    TestGoogleImages.task_google_images()
    TestGoogleImages.task_litterbox_upload()
    TestGoogleImages.task_serpapi_reverse_image()
    TestGoogleImages.task_serpapi_two_results()
    TestGoogleImages.task_serpapi_ten_results()
    TestGoogleImages.task_scale_down_image_1()
    TestGoogleImages.task_scale_down_image_2()
    TestImgDiff.task_1_vs_1_original()
    TestImgDiff.task_1_vs_1_cropped()
    TestImgDiff.task_1_vs_1_lossy_4x()
    TestImgDiff.task_1_vs_1_low_res()
    TestImgDiff.task_1_vs_1_shrunk_blown_up()
    TestImgDiff.task_1_vs_1_very_lossy()
    TestImgDiff.task_x_image_vs_reference_image()
    TestImgDiff.task_1_vs_2_original()
    TestImgDiff.task_1_vs_2_cropped()
    TestImgDiff.task_1_vs_2_lossy_4x()
    TestImgDiff.task_1_vs_2_low_res()
    TestImgDiff.task_1_vs_2_shrunk_blown_up()
    TestImgDiff.task_1_vs_2_very_lossy()
    TestIntegration.task_knock2_nolimit_purchased()
    TestIntegration.task_porter_robinson_worlds_purchased()
    TestMetadata.task_get_year_mp3()
    TestMetadata.task_set_year_mp3()
    TestMetadata.task_clear_year_mp3()
    TestMetadata.task_read_artist_mp3()
    TestMetadata.task_read_album_artist_mp3()
    TestMetadata.task_get_album_title_mp3()
    TestMetadata.task_set_album_title_mp3()
    TestMetadata.task_clear_album_title_mp3()
    TestMetadata.task_get_artist_mp3()
    TestMetadata.task_set_artist_mp3()
    TestMetadata.task_clear_artist_mp3()
    TestMetadata.task_get_album_artist_mp3()
    TestMetadata.task_set_album_artist_mp3()
    TestMetadata.task_clear_album_artist_mp3()
    TestMetadata.task_get_song_title_mp3()
    TestMetadata.task_set_song_title_mp3()
    TestMetadata.task_clear_song_title_mp3()
    TestMetadata.task_get_lyrics_mp3()
    TestMetadata.task_set_lyrics_mp3()
    TestMetadata.task_clear_lyrics_mp3()
    TestMetadata.task_get_cover_art_mp3()
    TestMetadata.task_set_cover_art_mp3()
    TestMetadata.task_clear_cover_art_mp3()
    TestMetadata.task_get_year_flac()
    TestMetadata.task_set_year_flac()
    TestMetadata.task_clear_year_flac()
    TestMetadata.task_read_artist_flac()
    TestMetadata.task_read_album_artist_flac()
    TestMetadata.task_get_album_title_flac()
    TestMetadata.task_set_album_title_flac()
    TestMetadata.task_clear_album_title_flac()
    TestMetadata.task_get_artist_flac()
    TestMetadata.task_set_artist_flac()
    TestMetadata.task_clear_artist_flac()
    TestMetadata.task_get_album_artist_flac()
    TestMetadata.task_set_album_artist_flac()
    TestMetadata.task_clear_album_artist_flac()
    TestMetadata.task_get_song_title_flac()
    TestMetadata.task_set_song_title_flac()
    TestMetadata.task_clear_song_title_flac()
    TestMetadata.task_get_lyrics_flac()
    TestMetadata.task_set_lyrics_flac()
    TestMetadata.task_clear_lyrics_flac()
    TestMetadata.task_get_cover_art_flac()
    TestMetadata.task_set_cover_art_flac()
    TestMetadata.task_clear_cover_art_flac()
    TestMisc.task_predownloaded_html()
    TestMisc.task_generate_lyrics_filename()
    TestMisc.task_lyrics_properly_terminated()
    TestParseClean.task_clean_title_parens()
    TestParseClean.task_clean_title_ft()
    TestParseClean.task_clean_title_feat()
    TestParseClean.task_clean_title_capital_feat()
    TestParseClean.task_clean_title_brackets()
    TestParseClean.task_clean_title_mixed()
    TestParseClean.task_clean_title_no_features()
    TestParseClean.task_clean_title_whitespace()
    TestParseClean.task_explicit_removal()
    TestParseClean.task_clean_title_push()
    TestParseClean.task_clean_artist_semicolons_and_commas()
    TestParseClean.task_clean_artist_semicolons_only()
    TestParseClean.task_clean_artist_commas_only()
    TestParseClean.task_clean_artist_no_separators()
    TestParseClean.task_clean_artist_whitespace()
    TestParseClean.task_parens()
    TestParseClean.task_brackets()
    TestParseClean.task_explicit_end()
    TestParseClean.task_no_explicit()
    TestParseClean.task_legit_explicit()
    TestParseClean.task_parens()
    TestParseClean.task_parens_capital_feat()
    TestParseClean.task_parens_ft()
    TestParseClean.task_parens_featuring()
    TestParseClean.task_no_parens_feat()
    TestParseClean.task_no_parens_capital_feat()
    TestParseClean.task_no_parens_ft()
    TestParseClean.task_no_parens_featuring()
    TestParseClean.task_no_features_found()
    TestParseClean.task_ampersand()
    TestParseClean.task_comma()
    TestParseClean.task_semicolon()
    TestParseClean.task_and()
    TestParseClean.task_and_with_exception_ampersand()
    TestParseClean.task_and_with_exception_and()
    TestParseClean.task_ampersand_with_exception_ampersand()
    TestParseClean.task_ampersand_with_exception_and()
    TestParseClean.task_exception_solo()
    TestSeleniumChrome.task_selenium_and_chrome()
    TestSevendigitalSearch.task_knock2_jade()
    TestSevendigitalSearch.task_martin_garrix_album_search()
    TestSevendigitalSearch.task_charli_xcx_360_track()
    TestSevendigitalSearch.task_charli_xcx_brat_album()
    TestSevendigitalSearch.task_one_direction_little_white_lies()
    TestSevendigitalSearch.task_martin_garrix_dont_look_down()
    TestSevendigitalSearch.task_rl_grime_ucla()
    TestSoundscrapeFileIo.task_input_dir_output_dir_exists()
    TestSoundscrapeFileIo.task_input_dir_output_dir_not_exists()
    TestSoundscrapeFileIo.task_invalid_input_path()
    TestSoundscrapeFileIo.task_input_file_instead_of_directory_error()
    TestSoundscrapeFileIo.task_noaudio_basic()
    TestSoundscrapeFileIo.task_noaudio_preserves_all_tags()
    TestSoundscrapeFileIo.task_noaudio_multiple_files()
    TestSpotify.task_hold_my_hand_album()
    TestSpotify.task_hold_my_hand_single()
    TestSpotify.task_single_and_album()
    TestSpotify.task_incorrect_album_title()
    TestSpotify.task_lose_my_mind()
    TestSpotify.task_push()
    TestSpotify.task_cli_search_title_only()
    TestSpotify.task_cli_search_artist_only()
    TestSpotify.task_cli_search_album_only()
    TestSpotify.task_cli_search_title_and_artist()
    TestSpotify.task_cli_search_title_and_album()
    TestSpotify.task_cli_search_artist_and_album()
    TestSpotify.task_cli_search_all_params()
    TestSpotify.task_compact_output()
    TestViewLink.task_full_url()
    TestViewLink.task_no_protocol()
    TestViewLink.task_with_www()
    TestViewLink.task_www_no_protocol()
    TestViewLink.task_bandcamp_subdomain()
    TestViewLink.task_http_protocol()
    TestViewLink.task_unknown_site()
    TestYtMusicMetadata.task_mameyudoufu_i_dont_know_what_im_doing()
    TestYtMusicMetadata.task_atmozfears_release()
    TestYtMusicMetadata.task_ghosts_n_stuff()
    TestYtMusicMetadata.task_clarity()
    TestYtMusicMetadata.task_dont_you_worry_child()
    TestYtMusicMetadata.task_get_lucky()
    TestYtMusicMetadata.task_i_remember()
    TestYtMusicMetadata.task_heroes()
