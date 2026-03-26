from selenium.webdriver.common.by import By
from common.base_page import BasePage

class LoginPage(BasePage):
    user = (By.ID, "username")
    pwd = (By.ID, "password")
    btn = (By.ID, "submit")

    def to_login(self, username, password):
        self.send(self.user, username)
        self.send(self.pwd, password)
        self.click(self.btn)