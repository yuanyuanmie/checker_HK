import os
from pydantic_settings import BaseSettings
from typing import List, Dict

class Settings(BaseSettings):
    # API 配置
    api_key: str = "sk-1cab26807b464ede94b5930079c515b7"
    base_url: str = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"
    model: str = "qwen-vl-max"

    # 文件路径配置
    pdf_path: str = "data/model_doc.pdf"
    json_path: str = "data/question_to_content_mapping.json"

    class Config:
        env_file = ".env"


settings = Settings()

# 监管问题配置（保持不变）
REGULATORY_QUESTIONS = {
    1: "Does the documentation consistently adopt terminology defined in the Banking (Capital) Rules (BCR) and ensure all statements are unambiguous?",
    2: "Does it clearly specify the IRB adoption category to which the model applies and demonstrate compliance with the minimum usage requirements set out in Part 6 and Schedule 2 of the BCR?",
    # ... 其他问题保持不变
    20: "Have third-party or group-level models undergone sufficient validation, with documentation disclosing methodological details and applicable boundaries?"
}