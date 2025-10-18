from dataclasses import dataclass
from io import BytesIO
import os
import sys
import time
from typing import List

from bs4 import BeautifulSoup
from PIL import Image
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from twocaptcha import TwoCaptcha
import yaml

from art_selector import CoverArtSelector
from get_img_bandcamp import get_image_bandcamp
from get_img_facebook import get_image_facebook
from get_img_genius import get_image_genius
from get_img_instagram import get_image_instagram
from get_img_soundcloud import get_image_soundcloud
from get_img_threads import get_image_threads
from get_img_x import get_image_x
from img_diff import image_difference
from stealth_driver import create_stealth_driver


with open("secrets.yaml", "r") as f:
    config = yaml.safe_load(f)
    TWOCAPTCHA_API_KEY = config["twocaptcha_api_key"]

HEADLESS = False
WAIT_TIME = 15


def _detect_captcha(soup: BeautifulSoup) -> bool:
    page_text = soup.get_text()

    captcha_indicators = [
        "Our systems have detected unusual traffic",
        "not a robot",
        "solving the above CAPTCHA",
    ]

    for indicator in captcha_indicators:
        if indicator in page_text:
            return True

    if soup.find(class_="g-recaptcha"):
        return True

    return False


def do_captcha(driver: webdriver.Chrome):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    recaptcha_element = soup.find(class_="g-recaptcha")

    data_sitekey = recaptcha_element.get("data-sitekey")
    page_url = driver.current_url

    solver = TwoCaptcha(TWOCAPTCHA_API_KEY)
    try:
        result = solver.recaptcha(sitekey=data_sitekey, url=page_url)

    except Exception:
        print("failed to solve captcha")

    code = result["code"]

    driver.execute_script(
        "document.getElementById('g-recaptcha-response').innerHTML = arguments[0];",
        str(code),
    )
    driver.execute_script("document.getElementById('captcha-form').submit();")


@dataclass
class ImageResult:
    link: str
    x_dimension: int
    y_dimension: int


def search_google_images(
    image_path: str, driver=None, min_size: int = 800
) -> List[ImageResult]:
    if driver is None:
        driver = create_stealth_driver(headless=HEADLESS)

    for i in range(3):
        try:
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
            camera_button = WebDriverWait(driver, WAIT_TIME).until(
                lambda d: d.find_element(
                    "css selector", '[aria-label="Search by image"]'
                )
            )
            camera_button.click()

            # Find file input and upload image directly
            file_input = WebDriverWait(driver, WAIT_TIME).until(
                lambda d: d.find_element("css selector", 'input[type="file"]')
            )
            file_input.send_keys(image_path)

            # Check for captcha
            time.sleep(2)
            captcha = True
            while captcha:
                soup = BeautifulSoup(driver.page_source, "html.parser")
                captcha = _detect_captcha(soup)
                if captcha:
                    print("captcha detected, solving...")
                    do_captcha(driver)
                    time.sleep(2)

            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Click "Exact matches"
            exact_matches = WebDriverWait(driver, WAIT_TIME).until(
                lambda d: d.find_element("xpath", "//div[text()='Exact matches']")
            )
            exact_matches.click()

            # Wait for results to load
            WebDriverWait(driver, WAIT_TIME).until(
                lambda d: d.find_elements("css selector", ".B2VR9.CJHX3e")
            )
            break
        except TimeoutException:
            print("driver timed out, creating new driver...")
            driver.quit()
            driver = create_stealth_driver(headless=HEADLESS)

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
                    link = str(link_element.get_attribute("href"))

                    results.append(
                        ImageResult(link=link, x_dimension=x_dim, y_dimension=y_dim)
                    )
                    break
        except Exception:
            continue

    return results


