from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_stealth_driver(headless: bool = True) -> webdriver.Chrome:
    """Create a Chrome driver with comprehensive stealth settings to avoid detection"""
    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless")

    # Basic stability options
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # User agent to appear like a real browser
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    # Additional stealth options to avoid automation detection
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
