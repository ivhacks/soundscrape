from typing import Dict, List

import requests


SESSION = requests.Session()


def search_bandcamp(query: str) -> List[Dict]:
    """Search Bandcamp for tracks/albums using the public API."""
    try:
        response = SESSION.post(
            "https://bandcamp.com/api/bcsearch_public_api/1/autocomplete_elastic",
            json={"search_text": query, "search_filter": "", "full_page": False},
            timeout=10,
        )

        if response.status_code != 200:
            return []

        data = response.json()
        results = []

        for item in data.get("auto", {}).get("results", []):
            title = item.get("name", "")
            artist = item.get("band_name", "Unknown")
            url = item.get("item_url_path", "")

            if title and url:
                results.append(
                    {
                        "title": title,
                        "artist": artist,
                        "url": url,
                        "site": "bandcamp",
                    }
                )

        return results[:10]

    except Exception as e:
        print(f"Error searching Bandcamp: {e}")
        return []
