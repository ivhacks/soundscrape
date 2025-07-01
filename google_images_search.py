from dataclasses import dataclass
import time
from typing import List

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


@dataclass
class ImageResult:
    link: str
    x_dimension: int
    y_dimension: int


def create_driver(headless: bool = False) -> webdriver.Chrome:
    # Set up Chrome options with stealth settings
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    # Additional stealth options
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Set Chrome binary location on macOS
    chrome_options.binary_location = (
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    )

    # Create driver with webdriver-manager - fix path issue
    chromedriver_path = ChromeDriverManager().install()

    # Fix the path if webdriver-manager returns wrong file
    if chromedriver_path.endswith("THIRD_PARTY_NOTICES.chromedriver"):
        chromedriver_path = chromedriver_path.replace(
            "THIRD_PARTY_NOTICES.chromedriver", "chromedriver"
        )

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)

    # Hide webdriver property to avoid detection
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver


def search_google_images(
    image_path: str, driver=None, min_size: int = 800
) -> List[ImageResult]:
    if driver is None:
        driver = create_driver()

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
    print("Looking for 'Exact matches' button...")
    exact_matches = WebDriverWait(driver, 10).until(
        lambda d: d.find_element("xpath", "//div[text()='Exact matches']")
    )
    print("Found and clicking 'Exact matches'")
    exact_matches.click()

    # Wait for results to load
    print("Waiting for results to load...")
    WebDriverWait(driver, 10).until(
        lambda d: d.find_elements("css selector", ".B2VR9.CJHX3e")
    )

    # Debug: dump page source to see what we have
    with open("debug_page.html", "w") as f:
        f.write(driver.page_source)
    print("Page source dumped to debug_page.html")

    # Extract image results
    result_elements = driver.find_elements("css selector", ".B2VR9.CJHX3e")[:30]
    print(f"Found {len(result_elements)} result elements")
    results = []

    for i, element in enumerate(result_elements):
        try:
            print(f"Processing element {i + 1}")
            # Extract dimensions from text like "500x500"
            dimension_elements = element.find_elements(
                "css selector", ".cyspcb.DH9lqb.VBZLA"
            )
            print(f"Found {len(dimension_elements)} dimension elements")

            for dim_elem in dimension_elements:
                dimension_text = dim_elem.text
                print(f"Dimension text: '{dimension_text}'")
                if "x" in dimension_text:
                    x_dim, y_dim = map(
                        lambda x: int(x.replace(",", "")), dimension_text.split("x")
                    )
                    print(f"Parsed dimensions: {x_dim}x{y_dim}")

                    # Skip if either dimension is below min_size
                    if x_dim < min_size or y_dim < min_size:
                        print(f"Skipping {x_dim}x{y_dim} (below {min_size})")
                        continue

                    # Extract link from the parent element
                    link_element = element.find_element("xpath", "..")
                    link = link_element.get_attribute("href")
                    print(f"Found link: {link}")

                    results.append(
                        ImageResult(link=link, x_dimension=x_dim, y_dimension=y_dim)
                    )
                    break
        except Exception as e:
            print(f"Error processing element {i + 1}: {e}")
            continue

    return results


if __name__ == "__main__":
    results = search_google_images("/Users/iv/nolimit/knock2_nolimit.jpg", min_size=500)

    print(f"Found {len(results)} image results:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.x_dimension}x{result.y_dimension} - {result.link}")
