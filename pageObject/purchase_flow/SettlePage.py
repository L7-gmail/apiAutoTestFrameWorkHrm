from time import sleep

import allure
from selenium.webdriver.common.by import By

from util_tools.BasePageMethod import BasePageMethod


class SettlePage(BasePageMethod):
    # 去计算中心的元素定位
    cart_url = "/flow.php"
    settle_button = (By.XPATH, "//img[@alt='checkout']")  # 结算中心按钮
    country_select_loc = (By.ID, 'selCountries_0')
    province_select_loc = (By.ID, 'selProvinces_0')
    city_select_loc = (By.ID, 'selCities_0')
    district_select_loc = (By.ID, 'selDistricts_0')
    deliver_loc = (By.NAME, "consignee")
    email_loc = (By.NAME, 'email')
    address_loc = (By.NAME, 'address')
    zipcode_loc = (By.NAME, 'zipcode')
    tel_loc = (By.NAME, 'tel')
    mobile_loc = (By.NAME, 'mobile')
    address_submit_buttons_loc = (By.NAME, 'Submit')
    # 配送方式元素定位
    shipping_radio = (By.NAME, 'shipping')
    # 支付方式元素定位
    payment_radio = (By.NAME, 'payment')
    order_submit = (By.XPATH, '//*[@id="theForm"]/div[15]/div[2]/input[1]')
    # 下单定位元素
    assert_order_success = (By.XPATH,'/html/body/div[7]/div/h6')
    assert_order_fail = (By.XPATH,'/html/body/div[6]/div/div/div/div/p[1]')

    @staticmethod
    def deliver_type_loc(value):
        """
        指定配送方式定位元素
        :param value: 配送方式对应的value
        :return: 返回对应定位逻辑
        """
        return By.XPATH, f"//input[@name='shipping' and @value={value}]"

    @staticmethod
    def pay_type_loc(value):
        """
        指定支付方式定位元素
        :param value: 支付方式对应的value
        :return:返回对应定位逻辑
        """
        return By.XPATH, f"//input[@name='payment' and @value={value}]"

    @staticmethod
    def pack_type_loc(value):
        """
        指定包装方式定位元素
        :param value: 包装方式对应的value
        :return:返回对应定位逻辑
        """
        return By.XPATH, f"//input[@name='pack' and @value={value}]"

    @staticmethod
    def card_type_loc(value):
        """
        指定贺卡方式定位元素
        :param value: 贺卡方式对应的value
        :return: 返回对应定位逻辑
        """
        return By.XPATH, f"//input[@name='card' and @value={value}]"

    def input_address_info(self, country, province, city, district, deliver, email, address, zipcode, tel, mobile):
        self.select_dropdown_by_content(self.country_select_loc, country)
        sleep(1)
        self.select_dropdown_by_content(self.province_select_loc, province)
        sleep(1)
        self.select_dropdown_by_content(self.city_select_loc, city)
        sleep(1)
        self.select_dropdown_by_content(self.district_select_loc, district)
        sleep(1)
        self.send_keys(self.deliver_loc, deliver)
        self.clear_input_text(self.email_loc)
        self.send_keys(self.email_loc, email)
        self.send_keys(self.address_loc, address)
        self.send_keys(self.zipcode_loc, zipcode)
        self.send_keys(self.tel_loc, tel)
        self.send_keys(self.mobile_loc, mobile)
        allure.attach(self.get_screen_png(), '输入地址信息', attachment_type=allure.attachment_type.PNG)

    # 点击结算中心按钮
    def click_to_settle_page(self, country, province, city, district, deliver, email, address, zipcode, tel, mobile,
                             open_cart_url=True):
        if open_cart_url:
            self.open_url(self.cart_url)
            allure.attach(self.get_current_url, '打开购物车页面', attachment_type=allure.attachment_type.TEXT)
        sleep(1)
        self.click(self.settle_button)
        sleep(1)
        allure.attach(self.get_screen_png(), '点击结算中心按钮后', attachment_type=allure.attachment_type.PNG)
        if self.element_is_present(self.country_select_loc):
            deliver_input_elements = self.location_elements(self.deliver_loc)
            address_submit_buttons_elements = self.location_elements(self.address_submit_buttons_loc)
            if deliver_input_elements[0].get_attribute('value') == '':
                self.input_address_info(country, province, city, district, deliver, email, address, zipcode, tel,
                                        mobile)
                address_submit_buttons_elements[0].click()
                allure.attach(self.get_screen_png(), '点击选择第一个地址配送后', attachment_type=allure.attachment_type.PNG)
            elif len(address_submit_buttons_elements) > 1 and deliver_input_elements[1].get_attribute('value') != '':
                address_submit_buttons_elements[1].click()
                allure.attach(self.get_screen_png(), '点击选择第二个地址配送后', attachment_type=allure.attachment_type.PNG)
            else:
                address_submit_buttons_elements[0].click()
                allure.attach(self.get_screen_png(), '点击选择第一个地址配送后', attachment_type=allure.attachment_type.PNG)
        sleep(2)

    # 不选择配送方式进行下单
    def order_when_unselect_delivery_type(self):
        is_select_delivery_type = False
        shipping_radio_elements = self.location_elements(self.shipping_radio)
        for elem in shipping_radio_elements:
            if elem.is_selected():
                is_select_delivery_type = True
                break
        if not is_select_delivery_type:
            self.click(self.order_submit)
            sleep(1)
            allure.attach("出现提示没有选择配送方式提示框", '点击提交订单后', attachment_type=allure.attachment_type.TEXT)

    # 下单
    def order(self, deliver_type_value, pay_type_value, pack_type_value, card_type_value):
        self.click(self.deliver_type_loc(deliver_type_value))
        allure.attach(self.get_screen_png(), '点击选择配送方式', attachment_type=allure.attachment_type.PNG)
        self.click(self.pay_type_loc(pay_type_value))
        allure.attach(self.get_screen_png(), '点击选择支付方式', attachment_type=allure.attachment_type.PNG)
        self.click(self.pack_type_loc(pack_type_value))
        allure.attach(self.get_screen_png(), '点击选择包装方式', attachment_type=allure.attachment_type.PNG)
        self.click(self.card_type_loc(card_type_value))
        allure.attach(self.get_screen_png(), '点击选择贺卡', attachment_type=allure.attachment_type.PNG)
        sleep(2)
        self.click(self.order_submit)
        sleep(2)
        allure.attach(self.get_screen_png(), '点击下单后', attachment_type=allure.attachment_type.PNG)

    # 不选择支付方式进行下单
    def order_when_unselect_pay_type(self):
        is_select_pay_type = False
        self.click(self.shipping_radio)
        payment_radio_elements = self.location_elements(self.payment_radio)
        for element in payment_radio_elements:
            if element.is_selected():
                is_select_pay_type = True
        if not is_select_pay_type:
            self.click(self.order_submit)
            sleep(1)
            allure.attach("出现提示没有选择支付方式的提示框", '点击下单后', attachment_type=allure.attachment_type.TEXT)

    # 断言不选择配送方式或支付方式进行下单
    def assert_order_when_unselect_delivery_or_order_type(self, expect_alert_text):
        alert_text = self.get_alert_text()
        assert expect_alert_text in alert_text
        self.alert_confirm()
        assert self.get_current_url == "http://localhost/ecshop/flow.php?step=checkout"
