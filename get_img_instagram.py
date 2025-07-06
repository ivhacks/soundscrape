import re

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from art_selector import CoverArtSelector
from stealth_driver import create_stealth_driver


def get_image_instagram(link: str, driver=None) -> bytes:
    if driver is None:
        driver = create_stealth_driver(headless=True)

    driver.get(link)

    # Wait for the image element to appear
    wait = WebDriverWait(driver, 30)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[src*="scontent"]'))
    )

    html_content = driver.page_source

    # Look for Instagram CDN images
    pattern = r'src="(https://scontent[^"]*\.jpg[^"]*)"'
    match = re.search(pattern, html_content)

    if not match:
        raise ValueError("Could not find Instagram image in page")

    image_url = match.group(1)
    image_url = image_url.replace("&amp;", "&")

    image_response = requests.get(image_url)
    image_response.raise_for_status()

    return image_response.content


if __name__ == "__main__":
    result = get_image_instagram("https://www.instagram.com/p/DDiBXLkTXds/")
    selector = CoverArtSelector([result])
    selected_index = selector.show_selection_window()
