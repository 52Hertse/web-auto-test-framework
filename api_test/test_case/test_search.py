import allure
import pytest
import yaml

from api_test.api.search_api import SearchApi

# 加载数据驱动文件
with open("../data/search_data.yml","r",encoding="utf-8") as f:
    search_data = yaml.safe_load(f)["search"]

@allure.feature("搜索业务")
class TestSearch:
    @allure.story("搜索接口数据驱动测试")
    @pytest.mark.parametrize("data",search_data)
    def test_search(self, data):
        keyword=data["keyword"]
        expect=data["expect"]
        # 1.调用接口
        res = SearchApi().search(keyword)
        result=res.json()

        # 2.接口层断言
        assert res.status_code == 200
        assert result["code"]==0

        # 3.数据层断言
        if expect == "存在商品":
            assert len(result["data"]["list"]) > 0
        else:
            assert len(result["data"]["list"]) == 0
