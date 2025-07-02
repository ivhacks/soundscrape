from dataclasses import dataclass
import time
from typing import List

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

from stealth_driver import create_stealth_driver


@dataclass
class ImageResult:
    link: str
    x_dimension: int
    y_dimension: int


def search_google_images(
    image_path: str, driver=None, min_size: int = 800
) -> List[ImageResult]:
    if driver is None:
        driver = create_stealth_driver()

    driver.get("https://images.google.com/")

    # Wait for page to load and bot protection to complete with longer timeout
    try:
        WebDriverWait(driver, 30).until(
            lambda d: "Client Challenge" not in d.page_source
        )
    except WebDriverException:
        # If timeout, try clicking somewhere on the page to trigger challenge completion
        try:
            driver.execute_script("document.body.click()")
            time.sleep(5)
            # Continue anyway - sometimes the page works even after timeout
        except WebDriverException:
            pass

    # Find and click the search by image button using aria-label (most future-proof)
    camera_button = WebDriverWait(driver, 10).until(
        lambda d: d.find_element("css selector", '[aria-label="Search by image"]')
    )
    camera_button.click()

    # Find file input and upload image directly
    file_input = WebDriverWait(driver, 10).until(
        lambda d: d.find_element("css selector", 'input[type="file"]')
    )
    file_input.send_keys(image_path)

    # Click "Exact matches"
    exact_matches = WebDriverWait(driver, 10).until(
        lambda d: d.find_element("xpath", "//div[text()='Exact matches']")
    )
    exact_matches.click()

    # Wait for results to load
    WebDriverWait(driver, 10).until(
        lambda d: d.find_elements("css selector", ".B2VR9.CJHX3e")
    )

    # Extract image results
    result_elements = driver.find_elements("css selector", ".B2VR9.CJHX3e")[:30]
    results = []

    for _, element in enumerate(result_elements):
        try:
            # Extract dimensions from text like "500x500"
            dimension_elements = element.find_elements(
                "css selector", ".cyspcb.DH9lqb.VBZLA"
            )

            for dim_elem in dimension_elements:
                dimension_text = dim_elem.text
                if "x" in dimension_text:
                    x_dim, y_dim = map(
                        lambda x: int(x.replace(",", "")), dimension_text.split("x")
                    )

                    if x_dim < min_size or y_dim < min_size:
                        continue

                    # Extract link from the parent element
                    link_element = element.find_element("xpath", "..")
                    link = link_element.get_attribute("href")

                    results.append(
                        ImageResult(link=link, x_dimension=x_dim, y_dimension=y_dim)
                    )
                    break
        except Exception:
            continue

    return results


if __name__ == "__main__":
    results = search_google_images("/Users/iv/nolimit/knock2_nolimit.jpg", min_size=500)
    print(f"Found {len(results)} image results:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.x_dimension}x{result.y_dimension} - {result.link}")
