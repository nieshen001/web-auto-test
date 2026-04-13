# page_objects/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.log_utils import LogUtils
import os
from config.settings import REPORT_PATH

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.log = LogUtils.get_logger()

    def find_element(self, locator, timeout=10):
        """查找单个元素，locator格式为 (By.ID, "username")"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            self.log.error(f"元素 {locator} 在 {timeout} 秒内未找到")
            self.take_screenshot("find_element_error.png")
            raise

    def click(self, locator, timeout=10):
        """点击元素"""
        element = self.find_element(locator, timeout)
        element.click()
        self.log.info(f"点击元素 {locator}")

    def input_text(self, locator, text, timeout=10):
        """输入文本"""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
        self.log.info(f"向元素 {locator} 输入文本：{text}")

    def get_title(self):
        """获取页面标题"""
        return self.driver.title

    def take_screenshot(self, file_name):
        """截图保存到reports目录"""
        screenshot_path = os.path.join(REPORT_PATH, file_name)
        self.driver.save_screenshot(screenshot_path)
        self.log.info(f"截图已保存：{screenshot_path}")