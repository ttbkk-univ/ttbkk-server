import env
from time import sleep
from selenium import webdriver


def setup_chrome():
    print('Initialize ChromeDriver Start...')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("window-size=1280x900")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(env.CHROMEDRIVER_PATH, chrome_options=chrome_options)
    sleep(5)
    print('Initialize ChromeDriver Complete...')
    return driver
