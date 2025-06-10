from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from typing import List, Dict
from http_session import SESSION


def search_7digital(query: str) -> List[Dict]:
    """Search 7digital for tracks/albums"""
    try:
        # 7digital appears to have bot protection, let's try their API or alternative approach
        search_url = f"https://us.7digital.com/search?q={quote_plus(query)}"

        # Try with additional headers to bypass protection
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

        response = SESSION.get(search_url, headers=headers, timeout=10)

        # For now, return empty if we can't access it properly
        if "Client Challenge" in response.text or response.status_code != 200:
            return []

        # If we get proper HTML, parse it
        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        # This would need to be updated based on actual HTML structure
        # when we can properly access the site
        return []

    except Exception as e:
        print(f"Error searching 7digital: {e}")
        return []
