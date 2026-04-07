from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOption
from selenium.webdriver.edge.options import Options as edgeOption
from selenium.webdriver.firefox.options import Options as firefoxOption
from selenium.webdriver.chrome.service import Service
from config.setting import BROWSER_TYPE, WAIT_TIMEOUT, HEADLESS


def init_driver(incognito=False):
    service = Service(r"D:/install/python/chromedriver.exe")
    browser_mapping = {
        "Chrome": webdriver.Chrome,
        "Edge": webdriver.Edge,
        "Firefox": webdriver.Firefox
    }
    options_browser_mapping = {
        "Chrome": chromeOption,
        "Edge": edgeOption,
        "Firefox": firefoxOption
    }
    options = None
    if incognito or HEADLESS:
        options = options_browser_mapping.get(BROWSER_TYPE.capitalize())()
    if incognito:
        # 使用无痕模式，防止出现密码保存提示
        options.add_argument("--incognito")
    if HEADLESS:
        # 使用无头模式
        options.add_argument('--headless')

    driver = browser_mapping.get(BROWSER_TYPE.capitalize())(
        service=service if BROWSER_TYPE.capitalize() == 'Chrome' else None, options=options)
    driver.maximize_window()
    driver.implicitly_wait(WAIT_TIMEOUT)
    return driver
