import allure
import pytest

from pageObject.purchase_flow.CartPage import CartPage


@allure.feature("购物车模块")
class TestCart:

    # 测试库存不足加入购物车
    # 给前置方法login_driver传参
    @allure.story("加入购物车")
    @allure.title("库存不足加入购物车")
    @allure.description("库存不足加入购物车")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("login_driver", [{"incognito": True}], indirect=True)
    @pytest.mark.parametrize("good_name,good_number", [("纸巾-test", 11)])
    def test_add_to_cart_when_insufficient_stock(self, login_driver, good_name, good_number):
        self.cart_page = CartPage(login_driver)
        self.cart_page.add_to_cart(good_name, good_number=good_number)
        # 断言
        if self.cart_page.alert_is_present():
            assert "对不起，该商品已经库存不足暂停销售" in self.cart_page.get_alert_text()
            self.cart_page.alert_cancel()
        assert "http://localhost/ecshop/goods.php?id=" in self.cart_page.get_current_url

    # 测试库存充足加入购物车
    @allure.story("加入购物车")
    @allure.title("库存充足加入购物车")
    @allure.description("库存充足加入购物车")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("login_driver", [{"incognito": True}], indirect=True)
    @pytest.mark.parametrize("good_name,good_number", [("纸巾-test", 10)])
    def test_add_to_cart_when_sufficient_stock(self, login_driver, good_name, good_number):
        self.cart_page = CartPage(login_driver)
        self.cart_page.add_to_cart(good_name, good_number=good_number)
        # 断言
        assert self.cart_page.get_current_url == "http://localhost/ecshop/flow.php?step=cart"
        assert self.cart_page.assert_good_in_cart("纸巾-test")

    # 测试清空购物车
    @allure.story("清空购物车")
    @allure.title("清空购物车")
    @allure.description("清空购物车")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("login_driver", [{"incognito": True}],
                             indirect=True)
    @pytest.mark.parametrize("good_name,good_number", [("纸巾-test", 2)])
    def test_clear_cart(self, login_driver, good_name, good_number):
        self.cart_page = CartPage(login_driver)
        self.cart_page.add_to_cart(good_name, good_number=good_number)
        self.cart_page.clear_cart(open_cart_url=False)
        # 断言
        self.cart_page.assert_clear_cart()

    # 测试购物车删除商品
    @allure.story("购物车删除商品")
    @allure.title("购物车删除商品")
    @allure.description("购物车删除商品")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("login_driver", [{"incognito": True}],
                             indirect=True)
    @pytest.mark.parametrize('confirm_remove,good_name,good_number', [(True, "纸巾-test", 5), (False, "纸巾-test", 5)])
    def test_remove_goods(self, login_driver, confirm_remove, good_name, good_number):
        self.cart_page = CartPage(login_driver)
        self.cart_page.add_to_cart(good_name, good_number=good_number)
        self.cart_page.remove_goods(is_remove=confirm_remove)
        if confirm_remove:
            assert self.cart_page.assert_good_in_cart(good_name) is False
        else:
            assert self.cart_page.assert_good_in_cart(good_name)

    # 测试放入收藏夹
    @allure.story("购物车中将商品放入收藏夹")
    @allure.title("购物车中将商品放入收藏夹")
    @allure.description("购物车中将商品放入收藏夹")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("login_driver", [{"incognito": True}],
                             indirect=True)
    @pytest.mark.parametrize('confirm_remove,good_name,good_number', [(False, "纸巾-test", 2), (True, "纸巾-test", 2)])
    def test_move_to_favourite(self, login_driver, confirm_remove, good_name, good_number):
        self.cart_page = CartPage(login_driver)
        self.cart_page.clear_cart()
        self.cart_page.add_to_cart(good_name, good_number=good_number, open_index_url=False)
        self.cart_page.move_to_favourite(is_remove=confirm_remove)
        if confirm_remove:
            assert self.cart_page.assert_good_in_cart(good_name) is False
            assert self.cart_page.assert_good_in_favourite(good_name)
        else:
            assert self.cart_page.assert_good_in_cart(good_name) is True
            assert self.cart_page.assert_good_in_favourite(good_name) is False

    # 测试更新购物车(库存充足跟不充足的清空)
    @allure.story("更新购物车")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("login_driver", [{"incognito": True}], indirect=True)
    @pytest.mark.parametrize('desc,good_name,good_number,update_good_number,expect_prompt',
                             [("更新商品数量不超过库存","纸巾-test", 2, 5, "购物车更新成功"),
                              ("更新商品数量超过库存","纸巾-test", 2, 11, "非常抱歉，您选择的商品")])
    def test_update_cart(self, login_driver,desc,good_name, good_number, update_good_number,
                         expect_prompt):
        allure.dynamic.title(desc)
        allure.dynamic.description(desc)
        self.cart_page = CartPage(login_driver)
        self.cart_page.clear_cart()
        self.cart_page.add_to_cart(good_name, good_number=good_number, open_index_url=False)
        self.cart_page.update_cart(update_good_number, open_cart_url=False)
        # 断言
        self.cart_page.assert_update_cart(expect_prompt, update_good_number)

    # 测试从购物车点击进入商品详情页
    @allure.story("进入商品详情页")
    @allure.title("进入商品详情页")
    @allure.description("从购物车点击进入商品详情页")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("login_driver", [{"incognito": True}],
                             indirect=True)
    @pytest.mark.parametrize('good_name,good_number', [("纸巾-test", 2)])
    def test_click_to_good_detail_page(self,login_driver,good_name,good_number):
        self.cart_page = CartPage(login_driver)
        self.cart_page.clear_cart()
        self.cart_page.add_to_cart(good_name, good_number=good_number, open_index_url=False)
        self.cart_page.click_to_good_detail_page(good_name,open_cart_url=False)
        assert "http://localhost/ecshop/goods.php?id" in self.cart_page.get_current_url

    # 测试点击继续购物按钮
    @allure.story("点击继续购物")
    @allure.title("点击继续购物")
    @allure.description("从购物车点击继续购物按钮")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("login_driver", [{"incognito": True}],
                             indirect=True)
    @pytest.mark.parametrize('good_name,good_number', [("纸巾-test", 2)])
    def test_click_continue_to_shop(self,login_driver, good_name,good_number):
        self.cart_page = CartPage(login_driver)
        self.cart_page.clear_cart()
        self.cart_page.add_to_cart(good_name, good_number=good_number, open_index_url=False)
        self.cart_page.click_continue_to_shop(open_cart_url=False)
        assert "http://localhost/ecshop/" in self.cart_page.get_current_url



