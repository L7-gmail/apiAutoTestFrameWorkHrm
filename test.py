from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# service = Service(r"D:/install/python/chromedriver.exe")
# driver = webdriver.Chrome(service=service)
# driver.maximize_window()
# driver.get("https://vibee.com/")
# driver.implicitly_wait(10)
#
# sleep(10)
# header_element = driver.find_element(By.XPATH,'//*[@id="__next"]/header/div/div')
# action = ActionChains(driver)
# action.move_to_element(header_element)
# sign_in_button_element = driver.find_element(By.XPATH,'//*[@id="__next"]/header/div/div/div[2]/div/button')
# sign_in_button_element.click()
# username_element = driver.find_element(By.XPATH,'//*[@id="registrationForm"]/div[1]/div/div/input')
# password_element = driver.find_element(By.XPATH,'//*[@id="registrationForm"]/div[2]/div/div/input')
# username_element.send_keys()
# password_element.send_keys()
# sleep(2)
# submit_element = driver.find_element(By.XPATH,'//*[@id="registrationForm"]/button')
# submit_element.click()
# sleep(10)
# driver.quit()

# result = []
# ls = [1,2,5,4,3,3,1,5,3]
# for i in range(len(ls)):
#     if ls[i] in ls[i+1:]:
#         result.append(ls[i])
# print(result)

# result = []
# ls = [1,2,5,4,3,3,1,5,3]
# for i in range(len(ls)):
#     if ls[i] not in result:
#         result.append(ls[i])
# print(result)

