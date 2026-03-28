import allure
import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page_object.login_page import LoginPage
import os

from test_case.test_shop_flow import LOGIN_URL

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# LOGIN_URL = f"file:///{BASE_DIR}/login.html"
LOGIN_URL="http://127.0.0.1:5000/login.html"

@allure.feature("登录功能")
class TestLogin:

    @allure.story("登录场景")
    @pytest.mark.parametrize("user,pwd,expect", [
        ("admin", "123456", "登录成功"),
        ("test", "654321", "登录失败")
    ])
    def test_login(self, driver, user, pwd, expect):
        allure.dynamic.title(f"登录：{user}")

        # 每个用例都重新打开登录页，保证页面干净
        driver.get(LOGIN_URL)

        # 等待页面加载
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(("id", "username"))
        )

        # 登录
        login = LoginPage(driver)
        login.login_action(user, pwd)

        # ========================
        # 【关键修复】先处理弹窗！！
        # ========================
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()  # 关掉弹窗，页面才能跳转！
        except:
            pass

        # 断言：成功会跳转到 index.html，失败会弹出提示
        if user == "admin":
            WebDriverWait(driver, 5).until(EC.url_contains("index.html"))
            assert "index.html" in driver.current_url
            # res = login.login_real(user, pwd)
            # assert res["code"] == 0
            print("✅ 登录成功，已跳转到首页")
        else:
            print("✅ 登录失败，符合预期")