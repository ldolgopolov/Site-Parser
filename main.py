import sqlite3
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import math
import time


# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()


url_main_page = "https://mpsmobile.de/en"
url_login_page = "https://mpsmobile.de/en/customer/login"
url_parsing = "https://mpsmobile.de/en/spare-parts-c-0274BA15B350?brand=apple,lg,samsung,huawei,xiaomi,sony,oppo,honor,asus,realme,oneplus,google&page="

profile_email = 'your-login'
profile_password = 'your-password'

# The words by which identify the right products
words_filter = ['LCD', 'Battery', 'Display', 'Vibration', 'Modulflex', 'Flexcable', 'Flex', 'Camera', 'Frontcamera', 'Earspeaker', 'Speaker', 'Sim', 'Button', 'Screw', 'Sensor', 'Adhesive', 'Home', 'Charging']
filter = ['iPhone 4', 'iPhone 4S', 'iPhone 4s', 'iPhone 4/4s', 'iPhone 3', 'iPhone 3G']

# Product categorization
prod_category = ['iPhone ']

# Pages for authorization
auth_pages = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170]

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
webdriver_path = Service(r"C:\your\path\to\chromedriver_win32\chromedriver.exe")
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


def authorization():
    driver.get(url_main_page)

    wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/header/div[2]/div[1]/div/div[2]/div/div[2]/div[4]")))
    driver.find_element(By.XPATH, "/html/body/header/div[2]/div[1]/div/div[2]/div/div[2]/div[4]").click()

    wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/header/div[2]/div[1]/div/div[2]/div/div[2]/div[4]/div/div/div[2]/ul/li[1]")))
    driver.find_element(By.XPATH, "/html/body/header/div[2]/div[1]/div/div[2]/div/div[2]/div[4]/div/div/div[2]/ul/li[1]").click()

    wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[2]/div/div/div[3]/div/div[2]/div/div[1]/div/form/div[1]/input")))
    email_input = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div[2]/div/div[1]/div/form/div[1]/input")
    email_input.clear()
    email_input.send_keys(profile_email)

    wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[2]/div/div/div[3]/div/div[2]/div/div[1]/div/form/div[2]/input")))
    password_input = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div[2]/div/div[1]/div/form/div[2]/input")
    password_input.clear()
    password_input.send_keys(profile_password)

    driver.execute_script("window.scrollTo(0, 100)") 
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div[2]/div/div[1]/div/form/div[3]/div[1]/div/button").click()
    time.sleep(2)


def sign_out():
    driver.get(url_main_page)
    
    wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/header/div[2]/div[1]/div/div[2]/div/div[2]/div[4]")))
    driver.find_element(By.XPATH, "/html/body/header/div[2]/div[1]/div/div[2]/div/div[2]/div[4]").click()
    
    driver.implicitly_wait(2)

    wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/header/div[2]/div[1]/div/div[2]/div/div[2]/div[4]/div/div/div[2]/ul/li[5]/a")))
    driver.find_element(By.XPATH, "/html/body/header/div[2]/div[1]/div/div[2]/div/div[2]/div[4]/div/div/div[2]/ul/li[5]/a").click()
    
    driver.implicitly_wait(2)


