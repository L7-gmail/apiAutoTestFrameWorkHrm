import os.path
from datetime import datetime

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from config import setting
from config.setting import WAIT_TIMEOUT, FILE_PATH
from util_tools.ConfigParser import ConfigParser
from util_tools.log_util.RecordLog import logs

import pytesseract
from PIL import Image


class BasePageMethod:

    def __init__(self, driver):
        self.__driver = driver
        self.__wait = WebDriverWait(self.__driver, WAIT_TIMEOUT)

    """
    窗口最大化
    仍然有：标题栏 / 地址栏 / 任务栏
    属于 OS 层面的窗口操作
    """

    def window_max(self):
        self.__driver.maximize_window()

    """
    真全屏（类似按 F11）
    没有地址栏 / 标签栏 / 任务栏
    属于浏览器层面的全屏
    """

    def window_fullscreen(self):
        self.__driver.fullscreen_window()

    # 打开url
    def open_url(self, url):
        if url.startswith("http") or url.startswith("https"):
            self.__driver.get(url)
        else:
            new_url = ConfigParser(FILE_PATH.get("config_ini")).get_host() + url
            self.__driver.get(new_url)

    # 关闭浏览器窗口
    def close_browser_window(self):
        self.__driver.close()

    # 关闭浏览器
    def quit_browser(self):
        self.__driver.quit()

    def refresh_browser(self):
        self.__driver.refresh()

    def location_element(self, locator: tuple[str, str]):
        """
        定位元素
        :param locator: 元素定位逻辑
        :return: 返回定位到的元素对象
        """
        try:
            elememt = self.__wait.until(ec.presence_of_element_located(locator))
            logs.info(f"成功找到元素：{locator}")
            return elememt
        except TimeoutException as e:
            logs.error(f"元素{locator}无法定位到：{str(e)}")
            raise
        except Exception as e:
            logs.error(f"定位元素{locator}，发生异常：{str(e)}")
            raise

    def location_elements(self, locator: tuple[str, str]):
        """
        定位一组元素
        :param locator: 元素定位逻辑
        :return: 返回定位到的元素对象列表
        """
        try:
            elements = self.__wait.until(ec.presence_of_all_elements_located(locator))
            logs.info(f"找到元素列表：{elements}, 定位逻辑：{locator}")
            return elements
        except TimeoutException as e:
            logs.error(f"元素无法定位到：{str(e)}")
            raise
        except Exception as e:
            logs.error(f"定位元素，发生异常：{str(e)}")
            raise

    def click_by_js(self, locator: tuple[str, str], force=False):
        """
        用js方式的方式点击元素
        :param locator: 要点击的元素定位逻辑
        :param force: 是否强制点击元素（无视前端限制）
        :return:
        """
        try:
            element = self.location_element(locator)
            if not force:
                self.__driver.execute_script('arguments[0].click()', element)
            else:
                self.__driver.execute_script("arguments[0].click({force:true})", element)
            logs.info(f"元素成功被点击：{locator}")
        except TimeoutException as e:
            logs.error(f"元素无法定位到：{str(e)}")
            raise
        except Exception as e:
            logs.error(f"点击元素发生异常：{str(e)}")
            raise

    def click(self, locator: tuple[str, str]):
        """
        普通方式点击
        :param locator: 要点击的元素定位逻辑
        :return:
        """
        try:
            element = self.location_element(locator)
            element.click()
            logs.info(f"元素成功被点击：{locator}")
        except TimeoutException as e:
            logs.error(f"元素无法定位到：{str(e)}")
            raise
        except Exception as e:
            logs.error(f"点击元素发生异常：{str(e)}")
            raise

    def send_keys(self, locator: tuple[str, str], value):
        """
        普通方式输入内容
        :param locator: 元素定位逻辑
        :param value: 要输入的内容
        :return:
        """
        try:
            element = self.location_element(locator)
            element.send_keys(value)
            logs.info(f"元素{locator}成功被输入内容:{value}")
        except TimeoutException as e:
            logs.error(f"元素无法定位到：{str(e)}")
            raise
        except Exception as e:
            logs.error(f"元素输入内容，发生异常：{str(e)}")
            raise

    def click_to_send_keys(self, locator: tuple[str, str], value):
        """
        鼠标点击定位到元素，逐步输入内容
        :param locator: 元素定位逻辑
        :param value: 要输入的内容
        :return:
        """
        try:
            element = self.location_element(locator)
            ActionChains(self.__driver).move_to_element(element).click().send_keys(value).perform()
            logs.info(f"元素{locator}成功被输入内容:{value}")
        except TimeoutException as e:
            logs.error(f"元素无法定位到：{str(e)}")
            raise
        except Exception as e:
            logs.error(f"元素输入内容，发生异常：{str(e)}")
            raise

    def enter(self):
        """
        按下回车健
        :return:
        """
        try:
            ActionChains(self.__driver).send_keys(Keys.ENTER).perform()
            logs.info("按下回车键")
        except Exception as e:
            logs.error(f"按下回车键，发送异常：{str(e)}")
            raise

    def right_click(self, locator: tuple[str, str]):
        """
        右键点击
        :param locator: 元素定位逻辑
        :return:
        """
        try:
            element = self.location_element(locator)
            ActionChains(self.__driver).context_click(element).perform()
            logs.info("右键点击")
        except Exception as e:
            logs.error(f"右键点击，发送异常：{str(e)}")
            raise

    def double_click(self, locator: tuple[str, str]):
        """
        右键点击
        :param locator: 元素定位逻辑
        :return:
        """
        try:
            element = self.location_element(locator)
            ActionChains(self.__driver).double_click(element).perform()
            logs.info("双击")
        except Exception as e:
            logs.error(f"双击，发送异常：{str(e)}")
            raise

    def mouse_move_to_element(self, locator: tuple[str, str]):
        """
        鼠标悬浮到对应元素
        :param locator: 元素定位逻辑
        :return:
        """
        try:
            element = self.location_element(locator)
            ActionChains(self.__driver).move_to_element(element).perform()
            logs.info(f"鼠标悬浮到元素：{locator}")
        except Exception as e:
            logs.error(f"鼠标悬浮到对应元素，发送异常：{str(e)}")
            raise

    def scroll_to_bottom(self):
        """
        滚动页面到底部
        :return:
        """
        try:
            self.__driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            logs.info("滚动页面到底部")
        except Exception as e:
            logs.error(f"滚动页面到底部，发送异常：{str(e)}")
            raise

    def screenshot_as_file(self, imgName):
        """
        截图并存在screenshots目录下
        :param imgName: 文件名
        :return:
        """
        try:
            current_date = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = imgName + '-' + current_date + '.png'
            filepath = os.path.join(FILE_PATH.get("screenshot"), filename)
            self.__driver.get_screenshot_as_file(filepath)
            logs.info("截图并存在screenshots目录下")
        except Exception as e:
            logs.error(f"截图，发送异常：{str(e)}")
            raise

    def get_screen_png(self):
        """
        截图，文件为png, 返回截图的二进制数据（bytes）
        :param self:
        :return:  返回截图的二进制数据（bytes）
        """
        return self.__driver.get_screenshot_as_png()

    def clear_input_text(self, locator: tuple[str, str]):
        """
        清空输入框
        :param locator: 元素定位逻辑
        :return:
        """
        try:
            element = self.location_element(locator)
            element.clear()
            logs.info(f"清空输入框:{locator}")
        except TimeoutException as e:
            logs.error(f"元素无法定位到：{str(e)}")
            raise
        except Exception as e:
            logs.error(f"元素清楚输入文本，发生异常：{str(e)}")
            raise

    def ocr_captcha(self, locator: tuple[str, str]):
        """
        识别图形验证码，不一定准确
        1）定位到图形验证码，保存图片
        2）调用Image去打开图像
        3）调用pytesseract模块进行OCR识别
        :param locator: 定位方法和定位表达式，（tuple）元组
        :return:
        """
        captcha_element = self.location_element(locator)
        # 截取图形验证码
        captcha_path = setting.FILE_PATH['screenshot'] + '/captcha.png'
        captcha_element.screenshot(captcha_path)
        # 调用Image去打开图像
        captcha_image = Image.open(captcha_path)
        try:
            # 调用pytesseract进行OCR识别
            captcha_text = pytesseract.image_to_string(captcha_image)
            logs.info(f'识别到的验证码为：{captcha_text}')
            return captcha_text
        except pytesseract.pytesseract.TesseractNotFoundError:
            logs.error("找不到tesseract,这是因为pytesseract模块依赖于TesseractOCR引擎来进行图像识别！")

    def select_dropdown_by_index(self, locator: tuple[str, str], select_index):
        """
        根据索引选择下拉框值
        :param locator: 下拉框定位逻辑
        :param select_index: 要选择的下拉框选项对应的索引
        :return:
        """
        try:
            element = self.location_element(locator)
            select = Select(element)
            select.select_by_index(select_index)
            logs.info(f"根据索引 {select_index} 选择下拉框 {locator} 选项")
        except Exception as e:
            logs.error(f"根据索引选择下拉框，发生异常：{str(e)}")
            raise

    def select_dropdown_by_content(self, locator: tuple[str, str], content):
        """
        根据索引选择下拉框值
        :param locator: 下拉框定位逻辑
        :param content: 要选择的下拉框选项对应的内容
        :return:
        """
        try:
            element = self.location_element(locator)
            select = Select(element)
            select.select_by_visible_text(content)
            logs.info(f"根据选项内容 {content} 选择下拉框 {locator} 选项")
        except Exception as e:
            logs.error(f"根据选项内容选择下拉框，发生异常：{str(e)}")
            raise

    @property
    def get_current_url(self):
        """
        获取当前url
        :return: 当前url
        """
        return self.__driver.current_url

    @property
    def get_current_title(self):
        """
        获取当前窗口标题
        :return: 当前窗口标题
        """
        return self.__driver.title

    def get_tag_text(self, locator: tuple[str, str]):
        """
        获取标签文本
        :param locator: 标签元素定位逻辑
        :return: 便签文本
        """
        try:
            element = self.location_element(locator)
            text = element.text
            logs.info(f"获取标签 {locator} 文本: {text}")
            return text
        except Exception as e:
            logs.error(f"获取标签文本，发生异常：{str(e)}")
            raise

    def get_tag_attribute(self,locator: tuple[str, str],attribute):
        """
            获取元素属性值
            :param locator: 元素定位逻辑
            :param attribute: 属性名
            :return: 属性值
            """
        try:
            element = self.location_element(locator)
            value = element.get_attribute(attribute)
            logs.info(f"获取元素 {locator}的{attribute}属性值: {value}")
            return value
        except Exception as e:
            logs.error(f"获取元素 {locator}的{attribute}属性值，发生异常：{str(e)}")
            raise

    def switch_to_frame(self, element):
        """
        切到页面里某个frame中
        :param element: frame元素对象
        :return:
        """
        try:
            self.__driver.switch_to.frame(element)
            logs.info(f"切到页面frame中: {element}")
        except Exception as e:
            logs.error(f"切到页面frame中，发生异常：{str(e)}")
            raise

    def exit_frame(self):
        """
        关闭frame，切回原页面中
        :return:
        """
        try:
            self.__driver.switch_to.default_content()
            logs.info(f"关闭frame，切回原页面中")
        except Exception as e:
            logs.error(f"关闭frame，切回原页面中，发生异常：{str(e)}")
            raise

    @property
    def alert(self):
        """
        获取js原生提示（对话）框
        :return:
        """
        try:
            alert = self.__wait.until(ec.alert_is_present())
            logs.info("获取js原生提示（对话）框")
            return alert
        except Exception as e:
            logs.error(f"获取js原生提示（对话）框，发生异常：{str(e)}")
            raise

    def alert_confirm(self):
        """
        点击确认对话框
        :return:
        """
        try:
            self.alert.accept()
            logs.info("点击确认对话框")
        except Exception as e:
            logs.error(f"点击确认对话框，发生异常：{str(e)}")
            raise

    def alert_cancel(self):
        """
        点击取消对话框
        :return:
        """
        try:
            self.alert.dismiss()
            logs.info("点击取消对话框")
        except Exception as e:
            logs.error(f"点击取消对话框，发生异常：{str(e)}")
            raise

    def get_alert_text(self):
        """
        获取js原生对话框的文本
        :return:
        """
        try:
            text = self.alert.text
            logs.info(f" 获取js原生对话框的文本:{text}")
            return text
        except Exception as e:
            logs.error(f" 获取js原生对话框的文本，发生异常：{str(e)}")
            raise

    def switch_to_new_tab(self):
        """
        切换到新窗口
        :return:
        """
        try:
            original_window = self.__driver.window_handles[0]
            all_window = self.__driver.window_handles
            new_window = None
            for window in all_window:
                if window != original_window:
                    new_window = window
                    break
            if new_window:
                self.__driver.switch_to.window(new_window)
                logs.info("成功切换到新窗口")
        except TimeoutException as e:
            logs.error(f"等待新标签窗口打开超时：{str(e)}")
        except NoSuchElementException as e:
            logs.error(f"未找到新标签页句柄：{str(e)}")
        except Exception as e:
            logs.error(f"切到新窗口，发生异常：{str(e)}")
            raise

    def switch_to_tab_by_index(self, index):
        """
        根据索引切换窗口（从0开始）
        :param index: 窗口句柄索引
        :return:
        """
        try:
            window_handles = self.__driver.window_handles
            if 0 <= index < len(window_handles):
                self.__driver.switch_to.window(window_handles[index])
                logs.info(f"切换第{index + 1}个窗口")
        except Exception as e:
            logs.error(f"根据索引切窗口，发生异常：{str(e)}")
            raise

    def element_is_present(self, locator: tuple[str, str]):
        """
        判断元素是否存在
        :param locator: 元素定位逻辑
        :return: 元素存在返回True,否则返回False
        """
        try:
            self.__wait.until(ec.presence_of_element_located(locator))
            logs.info(f"判断元素{locator}存在")
            return True
        except Exception as e:
            logs.info(f"判断元素{locator}不存在")
            return False

    def alert_is_present(self):
        """
        判断js提示框是否存在
        :return: 存在返回True,否则返回False
        """
        try:
            self.__wait.until(ec.alert_is_present())
            logs.info(f"js提示框存在")
            return True
        except Exception as e:
            logs.info(f"js提示框不存在")
            return False

    def assert_element_text(self, locator: tuple[str, str], expect):
        """
        判断元素文本是否跟预期相等
        :param locator: 元素定位逻辑
        :param expect: 预期文本
        :return: 相等返回True, 找不到元素或者不相等返回False
        """
        try:
            text = self.get_tag_text(locator)
            if text == expect:
                logs.info(f"元素文本 '{text}' 与预期文本 '{expect}' 相等")
                return True
            else:
                logs.info(f"元素文本 '{text}' 与预期文本 '{expect}' 不相等")
                return False
        except Exception as e:
            return False

    def get_cookies(self):
        """
        获取浏览器cookies
        :return: 浏览器cookies
        """
        try:
            logs.info("获取浏览器cookies")
            return self.__driver.get_cookies()
        except Exception as e:
            logs.info("获取浏览器cookies失败")
            raise

    def add_cookies(self,cookies):
        """
        给浏览器添加cookies
        :param cookies: 浏览器cookies
        :return:
        """
        try:
            for cookie in cookies:
                self.__driver.add_cookie(cookie)
            logs.info(f"给浏览器添加cookies:{cookies}")
        except Exception as e:
            logs.info(f"添加浏览器cookies失败:str{e}")
            raise
