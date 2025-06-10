import requests
import json
import re
from urllib.parse import quote_plus, urljoin
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from google import genai
import time

class MusicSiteSearcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
    def search_bandcamp(self, query: str) -> List[Dict]:
        """Search Bandcamp for tracks/albums"""
        try:
            search_url = f"https://bandcamp.com/search?q={quote_plus(query)}"
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code != 200:
                return []
                
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Find search results using the correct selector
            for item in soup.find_all('li', class_='searchresult'):
                try:
                    # Find title in .heading div
                    heading_div = item.find('div', class_='heading')
                    if not heading_div:
                        continue
                        
                    title_link = heading_div.find('a')
                    if not title_link:
                        continue
                        
                    title = title_link.get_text(strip=True)
                    url = title_link.get('href', '')
                    
                    # Find artist in .subhead div
                    subhead_div = item.find('div', class_='subhead')
                    if subhead_div:
                        artist_text = subhead_div.get_text(strip=True)
                        # Remove "by " prefix if present
                        artist = artist_text.replace('by ', '') if artist_text.startswith('by ') else artist_text
                    else:
                        artist = "Unknown"
                    
                    # Clean up URL - remove tracking parameters but keep the clean URL
                    if url:
                        # Extract the base URL before search parameters
                        base_url = url.split('?')[0]
                        if base_url and not base_url.startswith('http'):
                            base_url = urljoin('https://bandcamp.com', base_url)
                        url = base_url
                            
                    if title and url:
                        results.append({
                            'title': title,
                            'artist': artist,
                            'url': url,
                            'site': 'bandcamp'
                        })
                        
                except Exception as e:
                    continue
                    
            return results[:10]  # Limit to 10 results
            
        except Exception as e:
            print(f"Error searching Bandcamp: {e}")
            return []
    
    def search_7digital(self, query: str) -> List[Dict]:
        """Search 7digital for tracks/albums"""
        try:
            # 7digital appears to have bot protection, let's try their API or alternative approach
            search_url = f"https://us.7digital.com/search?q={quote_plus(query)}"
            
            # Try with additional headers to bypass protection
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            response = self.session.get(search_url, headers=headers, timeout=10)
            
            # For now, return empty if we can't access it properly
            if "Client Challenge" in response.text or response.status_code != 200:
                return []
                
            # If we get proper HTML, parse it
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # This would need to be updated based on actual HTML structure
            # when we can properly access the site
            return []
            
        except Exception as e:
            print(f"Error searching 7digital: {e}")
            return []
    
    def search_beatport(self, query: str) -> List[Dict]:
        """Search Beatport for tracks/albums"""
        try:
            search_url = f"https://www.beatport.com/search?q={quote_plus(query)}"
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code != 200:
                return []
                
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Look for the __NEXT_DATA__ script tag that contains JSON data
            script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
            if script_tag and script_tag.string:
                try:
                    # Parse the JSON data
                    json_data = json.loads(script_tag.string)
                    
                    # Navigate to the search results
                    props = json_data.get('props', {})
                    page_props = props.get('pageProps', {})
                    dehydrated_state = page_props.get('dehydratedState', {})
                    queries = dehydrated_state.get('queries', [])
                    
                    # Find the search query data
                    for query_data in queries:
                        state = query_data.get('state', {})
                        data = state.get('data', {})
                        tracks = data.get('tracks', {})
                        track_data = tracks.get('data', [])
                        
                        if track_data:
                            for track in track_data[:10]:  # Limit to 10 results
                                try:
                                    track_name = track.get('track_name', '')
                                    track_id = track.get('track_id', '')
                                    
                                    # Get artist name
                                    artists = track.get('artists', [])
                                    artist_name = artists[0].get('artist_name', 'Unknown') if artists else 'Unknown'
                                    
                                    # Construct Beatport URL
                                    url = f"https://www.beatport.com/track/{track_name.lower().replace(' ', '-')}/{track_id}"
                                    
                                    # Get price info
                                    price_info = track.get('price', {})
                                    price_display = price_info.get('display', '')
                                    
                                    results.append({
                                        'title': track_name,
                                        'artist': artist_name,
                                        'url': url,
                                        'site': 'beatport',
                                        'price': price_display,
                                        'track_id': track_id
                                    })
                                except Exception as e:
                                    continue
                            break
                            
                except Exception as e:
                    print(f"Error parsing Beatport JSON: {e}")
                    
            return results
            
        except Exception as e:
            print(f"Error searching Beatport: {e}")
            return []
    
    def search_amazon_music(self, query: str) -> List[Dict]:
        """Search Amazon for digital music"""
        try:
            # Amazon blocks automated access, we'd need to use their API
            # For now, return empty array
            return []
            
        except Exception as e:
            print(f"Error searching Amazon: {e}")
            return []
    
    def validate_url(self, url: str) -> bool:
        """Validate that a URL is accessible"""
        try:
            response = self.session.head(url, timeout=5, allow_redirects=True)
            return response.status_code == 200
        except:
            return False

