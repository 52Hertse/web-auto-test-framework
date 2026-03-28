import pymysql
import requests

from api_test.common.base_api import BaseApi
from page_object import search_page

class SearchApi(BaseApi):
    # 接口：搜索商品
    def search(self,keyword):
        url = "http://你的企业地址/api/search"
        # 构造请求
        data = {
            "keyword": keyword,
            "page": 1,
            "size": 10
        }
        return self.send("POST", url, json=data)

    # # 连接数据库
    # def test_search_db(self):
    #     # 1.连接数据库
    #     db = pymysql.connect(host="192.168.56.10",
    #                          port=3306, user="root",
    #                          password="123456",
    #                          database="api_test")
    #     cursor = db.cursor()
    #     # 2.执行SQL，查数据库真实数据
    #     cursor.execute("select * from user where username='admin'")
    #     db_data = cursor.fetchall()
    #
    #     # 3.断言：数据库有数据= 接口返回正确
    #     assert len(db_data) > 0
    #
    # # 测试：ui层
    # def test_search_ui(self):
    #     # 1.输入关键词
    #     search_page.input_keyword("笔记本电脑")
    #     # 2.点击搜索
    #     search_page.click_search()
    #     # 3.获取搜索结果
    #     result = search_page.get_result()
    #     # 4.断言页面结果
    #     assert "笔记本电脑" in result
