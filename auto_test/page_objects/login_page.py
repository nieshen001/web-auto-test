# page_objects/login_page.py
from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage

class LoginPage(BasePage):
    # 页面元素定位（使用元组形式）
    username_input = (By.ID, "user-name")
    password_input = (By.ID, "password")
    login_button = (By.ID, "login-button")
    error_message = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self, url):
        """打开登录页面"""
        self.driver.get(url)
        self.log.info(f"打开页面：{url}")

    def login(self, username, password):
        """执行登录操作"""
        self.input_text(self.username_input, username)
        self.input_text(self.password_input, password)
        self.click(self.login_button)
        self.log.info(f"尝试登录，用户名：{username}，密码：{password}")

    def get_error_message(self):
        """获取错误提示信息"""
        return self.find_element(self.error_message).text