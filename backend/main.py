"""
SAAQ API - Main Application Entry Point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Literal
from datetime import datetime
import uuid

# Initialize FastAPI app
app = FastAPI(
    title="SAAQ API",
    description="SkillfullyAware Awareness Quotient - Developmental Diagnostic System",
    version="0.1.0"
)

# CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== DATA MODELS =====

class IntakeResponse(BaseModel):
    q_id: str
    question_text: str
    answer_text: str
    word_count: Optional[int] = None

    @validator('answer_text')
    def answer_not_empty(cls, v):
        if not v or len(v.strip()) < 10:
            raise ValueError('Answer must be at least 10 characters')
        return v

class IntakeSubmission(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    intake_version: Literal["forum-ready-15-v1", "master-29-v1"]
    responses: List[IntakeResponse]
    context: Optional[Dict] = {}

    @validator('responses')
    def validate_question_count(cls, v, values):
        version = values.get('intake_version')
        expected_count = 15 if version == "forum-ready-15-v1" else 29
        
        if len(v) != expected_count:
            raise ValueError(
                f'Expected {expected_count} responses for {version}, got {len(v)}'
            )
        return v

# ===== ENDPOINTS =====

@app.get("/")
def health_check():
    """API health check"""
    return {
        "status": "healthy",
        "service": "SAAQ API",
        "version": "0.1.0",
        "supported_intakes": ["forum-ready-15-v1", "master-29-v1"],
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "versions": "/api/v1/intake/versions",
            "submit": "/api/v1/intake/submit"
        }
    }

@app.get("/health")
def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "not_connected",  # TODO: Add DB check
        "nlp_engine": "not_loaded"     # TODO: Add NLP check
    }

@app.get("/api/v1/intake/versions")
async def list_intake_versions():
    """
    List available intake versions.
    Frontend uses this to show assessment options.
    """
    return {
        "versions": [
            {
                "id": "forum-ready-15-v1",
                "name": "SAAQ - EO Forum Intake",
                "description": "Streamlined 15-question intake for forums",
                "question_count": 15,
                "estimated_time": "20 minutes",
                "active": True
            },
            {
                "id": "master-29-v1",
                "name": "SA360 Full Assessment",
                "description": "Comprehensive 29-question diagnostic",
                "question_count": 29,
                "estimated_time": "30-40 minutes",
                "active": True
            }
        ]
    }

@app.post("/api/v1/intake/submit")
async def submit_intake(submission: IntakeSubmission):
    """
    Accept intake responses for either 15Q or 29Q version.
    Validates question count, stores in DB, enqueues scoring.
    """
    
    # Generate IDs
    intake_id = str(uuid.uuid4())
    user_id = submission.user_id or str(uuid.uuid4())
    
    # TODO: Store in database
    # TODO: Enqueue scoring job based on version
    
    print(f"📥 Received intake: {intake_id}")
    print(f"   Version: {submission.intake_version}")
    print(f"   Responses: {len(submission.responses)}")
    print(f"   User: {submission.first_name or 'Anonymous'}")
    
    return {
        "intake_id": intake_id,
        "user_id": user_id,
        "version": submission.intake_version,
        "status": "submitted",
        "expected_completion": "15-30 minutes",
        "message": f"Successfully received {len(submission.responses)} responses"
    }

@app.get("/api/v1/report/{report_id}")
async def get_report(report_id: str):
    """
    Retrieve generated report by ID.
    Returns HTML, PDF, or DOCX based on Accept header.
    """
    # TODO: Fetch from database
    # TODO: Return report or 404
    raise HTTPException(
        status_code=404, 
        detail=f"Report {report_id} not found. Report generation not yet implemented."
    )

# ===== ADMIN ENDPOINTS =====

@app.get("/api/v1/admin/intakes")
async def list_pending_intakes(status: Optional[str] = "pending"):
    """
    List intakes for admin review.
    Filters by status: pending, processing, completed, error
    """
    # TODO: Query database for intakes with given status
    return {
        "intakes": [],
        "count": 0,
        "status_filter": status
    }

# ===== RUN SERVER =====

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting SAAQ API...")
    print("📖 Docs: http://localhost:8000/docs")
    print("🏥 Health: http://localhost:8000/health")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)