from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


def search_7digital(query: str) -> List[Dict]:
    """Search 7digital for tracks/albums using headless Chrome to bypass bot protection"""
    driver = None
    try:
        # Set up Chrome options with stealth settings
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Re-enable headless
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Additional stealth options
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Set Chrome binary location on macOS
        chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        
        # Create driver with webdriver-manager - fix path issue
        chromedriver_path = ChromeDriverManager().install()
        
        # Fix the path if webdriver-manager returns wrong file
        if chromedriver_path.endswith('THIRD_PARTY_NOTICES.chromedriver'):
            chromedriver_path = chromedriver_path.replace('THIRD_PARTY_NOTICES.chromedriver', 'chromedriver')
        
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)

        # Hide webdriver property to avoid detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Navigate to search page
        search_url = f"https://us.7digital.com/search?q={quote_plus(query)}"
        driver.get(search_url)

        # Wait for page to load and bot protection to complete with longer timeout
        try:
            WebDriverWait(driver, 30).until(
                lambda d: "Client Challenge" not in d.page_source
            )
        except Exception:
            # If timeout, try clicking somewhere on the page to trigger challenge completion
            try:
                driver.execute_script("document.body.click()")
                time.sleep(5)
                # Continue anyway - sometimes the page works even after timeout
            except:
                pass

        # Give it a bit more time to fully load the search results
        time.sleep(3)

        # Parse the page content
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = []

        # Look for track/album links - these typically contain product pages
        # Try multiple selectors to find purchase/product links
        links = soup.find_all("a", href=True)
        
        for link in links:
            href = link.get("href", "")
            # Look for product/album/track pages that would have purchase options
            if any(path in href for path in ["/artist/", "/album/", "/track/"]):
                if href.startswith("/"):
                    full_url = f"https://us.7digital.com{href}"
                else:
                    full_url = href
                
                # Remove query parameters (everything after and including ?)
                if "?" in full_url:
                    full_url = full_url.split("?")[0]
                    
                # Get track/album info from link text or nearby elements
                title = link.get_text(strip=True)
                if title and len(title) > 0:
                    results.append({
                        "title": title,
                        "url": full_url,
                        "source": "7digital"
                    })

        # Remove duplicates
        seen_urls = set()
        unique_results = []
        for result in results:
            if result["url"] not in seen_urls:
                seen_urls.add(result["url"])
                unique_results.append(result)

        return unique_results[:10]  # Limit to top 10 results

    except Exception as e:
        print(f"Error searching 7digital: {e}")
        return []
    finally:
        if driver:
            driver.quit()
