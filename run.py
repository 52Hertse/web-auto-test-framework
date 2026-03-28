import pytest
import os
import subprocess
# 执行用例
if __name__ == '__main__':
    # 1. 执行pytest用例（自动读取pytest.ini的配置）
    pytest.main()
    # 2.执行完自动启动Allure报告（不用手动输指令）
    # 检查report文件是否还存在
    if os.path.exists("./report"):
        # 启动Allure报告（Windows/Mac/Linux通用）
        subprocess.call("allure serve ./report", shell=True)
    else:
        print("报告文件夹不存在，请检查用例是否执行成功！")