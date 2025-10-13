import unittest

from view_link import _normalize_url, view_link


class TestNormalizeUrl(unittest.TestCase):
    def test_full_url(self):
        result = _normalize_url("https://music.youtube.com/watch?v=3W_EfEDbTec")
        self.assertEqual(result, "music.youtube.com/watch?v=3W_EfEDbTec")

    def test_no_protocol(self):
        result = _normalize_url("music.youtube.com/watch?v=3W_EfEDbTec")
        self.assertEqual(result, "music.youtube.com/watch?v=3W_EfEDbTec")

    def test_with_www(self):
        result = _normalize_url("https://www.music.youtube.com/watch?v=3W_EfEDbTec")
        self.assertEqual(result, "music.youtube.com/watch?v=3W_EfEDbTec")

    def test_www_no_protocol(self):
        result = _normalize_url("www.beatport.com/track/something")
        self.assertEqual(result, "beatport.com/track/something")

    def test_bandcamp_subdomain(self):
        result = _normalize_url("https://artist.bandcamp.com/album/test")
        self.assertEqual(result, "artist.bandcamp.com/album/test")

    def test_http_protocol(self):
        result = _normalize_url("http://soundcloud.com/track")
        self.assertEqual(result, "soundcloud.com/track")


class TestViewLink(unittest.TestCase):
    def test_unknown_site(self):
        result = view_link("https://example.com/")
        self.assertGreater(len(result), 400)
