import pytest
import allure
from page_object.login_page import LoginPage
from common.logger import log


@allure.feature("登录模块")
class TestLogin:

    @allure.story("登录场景")
    @pytest.mark.parametrize("user,pwd,expect", [
        ("admin", "123456", "登录成功"),
        ("test", "654321", "登录失败")
    ])
    def test_login(self, driver, user, pwd, expect):
        allure.dynamic.title(f"登录：{user}")

        # 1. 登录
        login = LoginPage(driver)
        login.login_action(user, pwd)

        # ================= 核心修复：等待弹窗出现，不会卡死 =================
        try:
            from selenium.webdriver.support.wait import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            # 最多等 3 秒，不会无限卡死
            WebDriverWait(driver, 3).until(EC.alert_is_present())

            # 切换弹窗
            alert = driver.switch_to.alert
            result = alert.text
            alert.accept()
            log.info(f"弹窗内容：{result}")

        except:
            result = ""
            log.warning("未检测到弹窗")

        # 断言
        assert expect in result, f"预期：{expect}，实际：{result}"