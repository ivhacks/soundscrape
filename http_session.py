import requests

# Shared HTTP session for all search providers
SESSION = requests.Session()
SESSION.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
)


def validate_url(url: str) -> bool:
    """Validate that a URL is accessible"""
    try:
        response = SESSION.head(url, timeout=5, allow_redirects=True)
        return response.status_code == 200
    except:
        return False
