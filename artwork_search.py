from typing import List
import os
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import requests
from io import BytesIO
from spoti import get_token, get_cover_artwork_url

MAX_NUM_THUMBNAILS = 5


# Returns tuple of (List[Image.Image], List[Bytes]) where both lists are the same length
# List of bytestrings are the directly downloaded image datas that will be used to create the pillow images
def search_cover_artwork_by_image(image: Image.Image):

    IMAGE_BUTTON_CLASS = "tdPRye"
    UPLOAD_IMAGE_TAB_CLASS = "iOGqzf H4qWMc aXIg1b"
    UPLOAD_IMAGE_TAB_XPATH = "/html/body/div[1]/div[3]/div/div[2]/form/div[1]/div/a"
    BROWSE_BUTTON_ID = "awyMjb"
    ALL_SIZES_LINK_XPATH = "/html/body/div[7]/div/div[10]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/span[1]/a"
    ALL_IMAGE_THUMBNAILS_DIV_CLASS = "islrc"
    ALL_IMAGE_THUMBNAILS_DIV_XPATH = "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]"
    EXPANDED_IMAGE_XPATH = "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img"

    # TODO: Determine this experimentally
    MAX_GOOGLE_IMAGES_LOAD_RESOLUTION = 3200

    # Save given image as a file so we can upload it to google images
    image_path = os.path.join(os.getcwd(), "temp", "temp_image.jpg")
    image.save(image_path)

    # driver = webdriver.Firefox()
    driver = webdriver.Chrome()

    ublock_origin_path = "ublock_origin-1.43.0.xpi"
    driver.install_addon(ublock_origin_path)

    driver.get(f"https://images.google.com")

    # Click the image button with the camera icon
    wait_for_section = WebDriverWait(driver, 180)
    wait_for_section.until(
        expected_conditions.presence_of_element_located(
            (By.CLASS_NAME, IMAGE_BUTTON_CLASS)
        )
    )
    image_button = driver.find_elements(By.CLASS_NAME, IMAGE_BUTTON_CLASS)[0]
    image_button.click()

    # Click the "Upload an image" tab
    wait_for_section = WebDriverWait(driver, 180)
    wait_for_section.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, UPLOAD_IMAGE_TAB_XPATH)
        )
    )
    upload_image_tab = driver.find_elements(By.XPATH, UPLOAD_IMAGE_TAB_XPATH)[0]
    upload_image_tab.click()

    # Click the "Browse" button to upload the image
    wait_for_section = WebDriverWait(driver, 180)
    wait_for_section.until(
        expected_conditions.presence_of_element_located((By.ID, BROWSE_BUTTON_ID))
    )
    browse_button = driver.find_elements(By.ID, BROWSE_BUTTON_ID)[0]
    browse_button.send_keys(image_path)

    # Click the "All sizes" link on the search results page to go to the list of image result thumbnails
    wait_for_section = WebDriverWait(driver, 180)
    wait_for_section.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, ALL_SIZES_LINK_XPATH)
        )
    )
    images_tab = driver.find_elements(By.XPATH, ALL_SIZES_LINK_XPATH)[0]
    images_tab.click()

    # We're done with the image file, delete it
    os.remove(image_path)

    # Get div that contains thumbnails of all the image results
    wait_for_section = WebDriverWait(driver, 180)
    wait_for_section.until(
        expected_conditions.presence_of_element_located(
            (By.CLASS_NAME, ALL_IMAGE_THUMBNAILS_DIV_CLASS)
        )
    )
    thumbnails_div = driver.find_elements(
        By.CLASS_NAME, ALL_IMAGE_THUMBNAILS_DIV_CLASS
    )[0]

    # First element is just a thing that says "Image results", cut it out
    thumbnails = thumbnails_div.find_elements(By.XPATH, "./child::*")[1:]

    # Sort thumbnails from highest to lowest resolution of the full-size image
    def full_resolution(thumbnail):
        width = int(thumbnail.get_attribute("data-ow"))
        height = int(thumbnail.get_attribute("data-oh"))
        return width * height

    thumbnails.sort(key=full_resolution, reverse=True)

    square_thumbnails = []
    for thumbnail in thumbnails:
        width = int(thumbnail.get_attribute("data-ow"))
        height = int(thumbnail.get_attribute("data-oh"))

        # Skip images that aren't roughly square, they probably aren't cover artworks or are cropped weirdly
        if width < (float(height) * 0.95) or height > (float(width) * 1.05):
            continue

        # If an image is too big, the full-sized image link will never be loaded on the results page.
        # Since we're not going to navigate to a site and try to figure out how to isolate the image, just skip these super huge images.
        if width * height > MAX_GOOGLE_IMAGES_LOAD_RESOLUTION**2:
            continue

        square_thumbnails.append(thumbnail)

    full_size_images_pillow = []
    full_size_images_raw = []
    for thumbnail in square_thumbnails:
        try:
            thumbnail.click()

            # Get expanded image element from clicking thumbnail
            wait_for_section = WebDriverWait(driver, 180)
            wait_for_section.until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, EXPANDED_IMAGE_XPATH)
                )
            )
            expanded_image = driver.find_elements(By.XPATH, EXPANDED_IMAGE_XPATH)[0]

            # Wait until full-sized image loads in (src changes from bas64 encoded thumbnail to a link that starts with http)
            # If the image takes more than 5 seconds to load, the link is probably broken so just skip it and move on
            wait_for_full_res_image = WebDriverWait(driver, 5)
            wait_for_full_res_image.until(
                expected_conditions.text_to_be_present_in_element_attribute(
                    (By.XPATH, EXPANDED_IMAGE_XPATH), "src", "http"
                )
            )

            image_url = expanded_image.get_attribute("src")

            response = requests.get(image_url)
            raw = response.content
            img = Image.open(BytesIO(raw))
            full_size_images_pillow.append(img)
            full_size_images_raw.append(raw)
        except:
            continue

        # Break once we have enough images
        if len(full_size_images_pillow) >= MAX_NUM_THUMBNAILS:
            break

    driver.close()

    # If the original image was a jpeg, we don't want to re-encode it when we're going from pillow to a file.
    # Return both the pillow versions and the originals so that once user chooses an image, we can use the raw original image rather than the pillow version.
    return (full_size_images_pillow, full_size_images_raw)


