from dataclasses import dataclass
from io import BytesIO
import time
from typing import List

from PIL import Image
import requests
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

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


def download_images(results: List[ImageResult]) -> List[bytes]:
    images = []

    for result in results:
        try:
            if "bandcamp.com" in result.link:
                image_data = get_image_bandcamp(result.link)
                images.append(image_data)
            elif "facebook.com" in result.link:
                image_data = get_image_facebook(result.link)
                images.append(image_data)
            elif "genius.com" in result.link:
                image_data = get_image_genius(result.link)
                images.append(image_data)
            elif "instagram.com" in result.link:
                image_data = get_image_instagram(result.link)
                images.append(image_data)
            elif "soundcloud.com" in result.link:
                image_data = get_image_soundcloud(result.link)
                images.append(image_data)
            elif "threads.net" in result.link or "threads.com" in result.link:
                image_data = get_image_threads(result.link)
                images.append(image_data)
            elif "x.com" in result.link or "twitter.com" in result.link:
                image_data = get_image_x(result.link)
                images.append(image_data)
        except (requests.exceptions.RequestException, WebDriverException, ValueError):
            continue

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
    results = search_google_images("/Users/iv/nolimit/knock2_nolimit.jpg", min_size=500)
    print(f"Found {len(results)} image results:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.x_dimension}x{result.y_dimension} - {result.link}")

    images = download_images(results)
    print(f"Downloaded {len(images)} images")

    # Load original image for comparison
    with open("/Users/iv/nolimit/knock2_nolimit.jpg", "rb") as f:
        original_image = f.read()

    # Downselect to best 5 images
    selected_images = downselect_images(images, original_image)

    selector = CoverArtSelector(selected_images)
    selected_index = selector.show_selection_window()
