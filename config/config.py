import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 多环境切换
ENV = "test"  # test / pre / prod
ENV_MAP = {
    "test": "file:///" + os.path.join(BASE_DIR, "login.html"),
    "pre": "https://pre.xxx.com",
    "prod": "https://xxx.com"
}
BASE_URL = ENV_MAP[ENV]

# 浏览器
BROWSER = "chrome"
HEADLESS = False  # 服务器运行改为 True
IMPLICIT_WAIT = 10
TIMEOUT = 15

# 报告&截图
REPORT_DIR = os.path.join(BASE_DIR, "report")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshot")
LOG_DIR = os.path.join(BASE_DIR, "logs")