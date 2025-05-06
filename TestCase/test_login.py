import time
from PageObject.page_login import LoginPage

def test_login_success(logged_in):
    """测试成功登录场景"""
    driver = logged_in
    assert LoginPage(driver).is_login_success(), "登录成功后应跳转到仪表盘页面"


def test_login_failure():
    """测试失败登录场景"""
    # 这里可以添加具体的失败测试逻辑
    assert True