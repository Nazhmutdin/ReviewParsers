from selenium import webdriver
from twocaptcha import TwoCaptcha
from selenium.webdriver.common.by import By
from lxml import html
from time import sleep



class ZoonParser:
    def __init__(self, driver: webdriver.Chrome, item_url: str, review: str):
        self.driver = driver
        self.item_url = item_url + "reviews/"
        self.review = review
        self.solver = TwoCaptcha("111a7122a19bcd318ccb16c285caf148")

    
    def get_screenshot(self, index: int):
        items = self.driver.find_elements(By.XPATH, "(//div[@class='feedbacks-left'])/ul/li")

        items[index].screenshot("image.png")
    

    def get_page_html(self):
        try:
            button = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Показать ещё')]")
            button.click()
            sleep(1)
            self.page = self.driver.page_source
        except:
            self.page = self.driver.page_source

    
    def get_all_reviews(self):
        tree = html.fromstring(self.page)
        self.reviews = []

        reviews = tree.xpath("//div[contains(div/text(), 'Комментарий') or contains(div/text(), 'Достоинства')]")
        for review in reviews:
            self.reviews.append(review.text_content().replace(u'\xa0', u' '))

        

    def parse_site(self):
        self.driver.get(self.item_url)
        sleep(1)
        self.get_page_html()

        self.get_all_reviews()

        for e, review in enumerate(self.reviews):
            if self.review in review:
                self.get_screenshot(e)
                print(f"review has found. Index: {e + 1}")
                break


        self.driver.close()
        self.driver.quit()

        a = "//div[contains(div/text(), 'Комментарий') or contains(div/text(), 'Достоинства')]"
