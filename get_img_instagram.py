import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from art_selector import CoverArtSelector
from stealth_driver import create_stealth_driver


REQUEST_TIMEOUT = 20


def get_image_instagram(link: str, driver=None) -> bytes:
    if driver is None:
        driver = create_stealth_driver(headless=True)

    driver.get(link)

    wait = WebDriverWait(driver, 20)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[src*="scontent"]'))
    )

    imgs = driver.find_elements(By.CSS_SELECTOR, 'img[src*="scontent"]')
    image_url = None
    for img in imgs:
        natural_width = int(img.get_property("naturalWidth"))
        if natural_width > 200:
            image_url = str(img.get_attribute("src"))
            break

    if not image_url:
        raise ValueError("Could not find Instagram image in page")

    image_url = image_url.replace("&amp;", "&")

    image_response = requests.get(image_url, timeout=REQUEST_TIMEOUT)
    image_response.raise_for_status()

    return image_response.content


if __name__ == "__main__":
    result = get_image_instagram("https://www.instagram.com/p/DDfmurKTFC5/")
    selector = CoverArtSelector([result])
    selected_index = selector.show_selection_window()
