from time import sleep

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from config.setting import WAIT_TIMEOUT, BROWSER_TYPE
from pageObject.login.LoginPage import LoginPage
from pageObject.purchase_flow.CartPage import CartPage
from pageObject.purchase_flow.SettlePage import SettlePage
from util_tools.InitDriver import init_driver
from util_tools.ConnectMysql import ConnectMysql
from util_tools.log_util.RecordLog import logs
from util_tools.operate_data.OperateYaml import operate_yaml

service = None
driver = None


@pytest.fixture
def not_login_driver(request):
    params = getattr(request, "param", {})
    incognito = params.get("incognito", False)
    global driver
    driver = init_driver(incognito=incognito)
    yield driver
    sleep(2)
    driver.quit()


@pytest.fixture
def login_driver(request):
    # 从 request.param 获取参数
    params = getattr(request, "param", {})
    username = params.get("username", "admin456")
    password = params.get("password", "123456")
    incognito = params.get("incognito", False)

    global driver
    driver = init_driver(incognito=incognito)
    driver.get("http://localhost/ecshop/user.php")
    login_page = LoginPage(driver)
    login_page.login(username, password)
    sleep(2)
    yield driver
    driver.quit()


# 前置条件：需要加个商品到购物车
def add_to_cart(driver_, good_name="纸巾-test", good_number=2):
    cart_page = CartPage(driver_)
    cart_page.clear_cart()
    cart_page.add_to_cart(good_name, good_number=good_number)


# 前置条件：需要加个商品到购物车，然后到结算页面
def go_to_settle_page(driver_, good_name="纸巾-test", good_number=2):
    add_to_cart(driver_, good_name, good_number)
    settle_page = SettlePage(driver_)
    address_info = operate_yaml("address_info.yaml")[0]
    settle_page.click_to_settle_page(*address_info, open_cart_url=False)


# 钩子函数,对失败测试用例进行截图
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport():
    global driver
    coucome = yield
    result = coucome.get_result()
    if result.when == 'call':
        xfail = hasattr(result, 'wasxfail')
        if (result.skipped and xfail) or (result.failed and not xfail):
            with allure.step('测试用例失败截图'):
                allure.attach(driver.get_screenshot_as_png(), '失败截图', attachment_type=allure.attachment_type.PNG)
