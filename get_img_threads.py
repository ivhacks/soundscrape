import re

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from art_selector import CoverArtSelector
from stealth_driver import create_stealth_driver


def get_image_threads(link: str, driver=None) -> bytes:
    if driver is None:
        driver = create_stealth_driver(headless=True)

    driver.get(link)
    # Wait for the thumbnail image to appear
    wait = WebDriverWait(driver, 30)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[src*="scontent"]'))
    )

    html_content = driver.page_source

    # Look for the main post image (1440x1440) with the standard filename pattern
    # Pattern: [numbers]_[numbers]_[numbers]_n.jpg
    main_image_pattern = r'<img[^>]*height="1440"[^>]*width="1440"[^>]*srcset="([^"]*)"'
    main_match = re.search(main_image_pattern, html_content)

    if main_match:
        srcset = main_match.group(1)

        # Extract filename pattern from the srcset to identify this specific image
        filename_match = re.search(r"(\d+_\d+_\d+_n\.jpg)", srcset)
        if filename_match:
            filename = filename_match.group(1)

            # Parse the srcset to get individual URLs for this image
            url_pattern = (
                r"(https://scontent[^,\s]*" + re.escape(filename) + r"[^,\s]*)"
            )
            urls = re.findall(url_pattern, srcset)

            if urls:
                # Find the URL with base quality (dst-jpg_e35_tt6) without size restrictions
                for url in urls:
                    if (
                        "dst-jpg_e35_tt6&" in url
                        and "s1440x1440" not in url
                        and "s1080x1080" not in url
                        and "s720x720" not in url
                        and "s640x640" not in url
                        and "s480x480" not in url
                        and "s320x320" not in url
                        and "s240x240" not in url
                        and "s150x150" not in url
                    ):
                        image_url = url
                        break
                else:
                    # Fallback to the first URL if no base quality found
                    image_url = urls[0]
            else:
                raise ValueError("Could not parse URLs from main image srcset")
        else:
            raise ValueError("Could not extract filename pattern from main image")
    else:
        # Fallback: look for any image with Instagram CDN and standard filename pattern
        fallback_pattern = r'srcset="([^"]*\d+_\d+_\d+_n\.jpg[^"]*)"'
        fallback_matches = re.findall(fallback_pattern, html_content)

        if fallback_matches:
            # Use the first match and parse it
            srcset = fallback_matches[0]
            url_pattern = r"(https://scontent[^,\s]*\.jpg[^,\s]*)"
            urls = re.findall(url_pattern, srcset)

            if urls:
                # Get the longest URL (likely highest resolution)
                image_url = max(urls, key=len)
            else:
                raise ValueError("Could not parse URLs from fallback srcset")
        else:
            raise ValueError("Could not find any Threads post image")

    image_url = image_url.replace("&amp;", "&")

    image_response = requests.get(image_url)
    image_response.raise_for_status()

    return image_response.content


if __name__ == "__main__":
    result = get_image_threads(
        "https://www.threads.com/@coverartmatters/post/DFBRbWGRqjO"
    )
    selector = CoverArtSelector([result])
    selected_index = selector.show_selection_window()
