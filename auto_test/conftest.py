# conftest.py
import pytest
import allure
import os
from selenium import webdriver
from config.settings import BASE_URL, IMPLICITLY_WAIT
from utils.log_utils import LogUtils

logger = LogUtils.get_logger()

@pytest.fixture(scope="function")
def driver():
    """每个测试用例独立启动一个浏览器实例，Selenium 自动管理 ChromeDriver"""
    _driver = webdriver.Chrome()  # 自动下载匹配的驱动
    _driver.implicitly_wait(IMPLICITLY_WAIT)
    _driver.maximize_window()
    _driver.get(BASE_URL)
    yield _driver
    _driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """在测试失败时自动截图并附加到 Allure 报告"""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get('driver', None)
        if driver:
            screenshot_dir = "reports/screenshots"
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}_failed.png")
            driver.save_screenshot(screenshot_path)
            logger.error(f"测试失败，截图保存至：{screenshot_path}")

            # 附加到 Allure 报告
            with open(screenshot_path, "rb") as f:
                allure.attach(f.read(), name=f"{item.name} 失败截图", attachment_type=allure.attachment_type.PNG)