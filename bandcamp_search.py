from typing import Dict, List
from urllib.parse import quote_plus, urljoin

from bs4 import BeautifulSoup
import requests


SESSION = requests.Session()


def search_bandcamp(query: str) -> List[Dict]:
    """Search Bandcamp for tracks/albums"""
    try:
        search_url = f"https://bandcamp.com/search?q={quote_plus(query)}"
        response = SESSION.get(search_url, timeout=10)

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        # Find search results using the correct selector
        for item in soup.find_all("li", class_="searchresult"):
            try:
                # Find title in .heading div
                heading_div = item.find("div", class_="heading")
                if not heading_div:
                    continue

                title_link = heading_div.find("a")
                if not title_link:
                    continue

                title = title_link.get_text(strip=True)
                url = title_link.get("href", "")

                # Find artist in .subhead div
                subhead_div = item.find("div", class_="subhead")
                if subhead_div:
                    artist_text = subhead_div.get_text(strip=True)
                    # Remove "by " prefix if present
                    artist = (
                        artist_text.replace("by ", "")
                        if artist_text.startswith("by ")
                        else artist_text
                    )
                else:
                    artist = "Unknown"

                # Clean up URL - remove tracking parameters but keep the clean URL
                if url:
                    # Extract the base URL before search parameters
                    base_url = url.split("?")[0]
                    if base_url and not base_url.startswith("http"):
                        base_url = urljoin("https://bandcamp.com", base_url)
                    url = base_url

                if title and url:
                    results.append(
                        {
                            "title": title,
                            "artist": artist,
                            "url": url,
                            "site": "bandcamp",
                        }
                    )

            except Exception:
                continue

        return results[:10]  # Limit to 10 results

    except Exception as e:
        print(f"Error searching Bandcamp: {e}")
        return []
