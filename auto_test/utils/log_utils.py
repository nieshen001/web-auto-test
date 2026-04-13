# utils/log_utils.py
import logging
import os
from config.settings import LOG_PATH
from datetime import datetime

class LogUtils:
    @staticmethod
    def get_logger():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # 避免重复添加handler
        if not logger.handlers:
            # 控制台输出
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(console_format)
            logger.addHandler(console_handler)

            # 文件输出
            if not os.path.exists(LOG_PATH):
                os.makedirs(LOG_PATH)
            log_file = os.path.join(LOG_PATH, f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_format)
            logger.addHandler(file_handler)

        return logger