def parcing_process():
    cursor.execute('SELECT page_number FROM settings')
    page_number = cursor.fetchone()[0]
    cursor.execute('SELECT max_page_number FROM settings')
    max_page_number = cursor.fetchone()[0]

    while True:
        prod_list = []

        if page_number in auth_pages:
            sign_out()
            authorization()

        for i in range(1, 25):
            driver.get(f'{url_parsing}{page_number}')

            print(f"Page number: {page_number}  Item: {i}")
            
            wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[2]/div/div/div/div[2]/div/div[2]/div[{i}]/div/div[1]/a[3]/span/img")))
            find_id = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div/div[2]/div/div[2]/div[{i}]/div/div[1]/a[3]/span/img").get_attribute("src")
            id = find_id[:90][55:]

            if db_item_availability(id) == True:

                # Get product's titles
                wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[2]/div/div/div/div[2]/div/div[2]/div[{i}]/div/div[2]/h2/a")))
                find_title = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div/div[2]/div/div[2]/div[{i}]/div/div[2]/h2/a").text
                title = find_title.replace("OEM ", "").replace("Oem ", "").replace("für", "for")

                if filter_item(title) == True:
                    if w_item_availability(title) == True:

                        # Get product's prices
                        wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[2]/div/div/div/div[2]/div/div[2]/div[{i}]/div/div[2]/div[2]/div/table/tbody/tr[3]/td")))
                        find_price = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div/div[2]/div/div[2]/div[{i}]/div/div[2]/div[2]/div/table/tbody/tr[3]/td").text
                        price = find_price.replace(" €", "")

                        # Get product's images and id
                        wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[2]/div/div/div/div[2]/div/div[2]/div[{i}]/div/div[1]/a[3]")))
                        driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div/div[2]/div/div[2]/div[{i}]/div/div[1]/a[3]").click()

                        wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[2]/div[1]/div[3]/div/div[1]/div[1]/div/img")))
                        image_url = driver.find_element(By.XPATH, f"/html/body/div[2]/div[1]/div[3]/div/div[1]/div[1]/div/img").get_attribute("src")
                        image_bytes = requests.get(str(image_url)).content

                        prod_list.append([id, capitalize_first_letter(title), round_up_price(float(price) * 1.21), image_bytes])

                        # Add to DB
                        add_to_db(prod_list)

                        prod_list.pop()

                        print("Parsed!")

        page_number += 1
        if page_number == max_page_number + 1:
            cursor.execute('UPDATE settings SET page_number=?', (1,))
            conn.commit()
            break
        else:
            cursor.execute('UPDATE settings SET page_number=?', (page_number,))
            conn.commit()


def db_item_availability(id):
    cursor.execute('SELECT id_item FROM items')
    db_list = cursor.fetchall()

    if len(db_list) == 0:
        return True
    else:
        for i in range(len(db_list)):
            if id in db_list[i][0]:
                return False
            elif i == len(db_list) - 1:
                if not id in db_list[i][0]:
                    return True
            

def w_item_availability(title):
    for i in range(len(words_filter)):
        if words_filter[i] in title or words_filter[i].lower() in title:
            return True
        

def filter_item(title):
    for i in range(len(filter)):
        if filter[i] in title or filter[i].lower() in title:
            return False
        elif i == len(filter) - 1:
            if not filter[i] in title:
                return True
            elif not filter[i].lower() in title:
                return True


def add_to_db(prod_list):
    for i in range(len(prod_list)):
        item = prod_list[i]
        # Insert item's title to the db
        cursor.execute('INSERT INTO items (id_item) VALUES(?)', (item[0],))

        # Insert item's id, price and image to the db
        cursor.execute('UPDATE items SET title_item=?, price_item=?, image_item=? WHERE id_item=?', (item[1], item[2], item[3], item[0],))
        conn.commit()


def capitalize_first_letter(input_string):
    first_letter = input_string[0].upper()
    rest_of_string = input_string[1:]

    return first_letter + rest_of_string


def convert_to_preferred_format(sec): 
    sec = sec % (24 * 3600) 
    hour = sec // 3600 
    sec %= 3600 
    min = sec // 60 
    sec %= 60 

    return "%02d:%02d:%02d" % (hour, min, sec)


def round_up_price(number):
    # Convert the number to the nearest half
    nearest_half = math.ceil(number * 2) / 2
    return nearest_half


def get_data():
    try:
        # ---------------------- AUTHORIZATION ----------------------
        authorization()
        
        # ---------------------- DATA PARSING ----------------------
        parcing_process()


    except Exception as ex:
        print(f'ERROR:\n{ex}')
        get_data()

    finally:
        time.sleep(3)
        driver.close()
        driver.quit()


def main():
    start = time.time()

    get_data()

    finish = time.time()
    print(f"Program 'get_data' running time - {convert_to_preferred_format(finish - start)}\nFinish 'get_data' - {convert_to_preferred_format(finish)}")


if __name__ == '__main__':
    main()