import requests
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from art_selector import CoverArtSelector
from stealth_driver import create_stealth_driver


REQUEST_TIMEOUT = 20


def _instagram_image_url(driver) -> str | None:
    # Prefer first large square scontent img in DOM (post art), not related-feed thumbs.
    large_square: list[str] = []
    large_any: list[tuple[int, str]] = []
    try:
        imgs = driver.find_elements(By.CSS_SELECTOR, 'img[src*="scontent"]')
    except StaleElementReferenceException:
        return None

    for img in imgs:
        try:
            width = int(img.get_property("naturalWidth") or 0)
            height = int(img.get_property("naturalHeight") or 0)
            src = img.get_attribute("src")
        except StaleElementReferenceException:
            continue
        if width <= 200 or not src:
            continue
        src = str(src)
        large_any.append((width, src))
        # full-res post frames are typically ~1080–1440; skip smaller related thumbs
        if height > 0 and width >= 1000 and 0.9 <= width / height <= 1.1:
            large_square.append(src)

    if large_square:
        return large_square[0]

    if large_any:
        large_any.sort(key=lambda item: item[0], reverse=True)
        return large_any[0][1]

    for meta in driver.find_elements(By.CSS_SELECTOR, 'meta[property="og:image"]'):
        content = meta.get_attribute("content")
        if content:
            return str(content)
    return None


def _has_large_square(driver) -> bool:
    try:
        for img in driver.find_elements(By.CSS_SELECTOR, 'img[src*="scontent"]'):
            try:
                width = int(img.get_property("naturalWidth") or 0)
                height = int(img.get_property("naturalHeight") or 0)
            except StaleElementReferenceException:
                continue
            if width >= 800 and height > 0 and 0.9 <= width / height <= 1.1:
                return True
    except StaleElementReferenceException:
        return False
    return False


def get_image_instagram(link: str, driver=None) -> bytes:
    if driver is None:
        driver = create_stealth_driver(headless=True)

    driver.get(link)

    wait = WebDriverWait(driver, 25)
    # wait for full post art (not just profile thumbs / unloaded imgs)
    wait.until(lambda d: _has_large_square(d) or _instagram_image_url(d) is not None)

    image_url = _instagram_image_url(driver)
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
