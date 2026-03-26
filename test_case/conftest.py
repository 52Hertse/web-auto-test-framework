import pytest
import os
from common.web_driver import WebDriver

@pytest.fixture(scope="class")
def driver():
    driver = WebDriver.get_driver()
    # 绝对正确打开本地登录页
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    login_path = f"file:///{base_dir}/login.html"
    driver.get(login_path.replace("\\", "/"))
    yield driver
    WebDriver.quit_driver()