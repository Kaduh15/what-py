from time import sleep
from urllib.parse import quote
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException


def wait_element_exit(driver, by, element):
    while True:
        try:
            driver.find_element(by, element)
            sleep(1)
        except NoSuchElementException:
            break


def wait_element(driver: Chrome, by, element):
    while True:
        try:
            element_found = driver.find_element(by, element)
            return element_found
        except NoSuchElementException:
            sleep(1)


class WAClient:
    IS_LOGGED = False
    __headless = True

    def __init__(self, headless=True):
        self.__headless = headless

        chrome_options = ChromeOptions()

        chrome_options.add_argument("--sendbox")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        if self.__headless:
            chrome_options.add_argument("--headless=new")

        chrome_service = ChromeService(ChromeDriverManager().install())

        driver = Chrome(options=chrome_options, service=chrome_service)
        driver.get("https://web.whatsapp.com/")

        self.driver = driver
        self.is_logged()

    def is_logged(self):
        if self.IS_LOGGED:
            return self.IS_LOGGED

        try:
            item = bool(
                self.driver.execute_script(
                    "return window.localStorage.getItem(arguments[0]);", "last-wid-md"
                )
            )
            self.IS_LOGGED = item
            return self.IS_LOGGED
        except NoSuchElementException:
            return False

    def login(self):
        if self.is_logged():
            return

        qr_code = self.get_qr_code()
        print("QR Code: ", qr_code)
        wait_element_exit(self.driver, By.CLASS_NAME, "_19vUU")

        self.IS_LOGGED = True

    def get_qr_code(self):
        if self.is_logged():
            return None

        self.driver.get("https://web.whatsapp.com/")
        element = wait_element(self.driver, By.CSS_SELECTOR, "._19vUU[data-ref]")
        return element.get_attribute("data-ref")

    def send_message(self, phone, message):
        if not self.is_logged():
            return False

        self.driver.get(
            f"https://web.whatsapp.com/send?phone={phone}&text={quote(message)}"
        )
        element = wait_element(self.driver, By.CSS_SELECTOR, "span[data-icon='send']")
        sleep(2)
        element.click()
        return True
