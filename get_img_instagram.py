import re

import requests
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from art_selector import CoverArtSelector
from stealth_driver import create_stealth_driver


def get_image_instagram(link: str, driver=None) -> bytes:
    if driver is None:
        driver = create_stealth_driver(headless=True)

    driver.get(link)

    # Close the login dialog if it appears
    try:
        wait = WebDriverWait(driver, 10)
        close_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg[aria-label="Close"]'))
        )
        close_button.click()
    except WebDriverException:
        # Login dialog might not appear, continue
        pass

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
