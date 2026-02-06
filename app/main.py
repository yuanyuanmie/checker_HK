from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import List, Optional
import time
import os

from app.config import settings, REGULATORY_QUESTIONS
from app.models import AnalysisResult, BatchAnalysisRequest, SingleAnalysisRequest
from app.services import RegulatoryAnalysisService
from app.utils import setup_logging, format_timestamp

# 设置日志
setup_logging()

# 创建 FastAPI 应用
app = FastAPI(
    title="监管合规分析 API",
    description="基于多模态AI的监管合规分析系统，支持HKMA Banking (Capital) Rules分析",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局服务实例
analysis_service = RegulatoryAnalysisService()


@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    print("监管合规分析 API 启动完成")


@app.get("/", summary="根路径")
async def root():
    """API 根路径"""
    return {
        "message": "监管合规分析 API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "single_analysis": "POST /analyze/single",
            "batch_analysis": "POST /analyze/batch",
            "questions": "GET /questions",
            "status": "GET /status"
        }
    }


@app.get("/status", summary="系统状态")
async def get_system_status():
    """获取系统运行状态"""
    return analysis_service.get_system_status()


@app.get("/questions", summary="获取所有监管问题")
async def get_all_questions():
    """获取所有20个监管问题的列表"""
    return {
        "total": len(REGULATORY_QUESTIONS),
        "questions": [
            {
                "qid": qid,
                "question": question,
                "has_context": str(qid) in analysis_service.question_contexts
            }
            for qid, question in REGULATORY_QUESTIONS.items()
        ]
    }


@app.post("/analyze/single", response_model=AnalysisResult, summary="分析单个问题")
async def analyze_single_question(request: SingleAnalysisRequest):
    """分析单个监管问题，返回大模型生成的结果"""
    if request.qid < 1 or request.qid > 20:
        raise HTTPException(status_code=400, detail="问题ID必须在1-20之间")

    result = analysis_service.analyze_single_question(request.qid)
    return AnalysisResult(**result)


@app.post("/analyze/batch", response_model=List[AnalysisResult], summary="批量分析问题")
async def analyze_batch_questions(request: BatchAnalysisRequest):
    """批量分析多个监管问题，返回大模型生成的结果列表"""
    # 验证问题ID
    invalid_qids = [qid for qid in request.qids if qid < 1 or qid > 20]
    if invalid_qids:
        raise HTTPException(
            status_code=400,
            detail=f"无效的问题ID: {invalid_qids}，必须在1-20之间"
        )

    # 如果未指定问题ID，分析所有问题
    qids_to_process = request.qids if request.qids else list(REGULATORY_QUESTIONS.keys())

    results = analysis_service.analyze_batch_questions(qids_to_process)
    return [AnalysisResult(**result) for result in results]


@app.get("/health", summary="健康检查")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "timestamp": format_timestamp()}

# 简化的服务类 (app/services.py)