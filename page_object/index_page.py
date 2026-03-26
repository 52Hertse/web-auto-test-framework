from selenium.webdriver.common.by import By
from common.base_page import BasePage

class IndexPage(BasePage):
    user_text = (By.ID, "user")
    to_search = (By.ID, "goSearch")

    def get_user(self):
        return self.get_text(self.user_text)

    def go_search_page(self):
        self.click(self.to_search)