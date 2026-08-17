from io import BytesIO
import os
import sys
from typing import List

from PIL import Image
from requests.exceptions import RequestException
from selenium.common.exceptions import WebDriverException
from serpapi import GoogleSearch
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
from temp_host import upload_temp_image


with open(os.environ.get("SOUNDSCRAPE_SECRETS_PATH", "secrets.yaml"), "r") as f:
    config = yaml.safe_load(f)
    SERPAPI_API_KEY = config["serpapi_api_key"]

HEADLESS = True


def serpapi_reverse_image(url: str, num_results: int = 10) -> List[str]:
    # google reverse image is dead/empty; lens exact matches is the replacement
    params = {
        "api_key": SERPAPI_API_KEY,
        "engine": "google_lens",
        "url": url,
        "type": "exact_matches",
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    urls = []
    for result in results.get("exact_matches", []):
        link = result.get("link")
        if link and link not in urls:
            urls.append(link)
            if len(urls) >= num_results:
                break

    return urls


def search_google_images(image_path: str) -> List[str]:
    uploaded_url = upload_temp_image(image_path)
    urls = serpapi_reverse_image(uploaded_url)
    return urls


def download_images(results: List[str], driver=None) -> List[bytes]:
    images = []
    created_driver = False

    if driver is None:
        driver = create_stealth_driver(headless=HEADLESS)
        created_driver = True
    try:
        for link in results:
            print(f"Attempting to download {link}", end="", flush=True)
            try:
                if "bandcamp.com" in link:
                    image_data = get_image_bandcamp(link)
                    images.append(image_data)
                elif "://facebook.com" in link:
                    image_data = get_image_facebook(link, driver)
                    images.append(image_data)
                elif "://genius.com" in link:
                    image_data = get_image_genius(link)
                    images.append(image_data)
                elif "://instagram.com" in link:
                    image_data = get_image_instagram(link, driver)
                    images.append(image_data)
                elif "://soundcloud.com" in link:
                    image_data = get_image_soundcloud(link)
                    images.append(image_data)
                elif "://threads.net" in link or "threads.com" in link:
                    image_data = get_image_threads(link, driver)
                    images.append(image_data)
                elif "://x.com" in link or "twitter.com" in link:
                    image_data = get_image_x(link)
                    images.append(image_data)
                else:
                    print(" - incompatible site")
                    continue
                print(" - success")
            except (
                RequestException,
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
        results = search_google_images(image_path)
        print(f"Found {len(results)} image results:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result}")

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
