import re

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from art_selector import CoverArtSelector
from stealth_driver import create_stealth_driver


def get_image_x(link: str, driver=None) -> bytes:
    if driver is None:
        driver = create_stealth_driver(headless=True)

    driver.get(link)

    # Wait for the image element to appear
    wait = WebDriverWait(driver, 30)
    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'img[src*="pbs.twimg.com/media"]')
        )
    )

    html_content = driver.page_source

    pattern = r'(https://pbs\.twimg\.com/media/[^"\']*\?format=jpg&amp;name=small)'
    match = re.search(pattern, html_content)

    if not match:
        raise ValueError("Could not find X image in page")

    image_url = match.group(1)
    # Replace HTML-encoded ampersand and change to large size
    image_url = image_url.replace("&amp;", "&").replace("name=small", "name=large")

    image_response = requests.get(image_url)
    image_response.raise_for_status()

    return image_response.content


if __name__ == "__main__":
    result = get_image_x("https://x.com/Knock2Music/status/1867292451918295158")
    selector = CoverArtSelector([result])
    selected_index = selector.show_selection_window()
