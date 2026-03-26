from selenium.webdriver.common.by import By
from common.base_page import BasePage

class SearchPage(BasePage):
    input_box = (By.ID, "searchInput")
    btn = (By.ID, "searchBtn")
    result = (By.ID, "searchResult")
    go_cart = (By.ID, "goCart")

    def search(self, key):
        self.send(self.input_box, key)
        self.click(self.btn)

    def get_result(self):
        return self.get_text(self.result)

    def go_cart_page(self):
        self.click(self.go_cart)