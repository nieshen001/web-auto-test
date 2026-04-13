# conftest.py
import pytest
import os
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from config.settings import BASE_URL, IMPLICITLY_WAIT
from utils.log_utils import LogUtils

logger = LogUtils.get_logger()

@pytest.fixture(scope="function")
def driver():
    """每个测试用例独立启动一个浏览器实例"""
    # 如果手动下载了 chromedriver.exe 并放在项目根目录，可以取消下面的注释并指定路径
    # service = Service(r"D:\py\auto_test\chromedriver.exe")
    # _driver = webdriver.Chrome(service=service)
    _driver = webdriver.Chrome()  # 让 Selenium Manager 自动管理驱动
    _driver.implicitly_wait(IMPLICITLY_WAIT)
    _driver.maximize_window()
    _driver.get(BASE_URL)
    yield _driver
    _driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
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

            # 将截图附加到 Allure 报告
            with open(screenshot_path, "rb") as f:
                allure.attach(f.read(), name=f"{item.name} 失败截图", attachment_type=allure.attachment_type.PNG)