from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.config import HEADLESS, IMPLICIT_WAIT
from common.logger import log

class WebDriver:
    _driver = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            option = webdriver.ChromeOptions()
            option.add_argument("--start-maximized")
            option.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            option.add_argument("--disable-gpu")
            option.add_argument("--no-sandbox")

            if HEADLESS:
                option.add_argument("--headless=new")

            cls._driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=option
            )
            cls._driver.implicitly_wait(IMPLICIT_WAIT)
            log.info("✅ 浏览器驱动初始化完成")
        return cls._driver

    @classmethod
    def quit_driver(cls):
        if cls._driver:
            cls._driver.quit()
            cls._driver = None
            log.info("✅ 浏览器已关闭")