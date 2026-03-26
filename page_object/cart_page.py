from selenium.webdriver.common.by import By
from common.base_page import BasePage

class CartPage(BasePage):
    checkout_btn = (By.ID, "checkout")
    def checkout(self):
        self.click(self.checkout_btn)