def search_cover_artwork_by_text(artist: str, title: str, album: bool = False) -> bytes:
    token = get_token()

    if album:
        # Search for album artwork
        artwork_url = get_cover_artwork_url(
            token, title, artist, single=False, is_album=False
        )
    else:
        artwork_url = get_cover_artwork_url(
            token, title, artist, single=True, is_album=False
        )

    response = requests.get(artwork_url)
    response.raise_for_status()

    return response.content


def search_cover_artwork_by_text_musicbrainz(
    artist: str, title: str, album: bool = False
) -> List[Image.Image]:
    # MusicBrainz requires a User-Agent header
    headers = {"User-Agent": "soundscrape/1.0 (https://github.com/user/soundscrape)"}

    # Build search query for MusicBrainz
    if album:
        # Search for album releases
        query = f'artist:"{artist}" AND release:"{title}"'
    else:
        # Search for any release containing the track
        query = f'artist:"{artist}" AND recording:"{title}"'

    # Search MusicBrainz for releases
    mb_url = "https://musicbrainz.org/ws/2/release"
    params = {
        "query": query,
        "fmt": "json",
        "limit": 25,  # Get more results to increase chances of finding cover art
    }

    try:
        response = requests.get(mb_url, params=params, headers=headers)
        response.raise_for_status()
        releases = response.json().get("releases", [])
    except:
        return []

    cover_images = []

    # Try to get cover art for each release
    for release in releases:
        if len(cover_images) >= MAX_NUM_THUMBNAILS:
            break

        mbid = release.get("id")
        if not mbid:
            continue

        # Try Cover Art Archive
        caa_url = f"https://coverartarchive.org/release/{mbid}"

        try:
            caa_response = requests.get(caa_url, headers=headers)
            caa_response.raise_for_status()
            artwork_data = caa_response.json()

            # Get the front cover image, or first image if no front cover
            images = artwork_data.get("images", [])
            if not images:
                continue

            # Prefer front cover
            front_cover = None
            for img in images:
                if img.get("front", False):
                    front_cover = img
                    break

            # Use front cover if found, otherwise use first image
            selected_image = front_cover if front_cover else images[0]
            image_url = selected_image.get("image")

            if image_url:
                # Download the image
                img_response = requests.get(image_url, headers=headers)
                img_response.raise_for_status()

                # Convert to PIL Image
                img = Image.open(BytesIO(img_response.content))
                cover_images.append(img)

        except:
            # Cover art not available for this release, continue to next
            continue

    return cover_images
