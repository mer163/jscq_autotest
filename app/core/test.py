# !/usr/bin/env python
# coding=utf-8

import selenium.webdriver.remote.webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep

driver = selenium.webdriver.remote.webdriver.WebDriver(command_executor="http://129.28.65.165:4444/wd/hub",
                                                       desired_capabilities=DesiredCapabilities.CHROME)
driver.get("http://www.baidu.com")
driver.find_element_by_id("kw").send_keys("python")
driver.find_element_by_id("su").click()
sleep(2)
