from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import time_ns


from otzovyk import OtzovykParser
from zoon import ZoonParser
from twogis import TwoGISParser



class Main:
    def __init__(self) -> None:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument("window-size=1280,800")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        service = Service(executable_path=r"C:\Users\Нажмутдин\Desktop\Python\Парсинг\SeleniumDrivers")
        self.driver = webdriver.Chrome(service=service, options=chrome_options)


    def main(self):
        url = input("Enter item url: ")
        review = input("Enter review that needed to be found: ")
        start = time_ns()
        parsers = {
            "2gis": TwoGISParser,
            "otzovik": OtzovykParser,
            "zoon": ZoonParser,
        }

        parser = parsers[url.split("/")[2].split(".")[0]](self.driver, url, review)
        parser.parse_site()
        end = time_ns()

        print(f"Run time: {(end - start)/1_000_000_000} s")


if __name__ == '__main__':
    Main().main()
    