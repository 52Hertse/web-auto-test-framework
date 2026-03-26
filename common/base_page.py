import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.logger import log
from config.config import SCREENSHOT_DIR

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_click(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def send(self, loc, value):
        ele = self.wait_click(loc)
        ele.clear()
        ele.send_keys(value)
        log.info(f"✅ 输入：{value}")

    def click(self, loc):
        self.wait_click(loc).click()
        log.info(f"✅ 点击元素：{loc}")

    def get_alert_text(self):
        alert = self.driver.switch_to.alert
        text = alert.text
        alert.accept()
        log.info(f"✅ 弹窗内容：{text}")
        return text

    def screenshot(self, name="截图"):
        import os, time
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        path = f"{SCREENSHOT_DIR}/{time.strftime('%Y%m%d_%H%M%S')}.png"
        self.driver.save_screenshot(path)
        allure.attach.file(path, name=name, attachment_type=allure.attachment_type.PNG)
        return path