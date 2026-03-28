import requests
from selenium.webdriver.common.by import By
from common.base_page import BasePage
from utils.db_util import DBUtil


class SearchPage(BasePage):
    # 元素定位
    input_loc = (By.ID, "searchInput")
    keyword = (By.ID, "keyword")
    search_btn = (By.ID, "searchBtn")
    result = (By.ID, "searchResult")
    add_to_cart = (By.ID, "addToCart")
    go_cart = (By.ID, "goCart")

    # def search(self, key):
    #     self.send(self.input_loc, key)
    #     self.click(self.search_btn)

    # def get_result(self):
    #     return self.get_text(self.result_loc)
    def search_goods(self, keyword):
        self.send(self.input_loc, keyword)
        self.click(self.search_btn)

    def go_cart_page(self):
        self.click(self.go_cart)

    # 搜索商品
    def search_real(self, keyword):
        # UI操作
        self.send(self.input_loc, keyword)
        self.click(self.search_btn)

        # 接口断言
        res=requests.post(
            url="http://127.0.0.1:5000/api/search",
            json={
                "keyword": keyword,
            })
        assert res.json().get("code") == 0

        # 数据库断言
        db=DBUtil()
        goods=db.query("select * from goods where name like '%{}%'".format(keyword))
        db.close()
        assert len(goods) > 0
        return res.json()

    # 加入购物车
    def add_to_cart_real(self):
        # 1. 接口-加入购物车
        self.click(self.add_to_cart)