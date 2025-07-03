import re

import requests
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from art_selector import CoverArtSelector
from stealth_driver import create_stealth_driver


def get_image_threads(link: str, driver=None) -> bytes:
    if driver is None:
        driver = create_stealth_driver(headless=True)

    driver.get(link)

    # Close any login dialog if it appears
    try:
        wait = WebDriverWait(driver, 10)
        close_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg[aria-label="Close"]'))
        )
        close_button.click()
    except WebDriverException:
        # Login dialog might not appear, continue
        pass

    # Wait for the thumbnail image to appear
    wait = WebDriverWait(driver, 30)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[src*="scontent"]'))
    )

    html_content = driver.page_source

    # Look for the main post image - extract clean URLs from srcset
    # Find srcset attributes containing the target filename pattern
    srcset_pattern = (
        r'srcset="([^"]*474587474_3939486272971106_3474843056868060500_n\.jpg[^"]*)"'
    )
    srcset_matches = re.findall(srcset_pattern, html_content)

    if srcset_matches:
        # Parse the srcset to get individual URLs
        srcset = srcset_matches[0]
        # Extract individual URLs (they're separated by commas)
        url_pattern = r"(https://scontent[^,\s]*\.jpg[^,\s]*)"
        urls = re.findall(url_pattern, srcset)

        if urls:
            # Find the URL with "dst-jpg_e35_tt6" (the base quality without size restrictions)
            for url in urls:
                if (
                    "dst-jpg_e35_tt6&" in url
                    and "s1440x1440" not in url
                    and "s1080x1080" not in url
                ):
                    image_url = url
                    break
            else:
                # Fallback to the first URL
                image_url = urls[0]
        else:
            raise ValueError("Could not parse URLs from srcset")
    else:
        # Fallback: look for regular src attributes
        pattern = r'src="(https://scontent[^"]*474587474_3939486272971106_3474843056868060500_n\.jpg[^"]*)"'
        matches = re.findall(pattern, html_content)

        if matches:
            image_url = matches[0]
        else:
            raise ValueError("Could not find target Threads image in page")

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
