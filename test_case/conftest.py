import pytest
import os
from common.web_driver import WebDriver

@pytest.fixture(scope="function")
def driver():
    driver = WebDriver.get_driver()
    # 绝对正确打开本地登录页
    # base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # login_path = f"file:///{base_dir}/login.html"
    # driver.get(login_path.replace("\\", "/"))
    LOGIN_URL = "http://127.0.0.1:5000/login.html"
    driver.get(LOGIN_URL)
    yield driver
    WebDriver.quit_driver()