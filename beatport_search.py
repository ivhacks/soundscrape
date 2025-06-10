import json
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from typing import List, Dict
from http_session import SESSION


def search_beatport(query: str) -> List[Dict]:
    """Search Beatport for tracks/albums"""
    try:
        search_url = f"https://www.beatport.com/search?q={quote_plus(query)}"
        response = SESSION.get(search_url, timeout=10)

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        # Look for the __NEXT_DATA__ script tag that contains JSON data
        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        if script_tag and script_tag.string:
            try:
                # Parse the JSON data
                json_data = json.loads(script_tag.string)

                # Navigate to the search results
                props = json_data.get("props", {})
                page_props = props.get("pageProps", {})
                dehydrated_state = page_props.get("dehydratedState", {})
                queries = dehydrated_state.get("queries", [])

                # Find the search query data
                for query_data in queries:
                    state = query_data.get("state", {})
                    data = state.get("data", {})
                    tracks = data.get("tracks", {})
                    track_data = tracks.get("data", [])

                    if track_data:
                        for track in track_data[:10]:  # Limit to 10 results
                            try:
                                track_name = track.get("track_name", "")
                                track_id = track.get("track_id", "")

                                # Get artist name
                                artists = track.get("artists", [])
                                artist_name = (
                                    artists[0].get("artist_name", "Unknown")
                                    if artists
                                    else "Unknown"
                                )

                                # Construct Beatport URL
                                url = f"https://www.beatport.com/track/{track_name.lower().replace(' ', '-')}/{track_id}"

                                # Get price info
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
                            except Exception as e:
                                continue
                        break

            except Exception as e:
                print(f"Error parsing Beatport JSON: {e}")

        return results

    except Exception as e:
        print(f"Error searching Beatport: {e}")
        return []
