import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium_stealth import stealth

from config import Config


options = webdriver.ChromeOptions()

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
webdriver_path = Service(Config.PATH)
driver = webdriver.Chrome(options=options, service=webdriver_path)

wait = WebDriverWait(driver, 240)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

def main():
    pass


if __name__ == '__main__':
    main()