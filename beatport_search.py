import json
from typing import Dict, List
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
import requests


SESSION = requests.Session()
SESSION.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
)


def search_beatport(query: str) -> List[Dict]:
    """Search Beatport for tracks/albums"""
    search_url = f"https://www.beatport.com/search?q={quote_plus(query)}"

    for _ in range(3):
        try:
            response = SESSION.get(search_url, timeout=20)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            results = []

            script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
            if not script_tag or not script_tag.string:
                continue

            json_data = json.loads(script_tag.string)

            props = json_data.get("props", {})
            page_props = props.get("pageProps", {})
            dehydrated_state = page_props.get("dehydratedState", {})
            queries = dehydrated_state.get("queries", [])

            for query_data in queries:
                state = query_data.get("state", {})
                data = state.get("data", {})
                tracks = data.get("tracks", {})
                track_data = tracks.get("data", [])

                if not track_data:
                    continue

                for track in track_data[:10]:
                    try:
                        track_name = track.get("track_name", "")
                        track_id = track.get("track_id", "")

                        artists = track.get("artists", [])
                        artist_name = (
                            artists[0].get("artist_name", "Unknown")
                            if artists
                            else "Unknown"
                        )

                        url = f"https://www.beatport.com/track/{track_name.lower().replace(' ', '-')}/{track_id}"

                        price_info = track.get("price", {})
                        price_display = price_info.get("display", "")

                        results.append(
                            {
                                "title": track_name,
                                "artist": artist_name,
                                "url": url,
                                "site": "beatport",
                                "price": price_display,
                                "track_id": track_id,
                            }
                        )
                    except Exception:
                        continue
                break

            return results
        except Exception as e:
            print(f"Error searching Beatport: {e}")
            continue

    return []


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python3 ./beatport_search.py artist title")
        sys.exit(1)

    artist = sys.argv[1]
    title = sys.argv[2]

    results = search_beatport(artist + " " + title)
    for result in results:
        print(result["url"])
