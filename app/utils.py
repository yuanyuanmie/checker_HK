import logging
import time
import json
import os
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from loguru import logger


def setup_logging():
    """设置日志配置"""
    logger.add(
        "logs/regulatory_api.log",
        rotation="500 MB",
        retention="10 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )


def load_question_contexts(json_path: str) -> Dict[str, str]:
    """从 JSON 文件加载问题上下文映射"""
    try:
        if not os.path.exists(json_path):
            logger.warning(f"JSON file not found: {json_path}. Using default contexts.")
            return create_default_contexts()

        with open(json_path, "r", encoding="utf-8") as f:
            contexts = json.load(f)

        # 验证所有问题ID是否存在
        for qid in range(1, 21):
            if str(qid) not in contexts:
                logger.error(f"Missing context for question ID {qid} in JSON file.")
                raise ValueError(f"Missing context for question ID {qid}")

        return contexts
    except Exception as e:
        logger.error(f"Error loading question contexts: {str(e)}")
        return create_default_contexts()


def create_default_contexts() -> Dict[str, str]:
    """创建默认上下文（当JSON文件不存在时）"""
    return {str(i): f"Default context for question {i}" for i in range(1, 21)}


def format_timestamp() -> str:
    """格式化时间戳"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")