import requests
from selenium.webdriver.common.by import By
from common.base_page import BasePage
from utils.db_util import DBUtil


class LoginPage(BasePage):
    user_loc = (By.ID, "username")
    pwd_loc = (By.ID, "password")
    btn_loc = (By.ID, "submit")

    def login_action(self, username, password):
        self.send(self.user_loc, username)
        self.send(self.pwd_loc, password)
        self.click(self.btn_loc)

    # 真实登录业务（接口+数据库断言）
    def login_real(self, username, password):
        self.login_action(username, password)

        try:
            alert=self.driver.switch_to.alert
            alert.accept()
            print("✅ 弹窗内容：", alert.text)
        except:
            pass
        # 接口校验
        res = requests.post(
            url="http://127.0.0.1:5000/api/login",
            json={
                "username": username,
                "password": password
            })
        return res.json()
        print("✅ 接口返回：", res.json())

        # 数据库校验
        db = DBUtil()
        user=db.query("SELECT * FROM user WHERE username=%s AND password=%s",
                   (username, password))
        db.close()

        assert res.json().get("code") == 0
        assert len(user)>0

    def get_user_name(self):
        return self.get_text(self.user_loc)
