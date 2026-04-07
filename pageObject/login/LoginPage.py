from time import sleep

import allure
import pytest
from selenium.webdriver.common.by import By
from util_tools.BasePageMethod import BasePageMethod
from util_tools.InitDriver import init_driver


class LoginPage(BasePageMethod):

    url = '/user.php'
    username_loc = (By.NAME,'username')
    password_loc = (By.NAME,'password')
    submit = (By.NAME,'submit')
    assert_nickname = (By.XPATH,'//*[@id="ECS_MEMBERZONE"]/font/font')
    remember_loc = (By.ID,'remember')

    # 密码问题找回密码测试的定位元素
    find_password_link_loc = (By.LINK_TEXT,'密码问题找回密码')
    find_password_input_username = (By.NAME,'user_name')
    username_submit = (By.NAME,'submit')
    passwd_answer = (By.NAME,'passwd_answer')
    passwd_answer_submit = (By.NAME, 'submit')
    new_password_loc = (By.NAME,'new_password')
    confirm_new_password_loc = (By.NAME,'confirm_password')
    new_password_submit_button = (By.NAME,'submit')
    assert_result_text = (By.XPATH,"//div[@class='boxCenterList RelaArticle']/div/p")

    def login(self,username,password):
        self.open_url(self.url)
        allure.attach(self.get_current_url, '打开登录页面', attachment_type=allure.attachment_type.TEXT)
        self.send_keys(self.username_loc,username)
        self.send_keys(self.password_loc,password)
        allure.attach(self.get_screen_png(), '输入用户名和密码截图', attachment_type=allure.attachment_type.PNG)
        self.click(self.submit)
        sleep(1)
        allure.attach(self.get_screen_png(), '点击登录按钮后截图', attachment_type=allure.attachment_type.PNG)

    # 找回密码
    def find_password(self,username,passwd_answer,new_passwd=None,confirm_new_password=None):
        self.open_url(self.url)
        allure.attach(self.get_current_url, '打开登录页面', attachment_type=allure.attachment_type.TEXT)
        self.click(self.find_password_link_loc)
        self.send_keys(self.find_password_input_username,username)
        allure.attach(self.get_screen_png(), '点击找回密码链接后，输入用户名截图', attachment_type=allure.attachment_type.PNG)
        self.click(self.username_submit)
        self.send_keys(self.passwd_answer,passwd_answer)
        allure.attach(self.get_screen_png(), '上一步点击提交用户名后，输入密码提示问题后截图', attachment_type=allure.attachment_type.PNG)
        self.click(self.passwd_answer_submit)
        allure.attach(self.get_screen_png(), '提交密码提示问题后截图', attachment_type=allure.attachment_type.PNG)
        if new_passwd:
            self.send_keys(self.new_password_loc,new_passwd)
            self.send_keys(self.confirm_new_password_loc,confirm_new_password)
            allure.attach(self.get_screen_png(), '输入新密码与确认新密码后截图', attachment_type=allure.attachment_type.PNG)
            self.click(self.new_password_submit_button)
            allure.attach(self.get_screen_png(), '点击提交新密码后截图', attachment_type=allure.attachment_type.PNG)





