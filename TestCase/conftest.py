import sys
from pathlib import Path
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# 添加项目根目录到Python路径（绝对路径）
sys.path.append(str(Path(__file__).resolve().parent.parent))
# from Base.base_page import BasePage
from PageObject.page_login import LoginPage
from Base.config import USERNAME, PASSWORD
import datetime

# 调用统一的日志配置
from Base.config import CHROME_DRIVER_PATH
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
    logging.info(f"Test case {item.name} started at {start_time}")
    yield

# 在pytest_runtest_teardown钩子中  
def pytest_runtest_teardown(item):
    """记录测试用例结束时间"""
    end_time = datetime.datetime.now()
    logging.info(f"Test case {item.name} ended at {end_time}")
    # 这里可以添加更多的清理逻辑

# 新增失败截图功能：
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 实现失败时自动截图并记录错误日志
    # 截图保存路径：TestCase/screenshots/
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('logged_in')
        if driver:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshots_dir = Path(__file__).parent / 'screenshots'
            screenshots_dir.mkdir(exist_ok=True)
            file_path = screenshots_dir / f'failure_{item.name}_{timestamp}.png'
            driver.save_screenshot(str(file_path))
            logging.error(f'测试失败截图已保存至：{file_path}')