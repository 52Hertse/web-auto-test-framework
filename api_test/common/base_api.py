import requests


class BaseApi:
    HOST = "http://127.0.0.1:5000"

    def send(self, method, url, **kwargs):
        return requests.request(method, self.HOST + url, **kwargs)
