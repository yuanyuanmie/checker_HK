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
    answer: str
    status: QuestionStatus
    processing_time: Optional[float] = None
    timestamp: Optional[str] = None
    pdf_path: Optional[str] = None  # ← 新增

class SingleAnalysisRequest(BaseModel):
    qid: int = Field(..., description="问题ID (1-20)")
    pdf_path: str = Field(..., description="PDF 文件路径")  # ← 新增

class BatchAnalysisRequest(BaseModel):
    qids: List[int] = Field(default_factory=list, description="要处理的问题ID列表，空数组表示处理所有问题")
    pdf_path: str = Field(..., description="PDF 文件路径")  # ← 新增