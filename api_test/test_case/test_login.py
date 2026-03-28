import allure
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from api_test.api.login_api import LoginApi

@allure.feature("接口自动化模块")
class TestLoginApi:
    @allure.story("登录接口测试")
    def test_login(self):
        res = LoginApi().login("admin", "123456")
        assert res.status_code == 200
        print("✅ 接口用例执行成功！")