def download_images(
    results: List[ImageResult], driver=None, fast_dl: bool = True
) -> List[bytes]:
    images = []
    created_driver = False

    if driver is None:
        driver = create_stealth_driver(headless=HEADLESS)
        created_driver = True
    highest_res = 0
    try:
        for result in results:
            print(f"Attempting to download {result.link}", end="", flush=True)
            if fast_dl:
                if result.x_dimension * result.y_dimension <= highest_res:
                    print(" - too small, skipping")
                    continue
            try:
                # Don't match :// for bandcamp because it has subdomains, e.g.
                # https://handsomeharlow.bandcamp.com/album/jackman
                if "bandcamp.com" in result.link:
                    image_data = get_image_bandcamp(result.link)
                    images.append(image_data)
                elif "://facebook.com" in result.link:
                    image_data = get_image_facebook(result.link, driver)
                    images.append(image_data)
                elif "://genius.com" in result.link:
                    image_data = get_image_genius(result.link)
                    images.append(image_data)
                elif "://instagram.com" in result.link:
                    image_data = get_image_instagram(result.link, driver)
                    images.append(image_data)
                elif "://soundcloud.com" in result.link:
                    image_data = get_image_soundcloud(result.link)
                    images.append(image_data)
                elif "://threads.net" in result.link or "threads.com" in result.link:
                    image_data = get_image_threads(result.link, driver)
                    images.append(image_data)
                elif "://x.com" in result.link or "twitter.com" in result.link:
                    image_data = get_image_x(result.link)
                    images.append(image_data)
                else:
                    print(" - incompatible site")
                    continue
                print(" - success")
                if fast_dl:
                    current_res = result.x_dimension * result.y_dimension
                    if current_res > highest_res:
                        highest_res = current_res
            except (
                requests.exceptions.RequestException,
                WebDriverException,
                ValueError,
            ):
                print(" - failure")
                continue
    finally:
        if created_driver:
            driver.quit()

    return images


def downselect_images(all_images: List[bytes], original: None | bytes) -> List[bytes]:
    # Step 1: Filter by visual similarity if original is provided
    if original is not None:
        similar_images = []
        for image in all_images:
            try:
                diff = image_difference(original, image)
                if diff <= 2:
                    similar_images.append(image)
            except Exception:
                continue
        filtered_images = similar_images
    else:
        filtered_images = all_images

    # Step 2: Filter by aspect ratio (square or almost square)
    square_images = []
    for image in filtered_images:
        try:
            pil_image = Image.open(BytesIO(image))
            width, height = pil_image.size
            aspect_ratio = width / height
            if 0.9 <= aspect_ratio <= 1.1:
                square_images.append(image)
        except Exception:
            continue
    filtered_images = square_images

    # Step 3: If still more than 5, take the 5 highest resolution
    if len(filtered_images) > 5:
        images_with_resolution = []
        for image in filtered_images:
            try:
                pil_image = Image.open(BytesIO(image))
                width, height = pil_image.size
                resolution = width * height
                images_with_resolution.append((image, resolution))
            except Exception:
                continue

        # Sort by resolution (highest first) and take top 5
        images_with_resolution.sort(key=lambda x: x[1], reverse=True)
        filtered_images = [img for img, _ in images_with_resolution[:5]]

    return filtered_images


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: google_images_search.py <image_path>")
        sys.exit(1)

    image_path = os.path.abspath(sys.argv[1])

    driver = create_stealth_driver(headless=HEADLESS)

    try:
        results = search_google_images(image_path, driver, min_size=500)
        print(f"Found {len(results)} image results:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.x_dimension}x{result.y_dimension} - {result.link}")

        images = download_images(results, driver)
        print(f"Downloaded {len(images)} images")

        with open(image_path, "rb") as f:
            original_image = f.read()

        selected_images = downselect_images(images, original_image)
        print(f"Selected {len(selected_images)} images for display")

        if selected_images:
            selector = CoverArtSelector(selected_images)
            selected_index = selector.show_selection_window()
        else:
            print("No suitable images found")
    finally:
        driver.quit()
