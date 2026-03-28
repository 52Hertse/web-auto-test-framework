from selenium.webdriver.common.by import By
from common.base_page import BasePage

class IndexPage(BasePage):
    # 元素定位
    user_text = (By.ID, "user")
    go_search = (By.ID, "goSearch")

    def get_user_name(self):
        return self.get_text(self.user_text)

    def to_search(self):
        self.click(self.go_search)
