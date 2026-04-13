# conftest.py
import pytest
import allure
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.settings import BASE_URL, IMPLICITLY_WAIT
from utils.log_utils import LogUtils

logger = LogUtils.get_logger()

@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-logging')
    _driver = webdriver.Chrome(options=chrome_options)
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
            with open(screenshot_path, "rb") as f:
                allure.attach(f.read(), name=f"{item.name} 失败截图", attachment_type=allure.attachment_type.PNG)