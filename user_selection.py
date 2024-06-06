from config import Config
import time


class CreateRequest():
    def __init__(self, driver, wait, EC, By):
        self.driver = driver
        self.url_page = Config.url_page
        self.wait = wait
        self.EC = EC
        self.By = By
        self.request = []


    def driver_quiting(self):
        time.sleep(3)
        self.driver.close()
        self.driver.quit()


    def check_answer(self, answer, count):
        try:
            num = int(input("Enter a number: "))
            if num in list(range(1, count)):
                answer.append(num)
                return answer
            else:
                print("Wrong answer!")
                self.check_answer(answer, count)
        except:
            print("Wrong answer!")
            self.check_answer(answer, count)



    def cookies_acception(self):
        self.wait.until(self.EC.presence_of_element_located((self.By.XPATH, f"/html/body/div[1]/div/div/div[3]/button[3]")))
        time.sleep(1)
        self.driver.find_element(self.By.XPATH, f"/html/body/div[1]/div/div/div[3]/button[3]").click()

    
    def parsing_setup(self, x):
        self.driver.get(self.url_page)
        time.sleep(3)
        if x == True:
            self.cookies_acception()
        self.select_lang()
        self.category_selection()

    
    def select_lang(self):
        self.wait.until(self.EC.presence_of_element_located((self.By.XPATH, f"/html/body/header/div[2]/div[1]/div[1]/div/ul/li[1]")))
        self.driver.find_element(self.By.XPATH, f"/html/body/header/div[2]/div[1]/div[1]/div/ul/li[1]").click()
        time.sleep(1)
        self.wait.until(self.EC.presence_of_element_located((self.By.XPATH, f"/html/body/header/div[2]/div[1]/div[1]/div/ul/li[2]/ul")))
        lang_element = self.driver.find_element(self.By.XPATH, f"/html/body/header/div[2]/div[1]/div[1]/div/ul/li[2]/ul")
        langs = lang_element.find_elements(self.By.CLASS_NAME, 'dropdown__list-item')

        lang_list = []
        for i in langs:
            lang_list.append(i.text)

        print(f'\nSelect the language in which you will parse items:')
        j = 1
        for i in lang_list: 
            print(f"{j}. {i}")
            j += 1

        answer = []
        self.check_answer(answer, j)

        self.request.append(lang_list[answer[0]-1])
        self.driver.find_element(self.By.XPATH, f"/html/body/header/div[2]/div[1]/div[1]/div/ul/li[2]/ul/li[{answer[0]}]").click()
        time.sleep(3)


    def category_selection(self):
        self.wait.until(self.EC.presence_of_element_located((self.By.XPATH, f"/html/body/header/div[2]/div[3]/div/nav/ul")))

        data = self.driver.find_element(self.By.XPATH, f"/html/body/header/div[2]/div[3]/div/nav/ul").text
        data_list = data.strip().split('\n')
        
        print(f'\nHello!\n\nPick the category you want to parse:')
        j = 1
        for i in data_list: 
            print(f"{j}. {i}")
            j += 1
        
        answer = []
        self.check_answer(answer, j)
        self.request.append(data_list[answer[0]-1])
        self.driver.find_element(self.By.XPATH, f"/html/body/header/div[2]/div[3]/div/nav/ul/li[{answer[0]}]/div[1]/a").click()
        self.subcategory_selection(answer[0])


    def subcategory_selection(self, category_answer):
        self.wait.until(self.EC.presence_of_element_located((self.By.XPATH, f"/html/body/header/div[2]/div[3]/div/nav/ul/li[{category_answer}]/div[2]")))
        category_element = self.driver.find_element(self.By.XPATH, f"/html/body/header/div[2]/div[3]/div/nav/ul/li[{category_answer}]/div[2]")
        data = category_element.find_elements(self.By.CLASS_NAME, 'sub-menu__block-heading')
        data_list = []
        for i in data:
            data_list.append(i.text)
        
        print(f'\nPick the subcategory you want to parse:')
        j = 1
        for i in data_list: 
            print(f"{j}. {i}")
            j += 1
        
        answer = []
        self.check_answer(answer, j)
        self.request.append(data_list[answer[0]-1])
        self.subcategory_option_selection(category_answer, answer[0])


    def subcategory_option_selection(self, category_answer, subcategory_answer):
        self.wait.until(self.EC.presence_of_element_located((self.By.XPATH, f"/html/body/header/div[2]/div[3]/div/nav/ul/li[{category_answer}]/div[2]/div[2]/div/div[{subcategory_answer}]/ul")))

        data = self.driver.find_element(self.By.XPATH, f"/html/body/header/div[2]/div[3]/div/nav/ul/li[{category_answer}]/div[2]/div[2]/div/div[{subcategory_answer}]/ul").text
        data_list = data.strip().split('\n')
        
        print(f"\nPick the subcategory's option you want to parse:")
        j = 1
        for i in data_list: 
            print(f"{j}. {i}")
            j += 1
        
        answer = []
        self.check_answer(answer, j)
        self.request.append(data_list[answer[0]-1])
        self.driver.find_element(self.By.XPATH, f"/html/body/header/div[2]/div[3]/div/nav/ul/li[{category_answer}]/div[2]/div[2]/div/div[{subcategory_answer}]/ul/li[{answer[0]+1}]/a").click()
        self.manufacturer_selection()

        
    def manufacturer_selection(self):
        self.wait.until(self.EC.presence_of_element_located((self.By.XPATH, f"/html/body/div[11]/div/div[2]/section")))
        sort_menu = self.driver.find_element(self.By.XPATH, f"/html/body/div[11]/div/div[2]/section")
        self.driver.find_element(self.By.XPATH, f"/html/body/div[11]/div/div[2]/section/ul/li[1]/button").click()
        sort_buttons = sort_menu.find_elements(self.By.CLASS_NAME, 'sort-menu__item')
        
        for button in sort_buttons:
            if 'Manufacturer' in button.text or 'Ražotājs' in button.text or 'Производитель' in button.text:
                button.click()

                data = button.find_elements(self.By.CLASS_NAME, 'sort-menu__sub')
                data_list = data[0].text.split('\n')[::2]
                
                if len(data_list) <= 1:
                    return
                print(f"\nPick the manufacturer you want to parse:")
                j = 1
                for i in data_list: 
                    print(f"{j}. {i}")
                    j += 1

                answer = []
                self.check_answer(answer, j)
                self.request.append(data_list[answer[0]-1])
                
                for position in sort_buttons:
                    if position.text.split('\n')[0] == data_list[answer[0]-1]:
                        position.click()
                        if '...Show all options' in data_list[answer[0]-1] or '...Rādīt visas iespējas' in data_list[answer[0]-1] or '...Показать все варианты' in data_list[answer[0]-1]:
                            self.request.pop()
                            self.check_all_options()
                        time.sleep(3)
                        self.request_confirmation()
                        break
                break

    def check_all_options(self):
        sort_menu = self.driver.find_element(self.By.XPATH, f"/html/body/div[11]/div/div[2]/section")
        sort_buttons = sort_menu.find_elements(self.By.CLASS_NAME, 'sort-menu__item')

        for button in sort_buttons:
            if 'Manufacturer' in button.text or 'Ražotājs' in button.text or 'Производитель' in button.text:
                data = button.find_elements(self.By.CLASS_NAME, 'sort-menu__sub')
                data_list = data[0].text.split('\n')[::2]
                print(data_list)
                if len(data_list) <= 1:
                    return
                print(f"\nPick the manufacturer you want to parse:")
                j = 1
                for i in data_list: 
                    print(f"{j}. {i}")
                    j += 1

                answer = []
                self.check_answer(answer, j)
                self.request.append(data_list[answer[0]-1])
                break



    def request_confirmation(self):
        print(f'\n----------- REQUEST -----------\nLanguage: {self.request[0]}\n\nCategory: {self.request[1]}\nSubcategory: {self.request[2]}\n- {self.request[3]}\nManufacturer: {self.request[4]}\n-------------------------------')
        answer = input('\nStart parsing? Yes(y) / No(N) / Exit(e): ')
        if answer == 'N':
            self.parsing_setup(False)
        elif answer == 'e':
            self.driver_quiting()
        elif answer == 'y':
            pass
        else:
            print("Wrong answer!")
            self.request_confirmation()
