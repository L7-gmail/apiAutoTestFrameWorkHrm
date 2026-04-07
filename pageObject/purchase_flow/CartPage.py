from time import sleep

import allure
from selenium.webdriver.common.by import By

from util_tools.BasePageMethod import BasePageMethod


class CartPage(BasePageMethod):
    index_url = 'http://localhost/ecshop/index.php'
    cart_url = "http://localhost/ecshop/flow.php"
    # 加入购物车定位元素
    keyword_loc = (By.ID, 'keyword')
    search_button = (By.NAME, 'imageField')
    good_number_loc = (By.ID, 'number')
    add_to_cart_button = (By.XPATH, '//*[@id="ECS_FORMBUY"]/ul/li[7]/a[1]/img')

    @staticmethod
    def good_title_loc(good_name: str) -> tuple[str, str]:
        return By.XPATH, f"//p/a[text()='{good_name}']"

    # 清空购物车定位元素
    clear_cart_button = (By.XPATH, "//input[@value='清空购物车']")
    select_cart_button = (By.XPATH, "//a[@title='查看购物车']")
    assert_is_have_good = (By.XPATH, '//*[@id="formCart"]/table[1]/tbody/tr[2]/td[1]/a[2]')
    # 购物车移除商品定位元素
    remove_button = (By.LINK_TEXT, '删除')
    # 放入收藏夹定位元素
    move_to_favourite_button = (By.LINK_TEXT, '放入收藏夹')
    user_center_button = (By.LINK_TEXT, '用户中心')
    my_favourite_button = (By.PARTIAL_LINK_TEXT, '我的收藏')
    # 更新购物车元素
    cart_frame = (By.ID,"formCart")
    update_number_loc = (By.XPATH, "//input[contains(@id,'goods_number_')]")
    update_cart_button = (By.XPATH, "//input[@value='更新购物车']")
    update_prompt = (By.XPATH, "/html/body/div[6]/div/div/div/div/p[1]")
    back_to_cart_button = (By.PARTIAL_LINK_TEXT, '返回')
    # 继续购物按钮
    continue_to_shop_button = (By.XPATH,"//img[@alt='continue']")

    @staticmethod
    def good_link_in_cart(good_name: str) -> tuple[str, str]:
        return By.XPATH, f"//*[@id='formCart']//a[text()='{good_name}']"

    @staticmethod
    def good_link_on_favourite_in_cart_page(good_name: str) -> tuple[str, str]:
        return By.XPATH, f"//div[3]/table/tbody/tr/td[1]/a[text()='{good_name}']"

    # 搜索商品，将商品加入购物车
    def add_to_cart(self, good_name, good_number=1, open_index_url=True):
        if open_index_url:
            self.open_url(self.index_url)
            allure.attach(self.get_current_url, '打开主页面', attachment_type=allure.attachment_type.TEXT)
        self.send_keys(self.keyword_loc, good_name)
        allure.attach(self.get_screen_png(), '搜索商品输入框输入商品名称', attachment_type=allure.attachment_type.PNG)
        sleep(1)
        self.click(self.search_button)
        sleep(1)
        allure.attach(self.get_screen_png(), '点击搜索按钮后', attachment_type=allure.attachment_type.PNG)
        self.click(self.good_title_loc(good_name))
        sleep(1)
        allure.attach(self.get_screen_png(), '点击商品名称进入商品详情页', attachment_type=allure.attachment_type.PNG)
        self.double_click(self.good_number_loc)
        sleep(1)
        self.send_keys(self.good_number_loc, good_number)
        sleep(1)
        allure.attach(self.get_screen_png(), '输入商品数量', attachment_type=allure.attachment_type.PNG)
        self.click(self.add_to_cart_button)
        sleep(1)
        if self.alert_is_present():
            allure.attach("出现提示框", '点击加入购物车后', attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach(self.get_screen_png(), '点击加入购物车后', attachment_type=allure.attachment_type.PNG)

    # 清空购物车
    def clear_cart(self, open_cart_url=True):
        if open_cart_url:
            self.open_url(self.cart_url)
            allure.attach(self.get_current_url, '打开购物车页面', attachment_type=allure.attachment_type.TEXT)
        sleep(1)
        self.click(self.clear_cart_button)
        sleep(1)
        allure.attach(self.get_screen_png(), '点击清空购物车后', attachment_type=allure.attachment_type.PNG)

    # 在购物车移除商品
    def remove_goods(self, is_remove=True):
        self.click(self.remove_button)
        allure.attach("出现确认是否删除商品提示框", '点击删除商品', attachment_type=allure.attachment_type.TEXT)
        if is_remove:
            self.alert_confirm()
            allure.attach(self.get_screen_png(), '点击确认移除商品后', attachment_type=allure.attachment_type.PNG)
        else:
            self.alert_cancel()
            allure.attach(self.get_screen_png(), '点击取消移除商品后', attachment_type=allure.attachment_type.PNG)

    # 在购物车将商品移到收藏夹
    def move_to_favourite(self, is_remove=True):
        self.click(self.move_to_favourite_button)
        sleep(1)
        allure.attach("出现是否加入收藏夹提示", '点击加入收藏', attachment_type=allure.attachment_type.TEXT)
        if is_remove:
            self.alert_confirm()
            sleep(2)
            allure.attach(self.get_screen_png(), '点击确认加入收藏后', attachment_type=allure.attachment_type.PNG)
        else:
            self.alert_cancel()
            sleep(2)
            allure.attach(self.get_screen_png(), '点击取消加入收藏后', attachment_type=allure.attachment_type.PNG)

    # 更新购物车
    def update_cart(self, update_good_number=1, open_cart_url=True):
        if open_cart_url:
            self.open_url(self.cart_url)
            allure.attach(self.get_current_url, '打开购物车页面', attachment_type=allure.attachment_type.TEXT)
        self.double_click(self.update_number_loc)
        self.send_keys(self.update_number_loc, update_good_number)
        sleep(1)
        allure.attach(self.get_screen_png(), '更改商品数量', attachment_type=allure.attachment_type.PNG)
        self.click(self.update_cart_button)
        allure.attach(self.get_screen_png(), '点击更新购物车后', attachment_type=allure.attachment_type.PNG)

    # 点击商品名字连接进入到商品详情页
    def click_to_good_detail_page(self,good_name,open_cart_url=True):
        if open_cart_url:
            self.open_url(self.cart_url)
            allure.attach(self.get_current_url, '打开购物车页面', attachment_type=allure.attachment_type.TEXT)
        self.click(self.good_link_in_cart(good_name))
        sleep(1)
        self.switch_to_new_tab()
        allure.attach(self.get_screen_png(), '点击商品名称链接后', attachment_type=allure.attachment_type.PNG)

    # 点击继续购物按钮
    def click_continue_to_shop(self,open_cart_url=True):
        if open_cart_url:
            self.open_url(self.cart_url)
            allure.attach(self.get_current_url, '打开购物车页面', attachment_type=allure.attachment_type.TEXT)
        self.click(self.continue_to_shop_button)
        allure.attach(self.get_screen_png(), '点击继续购物后', attachment_type=allure.attachment_type.PNG)

    # 断言购物车更新
    def assert_update_cart(self, expect_prompt, update_good_number):
        assert expect_prompt in self.get_tag_text(self.update_prompt)
        self.click(self.back_to_cart_button)
        sleep(1)
        assert self.get_tag_attribute(self.update_number_loc, "value") == str(update_good_number)

    # 断言产品是否在购物车
    def assert_good_in_cart(self, good_name: str):
        return self.element_is_present(self.good_link_in_cart(good_name))

    # 断言产品是否被加入收藏夹
    def assert_good_in_favourite(self, good_name: str):
        return self.element_is_present(self.good_link_on_favourite_in_cart_page(good_name))

    # 断言是否清空了购物车
    def assert_clear_cart(self):
        assert self.get_tag_text(self.select_cart_button) == '您的购物车中有 0 件商品，总计金额 ￥0.00元。'
        self.click(self.select_cart_button)
        assert self.element_is_present(self.assert_is_have_good) is False



