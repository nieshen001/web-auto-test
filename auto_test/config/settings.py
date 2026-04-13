# config/settings.py
import os

# 项目根目录路径（因为本文件在 config/ 下，所以向上两级得到根目录）
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 读取 YAML 配置文件的函数（直接写在 settings.py 中，避免循环导入）
import yaml
def _load_yaml_config():
    yaml_path = os.path.join(BASE_PATH, 'config', 'config.yaml')
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

_yaml_config = _load_yaml_config()

# 从 YAML 中获取配置，如果缺失则使用默认值
BROWSER = _yaml_config.get('browser', 'chrome')
BASE_URL = _yaml_config.get('base_url', 'https://www.saucedemo.com')
IMPLICITLY_WAIT = _yaml_config.get('implicitly_wait', 10)
EXPLICITLY_WAIT = _yaml_config.get('explicitly_wait', 10)
RERUNS = _yaml_config.get('reruns', 2)
RERUNS_DELAY = _yaml_config.get('reruns_delay', 1)

# 报告和日志路径
REPORT_PATH = os.path.join(BASE_PATH, "reports")
LOG_PATH = os.path.join(BASE_PATH, "logs")

# 确保目录存在
for path in [REPORT_PATH, LOG_PATH]:
    if not os.path.exists(path):
        os.makedirs(path)