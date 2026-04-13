# test_cases/test_login.py
import allure
import pytest
from page_objects.login_page import LoginPage


@allure.feature("登录功能")
class TestLogin:

    @allure.story("用户登录数据驱动")
    @allure.title("登录测试 - 用户: {username}")
    @pytest.mark.parametrize("username,password,expected", [
        ("standard_user", "secret_sauce", "inventory.html"),
        ("locked_out_user", "secret_sauce", "locked out"),
        ("standard_user", "wrong_password", "Username and password do not match"),
    ])
    def test_login(self, driver, username, password, expected):
        login_page = LoginPage(driver)
        login_page.login(username, password)

        if "inventory.html" in expected:
            assert expected in driver.current_url
        else:
            error_text = login_page.get_error_message()
            assert expected in error_text