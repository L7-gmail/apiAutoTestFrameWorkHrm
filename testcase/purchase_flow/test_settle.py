from time import sleep

import allure
import pytest

from pageObject.login.LoginPage import LoginPage
from pageObject.purchase_flow.CartPage import CartPage
from pageObject.purchase_flow.SettlePage import SettlePage
from testcase.conftest import add_to_cart, go_to_settle_page
from util_tools.operate_data.OperateJson import operate_json
from util_tools.operate_data.OperateYaml import operate_yaml


@allure.feature("结算模块")
class TestSettle:

    # 测试去结算中心页面
    @allure.story("点击进入结算中心页面")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("desc,username,password", operate_json("different_settle_user.json",is_remove_desc=False))
    @pytest.mark.parametrize("country, province, city, district, deliver, email, address, zipcode, tel, mobile",
                             operate_yaml("address_info.yaml"))
    @pytest.mark.parametrize("not_login_driver", [{"incognito": True}], indirect=True)
    def test_go_to_settle_page(self, not_login_driver, username, password, country, province,
                               city, district, deliver, email, address, zipcode, tel, mobile,desc):
        allure.dynamic.title(desc+"点击进入结算页面")
        allure.dynamic.description(desc+"点击进入结算页面")
        self.login_page = LoginPage(not_login_driver)
        self.login_page.login(username, password)
        sleep(1)
        add_to_cart(not_login_driver)
        self.settle_page = SettlePage(not_login_driver)
        self.settle_page.click_to_settle_page(country, province, city, district, deliver, email, address, zipcode, tel,
                                              mobile, open_cart_url=False)
        # 断言
        assert self.settle_page.get_current_url == 'http://localhost/ecshop/flow.php?step=checkout'

    # 测试下单成功
    @allure.story("下单成功")
    @allure.title("下单成功")
    @allure.description("下单成功")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("login_driver", [{"incognito": True}], indirect=True)
    @pytest.mark.parametrize("settle_info", operate_yaml("settle_info.yaml"))
    def test_order_success(self, login_driver, settle_info):
        go_to_settle_page(login_driver)
        self.settle_page = SettlePage(login_driver)
        self.settle_page.order(*settle_info)
        # 断言
        assert "感谢您在本店购物！您的订单已提交成功，请记住您的订单号:" in self.settle_page.get_tag_text(
            self.settle_page.assert_order_success)

    # 测试下单失败
    @allure.story("下单失败")
    @allure.title("下单失败")
    @allure.description("下单失败")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("login_driver", [{"username": "admin123", "password": "123456", "incognito": True}],
                             indirect=True)
    @pytest.mark.parametrize("settle_info", operate_yaml("settle_info.yaml"))
    def test_order_fail(self, login_driver, settle_info):
        go_to_settle_page(login_driver)
        self.settle_page = SettlePage(login_driver)
        self.settle_page.order(*settle_info)
        # 断言
        assert "您的余额不足以支付整个订单，请选择其他支付方式" in self.settle_page.get_tag_text(
            self.settle_page.assert_order_fail)

    # 测试不选择发货方式，点击下单
    @allure.story("不选择发货方式")
    @allure.title("不选择发货方式")
    @allure.description("不选择发货方式，点击下单")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("login_driver", [{"username": "test01", "password": "123456", "incognito": True}],
                             indirect=True)
    def test_order_when_unselect_delivery_type(self, login_driver):
        go_to_settle_page(login_driver)
        self.settle_page = SettlePage(login_driver)
        self.settle_page.order_when_unselect_delivery_type()
        # 断言
        self.settle_page.assert_order_when_unselect_delivery_or_order_type("您必须选定一个配送方式")

    # 测试不选择支付方式，点击下单
    @allure.story("不选择支付方式")
    @allure.title("不选择支付方式")
    @allure.description("不选择支付方式，点击下单")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("login_driver", [{"username": "test01", "password": "123456", "incognito": True}],
                             indirect=True)
    def test_order_when_unselect_pay_type(self, login_driver):
        go_to_settle_page(login_driver)
        self.settle_page = SettlePage(login_driver)
        self.settle_page.order_when_unselect_pay_type()
        # 断言
        self.settle_page.assert_order_when_unselect_delivery_or_order_type("您必须选定一个支付方式")
