from selenium import webdriver
import time

# 启动 Chrome 浏览器
driver = webdriver.Chrome()
driver.get("https://www.baidu.com")
time.sleep(2)          # 停留2秒，便于观察
print("页面标题：", driver.title)
driver.quit()