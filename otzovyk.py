from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from threading import Thread
from numpy import array_split
from random import choices
from string import ascii_lowercase
from twocaptcha import TwoCaptcha
from lxml import html
from time import sleep
from os import remove



class OtzovykParser:
    def __init__(self, driver: webdriver.Chrome, url: str, review: str):
        self.driver = driver
        self.url = url
        self.review = review
        self.solver = TwoCaptcha("111a7122a19bcd318ccb16c285caf148")
    

    def get_screenshot(self, href: str):
        index = self.review_urls.index(href)
        page_number = index // 20
        print(page_number, index)
        print(index - page_number * 20 + 1)

        self.driver.get(self.url + f"{page_number + 1}/")

        review = self.driver.find_elements(By.XPATH, "//div[@class='item status4 mshow0']")[index - page_number * 20]
        name = review.find_elements(By.XPATH, "//div[@class='item status4 mshow0']//a[@class='user-login']/span")[index - page_number * 20]
        review.screenshot(f'{name.text}.png')
        self.driver.close()
            
    
    def solve_captcha(self, driver: webdriver.Chrome):
        captcha_img = driver.find_element(By.XPATH, "//img")
        file_name = "".join(choices(ascii_lowercase, k=5)) + ".png"
        captcha_img.screenshot(file_name)
        result = self.solver.normal(file_name)
        remove(file_name)
        driver.find_element(By.XPATH, "//input[@name ='llllllllllll']").send_keys(result["code"])
        sleep(.3)
        driver.find_element(By.XPATH, "//input[@value = '     Я не робот!     ']").click()

    
    def get_full_review(self, href: str, driver: webdriver.Chrome):
        url = self.url.split("/reviews")[0] + href
        driver.get(url)

        if "Вы робот?" in driver.page_source:
            self.solve_captcha(driver)
            print("captcha solved")

        page = driver.page_source
        tree = html.fromstring(page)

        text = tree.xpath("//div[@class='review-body description']/text()")
        text = "\n".join(text)
        if self.review == text:
            self.status = True
            self.href = href
            
        print(f"review from {url} successfully received")
    

    def get_reviews(self, urls: list):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("window-size=1280,800")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        service = Service(executable_path=r"C:\Users\Нажмутдин\Desktop\Python\Парсинг\SeleniumDrivers")
        driver = webdriver.Chrome(service=service, options=chrome_options)

        for url in urls:
            self.get_full_review(url, driver)
            if self.status:
                print("review has found")
                break
            sleep(1)
        

    def run_threads(self, amountThreads: int):
        threads = []
        for urls in array_split(self.review_urls, amountThreads):
            thread = Thread(target=self.get_reviews, args=(urls, ))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()


    def parse_page(self, page: str):
        tree = html.fromstring(page)

        review_urls = tree.xpath("//div[@class='review-bar']/a/@href")
        
        return review_urls


    def get_review_urls(self):
        self.review_urls = []
        page = 1
        while True:

            self.driver.get(self.url + f"{page}/")

            if "Вы робот?" in self.driver.page_source:
                self.solve_captcha(self.driver)
                print("captcha solved")

            urls = self.parse_page(self.driver.page_source)
            

            if len(urls) == 0:
                break

            self.review_urls += urls
            print(f"urls from page {page} successfully received")
            page += 1
            sleep(2)
        self.cookies = self.driver.get_cookies()
    

    def parse_site(self):
        self.get_review_urls()
        self.run_threads(3)
        self.get_screenshot(href=self.href)
        self.driver.quit()
        if not self.status:
            print("Review hasn't found")
