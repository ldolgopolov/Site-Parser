import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

from config import Config
from user_selection import CreateRequest


options = webdriver.FirefoxOptions()


webdriver_path = Service(Config.PATH)
driver = webdriver.Firefox(options=options, service=webdriver_path)

wait = WebDriverWait(driver, 240)


cr = CreateRequest(driver, wait, EC, By)


def main():
    try:
        cr.parsing_setup(True)
    except Exception as ex:
        print(f'ERROR:\n{ex}')

    finally:
        cr.driver_quiting()


if __name__ == '__main__':
    main()