from time import sleep

import allure
from selenium.webdriver.common.by import By

from util_tools.BasePageMethod import BasePageMethod


class RegisterPage(BasePageMethod):
    username_loc = (By.ID, 'username')
    email_loc = (By.ID, 'email')
    password1_loc = (By.ID, 'password1')
    confirm_password_loc = (By.ID, 'conform_password')
    MSN_loc = (By.NAME, 'extend_field1')
    QQ_loc = (By.NAME, 'extend_field2')
    work_phone_loc = (By.NAME, 'extend_field3')
    family_phone_loc = (By.NAME, 'extend_field4')
    phone_loc = (By.NAME, 'extend_field5')
    sel_question_loc = (By.NAME, 'sel_question')
    passwd_answer_loc = (By.NAME, 'passwd_answer')
    agreement_loc = (By.NAME, 'agreement')
    Submit_loc = (By.NAME, 'Submit')
    username_notice = (By.ID,'username_notice')
    email_notice = (By.ID,'email_notice')
    password_notice = (By.ID,'password_notice')
    conform_password_notice = (By.ID,'conform_password_notice')
    assert_nickname = (By.XPATH, '//*[@id="ECS_MEMBERZONE"]/font/font')

    go_to_login_link = (By.LINK_TEXT,'我已有账号，我要登录')

    # 输入注册信息
    def register_input(self, username, email, password1, confirm_password, msn, qq, work_phone, family_phone, phone,
                 sel_question, passwd_answer, agreement):
        self.open_url("http://localhost/ecshop/user.php?act=register")
        allure.attach(self.get_current_url, '打开注册页面', attachment_type=allure.attachment_type.TEXT)
        self.click_to_send_keys(self.username_loc,username)
        self.click_to_send_keys(self.email_loc,email)
        self.send_keys(self.password1_loc,password1)
        self.send_keys(self.confirm_password_loc,confirm_password)
        self.send_keys(self.MSN_loc,msn)
        self.send_keys(self.QQ_loc,qq)
        self.send_keys(self.work_phone_loc,work_phone)
        self.send_keys(self.family_phone_loc,family_phone)
        self.send_keys(self.phone_loc,phone)
        if sel_question:
            self.select_dropdown_by_content(self.sel_question_loc,sel_question)
        self.send_keys(self.passwd_answer_loc,passwd_answer)
        agreement_element = self.location_element(self.agreement_loc)
        if agreement_element.is_selected() is False and agreement is True:
            agreement_element.click()
        elif agreement_element.is_selected() is True and agreement is False:
            agreement_element.click()
        allure.attach(self.get_screen_png(), '输入注册信息后截图', attachment_type=allure.attachment_type.PNG)
        sleep(2)

    # 点击注册
    def click_to_register(self, is_screenshot=False):
        self.click(self.Submit_loc)
        sleep(1)
        if is_screenshot:
            allure.attach(self.get_screen_png(), '点击注册按钮后截图', attachment_type=allure.attachment_type.PNG)
        else:
            allure.attach('点击立即注册按钮', '点击注册', attachment_type=allure.attachment_type.TEXT)

    # 跳转到登录页面
    def go_to_login_page(self):
        self.open_url("http://localhost/ecshop/user.php?act=register")
        allure.attach(self.get_current_url, '打开注册页面', attachment_type=allure.attachment_type.TEXT)
        self.click(self.go_to_login_link)
        allure.attach(self.get_screen_png(), "点击'我已有帐号，我要登录'的链接后截图", attachment_type=allure.attachment_type.PNG)

    # 断言注册信息有问题的提示信息
    def assert_register_notice(self, notice):
        # 断言提示框旁边的提示信息
        assert notice.get("username_notice") in self.get_tag_text(self.username_notice)
        assert notice.get("email_notice") in self.get_tag_text(self.email_notice)
        assert notice.get("password1") in self.get_tag_text(self.password_notice)
        assert notice.get("conform_password") in self.get_tag_text(self.conform_password_notice)
        self.click_to_register()
        # 断言提示框里的提示信息
        sleep(1)
        if self.alert_is_present():
            sleep(1)
            assert notice.get("alert") in self.get_alert_text()


