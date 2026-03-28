# import pytest
# import allure
# from common.web_driver import WebDriver
# from page_object.login_page import LoginPage
# from page_object.index_page import IndexPage
# from page_object.search_page import SearchPage
# from page_object.cart_page import CartPage
# from config.config import BASE_URL
#
# @pytest.fixture(scope="class")
# def driver():
#     driver = WebDriver.get_driver()
#     driver.get(BASE_URL)  # 指向 login.html
#     yield driver
#     WebDriver.quit_driver()
#
# @allure.feature("迷你电商项目")
# class TestShopFlow:
#     @allure.story("完整业务流程：登录 → 搜索 → 购物车")
#     def test_full_flow(self, driver):
#         # 1. 登录
#         login = LoginPage(driver)
#         login.login_action("admin", "123456")
#         # 处理登录成功弹窗
#         alert = driver.switch_to.alert
#         alert.accept()
#
#         # 2. 首页验证
#         index = IndexPage(driver)
#         assert index.get_user_name() == "admin", "登录失败，用户名不匹配"
#
#         # 3. 跳转到搜索页并搜索
#         index.to_search()
#         search = SearchPage(driver)
#         search.search_goods("笔记本电脑")
#         assert "笔记本电脑" in search.get_search_result(), "搜索结果异常"
#
#         # 4. 加入购物车并跳转
#         search.add_to_cart()
#         cart = CartPage(driver)
#         assert cart.get_cart_count() == 2, "购物车商品数量异常"
#
#         # 5. 结算
#         cart.checkout()
#         assert "结算" in driver.title, "结算页面跳转失败"