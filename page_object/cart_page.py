import requests
from selenium.webdriver.common.by import By
from common.base_page import BasePage
from utils.db_util import DBUtil


class CartPage(BasePage):
    cart_list = (By.ID, "cartList")
    checkout_btn = (By.ID, "checkout")

    def checkout(self):
        self.click(self.checkout_btn)

    def add_cart_real(self, user_id, goods_id, num):
        # 1. 接口-加入购物车
        res = requests.post("http://127.0.0.1:5000/api/cart/add",
                             json={"user_id": user_id, "goods_id": goods_id, "num": num})
        print("✅ 添加购物车结果：", res.json())
        # 2.数据库校验
        db = DBUtil()
        cart = db.query("SELECT * FROM cart WHERE user_id=%s AND goods_id=%s", (user_id, goods_id))
        db.close()
        assert len(cart) > 0
        return res.json()

    def get_cart_info(self):
        return self.get_text(self.cart_list)