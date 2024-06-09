import requests
import time

from db import Database
from config import Config


db = Database()


class Parser():
    def __init__(self, driver, wait, EC, By, manufacturer, category, lang):
        self.driver = driver
        self.url_page = Config.url_page
        self.wait = wait
        self.EC = EC
        self.By = By
        self.manufacturer = manufacturer
        self.category = category
        self.lang = lang
        self.current_page = 0
        self.item_data = []

    def parsing_process(self):
        try:
            while True:
                self.wait.until(self.EC.presence_of_element_located((self.By.XPATH, f"/html/body/div[11]/div/div[3]/section[3]")))
                page_data = self.driver.find_element(self.By.XPATH, f"/html/body/div[11]/div/div[3]/section[3]")
                page_codes = page_data.find_elements(self.By.CLASS_NAME, f'value')

                for i in range(self.current_page, len(page_codes)):
                    loaded_data = self.load_elements()
                    # Append item's code
                    self.item_data.append(loaded_data[0][i].text)
                    # Append item's title
                    self.item_data.append(loaded_data[1][i].text)
                    # Append item's price
                    self.item_data.append(float(loaded_data[2][i].text.replace("  €", "").replace(" €", "").split('\n')[0].replace(" ", ".")))
                    # Append item's status
                    self.item_data.append(self.translate_item_status(loaded_data[3][i].text))
                    # Append item's manufacturer
                    self.item_data.append(self.manufacturer)
                    # Append item's category
                    self.item_data.append(self.category)
                    print(1)
                    if db.check_availability_item(loaded_data[0][i].text) == False:
                        # Append item's image
                        self.get_item_image(loaded_data[4], index=i)
                        print(2)
                        db.add_new_item(self.item_data, self.lang)
                        print(f"Item number: {i+1}  Item: {self.item_data[1]}")
                        print('Parsed!')
                    else:
                        print(3)
                        db.check_uniqueness_item_values(loaded_data[0][i].text, self.item_data, self.lang)
                        print(f"Item number: {i+1}  Item: {self.item_data[0]}")
                    self.item_data.clear()
                if self.load_more_items() == False:
                    break
                else:
                    self.current_page += 30
        except Exception as e:
            print(f"Parsing ERROR:\n{str(e)}")
            self.item_data.clear()
            self.parsing_process()


    def load_elements(self):
        self.wait.until(self.EC.presence_of_element_located((self.By.XPATH, f"/html/body/div[11]/div/div[3]/section[3]")))
        page_data = self.driver.find_element(self.By.XPATH, f"/html/body/div[11]/div/div[3]/section[3]")
       
        page_codes = page_data.find_elements(self.By.CLASS_NAME, f'value')
        page_titles = page_data.find_elements(self.By.CLASS_NAME, f'product-card__title')
        page_prices = page_data.find_elements(self.By.CLASS_NAME, f'price')
        page_status = page_data.find_elements(self.By.CLASS_NAME, f'badge__wrapper')
        page_images = page_data.find_elements(self.By.CLASS_NAME, f'product_name')
        loaded_data = [page_codes, page_titles, page_prices, page_status, page_images]
        time.sleep(2)
        return loaded_data


    def get_item_image(self, page_images, index):
        try:
            page_images[index].click()

            self.wait.until(self.EC.presence_of_element_located((self.By.TAG_NAME, f"img")))
            image_url = self.driver.find_element(self.By.TAG_NAME, f"img").get_attribute("src")
            image_bytes = requests.get(str(image_url)).content

            self.item_data.append(image_bytes)
            self.driver.back()
            time.sleep(2)
        except Exception:
            self.driver.refresh()
            time.sleep(1)
            self.driver.back()
            self.parsing_process()

    def load_more_items(self):
        try:
            self.driver.execute_script("window.scrollTo(0, 10000)") 
            time.sleep(1)
            self.wait.until(self.EC.presence_of_element_located((self.By.XPATH, f"/html/body/div[11]/div/div[3]/a")))
            self.driver.find_element(self.By.XPATH, f"/html/body/div[11]/div/div[3]/a").click()
        except Exception:
            return False
        

    def translate_item_status(self, status_item):
        if status_item == 'Ir noliktavā' or status_item == 'На складе':
            return 'In stock'
        elif status_item == 'Iespējams pasūtīt' or status_item == 'На заказ':
            return 'On order'
        elif status_item == 'Tikai veikalos' or status_item == 'Только в магазинах':
            return 'Only available in shops'