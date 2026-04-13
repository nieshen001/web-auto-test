# run.py
import pytest
import os
import sys
import requests
import json
from config.settings import REPORT_PATH, RERUNS, RERUNS_DELAY
from utils.config_utils import load_yaml_config  # 需要创建这个工具函数

def send_dingtalk_message(webhook, content):
    """发送钉钉消息"""
    if not webhook or webhook == "":
        print("未配置钉钉webhook，跳过通知")
        return
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {"content": content}
    }
    try:
        response = requests.post(webhook, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print("钉钉通知发送成功")
        else:
            print(f"钉钉通知发送失败: {response.text}")
    except Exception as e:
        print(f"钉钉通知发送异常: {e}")

if __name__ == '__main__':
    allure_results_dir = os.path.join(REPORT_PATH, "allure-results")
    os.makedirs(allure_results_dir, exist_ok=True)

    # 运行测试并捕获退出码
    exit_code = pytest.main([
        "-v",
        f"--reruns={RERUNS}",
        f"--reruns-delay={RERUNS_DELAY}",
        f"--alluredir={allure_results_dir}",
        "-n auto",
        "test_cases/"
    ])

    # 统计测试结果（通过解析 pytest 的退出码或输出文件）
    # 这里简化：根据退出码判断整体状态
    if exit_code == 0:
        result_summary = "✅ 测试全部通过"
    else:
        result_summary = "❌ 测试存在失败"

    # 读取钉钉 webhook 配置
    config = load_yaml_config()
    webhook = config.get("dingtalk_webhook", "")

    # 组装通知内容
    message = f"【Web自动化测试报告】\n{result_summary}\n重试次数: {RERUNS}\n并发数: auto\n报告路径: {allure_results_dir}"
    send_dingtalk_message(webhook, message)

    sys.exit(exit_code)