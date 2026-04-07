from time import sleep

import allure
import pytest

from pageObject.register.RegisterPage import RegisterPage
from util_tools.operate_data.OperateJson import operate_json


@allure.feature("注册模块")
class TestRegister:

    @allure.story("用户注册")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("注册成功")
    @allure.description("注册成功")
    @pytest.mark.parametrize("data", operate_json("register_success.json"))
    def test_register_success(self, not_login_driver, data):
        allure.dynamic.parameter("data", data, mode=allure.parameter_mode.HIDDEN)
        data = tuple(data[0].values())
        self.register_page = RegisterPage(not_login_driver)
        self.register_page.register_input(*data)
        assert '可以注册' in self.register_page.get_tag_text(self.register_page.username_notice)
        assert '可以注册' in self.register_page.get_tag_text(self.register_page.email_notice)
        assert '可以注册' in self.register_page.get_tag_text(self.register_page.password_notice)
        assert '可以注册' in self.register_page.get_tag_text(self.register_page.conform_password_notice)
        self.register_page.click_to_register(is_screenshot=True)
        assert self.register_page.assert_element_text(self.register_page.assert_nickname, data[0])

    @allure.story("用户注册")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("desc,data,notice", operate_json("register_fail.json", is_remove_desc=False))
    def test_register_fail(self, not_login_driver, data, notice, desc):
        allure.dynamic.parameter("data", data, mode=allure.parameter_mode.HIDDEN)
        allure.dynamic.title(desc.split(",")[0])  # 给测试报告设置用例名
        allure.dynamic.description(desc)  # 测试报告设置用例描述
        data = tuple(data.values())
        self.register_page = RegisterPage(not_login_driver)
        self.register_page.register_input(*data)
        # 断言
        self.register_page.assert_register_notice(notice)
        assert self.register_page.element_is_present(self.register_page.assert_nickname) is False

    @allure.story("用户注册")
    @allure.title("点击跳转到登录页面")
    @allure.description("点击‘我已有账号，我要登录’链接跳转到登录页面")
    @allure.severity(allure.severity_level.NORMAL)
    def test_go_to_login_page(self,not_login_driver):
        self.register_page = RegisterPage(not_login_driver)
        self.register_page.go_to_login_page()
        assert self.register_page.get_current_url == "http://localhost/ecshop/user.php?act=login"
