from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_stealth_driver(headless: bool = True) -> webdriver.Chrome:
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--mute-audio")

    # Genius (and similar) keep network activity open forever under "normal" load;
    # eager returns once the document is interactive so waits can proceed.
    chrome_options.page_load_strategy = "eager"

    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
    )
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    chromedriver_path = ChromeDriverManager().install()

    # https://stackoverflow.com/questions/78806812/third-party-notices-chromedriver-exec-format-error-undetected-chromedriver
    if "THIRD_PARTY_NOTICES.chromedriver" in chromedriver_path:
        chromedriver_path = chromedriver_path.replace(
            "THIRD_PARTY_NOTICES.chromedriver", "chromedriver"
        )

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver
