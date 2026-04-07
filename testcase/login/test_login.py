from time import sleep

import allure
import pytest

from pageObject.login.LoginPage import LoginPage
from util_tools.InitDriver import init_driver
from util_tools.operate_data.OperateJson import operate_json


@allure.feature("登录模块")
class TestLogin:

    # 测试登录输入账号密码
    @allure.story("用户登录")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("desc,login_data,nickname_after_login",
                             operate_json("login.json", is_remove_desc=False),
                             ids=None)
    def test_login01(self, not_login_driver, login_data, nickname_after_login,desc):
        allure.dynamic.title(desc)  # 给测试报告添加用例标题
        allure.dynamic.description(desc)  # 给测试报告添加用例描述
        self.login_page = LoginPage(not_login_driver)
        self.login_page.login(**login_data)
        # 登录成功用例：断言登录后的nickname是否跟预期一致；登录失败用例：断言不存在登录后的nickname的元素，即没登录成功
        if nickname_after_login:
            assert self.login_page.assert_element_text(self.login_page.assert_nickname, nickname_after_login)
        else:
            assert self.login_page.element_is_present(self.login_page.assert_nickname) is False

    @allure.story("密码问题找回密码成功")
    @allure.title("密码问题找回密码成功")
    @allure.description("用户通过正确回答密码提示问题，成功重置密码")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_find_password_by_passwd_answer_success(self, not_login_driver, username='l777', passwd_answer='广州', new_passwd='456456',
                                   confirm_new_password='456456'):
        self.login_page = LoginPage(not_login_driver)
        self.login_page.find_password(username, passwd_answer, new_passwd, confirm_new_password)
        assert "您的新密码已设置成功" in self.login_page.get_tag_text(self.login_page.assert_result_text)
        sleep(3)
        self.login_page.login(username,new_passwd)
        assert self.login_page.assert_element_text(self.login_page.assert_nickname, username)

    @allure.story("密码问题找回密码失败")
    @allure.title("密码问题找回密码失败")
    @allure.description("用户通过错误回答密码提示问题，导致找回密码失败")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_find_password_by_passwd_answer_fail(self, not_login_driver, username='l777', passwd_answer='上海'):
        self.login_page = LoginPage(not_login_driver)
        self.login_page.find_password(username, passwd_answer)
        assert "您输入的密码答案是错误的" in self.login_page.get_tag_text(self.login_page.assert_result_text)
        sleep(3)
        assert self.login_page.get_current_url == 'http://localhost/ecshop/user.php?act=qpassword_name'
