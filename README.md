# 企业级 Web 自动化测试框架
基于 Selenium + Pytest + Allure + PO 模式实现的 Web 自动化实战项目，包含完整业务流程（登录、搜索、购物车、结算），可直接用于学习与公司项目落地。

## 技术栈
- Python 3.10+
- Selenium 4
- Pytest
- Allure 测试报告
- PO 设计模式
- 日志管理、失败自动截图

## 项目结构
test_auto_web_pro/

├── common/ # 公共工具类：驱动、基类、日志

├── config/ # 全局配置

├── page_object/ # PO 模式页面层

├── test_case/ # 测试用例

├── report/ # Allure 报告

├── screenshot/ # 失败截图

├── logs/ # 运行日志

├── run.py # 启动入口

└── pytest.ini # Pytest 配置

## 快速开始
```
1. 安装依赖
pip install -r requirements.txt
2. 运行测试用例
python run.py
3. 生成 Allure 报告
allure serve report/allure-results
实现功能
✅ 登录功能自动化
✅ 商品搜索流程
✅ 购物车 & 结算
✅ PO 模式解耦
✅ 失败自动截图
✅ 日志统一管理
✅ Allure 可视化报告
适用场景
自动化测试学习
企业 Web 项目自动化落地
简历项目经验
运行环境
Python 3.10+
Selenium 4
Pytest
Allure
浏览器：Chrome
测试环境：Windows 11
测试数据
账号：admin
密码：123456
测试数据存放在 config/test_data.py 文件中，可自行添加。
测试数据格式如下：
test_data = {}
test_data['login']['username'] = 'admin'
test_data['login']['password'] = 'admin'
测试用例存放在 test_case 目录下，可自行添加。
测试用例格式如下：
@pytest.mark.parametrize('data', test_data['login'])
def test_login(data):
    LoginPage().login(data['username'], data['password'])
测试用例执行顺序：
pytest -s -v test_case/test_login.py
测试报告生成位置：
report/allure-results
测试报告查看：
allure serve report/allure-results
```
