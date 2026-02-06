import os
from pydantic_settings import BaseSettings
from typing import List
from pydantic import Field

class Settings(BaseSettings):
    # API 配置
    api_key: str = "sk-1cab26807b464ede94b5930079c515b7"
    base_url: str = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"
    model: str = "qwen-vl-max"
    
    # 文件路径配置
    # pdf_path: str = "data/model_doc.pdf"
    json_path: str = "data/question_to_content_mapping.json"
    
    # CORS 配置
    allowed_origins: List[str] = Field(
        default=["*"],
        description="CORS 允许的源列表"
    )
    
    class Config:
        env_file = ".env"

settings = Settings()

# 监管问题配置（保持不变）
REGULATORY_QUESTIONS = {
    1: "Does the documentation consistently adopt terminology defined in the Banking (Capital) Rules (BCR) and ensure all statements are unambiguous?",
    2: "Does it clearly specify the IRB adoption category to which the model applies and demonstrate compliance with the minimum usage requirements set out in Part 6 and Schedule 2 of the BCR?",
    3: "Is the model development logic economically sound, ensuring that identified risk factors are not driven by spurious or purely data-based correlations?",
    4: "Is the model type clearly defined, and are judgmental components governed by written guidelines specifying the rationale and weight allocation of risk factors?",
    5: "Does the development process incorporate relevant lending practices, recovery processes, and any recent changes in AI-driven credit decisioning?",
    6: "Does the development dataset include representative samples from both favourable and adverse economic periods, consistent with the cyclical requirements of the BCR?",
    7: "Are the control measures for the entire data lifecycle—covering collection, storage, retrieval, and deletion—clearly documented?",
    8: "Does the data quality assessment include quantitative indicators, and is it performed at least annually?",
    9: "Is the consistency of external or pooled data validated, and is its suitability reviewed at least once every 12 months?",
    10: "Are statistical treatments for missing values and outliers properly explained and methodologically sound?",
    11: "Is the Probability of Default (PD) estimation based on approved methodologies, with validated discriminatory power and calibration accuracy?",
    12: "Does the Loss Given Default (LGD) estimation incorporate downturn adjustments, employ compliant methodologies, and maintain appropriate conservatism?",
    13: "Does the Exposure at Default (EAD) estimation reflect current credit management practices, and is the chosen methodology well justified?",
    14: "For Low Default Portfolios (LDPs), are data augmentation techniques or benchmarking tools appropriately applied?",
    15: "Does model validation cover both quantitative and qualitative dimensions, and is it conducted at least annually?",
    16: "Are out-of-sample and out-of-time validations performed, with alternative approaches documented in cases of data limitations?",
    17: "Are internal tolerance thresholds defined for validation results, and are clear remediation actions specified for threshold breaches?",
    18: "Do the Board and senior management approve key model components and material changes, and do they receive regular performance reports?",
    19: "Are model validation and rating approval functions independent, and is the compliance of these processes reviewed annually by internal audit?",
    20: "Have third-party or group-level models undergone sufficient validation, with documentation disclosing methodological details and applicable boundaries?"
}