import pytest
import requests
import logging
from utils.logger import setup_logging
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pages.login_page import LoginPage
from config.config import USERNAME, PASSWORD, PTUSER_USERNAME, PTUSER_PASSWORD, GETMENU
import datetime

# 调用统一的日志配置
logger = setup_logging()

from config.config import CHROME_DRIVER_PATH
# 记录使用的 ChromeDriver 路径
logging.info(f"使用的 ChromeDriver 路径: {CHROME_DRIVER_PATH}")

"""
测试账号登录，返回登录后的驱动实例
:return: 登录后的浏览器驱动实例
"""
@pytest.fixture(scope="function")
def logged_in():
    # 创建 Chrome 浏览器服务实例
    service = Service(str(CHROME_DRIVER_PATH))
    # 创建 Chrome 浏览器驱动实例
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    # 创建登录页面实例
    login_page = LoginPage(driver)
    # 使用测试账号进行登录
    result = login_page.login(USERNAME, PASSWORD)
    # 检查登录是否成功，若失败则终止测试
    if not result:
        pytest.fail("登录失败")
    yield driver  # 返回登录后的浏览器驱动实例

    # 关闭浏览器
    logging.info("关闭浏览器")
    driver.quit()



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    """记录测试用例开始时间"""
    start_time = datetime.datetime.now()
    logger.info(f"Test case {item.name} started at {start_time}")
    outcome = yield
    # 这里可以添加更多的清理逻辑

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item):
    """记录测试用例结束时间"""
    outcome = yield
    end_time = datetime.datetime.now()
    logger.info(f"Test case {item.name} ended at {end_time}")
    # 这里可以添加更多的清理逻辑