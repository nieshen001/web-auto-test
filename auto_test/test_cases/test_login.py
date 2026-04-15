# test_cases/test_login.py
import allure
import pytest
from selenium.webdriver.common.by import By
from page_objects.login_page import LoginPage


@allure.feature("登录功能")
class TestLogin:

    # ==================== 数据驱动测试（原有3个场景） ====================
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

    # ==================== 新增独立测试用例 ====================
    @allure.story("用户登录异常场景")
    @allure.title("用户名为空登录失败")
    def test_login_empty_username(self, driver):
        login_page = LoginPage(driver)
        login_page.login("", "secret_sauce")
        error = login_page.get_error_message()
        assert "Username is required" in error

    @allure.story("用户登录异常场景")
    @allure.title("密码为空登录失败")
    def test_login_empty_password(self, driver):
        login_page = LoginPage(driver)
        login_page.login("standard_user", "")
        error = login_page.get_error_message()
        assert "Password is required" in error

    @allure.story("商品浏览")
    @allure.title("商品列表加载成功")
    def test_product_list_load(self, driver):
        login_page = LoginPage(driver)
        login_page.login("standard_user", "secret_sauce")
        # 验证商品列表容器存在
        inventory_container = driver.find_element(By.CLASS_NAME, "inventory_list")
        assert inventory_container.is_displayed()
        # 验证商品数量大于0
        products = driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(products) > 0

    @allure.story("购物车操作")
    @allure.title("添加商品到购物车")
    def test_add_to_cart(self, driver):
        login_page = LoginPage(driver)
        login_page.login("standard_user", "secret_sauce")
        # 点击第一个商品的“Add to cart”按钮
        add_button = driver.find_element(By.CLASS_NAME, "btn_inventory")
        add_button.click()
        # 验证购物车徽章显示1
        cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert cart_badge.text == "1"

    @allure.story("购物车操作")
    @allure.title("从购物车移除商品")
    def test_remove_from_cart(self, driver):
        login_page = LoginPage(driver)
        login_page.login("standard_user", "secret_sauce")
        # 添加商品
        add_button = driver.find_element(By.CLASS_NAME, "btn_inventory")
        add_button.click()
        # 进入购物车页面
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        # 点击移除按钮
        remove_button = driver.find_element(By.CLASS_NAME, "cart_button")
        remove_button.click()
        # 验证购物车为空
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == 0