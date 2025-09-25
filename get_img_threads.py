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

    # Look for the main post image (1440x1440)
    main_image_pattern = r'<img[^>]*height="1440"[^>]*width="1440"[^>]*srcset="([^"]*)"'
    main_match = re.search(main_image_pattern, html_content).group(1)

    # Get filename, e.g. 474587474_3939486272971106_3474843056868060500_n.jpg
    filename = re.search(r"(\d+_\d+_\d+_n\.jpg)", main_match).group(1)

    # Find image URL containing filename and special magic string indicating it's hi-res
    image_url = re.findall(
        r"(https://scontent[^,\s]*"
        + re.escape(filename)
        + r"\?stp=dst-jpg_e35_tt6[^,\s]*)",
        main_match,
    )[0]

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
