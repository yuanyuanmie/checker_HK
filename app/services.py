import base64
import os
import requests
import fitz
import time
from typing import List, Dict
from app.config import settings, REGULATORY_QUESTIONS
from app.utils import load_question_contexts, format_timestamp


class RegulatoryAnalysisService:
    def __init__(self):
        self.base64_images = None
        self.question_contexts = load_question_contexts(settings.json_path)
        self._initialize_pdf()

    def _initialize_pdf(self):
        """初始化PDF转换"""
        try:
            if not os.path.exists(settings.pdf_path):
                raise FileNotFoundError(f"PDF file not found: {settings.pdf_path}")

            self.base64_images = self._pdf_to_base64_images()
        except Exception as e:
            print(f"PDF initialization failed: {str(e)}")
            raise

    def _pdf_to_base64_images(self, dpi: int = 150) -> List[str]:
        """将 PDF 转换为 Base64 编码的图像列表"""
        doc = fitz.open(settings.pdf_path)
        total_pages = len(doc)

        base64_images = []
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=dpi)
            img_data = pix.tobytes("png")
            b64 = base64.b64encode(img_data).decode("utf-8")
            base64_images.append(b64)

        return base64_images

    def _call_qwen_api(self, question_text: str, base64_images: list, max_retries: int = 3) -> str:
        """调用多模态模型API（带重试机制）"""
        headers = {
            "Authorization": f"Bearer {settings.api_key}",
            "Content-Type": "application/json"
        }

        content = [{"type": "text", "text": question_text}]
        for b64 in base64_images:
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{b64}"}
            })

        data = {
            "model": settings.model,
            "messages": [{"role": "user", "content": content}],
            "max_tokens": 1500,
            "temperature": 0.3
        }

        for attempt in range(max_retries):
            try:
                response = requests.post(settings.base_url, headers=headers, json=data, timeout=60)
                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"]
                else:
                    print(f"Attempt {attempt + 1} failed: API Error {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")

            # 指数退避策略
            wait_time = 2 ** attempt
            time.sleep(wait_time)

        return f"Error: Failed after {max_retries} attempts"

    def _create_analysis_prompt(self, question_text: str, context_text: str) -> str:
        """创建分析提示词"""
        return (
            f"You are a senior regulatory compliance analyst specializing in HKMA's Banking (Capital) Rules (BCR), particularly the IRB approach for credit risk. "
            f"Analyze the provided document images and respond to the regulatory question with strict adherence to BCR requirements.\n\n"
            f"Regulatory Question:\n{question_text}\n\n"
            f"Reference Context:\n{context_text}\n\n"
            f"Provide a structured analysis in the following EXACT format (include all headings):\n\n"
            f"**Findings:**\n"
            f"- Describe specifically what the documentation contains or lacks regarding this requirement\n"
            f"- Identify any explicit mentions or omissions of key concepts\n"
            f"- For each finding, cite document location (e.g., 'Page 5, Section 2.3')\n"
            f"- Quote relevant sections where possible\n\n"
            f"**Compliance Status:**\n"
            f"- Explicitly state if documentation complies with BCR Article 123.4 regarding model transparency\n"
            f"- Assess overall compliance (compliant/partially compliant/non-compliant)\n"
            f"- Summarize the core reason (1-2 sentences)\n\n"
            f"**Recommendation:**\n"
            f"- Suggest specific improvements if non-compliant\n"
            f"- Recommend additional documentation needed\n"
            f"- Reference relevant BCR articles (e.g., 'BCR Schedule 2 §1(e)')\n"
            f"- Distinguish between immediate fixes and long-term enhancements\n\n"
            f"**Actionable Steps for Remediation:**\n"
            f"- Numbered list of concrete tasks (assignable to teams)\n"
            f"- Include timeline estimates (e.g., '30 days')\n"
            f"- Mention regulatory engagement steps (e.g., 'Submit to HKMA for pre-approval')\n\n"
            f"Maintain a formal, evidence-based tone. Avoid speculation; only use facts from the document and BCR. "
            f"Prioritize clarity and traceability in all sections."
        )

    def analyze_single_question(self, qid: int) -> Dict:
        """分析单个问题，返回大模型结果"""
        start_time = time.time()

        try:
            if qid not in REGULATORY_QUESTIONS:
                raise ValueError(f"Invalid question ID: {qid}")

            question_text = REGULATORY_QUESTIONS[qid]
            context_text = self.question_contexts.get(str(qid), "Context not available")

            prompt = self._create_analysis_prompt(question_text, context_text)
            answer = self._call_qwen_api(prompt, self.base64_images)

            processing_time = time.time() - start_time

            return {
                "qid": qid,
                "question": question_text,
                "context": context_text,
                "answer": answer,  # 这里就是大模型生成的完整分析结果
                "status": "success",
                "processing_time": round(processing_time, 2),
                "timestamp": format_timestamp()
            }
        except Exception as e:
            processing_time = time.time() - start_time
            return {
                "qid": qid,
                "question": REGULATORY_QUESTIONS.get(qid, "Unknown"),
                "context": self.question_contexts.get(str(qid), "Context not available"),
                "answer": f"Error: {str(e)}",  # 错误信息也直接返回
                "status": "failed",
                "processing_time": round(processing_time, 2),
                "timestamp": format_timestamp()
            }

    def analyze_batch_questions(self, qids: List[int]) -> List[Dict]:
        """批量分析问题，返回大模型结果列表"""
        results = []
        for qid in qids:
            if qid not in REGULATORY_QUESTIONS:
                print(f"Invalid question ID: {qid}")
                continue
            result = self.analyze_single_question(qid)
            results.append(result)
        return results

    def get_system_status(self) -> Dict:
        """获取系统状态"""
        return {
            "pdf_loaded": self.base64_images is not None,
            "total_questions": len(REGULATORY_QUESTIONS),
            "processed_questions": 0,
            "api_status": "ready",
            "last_update": format_timestamp()
        }