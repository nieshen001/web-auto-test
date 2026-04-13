# utils/config_utils.py
import yaml
import os
from config.settings import BASE_PATH

def load_yaml_config():
    """加载 config/config.yaml 文件，返回字典"""
    yaml_path = os.path.join(BASE_PATH, 'config', 'config.yaml')
    with open(yaml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config