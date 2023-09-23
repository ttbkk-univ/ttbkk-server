import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def setup_chrome():
    print('init chrome driver')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("window-size=1280x900")
    chrome_options.add_argument('--disable-application-cache')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # os.system('pwd')
    # driver = webdriver.Chrome('./chromedriver.exe', chrome_options=chrome_options)
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options,
    )
    time.sleep(1)
    print('initiated chrome driver')
    return driver
