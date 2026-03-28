import allure
import pymysql
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

from api_test.api.search_api import SearchApi
from page_object.cart_page import CartPage
from page_object.login_page import LoginPage
from page_object.search_page import SearchPage

# 获取本地文件绝对路径（保证不报错）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# LOGIN_URL = f"file:///{BASE_DIR}/login.html"
# SEARCH_URL = f"file:///{BASE_DIR}/search.html"
# CART_URL = f"file:///{BASE_DIR}/cart.html"
LOGIN_URL = "http://127.0.0.1:5000/login.html"
SEARCH_URL = "http://127.0.0.1:5000/search.html"
CART_URL = "http://127.0.0.1:5000/cart.html"


@allure.feature("迷你电商完整流程")
@allure.story("登录 → 搜索 → 购物车 → 结算 全流程自动化")
def test_full_business_flow(driver):
    # 1.登录（真实业务：接口+DB断言）
    login = LoginPage(driver)
    res = login.login_real("admin", "123456")
    # 调试查看返回结果
    print("接口返回：", res)
    # 接口断言
    assert res is not None
    assert res["code"] == 0
    user_id = res["userId"]
    print("✅ 真实登录成功，用户ID：", user_id)

    # UI登录
    login.login_action("admin", "123456")
    assert login.get_user_name() == "admin", "登录失败，用户名不匹配"
    print("✅ 登录成功，已跳转到首页")
    # 关掉弹窗
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass

    # 进入搜索页（解决超时问题）
    driver.get(SEARCH_URL)
    # 等待页面加载
    WebDriverWait(driver, 5).until(EC.url_contains("search.html"))
    # 2.搜索（三层断言）
    search = SearchPage(driver)
    keyword = "笔记本"
    print(f"\n🔍 正在搜索关键词：{keyword}")
    goods = search.search_real(keyword)
    assert len(goods["data"]) > 0
    print("✅ 搜索成功，商品：", goods)

    # 3.加入购物车
    search.add_to_cart()

    # 4.查看购物车
    cart = CartPage(driver)
    info = cart.get_cart_info()
    print("🛒 购物车信息：", info)
    assert "笔记本电脑" in info
    print("✅ 真实加入购物车成功")

    print("\n🎉🎉🎉 【真实业务】全流程 100% 执行完成！")
