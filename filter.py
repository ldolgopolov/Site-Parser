from config import Config
import time


class CreateRequest():
    def __init__(self, driver, wait, EC, By):
        self.driver = driver
        self.url_page = Config.url_page
        self.wait = wait
        self.EC = EC
        self.By = By


    def driver_quiting(self):
        self.driver.close()
        self.driver.quit()


    def check_answer(self, answer, count):
        num = int(input("Enter a number of category: "))
        
        if num in list(range(1, count)):
            answer.append(num)
            return answer
        else:
            print("Wrong answer!")
            self.check_answer(answer, count)



    def cookies_acception(self):
        self.wait.until(self.EC.presence_of_element_located((self.By.XPATH, f"/html/body/div[1]/div/div/div[3]/button[3]")))
        time.sleep(1)
        self.driver.find_element(self.By.XPATH, f"/html/body/div[1]/div/div/div[3]/button[3]").click()



    def category_selection(self):
        self.driver.get(self.url_page)
        time.sleep(1)

        self.cookies_acception()
        
        self.wait.until(self.EC.presence_of_element_located((self.By.XPATH, f"/html/body/header/div[2]/div[3]/div/nav/ul")))

        data = self.driver.find_element(self.By.XPATH, f"/html/body/header/div[2]/div[3]/div/nav/ul").text
        data_list = data.strip().split('\n')
        
        print(f'\nHello!\n\nPick the category you want to parse?')
        j = 1
        for i in data_list: 
            print(f"{j}. {i}")
            j += 1
        
        answer = []
        self.check_answer(answer, j)

        self.driver.find_element(self.By.XPATH, f"/html/body/header/div[2]/div[3]/div/nav/ul/li[{answer[0]}]/div[1]/a").click()
        self.subcategory_selection(answer[0])


    def subcategory_selection(self, category_answer):


        self.wait.until(self.EC.presence_of_element_located((self.By.XPATH, f"/html/body/header/div[2]/div[3]/div/nav/ul/li[{category_answer}]/div[2]")))
        category_element = self.driver.find_element(self.By.XPATH, f"/html/body/header/div[2]/div[3]/div/nav/ul/li[{category_answer}]/div[2]")
        data = category_element.find_elements(self.By.CLASS_NAME, 'sub-menu__block-heading')
        data_list = []
        for i in data:
            data_list.append(i.text)
        
        print(f'\nPick the subcategory you want to parse?')
        j = 1
        for i in data_list: 
            print(f"{j}. {i}")
            j += 1
        
        answer = []
        self.check_answer(answer, j)
        self.subcategory_point(category_answer, answer[0])


    def subcategory_point(self, category_answer, subcategory_answer):

        self.wait.until(self.EC.presence_of_element_located((self.By.XPATH, f"/html/body/header/div[2]/div[3]/div/nav/ul/li[{category_answer}]/div[2]/div[2]/div/div[{subcategory_answer}]/ul")))

        data = self.driver.find_element(self.By.XPATH, f"/html/body/header/div[2]/div[3]/div/nav/ul/li[{category_answer}]/div[2]/div[2]/div/div[{subcategory_answer}]/ul").text
        data_list = data.strip().split('\n')
        
        print(f"\nPick the subcategory's type you want to parse?")
        j = 1
        for i in data_list: 
            print(f"{j}. {i}")
            j += 1
        
        answer = []
        self.check_answer(answer, j)

        self.driver.find_element(self.By.XPATH, f"/html/body/header/div[2]/div[3]/div/nav/ul/li[{category_answer}]/div[2]/div[2]/div/div[{subcategory_answer}]/ul/li[{answer[0]+1}]/a").click()

        


        
