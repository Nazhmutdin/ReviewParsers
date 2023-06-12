from selenium import webdriver
from twocaptcha import TwoCaptcha
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from lxml import html
from time import sleep


class TwoGISParser:
    def __init__(self, driver: webdriver.Chrome, url: str, review: str):
        self.driver = driver
        self.url = url
        self.review = review
        self.solver = TwoCaptcha("111a7122a19bcd318ccb16c285caf148")

    
    def get_screenshot(self, index: int):
        items = self.driver.find_elements(By.XPATH, "//div[./div/div/div/div/span/text() = '/5']/div")
        items[index + 2].screenshot("image.png")
    

    def get_all_reviews(self):
        action = ActionChains(self.driver)
        while True:
            try:
                button = self.driver.find_element(By.XPATH, "//button[text() = 'Загрузить ещё']")
                action.scroll_to_element(button).perform()
                sleep(2)
            except:
                break
        tree = html.fromstring(self.driver.page_source)

        self.reviews = tree.xpath("//div[./div/div/div/div/span/text() = '/5']/div/div[3]/div[1]/a/text()")
        print(len(self.reviews))

    

    def parse_site(self):
        self.driver.get("/tab/reviews?m".join(self.url.split("?m")))
        self.get_all_reviews()

        for e, review in enumerate(self.reviews):
            if self.review in review:
                self.get_screenshot(e)
                print(f"Review has found. Index: {e + 1}")
                break
        
        self.driver.close()
        self.driver.quit()
