from api_test.common.base_api import BaseApi

class LoginApi(BaseApi):
    def login(self, username, password):
        url = "https://httpbin.org/post"
        data = {
            "username": username,
            "password": password
        }
        return self.send("POST", url, data=data)