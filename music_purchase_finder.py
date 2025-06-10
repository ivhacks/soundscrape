"""
Music Purchase Research System
A simple, robust function to find the best place to buy music online.

This system searches music purchase sites and returns the best option,
prioritizing sites that support artists and offer high-quality downloads.
"""

from music_purchase_research import GeminiMusicResearcher


def find_best_music_purchase_site(search_term: str) -> str:
    """
    Find the best place to buy a song online.

    Args:
        search_term (str): The song to search for, e.g. "Knock2 - feel u luv me"

    Returns:
        str: URL to the best site to purchase the song

    Priority order:
        1. Bandcamp (best for artists)
        2. Beatport (professional DJ store)
        3. 7digital
        4. Amazon

    Only returns sites that sell downloadable files (MP3, M4A, WAV, FLAC).
    All links are validated before returning.
    """

    try:
        # Load API key
        with open(".env", "r") as f:
            api_key = f.read().strip()
    except:
        return "Error: Could not read API key from .env file"

    # Create researcher and find best option
    researcher = GeminiMusicResearcher(api_key)
    result = researcher.find_best_purchase_option(search_term)

    if "error" in result:
        return f"Error: {result['error']}"

    return result["purchase_url"]


if __name__ == "__main__":
    # Example usage
    search_term = "Knock2 - feel u luv me"

    print(f"Finding best place to buy: {search_term}")
    best_url = find_best_music_purchase_site(search_term)
    print(f"Result: {best_url}")
