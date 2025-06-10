# Music Purchase Research System

A simple, robust system to find the best place to buy music online. This system searches multiple music purchase sites and returns validated links to buy songs, prioritizing sites that support artists and offer high-quality downloads.

## Features

- **Dead Simple**: One function, one result - just pass a search term
- **Multiple Sites**: Searches Bandcamp and Beatport (more sites coming)
- **Smart Prioritization**: Prefers Bandcamp > Beatport > 7digital > Amazon
- **Validated Links**: All URLs are checked before returning
- **High-Quality Downloads**: Only returns sites with MP3, M4A, WAV, FLAC files
- **No Streaming Services**: Focuses on actual music purchases only

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your Gemini API key:
```
your_gemini_api_key_here
```

3. Use the function:
```python
from music_purchase_finder import find_best_music_purchase_site

# Get the best purchase URL
url = find_best_music_purchase_site("Knock2 - feel u luv me")
print(url)  # https://www.beatport.com/track/feel-u-luv-me/19431109
```

## API Reference

### `find_best_music_purchase_site(search_term: str) -> str`

Returns the URL to the best site to purchase the song.

**Example:**
```python
url = find_best_music_purchase_site("Artist - Song Name")
print(url)  # https://www.beatport.com/track/...
```

## Site Priority

1. **Bandcamp** - Best revenue share for artists, supports independent music
2. **Beatport** - Professional DJ music store, high-quality downloads
3. **7digital** - Digital music retailer
4. **Amazon** - Large marketplace (MP3 downloads only)

## Supported Sites

- ✅ **Bandcamp** - Independent artist platform
- ✅ **Beatport** - Professional DJ music store  
- 🚧 **7digital** - Coming soon
- 🚧 **Amazon** - Coming soon

## Architecture

The system follows the "grizzled senior developer" principle:
- **Simple**: One function does one thing well
- **Robust**: No complex fallbacks, just works reliably
- **Readable**: Clear code that's easy to understand and maintain
- **Minimalistic**: No unnecessary complexity or dependencies

## Files

- `music_purchase_finder.py` - Main user-facing function
- `music_purchase_research.py` - Core search and research logic
- `requirements.txt` - Python dependencies
- `test_bandcamp_search.py` - Unit tests for Bandcamp search
- `test_beatport_search.py` - Unit tests for Beatport search
- `test.sh` - Test runner script
- `format.sh` - Code formatter script

## Testing

Run the full test suite:
```bash
./test.sh
```

Test the main function:
```bash
python music_purchase_finder.py
```

Run individual test files:
```bash
python test_bandcamp_search.py
python test_beatport_search.py
```

## Code Formatting

Format all Python files with Black:
```bash
./format.sh
```

## Example Output

```bash
$ python music_purchase_finder.py

Finding best place to buy: Knock2 - feel u luv me
Result: https://www.beatport.com/track/feel-u-luv-me/19431109
``` 