# 基础页面类
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self,driver):
        self.driver = driver

    # 等待元素可见
    def wait_for_element_visible(self, loc, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(loc)
        )

    # 元素定位
    def locator(self,*loc):
        return self.wait_for_element_visible(loc)

    # 输入
    def input(self,loc,text):
        self.locator(*loc).send_keys(text)

    # 点击
    def click(self,loc):
        self.locator(*loc).click()

    # 清除
    def clear(self,loc):
        self.locator(*loc).clear()

    # 获取文本
    def get_text(self,loc):
        return self.locator(*loc).text

    # 获取属性
    def get_attribute(self,loc,attribute):
        return self.locator(*loc).get_attribute(attribute)

    
    def save_element_screenshot(self, locator, file_path):
        """通用元素截图方法"""
        element = self.locator(*locator)
        element.screenshot(file_path)