class GeminiMusicResearcher:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.searcher = MusicSiteSearcher()
        
    def create_search_tool(self):
        """Create a search tool for Gemini to use"""
        return {
            "function_declarations": [
                {
                    "name": "search_music_sites",
                    "description": "Search music purchase sites for a specific song or album",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string", 
                                "description": "The search query (e.g., artist name and song title)"
                            },
                            "sites": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of sites to search (bandcamp, 7digital, beatport, amazon)"
                            }
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "validate_purchase_links",
                    "description": "Validate that purchase links are working and return structured data",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "links": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "url": {"type": "string"},
                                        "site": {"type": "string"},
                                        "title": {"type": "string"},
                                        "artist": {"type": "string"}
                                    }
                                },
                                "description": "List of links to validate"
                            }
                        },
                        "required": ["links"]
                    }
                }
            ]
        }
    
    def search_music_sites(self, query: str, sites: List[str] = None) -> List[Dict]:
        """Execute search across specified music sites"""
        if sites is None:
            sites = ['bandcamp', '7digital', 'beatport', 'amazon']
        
        all_results = []
        
        for site in sites:
            if site == 'bandcamp':
                results = self.searcher.search_bandcamp(query)
            elif site == '7digital':
                results = self.searcher.search_7digital(query)
            elif site == 'beatport':
                results = self.searcher.search_beatport(query)
            elif site == 'amazon':
                results = self.searcher.search_amazon_music(query)
            else:
                continue
                
            all_results.extend(results)
            
        return all_results
    
    def validate_purchase_links(self, links: List[Dict]) -> List[Dict]:
        """Validate links and return only working ones"""
        validated_links = []
        
        for link in links:
            if self.searcher.validate_url(link['url']):
                validated_links.append({
                    **link,
                    'validated': True
                })
            else:
                validated_links.append({
                    **link,
                    'validated': False
                })
        
        return validated_links
    
    def find_best_purchase_option(self, search_term: str) -> Dict:
        """Main function to find the best place to buy a song"""
        
        # First, do direct searches without AI to get the data
        print(f"Searching for: {search_term}")
        
        all_results = []
        
        # Search Bandcamp first (preferred)
        print("Searching Bandcamp...")
        bandcamp_results = self.searcher.search_bandcamp(search_term)
        all_results.extend(bandcamp_results)
        
        # Search Beatport
        print("Searching Beatport...")
        beatport_results = self.searcher.search_beatport(search_term)
        all_results.extend(beatport_results)
        
        # For now skip 7digital and Amazon since they have issues
        
        if not all_results:
            return {"error": "No results found on any music sites"}
        
        print(f"Found {len(all_results)} total results")
        
        # Validate URLs and apply prioritization logic
        validated_results = []
        for result in all_results:
            print(f"Validating: {result['title']} on {result['site']}")
            if self.searcher.validate_url(result['url']):
                validated_results.append({**result, 'validated': True})
                print(f"✓ Valid: {result['url']}")
            else:
                print(f"✗ Invalid: {result['url']}")
        
        if not validated_results:
            return {"error": "No valid links found"}
        
        # Apply priority logic: Bandcamp > Beatport > Others
        site_priority = {'bandcamp': 1, 'beatport': 2, '7digital': 3, 'amazon': 4}
        
        # Sort by priority, then by how well the title matches the search term
        def sort_key(result):
            priority = site_priority.get(result['site'], 99)
            title_match = 1 if search_term.lower() in result['title'].lower() else 2
            return (priority, title_match)
        
        validated_results.sort(key=sort_key)
        
        best_result = validated_results[0]
        
        # Create reasoning
        reasoning = f"Selected {best_result['site']} because "
        if best_result['site'] == 'bandcamp':
            reasoning += "Bandcamp provides the best revenue share for artists and supports independent music."
        elif best_result['site'] == 'beatport':
            reasoning += "Beatport is a trusted professional DJ music store with high-quality downloads."
        else:
            reasoning += f"it was the best available option among the search results."
        
        return {
            "recommended_site": best_result['site'],
            "purchase_url": best_result['url'],
            "title": best_result['title'],
            "artist": best_result['artist'],
            "price": best_result.get('price', 'Price not available'),
            "reasoning": reasoning,
            "all_results": validated_results,
            "total_found": len(all_results)
        }

def main():
    """Main function to find best music purchase option"""
    
    # Load API key
    try:
        with open(".env", "r") as f:
            api_key = f.read().strip()
    except:
        print("Error: Could not read API key from .env file")
        return
    
    # Create researcher
    researcher = GeminiMusicResearcher(api_key)
    
    # Test with a search term
    search_term = "Knock2 - feel u luv me"
    result = researcher.find_best_purchase_option(search_term)
    
    print(f"Search results for: {search_term}")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main() 