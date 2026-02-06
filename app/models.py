from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class QuestionStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"

class AnalysisResult(BaseModel):
    qid: int
    question: str
    context: str
    answer: str  # 大模型生成的完整分析结果
    status: QuestionStatus
    processing_time: Optional[float] = None
    timestamp: Optional[str] = None

class BatchAnalysisRequest(BaseModel):
    qids: List[int] = Field(default_factory=list, description="要处理的问题ID列表，空数组表示处理所有问题")

class SingleAnalysisRequest(BaseModel):
    qid: int = Field(..., description="问题ID (1-20)")