# checker_HK

An AI-driven regulatory compliance analysis system supporting HKMA Banking (Capital) Rules (BCR), with a focus on the Internal Ratings-Based (IRB) approach for credit risk.

## Features

- Multimodal AI analysis (text + document images)
- Pre-defined set of 20 HKMA regulatory questions
- Batch and single-question analysis of compliance documents in PDF format
- Detailed, structured response including findings, compliance status, recommendations, and remediation steps
- Easy-to-use FastAPI endpoints for integration

## Project Structure

- `app/main.py`: FastAPI server with API endpoints for analysis and system health
- `app/config.py`: Configuration and regulatory question definitions
- `app/models.py`: Pydantic models for API input/output schemas
- `app/services.py`: Core logic for processing documents and interacting with Qwen AI API
- `app/utils.py`: Utility functions (logging, context loading, timestamps)
- `data/question_to_content_mapping.json`: Regulatory question context references
- `.vscode/`, `.idea/`: Project and editor settings

## Requirements

- Python 3.10+
- FastAPI
- Pydantic
- fitz (PyMuPDF)
- requests
- loguru

(Install dependencies via `pip install -r requirements.txt` after adding a requirements file.)

## Usage

1. **Start the FastAPI server:**

   ```bash
   uvicorn app.main:app --reload

2. **API Endpoints:**
  GET /: API root with description and endpoints
  GET /status: Get system status
  GET /questions: Get all regulatory questions
  POST /analyze/single: Analyze one question (provide qid and pdf_path)
  POST /analyze/batch: Analyze multiple questions (provide qids and pdf_path)
  GET /health: Health check
