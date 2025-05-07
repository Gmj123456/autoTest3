import pytest
import time
from PageObject.page_login import LoginPage

def test_login_success(logged_in):
    """测试成功登录场景"""
    driver = logged_in
    assert LoginPage(driver).is_login_success(), "登录成功后应跳转到仪表盘页面"


# 完善失败测试场景：
@pytest.mark.parametrize('username, password', [
    ('', 'correct_pass'),  # 空用户名
    ('wrong_user', ''),     # 空密码
    ('wrong', 'wrong')     # 错误组合
])
def test_login_failure_with_invalid_credentials(logged_in, username, password):
    login_page.login(username, password)
    assert login_page.is_login_failure(), f"{username}/{password} 应触发登录失败弹窗"

@pytest.mark.parametrize('username, password', [
    ('valid_user', 'valid_pass'),
    ('admin', 'admin123')
])
def test_login_success_with_valid_credentials(logged_in, username, password):
    login_page.login(username, password)
    assert login_page.is_login_success(), f"{username}/{password} 应登录成功"