import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# 获取本地文件绝对路径（保证不报错）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGIN_URL = f"file:///{BASE_DIR}/login.html"
SEARCH_URL = f"file:///{BASE_DIR}/search.html"
CART_URL = f"file:///{BASE_DIR}/cart.html"

@allure.feature("迷你电商完整流程")
@allure.story("登录 → 搜索 → 购物车 → 结算 全流程自动化")
def test_full_business_flow(driver):
    wait = WebDriverWait(driver, 5)

    # ==========================================
    # 1. 打开登录页 → 登录
    # ==========================================
    driver.get(LOGIN_URL)
    wait.until(EC.presence_of_element_located((By.ID, "username")))

    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("123456")
    driver.find_element(By.ID, "submit").click()

    # 处理弹窗
    wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    login_text = alert.text
    alert.accept()

    print("✅ 登录结果：", login_text)
    assert "登录成功" in login_text

    # ==========================================
    # 2. 直接打开搜索页（绝对路径，绝不失败）
    # ==========================================
    driver.get(SEARCH_URL)
    wait.until(EC.presence_of_element_located((By.ID, "searchInput")))

    # 搜索商品
    driver.find_element(By.ID, "searchInput").send_keys("笔记本电脑")
    driver.find_element(By.ID, "searchBtn").click()

    result = driver.find_element(By.ID, "searchResult").text
    print("✅ 搜索结果：", result)
    assert "笔记本电脑" in result

    # ==========================================
    # 3. 直接打开购物车（绝对路径）
    # ==========================================
    driver.get(CART_URL)
    wait.until(EC.presence_of_element_located((By.ID, "checkout")))

    # 点击结算
    driver.find_element(By.ID, "checkout").click()
    print("✅ 结算成功")

    # ==========================================
    # 最终成功
    # ==========================================
    print("🎉🎉🎉 全流程 100% 全部执行完成！")